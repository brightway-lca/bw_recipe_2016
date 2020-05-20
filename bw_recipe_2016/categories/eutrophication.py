from ..base import ReCiPe2016
from ..strategies import (
    name_matcher,
    match_single,
    complete_method_name,
    final_method_name,
)
from ..strategies.eutrophication import add_water_category
from ..strategies.ozone_formation import drop_last_name_component
from functools import partial


class FreshwaterEutrophication(ReCiPe2016):
    name_mapping = {
        "phosphorus (p)": "phosphorus",
        "phosphate (po43-)": "phosphate",
        "Phosphoric acid": "phosphoric acid",
    }
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "freshwater eutrophication",
        "FEP",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            add_water_category,
            drop_last_name_component,
            partial(match_single, other=self.biosphere,),
            final_method_name,
        ]


class MarineEutrophication(ReCiPe2016):
    name_mapping = {
        "n": "nitrogen",
        "nh4+": "ammonium, ion",
        "nh3": "ammonia",
        "no": "nitric oxide",
        "no2": "nitrogen dioxide",
        "no3": "nitrate",
        "nox": "nitrogen oxides",
    }
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "marine eutrophication", "MEP")

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            add_water_category,
            drop_last_name_component,
            partial(match_single, other=self.biosphere,),
            final_method_name,
        ]
