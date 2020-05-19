from bw_recipe_2016.strategies.matching import match_cas_number, normalized_cas


def test_normalized_cas():
    assert normalized_cas(7440473) == normalized_cas(7440473.0)
    assert normalized_cas(7440473) == normalized_cas("7440-47-3")
    assert normalized_cas("7440-47-3") == normalized_cas("0007440-47-3")


# def match_cas_number(data, other):
#     """Match based on `CAS number <https://en.wikipedia.org/wiki/CAS_Registry_Number>`. Uses the key ``CAS number`` for elements in both ``data`` and ``other``."""
#     lookup = {normalized_cas[elem["CAS number"]]: elem.key for elem in other if "CAS number" in elem}
#     for ds in data:
#         for cf in unlinked(ds['exchanges']):
#             try:
#                 cf['input'] = lookup(cf['CAS number'])
#             except KeyError:
#                 pass
#     return data
