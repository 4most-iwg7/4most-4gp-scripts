#!../../../../virtualenv/bin/python3
# -*- coding: utf-8 -*-

# NB: The shebang line above assumes you've installed a python virtual environment alongside your working copy of the
# <4most-4gp-scripts> git repository. It also only works if you invoke this python script from the directory where it
# is located. If these two assumptions are incorrect (e.g. you're using Conda), you can still use this script by typing
# <python synthesize_demo_stars_2.py>, but <./synthesize_demo_stars_2.py> will not work.

"""
Synthesize a handful of demo stars, e.g. the Sun, using TurboSpectrum.
"""

import logging

from lib.base_synthesizer import Synthesizer
from fourgp_speclib import SpectrumLibrarySqlite

# Start logging our progress
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(filename)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.info("Synthesizing spectra of pepsi")

# Instantiate base synthesizer
synthesizer = Synthesizer(library_name="turbo_pepsi_replica_3label",
                          logger=logger,
                          docstring=__doc__)

spectra = SpectrumLibrarySqlite.open_and_search(
        library_spec='pepsi_4fs_hrs/',
        workspace='/home/travegre/Projects/4GP/4most-4gp-scripts/workspace/',
        extra_constraints={"continuum_normalised": True}
    )
pepsi_library, pepsi_library_items = [spectra[i] for i in ("library", "items")]
# Load test set
pepsi_library_ids = [i["specId"] for i in pepsi_library_items]

spectra = [pepsi_library.open(ids=i).extract_item(0) for i in pepsi_library_ids]
print(spectra)

star_list = []
for spectrum in spectra:
  try:

    #star_list.append({'name': spectrum.metadata['Starname'], 'Teff': spectrum.metadata['Teff'], 'logg': spectrum.metadata['logg'], '[Fe/H]': spectrum.metadata['[Fe/H]'], 'microturbulence': spectrum.metadata['vmic_GES'], 'extra_metadata': {'set_id': 1}})
    star_list.append({'name': spectrum.metadata['Starname'], 'Teff': spectrum.metadata['Teff'], 'logg': spectrum.metadata['logg'], '[Fe/H]': spectrum.metadata['[Fe/H]'], 'extra_metadata': {'set_id': 1}})
    print(spectrum.metadata['Starname'])
  except:
    pass#print(spectrum.metadata['Starname'])
  
  '''
  #print(spectrum.metadata)
  ref_labels = []
  for j in ['Teff', '[Fe/H]', 'logg', 'vmic_GES', 'vsini']:
    try:
      print(j, ' ', spectrum.metadata[j])
      ref_labels.append(spectrum.metadata[j])
    except:
      continue
  print(ref_labels)
  '''

print(star_list)


# Pass list of stars to synthesizer
synthesizer.set_star_list(star_list)

# Output data into sqlite3 db
synthesizer.dump_stellar_parameters_to_sqlite()

# Create new SpectrumLibrary
synthesizer.create_spectrum_library()

# Iterate over the spectra we're supposed to be synthesizing
synthesizer.do_synthesis()

# Close TurboSpectrum synthesizer instance
synthesizer.clean_up()
