from copy import deepcopy


def set_categories(obj, tpl):
    obj["categories"] = tpl
    return obj


def set_toxicity_categories(data):
    category_mapping = {
        "agriculturalsoil": [("soil", "agricultural")],
        "freshwater": [("water", "surface water"), ("water",), ("water", "ground-")],
        "industrialsoil": [("soil", "industrial")],
        "ruralair": [
            ("air",),
            ("air", "low population density, long-term"),
            ("air", "non-urban air or from high stacks"),
        ],
        "seawater": [("water", "ocean")],
        "urbanair": [("air", "urban air close to ground"), ("air", "indoor"),],
    }

    for ds in data:
        to_add, to_remove = [], []
        for cf in ds["exchanges"]:
            try:
                categories = category_mapping[
                    cf["compartment"].replace(" ", "").lower()
                ]
                to_remove.append(cf)
                to_add.extend([set_categories(deepcopy(cf), cat) for cat in categories])
            except KeyError:
                continue
        ds["exchanges"] = [cf for cf in ds["exchanges"] if cf not in to_remove] + to_add
    return data


def correct_ion_cas_registry_numbers(data):
    CORRECTIONS = {
        (7440382, "As(V)"): "17428-41-0",
        (7440224, "Ag(I)"): "14701-21-4",
        (7440417, "Be(II)"): "22537-20-8",
        (7440439, "Cd(II)"): "22537-48-0",
        (7440484, "Co(II)"): "22541-53-3",  # Group of all +2 ions, i.e. 57, 58, and 60
        (7440473, "Cr(III)"): "16065-83-1",
        (7440473, "Cr(VI)"): "18540-29-9",
        (7440508, "Cu(II)"): "15158-11-9",
        (7439976, "Hg(II)"): "14302-87-5",
        (7439987, "Mo(VI)"): "16065-87-5",
        (7440020, "Ni(II)"): "14701-22-5",
        (7439921, "Pb(II)"): "14280-50-3",
        (7440360, "Sb(III)"): "23713-48-6",
        (7440360, "Sb(V)"): "22537-51-5",
        (7782492, "Se(IV)"): "22541-55-5",
        (7440315, "Sn(II)"): "22541-90-8",
        (7440280, "Tl(I)"): "22537-56-0",
        (7440622, "V(V)"): "22537-31-1",
        (7440666, "Zn(II)"): "23713-49-7",
    }
    for ds in data:
        for cf in ds["exchanges"]:
            try:
                cf["CAS number"] = CORRECTIONS[(cf["CAS number"], cf["name"])]
            except KeyError:
                continue
    return data


def drop_unmatchable_ions(data):
    ECOINVENT_MISSING = {
        "As(V)",
        "Cu(II)",
        "Be(II)",
        "Hg(II)",
        "Mo(VI)",
        "Pb(II)",
        "Sb(III)",
        "Sb(V)",
        "Se(IV)",
        "Sn(II)",
        "Tl(I)",
        "V(V)",
    }
    for ds in data:
        ds["exchanges"] = [
            cf for cf in ds["exchanges"] if cf["name"] not in ECOINVENT_MISSING
        ]
    return data


def drop_homonyms(data):
    """Drop some CFs which have the correct name, but not the correct CAS number, to avoid duplicate matches based on the name alone."""
    NOT_USED = {
        ("fenpropathrin", 64257847),
        ("mecoprop", 7085190),
        # Slightly cheating here for fenoxycarb - ecoinvent doesn't specify
        # the correct CAS number, so we take the higher value
        ("fenoxycarb", 72490018),
    }
    for ds in data:
        ds["exchanges"] = [
            cf
            for cf in ds["exchanges"]
            if (cf["name"].lower(), cf["CAS number"]) not in NOT_USED
        ]
    return data
