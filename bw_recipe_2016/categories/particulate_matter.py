from ..base import ReCiPe2016
from ..strategies import (
    add_air_category,
    fix_unit_string,
    generic_reformat,
    match_multiple,
    name_matcher,
    final_method_name,
)
from ..strategies.particulate_matter import complete_method_name
from functools import partial


class ParticulateMatterFormation(ReCiPe2016):
    name_mapping = {
        "no": "nitric oxide",
        "no3": "nitrate",
        "nh3": "ammonia",
        "nox": "nitrogen oxides",
        "pm2.5": "particulates, < 2.5 um",
        "no2": "nitrogen dioxide",
        # 'so': '',
        "so2": "sulfur dioxide",
        # 'so3': '',
        "sox": "sulfur oxides",
    }
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "particulate matter formation",
        "PMFP",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = [
            generic_reformat,
            fix_unit_string,
            partial(name_matcher, mapping=self.name_mapping),
            complete_method_name,
            add_air_category,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]
