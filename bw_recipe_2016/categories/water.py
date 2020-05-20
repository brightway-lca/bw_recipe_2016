from .. import BASE_MIDPOINT_NAME, FILENAME
from ..base import ReCiPe2016
from ..strategies import match_single, final_method_name
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
    # Provided data is effectively useless, do it ourselves
    data = [
        {
            "name": BASE_MIDPOINT_NAME + ("Water consumption",),
            "unit": "m3-eq.",
            "filename": FILENAME,
            "description": "",
            "exchanges": [{"amount": 1, "name": x, "categories": y} for x, y in FLOWS],
        }
    ]

    def __init__(self, data, biosphere):
        self.biosphere = biosphere
        self.strategies = [
            partial(match_single, other=self.biosphere),
            final_method_name,
        ]
