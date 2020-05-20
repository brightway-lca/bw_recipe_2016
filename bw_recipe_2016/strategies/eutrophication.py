from copy import deepcopy


def set_categories(obj, tpl):
    obj["categories"] = tpl
    return obj


def add_water_category(data):
    mapping = {
        "agricultural soil": ("soil", "agricultural"),
        "sea water": ("water", "ocean"),
        "seawater": ("water", "ocean"),
    }
    for ds in data:
        to_add, to_remove = [], []
        for cf in ds["exchanges"]:
            if cf["compartment"] == 'freshwater':
                to_remove.append(cf)
                to_add.extend(
                    [set_categories(deepcopy(cf), cat) for cat in [("water", "surface water"), ("water",), ("water", "ground-")]]
                )
            else:
                cf["categories"] = mapping[cf["compartment"]]
            # Only the general "water" flow exists for this flow...
            if cf["name"].lower() == "phosphoric acid" and cf.get("categories") == (
                "water",
                "surface water",
            ):
                cf["categories"] = ("water",)
        ds["exchanges"] = [cf for cf in ds["exchanges"] if cf not in to_remove] + to_add
    return data
