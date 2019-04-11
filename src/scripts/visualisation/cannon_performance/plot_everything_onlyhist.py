#!../../../../../virtualenv/bin/python3
# -*- coding: utf-8 -*-

# NB: The shebang line above assumes you've installed a python virtual environment alongside your working copy of the
# <4most-4gp-scripts> git repository. It also only works if you invoke this python script from the directory where it
# is located. If these two assumptions are incorrect (e.g. you're using Conda), you can still use this script by typing
# <python plot_everything.py>, but <./plot_everything.py> will not work.

"""
This script looks in the directory <4most-4gp-scripts/output_data/cannon> to see what tests you've run through the
Cannon and plots up the results automatically.
"""

import glob
import gzip
import json
import logging
import re
from os import path as os_path

from lib import plot_settings
from lib.batch_processor import BatchProcessor
from lib.label_information import LabelInformation

# Create logger
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(filename)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

# Set path to workspace where we expect to find libraries of spectra
our_path = os_path.split(os_path.abspath(__file__))[0]
cannon_output_dir = os_path.join(our_path, "../../../../output_data/cannon")

# Create a long list of all the shell commands we want to run
batch = BatchProcessor(logger=logger,
                       output_path=os_path.join(our_path, "../../../../output_plots/cannon_performance")
                       )

# We run most jobs for both 4MOST LRS and HRS
modes_4most = ["hrs", "lrs"]

offset_scripts = [#"offset_box_and_whisker.py",
                  #"offset_correlation_scatter_plot.py",
                  "offset_histogram.py",
                  #"offset_rms.py"
                  ]



# Now plot performance vs SNR for every Cannon run we have
cannon_json_summaries = sorted(glob.glob(os_path.join(cannon_output_dir, "*.summary.json.gz")))
for i, cannon_json_summary in enumerate(cannon_json_summaries):

    # Keep user updated on progress
    logger.info("{:4d}/{:4d} Working out jobs for <{}>".format(i + 1, len(cannon_json_summaries), cannon_json_summary))

    # Extract name of Cannon run from filename
    test = re.match(os_path.join(cannon_output_dir, r"(.*).summary.json.gz"), cannon_json_summary)
    cannon_run_name = test.group(1)
    cannon_run_file_stub = os_path.join(cannon_output_dir, cannon_run_name)

    # Produce a plot of precision vs SNR
    for offset_script in offset_scripts:
        batch.register_job(script=offset_script,
                           output="{plots_path}/{cannon_run_name}",
                           arguments={
                               "cannon-output": cannon_run_file_stub
                           },
                           substitutions={
                               "cannon_run_name": cannon_run_name,
                               "plots_path": "performance_vs_label"
                           }
                           )
    continue
    # Produce a scatter plot of the nominal uncertainties in the Cannon's label estimates
    batch.register_job(script="scatter_plot_cannon_uncertainty.py",
                       output="{plots_path}/{cannon_run_name}",
                       arguments={"cannon-output": cannon_run_file_stub},
                       substitutions={
                           "cannon_run_name": cannon_run_name,
                           "plots_path": "performance_vs_label"
                       }
                       )

    # Now produce scatter plots of the SNR required to achieve the target precision in each label for each star
    label_metadata = LabelInformation().label_metadata
    cannon_output_data = json.loads(gzip.open(cannon_json_summary, "rt").read())
    label_names = [item for item in cannon_output_data['labels'] if item in label_metadata]
    for colour_by_label in label_names:
        # Figure out the target precision for each label, and units
        target_accuracy = label_metadata[colour_by_label]['targets'][0]
        target_unit = label_metadata[colour_by_label]['unit']

        # Produce a version of each label which is safe to put in the filename of a file
        path_safe_label = re.sub(r"\[(.*)/H\]", r"\g<1>", colour_by_label)

        # required_snrA
        # Scatter plots of required SNR in the Teff / log(g) plane
        batch.register_job(script="scatter_plot_snr_required.py",
                           output="{plots_path}/{cannon_run_name}/{path_safe_label}",
                           arguments={
                               "label": ["Teff{{7000:3400}}", "logg{{5:0}}"],
                               "colour-by-label": "{}{{{{:}}}}".format(colour_by_label),
                               "target-accuracy": target_accuracy,
                               "colour-range-min": 30,
                               "colour-range-max": 120,
                               "cannon-output": cannon_run_file_stub,
                               "accuracy-unit": target_unit
                           },
                           substitutions={
                               "cannon_run_name": cannon_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "required_snrA"
                           }
                           )

        # required_snrB
        # Scatter plots of required SNR in the metallicity / log(g) plane
        batch.register_job(script="scatter_plot_snr_required.py",
                           output="{plots_path}/{cannon_run_name}/{path_safe_label}",
                           arguments={
                               "label": ["[Fe/H]{{1:-3}}", "logg{{5:0}}"],
                               "colour-by-label": "{}{{{{:}}}}".format(colour_by_label),
                               "target-accuracy": target_accuracy,
                               "colour-range-min": 30,
                               "colour-range-max": 120,
                               "cannon-output": cannon_run_file_stub,
                               "accuracy-unit": target_unit
                           },
                           substitutions={
                               "cannon_run_name": cannon_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "required_snrB"
                           }
                           )

        # label_offsets/A_*
        # Scatter plots of the absolute offsets in each label, in the Teff / log(g) plane
        batch.register_job(script="scatter_plot_coloured.py",
                           output="{plots_path}/{cannon_run_name}/A_{path_safe_label}",
                           arguments={
                               "label": ["Teff{{7000:3400}}", "logg{{5:0}}"],
                               "colour-by-label": "{0}{{{{{1}:{2}}}}}".format(colour_by_label,
                                                                              -3 * target_accuracy,
                                                                              3 * target_accuracy),
                               "cannon-output": cannon_run_file_stub
                           },
                           substitutions={
                               "cannon_run_name": cannon_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "label_offsets"
                           }
                           )

        # label_offsets/B_*
        # Scatter plots of the absolute offsets in each label, in the [Fe/H] / log(g) plane
        batch.register_job(script="scatter_plot_coloured.py",
                           output="{plots_path}/{cannon_run_name}/B_{path_safe_label}",
                           arguments={
                               "label": ["[Fe/H]{{1:-3}}", "logg{{5:0}}"],
                               "colour-by-label": "{0}{{{{{1}:{2}}}}}".format(colour_by_label,
                                                                              -3 * target_accuracy,
                                                                              3 * target_accuracy),
                               "cannon-output": cannon_run_file_stub
                           },
                           substitutions={
                               "cannon_run_name": cannon_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "label_offsets"
                           }
                           )

# If we are not overwriting plots we've already made, then check which files already exist
if not plot_settings.overwrite_plots:
    batch.filter_jobs_where_products_already_exist()

# Report how many plots need making afresh
batch.report_status()
batch.list_shell_commands_to_file("plotting.log")

# Now run the shell commands
batch.run_jobs()
