from .. import BASE_ENDPOINT_NAME, FILENAME
from ..base import ReCiPe2016
from ..strategies import (
    fix_unit_string,
    generic_reformat,
    match_single,
    match_multiple,
    name_matcher,
    final_method_name,
)
from ..strategies.particulate_matter import complete_method_name
from ..strategies.resources import (
    remove_asterisk,
    add_fossil_natural_resource_category,
    add_mineral_natural_resource_category,
    add_synonyms,
    fossil_method_name,
)
from functools import partial
from bw2io.importers.base_lcia import LCIAImporter


class MineralResourceScarcity(ReCiPe2016):
    name_mapping = {
        "Aluminium": [
            "aluminium, in ground",
            r"aluminium, 24% in bauxite, 11% in crude ore, in ground",
        ],
        "cobalt": ["cobalt, co 5.0e-2%, in mixed ore, in ground", "cobalt, in ground",],
        "copper": [
            r"copper, 0.52% in sulfide, cu 0.27% and mo 8.2e-3% in crude ore, in ground",
            r"copper, 0.59% in sulfide, cu 0.22% and mo 8.2e-3% in crude ore, in ground",
            r"copper, 0.97% in sulfide, cu 0.36% and mo 4.1e-2% in crude ore, in ground",
            r"copper, 0.99% in sulfide, cu 0.36% and mo 8.2e-3% in crude ore, in ground",
            r"copper, 1.13% in sulfide, cu 0.76% and ni 0.76% in crude ore, in ground",
            r"copper, 1.18% in sulfide, cu 0.39% and mo 8.2e-3% in crude ore, in ground",
            r"copper, 1.42% in sulfide, cu 0.81% and mo 8.2e-3% in crude ore, in ground",
            r"copper, 2.19% in sulfide, cu 1.83% and mo 8.2e-3% in crude ore, in ground",
            "copper, cu 0.2%, in mixed ore, in ground",
            "copper, cu 0.38%, in mixed ore, in ground",
            "copper, cu 6.8e-1%, in mixed ore, in ground",
            "copper, in ground",
            r"cu, cu 3.2e+0%, pt 2.5e-4%, pd 7.3e-4%, rh 2.0e-5%, ni 2.3e+0% in ore, in ground",
            r"cu, cu 5.2e-2%, pt 4.8e-4%, pd 2.0e-4%, rh 2.4e-5%, ni 3.7e-2% in ore, in ground",
        ],
        "bentonite clay": "clay, bentonite, in ground",
        "gold": [
            r"gold, au 1.0e-7%, in mixed ore, in ground",
            r"gold, au 1.1e-4%, ag 4.2e-3%, in ore, in ground",
            r"gold, au 1.3e-4%, ag 4.6e-5%, in ore, in ground",
            r"gold, au 1.4e-4%, in ore, in ground",
            r"gold, au 1.8e-4%, in mixed ore, in ground",
            r"gold, au 2.1e-4%, ag 2.1e-4%, in ore, in ground",
            r"gold, au 4.3e-4%, in ore, in ground",
            r"gold, au 4.9e-5%, in ore, in ground",
            r"gold, au 5.4e-4%, ag 1.5e-5%, in ore, in ground",
            r"gold, au 6.7e-4%, in ore, in ground",
            r"gold, au 6.8e-4%, ag 1.5e-4%, in ore, in ground",
            r"gold, au 7.1e-4%, in ore, in ground",
            r"gold, au 9.7e-4%, in mixed ore, in ground",
            r"gold, au 9.7e-5%, ag 7.6e-5%, in ore, in ground",
            "gold, in ground",
        ],
        "lead": [
            r"lead, 5.0% in sulfide, pb 3.0%, zn, ag, cd, in, in ground",
            "lead, in ground",
            "lead, pb 0.014%, in mixed ore, in ground",
            "lead, pb 3.6e-1%, in mixed ore, in ground",
        ],
        "manganese": [
            r"manganese, 35.7% in sedimentary deposit, 14.2% in crude ore, in ground",
            "manganese, in ground",
        ],
        "molybdenum": [
            r"molybdenum, 0.010% in sulfide, mo 8.2e-3% and cu 1.83% in crude ore, in ground",
            r"molybdenum, 0.014% in sulfide, mo 8.2e-3% and cu 0.81% in crude ore, in ground",
            r"molybdenum, 0.016% in sulfide, mo 8.2e-3% and cu 0.27% in crude ore, in ground",
            r"molybdenum, 0.022% in sulfide, mo 8.2e-3% and cu 0.22% in crude ore, in ground",
            r"molybdenum, 0.022% in sulfide, mo 8.2e-3% and cu 0.36% in crude ore, in ground",
            r"molybdenum, 0.025% in sulfide, mo 8.2e-3% and cu 0.39% in crude ore, in ground",
            r"molybdenum, 0.11% in sulfide, mo 4.1e-2% and cu 0.36% in crude ore, in ground",
        ],
        "nickel": [
            r"ni, ni 2.3e+0%, pt 2.5e-4%, pd 7.3e-4%, rh 2.0e-5%, cu 3.2e+0% in ore, in ground",
            r"ni, ni 3.7e-2%, pt 4.8e-4%, pd 2.0e-4%, rh 2.4e-5%, cu 5.2e-2% in ore, in ground",
            r"nickel, 1.13% in sulfide, ni 0.76% and cu 0.76% in crude ore, in ground",
            r"nickel, 1.98% in silicates, 1.04% in crude ore, in ground",
            "nickel, in ground",
            "nickel, ni 2.5e+0%, in mixed ore, in ground",
        ],
        "Graphite": "Metamorphous rock, graphite containing, in ground",
        "Iron": "Iron, in ground",
        "Iron ore": [
            r"Iron, 46% in ore, 25% in crude ore, in ground",
            r"Iron, 72% in magnetite, 14% in crude ore, in ground",
        ],
        "Potash": "Potassium, in ground",
        "Pumice and pumicite": "Pumice, in ground",
        "Titanium dioxide": [
            r"TiO2, 54% in ilmenite, 18% in crude ore, in ground",
            r"TiO2, 54% in ilmenite, 2.6% in crude ore, in ground",
            r"TiO2, 95% in rutile, 0.40% in crude ore, in ground",
        ],
        "palladium": [
            r"Palladium, Pd 1.6E-6%, in mixed ore, in ground",
            "Palladium, in ground",
            r"Pd, Pd 2.0E-4%, Pt 4.8E-4%, Rh 2.4E-5%, Ni 3.7E-2%, Cu 5.2E-2% in ore, in ground",
            r"Pd, Pd 7.3E-4%, Pt 2.5E-4%, Rh 2.0E-5%, Ni 2.3E+0%, Cu 3.2E+0% in ore, in ground",
        ],
        "Platinum-group metals": [
            "Ruthenium, in ground",
            r"Rhodium, Rh 1.6E-7%, in mixed ore, in ground",
            "Rhodium, in ground",
            r"Rh, Rh 2.0E-5%, Pt 2.5E-4%, Pd 7.3E-4%, Ni 2.3E+0%, Cu 3.2E+0% in ore, in ground",
            r"Rh, Rh 2.4E-5%, Pt 4.8E-4%, Pd 2.0E-4%, Ni 3.7E-2%, Cu 5.2E-2% in ore, in ground",
            r"Platinum, Pt 4.7E-7%, in mixed ore, in ground",
            "Platinum, in ground",
            r"pt, pt 2.5e-4%, pd 7.3e-4%, rh 2.0e-5%, ni 2.3e+0%, cu 3.2e+0% in ore, in ground",
            r"pt, pt 4.8e-4%, pd 2.0e-4%, rh 2.4e-5%, ni 3.7e-2%, cu 5.2e-2% in ore, in ground",
            "Osmium, in ground",
            "Iridium, in ground",
        ],
        "silver": [
            r"silver, 0.007% in sulfide, ag 0.004%, pb, zn, cd, in, in ground",
            r"silver, 0.01% in crude ore, in ground",
            "silver, 3.2ppm in sulfide, ag 1.2ppm, cu and te, in crude ore, in ground",
            "silver, ag 1.5e-4%, au 6.8e-4%, in ore, in ground",
            "silver, ag 1.5e-5%, au 5.4e-4%, in ore, in ground",
            "silver, ag 1.8e-6%, in mixed ore, in ground",
            "silver, ag 2.1e-4%, au 2.1e-4%, in ore, in ground",
            "silver, ag 4.2e-3%, au 1.1e-4%, in ore, in ground",
            "silver, ag 4.6e-5%, au 1.3e-4%, in ore, in ground",
            "silver, ag 5.4e-3%, in mixed ore, in ground",
            "silver, ag 7.6e-5%, au 9.7e-5%, in ore, in ground",
            "silver, ag 9.7e-4%, in mixed ore, in ground",
            "silver, in ground",
        ],
        "tin": [
            r"tin, 79% in cassiterite, 0.1% in crude ore, in ground",
            "tin, in ground",
        ],
        "Rare earth metals": [
            "Yttrium, in ground",
            "Scandium, in ground",
            r"Cerium, 24% in bastnasite, 2.4% in crude ore, in ground",
            "Cerium, in ground",
            "Dysprosium, in ground",
            "Erbium, in ground",
            r"Europium, 0.06% in bastnasite, 0.006% in crude ore, in ground",
            "Europium, in ground",
            r"Gadolinium, 0.15% in bastnasite, 0.015% in crude ore, in ground",
            "Gadolinium, in ground",
            "Holmium, in ground",
            "Lanthanum, in ground",
            r"Lanthanum, 7.2% in bastnasite, 0.72% in crude ore, in ground",
            "Lutetium, in ground",
            r"Neodymium, 4% in bastnasite, 0.4% in crude ore, in ground",
            "Neodymium, in ground",
            r"Praseodymium, 0.42% in bastnasite, 0.042% in crude ore, in ground",
            "Praseodymium, in ground",
            "Samarium, in ground",
            r"Samarium, 0.3% in bastnasite, 0.03% in crude ore, in ground",
            "Terbium, in ground",
            "Thulium, in ground",
            "Ytterbium, in ground",
        ],
        "Zirconium minerals": [
            r"Zirconium, 50% in zircon, 0.39% in crude ore, in ground",
            "Zirconium, in ground",
        ],
        "gallium": [r"Gallium, 0.014% in bauxite, in ground", "Gallium, in ground",],
        "indium": [
            r"Indium, 0.005% in sulfide, In 0.003%, Pb, Zn, Ag, Cd, in ground",
            "Indium, in ground",
        ],
        "tantalum": [
            r"Tantalum, 81.9% in tantalite, 1.6E-4% in crude ore, in ground",
            "Tantalum, in ground",
        ],
        "kaolin": [r"Kaolinite, 24% in crude ore, in ground", "Kaolinite, in ground",],
        "cesium": "caesium, in ground",
        "zinc": [
            "zinc, in ground",
            r"zinc, 9.0% in sulfide, zn 5.3%, pb, ag, cd, in, in ground",
            "zinc, zn 0.63%, in mixed ore, in ground",
            "zinc, zn 3.1%, in mixed ore, in ground",
        ],
    }
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "metal depletion", "MDP")

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            remove_asterisk,
            partial(name_matcher, mapping=self.name_mapping),
            add_synonyms,
            complete_method_name,
            add_mineral_natural_resource_category,
            partial(match_single, other=self.biosphere,),
            final_method_name,
        ]


class FossilResourceScarcity(ReCiPe2016):
    name_mapping = {
        "Crude oil": "Oil, crude, in ground",
        "Natural gas": "Gas, natural, in ground",
        "Hard coal": "Coal, hard, unspecified, in ground",
        "Brown coal": "Coal, brown, in ground",
        "Peat": "Peat, in ground",
    }
    previous_reference = ("ReCiPe Midpoint (E) V1.13", "fossil depletion", "FDP")

    def __init__(self, data, biosphere):
        self.data = data
        self.biosphere = biosphere
        self.strategies = self.global_strategies + [
            partial(name_matcher, mapping=self.name_mapping),
            fossil_method_name,
            add_fossil_natural_resource_category,
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]


class FossilResourceScarcityEndpoint(LCIAImporter):
    data = [
        {
            "name": BASE_ENDPOINT_NAME + ("Resources", "Fossil resource scarcity", "Individualist"),
            "unit": "USD2013/(kg or nM3)",
            "filename": FILENAME,
            "description": "",
            "exchanges": [
                {
                    "name": "Oil, crude, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.46,
                },
                {
                    "name": "Gas, natural, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.3,
                },
                {
                    "name": "Coal, hard, unspecified, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.03,
                },
                {
                    "name": "Coal, brown, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.0,
                },
                {
                    "name": "Peat, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.0,
                },
            ],
        },
        {
            "name": BASE_ENDPOINT_NAME + ("Resources", "Fossil resource scarcity", "Hierarchist"),
            "unit": "USD2013/(kg or nM3)",
            "filename": FILENAME,
            "description": "",
            "exchanges": [
                {
                    "name": "Oil, crude, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.46,
                },
                {
                    "name": "Gas, natural, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.3,
                },
                {
                    "name": "Coal, hard, unspecified, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.03,
                },
                {
                    "name": "Coal, brown, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.0,
                },
                {
                    "name": "Peat, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.0,
                },
            ],
        },
        {
            "name": BASE_ENDPOINT_NAME
            + ("Resources", "Fossil resource scarcity", "Egalitarian"),
            "unit": "USD2013/(kg or nM3)",
            "filename": FILENAME,
            "description": "",
            "exchanges": [
                {
                    "name": "Oil, crude, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.46,
                },
                {
                    "name": "Gas, natural, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.3,
                },
                {
                    "name": "Coal, hard, unspecified, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.03,
                },
                {
                    "name": "Coal, brown, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.03,
                },
                {
                    "name": "Peat, in ground",
                    "categories": ("natural resource",),
                    "amount": 0.03,
                },
            ],
        },
    ]

    def __init__(self, biosphere):
        self.biosphere = biosphere
        self.strategies = [
            partial(match_multiple, other=self.biosphere,),
            final_method_name,
        ]
