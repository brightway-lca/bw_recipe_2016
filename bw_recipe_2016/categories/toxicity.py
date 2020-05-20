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
from ..strategies.particulate_matter import complete_method_name
from ..strategies.toxicity import set_toxicity_categories
from functools import partial


class TerrestrialEcotoxicity(ReCiPe2016):
    # Have to fix names manually because CAS numbers for metal ions are wrong!
    name_mapping = {
        "Ag(I)": "silver, ion",
        "As(V)": "arsenic, ion",
        "Cd(II)": "cadmium, ion",
        "Cr(III)": "chromium, ion",
        "Cr(VI)": "Chromium VI",
        # "Cu(II)": , Ecoinvent only has Copper(I)
        "Mo(VI)": "Molybdenum",
        "Ni(II)": "Nickel, ion",
        # "Sn(II)": , Ecoinvent only has Tin(IV)
        "V(V)": "Vanadium, ion",
        "Zn(II)": "Zinc, ion",
    }
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "terrestrial ecotoxicity",
        "TETPinf",
    )

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = [
            generic_reformat,
            fix_unit_string,
            partial(name_matcher, mapping=self.name_mapping),
            set_toxicity_categories,
            complete_method_name,
            partial(match_multiple, other=self.biosphere,),
            partial(match_cas_number, other=self.biosphere,),
            chemid_name_mapping,
            partial(match_multiple, other=self.biosphere,),
            chemid_cas_to_name_mapping,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]


class FreshwaterEcotoxicity(TerrestrialEcotoxicity):
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "freshwater ecotoxicity",
        "FETPinf",
    )


class MarineEcotoxicity(TerrestrialEcotoxicity):
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "marine ecotoxicity", "METPinf")


class HumanCarcinogenicToxicity(TerrestrialEcotoxicity):
    previous_reference = (("ReCiPe Midpoint (E) V1.13", "human toxicity", "HTPinf"),)


class HumanNoncarcinogenicToxicity(TerrestrialEcotoxicity):
    previous_reference = (("ReCiPe Midpoint (E) V1.13", "human toxicity", "HTPinf"),)
