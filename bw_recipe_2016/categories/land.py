from ..base import ReCiPe2016
from ..strategies import match_multiple, generic_reformat, final_method_name
from ..strategies.land import (
    complete_method_name,
    set_unit,
    reset_categories,
    add_missing_flows,
)
from functools import partial


class LandTransformation(ReCiPe2016):
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "natural land transformation",
        "NLTP",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = [
            generic_reformat,
            set_unit,
            partial(complete_method_name, name="Land transformation"),
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]


class LandOccupation(ReCiPe2016):
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "agricultural land occupation",
        "ALOP",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = [
            generic_reformat,
            set_unit,
            add_missing_flows,
            reset_categories,
            partial(complete_method_name, name="Land occupation"),
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]
