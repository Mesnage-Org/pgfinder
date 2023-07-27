import json
import sys
from pathlib import Path
from typing import Dict

MASS_LIB_DIR = Path(sys.modules["pgfinder"].__file__).parent / "masses"


def mass_library_index() -> Dict:
    return json.load(open(MASS_LIB_DIR / "index.json"))


def load_mass_library(file) -> str:
    return open(MASS_LIB_DIR / file, "rb").read()
