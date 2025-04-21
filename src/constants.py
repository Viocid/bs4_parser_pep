from pathlib import Path

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = "https://docs.python.org/3/"
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = "%d.%m.%Y %H:%M:%S"
CODING = "utf-8"
FIRST_EL = 0
FIRST = 1
PEPS_URL = "https://peps.python.org/"
EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}
STATUS_ID = -1
STATUS = 1
STATUS_TABLE = 2
