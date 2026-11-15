"""Check whether an EFDA label year shows in the summer image of the same year.

For each group of label pixels it prints the median change of NBR between
two consecutive summer composites, and the share of pixels whose NBR dropped
by more than a threshold. If a label of year t appeared only in the image of
year t+1, the 24->25 column would be high for the 2024 labels. It is not.

Run:  python -m forest.check_label_lag --candidate 1
"""

import argparse

import numpy as np
import pandas as pd
import rasterio

from forest.config import FOREST_RESULTS_DIR, SENTINEL2_DIR
from forest.data import efda
from forest.data.sentinel2 import candidate_bounds

YEARS = (2023, 2024, 2025)
THRESHOLD = 0.15  # NBR drop that counts as "vegetation lost"


def nbr_on_label_grid(folder, year: int) -> np.ndarray:
    """NBR = (NIR - SWIR22) / (NIR + SWIR22), averaged per 3x3 block.

    One block of 3x3 image pixels covers exactly one 30 m label pixel.
    Band order in the files: B02, B03, B04, B08, B11, B12.
    """
    with rasterio.open(folder / f"s2_{year}.tif") as source:
        nir = source.read(4).astype("float32")
        swir = source.read(6).astype("float32")
    nbr = (nir - swir) / np.maximum(nir + swir, 1)
    rows, columns = nbr.shape
    return nbr.reshape(rows // 3, 3, columns // 3, 3).mean(axis=(1, 3))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--candidate", type=int, default=1)
    arguments = parser.parse_args()

    bounds = candidate_bounds(arguments.candidate)
    folder = SENTINEL2_DIR / f"aoi_{arguments.candidate:02d}"

    nbr = {year: nbr_on_label_grid(folder, year) for year in YEARS}
    drop_2024 = nbr[2023] - nbr[2024]  # positive = loss between summer 2023 and 2024
    drop_2025 = nbr[2024] - nbr[2025]

    forest = efda.read_forest_mask(bounds) == 1
    disturbed = {year: efda.read_disturbance(year, bounds) == 1 for year in (2022, 2023, 2024)}
    agent_2024 = efda.read_agent(2024, bounds)
    stable = forest & ~disturbed[2022] & ~disturbed[2023] & ~disturbed[2024]

    groups = {
        "stable forest (control)": stable,
        "EFDA 2024, all": disturbed[2024],
        "EFDA 2024, harvest": disturbed[2024] & (agent_2024 == 3),
        "EFDA 2024, wind/bark beetle": disturbed[2024] & (agent_2024 == 1),
        "EFDA 2023, all": disturbed[2023],
        "EFDA 2022, all": disturbed[2022],
    }
    rows = []
    for name, mask in groups.items():
        rows.append({
            "group": name,
            "pixels": int(mask.sum()),
            "median_drop_2023_2024": float(np.median(drop_2024[mask])),
            "median_drop_2024_2025": float(np.median(drop_2025[mask])),
            f"share_above_{THRESHOLD}_2023_2024": float(np.mean(drop_2024[mask] > THRESHOLD)),
            f"share_above_{THRESHOLD}_2024_2025": float(np.mean(drop_2025[mask] > THRESHOLD)),
        })
    table = pd.DataFrame(rows)
    print(table.to_string(index=False, float_format="%.3f"))
    output = FOREST_RESULTS_DIR / f"label_lag_aoi_{arguments.candidate:02d}.csv"
    table.to_csv(output, index=False, float_format="%.4f")
    print(f"\nSaved: {output}")


if __name__ == "__main__":
    main()
