# Engangsopsætning

Det her skal gøres én gang. Regn med 45-60 minutter. Du skal selv oprette Meta-appen og indsætte nøglerne; de må aldrig deles i chatten eller skrives i en fil i repoet.

## 1. Gør Instagram-kontoen klar (2 min)

I Instagram-appen på @hverdag.med.ai:
- Skift til en **professionel konto** (creator eller virksomhed) under *Indstillinger → Kontotype og værktøjer*.
- Sørg for, at kontoen er **offentlig**.

## 2. Slå GitHub Pages til (2 min)

Billederne skal ligge offentligt, så Instagram kan hente dem.

1. Gå til repoets **Settings → Pages**.
2. Under *Build and deployment*: vælg **Deploy from a branch**, branch **main**, mappe **/ (root)**, og tryk **Save**.
3. Efter et par minutter er siden live på `https://thomascarlsson.github.io/hverdag-med-ai/`.

## 3. Opret en Meta-app (15-20 min)

1. Gå til **developers.facebook.com**, log ind, og vælg **My Apps → Create App**.
2. Vælg use case **Other**, derefter app-typen **Business**.
3. Giv appen et navn, fx `hverdag-med-ai-poster`, og skriv din e-mail.
4. Find **Instagram** på listen over produkter, og tryk **Set up**. *API setup with Instagram login* tilføjes automatisk.
5. Under *API setup with Instagram login*: tilføj **@hverdag.med.ai** som Instagram-konto/tester, og log ind på den, når du bliver spurgt.
6. Tryk **Generate token** ud for kontoen, og godkend adgangen. Kopiér nøglen, og indsæt den med det samme i trin 4. Den vises kun én gang.

Appen kan blive i udviklingstilstand, fordi den kun bruges til din egen konto. Beder Meta om *App Review* eller virksomhedsverificering, før posting virker, så skriv til Claude, så finder vi en vej.

## 4. Gem nøglerne som hemmeligheder i GitHub (5 min)

Gå til repoets **Settings → Secrets and variables → Actions → New repository secret**:

| Navn | Værdi |
|---|---|
| `IG_TOKEN` | Nøglen fra trin 3.6 |

Hemmeligheder kan ingen se igen, heller ikke på et offentligt repo.

## 5. Automatisk fornyelse af nøglen (10 min)

Instagram-nøglen gælder i ca. 60 dage. Repoet fornyer den selv den 1. og 15. hver måned, men skal have lov til at gemme den nye nøgle:

1. På GitHub: dit profilbillede → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Navn: `hverdag-forny-noegle`. Udløb: 1 år. *Repository access*: **Only select repositories** → `hverdag-med-ai`.
3. Under *Permissions → Repository permissions*: sæt **Secrets** til **Read and write**.
4. Generér, kopiér, og gem den som hemmeligheden **`GH_PAT`** (samme sted som i trin 4).

Husk at forny denne GitHub-nøgle om et år.

## 6. Test (5 min)

1. Gå til fanen **Actions**. Tillad workflows, hvis GitHub spørger.
2. Vælg **Forny Instagram-nøgle → Run workflow**. Den skal blive grøn. Så virker nøglen.
3. Vælg **Post til Instagram → Run workflow**. Den skal blive grøn og skrive, at intet var klar til posting endnu.

Herefter poster systemet selv, når første opslag rammer sit tidspunkt.

**Bemærk:** GitHub slår tidsstyrede workflows fra i offentlige repos uden aktivitet i 60 dage. Den ugentlige levering fra Claude holder repoet aktivt.
