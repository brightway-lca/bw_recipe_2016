from ..base import ReCiPe2016
from ..strategies import (
    add_air_category,
    check_duplicate_cfs,
    chemid_cas_to_name_mapping,
    chemid_name_mapping,
    final_method_name,
    fix_unit_string,
    generic_reformat,
    match_cas_number,
    match_single,
    name_matcher,
)
from ..strategies.particulate_matter import complete_method_name
from ..strategies.toxicity import (
    set_toxicity_categories,
    correct_ion_cas_registry_numbers,
    drop_unmatchable_ions,
    drop_homonyms,
)
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
        # There are many ions of molybdenum, don't just pick one to apply to all
        # "Mo(VI)": "Molybdenum",
        "Ni(II)": "Nickel, ion",
        # "Sn(II)": , Ecoinvent only has Tin(IV)
        # "V(V)":  Ecoinvent only has V(III)
        "Zn(II)": "Zinc, ion",
    }
    previous_reference = (
        "ReCiPe Midpoint (E) V1.13",
        "terrestrial ecotoxicity",
        "TETPinf",
    )

    def __init__(self, data, biosphere, version=2):
        super().__init__(data, biosphere, version)
        self.strategies = [
            partial(generic_reformat, config=self.config),
            fix_unit_string,
            drop_unmatchable_ions,
            drop_homonyms,
            correct_ion_cas_registry_numbers,
            partial(name_matcher, mapping=self.name_mapping),
            set_toxicity_categories,
            partial(complete_method_name, config=self.config),
            partial(match_single, other=self.biosphere,),
            partial(match_cas_number, other=self.biosphere, exact_category=True),
            chemid_name_mapping,
            partial(match_single, other=self.biosphere,),
            chemid_cas_to_name_mapping,
            partial(match_single, other=self.biosphere,),
            final_method_name,
            partial(check_duplicate_cfs, biosphere=biosphere),
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
