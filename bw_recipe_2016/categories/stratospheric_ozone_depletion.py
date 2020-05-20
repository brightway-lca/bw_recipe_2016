from ..base import ReCiPe2016
from ..strategies import (
    name_matcher,
    match_multiple,
    add_air_category,
    complete_method_name,
    final_method_name,
)
from functools import partial


class StratosphericOzoneDepletion(ReCiPe2016):
    name_mapping = {
        "cfc-113": "ethane, 1,1,2-trichloro-1,2,2-trifluoro-, cfc-113",
        "cfc-114": "ethane, 1,2-dichloro-1,1,2,2-tetrafluoro-, cfc-114",
        "cfc-115": "ethane, chloropentafluoro-, cfc-115",
        "hcfc-123": "ethane, 2,2-dichloro-1,1,1-trifluoro-, hcfc-123",
        "hcfc-124": "ethane, 2-chloro-1,1,1,2-tetrafluoro-, hcfc-124",
        "carbon tetrachloride": "methane, tetrachloro-, r-10",
        "ccl4": "Methane, tetrachloro-, R-10",
        "cfc-11": "methane, trichlorofluoro-, cfc-11",
        "cfc-12": "methane, dichlorodifluoro-, cfc-12",
        "ch3br": "methane, bromo-, halon 1001",
        "ch3ccl3": "Ethane, 1,1,1-trichloro-, HCFC-140",
        "ch3cl": "methane, monochloro-, r-40",
        "halon-1211": "methane, bromochlorodifluoro-, halon 1211",
        "halon-1301": "methane, bromotrifluoro-, halon 1301",
        "n2o": "dinitrogen monoxide",
        "hcfc-141b": "ethane, 1,1-dichloro-1-fluoro-, hcfc-141b",
        "hcfc-142b": "ethane, 1-chloro-1,1-difluoro-, hcfc-142b",
        "hcfc-22": "methane, chlorodifluoro-, hcfc-22",
    }
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "ozone depletion", "ODPinf")

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            add_air_category,
            complete_method_name,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]
