# Work journal

What was done each day, what was decided and why. Filled in at the end of every session, newest entry at the bottom. Decisions carry their reason so they are not reopened from scratch.

## To check (do not forget)

- [ ] **Which official harvest data can actually be obtained** (SUMAL 2.0 / Inspectorul Pădurii): can authorised harvest sites be downloaded in bulk, with outline and year, or only looked up one by one? Answer before discussing the topic with the supervisor.
- [ ] Choice of study area among the three candidates (`results/aoi_candidates.csv`).
- [ ] Time lag between label and image (see 15 Nov): download 2025 and compare.
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
- Still open: some 2024 outlines fall on ground that still looks forested in the summer 2024 composite. Probably autumn cuts, visible only in 2025. To be checked with the 2025 composite before fixing the rule "the label of year t shows in the image of year t or t+1".

**Decisions**
- EFDA as main labels, Hansen only for comparison. *Reason:* EFDA is made for Europe, is more recent and has the agent.
- Everything in EPSG:3035, with 10 m images placed exactly over the label grid. *Reason:* alignment becomes simple pixel repetition, with no resampling of labels.
- Area side of 46,080 m. *Reason:* a whole number of label pixels (1536) and of 256-pixel patches (18).
- Separate repository for the forest work. *Reason:* the old one stays the warm-up exercise, clean, to be shown as such.
- The dissertation is in English, written and presented, so everything in this repository is in English, including the plan and this journal. The EuroSAT repository stays as it is. *Reason:* the repository may be seen by others.
- The manually verified test set moves from "nice to have" to "must", in a small version (M9, 20–30 patches). *Reason:* EFDA labels are themselves derived from an NBR change, so a dNBR baseline has an advantage when scored against them.

**Mistakes caught**
- The `data/` rule in `.gitignore` also hid the code folder `src/data/` in the EuroSAT project; three files were missing from GitHub. Fixed and pushed.
- A patch script emptied the report generator, which was not yet in Git. Rewritten. *Lesson:* commit right after creating any new file.

**Left for later**
- Exercises for day 1 and Quiz 1 (Teodor).
