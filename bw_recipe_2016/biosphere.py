import bw2data as bd


def get_biosphere_database():
    ERROR = "ReCiPe 2016 only tested for ecoinvent biosphere flows; install base ecoinvent data"
    assert "biosphere3" in bd.databases, ERROR
    return list(bd.Database("biosphere3"))
