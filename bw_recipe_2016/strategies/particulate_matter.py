from .. import BASE_MIDPOINT_NAME


def complete_method_name(data):
    for ds in data:
        ds["name"] = BASE_MIDPOINT_NAME + ds["name"][0]
    return data
