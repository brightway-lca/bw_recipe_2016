from .. import BASE_MIDPOINT_NAME


def complete_method_name(data, name):
    for ds in data:
        ds["name"] = BASE_MIDPOINT_NAME + (name,)
    return data


def set_unit(data):
    for ds in data:
        ds["unit"] = "m2∙annual crop eq"
    return data


def reset_categories(data):
    for ds in data:
        for cf in ds["exchanges"]:
            cf["categories"] = ("natural resource",)
    return data


def add_missing_flows(data):
    """There are some flows not given in ReCiPe that seem like they should be there, given the relatively coarse precision of these CFs."""
    new_cfs = {
        "managed forest": {
            "amount": 0.3,
            "flows": [
                "occupation, forest, unspecified",
                "occupation, field margin/hedgerow",
            ],
        },
        "annual crops": {
            "amount": 1.0,
            "flows": [
                "occupation, annual crop, flooded crop",
                "occupation, annual crop, irrigated, extensive",
            ],
        },
        "pasture": {
            "amount": 0.55,
            "flows": [
                "occupation, arable land, unspecified use",
                "occupation, grassland, natural, for livestock grazing",
                "occupation, heterogeneous, agricultural",
            ],
        },
        "artificial area": {"amount": 0.73, "flows": [],},
        "permanent crops": {
            "amount": 0.7,
            "flows": [
                "occupation, permanent crop, irrigated",
                "occupation, permanent crop, irrigated, extensive",
                "occupation, permanent crop, non-irrigated",
                "occupation, permanent crop, non-irrigated, extensive",
            ],
        },
    }
    """ The following were included in an earlier version of ReCiPe, but are skipped here, as we don't have enough info to use them consistently:

    * 'occupation, bare area (non-use)',
    * 'occupation, cropland fallow (non-use)',
    * 'occupation, forest, primary (non-use)',
    * 'occupation, forest, secondary (non-use)',
    * 'occupation, inland waterbody, unspecified',
    * 'occupation, lake, natural (non-use)',
    * 'occupation, river, natural (non-use)',
    * 'occupation, seabed, natural (non-use)',
    * 'occupation, seabed, unspecified',
    * 'occupation, snow and ice (non-use)',
    * 'occupation, unspecified',
    * 'occupation, unspecified, natural (non-use)',
    * 'occupation, wetland, coastal (non-use)',
    * 'occupation, wetland, inland (non-use)'
    """
    for ds in data:
        ds["exchanges"].extend(
            [
                {"name": flow, "amount": obj["amount"]}
                for obj in new_cfs.values()
                for flow in obj["flows"]
            ]
        )
    return data
