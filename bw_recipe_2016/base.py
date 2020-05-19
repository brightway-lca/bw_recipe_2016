from bw2data import get_activity, Method
from bw2io.importers.base_lcia import LCIAImporter
from .strategies import (
    fix_perspective_string,
    fix_unit_string,
    generic_reformat,
    more_synonyms,
    split_synonyms,
)


class ReCiPe2016(LCIAImporter):
    """Base import class for ReCiPe 2016. Each impact category will be a subclass.

    The internal data format for LCIA methods is:

    .. code-block:: python

        [
            {
                'name': tuple; name of LCIA method,
                'description': str,
                'filename': str,
                'unit': str,
                'exchanges': [  # CFs
                    'input': tuple; key of biosphere flow,
                    'amount': float,
                    # plus any applicable uncertainty fields
                ]
            }
        ]

    We don't do extraction in the ``Importer`` class, but in a separate function, as we don't want to extract each time a subclass is used.

    """

    global_strategies = [
        fix_perspective_string,
        generic_reformat,
        split_synonyms,
        more_synonyms,
        fix_unit_string,
    ]

    def compare_to_previous(self):
        if not hasattr(self, "previous_reference"):
            raise ValueError("No previous reference method found")
        names_found_in_data = {
            get_activity(cf["input"])["name"].lower()
            for ds in self.data
            for cf in ds["exchanges"]
            if cf.get("input")
        }
        names_missing_in_data = {
            cf["name"].lower()
            for ds in self.data
            for cf in ds["exchanges"]
            if not cf.get("input")
        }
        names_in_reference = {
            get_activity(key)["name"].lower()
            for key, _ in Method(self.previous_reference).load()
        }
        return {
            "found": names_found_in_data,
            "missing": names_missing_in_data,
            "reference": names_in_reference,
        }
