#!../../../../virtualenv/bin/python2.7
# -*- coding: utf-8 -*-

# NB: The shebang line above assumes you've installed a python virtual environment alongside your working copy of the
# <4most-4gp-scripts> git repository. It also only works if you invoke this python script from the directory where it
# is located. If these two assumptions are incorrect (e.g. you're using Conda), you can still use this script by typing
# <python mean_performance_vs_label.py>, but <./mean_performance_vs_label.py> will not work.

"""
Plot results of testing the Cannon against noisy test spectra, to see how well it reproduces stellar labels.
"""

import os
from os import path as os_path
import re
import numpy as np
import json

from lib.pyxplot_driver import PyxplotDriver
from lib.label_information import LabelInformation
from lib.abscissa_information import AbcissaInformation
from lib.compute_cannon_offsets import CannonAccuracyCalculator

from offset_cmd_line_interface import fetch_command_line_arguments


def generate_correlation_scatter_plots(data_sets, abscissa_label, assume_scaled_solar,
                                       compare_against_reference_labels, output_figure_stem, run_title,
                                       abundances_over_h=True):
    """
    Create a set of plots of a number of Cannon runs.

    :param data_sets:
        A list of runs of the Cannon which are to be plotted. This should be a list of dictionaries. Each dictionary
        should have the entries:

        cannon_output: The filename of the JSON output file from the Cannon.
        title: Legend caption to use for each Cannon run.
        filters: A string containing semicolon-separated set of constraints on stars we are to include.
        colour: The colour to plot the dataset in.
        line_type: The Pyxplot line type to use for this Cannon run.


    :param abscissa_label:
        The name of the label we are to plot on the horizontal axis. This should be 'SNR/A', 'SNR/pixel', 'ebv'. See
        <lib/abcissa_information.py>, where these are defined.

    :param compare_against_reference_labels:
        If true, we measure the difference between each label value estimated by the Cannon and the target value taken
        from that star's metadata in the original spectrum library. I.e. the value used to synthesise the spectrum.

        If false, we measure the deviation from the value for each label estimated at the highest abscissa value -- e.g.
        highest SNR.

    :param output_figure_stem:
        Directory to save plots in

    :param run_title:
        A suffix to put at the end of the label in the top-left corner of each plot

    :param abundances_over_h:
        Boolean flag to select whether we plot abundances over H or Fe.

    :return:
        None
    """

    # Metadata about all the labels which we can plot the Cannon's precision in estimating
    label_info = LabelInformation().label_info

    # Metadata data about all of the horizontal axes that we can plot precision against
    abscissa_info = AbcissaInformation().abscissa_labels

    # Look up a list of all the (unique) labels the Cannon tried to fit in all the data sets we're plotting
    unique_json_files = set([item['cannon_output'] for item in data_sets])
    labels_in_each_data_set = [json.loads(open(json_file).read())['labels'] for json_file in unique_json_files]
    unique_labels = set([label for label_list in labels_in_each_data_set for label in label_list])

    # Filter out any labels where we don't have metadata about how to plot them
    label_names = [item for item in unique_labels if item in label_info]

    # Create directory to store output files in
    os.system("mkdir -p {}".format(output_figure_stem))

    data_set_titles = []
    output_figure_stem = os_path.abspath(output_figure_stem) + "/"
    data_set_counter = -1
    plot_cross_correlations = [{} for j in data_sets]

    # If requested, plot all abundances (apart from Fe) over Fe
    if not abundances_over_h:
        for j, label_name in enumerate(label_names):
            test = re.match("\[(.*)/H\]", label_name)
            if test is not None:
                if test.group(1) != "Fe":
                    label_names[j] = "[{}/Fe]".format(test.group(1))

    common_x_limits = abscissa_info[3]

    # Loop over the various Cannon runs we have, e.g. LRS and HRS
    for counter, data_set in enumerate(data_sets):

        data = json.loads(open(data_set['cannon_output']).read())

        # If no label has been specified for this Cannon run, use the description field from the JSON output
        if data_set['title'] is None:
            data_set['title'] = data['description']

        # Calculate the accuracy of the Cannon's abundance determinations
        accuracy_calculator = CannonAccuracyCalculator(
            cannon_json_output=data,
            label_names=label_names,
            compare_against_reference_labels=compare_against_reference_labels,
            assume_scaled_solar=assume_scaled_solar)

        stars_which_meet_filter = accuracy_calculator.filter_test_stars(constraints=data_set['filters'].split(";"))

        accuracy_calculator.calculate_cannon_offsets(filter_on_indices=stars_which_meet_filter)

        # Add data set to plot
        legend_label = data_set['title']  # Read the title which was supplied on the command line for this dataset
        if run_title:
            legend_label += " ({})".format(run_title)  # Possibly append a run title to the end, if supplied

        # add data set
        # Convert SNR/pixel to SNR/A at 6000A
        raster = np.array(cannon_json['wavelength_raster'])
        raster_diff = np.diff(raster[raster > 6000])
        pixels_per_angstrom = 1.0 / raster_diff[0]

        data_set_titles.append(legend_label)

        # LaTeX strings to use to label each stellar label on graph axes
        labels_info = [label_info[ln] for ln in label_names]

        # Create a sorted list of all the abscissa values we've got
        abscissa_info = abscissa_labels[abscissa_label]
        abscissa_values = [item[abscissa_info[0]] for item in cannon_stars]
        abscissa_values = sorted(set(abscissa_values))

        # If all abscissa values are off the range of the x axis, rescale axis
        if common_x_limits is not None:
            if abscissa_values[0] > common_x_limits[1]:
                common_x_limits[1] = abscissa_values[0]
                print "Rescaling x-axis to include {:.1f}".format(abscissa_values[0])
            if abscissa_values[-1] < common_x_limits[0]:
                common_x_limits[0] = abscissa_values[-1]
                print "Rescaling x-axis to include {:.1f}".format(abscissa_values[-1])

        data_set_counter += 1

        # Construct a datafile listing all the offsets for each label, for each abscissa value
        # This full list of data points is used to make histograms
        scale = np.sqrt(pixels_per_angstrom)
        for k, xk in enumerate(abscissa_values):
            snr_per_a = None
            if abscissa_label.startswith("SNR"):
                snr_per_a = xk * scale

            keyword = snr_per_a if abscissa_label == "SNR/A" else xk

            y = []
            for i, (label_name, label_info) in enumerate(zip(label_names, labels_info)):
                # List of offsets
                diffs = label_offset[xk][label_name]
                y.append(diffs)

                # Filename for data file containing all offsets
                data_file = "{}data_offsets_all_{:d}_{:06.1f}.dat".format(output_figure_stem,
                                                                          data_set_counter,
                                                                          keyword)

                # Output histogram of label mismatches at this abscissa value
                plot_histograms[i][data_set_counter][keyword] = [
                    (data_file, scale, i + 1)  # Pyxplot counts columns starting from 1, not 0
                ]

            # Output data file of label mismatches at this abscissa value
            np.savetxt(fname=data_file, X=np.transpose(y), header="""
# Each row represents a star
# {0}

""".format("     ".join(["offset_{}".format(x) for x in label_names]))
                       )

            # Output scatter plots of label cross-correlations at this abscissa value
            if correlation_plots:
                plot_cross_correlations[data_set_counter][keyword] = (data_file, scale)

        del data

    # make plots

    # LaTeX strings to use to label each stellar label on graph axes
    labels_info = [label_info[ln] for ln in label_names]

    abscissa_info = abscissa_labels[abscissa_label]

    # Create pyxplot script to produce this plot
    plotter = PyxplotDriver()

    # Create a new pyxplot script for correlation plots
    for data_set_counter, data_set_items in enumerate(plot_cross_correlations):
        for k, (abscissa_value, plot_item) in enumerate(sorted(data_set_items.iteritems())):
            (data_filename, snr_scaling) = plot_item

            if abscissa_label == "SNR/A":
                caption = "SNR/A {0:.1f}; SNR/pixel {1:.1f}". \
                    format(abscissa_value, abscissa_value / snr_scaling)
            elif abscissa_label == "SNR/pixel":
                caption = "SNR/A {0:.1f}; SNR/pixel {1:.1f}". \
                    format(abscissa_value * snr_scaling, abscissa_value)
            else:
                caption = "{0} {1}".format(abscissa_info[1], abscissa_value)

            ppl = """
set nokey
set fontsize 1.6
                  """

            for i in range(len(label_names) - 1):
                for j in range(i + 1, len(label_names)):
                    label_info = label_info[label_names[j]]
                    if i == 0:
                        ppl += "unset yformat\n"
                        ppl += "set ylabel \"$\Delta$ {}\"\n".format(label_info["latex"])
                    else:
                        ppl += "set yformat '' ; set ylabel ''\n"
                    ppl += "set yrange [{}:{}]\n".format(-label_info["offset_max"] * 1.2,
                                                         label_info["offset_max"] * 1.2)

                    label_info = label_info[label_names[i]]
                    if j == len(label_names) - 1:
                        ppl += "unset xformat\n"
                        ppl += "set xlabel \"$\Delta$ {}\"\n".format(label_info["latex"])
                    else:
                        ppl += "set xformat '' ; set xlabel ''\n"
                    ppl += "set xrange [{}:{}]\n".format(-label_info["offset_max"] * 1.2,
                                                         label_info["offset_max"] * 1.2)

                    ppl += "set origin {},{}\n".format(i * item_width, (len(label_names) - 1 - j) * item_width)

                    ppl += "plot  \"{}\" using {}:{} w dots ps 2\n".format(data_filename, i + 1, j + 1)

            plotter.make_plot(output_filename=("{}correlation_{:d}_{:d}".
                                               format(output_figure_stem, k, data_set_counter)),
                              caption=r"""
{data_set_title} \newline {caption}
                              """.format(data_set_title=data_set_titles[data_set_counter],
                                         caption=caption
                                         ),
                              pyxplot_script=ppl
                              )


if __name__ == "__main__":
    # Read input parameters
    command_line_arguments = fetch_command_line_arguments()
    generate_correlation_scatter_plots(**command_line_arguments)
