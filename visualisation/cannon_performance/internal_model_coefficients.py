#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Take an output file from the Cannon, and plot the Cannon's predictive model coefficients.
"""

import os
from os import path as os_path
import argparse
import re
import json
import numpy as np

from operator import itemgetter

from fourgp_speclib import SpectrumLibrarySqlite
from fourgp_cannon import CannonInstance


def dict_merge(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


# Read input parameters
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--label', default="Teff", dest='label',
                    help="The label we should vary.")
parser.add_argument('--cannon-output',
                    default="../../output_data/cannon/cannon_galah_hrs_10label",
                    dest='cannon',
                    help="Cannon output file we should analyse.")
parser.add_argument('--output-stub', default="/tmp/cannon_model_", dest='output_stub',
                    help="Data file to write output to.")
args = parser.parse_args()

# Set path to workspace where we expect to find libraries of spectra
our_path = os_path.split(os_path.abspath(__file__))[0]
workspace = os_path.join(our_path, "..", "..", "workspace")

# Fetch title for this Cannon run
cannon_output = json.loads(open(args.cannon + ".json").read())
description = cannon_output['description']

# Open spectrum library we originally trained the Cannon on
training_spectra_info = SpectrumLibrarySqlite.open_and_search(
    library_spec=cannon_output["train_library"],
    workspace=workspace,
    extra_constraints={"continuum_normalised": 1}
)

training_library, training_library_items = [training_spectra_info[i] for i in ("library", "items")]

# Load training set
training_library_ids = [i["specId"] for i in training_library_items]
training_spectra = training_library.open(ids=training_library_ids)

# Recreate a Cannon instance, using the saved state
censoring_masks = cannon_output["censoring_mask"]
if censoring_masks is not None:
    for key, value in censoring_masks.iteritems():
        censoring_masks[key] = np.asarray(value)

model = CannonInstance(training_set=training_spectra,
                       load_from_file=args.cannon + ".cannon",
                       label_names=cannon_output["labels"],
                       censors=censoring_masks,
                       threads=None
                       )

