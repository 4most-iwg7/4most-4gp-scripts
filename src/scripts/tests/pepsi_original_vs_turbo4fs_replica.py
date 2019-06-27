#!../../../../virtualenv/bin/python3
# -*- coding: utf-8 -*-

# NB: The shebang line above assumes you've installed a python virtual environment alongside your working copy of the
# <4most-4gp-scripts> git repository. It also only works if you invoke this python script from the directory where it
# is located. If these two assumptions are incorrect (e.g. you're using Conda), you can still use this script by typing
# <python import_pepsi.py>, but <./import_pepsi.py> will not work.

"""
Compare the original pepsi spectra with synthetic replica based on literature reported parameters
"""


import logging
from fourgp_speclib import SpectrumLibrarySqlite

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import imp
payne_test2 = imp.load_source('payne_test2', '../test_payne/payne_test2.py')

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(filename)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


spectra = SpectrumLibrarySqlite.open_and_search(
        library_spec='pepsi_4fs_hrs/',
        workspace='/home/travegre/Projects/4GP/4most-4gp-scripts/workspace/',
        extra_constraints={"continuum_normalised": True}
    )
pepsi_library, pepsi_library_items = [spectra[i] for i in ("library", "items")]
# Load test set
pepsi_library_ids = [i["specId"] for i in pepsi_library_items]
spectra = [pepsi_library.open(ids=i).extract_item(0) for i in pepsi_library_ids]

star_list = {}

# CREATE MASK
#print(list(spectra[0].wavelengths))
mask = payne_test2.create_censoring_masks(3, spectra[0].wavelengths, "../test_payne/line_list_filter_2016MNRAS.461.2174R_without_cores.txt", ['Teff'], '', logger)['Teff']
mask = payne_test2.create_censoring_masks(3, spectra[0].wavelengths, "../test_payne/line_list_filter_2016MNRAS.461.2174R_without_cores.txt", ['logg'], '', logger)['logg']
mask = payne_test2.create_censoring_masks(3, spectra[0].wavelengths, "../test_payne/line_list_filter_2016MNRAS.461.2174R_without_cores.txt", ['[Fe/H]'], '', logger)['[Fe/H]']
mask = payne_test2.create_censoring_masks(3, spectra[0].wavelengths, "../test_payne/line_list_filter_2016MNRAS.461.2174R_without_cores.txt", ['Teff', 'logg', '[Fe/H]'], '', logger)['Teff']

for spectrum in spectra:
  try:
    star_list[spectrum.metadata['Starname']] = {'Teff': spectrum.metadata['Teff'], 'logg': spectrum.metadata['logg'], 'vmic': spectrum.metadata['vmic_GES'], '[Fe/H]': spectrum.metadata['[Fe/H]'], 'values':spectrum.values[mask], 'wavelengths': spectrum.wavelengths[mask]}
  except:
    pass#print(spectrum.metada






spectra = SpectrumLibrarySqlite.open_and_search(
        library_spec='turbospec_turbo_pepsi_replica_3label_hrs/',
        workspace='/home/travegre/Projects/4GP/4most-4gp-scripts/workspace/',
        extra_constraints={"continuum_normalised": True}
    )
pepsi_library, pepsi_library_items = [spectra[i] for i in ("library", "items")]
# Load test set
pepsi_library_ids = [i["specId"] for i in pepsi_library_items]
spectra = [pepsi_library.open(ids=i).extract_item(0) for i in pepsi_library_ids]

star_list_3label = {}
for spectrum in spectra:
  try:
    star_list_3label[spectrum.metadata['Starname']] = {'Teff': spectrum.metadata['Teff'], 'logg': spectrum.metadata['logg'], '[Fe/H]': spectrum.metadata['[Fe/H]'], 'values':spectrum.values[mask], 'wavelengths': spectrum.wavelengths[mask]}
  except:
    pass#print(spectrum.metada




spectra = SpectrumLibrarySqlite.open_and_search(
        library_spec='turbospec_turbo_pepsi_replica_4label_hrs/',
        workspace='/home/travegre/Projects/4GP/4most-4gp-scripts/workspace/',
        extra_constraints={"continuum_normalised": True}
    )
pepsi_library, pepsi_library_items = [spectra[i] for i in ("library", "items")]
# Load test set
pepsi_library_ids = [i["specId"] for i in pepsi_library_items]
spectra = [pepsi_library.open(ids=i).extract_item(0) for i in pepsi_library_ids]

star_list_4label = {}
for spectrum in spectra:
  try:
    star_list_4label[spectrum.metadata['Starname']] = {'Teff': spectrum.metadata['Teff'], 'logg': spectrum.metadata['logg'], '[Fe/H]': spectrum.metadata['[Fe/H]'], 'values':spectrum.values[mask], 'wavelengths': spectrum.wavelengths[mask]}
  except:
    pass#print(spectrum.metada



for i in star_list.keys():
    fig = plt.figure(figsize=(12, 8), dpi=200)

    mask = ~np.isnan(star_list[i]['wavelengths'])#(star_list[i]['wavelengths'] > float(wav.split('-')[0])) & (star_list[i]['wavelengths'] < float(wav.split('-')[1]))

    plt.plot(star_list[i]['wavelengths'][mask], star_list[i]['values'][mask], label='original', lw=1)
    plt.plot(star_list_3label[i]['wavelengths'][mask], star_list_3label[i]['values'][mask], lw=1, label='3 label, o-c: %.5f'%np.abs(star_list_3label[i]['values']-star_list[i]['values']).mean())
    plt.plot(star_list_4label[i]['wavelengths'][mask], star_list_4label[i]['values'][mask], lw=1, label='4 label, o-c: %.5f'%np.abs(star_list_4label[i]['values']-star_list[i]['values']).mean())
    
    plt.title("%s, teff: %.2f, logg: %.2f, feh: %.2f, vmic: %.2f" % (i, star_list[i]['Teff'], star_list[i]['logg'], star_list[i]['[Fe/H]'], star_list[i]['vmic']), fontsize=20)
    plt.legend()
    #plt.show()
    fig.savefig('pepsi_plots/%s.png' % (i.replace(' ', '_')))


    for wav in ['5224-5235', '5372-5391', '6480-6530', '6600-6650']:
        fig = plt.figure(figsize=(12, 8), dpi=200)

        mask = (star_list[i]['wavelengths'] > float(wav.split('-')[0])) & (star_list[i]['wavelengths'] < float(wav.split('-')[1]))

        plt.plot(star_list[i]['wavelengths'][mask], star_list[i]['values'][mask], label='original', lw=1)
        plt.plot(star_list_3label[i]['wavelengths'][mask], star_list_3label[i]['values'][mask], lw=1, label='3 label, o-c: %.5f'%np.abs(star_list_3label[i]['values']-star_list[i]['values']).mean())
        plt.plot(star_list_4label[i]['wavelengths'][mask], star_list_4label[i]['values'][mask], lw=1, label='4 label, o-c: %.5f'%np.abs(star_list_4label[i]['values']-star_list[i]['values']).mean())
        
        plt.title("%s, teff: %.2f, logg: %.2f, feh: %.2f, vmic: %.2f" % (i, star_list[i]['Teff'], star_list[i]['logg'], star_list[i]['[Fe/H]'], star_list[i]['vmic']), fontsize=20)
        plt.legend()
        #plt.show()
        fig.savefig('pepsi_plots/%s_%s.png' % (i.replace(' ', '_'), wav))