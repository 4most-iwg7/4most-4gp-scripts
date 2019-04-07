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

python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
                       --test "galah_test_sample_4fs_hrs" \
                       --reload-payne "true" \
                       --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
                       --description "4MOST HRS (censored) - Payne 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
                       --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
                       --assume-scaled-solar \
                       --output-file "../../../output_data/payne/payne_galah_censored_hrs_10label" \
                       --train-batch-count 10 \
                       --train-batch-number 8 \
                       --test-batch-count 17000 \
                       --test-batch-number 1 \
                       --neuron-count "10"

#python3 payne_test2.py --train "galah_training_sample_4fs_lrs[SNR=250]" \
#                       --test "galah_test_sample_4fs_lrs" \
#                       --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
#                       --description "4MOST LRS (censored) - Payne 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                       --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
#                       --assume-scaled-solar \
#                       --output-file "../../../output_data/payne/payne_galah_censored_lrs_10label" \
#                       --neuron-count "5" 

