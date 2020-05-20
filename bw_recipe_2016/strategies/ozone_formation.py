from .. import BASE_MIDPOINT_NAME


def drop_last_name_component(data):
    for ds in data:
        ds["name"] = BASE_MIDPOINT_NAME + ds["name"][:-1]
    return data
