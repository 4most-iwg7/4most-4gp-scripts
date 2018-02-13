#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Take a library of spectra, perhaps generated by Turbospectrum, and pass them through 4FS.
"""

import argparse
import os
from os import path as os_path
import hashlib
import time
import re
import logging

from fourgp_speclib import SpectrumLibrarySqlite
from fourgp_fourfs import FourFS

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(filename)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

# Read input parameters
our_path = os_path.split(os_path.abspath(__file__))[0]
root_path = os_path.join(our_path, "..", "..")
pid = os.getpid()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-library',
                    required=False,
                    default="demo_stars",
                    dest="input_library",
                    help="Specify the name of the SpectrumLibrary we are to read input spectra from.")
parser.add_argument('--output-library-lrs',
                    required=False,
                    default="4fs_demo_stars_lrs",
                    dest="output_library_lrs",
                    help="Specify the name of the SpectrumLibrary we are to feed synthesized LRS spectra into.")
parser.add_argument('--output-library-hrs',
                    required=False,
                    default="4fs_demo_stars_hrs",
                    dest="output_library_hrs",
                    help="Specify the name of the SpectrumLibrary we are to feed synthesized HRS spectra into.")
parser.add_argument('--workspace', dest='workspace', default="",
                    help="Directory where we expect to find spectrum libraries.")
parser.add_argument('--snr-definition',
                    action="append",
                    dest="snr_definitions",
                    help="Specify a way of defining SNR, in the form 'name,minimum,maximum', meaning we calculate the "
                         "median SNR per pixel between minimum and maximum wavelengths in Angstrom.")
parser.add_argument('--snr-list',
                    required=False,
                    default="10,20,50,80,100,130,180,250,500",
                    dest="snr_list",
                    help="Specify a comma-separated list of the SNRs that 4FS is to degrade spectra to.")
parser.add_argument('--mag-list',
                    required=False,
                    default="15",
                    dest="mag_list",
                    help="Specify a comma-separated list of the r' band magnitudes to pass to 4FS.")
parser.add_argument('--snr-definitions-lrs',
                    required=False,
                    default="",
                    dest="snr_definitions_lrs",
                    help="Specify the SNR definitions to use for the R, G and B bands of 4MOST LRS.")
parser.add_argument('--snr-definitions-hrs',
                    required=False,
                    default="",
                    dest="snr_definitions_hrs",
                    help="Specify the SNR definitions to use for the R, G and B bands of 4MOST HRS.")
parser.add_argument('--binary-path',
                    required=False,
                    default=root_path,
                    dest="binary_path",
                    help="Specify a directory where 4FS package is installed.")
parser.add_argument('--create',
                    required=False,
                    action='store_true',
                    dest="create",
                    help="Create a clean SpectrumLibrary to feed synthesized spectra into")
parser.add_argument('--no-create',
                    required=False,
                    action='store_false',
                    dest="create",
                    help="Do not create a clean SpectrumLibrary to feed synthesized spectra into")
parser.set_defaults(create=True)
parser.add_argument('--log-file',
                    required=False,
                    default="/tmp/fourfs_apokasc_{}.log".format(pid),
                    dest="log_to",
                    help="Specify a log file where we log our progress.")
args = parser.parse_args()

logger.info("Running 4FS on spectra with arguments <{}> <{}> <{}>".format(args.input_library,
                                                                          args.output_library_lrs,
                                                                          args.output_library_hrs))

# Set path to workspace where we create libraries of spectra
workspace = args.workspace if args.workspace else os_path.join(our_path, "..", "workspace")
os.system("mkdir -p {}".format(workspace))


# Helper for opening input SpectrumLibrary(s)
def open_input_libraries(library_spec):
    test = re.match("([^\[]*)\[(.*)\]$", library_spec)
    constraints = {"continuum_normalised": 0}
    if test is None:
        library_name = library_spec
    else:
        library_name = test.group(1)
        for constraint in test.group(2).split(","):
            words_1 = constraint.split("=")
            words_2 = constraint.split("<")
            if len(words_1) == 2:
                constraint_name = words_1[0]
                try:
                    constraint_value = float(words_1[1])
                except ValueError:
                    constraint_value = words_1[1]
                constraints[constraint_name] = constraint_value
            elif len(words_2) == 3:
                constraint_name = words_2[1]
                try:
                    constraint_value_a = float(words_2[0])
                    constraint_value_b = float(words_2[2])
                except ValueError:
                    constraint_value_a = words_2[0]
                    constraint_value_b = words_2[2]
                constraints[constraint_name] = (constraint_value_a, constraint_value_b)
            else:
                assert False, "Could not parse constraint <{}>".format(constraint)
    library_path = os_path.join(workspace, library_name)
    input_library = SpectrumLibrarySqlite(path=library_path, create=False)
    library_items = input_library.search(**constraints)
    return {
        "library": input_library,
        "items": library_items,
        "constraints": constraints
    }


# Open input SpectrumLibrary
spectra = open_input_libraries(args.input_library)
input_library, input_spectra_ids, input_spectra_constraints = [spectra[i] for i in ("library", "items", "constraints")]

# Create new SpectrumLibrary
output_libraries = {}

for mode in ({"name": "LRS", "library": args.output_library_lrs},
             {"name": "HRS", "library": args.output_library_hrs}):
    library_name = re.sub("/", "_", mode['library'])
    library_path = os_path.join(workspace, library_name)
    output_libraries[mode['name']] = SpectrumLibrarySqlite(path=library_path, create=args.create)

# Definitions of SNR
if (args.snr_definitions is None) or (len(args.snr_definitions) < 1):
    snr_definitions = None
else:
    snr_definitions = []
    for snr_definition in args.snr_definitions:
        words = snr_definition.split(",")
        snr_definitions.append([words[0], float(words[1]), float(words[2])])

if len(args.snr_definitions_lrs) < 1:
    snr_definitions_lrs = None
else:
    snr_definitions_lrs = args.snr_definitions_lrs.split(",")
    assert len(snr_definitions_lrs) == 3

if len(args.snr_definitions_hrs) < 1:
    snr_definitions_hrs = None
else:
    snr_definitions_hrs = args.snr_definitions_hrs.split(",")
    assert len(snr_definitions_hrs) == 3

snr_list = [float(item.strip()) for item in args.snr_list.split(",")]

mag_list = [float(item.strip()) for item in args.mag_list.split(",")]

# Loop over spectra to process
with open(args.log_to, "w") as result_log:
    for magnitude in mag_list:

        # Instantiate 4FS wrapper
        etc_wrapper = FourFS(
            path_to_4fs=os_path.join(args.binary_path, "OpSys/ETC"),
            snr_definitions=snr_definitions,
            magnitude=magnitude,
            lrs_use_snr_definitions=snr_definitions_lrs,
            hrs_use_snr_definitions=snr_definitions_hrs,
            snr_list=snr_list
        )

        for input_spectrum_id in input_spectra_ids:
            logger.info("Working on <{}>".format(input_spectrum_id['filename']))
            # Open Spectrum data from disk
            input_spectrum_array = input_library.open(ids=input_spectrum_id['specId'])
            input_spectrum = input_spectrum_array.extract_item(0)

            # Look up the name of the star we've just loaded
            spectrum_matching_field = 'uid' if 'uid' in input_spectrum.metadata else 'Starname'
            object_name = input_spectrum.metadata[spectrum_matching_field]

            # Write log message
            result_log.write("\n[{}] {}... ".format(time.asctime(), object_name))
            result_log.flush()

            # Search for the continuum-normalised version of this same object
            search_criteria = input_spectra_constraints.copy()
            search_criteria[spectrum_matching_field] = object_name
            search_criteria['continuum_normalised'] = 1
            continuum_normalised_spectrum_id = input_library.search(**search_criteria)

            # Check that continuum-normalised spectrum exists
            assert len(continuum_normalised_spectrum_id) == 1, "Could not find continuum-normalised spectrum."

            # Load the continuum-normalised version
            input_spectrum_continuum_normalised_arr = input_library.open(
                ids=continuum_normalised_spectrum_id[0]['specId'])
            input_spectrum_continuum_normalised = input_spectrum_continuum_normalised_arr.extract_item(0)

            # Process spectra through 4FS
            degraded_spectra = etc_wrapper.process_spectra(
                spectra_list=((input_spectrum, input_spectrum_continuum_normalised),)
            )

            # Import degraded spectra into output spectrum library
            for mode in degraded_spectra:
                for index in degraded_spectra[mode]:
                    for snr in degraded_spectra[mode][index]:
                        unique_id = hashlib.md5(os.urandom(32).encode("hex")).hexdigest()[:16]
                        for spectrum_type in degraded_spectra[mode][index][snr]:
                            output_libraries[mode].insert(spectra=degraded_spectra[mode][index][snr][spectrum_type],
                                                          filenames=input_spectrum_id['filename'],
                                                          metadata_list={"uid": unique_id})

        # Clean up 4FS
        etc_wrapper.close()
