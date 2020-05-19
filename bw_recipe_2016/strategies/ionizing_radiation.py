from copy import deepcopy


FRESH_WATER = [
    ("water", "ground-"),
    ("water", "surface water"),
]


def set_categories(obj, tpl):
    obj["categories"] = tpl
    return obj


def fix_water_categories(data):
    for ds in data:
        to_add, to_remove = [], []
        for cf in ds["exchanges"]:
            if cf["categories"] == "fresh water":
                to_remove.append(cf)
                to_add.extend(
                    [set_categories(deepcopy(cf), cat) for cat in FRESH_WATER]
                )
                cf["categories"] = ("water", "surface water")
            elif cf["categories"] == "marine water":
                cf["categories"] = ("water", "ocean")
        ds["exchanges"] = [cf for cf in ds["exchanges"] if cf not in to_remove] + to_add
    return data
