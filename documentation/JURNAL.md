# Jurnal de lucru

Ce s-a făcut în fiecare zi, ce s-a decis și de ce. Se completează la sfârșitul fiecărei sesiuni, cu intrarea cea mai nouă jos. Deciziile au și motivul, ca să nu le rediscutăm de la zero.

## De verificat (nu uita)

- [ ] **Ce date oficiale despre tăieri se pot obține efectiv** (SUMAL 2.0 / Inspectorul Pădurii): se pot descărca în bloc parchetele autorizate, cu contur și an, sau doar consulta pe rând? De răspuns înainte de discuția cu proful despre temă.
- [ ] Alegerea zonei de studiu dintre cele trei candidate (`results/aoi_candidates.csv`).
- [ ] Dacă Hansen Global Forest Change are deja versiunea 1.13 (cu anul 2025).
- [ ] Răspunsul profului la mesaj și la propunerea de temă; de întrebat dacă întrebările de cercetare Î1–Î4 sunt de ajuns.

## Sâmbătă, 14 noiembrie 2026 — punctul de plecare

**De unde am pornit.** Proiectul de încălzire `AI_LandCover_POC` (EuroSAT, ResNet18) funcționa, dar avea structura încâlcită, o documentație neterminată și nu era în Git. Proful a acceptat reluarea colaborării cu trei condiții: POC până pe 15 decembrie, prezență, autonomie.

**Ce s-a făcut**
- Curățenie în proiectul EuroSAT, Git local și repository pe GitHub.
- Documentația Word refăcută cap-coadă, generată din rezultate (14 pagini, 11 figuri, 6 tabele).
- Mesajul de răspuns către prof, cu propunerea de temă.
- Planul pe zile pentru POC (`PLAN_POC.md`) și exercițiile pentru ziua 1.

**Ce am aflat**
- Diferențele dintre cele patru configurații EuroSAT (96,9–98,3%) nu sunt concludente: un singur seed, iar o rulare a fost oprită prea devreme de early stopping.
- Splitul „spațial" elimina suprapunerile, dar 38% dintre imaginile de test aveau imaginea vecină în antrenare. Nu era un test de generalizare geografică.
- Numele ultimelor cinci benzi erau decalate în cod (B8A este ultima în fișierele EuroSAT). Antrenarea nu a fost afectată.

**Decizii**
- Tema propusă: pierderi de pădure în Carpați pe Sentinel-2, cu segmentare. *Motiv:* continuă ce s-a învățat (benzi, split geografic, model preantrenat) și nu am găsit un benchmark deschis pentru regiune.
- Se spune „pierdere de acoperire forestieră", nu „defrișare ilegală". *Motiv:* din satelit nu se vede legalitatea.
- POC restrâns la o zonă de ~46 km și schimbare de la an la an. *Motiv:* 14 zile de lucru; toată România și detecția lunară rămân pentru disertație.
- Mod de lucru: teorie întâi, Teodor scrie bucățile marcate „scrii tu", teste după fiecare etapă. *Motiv:* nu rămâne în proiect cod pe care nu-l poate explica.

## Duminică, 15 noiembrie 2026 (noaptea) — datele, fără cont

**Ce s-a făcut**
- Etichetele EFDA v3.0 pentru România descărcate (2 GB) și citite: 30 m, o bandă pe an, cu cauza perturbării și mască de pădure.
- România împărțită în celule de 46 km; trei zone candidate alese după hectarele perturbate în 2019–2024.
- Script pentru compozite de vară Sentinel-2, citite din catalogul public Earth Search; probă pe zona 1.
- Fișe de concepte, flashcards și ghid de lectură (în `AI_LandCover_POC/documentation/invatare/`).
- Proiectul de pădure mutat în repository propriu (`forest-loss-romania`).

**Ce am aflat**
- Nu avem nevoie de cont Google Earth Engine: Sentinel-2 L2A se citește anonim din Earth Search.
- EFDA are tipul cauzei pe fiecare an (tăiere / vânt și gândaci / incendiu). În zonele candidate, cam jumătate din perturbări sunt tăieri.
- În anii vechi, aceeași scenă apare de două ori în catalog (procesare originală și reprocesată), cu scări diferite ale valorilor. Scriptul păstrează doar varianta nouă.

**Decizii**
- Etichete principale EFDA, Hansen doar pentru comparație. *Motiv:* EFDA e făcut pentru Europa, e mai recent și are cauza.
- Totul în EPSG:3035, cu imaginile la 10 m așezate exact peste grila etichetelor (3×3 pixeli pe un pixel de etichetă). *Motiv:* alinierea devine o simplă repetare de pixeli, fără reeșantionare a etichetelor.
- Zona are 46.080 m pe latură. *Motiv:* număr întreg de pixeli de etichetă (1536) și de patch-uri de 256 (18).
- Repository separat pentru pădure. *Motiv:* cel vechi rămâne exercițiul de încălzire, curat, de arătat ca atare.

**Greșeli prinse**
- Regula `data/` din `.gitignore` ascundea și folderul de cod `src/data/` din proiectul EuroSAT; trei fișiere lipseau de pe GitHub. Reparat și urcat.
- Un script de corecție a golit generatorul de documentație, care nu era încă în Git. Rescris. *Lecție:* commit imediat după orice fișier nou.

**Rămas pe mai târziu**
- Compozitul 2023 și figura de control a alinierii.
- Exercițiile de ziua 1 și Testul 1 (Teodor).

**Decizii luate dimineața**
- Disertația este în engleză (scrisă și prezentată). Tot ce e public trece în engleză: cod, texte din figuri, README, TRACEABILITY, raport, prezentare, mesaje de commit. Notele de lucru (plan, jurnal) rămân în română. *Motiv:* repository-ul poate fi văzut și de alții.
- Setul de test verificat manual urcă din „dacă reușesc" în „musai", în variantă mică (M9, 20–30 de patch-uri). *Motiv:* etichetele EFDA sunt derivate tot dintr-o schimbare de NBR, deci baseline-ul pe dNBR e avantajat când e notat după ele.
