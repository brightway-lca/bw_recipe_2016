from ..base import ReCiPe2016
from ..strategies import (
    add_air_category,
    chemid_cas_to_name_mapping,
    chemid_name_mapping,
    fix_unit_string,
    generic_reformat,
    match_cas_number,
    match_multiple,
    name_matcher,
    final_method_name,
)
from ..strategies.ozone_formation import drop_last_name_component
from functools import partial


class OzoneFormationHumans(ReCiPe2016):
    name_mapping = {
        "nitrogen oxides (as nitrogen dioxide)": "nitrogen oxides",
        "nmvoc (non-methane volatile organic chemicals)": "nmvoc, non-methane volatile organic compounds, unspecified origin",
        "ethylene": "ethene",
        "trichloroethylene": "ethene, trichloro-",
        "no": "nitric oxide",
        "no3": "nitrate",
    }
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "photochemical oxidant formation",
        "POFP",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = [
            generic_reformat,
            fix_unit_string,
            partial(name_matcher, mapping=self.name_mapping),
            add_air_category,
            drop_last_name_component,
            # drop_known_missing,
            partial(match_multiple, other=self.biosphere,),
            partial(match_cas_number, other=self.biosphere,),
            chemid_name_mapping,
            partial(match_multiple, other=self.biosphere,),
            chemid_cas_to_name_mapping,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]


class OzoneFormationEcosystems(OzoneFormationHumans):
    pass
