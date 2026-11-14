"""Control figure: a Sentinel-2 composite with the EFDA disturbances on top.

Left: the whole study area in natural colours. Right: a 5 km close-up of the
place with the most disturbance, before and after, with the label outline.
If the red patches sit on visibly cleared ground, the image and the labels
are aligned.

Usage:
    python -m forest.plot_quicklook --candidate 1 --year 2024
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
import rasterio

from forest.config import (
    FOREST_RESULTS_DIR,
    PIXELS_PER_LABEL,
    SENTINEL2_BANDS,
    SENTINEL2_DIR,
)
from forest.data import efda
from forest.data.sentinel2 import candidate_bounds
from forest.plot_style import PAGE_WIDTH, RED, apply_style, save_figure

ZOOM_PIXELS = 510          # 5.1 km at 10 m; a multiple of 3 label pixels
BAND_INDEX = {name: index for index, name in enumerate(SENTINEL2_BANDS)}


def read_composite(candidate: int, year: int) -> np.ndarray:
    path = SENTINEL2_DIR / f"aoi_{candidate:02d}" / f"s2_{year}.tif"
    with rasterio.open(path) as source:
        return source.read()


def to_rgb(image: np.ndarray) -> np.ndarray:
    """Natural-colour picture from reflectance x 10000 (fixed stretch, for viewing)."""
    rgb = np.stack([image[BAND_INDEX[band]] for band in ("B04", "B03", "B02")], axis=-1)
    return np.clip(rgb.astype(np.float32) / 2000, 0, 1) ** 0.8


def to_image_grid(labels: np.ndarray) -> np.ndarray:
    """Repeat every 30 m label pixel 3 x 3 times to match the 10 m image."""
    return np.repeat(np.repeat(labels, PIXELS_PER_LABEL, axis=0), PIXELS_PER_LABEL, axis=1)


def busiest_window(mask: np.ndarray, size: int) -> tuple[int, int]:
    """Top-left corner of the size x size window containing the most labelled pixels."""
    rows = mask.shape[0] // size
    columns = mask.shape[1] // size
    blocks = mask[:rows * size, :columns * size].reshape(rows, size, columns, size)
    totals = blocks.sum(axis=(1, 3))
    row, column = np.unravel_index(totals.argmax(), totals.shape)
    return row * size, column * size


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--candidate", type=int, default=1)
    parser.add_argument("--year", type=int, required=True,
                        help="Year of the disturbances; the year before is shown too.")
    arguments = parser.parse_args()
    apply_style()

    bounds = candidate_bounds(arguments.candidate)
    after = read_composite(arguments.candidate, arguments.year)
    before = read_composite(arguments.candidate, arguments.year - 1)
    disturbed = to_image_grid(efda.read_disturbance(arguments.year, bounds))
    if disturbed.shape != after.shape[1:]:
        raise ValueError(f"Label grid {disturbed.shape} does not match image {after.shape[1:]}.")

    row, column = busiest_window(disturbed, ZOOM_PIXELS)
    window = (slice(row, row + ZOOM_PIXELS), slice(column, column + ZOOM_PIXELS))

    fig, axes = plt.subplots(1, 3, figsize=(PAGE_WIDTH, 2.6),
                             gridspec_kw={"width_ratios": [1.25, 1, 1]})

    overview = to_rgb(after[:, ::6, ::6])
    axes[0].imshow(overview)
    red_layer = np.zeros((*disturbed[::6, ::6].shape, 4))
    red_layer[disturbed.reshape(disturbed.shape[0] // 6, 6, -1, 6).max(axis=(1, 3)) > 0] = (
        0.89, 0.29, 0.28, 1.0
    )
    axes[0].imshow(red_layer)
    axes[0].add_patch(plt.Rectangle((column / 6, row / 6), ZOOM_PIXELS / 6, ZOOM_PIXELS / 6,
                                    fill=False, edgecolor="white", linewidth=1.2))
    axes[0].set_title(f"Whole area, {arguments.year}", loc="center", fontsize=8.5)

    axes[1].imshow(to_rgb(before[:, window[0], window[1]]))
    axes[1].set_title(f"5 km close-up, {arguments.year - 1}", loc="center", fontsize=8.5)
    axes[2].imshow(to_rgb(after[:, window[0], window[1]]))
    axes[2].contour(disturbed[window], levels=[0.5], colors=[RED], linewidths=0.9)
    axes[2].set_title(f"5 km close-up, {arguments.year}", loc="center", fontsize=8.5)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.tight_layout()
    save_figure(fig, FOREST_RESULTS_DIR
                / f"quicklook_aoi_{arguments.candidate:02d}_{arguments.year}.png")

    hectares = efda.read_disturbance(arguments.year, bounds).sum() * 0.09
    print(f"EFDA {arguments.year}: {hectares:,.0f} ha disturbed in this area.")


if __name__ == "__main__":
    main()
