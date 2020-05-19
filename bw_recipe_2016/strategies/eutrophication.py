def add_water_category(data):
    mapping = {
        "agricultural soil": ("soil", "agricultural"),
        "sea water": ("water", "ocean"),
        "seawater": ("water", "ocean"),
        "freshwater": ("water", "surface water"),
    }
    for ds in data:
        for cf in ds["exchanges"]:
            cf["categories"] = mapping[cf["compartment"]]
            # Only the general "water" flow exists
            if cf["name"].lower() == "phosphoric acid" and cf["categories"] == (
                "water",
                "surface water",
            ):
                cf["categories"] = ("water",)
    return data
