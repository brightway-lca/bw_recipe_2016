from ..base import ReCiPe2016
from ..strategies import (
    add_air_category,
    check_duplicate_cfs,
    final_method_name,
    fix_unit_string,
    generic_reformat,
    match_multiple,
    name_matcher,
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

    def __init__(self, data, biosphere, version=2):
        super().__init__(data, biosphere, version)
        self.strategies = [
            partial(generic_reformat, config=self.config),
            fix_unit_string,
            partial(name_matcher, mapping=self.name_mapping),
            partial(complete_method_name, config=self.config),
            add_air_category,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
            partial(check_duplicate_cfs, biosphere=biosphere),
        ]
