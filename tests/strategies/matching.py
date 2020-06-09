from bw_recipe_2016.chemidplus import canonical_cas


def test_normalized_cas():
    assert canonical_cas(7440473) == canonical_cas(7440473.0)
    assert canonical_cas(7440473) == canonical_cas("7440-47-3")
    assert canonical_cas("7440-47-3") == canonical_cas("0007440-47-3")
