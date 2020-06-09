def generic_reformat(data, config):
    """Change from:

            {
            category name (str): {
                'unit': unit (str),
                'perspective': individualist|hierarchist|egalitarian (str),
                'cfs': [{
                    'amount': float,
                    'name': str,
                    'synonyms': [str],
                    'CAS number': str,
                    'formula': str,
                    'compartment': str,
                    'subcompartment': str,
                }]
            }
        }

    To:

        [
            {
                'name': tuple; name of LCIA method,
                'description': str,
                'filename': str,
                'unit': str,
                'exchanges': [  # CFs
                    'input': tuple; key of biosphere flow,
                    'amount': float,
                    # plus any applicable uncertainty fields
                ]
            }
        ]

    """
    return [
        {
            "name": (k, v["perspective"]) if "perspective" in v else (k,),
            "unit": v["unit"],
            "filename": config.filename,
            "description": "",
            "exchanges": v["cfs"],
        }
        for k, v in data.items()
    ]


def complete_method_name(data, config):
    for ds in data:
        ds["name"] = config.base_midpoint_name + ds["name"]
    return data


def tupleize_categories(data):
    for ds in data:
        for cf in ds["exchanges"]:
            if "categories" in cf:
                if isinstance(cf["categories"], str):
                    cf["categories"] = (cf["categories"],)
                else:
                    cf["categories"] = tuple(cf["categories"])
    return data
