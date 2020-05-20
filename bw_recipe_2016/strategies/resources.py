from .. import BASE_MIDPOINT_NAME


def remove_asterisk(data):
    for ds in data:
        for cf in ds["exchanges"]:
            if cf["name"].endswith("*"):
                cf["name"] = cf["name"][:-1]
    return data


def add_mineral_natural_resource_category(data):
    for ds in data:
        for cf in ds["exchanges"]:
            cf["categories"] = cf.get("categories", ("natural resource", "in ground"))
    return data


def add_fossil_natural_resource_category(data):
    for ds in data:
        for cf in ds["exchanges"]:
            cf["categories"] = cf.get("categories", ("natural resource",))
    return data


def add_synonyms(data):
    for ds in data:
        for cf in ds["exchanges"]:
            cf["synonyms"] = [cf["name"] + ", in ground"]
    return data


def fossil_method_name(data):
    for ds in data:
        ds["name"] = BASE_MIDPOINT_NAME + ("Fossil resource scarcity",)
    return data
