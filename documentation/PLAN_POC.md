# Plan: de la EuroSAT la POC-ul „pierderi de pădure în România pe Sentinel-2" (15 decembrie)

## Context

Proiectul de încălzire (EuroSAT + ResNet18) e terminat, documentat și pe GitHub. Urmează POC-ul cerut de prof pentru 15 decembrie. Teodor vrea: bazele învățate temeinic, drumul spre tema cu defrișările, seturile de date, teste ca să înțeleagă codul, un aport personal clar și o împărțire în „musai" și „dacă reușesc". Timp rămas: 14 zile întregi (azi, 14 nov, e consumată) plus seri de 1–2 ore.

Presupunere: proful acceptă direcția. Dacă propune altă temă, zilele 1 și serile din prima săptămână rămân valabile (sunt fundamente), iar restul se replanifică.

## Ce cere proful și cum răspunde planul

| Cerința | Răspunsul |
|---|---|
| POC până pe 15 decembrie | Lanț complet pe o zonă: date → etichete → baseline → U-Net → hartă cu roșu + arie |
| Prezență și comunicare | Câte un rezultat de arătat după fiecare weekend; mesaj scurt de progres pe 22 nov și 6 dec |
| Parte practică consistentă, autonomie | Date construite de tine, nu un set gata făcut; comparație cu baseline; evaluare cinstită |
| Folosirea AI | Regula ta: nimic în proiect ce nu poți explica; testele de mai jos o verifică |

## Tema și aportul tău

**Formulare corectă:** din satelit se vede *pierderea acoperirii forestiere* (tăiere rasă, doborâturi de vânt, gândaci de scoarță, incendiu), nu „defrișarea" în sens legal. Titlu de lucru: „Detecția pierderilor de pădure din Carpații românești pe imagini Sentinel-2 cu rețele de segmentare".

**De ce e loc de contribuție:** căutarea nu a găsit un benchmark deschis de segmentare a tăierilor pe Sentinel-2 pentru Europa Centrală și de Est; cel mai apropiat e setul din Ucraina (regiunea Harkov). Hărțile existente pentru România (Hansen, EFDA) sunt la 30 m, din Landsat.

**Întrebările de cercetare (disertația întreagă):**
1. Poate un model antrenat pe etichete slabe de 30 m să producă măști mai fine, la 10 m, pe Sentinel-2? Se măsoară pe un set de test verificat manual.
2. Cât câștigă o rețea față de un prag pe diferența de indici (dNBR/dNDVI)?
3. Ajută benzile în plus (NIR, SWIR) și ponderile preantrenate pe Sentinel-2 față de ImageNet? (continuă întrebarea din proiectul EuroSAT)
4. Generalizează modelul într-o zonă pe care nu a văzut-o? (split pe blocuri geografice, lecția învățată deja)

**Ce înseamnă întrebarea 2.** Baseline-ul e o metodă fără antrenare, de vreo 30 de linii: NBR = (B08 − B12) / (B08 + B12) e mare pentru pădure sănătoasă și scade brusc după tăiere. dNBR = NBR dinainte − NBR de după; pixelii peste un prag sunt marcați „pierdere". Rețeaua trebuie să-l bată pe același test, altfel nu se justifică. Costă o zi (Z3) și dă prima hartă cu roșu cu trei săptămâni înainte de termen.

**Este suficient?** Pentru POC, da. Pentru disertație, da dacă există setul de test verificat manual și cel puțin două comparații făcute riguros (cu seed-uri). Nu e o arhitectură nouă, ci un set de date nou pentru o regiune și o evaluare corectă, ceea ce e o contribuție aplicată legitimă la nivel de master. Ar fi slab doar „am rulat U-Net pe etichetele altcuiva", fără validare proprie. Judecătorul final e proful: întreabă-l direct, la prima întâlnire, dacă întrebările 1–4 sunt de ajuns.

**Ce e al tău, concret:**
- setul de date pentru România (compozite Sentinel-2 anuale + etichete aliniate), reproductibil din cod;
- un set de test verificat de tine manual, la 10 m;
- protocolul de evaluare pe blocuri geografice și comparația baseline vs. rețea;
- harta cu roșu și aria pe an, comparate cu Hansen și EFDA.

## Seturi de date

| Ce | Rol | De unde |
|---|---|---|
| Sentinel-2 L2A, 10 m | Intrarea modelului: compozite de vară (iun–aug) pe an, benzi B02, B03, B04, B08, B11, B12 | Google Earth Engine (`COPERNICUS/S2_SR_HARMONIZED`) sau [Copernicus Data Space](https://dataspace.copernicus.eu) |
| European Forest Disturbance Atlas (EFDA) | Etichete principale: perturbări anuale 1985–2024, 30 m, 38 de țări, cu tipul cauzei; CC BY 4.0 | [Zenodo](https://zenodo.org/records/21722408), [pagina TUM](https://www.lss.ls.tum.de/en/eoem/datasets/european-forest-disturbance-atlas-efda/) |
| Hansen Global Forest Change v1.12 | Etichete de comparație: anul pierderii 2001–2024, 30 m | [pagina de descărcare](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/download.html), în GEE `UMD/hansen/global_forest_change_2024_v1_12` |
| Eșantioane de referință EFDA | Puncte verificate de experți, pentru validare | [Zenodo](https://zenodo.org/records/20431478) |
| Tăieri rase în Ucraina (Sentinel-2) | Plan B: poligoane desenate manual, ~36 GB | [Kaggle](https://www.kaggle.com/datasets/isaienkov/deforestation-in-ukraine), [cod](https://github.com/QuantuMobileSoftware/forest_change_detection) |

De verificat în ziua 2: formatul fișierelor EFDA pentru România și dacă Hansen are deja v1.13 (2025). Volumul e mic: o zonă de 50×50 km la 10 m cu 6 benzi are ~300 MB pe an, deci totul stă local.

## Musai și „dacă reușesc"

**Musai pentru 15 decembrie**
- [ ] M1. Compozite Sentinel-2 pentru o zonă, cel puțin 3 ani consecutivi
- [ ] M2. Etichete EFDA și Hansen aliniate pixel cu pixel la imagini
- [ ] M3. Baseline fără rețea: prag pe dNBR → mască, hartă cu roșu, arie în hectare
- [ ] M4. U-Net antrenat, cu split pe blocuri geografice; IoU și F1 pe test
- [ ] M5. Tabel baseline vs. U-Net pe același test
- [ ] M6. Inferență pe toată zona: hartă pe an și arie pe an, lângă cifrele Hansen/EFDA
- [ ] M7. Document de 8–10 pagini și prezentare de 10 minute
- [ ] M8. Poți explica fiecare pas fără notițe (testele trecute)

**Dacă reușesc, în ordinea valorii**
- [ ] N1. Set de test verificat manual (40–60 de patch-uri în QGIS) — devine musai pentru disertație
- [ ] N2. Câte 3 seed-uri la comparația principală, cu medie ± abatere
- [ ] N3. Ablație pe benzi: RGB vs. RGB+NIR vs. toate 6
- [ ] N4. Encoder preantrenat pe Sentinel-2 (SSL4EO-S12) vs. ImageNet
- [ ] N5. Rețea siameză bi-temporală (Daudt) vs. U-Net cu anii concatenați
- [ ] N6. A doua zonă, nevăzută la antrenare
- [ ] N7. Teste automate (pytest) pentru pregătirea datelor
- [ ] N8. Hartă interactivă (folium, ca `eurosat_map.html`)

**Pentru disertație, după POC:** mai multe zone din Carpați, detecție sezonieră/lunară pe serii de timp, separarea tăierilor de doborâturi cu tipul cauzei din EFDA, statistici pe județe, radar Sentinel-1 pentru lunile cu nori.

## Calendar

| Când | Înveți | Faci | Rezultat |
|---|---|---|---|
| **Z1 · D 15 nov** | Bucla de antrenare, `train/eval`, `no_grad`, batch norm, weight decay, pe `runner.py` rând cu rând | Exercițiile 1–4 de mai jos; trimiți mesajul și documentul la prof; **faci cont Google Earth Engine** (aprobarea poate dura) | Test 1 |
| Seri 16–20 nov | ResNet (secțiunile 1 și 3), U-Net | Primul script GEE: afișezi o imagine Sentinel-2 a unei zone | Test 2 |
| **Z2 · S 21 nov** | L1C vs. L2A, mascarea norilor, compozit median, CRS, reeșantionare | Alegi zona după harta EFDA (cu multe perturbări); exporți compozitele pe ani și etichetele; le deschizi în QGIS | M1, M2 |
| **Z3 · D 22 nov** | NDVI, NBR, IoU, precizie/recall, aria unui pixel | dNBR între ani consecutivi, prag, mască, suprapunere cu roșu, hectare pe an, comparație cu etichetele | M3; mesaj de progres la prof cu prima hartă |
| Seri 23–27 nov | Change detection (Daudt), EFDA (cum s-au făcut etichetele), Dice vs. cross-entropy | Instalezi `segmentation_models_pytorch`; treci un tensor prin U-Net și urmărești formele | Test 3 |
| **Z4 · S 28 nov** | Segmentare vs. clasificare, dezechilibru de clase, split pe blocuri | Tai zona în patch-uri 256×256; intrare = anul t și t+1 concatenate; țintă = pierderea din t+1; `Dataset` după modelul `EuroSATDataset`; normalizare doar din antrenare | Set de date gata |
| **Z5 · D 29 nov** | Encoder–decoder, skip connections, BCE + Dice, augmentări, precizie mixtă | Prima antrenare U-Net (encoder ResNet34, prima convoluție adaptată ca în `_adapt_first_convolution`) | Primul IoU pe validare |
| **Z6 · L 30 nov** | Analiza erorilor | Predicții lângă etichete pe 30 de patch-uri; corectezi ce e stricat; evaluezi pe test | M4, M5 |
| **Z7 · M 1 dec** | Inferență cu fereastră glisantă | Hartă pe toată zona pentru fiecare an; arie pe an; grafic față de Hansen/EFDA | M6 |
| **Z8 · M 2 dec** | Zgomotul etichetelor | Verifici manual 40–60 de patch-uri în QGIS; reevaluezi modelul și etichetele pe ele | N1 |
| **Z9 · J 3 dec** | Proiectarea unui experiment | Unul dintre N2–N4, ales după ce a mers mai ușor | Un al doilea rezultat |
| **Z10 · V 4 dec** | — | Rezervă: recuperezi ce a rămas în urmă | — |
| **Z11 · S 5 dec** | Scrierea unui raport | Documentul, generat din rezultate ca `build_documentation.py` | M7 (document) |
| **Z12 · D 6 dec** | — | Prezentarea; trimiți ciorna la prof | M7 (prezentare) |
| Seri 7–11 dec | Recapitulare | Corecturi după răspunsul profului | Test 4 |
| **Z13 · S 12 dec** | — | Rezervă și finisaje | — |
| **Z14 · D 13 dec** | — | Susținere de probă: eu pun întrebările profului | M8 |

**Punct de control pe 29 nov seara:** dacă nu există încă un U-Net care învață ceva, treci la planul B (setul din Ucraina pentru antrenare, România doar la inferență) și renunți la N-uri.

## Cum arată o zi de lucru

0. **Recapitulare, 10 min:** 5 întrebări din zilele trecute (din `documentation/invatare/flashcards.csv`, în repository-ul AI_LandCover_POC), înainte de orice altceva. Ce nu știi revine și data viitoare.
1. **Teorie, 45–60 min:** îți explic conceptele zilei pe exemple mici, înainte de orice cod. Nu trecem mai departe până nu le poți spune cu vorbele tale.
2. **Tu scrii, 1–2 ore:** o bucată mică și bine delimitată, cu indicații, nu cu soluția. Eu o revizuiesc și îți explic ce aș schimba.
3. **Eu scriu, tu citești:** partea de instalații (descărcare, aliniere, salvare, grafice). O parcurgem împreună și trebuie să o poți explica.
4. **Test, 15 min:** 5 întrebări la final.

## Cine scrie ce

| Scrii tu (cu revizie) | Scriu eu (tu citești și explici) |
|---|---|
| Z1: bucla de antrenare pe un singur lot, de la zero | Exportul din Earth Engine și descărcarea |
| Z3: `ndvi()`, `nbr()`, `iou()`, aria în hectare | Alinierea etichetelor de 30 m la grila de 10 m |
| Z4: `__getitem__` pentru noul `Dataset` | Tăierea în patch-uri și fișierul CSV de split |
| Z5: bucla de antrenare pentru U-Net, pornind de la `train_one_epoch` | Inferența cu fereastră glisantă, hărțile |
| Z6: funcția care afișează predicție lângă etichetă | Generatorul de document |

Dacă scrisul de cod merge mai încet decât e planificat, se taie din lista „dacă reușesc", nu din înțelegere și nu din M1–M8.

## Cum se construiește setul de date

Nu e o bază de date propriu-zisă, ci același tipar ca la EuroSAT: un folder cu fișiere GeoTIFF și un CSV care spune ce e fiecare.

1. Alegi un dreptunghi pe hartă (colțurile, în coordonate).
2. Un script cere din Earth Engine, pentru fiecare an, mediana imaginilor de vară fără nori din acel dreptunghi și o salvează ca GeoTIFF (`data/s2/2021.tif`, …).
3. Același script decupează etichetele EFDA și Hansen pe același dreptunghi.
4. Etichetele sunt aduse pe grila imaginilor, ca pixelul (i, j) să însemne același loc în toate fișierele.
5. Totul se taie în patch-uri de 256×256, iar un CSV ține: patch, an, bloc geografic, subset.

Toate sursele sunt gratuite: Sentinel-2 e deschis oricui, Earth Engine e gratuit pentru uz academic (cere doar înregistrare), EFDA și Hansen au licență CC BY 4.0.

## Teste

După fiecare etapă primești în chat 5 întrebări, răspunzi fără cod în față, iar eu corectez ca azi. Pe lângă ele, exerciții de tip „prezici, apoi rulezi", pe codul tău:

1. **Supraînvață un singur lot.** Antrenezi pe 32 de imagini până la loss ≈ 0. Dacă nu ajunge, e o greșeală în buclă.
2. **Uită `model.eval()`.** Evaluezi pe validare cu și fără; explici diferența prin `running_mean`.
3. **Urmărește formele.** Printezi dimensiunea tensorului după fiecare etapă din ResNet18, pentru 3 și pentru 13 canale.
4. **Calculează de mână.** Eroarea standard a acurateței; IoU pe o mască 4×4; numărul de parametri ai primei convoluții.
5. (Z3) **Scrie tu IoU** în numpy, fără bibliotecă, și verifică-l pe un exemplu făcut pe hârtie.
6. (Z5) **Strică ceva intenționat:** normalizare calculată din test, split aleator pe patch-uri vecine; vezi cum crește fals scorul.

## Concepte de bifat

- **Rețele:** convoluție, pas, padding, câmp receptiv, batch norm (lot vs. `running_mean`), bloc rezidual, encoder–decoder, skip connections în U-Net
- **Antrenare:** forward/backward, optimizator, AdamW și weight decay, rată de învățare, cosine + warmup, early stopping, augmentări, precizie mixtă, seed
- **Evaluare:** cele trei seturi, scurgere de informație, overfitting, acuratețe vs. F1, IoU, precizie/recall, medie ± abatere pe seed-uri, eroare standard
- **Teledetecție:** benzi și indici (NDVI, NBR), L1C/L2A, nori și compozite, rezoluție, CRS și reproiecție, GeoTIFF, autocorelare spațială
- **Segmentare și schimbare:** mască, dezechilibru de clase, Dice, fereastră glisantă, intrare bi-temporală, etichete slabe
- **Inginerie:** Git, structura unui experiment, rezultate reproductibile din cod

## De citit

- ResNet: https://arxiv.org/abs/1512.03385
- U-Net: https://arxiv.org/abs/1505.04597
- Daudt (siameze pentru change detection): https://arxiv.org/abs/1810.08462
- EFDA: https://essd.copernicus.org/articles/17/2373/2025/
- Hansen: https://www.science.org/doi/10.1126/science.1244693
- Tăieri în Ucraina pe Sentinel-2: https://ieeexplore.ieee.org/abstract/document/9241044
- SSL4EO-S12: https://arxiv.org/abs/2211.07044
- Validare spațială (Roberts): https://onlinelibrary.wiley.com/doi/10.1111/ecog.02881
- Practic: https://d2l.ai/chapter_convolutional-modern/resnet.html · https://developers.google.com/earth-engine/guides · https://smp.readthedocs.io · https://torchgeo.readthedocs.io

Numerele arXiv sunt din memorie; dacă unul deschide altă lucrare, caută titlul.

## Riscuri

- **Etichete de 30 m pe imagini de 10 m:** marginile sunt imprecise. De aceea contează setul verificat manual și comparația cu baseline-ul pe același test.
- **Anul din etichetă:** o tăiere din toamnă apare în compozitul verii următoare. Se verifică vizual în Z2–Z3 și se decalează anul dacă e cazul.
- **Dezechilibru:** pierderile sunt 1–2% din pixeli. Se aleg patch-uri care conțin pădure, se folosește Dice, se raportează IoU pe clasa „pierdere", nu acuratețea.
- **Accesul la date:** dacă GEE nu e aprobat până pe 21 nov, se descarcă din Copernicus Browser, manual, pentru doi ani.

