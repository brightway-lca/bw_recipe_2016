from ..base import ReCiPe2016
from ..strategies import (
    match_multiple,
    generic_reformat,
    final_method_name,
    check_duplicate_cfs,
)
from ..strategies.land import (
    add_missing_flows,
    complete_method_name,
    reset_categories,
    set_unit,
)
from functools import partial


class LandTransformation(ReCiPe2016):
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "natural land transformation",
        "NLTP",
    )

    def __init__(self, data, biosphere, version=2):
        super().__init__(data, biosphere, version)
        self.strategies = [
            partial(generic_reformat, config=self.config),
            set_unit,
            reset_categories,
            partial(
                complete_method_name, name="Land transformation", config=self.config
            ),
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
            partial(check_duplicate_cfs, biosphere=biosphere),
        ]


class LandOccupation(ReCiPe2016):
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "agricultural land occupation",
        "ALOP",
    )

    def __init__(self, data, biosphere, version=2):
        super().__init__(data, biosphere, version)
        self.strategies = [
            partial(generic_reformat, config=self.config),
            set_unit,
            add_missing_flows,
            reset_categories,
            partial(complete_method_name, name="Land occupation", config=self.config),
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
            partial(check_duplicate_cfs, biosphere=biosphere),
        ]
