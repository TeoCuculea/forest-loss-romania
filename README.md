# Pierderi de pădure în Carpații românești pe Sentinel-2

Proiect de disertație: detecția, cu rețele de segmentare, a zonelor în care pădurea a dispărut de la un an la altul (tăieri, doborâturi de vânt, gândaci de scoarță, incendii), cu hartă și arie în hectare.

Stadiu: pregătirea datelor. Planul pe zile este în [documentation/PLAN_POC.md](documentation/PLAN_POC.md), iar starea fiecărui livrabil în [documentation/TRASABILITATE.md](documentation/TRASABILITATE.md). Exercițiul de încălzire (clasificare EuroSAT cu ResNet18) este în repository-ul separat `AI_LandCover_POC`.

## Date

| Ce | Sursă | Unde ajunge |
|---|---|---|
| Etichete: European Forest Disturbance Atlas v3.0, 30 m, 1985–2024 | `Romania.zip` de pe [Zenodo](https://zenodo.org/records/21722408), despachetat | `data/efda/` |
| Imagini: Sentinel-2 L2A, compozite de vară la 10 m | catalogul public [Earth Search](https://earth-search.aws.element84.com/v1), fără cont | `data/sentinel2/aoi_<nr>/s2_<an>.tif` |

Folderul `data/` nu este în Git. Totul e ținut în EPSG:3035, pe o grilă comună: 3×3 pixeli de imagine acoperă exact un pixel de etichetă.

## Pași

Toate comenzile se rulează din rădăcina proiectului.

```powershell
python -m pip install -r requirements.txt

# 1. Zonele candidate: cele mai perturbate celule de 46 km din România
python -m forest.select_aoi

# 2. Compozite Sentinel-2 pentru o zonă și câțiva ani
python -m forest.data.sentinel2 --candidate 1 --years 2023 2024

# 3. Figură de control: imaginea cu etichetele suprapuse
python -m forest.plot_quicklook --candidate 1 --year 2024
```

## Structura

```text
forest/
  config.py            Căi și constante (grilă, benzi, sezon, mărimea zonei)
  select_aoi.py        Clasamentul zonelor după hectarele perturbate
  plot_quicklook.py    Verificarea vizuală a alinierii imagine–etichete
  plot_style.py        Aspectul comun al figurilor
  data/
    efda.py            Citirea etichetelor pe un an și un dreptunghi
    sentinel2.py       Căutarea scenelor, mascarea norilor, mediana pe pixel
results/               Tabele și figuri mici
documentation/         Planul și matricea de trasabilitate
```
