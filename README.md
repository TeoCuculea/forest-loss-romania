# Forest loss in the Romanian Carpathians from Sentinel-2

Master's dissertation project: segmentation networks that detect where forest cover disappeared from one year to the next (harvest, windthrow, bark beetle, fire), producing a map and the affected area in hectares.

Status: data preparation. The day-by-day plan is in [documentation/POC_PLAN.md](documentation/POC_PLAN.md) and the state of each deliverable in [documentation/TRACEABILITY.md](documentation/TRACEABILITY.md). The warm-up exercise (EuroSAT classification with ResNet18) lives in the separate `AI_LandCover_POC` repository.

## Data

| What | Source | Location |
|---|---|---|
| Labels: European Forest Disturbance Atlas v3.0, 30 m, 1985–2024 | `Romania.zip` from [Zenodo](https://zenodo.org/records/21722408), unpacked | `data/efda/` |
| Images: Sentinel-2 L2A summer composites at 10 m | public [Earth Search](https://earth-search.aws.element84.com/v1) catalogue, no account needed | `data/sentinel2/aoi_<n>/s2_<year>.tif` |

The `data/` folder is not tracked by Git. Everything is kept in EPSG:3035 on one shared grid: 3×3 image pixels cover exactly one label pixel.

## Steps

Run all commands from the project root.

```powershell
python -m pip install -r requirements.txt

# 1. Candidate study areas: the most disturbed 46 km cells in Romania
python -m forest.select_aoi

# 2. Sentinel-2 composites for one area and a few years
python -m forest.data.sentinel2 --candidate 1 --years 2023 2024

# 3. Control figure: the image with the labels drawn on top
python -m forest.plot_quicklook --candidate 1 --year 2024
```

## Layout

```text
forest/
  config.py            Paths and constants (grid, bands, season, area size)
  select_aoi.py        Ranks areas by disturbed hectares
  plot_quicklook.py    Visual check of image–label alignment
  plot_style.py        Shared look of the figures
  data/
    efda.py            Reads labels for one year and one rectangle
    sentinel2.py       Scene search, cloud masking, per-pixel median
results/               Small tables and figures
documentation/         Plan, traceability matrix, work journal
```

## A note on wording

Satellites show the loss of forest cover, not its cause in a legal sense. This project never labels a detected loss as illegal.
