from bw_recipe_2016.strategies import (
    fix_unit_string,
    split_synonyms,
    more_synonyms,
    fix_perspective_string,
    name_matcher,
)


def test_fix_unit_string():
    def wrap(s):
        return [{"unit": s}]

    assert fix_unit_string(wrap("(kg CO2eq/ kg GHG)")) == wrap("kg CO2eq/kg GHG")
    assert fix_unit_string(wrap("kg CO2eq/kg GHG")) == wrap("kg CO2eq/kg GHG")


def test_split_synonyms():
    def wrap(s):
        return [{"exchanges": [{"synonyms": s}]}]

    assert split_synonyms(wrap("dinitrogen oxide (nitrous oxide)")) == wrap(
        ["dinitrogen oxide", "nitrous oxide"]
    )
    assert split_synonyms(wrap("dinitrogen oxide nitrous oxide ")) == wrap(
        ["dinitrogen oxide nitrous oxide"]
    )
    assert split_synonyms([{"exchanges": [{}]}]) == [{"exchanges": [{"synonyms": []}]}]


def test_more_synoyms():
    given = [{"exchanges": [{"synonyms": ["foo bar", "baz_2"]}]}]
    expected = [{"exchanges": [{"synonyms": ["foo bar", "foo-bar", "baz_2"]}]}]
    assert more_synonyms(given) == expected


def test_fix_perspective_string():
    given = {
        1: {"perspective": "Hierarchist"},
        2: {"perspective": "EGALITARIAN"},
        3: {"perspective": "I"},
    }
    expected = {
        1: {"perspective": "Hierarchist"},
        2: {"perspective": "Egalitarian"},
        3: {"perspective": "Individualist"},
    }
    assert fix_perspective_string(given) == expected


def test_name_matcher():
    given = [{'exchanges': [{"name": "FOO"}, {"name": "Baz"}]}]
    expected = [{'exchanges': [{"name": "bar"}, {"name": "Baz"}]}]
    mapping = {"foo": "bar"}
    assert name_matcher(given, mapping) == expected
