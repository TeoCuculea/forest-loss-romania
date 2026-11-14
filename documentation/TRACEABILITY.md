# Traceability: from question to result

Each row links what we want to find out to the experiment that answers it, the script that runs it, the file where the result lands and the place in the report where it is discussed. A row without a script or a result shows what is still to do. Updated after every finished step.

States: **done**, **in progress**, **to do**.

## Research questions

| # | Question | Experiment | Script | Result | State |
|---|---|---|---|---|---|
| Q1 | Can a model trained on 30 m labels produce finer masks at 10 m? | U-Net scored on a manually verified test set, next to the EFDA labels on the same set | — | — | to do (M9) |
| Q2 | How much does a network gain over a threshold on dNBR? | dNBR baseline and U-Net on the same test set, IoU and F1 | — | — | to do (M3–M5) |
| Q3 | Do extra bands and Sentinel-2 pretrained weights help? | Band ablation; ImageNet vs. SSL4EO-S12 encoder | — | — | to do (N3, N4) |
| Q4 | Does the model generalise to an unseen area? | Geographic block split; a second area | — | — | to do (M4, N6) |

## Deliverables for 15 December

| # | What | Script | Result | State |
|---|---|---|---|---|
| M1 | Sentinel-2 composites, one area, at least 3 years | [forest/data/sentinel2.py](../forest/data/sentinel2.py) | `data/sentinel2/aoi_01/s2_<year>.tif`, log in `results/sentinel2_aoi_01.csv` | in progress: trial on 2 years |
| M2 | EFDA and Hansen labels aligned to the images | [forest/data/efda.py](../forest/data/efda.py) | EFDA read directly on the shared grid; Hansen missing | in progress |
| M3 | dNBR baseline: mask, red overlay map, hectares | — | — | to do (day 3; Teodor writes `nbr`, `iou`) |
| M4 | U-Net with block split; IoU and F1 on test | — | — | to do (days 4–6) |
| M5 | Baseline vs. U-Net table | — | — | to do (day 6) |
| M6 | Map and area per year for the whole area | — | — | to do (day 7) |
| M7 | Report and presentation, in English | — | — | to do (days 11–12) |
| M8 | Teodor can explain every step | exercises, quizzes | Quizzes 1–4 | in progress |
| M9 | Small manually verified test set (20–30 patches) | — | — | to do (day 8) |

## Preparatory steps

| What | Script | Result | State |
|---|---|---|---|
| Choosing the study area | [forest/select_aoi.py](../forest/select_aoi.py) | [aoi_candidates.csv](../results/aoi_candidates.csv), [aoi_candidates.png](../results/aoi_candidates.png) | 3 candidates proposed; Teodor chooses |
| Checking image–label alignment | [forest/plot_quicklook.py](../forest/plot_quicklook.py) | `results/quicklook_aoi_01_2024.png` | in progress |
