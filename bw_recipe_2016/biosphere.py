import bw2data as bd


def get_biosphere_database():
    ERROR = "ReCiPe 2016 only tested for ecoinvent biosphere flows; install base ecoinvent data"
    assert "biosphere3" in bd.databases, ERROR
    return list(bd.Database("biosphere3"))


def fix_acrolein():
    ERROR = "ReCiPe 2016 only tested for ecoinvent biosphere flows; install base ecoinvent data"
    assert "biosphere3" in bd.databases, ERROR

    bio = bd.Database("biosphere3")
    if bio.metadata.get("acrolein fixed"):
        return

    flow = bd.get_activity(("biosphere3", "fa8bd05b-015d-5a82-878c-bde991551695"))
    flow["CAS number"] = "107-02-8"
    flow.save()

    bio.metadata["acrolein fixed"] = True
    bd.databases.flush()
