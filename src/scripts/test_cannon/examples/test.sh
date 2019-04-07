#!/bin/bash

# A little bit of scripting magic so that whatever directory this script is
# run from, we always find the python scripts and data we need.
cd "$(dirname "$0")"
cwd=`pwd`/..
cd ${cwd}

# Activate python virtual environment
source ../../../../virtualenv/bin/activate

# Now do some work
mkdir -p ../output_data/cannon


python3 cannon_test.py --train "galah_training_sample_4fs_hrs[SNR=250,5000<Teff<5500,-1<[Fe/H]<1]" \
                        --test "galah_test_sample_4fs_hrs" \
                        --description "4MOST HRS - 3 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
                        --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
                        --train-wavelength-window "5500-5505" \
                        --output-file "../../../output_data/cannon/test_redo_cannon_galah_hrs_10label"

# python3 cannon_test.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                        --test "galah_test_sample_4fs_hrs" \
#                        --description "4MOST HRS - 3 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                        --labels "Teff,logg,[Fe/H]" \
#                        --output-file "../../../output_data/cannon/redo_cannon_galah_hrs_3label"

# python3 cannon_test.py --train "galah_training_sample_4fs_lrs[SNR=250]" \
#                        --test "galah_test_sample_4fs_lrs" \
#                        --description "4MOST LRS - 3 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                        --labels "Teff,logg,[Fe/H]" \
#                        --output-file "../../../output_data/cannon/redo_cannon_galah_lrs_3label"

# python3 cannon_test.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                        --test "galah_test_sample_4fs_hrs" \
#                        --reload-cannon "../../../../output_data/cannon/redo_cannon_galah_censored_hrs_10label.cannon" \
#                        --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
#                        --description "4MOST HRS (censored) - 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                        --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
#                        --assume-scaled-solar \
#                        --output-file "../../../output_data/cannon/redo_cannon_galah_censored_hrs_10label"

# python3 cannon_test.py --train "galah_training_sample_4fs_lrs[SNR=250]" \
#                        --test "galah_test_sample_4fs_lrs" \
#                        --censor "line_list_filter_2016MNRAS.461.2174R.txt" \
#                        --description "4MOST LRS (censored) - 10 labels - Train on 0.25 GALAH. Test on 0.75 GALAH." \
#                        --labels "Teff,logg,[Fe/H],[Ca/H],[Mg/H],[Ti/H],[Si/H],[Na/H],[Ni/H],[Cr/H]" \
#                        --assume-scaled-solar \
#                        --output-file "../../../output_data/cannon/redo_cannon_galah_censored_lrs_10label" 

#python3 cannon_test.py --train "galah_training_sample_4fs_hrs[SNR=250]" \
#                       --test "galah_test_sample_4fs_hrs_50only[SNR=50,4500<Teff<6500,1<logg<4.8]" \
#                       --description "4MOST HRS - 3 labels - Train on GALAH" \
#                       --labels "Teff,logg,[Fe/H]" \
#                       --output-file "../../../output_data/cannon/cannon_galah_hrs_3label_5300-5600AA" \
#                       --train-wavelength-window "5300-5600"
