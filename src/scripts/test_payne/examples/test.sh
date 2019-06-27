#!/bin/bash

# A little bit of scripting magic so that whatever directory this script is
# run from, we always find the python scripts and data we need.
cd "$(dirname "$0")"
cwd=`pwd`/..
cd ${cwd}

# Activate python virtual environment
source ../../../../virtualenv/bin/activate

# Now do some work
mkdir -p ../../../output_data/payne

# ----------------------
export OMP_NUM_THREADS=1

# python3 payne_test2.py --train "galah_training_sample_4fs_lrs[SNR=250]" \
#                        --test "galah_test_sample_4fs_lrs" \
#                        --reload-payne "false" \
#                        --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
#                        --description "4MOST LRS (censored) - Payne 3 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                        --labels "Teff,logg,[Fe/H]" \
#                        --assume-scaled-solar \
#                        --num-training-workers 40 \
#                        --num-testing-workers 40 \
#                        --output-file "../../../output_data/payne/payne_galah_censored_lrs_3label_10neuron" \
#                        --neuron-count "10"



python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
                       --test "galah_test_sample_4fs_hrs" \
                       --reload-payne "true" \
                       --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
                       --description "4MOST HRS (censored) - Payne 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
                       --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
                       --assume-scaled-solar \
                       --num-training-workers 40 \
                       --num-testing-workers 40 \
                       --output-file "../../../output_data/payne/payne_galah_censored_hrs_10label_20neuron" \
                       --neuron-count "20"







# python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                       --test "pepsi_synthetic_4fs_hrs" \
#                       --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
#                       --description "4MOST HRS (censored) - Payne 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                       --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
#                       --reload-payne "true" \
#                       --assume-scaled-solar \
#                       --train-batch-count 10 \
#                       --test-batch-count 1 \
#                       --output-file "../../../output_data/payne/payne_galah_censored_hrs_10label_test_pepsi_synthetic" \
#                       --neuron-count "10"

# python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                       --test "galah_test_sample_4fs_hrs" \
#                       --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
#                       --description "4MOST HRS (censored) - Payne 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                       --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
#                       --assume-scaled-solar \
#                       --output-file "../../../output_data/payne/payne_galah_censored_hrs_test" \
#                       --neuron-count "10"

