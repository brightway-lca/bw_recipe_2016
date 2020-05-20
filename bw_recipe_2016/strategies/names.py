SUBSTITUTIONS = {
    "ODP20": ("Stratospheric Ozone Depletion", "20 year timescale"),
    "ODP100": ("Stratospheric Ozone Depletion", "100 year timescale"),
    "ODPinfinite": ("Stratospheric Ozone Depletion", "Infinite timescale"),
    "EOFP": ("Ozone Formation", "Damage to Ecosystems"),
    "HOFP": ("Ozone Formation", "Damage to Humans"),
    "I": "Individualist",
    "H": "Hierarchist",
    "E": "Egalitarian",
    "Individualistic": "Individualist",
    "Hierarchic": "Hierarchist",
    "PMFP": "Particulate Matter Formation",
    "GWP20": ("Global Warming", "20 year timescale"),
    "GWP100": ("Global Warming", "100 year timescale"),
    "GWP1000": ("Global Warming", "1000 year timescale"),
    "AP": "Terrestrial Acidification",
    "FEP": "Freshwater Eutrophication",
    "ETPterrestrial": ("Ecotoxicity", "Terrestrial"),
    "ETPfw": ("Ecotoxicity", "Freshwater"),
    "ETPmarine": ("Ecotoxicity", "Marine"),
    "CFhuman-mid-ncarc": ("Toxicity", "Non-carcinogenic"),
    "CFhuman-mid-carc": ("Toxicity", "Carcinogenic"),
    "SOP": "Mineral Resource Scarcity",
    "IRP": "Ionizing Radiation",
}


def final_method_name(data):
    for ds in data:
        for k, v in SUBSTITUTIONS.items():
            name = []
            for elem in ds["name"]:
                try:
                    r = SUBSTITUTIONS[elem]
                    if isinstance(r, str):
                        name.append(r)
                    else:
                        name.extend(list(r))
                except KeyError:
                    name.append(elem)
            ds["name"] = tuple(name)
    return data
