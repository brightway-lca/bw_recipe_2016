def complete_method_name(data, config):
    for ds in data:
        ds["name"] = config.base_midpoint_name + ds["name"][0]
    return data
