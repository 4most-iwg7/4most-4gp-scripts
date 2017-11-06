#!/bin/bash

source ../../../virtualenv/bin/activate

mkdir -p ../../output_plots/cannon_performance/internal_model

python internal_model_one_variable.py \
    --output-stub "../../output_plots/internal_model/rect_grid_5731.7618" \
    --wavelength 5731.7618 \
    --label "[Fe/H]" \
    --label-axis-latex "[Fe/H]" \
    --fixed-label "Teff=6000" \
    --fixed-label "logg=4.2" \
    --library "turbospec_rect_grid" \
    --train-library "4fs_rect_grid_lrs[SNR=250]" \
    --cannon-output "../../output_data/cannon/cannon_rect_rect_lrs_3label"
