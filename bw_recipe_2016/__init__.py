__all__ = (
    "add_recipe_2016",
    "create_aggregated_endpoints",
    "create_single_endpoints",
    "delete_recipe_2016",
    "extract_recipe",
    "FossilResourceScarcity",
    "FossilResourceScarcityEndpoint",
    "FreshwaterEcotoxicity",
    "FreshwaterEutrophication",
    "get_biosphere_database",
    "GlobalWarming",
    "HumanCarcinogenicToxicity",
    "HumanNoncarcinogenicToxicity",
    "IonizingRadiation",
    "LandOccupation",
    "MarineEcotoxicity",
    "MarineEutrophication",
    "MineralResourceScarcity",
    "OzoneFormationEcosystems",
    "OzoneFormationHumans",
    "ParticulateMatterFormation",
    "StratosphericOzoneDepletion",
    "TerrestrialAcidification",
    "TerrestrialEcotoxicity",
    "WaterConsumption",
)


BASE_NAME = ("ReCiPe 2016", "v1.1 (20180117)")
BASE_MIDPOINT_NAME = BASE_NAME + ("Midpoint",)
BASE_ENDPOINT_NAME = BASE_NAME + ("Endpoint",)
FILENAME = "ReCiPe2016_CFs_v1.1_20180117.xlsx"


from .version import version as __version__

from .biosphere import get_biosphere_database
from .extraction import extract_recipe
from .categories import (
    FossilResourceScarcity,
    FossilResourceScarcityEndpoint,
    FreshwaterEcotoxicity,
    FreshwaterEutrophication,
    GlobalWarming,
    HumanCarcinogenicToxicity,
    HumanNoncarcinogenicToxicity,
    IonizingRadiation,
    LandOccupation,
    LandTransformation,
    MarineEcotoxicity,
    MarineEutrophication,
    MineralResourceScarcity,
    OzoneFormationEcosystems,
    OzoneFormationHumans,
    ParticulateMatterFormation,
    StratosphericOzoneDepletion,
    TerrestrialAcidification,
    TerrestrialEcotoxicity,
    WaterConsumption,
)
from .endpoints import create_single_endpoints, create_aggregated_endpoints


def add_recipe_2016():
    biosphere = get_biosphere_database()
    data = extract_recipe()
    categories = {
        (2, GlobalWarming),
        (3, StratosphericOzoneDepletion),
        (4, IonizingRadiation),
        (5, OzoneFormationHumans),
        (6, ParticulateMatterFormation),
        (7, OzoneFormationEcosystems),
        (8, TerrestrialAcidification),
        (9, FreshwaterEutrophication),
        (10, MarineEutrophication),
        (11, TerrestrialEcotoxicity),
        (12, FreshwaterEcotoxicity),
        (13, MarineEcotoxicity),
        (14, HumanCarcinogenicToxicity),
        (15, HumanNoncarcinogenicToxicity),
        (16, LandTransformation),
        (17, LandOccupation),
        (18, WaterConsumption),
        (19, MineralResourceScarcity),
        (20, FossilResourceScarcity),
    }
    for i, c in categories:
        category = c(data[i], biosphere)
        category.apply_strategies()
        category.drop_unlinked()
        category.write_methods(overwrite=True)

    create_single_endpoints(data[1])
    create_aggregated_endpoints()


def delete_recipe_2016():
    from bw2data import methods

    all_methods = list(methods)
    for method_name in all_methods:
        if method_name[: len(BASE_NAME)] == BASE_NAME:
            del methods[method_name]
