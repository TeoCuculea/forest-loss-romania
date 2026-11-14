# Plan: proof of concept "forest loss in Romania from Sentinel-2" (due 15 December 2026)

## Context

The warm-up project (EuroSAT + ResNet18) is finished, documented and on GitHub. Next is the proof of concept the supervisor asked for by 15 December. Goals: solid fundamentals, a path to the forest-loss topic, the datasets, quizzes to understand the code, a clear personal contribution, and a split into "must" and "nice to have". Time left on 15 November: 14 full days plus evenings of 1–2 hours.

Assumption: the supervisor accepts the direction. If he proposes another topic, day 1 and the first week's evenings still hold (they are fundamentals) and the rest is replanned.

## What the supervisor asks and how the plan answers

| Requirement | Answer |
|---|---|
| POC by 15 December | Complete chain on one area: data → labels → baseline → U-Net → red overlay map + area |
| Attendance and communication | Something to show after each weekend; short progress messages on 22 Nov and 6 Dec |
| Substantial practical part, autonomy | Data built by you, not a ready-made set; comparison with a baseline; honest evaluation |
| Use of AI | Your rule: nothing in the project you cannot explain; the quizzes below check it |

## Topic and your contribution

**Correct wording:** satellites show *forest cover loss* (clear-cut, windthrow, bark beetle, fire), not "deforestation" in a legal sense. Working title: "Detecting forest cover loss in the Romanian Carpathians from Sentinel-2 with segmentation networks".

**Why there is room for a contribution:** a search found no open Sentinel-2 clear-cut segmentation benchmark for Central and Eastern Europe; the closest is the Ukraine dataset (Kharkiv region). Existing maps for Romania (Hansen, EFDA) are at 30 m, from Landsat.

**Research questions (whole dissertation):**
1. Can a model trained on weak 30 m labels produce finer masks, at 10 m, on Sentinel-2? Measured on a manually verified test set.
2. How much does a network gain over a threshold on an index difference (dNBR/dNDVI)?
3. Do extra bands (NIR, SWIR) and Sentinel-2 pretrained weights help compared with ImageNet? (continues the EuroSAT question)
4. Does the model generalise to an area it has not seen? (geographic block split)

**What question 2 means.** The baseline is a method without training, about 30 lines: NBR = (B08 − B12) / (B08 + B12) is high for healthy forest and drops sharply after a cut. dNBR = NBR before − NBR after; pixels above a threshold are marked "loss". The network must beat it on the same test set, otherwise it is not justified. It costs one day (day 3) and gives the first red overlay map three weeks before the deadline.

**Is it enough?** For the POC, yes. For the dissertation, yes if the manually verified test set exists and at least two comparisons are done rigorously (with several seeds). It is not a new architecture but a new dataset for a region plus a correct evaluation, which is a legitimate applied contribution at master's level. Only "I ran U-Net on someone else's labels", with no validation of your own, would be weak. The final judge is the supervisor: ask him directly, at the first meeting, whether questions 1–4 are enough.

**What is concretely yours:**
- the dataset for Romania (annual Sentinel-2 composites + aligned labels), reproducible from code;
- a test set verified by you manually, at 10 m;
- the evaluation protocol on geographic blocks and the baseline vs. network comparison;
- the red overlay map and area per year, compared with Hansen and EFDA.

## Datasets

| What | Role | Where from |
|---|---|---|
| Sentinel-2 L2A, 10 m | Model input: summer composites (Jun–Aug) per year, bands B02, B03, B04, B08, B11, B12 | Public [Earth Search](https://earth-search.aws.element84.com/v1) catalogue, no account (`forest/data/sentinel2.py`) |
| European Forest Disturbance Atlas (EFDA) v3.0 | Main labels: annual disturbances 1985–2024, 30 m, with the causal agent; CC BY 4.0 | [Zenodo](https://zenodo.org/records/21722408), [TUM page](https://www.lss.ls.tum.de/en/eoem/datasets/european-forest-disturbance-atlas-efda/) |
| Hansen Global Forest Change v1.12 | Comparison labels: loss year 2001–2024, 30 m | [download page](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/download.html) |
| EFDA reference samples | Expert-verified points, for validation | [Zenodo](https://zenodo.org/records/20431478) |
| Clear-cuts in Ukraine (Sentinel-2) | Plan B: hand-drawn polygons, ~36 GB | [Kaggle](https://www.kaggle.com/datasets/isaienkov/deforestation-in-ukraine), [code](https://github.com/QuantuMobileSoftware/forest_change_detection) |

All sources are free. Volume is small: one 46 km area at 10 m with 6 bands is ~200 MB per year, so everything stays local.

## Must and nice to have

**Must for 15 December**
- [ ] M1. Sentinel-2 composites for one area, at least 3 consecutive years
- [ ] M2. EFDA and Hansen labels aligned pixel by pixel with the images
- [ ] M3. Baseline without a network: threshold on dNBR → mask, red overlay map, area in hectares
- [ ] M4. U-Net trained with a geographic block split; IoU and F1 on test
- [ ] M5. Baseline vs. U-Net table on the same test set
- [ ] M6. Inference on the whole area: map per year and area per year, next to the Hansen/EFDA figures
- [ ] M7. Report of 8–10 pages and a 10-minute presentation, **in English**
- [ ] M8. You can explain every step without notes (quizzes passed)
- [ ] M9. Small manually verified test set (20–30 patches). *Promoted from N1:* EFDA labels are themselves derived from an NBR change, so a dNBR baseline has an advantage when scored against them; without an independent test set the comparison with the network is not fair.

**Nice to have, in order of value**
- [ ] N1. Extending the verified test set to 40–60 patches
- [ ] N2. Three seeds for the main comparison, mean ± standard deviation
- [ ] N3. Band ablation: RGB vs. RGB+NIR vs. all 6
- [ ] N4. Sentinel-2 pretrained encoder (SSL4EO-S12) vs. ImageNet
- [ ] N5. Bi-temporal Siamese network (Daudt) vs. U-Net with concatenated years
- [ ] N6. A second area, unseen in training
- [ ] N7. Automated tests (pytest) for data preparation
- [ ] N8. Interactive map (folium)

**For the dissertation, after the POC:** several Carpathian areas, seasonal/monthly detection on time series, separating harvest from windthrow using the EFDA agent, per-county statistics, Sentinel-1 radar for cloudy months, comparison with officially declared harvest sites if such data can be obtained.

## Calendar

| When | You learn | You do | Result |
|---|---|---|---|
| **D1 · Sun 15 Nov** | Training loop, `train/eval`, `no_grad`, batch norm, weight decay, on `runner.py` line by line | Exercises 1–4 (in the EuroSAT repository); send the message and the report to the supervisor | Quiz 1 |
| Evenings 16–20 Nov | ResNet (sections 1 and 3), U-Net | Read `forest/data/sentinel2.py` and explain it | Quiz 2 |
| **D2 · Sat 21 Nov** | L1C vs. L2A, cloud masking, median composite, CRS, resampling | Choose the area; composites for all years; settle the label–image time lag; open everything in QGIS | M1, M2 |
| **D3 · Sun 22 Nov** | NDVI, NBR, IoU, precision/recall, pixel area | dNBR between consecutive years, threshold, mask, red overlay, hectares per year, comparison with the labels | M3; progress message to the supervisor with the first map |
| Evenings 23–27 Nov | Change detection (Daudt), EFDA (how the labels were made), Dice vs. cross-entropy | Install `segmentation_models_pytorch`; pass a tensor through U-Net and follow the shapes | Quiz 3 |
| **D4 · Sat 28 Nov** | Segmentation vs. classification, class imbalance, block split | Cut the area into 256×256 patches; input = year t and t+1 concatenated; target = loss in t+1; `Dataset` modelled on `EuroSATDataset`; normalisation from training only | Dataset ready |
| **D5 · Sun 29 Nov** | Encoder–decoder, skip connections, BCE + Dice, augmentations, mixed precision | First U-Net training (ResNet34 encoder, first convolution adapted as in `_adapt_first_convolution`) | First IoU on validation |
| **D6 · Mon 30 Nov** | Error analysis | Predictions next to labels on 30 patches; fix what is broken; evaluate on test | M4, M5 |
| **D7 · Tue 1 Dec** | Sliding-window inference | Map of the whole area for each year; area per year; chart against Hansen/EFDA | M6 |
| **D8 · Wed 2 Dec** | Label noise | Verify 20–30 patches manually in QGIS; re-score the model and the labels on them | M9 |
| **D9 · Thu 3 Dec** | Designing an experiment | One of N2–N4, whichever is closest to working | A second result |
| **D10 · Fri 4 Dec** | — | Buffer: catch up | — |
| **D11 · Sat 5 Dec** | Writing a report | The report, generated from the results | M7 (report) |
| **D12 · Sun 6 Dec** | — | The presentation; send the draft to the supervisor | M7 (presentation) |
| Evenings 7–11 Dec | Review | Corrections after the supervisor's reply | Quiz 4 |
| **D13 · Sat 12 Dec** | — | Buffer and polish | — |
| **D14 · Sun 13 Dec** | — | Mock defence: I ask the supervisor's questions | M8 |

**Checkpoint on the evening of 29 Nov:** if there is still no U-Net that learns something, switch to plan B (Ukraine dataset for training, Romania only for inference) and drop the N list.

## What a working day looks like

0. **Recap, 10 min:** 5 questions from previous days, before anything else. What you miss comes back next time.
1. **Theory, 45–60 min:** the day's concepts on small examples, before any code. We do not move on until you can say them in your own words.
2. **You write, 1–2 hours:** a small, well-delimited piece, from hints, not from a solution. I review it and explain what I would change.
3. **I write, you read:** the plumbing (download, alignment, saving, plots). We go through it together and you must be able to explain it.
4. **Quiz, 15 min:** 5 questions at the end.

## Who writes what

| You write (reviewed) | I write (you read and explain) |
|---|---|
| D1: training loop on a single batch, from scratch | Scene search and download |
| D3: `ndvi()`, `nbr()`, `iou()`, area in hectares | Reading labels on the shared grid |
| D4: `__getitem__` for the new `Dataset` | Cutting into patches and the split CSV |
| D5: the U-Net training loop, starting from `train_one_epoch` | Sliding-window inference, the maps |
| D6: the function that shows prediction next to label | The report generator |

If writing code goes slower than planned, cut from the "nice to have" list, not from understanding and not from M1–M9.

## How the dataset is built

Not a database in the strict sense, but the same pattern as EuroSAT: a folder of GeoTIFF files and a CSV that says what each one is.

1. Choose a rectangle on the map (`forest/select_aoi.py` proposes three).
2. For each year, a script takes the median of the cloud-free summer images over that rectangle and saves it as a GeoTIFF (`data/sentinel2/aoi_01/s2_2021.tif`, …).
3. EFDA and Hansen labels are read on the same rectangle.
4. Images sit on a 10 m grid placed exactly over the 30 m label grid, so pixel (i, j) means the same place in every file.
5. Everything is cut into 256×256 patches and a CSV keeps: patch, year, geographic block, subset.

## Quizzes and exercises

After each stage you get 5 questions in chat, you answer without the code open, and I grade each answer. Alongside them, "predict, then run" exercises:

1. **Overfit a single batch.** Train on 32 images until the loss is ≈ 0. If it does not get there, the loop has a bug.
2. **Forget `model.eval()`.** Evaluate on validation with and without it; explain the difference through `running_mean`.
3. **Follow the shapes.** Print the tensor shape after each ResNet18 stage, for 3 and for 13 channels.
4. **Compute by hand.** Standard error of an accuracy; IoU on a 4×4 mask; parameter count of the first convolution.
5. (D3) **Write IoU yourself** in numpy, no library, and check it on an example done on paper.
6. (D5) **Break something on purpose:** normalisation computed from test, random split over neighbouring patches; watch the score rise falsely.

## Concepts to tick off

- **Networks:** convolution, stride, padding, receptive field, batch norm (batch vs. `running_mean`), residual block, encoder–decoder, skip connections in U-Net
- **Training:** forward/backward, optimiser, AdamW and weight decay, learning rate, cosine + warmup, early stopping, augmentations, mixed precision, seed
- **Evaluation:** the three subsets, data leakage, overfitting, accuracy vs. F1, IoU, precision/recall, mean ± std over seeds, standard error
- **Remote sensing:** bands and indices (NDVI, NBR), L1C/L2A, clouds and composites, resolution, CRS and reprojection, GeoTIFF, spatial autocorrelation
- **Segmentation and change:** mask, class imbalance, Dice, sliding window, bi-temporal input, weak labels
- **Engineering:** Git, structure of an experiment, results reproducible from code

## Reading list

- ResNet: https://arxiv.org/abs/1512.03385
- U-Net: https://arxiv.org/abs/1505.04597
- Daudt (Siamese networks for change detection): https://arxiv.org/abs/1810.08462
- EFDA: https://essd.copernicus.org/articles/17/2373/2025/
- Hansen: https://www.science.org/doi/10.1126/science.1244693
- Clear-cuts in Ukraine on Sentinel-2: https://ieeexplore.ieee.org/abstract/document/9241044
- SSL4EO-S12: https://arxiv.org/abs/2211.07044
- Spatial validation (Roberts): https://onlinelibrary.wiley.com/doi/10.1111/ecog.02881
- Practical: https://d2l.ai/chapter_convolutional-modern/resnet.html · https://smp.readthedocs.io · https://torchgeo.readthedocs.io

A reading guide with questions per paper (in Romanian) is in the EuroSAT repository, `documentation/invatare/ghid_lectura.md`.

## Risks

- **30 m labels on 10 m images:** edges are imprecise. This is why the manually verified set and the baseline comparison on the same test set matter.
- **Label year vs. image year:** an autumn cut shows only in the next summer's composite. First seen in the 2024 trial; to be settled on day 2 before any training.
- **Imbalance:** loss is 1–2% of pixels. Choose patches that contain forest, use Dice, report IoU on the "loss" class, not accuracy.
- **Download time:** two years took about an hour. All years are built in one overnight run.
