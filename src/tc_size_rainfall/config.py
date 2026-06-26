from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"
FIGURE_INPUT_DIR = DATA_DIR / "figure_inputs"

OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"

# Study domain: Middle Americas
DOMAIN = {
    "lon_min": -130,
    "lon_max": -60,
    "lat_min": 5,
    "lat_max": 35,
}

BASINS = ["NA", "EP"]
QUADRANTS = ["RNE", "RNW", "RSW", "RSE"]

CATEGORY_ORDER = [
    "TD",
    "TS",
    "MIN_HUR",
    "MAJ_HUR",
]

CATEGORY_LABELS = {
    "TD": "TD",
    "TS": "TS",
    "MIN HUR": "Minor hurricane",
    "MIN_HUR": "Minor hurricane",
    "MAJ HUR": "Major hurricane",
    "MAJ_HUR": "Major hurricane",
}

SEASON_GROUPS = {
    "MJJ": [5, 6],
    "JAS": [7, 8, 9],
    "ON": [10, 11],
}
