"""Rank square areas of Romania by how much forest disturbance they contain.

The country is cut into cells of AOI_SIZE_M (about 46 km). For each cell the
script adds up, over RANKING_YEARS, the hectares of forest disturbed and
their cause, using EFDA. It writes a table of all forested cells and a map
with the three proposed study areas.

Usage:
    python -m forest.select_aoi
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyproj import Transformer

from forest.config import (
    AOI_SIZE_M,
    CRS,
    EFDA_AGENTS,
    EFDA_PIXEL_M,
    FOREST_RESULTS_DIR,
    RANKING_YEARS,
)
from forest.data import efda
from forest.plot_style import (
    INK,
    ORANGE,
    PAGE_WIDTH,
    SEQUENTIAL_BLUE,
    apply_style,
    save_figure,
)

CELL_PIXELS = AOI_SIZE_M // EFDA_PIXEL_M
HECTARES_PER_PIXEL = EFDA_PIXEL_M * EFDA_PIXEL_M / 10_000
MINIMUM_FOREST_SHARE = 0.40
CANDIDATES = 3


def sum_per_cell(image: np.ndarray) -> np.ndarray:
    """Add up the pixels inside each cell (partial cells at the edges are dropped)."""
    rows = image.shape[0] // CELL_PIXELS
    columns = image.shape[1] // CELL_PIXELS
    trimmed = image[:rows * CELL_PIXELS, :columns * CELL_PIXELS]
    blocks = trimmed.reshape(rows, CELL_PIXELS, columns, CELL_PIXELS)
    return blocks.sum(axis=(1, 3), dtype=np.int64)


def build_cell_table() -> pd.DataFrame:
    """One row per cell: forest area, disturbed area by cause, and its bounds."""
    transform, _ = efda.grid()
    forest = sum_per_cell(efda.read_forest_mask())

    disturbed = np.zeros_like(forest)
    by_agent = {name: np.zeros_like(forest) for name in EFDA_AGENTS.values()}
    for year in RANKING_YEARS:
        print(f"Reading {year}...")
        disturbed += sum_per_cell(efda.read_disturbance(year))
        agent = efda.read_agent(year)
        for code, name in EFDA_AGENTS.items():
            by_agent[name] += sum_per_cell(agent == code)

    to_lonlat = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)
    rows = []
    for row in range(forest.shape[0]):
        for column in range(forest.shape[1]):
            if forest[row, column] == 0:
                continue
            left = transform.c + column * AOI_SIZE_M
            top = transform.f - row * AOI_SIZE_M
            longitude, latitude = to_lonlat.transform(
                left + AOI_SIZE_M / 2, top - AOI_SIZE_M / 2
            )
            record = {
                "cell_row": row,
                "cell_column": column,
                "left": left,
                "bottom": top - AOI_SIZE_M,
                "right": left + AOI_SIZE_M,
                "top": top,
                "center_longitude": round(longitude, 3),
                "center_latitude": round(latitude, 3),
                "forest_share": forest[row, column] / CELL_PIXELS ** 2,
                "forest_ha": forest[row, column] * HECTARES_PER_PIXEL,
                "disturbed_ha": disturbed[row, column] * HECTARES_PER_PIXEL,
            }
            for name, values in by_agent.items():
                record[f"{name}_ha"] = values[row, column] * HECTARES_PER_PIXEL
            rows.append(record)

    table = pd.DataFrame(rows)
    # Share of the forest in the cell that was disturbed during the period.
    table["disturbed_share_of_forest"] = table["disturbed_ha"] / table["forest_ha"]
    return table


def choose_candidates(table: pd.DataFrame) -> pd.DataFrame:
    """Most disturbed, mostly forested cells that do not touch each other."""
    ranked = table.loc[table["forest_share"] >= MINIMUM_FOREST_SHARE]
    ranked = ranked.sort_values("disturbed_ha", ascending=False)

    chosen = []
    for cell in ranked.itertuples():
        touches = any(
            abs(cell.cell_row - other.cell_row) <= 1
            and abs(cell.cell_column - other.cell_column) <= 1
            for other in chosen
        )
        if not touches:
            chosen.append(cell)
        if len(chosen) == CANDIDATES:
            break
    candidates = pd.DataFrame(chosen).drop(columns="Index")
    candidates.insert(0, "candidate", range(1, len(candidates) + 1))
    return candidates


def save_map(table: pd.DataFrame, candidates: pd.DataFrame) -> None:
    """Map of disturbed hectares per cell, with the proposed areas outlined."""
    rows = table["cell_row"].max() + 1
    columns = table["cell_column"].max() + 1
    image = np.full((rows, columns), np.nan)
    image[table["cell_row"], table["cell_column"]] = table["disturbed_ha"]

    fig, ax = plt.subplots(figsize=(PAGE_WIDTH, 4.3))
    picture = ax.imshow(image, cmap=SEQUENTIAL_BLUE)
    for cell in candidates.itertuples():
        ax.add_patch(plt.Rectangle(
            (cell.cell_column - 0.5, cell.cell_row - 0.5), 1, 1,
            fill=False, edgecolor=ORANGE, linewidth=2,
        ))
        ax.text(cell.cell_column, cell.cell_row, str(cell.candidate), ha="center",
                va="center", fontsize=9, fontweight="bold", color=INK,
                bbox={"boxstyle": "circle,pad=0.15", "facecolor": "white",
                      "edgecolor": "none"})
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    years = f"{RANKING_YEARS[0]}–{RANKING_YEARS[-1]}"
    fig.colorbar(picture, ax=ax, pad=0.02, shrink=0.85,
                 label=f"Pădure perturbată {years} (ha pe celulă de 46 km)")
    fig.tight_layout()
    save_figure(fig, FOREST_RESULTS_DIR / "aoi_candidates.png")


def main() -> None:
    apply_style()
    FOREST_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    table = build_cell_table()
    table.to_csv(FOREST_RESULTS_DIR / "aoi_cells.csv", index=False, float_format="%.4f")

    candidates = choose_candidates(table)
    candidates.to_csv(FOREST_RESULTS_DIR / "aoi_candidates.csv", index=False,
                      float_format="%.4f")
    save_map(table, candidates)

    shown = candidates[[
        "candidate", "center_longitude", "center_latitude", "forest_share",
        "disturbed_ha", "harvest_ha", "wind_bark_beetle_ha", "fire_ha",
        "disturbed_share_of_forest",
    ]]
    print(shown.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    total = table["disturbed_ha"].sum()
    print(f"\nRomania, {RANKING_YEARS[0]}-{RANKING_YEARS[-1]}: "
          f"{total:,.0f} ha disturbed in the cells counted.")


if __name__ == "__main__":
    main()
