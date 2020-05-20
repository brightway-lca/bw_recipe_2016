from ..base import ReCiPe2016
from ..strategies import (
    name_matcher,
    match_multiple,
    add_air_category,
    complete_method_name,
    final_method_name,
)
from ..strategies.ozone_formation import drop_last_name_component
from functools import partial


class TerrestrialAcidification(ReCiPe2016):
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
        "h2so4 (sulphuric acid)": "sulfuric acid",
    }
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "terrestrial acidification",
        "TAP500",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            add_air_category,
            drop_last_name_component,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]
