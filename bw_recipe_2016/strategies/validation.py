import warnings


MESSAGE = """Duplicate CFs:
    Method: {method}
    Flow: {flow}
    Categories: {categories}
    Amounts: {x}, {y}
"""


def check_duplicate_cfs(data, biosphere):
    """Check that multiple substances in input data are not matched to same ecoinvent flow"""
    bd = {obj.key: obj for obj in biosphere}
    for ds in data:
        seen = {}
        for cf in ds["exchanges"]:
            if not cf.get("input"):
                continue
            flow = bd[cf["input"]]
            key = (flow["name"], flow["categories"])
            if key in seen:
                warnings.warn(
                    MESSAGE.format(
                        method=ds["name"],
                        flow=cf["name"],
                        categories=cf["categories"],
                        x=seen[key],
                        y=cf["amount"],
                    )
                )
            else:
                seen[key] = cf["amount"]
    return data
