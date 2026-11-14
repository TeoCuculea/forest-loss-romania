"""Build one cloud-free summer image per year from Sentinel-2 L2A.

The scenes are read from the public Earth Search catalogue (no account
needed). For a rectangle and a year the script:
  1. finds the scenes taken between 1 June and 31 August;
  2. keeps the clearest days;
  3. hides clouds, cloud shadows and snow using the scene classification (SCL);
  4. takes, for every pixel and band, the median of the remaining values.

The result is a GeoTIFF on a 10 m grid in EPSG:3035 that sits exactly on the
EFDA label grid: 3 x 3 image pixels cover one 30 m label pixel.

Usage (candidate 1 from results/aoi_candidates.csv, two years):
    python -m forest.data.sentinel2 --candidate 1 --years 2023 2024
"""

import argparse

import numpy as np
import odc.stac
import pandas as pd
import pystac_client
import rasterio
from dask.diagnostics import ProgressBar
from odc.geo.geobox import GeoBox
from pyproj import Transformer

from forest.config import (
    CRS,
    FOREST_RESULTS_DIR,
    SEASON_END,
    SEASON_START,
    SENTINEL2_BANDS,
    SENTINEL2_DIR,
    SENTINEL2_PIXEL_M,
)

CATALOGUE_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"

# A scene is considered only if less than this share of it is cloud.
MAX_SCENE_CLOUD_PERCENT = 30
# Days used for one composite: the clearest ones.
MAX_DAYS = 16

# Scene classification values treated as a usable view of the ground:
# 2 dark area (terrain shadow), 4 vegetation, 5 bare soil, 6 water, 7 unclassified.
# Left out: 0 no data, 1 saturated, 3 cloud shadow, 8-10 clouds, 11 snow.
CLEAR_CLASSES = (2, 4, 5, 6, 7)

# Since processing baseline 04.00 the pixel values carry an offset of 1000.
# Earth Search removes it and flags the scene; other scenes are not comparable.
OFFSET_BASELINE = "04.00"

Bounds = tuple[float, float, float, float]


def find_scenes(bounds: Bounds, year: int) -> list:
    """Search the catalogue and return the scenes to use, clearest days first."""
    to_lonlat = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)
    left, bottom, right, top = bounds
    longitudes, latitudes = to_lonlat.transform(
        [left, right, left, right], [bottom, bottom, top, top]
    )
    catalogue = pystac_client.Client.open(CATALOGUE_URL)
    search = catalogue.search(
        collections=[COLLECTION],
        bbox=[min(longitudes), min(latitudes), max(longitudes), max(latitudes)],
        datetime=f"{year}-{SEASON_START}/{year}-{SEASON_END}",
        query={"eo:cloud_cover": {"lt": MAX_SCENE_CLOUD_PERCENT}},
    )
    scenes = list(search.items())

    # The same acquisition can be listed twice (original and reprocessed).
    # Keep the newest processing for each tile and date.
    newest = {}
    for scene in scenes:
        key = (scene.properties["grid:code"], scene.datetime.date())
        baseline = scene.properties.get("s2:processing_baseline", "")
        if key not in newest or baseline > newest[key].properties.get(
            "s2:processing_baseline", ""
        ):
            newest[key] = scene

    usable = [
        scene for scene in newest.values()
        if scene.properties.get("s2:processing_baseline", "") < OFFSET_BASELINE
        or scene.properties.get("earthsearch:boa_offset_applied", False)
    ]
    dropped = len(newest) - len(usable)
    if dropped:
        print(f"  {dropped} scene(s) left out: value offset not harmonised.")

    # Rank the days by their cloudiest tile and keep the clearest ones.
    cloud_by_day = {}
    for scene in usable:
        day = scene.datetime.date()
        cloud_by_day[day] = max(cloud_by_day.get(day, 0), scene.properties["eo:cloud_cover"])
    best_days = sorted(cloud_by_day, key=cloud_by_day.get)[:MAX_DAYS]
    chosen = [scene for scene in usable if scene.datetime.date() in best_days]
    print(f"  {year}: {len(scenes)} scenes found, {len(chosen)} used "
          f"over {len(best_days)} days.")
    return chosen


def build_composite(bounds: Bounds, year: int, output_path) -> dict:
    """Write the median summer image of ``year`` and return a few quality numbers."""
    scenes = find_scenes(bounds, year)
    if not scenes:
        raise RuntimeError(f"No usable Sentinel-2 scenes for {year}.")

    # The exact output grid: 10 m pixels whose corners fall on the label grid.
    geobox = GeoBox.from_bbox(bounds, crs=CRS, resolution=SENTINEL2_PIXEL_M, tight=True)
    assets = list(SENTINEL2_BANDS.values())

    stack = odc.stac.load(
        scenes,
        bands=assets + ["scl"],
        geobox=geobox,
        groupby="solar_day",          # tiles of the same day are merged
        resampling={"scl": "nearest", "*": "bilinear"},
        chunks={"x": 1536, "y": 1536},
    )

    clear = stack["scl"].isin(CLEAR_CLASSES)
    bands = stack[assets]
    clear = clear & (bands[assets[0]] > 0)          # 0 means no data
    observations = clear.sum("time").astype("uint8")
    median = (
        bands.where(clear)
        .chunk({"time": -1})
        .median("time", skipna=True)
    )

    print("  Reading and reducing (this is the slow part)...")
    with ProgressBar(dt=30):
        median, observations = median.compute(), observations.compute()

    image = np.stack([median[asset].values for asset in assets])
    image = np.nan_to_num(image, nan=0).round().clip(0, 65535).astype("uint16")
    counts = observations.values

    output_path.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "driver": "GTiff", "height": image.shape[1], "width": image.shape[2],
        "count": image.shape[0], "dtype": "uint16", "crs": CRS,
        "transform": geobox.affine, "nodata": 0, "compress": "deflate",
        "tiled": True, "blockxsize": 512, "blockysize": 512,
    }
    with rasterio.open(output_path, "w", **profile) as target:
        target.write(image)
        target.descriptions = tuple(SENTINEL2_BANDS)
        target.update_tags(year=str(year), scenes=str(len(scenes)),
                           scale="reflectance = value / 10000")

    count_path = output_path.with_name(output_path.stem + "_observations.tif")
    with rasterio.open(count_path, "w", **{**profile, "count": 1, "dtype": "uint8",
                                           "nodata": None}) as target:
        target.write(counts, 1)

    return {
        "year": year,
        "scenes": len(scenes),
        "days": int(stack.sizes["time"]),
        "rows": image.shape[1],
        "columns": image.shape[2],
        "share_without_data": float((counts == 0).mean()),
        "median_clear_observations": float(np.median(counts)),
        "file": output_path.name,
    }


def candidate_bounds(candidate: int) -> Bounds:
    """Bounds of one proposed study area from results/aoi_candidates.csv."""
    table = pd.read_csv(FOREST_RESULTS_DIR / "aoi_candidates.csv")
    row = table.loc[table["candidate"] == candidate].iloc[0]
    return (row["left"], row["bottom"], row["right"], row["top"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--candidate", type=int, default=1,
                        help="Study area number from aoi_candidates.csv.")
    parser.add_argument("--years", type=int, nargs="+", required=True)
    arguments = parser.parse_args()

    # Anonymous access to the public bucket, tuned for reading parts of files.
    odc.stac.configure_rio(cloud_defaults=True, aws={"aws_unsigned": True})

    bounds = candidate_bounds(arguments.candidate)
    folder = SENTINEL2_DIR / f"aoi_{arguments.candidate:02d}"
    summary = []
    for year in arguments.years:
        output_path = folder / f"s2_{year}.tif"
        if output_path.is_file():
            print(f"  {year}: already built, skipping ({output_path}).")
            continue
        summary.append(build_composite(bounds, year, output_path))

    if summary:
        table = pd.DataFrame(summary)
        log_path = FOREST_RESULTS_DIR / f"sentinel2_aoi_{arguments.candidate:02d}.csv"
        if log_path.is_file():
            table = pd.concat([pd.read_csv(log_path), table]).drop_duplicates("year", keep="last")
        table.sort_values("year").to_csv(log_path, index=False, float_format="%.4f")
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
