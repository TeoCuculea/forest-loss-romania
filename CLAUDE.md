# Forest_Lost_Romania

Disertația lui Teodor (master ML): detecția pierderilor de pădure din Carpații românești pe Sentinel-2, cu segmentare. POC cu termen **15 decembrie 2026**. Repository GitHub: `TeoCuculea/forest-loss-romania` (privat).

- Planul pe zile, cu ce e musai (M1–M8) și ce e opțional (N1–N8): [documentation/PLAN_POC.md](documentation/PLAN_POC.md).
- Starea fiecărui punct: [documentation/TRASABILITATE.md](documentation/TRASABILITATE.md). Se actualizează la fiecare pas terminat.
- Jurnalul zilnic, cu deciziile și lista „de verificat": [documentation/JURNAL.md](documentation/JURNAL.md). Se completează la sfârșitul fiecărei sesiuni.
- Exercițiul de încălzire (EuroSAT, ResNet18) și materialele de învățare de până acum sunt în `e:\AI-LandCover_POC` (`documentation/invatare/`, `exercises/`). Exercițiile noi, despre acest proiect, se pun aici, în `exercises/`.

## Cum se lucrează cu Teodor

- Răspunde în română. Explică prin flow și prin legătura cu ce știe deja.
- O zi de lucru: 5 întrebări din zilele trecute, teorie pe exemple mici, apoi el scrie o bucată delimitată, apoi citește ce ai scris tu, apoi 5 întrebări noi.
- Bucățile marcate „scrii tu" în plan **nu se rezolvă în locul lui**. Dai indicii, îi revizuiești încercarea, spui ce parte e corectă și corectezi raționamentul.
- Regula lui: nu rămâne în proiect cod pe care nu-l poate explica.
- Când ceva amenință termenul, se taie din lista N, nu din M1–M8 și nu din înțelegere. Spune devreme.

## Date și convenții

- Etichete: EFDA v3.0 în `data/efda/` (30 m, o bandă pe an, 1985 = banda 1; cauze: 1 vânt/gândaci, 2 incendiu, 3 tăiere).
- Imagini: compozite de vară Sentinel-2 L2A în `data/sentinel2/aoi_<nr>/`, 6 benzi (B02, B03, B04, B08, B11, B12), valori = reflectanță × 10000, 0 = fără date.
- Grila comună: EPSG:3035; 3×3 pixeli de 10 m acoperă exact un pixel de etichetă. Zonele au 46.080 m pe latură (1536 pixeli de etichetă, 18 patch-uri de 256).
- `data/` și `*.pth` nu sunt în Git.
- Cod, nume și comentarii în engleză; texte din figuri și documentație în română.
- Figurile folosesc `forest/plot_style.py` și se salvează pe disc.
- Din satelit se vede pierderea acoperirii forestiere, nu legalitatea ei: nu scrie „defrișare ilegală" nicăieri.

## Comenzi

```powershell
python -m forest.select_aoi
python -m forest.data.sentinel2 --candidate 1 --years 2023 2024
python -m forest.plot_quicklook --candidate 1 --year 2024
```
