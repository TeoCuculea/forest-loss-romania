# Trasabilitate: de la întrebare la rezultat

Fiecare rând leagă ce vrem să aflăm de experimentul care răspunde, de scriptul care îl rulează, de fișierul în care ajunge rezultatul și de locul din document unde e discutat. Un rând fără script sau fără rezultat arată ce mai e de făcut. Se actualizează la fiecare pas terminat.

Stări: **făcut**, **în lucru**, **de făcut**.

## Întrebările de cercetare

| # | Întrebare | Experiment | Script | Rezultat | Stare |
|---|---|---|---|---|---|
| Î1 | Poate un model antrenat pe etichete de 30 m să dea măști mai fine, la 10 m? | U-Net evaluat pe un set de test verificat manual, față de etichetele EFDA pe același set | — | — | de făcut (N1) |
| Î2 | Cât câștigă o rețea față de un prag pe dNBR? | Baseline dNBR și U-Net pe același test, IoU și F1 | — | — | de făcut (M3–M5) |
| Î3 | Ajută benzile în plus și ponderile preantrenate pe Sentinel-2? | Ablație pe benzi; encoder ImageNet vs. SSL4EO-S12 | — | — | de făcut (N3, N4) |
| Î4 | Generalizează modelul într-o zonă nevăzută? | Split pe blocuri geografice; a doua zonă | — | — | de făcut (M4, N6) |

## Livrabilele pentru 15 decembrie

| # | Ce | Script | Rezultat | Stare |
|---|---|---|---|---|
| M1 | Compozite Sentinel-2, o zonă, cel puțin 3 ani | [forest/data/sentinel2.py](../forest/data/sentinel2.py) | `data/sentinel2/aoi_01/s2_<an>.tif`, jurnal în `results/sentinel2_aoi_01.csv` | în lucru: probă pe 2 ani |
| M2 | Etichete EFDA și Hansen aliniate la imagini | [forest/data/efda.py](../forest/data/efda.py) | EFDA citit direct pe grila comună; Hansen lipsește | în lucru |
| M3 | Baseline dNBR: mască, hartă cu roșu, hectare | — | — | de făcut (Z3, scrie Teodor `nbr`, `iou`) |
| M4 | U-Net cu split pe blocuri; IoU și F1 pe test | — | — | de făcut (Z4–Z6) |
| M5 | Tabel baseline vs. U-Net | — | — | de făcut (Z6) |
| M6 | Hartă și arie pe an pentru toată zona | — | — | de făcut (Z7) |
| M7 | Document și prezentare | — | — | de făcut (Z11–Z12) |
| M8 | Teodor poate explica fiecare pas | [exercises/](../exercises/), [invatare/](invatare/) | Testele 1–4 | în lucru |

## Pași pregătitori

| Ce | Script | Rezultat | Stare |
|---|---|---|---|
| Alegerea zonei de studiu | [forest/select_aoi.py](../forest/select_aoi.py) | [aoi_candidates.csv](../results/aoi_candidates.csv), [aoi_candidates.png](../results/aoi_candidates.png) | 3 candidate propuse; alegerea e a lui Teodor |
| Verificarea alinierii imagine–etichete | [forest/plot_quicklook.py](../forest/plot_quicklook.py) | `results/quicklook_aoi_01_2024.png` | în lucru |

## Proiectul de încălzire (EuroSAT)

| Întrebare | Script | Rezultat | Unde e discutat |
|---|---|---|---|
| Ajută cele 13 benzi față de RGB? | [src/training/runner.py](../src/training/runner.py), [compare_experiments.py](../src/analysis/compare_experiments.py) | `results/runs/disertatie_final_01/tables/experiment_comparison.csv` | Document, 8.1: neconcludent |
| Supraestimează splitul aleator? | [create_spatial_split.py](../src/geospatial/create_spatial_split.py), [leakage.py](../src/geospatial/leakage.py) | `results/tables/spatial_leakage_summary.csv`, `spatial_distance_summary.csv` | Document, 8.2: splitul spațial nu e independent geografic |
