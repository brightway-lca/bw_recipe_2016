__all__ = (
    "add_recipe_2016",
    "Config",
    "create_aggregated_endpoints",
    "create_single_endpoints",
    "delete_recipe_2016",
    "extract_recipe",
    "fix_acrolein",
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


from .version import version as __version__
from .biosphere import get_biosphere_database, fix_acrolein
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
from .config import Config
from .endpoints import create_single_endpoints, create_aggregated_endpoints


def add_recipe_2016(version=2):
    fix_acrolein()

    delete_recipe_2016(version)
    biosphere = get_biosphere_database()
    data = extract_recipe(version)
    if version > 0:
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
    else:
        categories = {
            (2, GlobalWarming),
            (3, StratosphericOzoneDepletion),
            (4, IonizingRadiation),
            (5, OzoneFormationHumans),
            (6, ParticulateMatterFormation),
            (7, OzoneFormationEcosystems),
            (8, TerrestrialAcidification),
            (9, FreshwaterEutrophication),
            (10, TerrestrialEcotoxicity),
            (11, FreshwaterEcotoxicity),
            (12, MarineEcotoxicity),
            (13, HumanCarcinogenicToxicity),
            (14, HumanNoncarcinogenicToxicity),
            (15, LandOccupation),
            (16, WaterConsumption),
            (17, MineralResourceScarcity),
            (18, FossilResourceScarcity),
        }
    for i, c in categories:
        print("Adding {}".format(c.__name__))
        category = c(data[i], biosphere, version)
        category.apply_strategies(verbose=False)
        try:
            category.drop_unlinked(verbose=False)
            category.write_methods(overwrite=True, verbose=False)
        except TypeError:
            category.drop_unlinked()
            category.write_methods(overwrite=True)

    print("Adding single endpoints")
    create_single_endpoints(data[1], version)
    print("Adding aggregated endpoints")
    create_aggregated_endpoints(version)


def delete_recipe_2016(version=2):
    from bw2data import methods

    config = Config(version)
    all_methods = list(methods)
    for method_name in all_methods:
        if method_name[: len(config.base_name)] == config.base_name:
            del methods[method_name]
        if len(method_name) < 3:
            continue
        older_version = (method_name[0], "v" + method_name[1]) + method_name[2:]
        if older_version[: len(config.base_name)] == config.base_name:
            del methods[older_version]
