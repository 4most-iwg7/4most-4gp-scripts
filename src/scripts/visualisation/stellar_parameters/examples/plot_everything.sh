#!/bin/bash

# A little bit of scripting magic so that whatever directory this script is
# run from, we always find the python scripts and data we need.
cd "$(dirname "$0")"
cwd=`pwd`/..
cd ${cwd}

# Activate python virtual environment
source ../../../../../virtualenv/bin/activate

mkdir -p ../../../../output_plots/stellar_parameters

# -------------------------------------------------------------------------------------------------------------------

#python scatter_plot.py --library turbospec_apokasc_test_set --library-colour red --library-title "Test set" \
#                       --label "[Fe/H]{-1:0.6}" --label "[Mg/H]{-0.4:1.2}" \
#                       --label-axis-latex "[Fe/H]" --label-axis-latex "[Mg/Fe]" \
#                       --using "\$1:(\$2-\$1)" \
#                       --output ../../../../output_plots/stellar_parameters/apogee_magnesium_test

#python scatter_plot.py --library turbospec_apokasc_training_set --library-colour blue --library-title "Training set" \
#                       --label "[Fe/H]{-1:0.6}" --label "[Mg/H]{-0.4:1.2}" \
#                       --label-axis-latex "[Fe/H]" --label-axis-latex "[Mg/Fe]" \
#                       --using "\$1:(\$2-\$1)" \
#                       --output ../../../../output_plots/stellar_parameters/apogee_magnesium_training

#python scatter_plot.py --library turbospec_apokasc_test_set --library-colour red --library-title "Test set" \
#                       --library turbospec_apokasc_training_set --library-colour blue --library-title "Training set" \
#                       --label "Teff{5100:4000}" --label "logg{3.8:1.2}" \
#                       --label-axis-latex "Teff" --label-axis-latex "log(g)" \
#                       --output ../../../../output_plots/stellar_parameters/apogee_teff_logg_both

#python scatter_plot.py --library turbospec_apokasc_test_set --library-colour red --library-title "Test set" \
#                       --label "Teff{5100:4000}" --label "logg{3.8:1.2}" \
#                       --label-axis-latex "Teff" --label-axis-latex "log(g)" \
#                       --output ../../../../output_plots/stellar_parameters/apogee_teff_logg_test

#python scatter_plot.py --library turbospec_apokasc_training_set --library-colour blue --library-title "Training set" \
#                       --label "Teff{5100:4000}" --label "logg{3.8:1.2}" \
#                       --label-axis-latex "Teff" --label-axis-latex "log(g)" \
#                       --output ../../../../output_plots/stellar_parameters/apogee_teff_logg_training

# -------------------------------------------------------------------------------------------------------------------

python histogram.py --library turbospec_ahm2017_sample --library-colour red --library-title "Training set" \
                    --library turbospec_ahm2017_perturbed  --library-colour blue --library-title "Test set" \
                    --label "Teff{7000:3400}" --label "logg{5:0}" --label "[Fe/H]{1:-3}" \
                    --label-axis-latex "Teff" --label-axis-latex "log(g)" --label-axis-latex "[Fe/H]" \
                    --using "\$1" --using "\$2" --using "\$3" \
                    --output ../../../../output_plots/stellar_parameters/histogram_ahm2017_pair

python scatter_plot_coloured.py --library turbospec_ahm2017_sample --library-title "Training set" \
                                --label "Teff{7000:3400}" --label "logg{5:0}" --label "[Fe/H]{:}" \
                                --label-axis-latex "Teff" --label-axis-latex "log(g)" --label-axis-latex "[Fe/H]" \
                                --colour-range-min -0.7 --colour-range-max 0.5 \
                                --output ../../../../output_plots/stellar_parameters/hr_coloured_ahm2017_pair_1

python scatter_plot_coloured.py --library turbospec_ahm2017_perturbed --library-title "Test set" \
                                --label "Teff{7000:3400}" --label "logg{5:0}" --label "[Fe/H]{:}" \
                                --label-axis-latex "Teff" --label-axis-latex "log(g)" --label-axis-latex "[Fe/H]" \
                                --colour-range-min -0.7 --colour-range-max 0.5 \
                                --output ../../../../output_plots/stellar_parameters/hr_coloured_ahm2017_pair_2

# -------------------------------------------------------------------------------------------------------------------

python histogram.py --library galah_training_sample_turbospec --library-colour red --library-title "Training set" \
                    --library galah_test_sample_turbospec  --library-colour blue --library-title "Test set" \
                    --label "Teff{7000:3400}" --label "logg{5:0}" --label "[Fe/H]{1:-3}" \
                    --label-axis-latex "Teff" --label-axis-latex "log(g)" --label-axis-latex "[Fe/H]" \
                    --using "\$1" --using "\$2" --using "\$3" \
                    --output ../../../../output_plots/stellar_parameters/histogram_galah_pair

python scatter_plot_coloured.py --library galah_training_sample_turbospec --library-title "Training set" \
                                --label "Teff{7000:3400}" --label "logg{5:0}" --label "[Fe/H]{:}" \
                                --label-axis-latex "Teff" --label-axis-latex "log(g)" --label-axis-latex "[Fe/H]" \
                                --colour-range-min -0.7 --colour-range-max 0.5 \
                                --output ../../../../output_plots/stellar_parameters/hr_coloured_galah_pair_1

python scatter_plot_coloured.py --library galah_test_sample_turbospec --library-title "Test set" \
                                --label "Teff{7000:3400}" --label "logg{5:0}" --label "[Fe/H]{:}" \
                                --label-axis-latex "Teff" --label-axis-latex "log(g)" --label-axis-latex "[Fe/H]" \
                                --colour-range-min -0.7 --colour-range-max 0.5 \
                                --output ../../../../output_plots/stellar_parameters/hr_coloured_galah_pair_2
