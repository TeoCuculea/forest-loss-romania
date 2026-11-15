# Work journal

What was done each day, what was decided and why. Filled in at the end of every session, newest entry at the bottom. Decisions carry their reason so they are not reopened from scratch.

## To check (do not forget)

- [x] **Which official harvest data can actually be obtained** (SUMAL 2.0 / Inspectorul Pădurii): checked on 15 Nov from public sources, see that day's entry. Short answer: points, not outlines; no bulk download found.
- [ ] Open the Inspectorul Pădurii map by hand over area 1: how many harvest permits (APV) appear, do old (closed) ones stay visible, is there any date in the details window?
- [ ] Choice of study area among the three candidates (`results/aoi_candidates.csv`).
- [x] Time lag between label and image: checked on 15 Nov with the 2025 composite, see "Label–image lag" below. Result: no lag; label year t shows in the image pair (t−1, t).
- [ ] Whether Hansen Global Forest Change already has version 1.13 (with 2025).
- [ ] The supervisor's reply to the message and the topic proposal; ask whether research questions Q1–Q4 are enough.

## Saturday, 14 November 2026 — starting point

**Where we started.** The warm-up project `AI_LandCover_POC` (EuroSAT, ResNet18) worked but had a tangled structure, unfinished documentation and no Git. The supervisor agreed to resume the collaboration on three conditions: POC by 15 December, attendance, autonomy.

**Done**
- Cleaned up the EuroSAT project, local Git and a GitHub repository.
- Word report rewritten end to end, generated from the results (14 pages, 11 figures, 6 tables).
- Reply to the supervisor, with the topic proposal.
- Day-by-day plan for the POC and the exercises for day 1.

**Learned**
- Differences between the four EuroSAT configurations (96.9–98.3%) are not conclusive: a single seed, and one run was stopped too early by early stopping.
- The "spatial" split removed overlaps, but 38% of test images had their neighbouring image in training. It was not a test of geographic generalisation.
- The names of the last five bands were shifted in the code (B8A is last in the EuroSAT files). Training was not affected.

**Decisions**
- Proposed topic: forest loss in the Carpathians from Sentinel-2, with segmentation. *Reason:* it continues what was learned (bands, geographic split, pretrained model) and no open benchmark was found for the region.
- Say "forest cover loss", never "illegal deforestation". *Reason:* legality cannot be seen from a satellite.
- POC limited to one ~46 km area and year-to-year change. *Reason:* 14 working days; all of Romania and monthly detection are left for the dissertation.
- Working mode: theory first, Teodor writes the pieces marked "you write", quizzes after each stage. *Reason:* no code stays in the project that he cannot explain.

## Sunday, 15 November 2026 — the data, without an account

**Done**
- EFDA v3.0 labels for Romania downloaded (2 GB) and read: 30 m, one band per year, with the causal agent and a forest mask.
- Romania cut into 46 km cells; three candidate areas chosen by hectares disturbed in 2019–2024.
- Script for Sentinel-2 summer composites, read from the public Earth Search catalogue; trial on area 1.
- Concept cards, flashcards and a reading guide (in `AI_LandCover_POC/documentation/invatare/`).
- Forest project moved to its own repository (`forest-loss-romania`).

**Learned**
- No Google Earth Engine account is needed: Sentinel-2 L2A can be read anonymously from Earth Search.
- EFDA has the causal agent for every year (harvest / wind and bark beetle / fire). In the candidate areas about half of the disturbances are harvest.
- For older years the same scene is listed twice in the catalogue (original and reprocessed), with different value scales. The script keeps only the newer one.

**Trial download result**
- Summer composites for 2023 and 2024 over area 1 are built: 4608×4608 pixels, 6 bands, no gaps (9–12 clear observations per pixel, from 16 days).
- The image grid falls exactly on the label grid (whole-number offset in label pixels, 3×3 pixels per label pixel). M2 is solved for EFDA.
- Open at the time: some 2024 outlines fall on ground that still looks forested in the summer 2024 composite. Guess: autumn cuts visible only in 2025. Checked later the same day, guess rejected (see "Label–image lag" below).

**Decisions**
- EFDA as main labels, Hansen only for comparison. *Reason:* EFDA is made for Europe, is more recent and has the agent.
- Everything in EPSG:3035, with 10 m images placed exactly over the label grid. *Reason:* alignment becomes simple pixel repetition, with no resampling of labels.
- Area side of 46,080 m. *Reason:* a whole number of label pixels (1536) and of 256-pixel patches (18).
- Separate repository for the forest work. *Reason:* the old one stays the warm-up exercise, clean, to be shown as such.
- The dissertation is in English, written and presented, so everything in this repository is in English, including the plan and this journal. The EuroSAT repository stays as it is. *Reason:* the repository may be seen by others.
- The manually verified test set moves from "nice to have" to "must", in a small version (M9, 20–30 patches). *Reason:* EFDA labels are themselves derived from an NBR change, so a dNBR baseline has an advantage when scored against them.

**Official harvest data: what can be obtained (checked from public sources)**
- The public portal inspectorulpadurii.ro (SUMAL 2.0) shows each harvest permit (APV, *act de punere în valoare*) as **one point** on a map, not as an outline. Fields the page displays: permit number, status, county, initial volume, number of inventoried trees, species groups (conifer/broadleaf), linked transport notices. No date field was seen in the page code. The only polygons the page draws are administrative units.
- The map can be filtered by forest district, permit status and permit number. No export button and no documented public interface for bulk download were found; nothing on data.gov.ro either. Transport notices are visible only for the last few days.
- The portal's data interface was not queried by script: it is undocumented and no terms of use were found, so automated collection is not assumed to be allowed.
- Forest management plans (stand outlines) are not open GIS data; the public ones are mostly PDF, often redacted.
- The official "forest loss alerts" inside SUMAL are themselves produced from Sentinel/Landsat change detection, so they are not independent ground truth.
- NGOs (Agent Green, Declic, Greenpeace) have complained since 2021 that the public part shows less than Government Decision 497/2020 promises. News sources found are mostly from 2020–2022; the present state of the portal must be confirmed by opening it.

**Consequence for the project**
- Official records cannot serve as segmentation labels (no outlines). EFDA stays the label source and the hand-verified test set (M9) stays the reference for scoring.
- Realistic use, as an optional item for the dissertation and not for the POC: for each detected loss patch, check whether a permit point lies within some distance ("loss with / without a nearby permit"), with wording that never implies illegality.
- Possible way to get more: a written request under the public-information law (544/2001) to the Ministry of Environment or the local Forest Guard for the permits of one forest district. Answer takes up to 30 days, so it cannot be relied on for 15 December.

**Label–image lag (checked with the summer 2025 composite, `forest/check_label_lag.py`)**
- Measure: change of NBR between two summer composites, averaged per label pixel; "drop" = NBR(t−1) − NBR(t). Results in `results/label_lag_aoi_01.csv`.
- Stable forest (control, 1.96 M pixels): median drop 0.003; 0.3% of pixels above 0.15.
- EFDA 2024 disturbance (11,223 pixels): median drop **0.151** between summer 2023 and 2024, 50% of pixels above 0.15. Between 2024 and 2025 the median is −0.037 (NBR rises again) and only 3% are above 0.15.
- So the earlier guess "autumn cuts that show only in 2025" is **rejected**: if it were true the 2024→2025 column would be high. A label of year t is seen in the pair of summers (t−1, t).
- Harvest (48% above threshold) and wind/bark beetle (54%) behave alike.
- About half of the labelled pixels show no strong NBR drop. Possible reasons, not yet checked: partial cuts or thinning inside a 30 m pixel, labels that are wrong at pixel level, a threshold that is too high. This puts a ceiling on any score measured against EFDA and is one more reason for the hand-verified test set (M9).

**Mistakes caught**
- The `data/` rule in `.gitignore` also hid the code folder `src/data/` in the EuroSAT project; three files were missing from GitHub. Fixed and pushed.
- A patch script emptied the report generator, which was not yet in Git. Rewritten. *Lesson:* commit right after creating any new file.

**Later the same day**
- Teodor read through the whole EuroSAT code instead of doing the exercises.
- Reading guide extended: how to read a paper, role and priority of each one, EuroSAT entry, practical reading.
- K-means and k-nearest neighbours reviewed, as used in the EuroSAT spatial analysis. Neither is planned for the POC; "nearest" in `sentinel2.py` is a resampling method, not the classifier.
- Theory test of 15 questions on the warm-up project handed out.

**Decision**
- Exercises 1–4 move to the evenings of 16–20 Nov. *Reason:* the day went to reading the code; exercise 1 is still needed before D5.

**Left for later**
- Answers to the theory test (Teodor).
- Exercises for day 1 and Quiz 1 (Teodor).
