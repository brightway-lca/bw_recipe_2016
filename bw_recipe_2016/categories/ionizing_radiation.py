from ..base import ReCiPe2016
from ..strategies import (
    check_duplicate_cfs,
    final_method_name,
    fix_water_categories,
    match_multiple,
    name_matcher,
    tupleize_categories,
)
from ..strategies.particulate_matter import complete_method_name
from functools import partial


class IonizingRadiation(ReCiPe2016):
    name_mapping = {
        "ch3cl": "methane, monochloro-, r-40",
        "ch3br": "methane, bromo-, halon 1001",
        "actinides, unspecified": "actinides, radioactive, unspecified",
        "cs-134": "cesium-134",
        "cs-137": "cesium-137",
        "co-58": "cobalt-58",
        "h-3": "hydrogen-3, tritium",
        "cm alphaa": "curium alpha",
        "pb-210": "lead-210",
        "pu-238": "plutonium-238",
        "pu-239": "plutonium-239",
        "mn-54": "manganese-54",
        "ra-226a": "radium-226",
        "ra-226": "radium-226",
        "sb-124": "antimony-124",
        "i-133": "iodine-133",
        "po-210": "polonium-210",
        "ag-110m": "silver-110",
        "pu alpha": "plutonium-alpha",
        "pu alphaa": "plutonium-alpha",
        "u-238a": "uranium-238",
        "xe-133": "xenon-133",
        # Ecoinvent calls the same substance three names, because reasons...
        "U-238a": ["Uranium", "Uranium alpha", "Uranium-238"],
    }
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "ionising radiation", "IRP_HE")

    def __init__(self, data, biosphere, version=2):
        super().__init__(data, biosphere, version)
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            fix_water_categories,
            tupleize_categories,
            partial(complete_method_name, config=self.config),
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
            partial(check_duplicate_cfs, biosphere=biosphere),
        ]
