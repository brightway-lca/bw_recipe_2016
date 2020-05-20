from .string_manipulation import (
    fix_unit_string,
    split_synonyms,
    more_synonyms,
    fix_perspective_string,
)
from .formatting import (
    generic_reformat,
    complete_method_name,
    tupleize_categories,
)
from .matching import (
    name_matcher,
    match_multiple,
    match_cas_number,
    match_single,
    chemid_name_mapping,
    chemid_cas_to_name_mapping,
)
from .global_warming import add_air_category
from .ionizing_radiation import fix_water_categories
from .names import final_method_name
