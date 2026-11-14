# Forest_Lost_Romania

Teodor's master's dissertation (ML): detecting forest cover loss in the Romanian Carpathians from Sentinel-2, with segmentation. POC due **15 December 2026**. GitHub repository: `TeoCuculea/forest-loss-romania` (private).

- Day-by-day plan, with what is a must (M1–M9) and what is optional (N1–N8): [documentation/POC_PLAN.md](documentation/POC_PLAN.md).
- State of each item: [documentation/TRACEABILITY.md](documentation/TRACEABILITY.md). Update after every finished step.
- Daily journal with decisions and the "to check" list: [documentation/JOURNAL.md](documentation/JOURNAL.md). Fill in at the end of every session.
- The warm-up exercise (EuroSAT, ResNet18) and the learning material so far are in `e:\AI-LandCover_POC` (`documentation/invatare/`, `exercises/`), in Romanian. New exercises, about this project, go here in `exercises/`, in English.

## Language

- **The dissertation is in English**, written and presented. Everything in this repository is in English: code, comments, figure text, all documentation, commit messages, exercises.
- Talk to Teodor in Romanian, but keep the technical terms in English (training loop, batch norm, data leakage, IoU, weak labels…), so he learns the vocabulary he will write and present with.

## How to work with Teodor

- Explain through the flow and through what he already knows.
- A working day: 5 recap questions from previous days, theory on small examples, then he writes a delimited piece, then he reads what you wrote, then 5 new questions.
- Pieces marked "you write" in the plan **are not solved for him**. Give hints, review his attempt, say which part is right and correct the reasoning.
- His rule: no code stays in the project that he cannot explain.
- When something threatens the deadline, cut from the N list, not from M1–M9 and not from understanding. Say so early.

## Data and conventions

- Labels: EFDA v3.0 in `data/efda/` (30 m, one band per year, 1985 = band 1; agents: 1 wind/bark beetle, 2 fire, 3 harvest).
- Images: Sentinel-2 L2A summer composites in `data/sentinel2/aoi_<n>/`, 6 bands (B02, B03, B04, B08, B11, B12), values = reflectance × 10000, 0 = no data.
- Shared grid: EPSG:3035; 3×3 pixels of 10 m cover exactly one label pixel. Areas are 46,080 m on a side (1536 label pixels, 18 patches of 256).
- `data/` and `*.pth` are not in Git.
- Figures use `forest/plot_style.py` and are saved to disk.
- Satellites show forest cover loss, not its legality: never write "illegal deforestation".

## Commands

```powershell
python -m forest.select_aoi
python -m forest.data.sentinel2 --candidate 1 --years 2023 2024
python -m forest.plot_quicklook --candidate 1 --year 2024
```
