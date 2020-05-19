def add_biomass_stock_cfs(data):
    missing = [
        {
            "name": "carbon dioxide, from soil or biomass stock",
            "synonyms": [],
            "categories": ("air",),
            "amount": 1,
        },
        {
            "name": "carbon dioxide, to soil or biomass stock",
            "synonyms": [],
            "categories": ("soil",),
            "amount": -1,
        },
    ]

    for ds in data:
        ds["exchanges"].extend(missing)
        methane = next(o for o in ds["exchanges"] if o["name"] == "methane, fossil")
        ds["exchanges"].append(
            {
                "name": "methane",
                "synonyms": [],
                "categories": ("air",),
                "amount": methane["amount"],
            }
        )
        methane = next(o for o in ds["exchanges"] if o["name"] == "methane, non-fossil")
        ds["exchanges"].append(
            {
                "name": "methane, from soil or biomass stock",
                "synonyms": [],
                "categories": ("air",),
                "amount": methane["amount"],
            }
        )
    return data


def drop_known_missing(data):
    known_missing = {
        "ethane, 1,1,1-trichloro-, hcfc-140",
        "carbon monoxide, fossil",
        "carbon monoxide, from soil or biomass stock",
        "carbon monoxide, non-fossil",
        "methane, bromo-, halon 1001",
        "nitric oxide",
        "voc, volatile organic compounds, unspecified origin",  # What could the CF even be?
        "ethane, 1,2-dichloro-",
        "dimethyl ether",
    }
    for ds in data:
        ds["exchanges"] = [
            cf for cf in ds["exchanges"] if cf["name"].lower() not in known_missing
        ]
    return data


def add_air_category(data):
    for ds in data:
        for cf in ds["exchanges"]:
            cf["categories"] = cf.get("categories", ("air",))
    return data
