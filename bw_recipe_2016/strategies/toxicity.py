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
        "urbanair": [
            ("air", "urban air close to ground"),
            ("air", "indoor"),
            ("air", "urban air close to ground"),
        ],
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
