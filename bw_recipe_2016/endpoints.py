from bw2data import methods, Method
from . import BASE_MIDPOINT_NAME, BASE_ENDPOINT_NAME, FILENAME, get_biosphere_database
from copy import copy
from .categories.resources import FossilResourceScarcityEndpoint
from collections import defaultdict


NAME_MAPPING = {
    ("Acidification - Terrestrial ecosystems", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Terrestrial Acidification",),
    ),
    ("Acidification - Terrestrial ecosystems", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Terrestrial Acidification",),
    ),
    ("Acidification - Terrestrial ecosystems", "Individualist"): (
        "Terrestrial ecosystems",
        ("Terrestrial Acidification",),
    ),
    ("Eutrophication - Freshwater ecosystems", "Egalitarian"): (
        "Freshwater ecosystems",
        ("Freshwater Eutrophication",),
    ),
    ("Eutrophication - Freshwater ecosystems", "Hierarchist"): (
        "Freshwater ecosystems",
        ("Freshwater Eutrophication",),
    ),
    ("Eutrophication - Freshwater ecosystems", "Individualist"): (
        "Freshwater ecosystems",
        ("Freshwater Eutrophication",),
    ),
    ("Eutrophication - Marine ecosystems", "Egalitarian"): (
        "Marine ecosystems",
        ("Marine eutrophication",),
    ),
    ("Eutrophication - Marine ecosystems", "Hierarchist"): (
        "Marine ecosystems",
        ("Marine eutrophication",),
    ),
    ("Eutrophication - Marine ecosystems", "Individualist"): (
        "Marine ecosystems",
        ("Marine eutrophication",),
    ),
    ("Fine particulate matter formation - Human health", "Egalitarian"): (
        "Human health",
        ("Particulate Matter Formation", "Egalitarian"),
    ),
    ("Fine particulate matter formation - Human health", "Hierarchist"): (
        "Human health",
        ("Particulate Matter Formation", "Hierarchist"),
    ),
    ("Fine particulate matter formation - Human health", "Individualist"): (
        "Human health",
        ("Particulate Matter Formation", "Individualist"),
    ),
    ("Global Warming - Freshwater ecosystems", "Egalitarian"): (
        "Freshwater ecosystems",
        ("Global Warming", "1000 year timescale", "Egalitarian"),
    ),
    ("Global Warming - Freshwater ecosystems", "Hierarchist"): (
        "Freshwater ecosystems",
        ("Global Warming", "100 year timescale", "Hierarchist"),
    ),
    ("Global Warming - Freshwater ecosystems", "Individualist"): (
        "Freshwater ecosystems",
        ("Global Warming", "20 year timescale", "Individualist"),
    ),
    ("Global Warming - Human health", "Egalitarian"): (
        "Human health",
        ("Global Warming", "1000 year timescale", "Egalitarian"),
    ),
    ("Global Warming - Human health", "Hierarchist"): (
        "Human health",
        ("Global Warming", "100 year timescale", "Hierarchist"),
    ),
    ("Global Warming - Human health", "Individualist"): (
        "Human health",
        ("Global Warming", "20 year timescale", "Individualist"),
    ),
    ("Global Warming - Terrestrial ecosystems", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Global Warming", "1000 year timescale", "Egalitarian"),
    ),
    ("Global Warming - Terrestrial ecosystems", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Global Warming", "100 year timescale", "Hierarchist"),
    ),
    ("Global Warming - Terrestrial ecosystems", "Individualist"): (
        "Terrestrial ecosystems",
        ("Global Warming", "20 year timescale", "Individualist"),
    ),
    ("Ionzing Radiation - Human health", "Egalitarian"): (
        "Human health",
        ("Ionizing Radiation", "Egalitarian"),
    ),
    ("Ionzing Radiation - Human health", "Hierarchist"): (
        "Human health",
        ("Ionizing Radiation", "Hierarchist"),
    ),
    ("Ionzing Radiation - Human health", "Individualist"): (
        "Human health",
        ("Ionizing Radiation", "Individualist"),
    ),
    ("Land use - occupation", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Land occupation",),
    ),
    ("Land use - occupation", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Land occupation",),
    ),
    ("Land use - occupation", "Individualist"): (
        "Terrestrial ecosystems",
        ("Land occupation",),
    ),
    ("Land use - transformation", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Land transformation",),
    ),
    ("Land use - transformation", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Land transformation",),
    ),
    ("Land use - transformation", "Individualist"): (
        "Terrestrial ecosystems",
        ("Land transformation",),
    ),
    ("Photochemical ozone formation - Human health", "Egalitarian"): (
        "Human health",
        ("Ozone Formation", "Damage to Humans"),
    ),
    ("Photochemical ozone formation - Human health", "Hierarchist"): (
        "Human health",
        ("Ozone Formation", "Damage to Humans"),
    ),
    ("Photochemical ozone formation - Human health", "Individualist"): (
        "Human health",
        ("Ozone Formation", "Damage to Humans"),
    ),
    ("Photochemical ozone formation - Terrestrial ecosystems", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Ozone Formation", "Damage to Ecosystems"),
    ),
    ("Photochemical ozone formation - Terrestrial ecosystems", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Ozone Formation", "Damage to Ecosystems"),
    ),
    ("Photochemical ozone formation - Terrestrial ecosystems", "Individualist"): (
        "Terrestrial ecosystems",
        ("Ozone Formation", "Damage to Ecosystems"),
    ),
    ("Stratospheric ozone depletion - Human health", "Egalitarian"): (
        "Human health",
        ("Stratospheric Ozone Depletion", "Infinite timescale", "Egalitarian"),
    ),
    ("Stratospheric ozone depletion - Human health", "Hierarchist"): (
        "Human health",
        ("Stratospheric Ozone Depletion", "100 year timescale", "Hierarchist"),
    ),
    ("Stratospheric ozone depletion - Human health", "Individualist"): (
        "Human health",
        ("Stratospheric Ozone Depletion", "20 year timescale", "Individualist"),
    ),
    ("Toxicity - Freshwater ecosystems", "Egalitarian"): (
        "Freshwater ecosystems",
        ("Ecotoxicity", "Freshwater", "Egalitarian"),
    ),
    ("Toxicity - Freshwater ecosystems", "Hierarchist"): (
        "Freshwater ecosystems",
        ("Ecotoxicity", "Freshwater", "Hierarchist"),
    ),
    ("Toxicity - Freshwater ecosystems", "Individualist"): (
        "Freshwater ecosystems",
        ("Ecotoxicity", "Freshwater", "Individualist"),
    ),
    ("Toxicity - Human health (cancer)", "Egalitarian"): (
        "Human health",
        ("Toxicity", "Carcinogenic", "Egalitarian"),
    ),
    ("Toxicity - Human health (cancer)", "Hierarchist"): (
        "Human health",
        ("Toxicity", "Carcinogenic", "Hierarchist"),
    ),
    ("Toxicity - Human health (cancer)", "Individualist"): (
        "Human health",
        ("Toxicity", "Carcinogenic", "Individualist"),
    ),
    ("Toxicity - Human health (non-cancer)", "Egalitarian"): (
        "Human health",
        ("Toxicity", "Non-carcinogenic", "Egalitarian"),
    ),
    ("Toxicity - Human health (non-cancer)", "Hierarchist"): (
        "Human health",
        ("Toxicity", "Non-carcinogenic", "Hierarchist"),
    ),
    ("Toxicity - Human health (non-cancer)", "Individualist"): (
        "Human health",
        ("Toxicity", "Non-carcinogenic", "Individualist"),
    ),
    ("Toxicity - Marine ecosystems", "Egalitarian"): (
        "Marine ecosystems",
        ("Ecotoxicity", "Marine", "Egalitarian"),
    ),
    ("Toxicity - Marine ecosystems", "Hierarchist"): (
        "Marine ecosystems",
        ("Ecotoxicity", "Marine", "Hierarchist"),
    ),
    ("Toxicity - Marine ecosystems", "Individualist"): (
        "Marine ecosystems",
        ("Ecotoxicity", "Marine", "Individualist"),
    ),
    ("Toxicity - Terrestrial ecosystems", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Ecotoxicity", "Terrestrial", "Egalitarian"),
    ),
    ("Toxicity - Terrestrial ecosystems", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Ecotoxicity", "Terrestrial", "Hierarchist"),
    ),
    ("Toxicity - Terrestrial ecosystems", "Individualist"): (
        "Terrestrial ecosystems",
        ("Ecotoxicity", "Terrestrial", "Individualist"),
    ),
    ("Water consumption - human health", "Egalitarian"): (
        "Human health",
        ("Water consumption",),
    ),
    ("Water consumption - human health", "Hierarchist"): (
        "Human health",
        ("Water consumption",),
    ),
    ("Water consumption - human health", "Individualist"): (
        "Human health",
        ("Water consumption",),
    ),
    ("Water consumption - terrestrial ecosystems", "Egalitarian"): (
        "Terrestrial ecosystems",
        ("Water consumption",),
    ),
    ("Water consumption - terrestrial ecosystems", "Hierarchist"): (
        "Terrestrial ecosystems",
        ("Water consumption",),
    ),
    ("Water consumption - terrestrial ecosystems", "Individualist"): (
        "Terrestrial ecosystems",
        ("Water consumption",),
    ),
    ("Water consumption -aquatic ecosystems", "Egalitarian"): (
        "Freshwater ecosystems",
        ("Water consumption",),
    ),
    ("Water consumption -aquatic ecosystems", "Hierarchist"): (
        "Freshwater ecosystems",
        ("Water consumption",),
    ),
    ("Water consumption -aquatic ecosystems", "Individualist"): (
        "Freshwater ecosystems",
        ("Water consumption",),
    ),
    ("Mineral resource scarcity", "Egalitarian"): (
        "Resources",
        ("Mineral Resource Scarcity", 'Egalitarian'),
    ),
    ("Mineral resource scarcity", "Hierarchist"): (
        "Resources",
        ("Mineral Resource Scarcity", 'Hierarchist'),
    ),
    ("Mineral resource scarcity", "Individualist"): (
        "Resources",
        ("Mineral Resource Scarcity", 'Individualist'),
    ),
}


def create_single_endpoints(data):
    formatted = [
        {label: value for label, value in zip(data[1][0], row[:5])}
        for row in data[1][1:33]
        if row[1]
    ]

    # Split land occupation and transformation for easier processing
    new = []
    for elem in formatted:
        if (
            elem["Midpoint to endpoint conversion factor"]
            == "Land use - occupation and transformation"
        ):
            elem["Midpoint to endpoint conversion factor"] = "Land use - occupation"
            new_elem = copy(elem)
            new_elem[
                "Midpoint to endpoint conversion factor"
            ] = "Land use - transformation"
            new.append(new_elem)

    formatted.extend(new)

    # Correct inconsistent labels
    for elem in formatted:
        elem["Individualist"] = elem.pop("Individualistic")
        elem["Hierarchist"] = elem.pop("Hierarchic")

    for elem in formatted:
        for perspective in ("Individualist", "Hierarchist", "Egalitarian"):
            section, ending = NAME_MAPPING[
                (elem["Midpoint to endpoint conversion factor"]), perspective
            ]
            midpoint = BASE_MIDPOINT_NAME + ending
            assert midpoint in methods
            endpoint = BASE_ENDPOINT_NAME + (section,) + ending
            if endpoint[-1] != perspective:
                endpoint += (perspective,)

            endpoint_method = Method(endpoint)
            endpoint_method.register(
                unit=elem["unit"], description="", filename=FILENAME
            )
            endpoint_method.write(
                [(flow, cf * elem[perspective]) for flow, cf in Method(midpoint).load()]
            )

    frse = FossilResourceScarcityEndpoint(get_biosphere_database())
    frse.apply_strategies()
    frse.drop_unlinked()
    frse.write_methods(overwrite=True)


def create_aggregated_endpoints():
    UNIT_MAPPING = {
        'Freshwater ecosystems': 'Species∙yr',
        'Resources': 'USD (2013)',
        'Human health': 'DALY',
        'Marine ecosystems': 'Species∙yr',
        'Terrestrial ecosystems': 'Species∙yr',
    }

    sections = ['Freshwater ecosystems', 'Resources', 'Human health', 'Marine ecosystems', 'Terrestrial ecosystems']
    perspectives = ["Egalitarian", "Hierarchist", "Individualist"]

    for section in sections:
        for perspective in perspectives:
            name = BASE_ENDPOINT_NAME + (section, "Aggregated", perspective)
            metadata = {
                'unit': UNIT_MAPPING[section],
                'filename': FILENAME,
                'description': ''
            }
            children = [m for m in methods if m[:len(BASE_ENDPOINT_NAME)] == BASE_ENDPOINT_NAME and perspective in m and section in m and "Aggregated" not in m]
            combine_methods(name, children, metadata)

    for perspective in perspectives:
        name = BASE_ENDPOINT_NAME + ("Ecosystems", "Aggregated", perspective)
        metadata = {
            'unit': 'Species∙yr',
            'filename': FILENAME,
            'description': ''
        }
        children = [m for m in methods if m[:len(BASE_ENDPOINT_NAME)] == BASE_ENDPOINT_NAME and perspective in m and m[3] in ('Freshwater ecosystems', 'Marine ecosystems', 'Terrestrial ecosystems') and m[4] == 'Aggregated']
        combine_methods(name, children, metadata)


def combine_methods(name, methods, metadata):
    data = defaultdict(float)

    method = Method(name)
    method.register(**metadata)
    for child in methods:
        for cf, amount in Method(child).load():
            data[cf] += amount

    method.write([(k, v) for k, v in data.items()])
