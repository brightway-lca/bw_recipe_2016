from ..base import ReCiPe2016
from ..strategies import (
    name_matcher,
    match_multiple,
    add_air_category,
    complete_method_name,
    final_method_name,
)
from ..strategies.global_warming import add_biomass_stock_cfs
from functools import partial


class GlobalWarming(ReCiPe2016):
    name_mapping = {
        "carbon dioxide": "carbon dioxide, fossil",
        "carbon monoxide": "carbon monoxide, fossil",
        "carbon tetrachloride": "methane, tetrachloro-, r-10",
        "cfc-11": "methane, trichlorofluoro-, cfc-11",
        "cfc-113": "ethane, 1,1,2-trichloro-1,2,2-trifluoro-, cfc-113",
        "cfc-114": "ethane, 1,2-dichloro-1,1,2,2-tetrafluoro-, cfc-114",
        "cfc-115": "ethane, chloropentafluoro-, cfc-115",
        "cfc-12": "methane, dichlorodifluoro-, cfc-12",
        "cfc-13": "methane, chlorotrifluoro-, cfc-13",
        "fossil methane": "methane, fossil",
        "halon 1001": "methane, bromo-, halon 1001",
        "halon-1211": "methane, bromochlorodifluoro-, halon 1211",
        "halon-1301": "methane, bromotrifluoro-, halon 1301",
        "hcfc-123": "ethane, 2,2-dichloro-1,1,1-trifluoro-, hcfc-123",
        "hcfc-124": "ethane, 2-chloro-1,1,1,2-tetrafluoro-, hcfc-124",
        "hcfc-140": "ethane, 1,1,1-trichloro-, hcfc-140",
        "hcfc-141b": "ethane, 1,1-dichloro-1-fluoro-, hcfc-141b",
        "hcfc-142b": "ethane, 1-chloro-1,1-difluoro-, hcfc-142b",
        "hcfc-21": "methane, dichlorofluoro-, hcfc-21",
        "hcfc-22": "methane, chlorodifluoro-, hcfc-22",
        "hfc-125": "ethane, pentafluoro-, hfc-125",
        "hfc-134a": "ethane, 1,1,1,2-tetrafluoro-, hfc-134a",
        "hfc-143a": "ethane, 1,1,1-trifluoro-, hfc-143a",
        "hfc-152a": "ethane, 1,1-difluoro-, hfc-152a",
        "hfc-23": "methane, trifluoro-, hfc-23",
        "hfc-32": "methane, difluoro-, hfc-32",
        "methane": "methane, non-fossil",
        "methyl bromide": "methane, bromo-, halon 1001",
        "methyl chloride": "methane, monochloro-, r-40",
        "methylene chloride": "methane, dichloro-, hcc-30",
        "nitrogen trifluoride": "nitrogen fluoride",
        "nitrous oxide": "dinitrogen monoxide",
        "pfc-116": "ethane, hexafluoro-, hfc-116",
        "pfc-14": "methane, tetrafluoro-, r-14",
        "pfc-41-12": "perfluoropentane",
        "sulphur hexafluoride": "sulfur hexafluoride",
        "n2o": "dinitrogen monoxide",
    }
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "climate change", "GWP500")

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            add_biomass_stock_cfs,
            add_air_category,
            complete_method_name,
            # drop_known_missing,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]
