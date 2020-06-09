from pathlib import Path

DIRPATH = Path(__file__).parent.resolve()


class Config:
    mapping = {0: "1.0 (20161004)", 1: "1.1 (20170929)", 2: "1.1 (20180117)"}
    filenames = {
        0: "ReCiPe2016_CFs_v1.0_20161004.xlsx",
        1: "ReCiPe2016_CFs_v1.1_20170929.xlsx",
        2: "ReCiPe2016_CFs_v1.1_20180117.xlsx",
    }

    def __init__(self, version=2):
        assert version in (0, 1, 2), "Invalid version"
        self.base_name = ("ReCiPe 2016",) + (self.mapping[version],)
        self.base_midpoint_name = self.base_name + ("Midpoint",)
        self.base_endpoint_name = self.base_name + ("Endpoint",)
        self.filename = self.filenames[version]
        self.filepath = DIRPATH / "data" / self.filename
