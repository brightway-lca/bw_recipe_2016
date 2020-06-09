import warnings


MESSAGE = """Duplicate CFs:
    Method: {method}
    Flow: {flow}
    Categories: {categories}
    Amounts: {x}, {y}
"""


def check_duplicate_cfs(data):
    """Check that multiple substances in input data are not matched to same ecoinvent flow"""
    for ds in data:
        seen = {}
        for cf in ds['exchanges']:
            key = (cf['name'], cf['categories'])
            if key in seen:
                warnings.warn(MESSAGE.format(method=ds['name'], flow=cf['name'], categories=cf['categories'], x=seen[key], y=cf['amount']))
            else:
                seen[key] = cf['amount']
    return data
