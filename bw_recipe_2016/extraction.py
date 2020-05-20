from . import FILENAME
from .excel_extraction import ExcelExtractor
from pathlib import Path

DIRPATH = Path(__file__).parent.resolve()
FILEPATH = DIRPATH / "data" / FILENAME


def maybe_number(x):
    if x in ("-",):
        return 0.0
    else:
        return float(x)


class ReCiPeExtractor:
    """Extract ReCiPe data to a common format.

    Usage example:

        RE = ReCiPeExtractor()
        RE.extract()
        RE.harmonize()

    Creates ``self.data``,  a dictionary of form:

        {
            category name (str): {
                'unit': unit (str),
                'perspective': individualist|hierarchist|egalitarian (str),
                'cfs': [{
                    'amount': float,
                    'name': str,
                    'synonyms': [str],
                    'CAS number': str,
                    'formula': str,
                    'compartment': str,
                    'subcompartment': str,
                }]
            }
        }

    This does not do any data matching steps (i.e. changing names to match other nomenclatures). All data transformation is done with strategy functions, in line with ``bw2io`` practice.

    """

    config = {
        "Global Warming": {
            "column_labels": ["name", "synonyms", "formula"],
            "indices": (3, 6),
        },
        "Stratospheric ozone depletion": {
            "column_labels": ["name", "synonyms"],
            "indices": (2, 5),
        },
        "Ionizing radiation": {
            "column_labels": ["name", "synonyms", "dummy", "categories"],
            "indices": (4, 7),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Human damage ozone formation": {
            "column_labels": ["CAS number", "name", "dummy", "dummy"],
            "indices": (4, 5),
        },
        "Particulate matter formation": {
            "column_labels": ["dummy", "name"],
            "indices": (2, 5),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Ecosyste damage ozone formation": {
            "column_labels": ["CAS number", "name", "dummy", "dummy"],
            "indices": (4, 5),
        },
        "Terrestrial acidification": {"column_labels": ["name"], "indices": (2, 3),},
        "Freshwater eutrophication": {
            "column_labels": ["name", "compartment"],
            "indices": (2, 3),
        },
        "Marine eutrophication": {
            "column_labels": ["name", "compartment"],
            "indices": (2, 3),
            "key_function": lambda s, i: "Marine eutrophication",
        },
        "Land transformation": {
            "column_labels": ["name", "categories"],
            "indices": (2, 3),
            "offset": 2,
        },
        "Land occupation": {
            "column_labels": ["name", "categories"],
            "indices": (2, 3),
            "offset": 2,
        },
        "Mineral resource scarcity": {
            "column_labels": ["name", "element"],
            "indices": (2, 5),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Fossil resource scarcity": {
            "column_labels": ["name", "dummy"],
            "indices": (2, 3),
        },
        "Terrestrial ecotoxicity": {
            "column_labels": ["CAS number", "name", "dummy", "compartment"],
            "indices": (4, 7),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Freshwater ecotoxicity": {
            "column_labels": ["CAS number", "name", "dummy", "dummy", "compartment"],
            "indices": (5, 8),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Marine ecotoxicity": {
            "column_labels": ["CAS number", "name", "dummy", "dummy", "compartment"],
            "indices": (5, 8),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Human carcinogenic toxicity": {
            "column_labels": ["CAS number", "name", "dummy", "dummy", "compartment"],
            "indices": (5, 8),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
        "Human noncarcinogenic toxicity": {
            "column_labels": ["CAS number", "name", "dummy", "dummy", "compartment"],
            "indices": (5, 8),
            "key_function": lambda s, i: (s[0][i], s[2][i]),
        },
    }

    def __init__(self, filepath=None):
        self.filepath = filepath or FILEPATH

    def extract(self):
        self.data = ExcelExtractor.extract(self.filepath)
        self.categories = [o[0] for o in self.data]

    def extract_column(self, data, column_labels, cf_index):
        return [
            {**dict(zip(column_labels, row)), "amount": maybe_number(row[cf_index])}
            for row in data
        ]

    def filter_rows(self, data, required_column):
        return (row for row in data if row[required_column] not in {"", None})

    def harmonize_generic(
        self, sheet, column_labels, indices, offset=3, key_function=None
    ):
        if key_function is None:
            key_function = lambda sheet, index: sheet[0][index]
        return {
            key_function(sheet, index): {
                "unit": sheet[1][index],
                "perspective": sheet[2][index],
                "cfs": self.extract_column(
                    self.filter_rows(sheet[offset:], index),  # Skip section headers
                    column_labels=column_labels,
                    cf_index=index,
                ),
            }
            for index in range(*indices)
        }

    def get_index(self, label):
        return next(i for i, o in enumerate(self.data) if o[0] == label)

    def harmonize(self):
        for k, v in self.config.items():
            index = self.categories.index(k)
            self.data[index] = self.harmonize_generic(self.data[index][1], **v)


def extract_recipe():
    RE = ReCiPeExtractor()
    RE.extract()
    RE.harmonize()
    return RE.data
