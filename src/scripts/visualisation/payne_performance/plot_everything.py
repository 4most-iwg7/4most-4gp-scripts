#!../../../../../virtualenv/bin/python3
# -*- coding: utf-8 -*-

# NB: The shebang line above assumes you've installed a python virtual environment alongside your working copy of the
# <4most-4gp-scripts> git repository. It also only works if you invoke this python script from the directory where it
# is located. If these two assumptions are incorrect (e.g. you're using Conda), you can still use this script by typing
# <python plot_everything.py>, but <./plot_everything.py> will not work.

"""
This script looks in the directory <4most-4gp-scripts/output_data/payne> to see what tests you've run through the
payne and plots up the results automatically.
"""

import glob
import gzip
import json
import logging
import re
import sys
from os import path as os_path

sys.path.append('../cannon_performance/')
from lib import plot_settings
from lib.batch_processor import BatchProcessor
from lib.label_information import LabelInformation


# Create logger
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(filename)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

# Set path to workspace where we expect to find libraries of spectra
our_path = os_path.split(os_path.abspath(__file__))[0]
payne_output_dir = os_path.join(our_path, "../../../../output_data/payne")

# Create a long list of all the shell commands we want to run
batch = BatchProcessor(logger=logger,
                       output_path=os_path.join(our_path, "../../../../output_plots/payne_performance")
                       )

# We run most jobs for both 4MOST LRS and HRS
modes_4most = ["hrs", "lrs"]

offset_scripts = ["../cannon_performance/offset_box_and_whisker.py",
                  "../cannon_performance/offset_correlation_scatter_plot.py",
                  "../cannon_performance/offset_histogram.py",
                  "../cannon_performance/offset_rms.py"
                  ]

# comparison_censoring_schemes_*
# Create plots of the relative performance of the 4 censoring schemes, trained and tested on UVES or GALAH
for mode in modes_4most:
    for sample in ["galah"]:
        for offset_script in offset_scripts:
            batch.register_job(script=offset_script,
                               output="{plots_path}/comparison_censoring_schemes_{sample}_{mode}",
                               arguments={
                                   "cannon-output": ["{data_path}/payne_{sample}_{mode}_10label",
                                                     "{data_path}/payne_{sample}_censored_{mode}_10label",
                                                     "{data_path}/payne_{sample}_censored2_{mode}_10label",
                                                     "{data_path}/payne_{sample}_censored3_{mode}_10label"
                                                     ],
                                   "dataset-label": ["No censoring",
                                                     "Censoring scheme 1",
                                                     "Censoring scheme 2",
                                                     "Censoring scheme 3"
                                                     ],
                                   "dataset-colour": ["green", "blue", "red", "purple"]
                               },
                               substitutions={"mode": mode,
                                              "sample": sample,
                                              "data_path": payne_output_dir,
                                              "plots_path": "performance_vs_label"}
                               )

# comparison_low_z_*
# Create a plot of the performance of the payne, when trained and tested on the [Fe/H] < -1 and [Fe/H] > 1 regimes
# separately
for mode in modes_4most:
    for sample in ["galah"]:
        for offset_script in offset_scripts:
            batch.register_job(script=offset_script,
                               output="{plots_path}/comparison_low_z_{sample}_{mode}",
                               arguments={
                                   "cannon-output": ["{data_path}/payne_{sample}_fehcut2_{mode}_10label",
                                                     "{data_path}/payne_{sample}_{mode}_10label"
                                                     ],
                                   "dataset-filter": ["[Fe/H]<-1", "[Fe/H]<-1"],
                                   "dataset-label": ["Trained \$z<-1\$ only", "Trained on full sample"],
                                   "dataset-colour": ["green", "red"]
                               },
                               substitutions={"mode": mode,
                                              "sample": sample,
                                              "data_path": payne_output_dir,
                                              "plots_path": "performance_vs_label"}
                               )

# comparisonA -- Plot the performance of the payne for different types of stars -- giants and dwarfs, metal rich and
# metal poor
for mode in modes_4most:
    for sample in ["galah"]:
        for divisor in ["h", "fe"]:
            for offset_script in offset_scripts:
                batch.register_job(script=offset_script,
                                   output="{plots_path}/comparisonA_{sample}_{mode}_{divisor}",
                                   arguments={
                                       "cannon-output":
                                           ["{data_path}/payne_{sample}_censored_{mode}_10label"] * 8,
                                       "dataset-filter": ["logg<3.25;[Fe/H]>0;[Fe/H]<1",
                                                          "logg>3.25;[Fe/H]>0;[Fe/H]<1",
                                                          "logg<3.25;[Fe/H]>-0.5;[Fe/H]<0",
                                                          "logg>3.25;[Fe/H]>-0.5;[Fe/H]<0",
                                                          "logg<3.25;[Fe/H]>-1;[Fe/H]<-0.5",
                                                          "logg>3.25;[Fe/H]>-1;[Fe/H]<-0.5",
                                                          "logg<3.25;[Fe/H]>-2;[Fe/H]<-1",
                                                          "logg>3.25;[Fe/H]>-2;[Fe/H]<-1"],
                                       "dataset-label": ["Giants; [Fe/H]\$>0\$",
                                                         "Dwarfs; [Fe/H]\$>0\$",
                                                         "Giants; \$-0.5<\$[Fe/H]\$<0\$",
                                                         "Dwarfs; \$-0.5<\$[Fe/H]\$<0\$",
                                                         "Giants; \$-1<\$[Fe/H]$<-0.5$",
                                                         "Dwarfs; \$-1<\$[Fe/H]$<-0.5$",
                                                         "Giants; [Fe/H]$<-1$",
                                                         "Dwarfs; [Fe/H]$<-1$"],
                                       "dataset-colour": ["purple", "magenta", "blue", "red",
                                                          "cyan", "orange", "green", "brown"],
                                       "dataset-line-type": [1] * 8,
                                       "abundances-over-{divisor}": None
                                   },
                                   substitutions={"mode": mode,
                                                  "sample": sample,
                                                  "divisor": divisor,
                                                  "data_path": payne_output_dir,
                                                  "plots_path": "performance_vs_label"}
                                   )

# comparisonB -- Plot the performance of the payne when fitting 3 or 10 parameters
for mode in modes_4most:
    for sample in ["galah"]:
        for divisor in ["h", "fe"]:
            for censoring in ["", "_censored"]:
                for offset_script in offset_scripts:
                    batch.register_job(script=offset_script,
                                       output="{plots_path}/comparisonB_{sample}{censoring}_{mode}_{divisor}",
                                       arguments={
                                           "cannon-output": [
                                               "{data_path}/payne_{sample}{censoring}_{mode}_3label",
                                               "{data_path}/payne_{sample}{censoring}_{mode}_4label",
                                               "{data_path}/payne_{sample}{censoring}_{mode}_5label",
                                               "{data_path}/payne_{sample}{censoring}_{mode}_10label",
                                               "{data_path}/payne_{sample}{censoring}_{mode}_12label"
                                           ],
                                           "dataset-label": ["3 parameter; uncensored",
                                                             "4 parameter; uncensored",
                                                             "5 parameter; uncensored",
                                                             "10 parameters; uncensored",
                                                             "12 parameters; uncensored"],
                                           "dataset-colour": ["green", "blue", "orange", "red", "purple"],
                                           "dataset-line-type": [1] * 5,
                                           "abundances-over-{divisor}": None
                                       },
                                       substitutions={"mode": mode,
                                                      "sample": sample,
                                                      "censoring": censoring,
                                                      "divisor": divisor,
                                                      "data_path": payne_output_dir,
                                                      "plots_path": "performance_vs_label"}
                                       )

# Now plot performance vs SNR for every payne run we have
payne_json_summaries = sorted(glob.glob(os_path.join(payne_output_dir, "*.summary.json.gz")))
for i, payne_json_summary in enumerate(payne_json_summaries):

    # Keep user updated on progress
    logger.info("{:4d}/{:4d} Working out jobs for <{}>".format(i + 1, len(payne_json_summaries), payne_json_summary))

    # Extract name of payne run from filename
    test = re.match(os_path.join(payne_output_dir, r"(.*).summary.json.gz"), payne_json_summary)
    payne_run_name = test.group(1)
    payne_run_file_stub = os_path.join(payne_output_dir, payne_run_name)

    # Produce a plot of precision vs SNR
    for offset_script in offset_scripts:
        batch.register_job(script=offset_script,
                           output="{plots_path}/{payne_run_name}",
                           arguments={
                               "cannon-output": payne_run_file_stub
                           },
                           substitutions={
                               "payne_run_name": payne_run_name,
                               "plots_path": "performance_vs_label"
                           }
                           )

    # Produce a scatter plot of the nominal uncertainties in the payne's label estimates
    batch.register_job(script="../cannon_performance/scatter_plot_cannon_uncertainty.py",
                       output="{plots_path}/{payne_run_name}",
                       arguments={"cannon-output": payne_run_file_stub},
                       substitutions={
                           "payne_run_name": payne_run_name,
                           "plots_path": "performance_vs_label"
                       }
                       )

    # Now produce scatter plots of the SNR required to achieve the target precision in each label for each star
    label_metadata = LabelInformation().label_metadata
    payne_output_data = json.loads(gzip.open(payne_json_summary, "rt").read())
    label_names = [item for item in payne_output_data['labels'] if item in label_metadata]
    for colour_by_label in label_names:
        # Figure out the target precision for each label, and units
        target_accuracy = label_metadata[colour_by_label]['targets'][0]
        target_unit = label_metadata[colour_by_label]['unit']

        # Produce a version of each label which is safe to put in the filename of a file
        path_safe_label = re.sub(r"\[(.*)/H\]", r"\g<1>", colour_by_label)

        # required_snrA
        # Scatter plots of required SNR in the Teff / log(g) plane
        batch.register_job(script="../cannon_performance/scatter_plot_snr_required.py",
                           output="{plots_path}/{payne_run_name}/{path_safe_label}",
                           arguments={
                               "label": ["Teff{{7000:3400}}", "logg{{5:0}}"],
                               "colour-by-label": "{}{{{{:}}}}".format(colour_by_label),
                               "target-accuracy": target_accuracy,
                               "colour-range-min": 30,
                               "colour-range-max": 120,
                               "cannon-output": payne_run_file_stub,
                               "accuracy-unit": target_unit
                           },
                           substitutions={
                               "payne_run_name": payne_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "required_snrA"
                           }
                           )

        # required_snrB
        # Scatter plots of required SNR in the metallicity / log(g) plane
        batch.register_job(script="../cannon_performance/scatter_plot_snr_required.py",
                           output="{plots_path}/{payne_run_name}/{path_safe_label}",
                           arguments={
                               "label": ["[Fe/H]{{1:-3}}", "logg{{5:0}}"],
                               "colour-by-label": "{}{{{{:}}}}".format(colour_by_label),
                               "target-accuracy": target_accuracy,
                               "colour-range-min": 30,
                               "colour-range-max": 120,
                               "cannon-output": payne_run_file_stub,
                               "accuracy-unit": target_unit
                           },
                           substitutions={
                               "payne_run_name": payne_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "required_snrB"
                           }
                           )

        # label_offsets/A_*
        # Scatter plots of the absolute offsets in each label, in the Teff / log(g) plane
        batch.register_job(script="../cannon_performance/scatter_plot_coloured.py",
                           output="{plots_path}/{payne_run_name}/A_{path_safe_label}",
                           arguments={
                               "label": ["Teff{{7000:3400}}", "logg{{5:0}}"],
                               "colour-by-label": "{0}{{{{{1}:{2}}}}}".format(colour_by_label,
                                                                              -3 * target_accuracy,
                                                                              3 * target_accuracy),
                               "cannon-output": payne_run_file_stub
                           },
                           substitutions={
                               "payne_run_name": payne_run_name,
                               "path_safe_label": path_safe_label,
                               "plots_path": "label_offsets"
                           }
                           )

        # label_offsets/B_*
        # Scatter plots of the absolute offsets in each label, in the [Fe/H] / log(g) plane
        batch.register_job(script="../cannon_performance/scatter_plot_coloured.py",
                           output="{plots_path}/{payne_run_name}/B_{path_safe_label}",
                           arguments={
                               "label": ["[Fe/H]{{1:-3}}", "logg{{5:0}}"],
                               "colour-by-label": "{0}{{{{{1}:{2}}}}}".format(colour_by_label,
                                                                              -3 * target_accuracy,
                                                                              3 * target_accuracy),
                               "cannon-output": payne_run_file_stub
                           },
                           substitutions={
                               "payne_run_name": payne_run_name,
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
