def drop_last_name_component(data, config):
    for ds in data:
        ds["name"] = config.base_midpoint_name + ds["name"][:-1]
    return data
