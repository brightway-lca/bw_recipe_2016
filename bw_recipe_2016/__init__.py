__all__ = (
    "extract_recipe",
    "get_biosphere_database",
    "GlobalWarming",
    "StratosphericOzoneDepletion",
    "IonizingRadiation",
    "OzoneFormationHumans",
    "ParticulateMatterFormation",
    "OzoneFormationEcosystems",
    "TerrestrialAcidification",
    "MarineEutrophication",
    "FreshwaterEutrophication",
    "LandOccupation",
    'WaterConsumption',
    'MineralResourceScarcity',
    'add_recipe_2016',
)


BASE_NAME = ("ReCiPe 2016", "v1.1 (20180117)")
FILENAME = "ReCiPe2016_CFs_v1.1_20180117.xlsx"


from .version import version as __version__

from .biosphere import get_biosphere_database
from .extraction import extract_recipe
from .categories import (
    GlobalWarming,
    StratosphericOzoneDepletion,
    IonizingRadiation,
    OzoneFormationHumans,
    ParticulateMatterFormation,
    OzoneFormationEcosystems,
    TerrestrialAcidification,
    MarineEutrophication,
    FreshwaterEutrophication,
    LandTransformation,
    LandOccupation,
    WaterConsumption,
    MineralResourceScarcity,
)


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
        (16, LandTransformation),
        (17, LandOccupation),
        (18, WaterConsumption),
        (19, MineralResourceScarcity),
    }
    for i, c in categories:
        print(i)
        category = c(data[i], biosphere)
        category.apply_strategies()
        category.drop_unlinked()
        category.write_methods(overwrite=True)
