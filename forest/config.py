"""Paths and constants for the forest-loss proof of concept."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input data (not tracked by Git).
FOREST_DATA_DIR = PROJECT_ROOT / "data"
EFDA_DIR = FOREST_DATA_DIR / "efda"
SENTINEL2_DIR = FOREST_DATA_DIR / "sentinel2"

# Small outputs: tables and figures (tracked by Git).
FOREST_RESULTS_DIR = PROJECT_ROOT / "results"

# Everything is kept in one metric coordinate system, the one EFDA uses.
CRS = "EPSG:3035"

# European Forest Disturbance Atlas v3.0: one band per year, 1985 = band 1.
EFDA_FIRST_YEAR = 1985
EFDA_LAST_YEAR = 2024
EFDA_PIXEL_M = 30
EFDA_NODATA = 255
EFDA_AGENTS = {1: "wind_bark_beetle", 2: "fire", 3: "harvest"}

# Sentinel-2 is resampled to 10 m, so 3 x 3 image pixels fill one label pixel.
SENTINEL2_PIXEL_M = 10
PIXELS_PER_LABEL = EFDA_PIXEL_M // SENTINEL2_PIXEL_M

# Bands kept from Sentinel-2 L2A: output name -> asset name in the catalogue.
SENTINEL2_BANDS = {
    "B02": "blue",
    "B03": "green",
    "B04": "red",
    "B08": "nir",
    "B11": "swir16",
    "B12": "swir22",
}

# Summer composites: leaves are on, snow is gone, clouds are rarer.
SEASON_START = "06-01"
SEASON_END = "08-31"

# Side of a study area. 46 080 m is a whole number of label pixels (1536)
# and of 256-pixel image patches (18), so nothing has to be cropped later.
PATCH_PIXELS = 256
AOI_SIZE_M = 46_080

# Years used to rank candidate areas (Sentinel-2 L2A is complete from 2019).
RANKING_YEARS = tuple(range(2019, 2025))
