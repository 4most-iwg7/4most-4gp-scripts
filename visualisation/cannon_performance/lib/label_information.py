# -*- coding: utf-8 -*-

"""

Define all of the allowed labels we can plot precision for. For each label we define the LaTeX
title to put on the precision axis, as well the the limits of the axis and the target values to indicate.
"""

import re


class LabelInformation:
    def __init__(self):

        self.label_info = {
            "Teff": {"latex": r"$T_{\rm eff}$ $[{\rm K}]$", "cannon_label": "Teff", "over_fe": False, "offset_min": 0,
                     "offset_max": 300, "targets": [100], "unit": "K"},
            "logg": {"latex": r"$\log{g}$ $[{\rm dex}]$", "cannon_label": "logg", "over_fe": False, "offset_min": 0,
                     "offset_max": 0.8, "targets": [0.3], "unit": "dex"},
            "[Fe/H]": {"latex": r"$[{\rm Fe}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Fe/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[C/H]": {"latex": r"$[{\rm C}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[C/H]", "over_fe": False,
                      "offset_min": 0, "offset_max": 1.1, "targets": [0.1, 0.2], "unit": "dex"},
            "[N/H]": {"latex": r"$[{\rm N}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[N/H]", "over_fe": False,
                      "offset_min": 0, "offset_max": 1.1, "targets": [0.1, 0.2], "unit": "dex"},
            "[O/H]": {"latex": r"$[{\rm O}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[O/H]", "over_fe": False,
                      "offset_min": 0, "offset_max": 1.1, "targets": [0.1, 0.2], "unit": "dex"},
            "[Na/H]": {"latex": r"$[{\rm Na}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Na/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Mg/H]": {"latex": r"$[{\rm Mg}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Mg/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Al/H]": {"latex": r"$[{\rm Al}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Al/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Si/H]": {"latex": r"$[{\rm Si}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Si/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Ca/H]": {"latex": r"$[{\rm Ca}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Ca/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Ti/H]": {"latex": r"$[{\rm Ti}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Ti/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Mn/H]": {"latex": r"$[{\rm Mn}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Mn/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Co/H]": {"latex": r"$[{\rm Co}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Co/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Ni/H]": {"latex": r"$[{\rm Ni}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Ni/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Ba/H]": {"latex": r"$[{\rm Ba}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Ba/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 1.1, "targets": [0.1, 0.2], "unit": "dex"},
            "[Sr/H]": {"latex": r"$[{\rm Sr}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Sr/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Cr/H]": {"latex": r"$[{\rm Cr}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Cr/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 0.75, "targets": [0.1, 0.2], "unit": "dex"},
            "[Li/H]": {"latex": r"$[{\rm Li}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Li/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 1.1, "targets": [0.2, 0.4], "unit": "dex"},
            "[Eu/H]": {"latex": r"$[{\rm Eu}/{\rm H}]$ $[{\rm dex}]$", "cannon_label": "[Eu/H]", "over_fe": False,
                       "offset_min": 0, "offset_max": 1.1, "targets": [0.2, 0.4], "unit": "dex"},
        }

        # Allow abundance over Fe to also be plotted
        for key in self.label_info.keys():
            test = re.match("\[(.*)/H\]", key)
            if test is not None:
                info = self.label_info[key].copy()
                new_key = "[{}/Fe]".format(test.group(1))
                info["over_fe"] = True
                info["latex"] = re.sub("rm H}", "rm Fe}", info["latex"])
                self.label_info[new_key] = info
