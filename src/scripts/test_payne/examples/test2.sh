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

#python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                      --test "galah_test_sample_4fs_hrs_50only[SNR=50,5000<Teff<6000,3.8<logg<5]" \
#                      --reload-payne "true" \
#                      --description "4MOST HRS - 3 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                      --labels "Teff,logg,[Fe/H]" \
#                      --output-file "../../../output_data/payne/payne_galah_hrs_3label_5000-6000AA" \
#                      --train-wavelength-window "5000-6000" \
#                      --neuron-count "6"



python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
                       --test "galah_test_sample_4fs_hrs_50only[SNR=50,4500<Teff<6500,1<logg<4.8]" \
                       --reload-payne "true" \
                       --description "4MOST HRS - 3 labels - Train on GALAH, 3 neurons" \
                       --labels "Teff,logg,[Fe/H]" \
                       --output-file "../../../output_data/payne/payne_galah_hrs_3label_5300-5600AA_3neurons" \
                       --train-wavelength-window "5300-5600" \
                       --neuron-count "3"

#python3 payne_test2.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                       --test "galah_test_sample_4fs_hrs_50only[SNR=50,4500<Teff<6500,1<logg<4.8]" \
#                       --description "4MOST HRS - 3 labels - Train on GALAH, 10 neurons" \
#                       --labels "Teff,logg,[Fe/H]" \
#                       --output-file "../../../output_data/payne/payne_galah_hrs_3label_5300-5600AA_10neurons" \
#                       --train-wavelength-window "5300-5600" \
#                       --neuron-count "10"