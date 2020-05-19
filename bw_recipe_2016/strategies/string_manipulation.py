import re


multiple = re.compile(r"^(.*)\((.*)\)$")


def fix_unit_string(data):
    """Clean up some minor typos.

    Turns `(kg CO2eq/ kg GHG)` into `kg CO2eq/kg GHG`."""

    def fix(s):
        if s.startswith("("):
            s = s[1:]
        if s.endswith(")"):
            s = s[:-1]
        return s.replace("/ ", "/")

    for ds in data:
        ds["unit"] = fix(ds["unit"])
    return data


def split_synonyms(data):
    """Split synonyms given in one string. Also makes sure ``synonyms`` exists, has no trailing whitespace, and is a list.

    E.g. ``dinitrogen oxide (nitrous oxide)`` to ``["dinitrogen oxide", "nitrous oxide"]``,"""
    for ds in data:
        for cf in ds["exchanges"]:
            if "synonyms" in cf:
                match = multiple.match(cf["synonyms"])
                if match:
                    cf["synonyms"] = [x.strip() for x in match.groups()]
                elif not isinstance(cf["synonyms"], list):
                    cf["synonyms"] = [cf["synonyms"].strip()]
            else:
                cf["synonyms"] = []
    return data


def more_synonyms(data):
    """Expand list of possible synonyms from ["foo bar"] to ["foo-bar"]"""

    def moar(s):
        yield s
        if " " in s:
            yield s.replace(" ", "-")

    for ds in data:
        for cf in ds["exchanges"]:
            cf["synonyms"] = [s for item in cf["synonyms"] for s in moar(item)]
    return data


def fix_perspective_string(data):
    """Fix inconsistent perspective names"""
    mapping = {
        "I": "individualist",
        "H": "hierarchist",
        "E": "egalitarian",
    }
    for ds in data.values():
        ds["perspective"] = (mapping.get(ds["perspective"], ds["perspective"])).title()
    return data
