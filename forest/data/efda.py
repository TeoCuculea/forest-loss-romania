"""Read the European Forest Disturbance Atlas (EFDA) layers for Romania.

All layers share one grid: 30 m pixels in EPSG:3035. The annual layers have
40 bands, one per year from 1985 to 2024.
"""

import numpy as np
import rasterio
from rasterio.windows import Window, from_bounds

from forest.config import (
    EFDA_DIR,
    EFDA_FIRST_YEAR,
    EFDA_LAST_YEAR,
    EFDA_NODATA,
)

COUNTRY = "romania"

# Bounds are always (left, bottom, right, top) in EPSG:3035 metres.
Bounds = tuple[float, float, float, float]


def layer_path(layer: str):
    """Path of one EFDA layer, for example ``annual_disturbance``."""
    path = EFDA_DIR / f"{layer}_{COUNTRY}_v30.tif"
    if not path.is_file():
        raise FileNotFoundError(
            f"EFDA layer not found: {path}. Download Romania.zip from "
            "https://zenodo.org/records/21722408 and unpack it there."
        )
    return path


def year_to_band(year: int) -> int:
    """Band number of a year in the annual layers (1985 is band 1)."""
    if not EFDA_FIRST_YEAR <= year <= EFDA_LAST_YEAR:
        raise ValueError(f"EFDA covers {EFDA_FIRST_YEAR}-{EFDA_LAST_YEAR}, not {year}.")
    return year - EFDA_FIRST_YEAR + 1


def _window(source, bounds: Bounds | None) -> Window | None:
    """Pixel window for the given bounds; they must sit on the 30 m grid.

    A thousandth of a pixel (3 cm) is tolerated: bounds read back from a
    CSV file are rounded.
    """
    if bounds is None:
        return None
    window = from_bounds(*bounds, transform=source.transform)
    rounded = window.round_offsets().round_lengths()
    if (abs(window.col_off - rounded.col_off) > 1e-3
            or abs(window.row_off - rounded.row_off) > 1e-3):
        raise ValueError("Bounds are not aligned to the EFDA 30 m grid.")
    return rounded


def read_layer(layer: str, year: int | None = None,
               bounds: Bounds | None = None) -> np.ndarray:
    """Read one band of a layer, for the whole country or for a rectangle."""
    with rasterio.open(layer_path(layer)) as source:
        band = 1 if year is None else year_to_band(year)
        return source.read(band, window=_window(source, bounds))


def read_disturbance(year: int, bounds: Bounds | None = None) -> np.ndarray:
    """Mask of pixels disturbed in ``year``: 1 = disturbed, 0 = everything else."""
    data = read_layer("annual_disturbance", year, bounds)
    return (data == 1).astype(np.uint8)


def read_agent(year: int, bounds: Bounds | None = None) -> np.ndarray:
    """Cause of the disturbance in ``year``: 1 wind/bark beetle, 2 fire, 3 harvest, 0 none."""
    data = read_layer("disturbance_agent", year, bounds)
    return np.where(data == EFDA_NODATA, 0, data).astype(np.uint8)


def read_forest_mask(bounds: Bounds | None = None) -> np.ndarray:
    """Forest land-use mask: 1 = forest land, 0 = not forest."""
    return (read_layer("forestlanduse_mask", None, bounds) == 1).astype(np.uint8)


def grid() -> tuple[rasterio.Affine, tuple[int, int]]:
    """Transform and (rows, columns) of the country grid."""
    with rasterio.open(layer_path("forestlanduse_mask")) as source:
        return source.transform, source.shape
