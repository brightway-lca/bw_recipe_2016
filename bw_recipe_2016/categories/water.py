from ..base import ReCiPe2016
from ..strategies import match_single, final_method_name, check_duplicate_cfs
from functools import partial

FLOWS = [
    ("Water", ("water",)),
    ("Water", ("water", "fossil well")),
    ("Water", ("water", "ground-")),
    ("Water", ("water", "ground-, long-term")),
    ("Water", ("water", "surface water")),
    ("Water, cooling, unspecified natural origin", ("natural resource", "in water")),
    ("Water, lake", ("natural resource", "in water")),
    ("Water, river", ("natural resource", "in water")),
    (
        "Water, turbine use, unspecified natural origin",
        ("natural resource", "in water"),
    ),
    # ('Water, unspecified natural origin', ('natural resource', 'fossil well')),
    ("Water, unspecified natural origin", ("natural resource", "in ground")),
    ("Water, unspecified natural origin", ("natural resource", "in water")),
    ("Water, well, in ground", ("natural resource", "in water")),
]


class WaterConsumption(ReCiPe2016):
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "water depletion", "WDP")

    def __init__(self, data, biosphere, version=2):
        super().__init__(None, biosphere, version)
        self.set_data()
        self.strategies = [
            partial(match_single, other=self.biosphere),
            final_method_name,
            partial(check_duplicate_cfs, biosphere=biosphere),
        ]

    def set_data(self):
        # Provided data is effectively useless, do it ourselves
        self.data = [
            {
                "name": self.config.base_midpoint_name + ("Water consumption",),
                "unit": "m3-eq.",
                "filename": self.config.filename,
                "description": "",
                "exchanges": [
                    {
                        "amount": (1 if categories[0] == "natural resource" else -1),
                        "name": name,
                        "categories": categories,
                    }
                    for name, categories in FLOWS
                ],
            }
        ]
