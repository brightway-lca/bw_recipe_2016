from copy import deepcopy
from collections import defaultdict
from ..chemidplus import canonical_cas, ChemIDPlus


def unlinked(elems):
    return (obj for obj in elems if not obj.get("input"))


def name_matcher(data, mapping):
    def change_name(a, b):
        a["name"] = b.lower()
        return a

    mapping = {k.lower(): v for k, v in mapping.items()}

    for ds in data:
        to_add, to_remove = [], []
        for cf in ds["exchanges"]:
            match = mapping.get(cf["name"].lower())
            if not match:
                continue
            elif isinstance(match, list):
                to_remove.append(cf)
                to_add.extend([change_name(deepcopy(cf), name) for name in match])
            else:
                cf["name"] = match.lower()
        ds["exchanges"] = [cf for cf in ds["exchanges"] if cf not in to_remove] + to_add
    return data


def add_flow(a, b):
    """Add reference to ``b`` in ``a``"""
    a["input"] = b.key
    return a


def category_match(a, b):
    """Return bool, whether the starting categories in a match the categories in b.

    For example, ``category_match({'categories': ('foo',)}, {"categories": ('foo', 'bar')})`` is true."""
    return tuple(a["categories"][: len(b["categories"])]) == tuple(b["categories"])


def category_match_exact(a, b):
    return tuple(a["categories"]) == tuple(b["categories"])


def match_single(data, other):
    """Match to a single, specified category"""
    other_dict = {(ds["name"].lower(), tuple(ds["categories"])): ds.key for ds in other}

    for ds in data:
        for cf in unlinked(ds["exchanges"]):
            try:
                cf["input"] = other_dict[(cf["name"].lower(), cf.get("categories"))]
            except KeyError:
                for synonym in cf.get("synonyms", []):
                    try:
                        cf["input"] = other_dict[
                            (synonym.lower(), cf.get("categories"))
                        ]
                        break
                    except KeyError:
                        pass
    return data


def match_multiple(data, other):
    """Match based on name and possible synonyms."""
    other_dict = defaultdict(list)
    for ds in other:
        other_dict[ds["name"].lower()].append(ds)

    for ds in data:
        to_add, to_remove = [], []
        for cf in unlinked(ds["exchanges"]):
            if cf["name"].lower() in other_dict:
                to_remove.append(cf)
                to_add.extend(
                    [
                        add_flow(deepcopy(cf), ds)
                        for ds in other_dict[cf["name"].lower()]
                        if category_match(ds, cf)
                    ]
                )
            else:
                for synonym in cf.get("synonyms", []):
                    if synonym.lower() in other_dict:
                        to_remove.append(cf)
                        to_add.extend(
                            [
                                add_flow(deepcopy(cf), o)
                                for o in other_dict[synonym.lower()]
                                if category_match(o, cf)
                            ]
                        )
        ds["exchanges"] = [cf for cf in ds["exchanges"] if cf not in to_remove] + to_add
    return data


def match_cas_number(data, other, exact_category=False):
    """Match based on `CAS number <https://en.wikipedia.org/wiki/CAS_Registry_Number>`. Uses the key ``CAS number`` for elements in both ``data`` and ``other``."""
    lookup = defaultdict(list)

    for elem in other:
        if not elem.get("CAS number"):
            continue
        lookup[canonical_cas(elem.get("CAS number"))].append(elem)

    category_function = category_match_exact if exact_category else category_match

    for ds in data:
        to_add, to_remove = [], []
        for cf in unlinked(ds["exchanges"]):
            try:
                possibles = lookup[canonical_cas(cf["CAS number"])]
                to_add.extend(
                    [
                        add_flow(deepcopy(cf), o)
                        for o in possibles
                        if category_function(o, cf)
                    ]
                )
                to_remove.append(cf)
            except KeyError:
                pass

        ds["exchanges"] = [cf for cf in ds["exchanges"] if cf not in to_remove] + to_add

    return data


def chemid_name_mapping(data, search=False):
    # Currently hardcoded with ecoinvent flow names
    c = ChemIDPlus()
    for ds in data:
        for cf in unlinked(ds["exchanges"]):
            translated = c.match(cf["name"], search=search)
            if translated:
                cf["name"] = translated
    return data


def chemid_cas_to_name_mapping(data):
    # Currently hardcoded with ecoinvent flow names
    c = ChemIDPlus()
    for ds in data:
        for cf in unlinked(ds["exchanges"]):
            if canonical_cas(cf.get("CAS number")):
                try:
                    cf["name"] = c.match_cas(cf["CAS number"])
                except KeyError:
                    continue
    return data
