# Engangsopsætning

Det her skal gøres én gang. Nøglerne må aldrig deles i chatten eller skrives i en fil i repoet. De gemmes kun som hemmeligheder i GitHub.

## 1. Gør Instagram-kontoen klar ✅

@hverdag.med.ai er en professionel og offentlig konto.

## 2. Slå GitHub Pages til ✅

Billederne ligger offentligt på `https://hverdag-med-ai.github.io/hverdag-med-ai/`.

## 3. Opret Meta-appen ✅

Appen `hverdag-med-ai-poster` med use casen *Manage messaging & content on Instagram*.

## 4. Opret en Facebook-side og forbind Instagram (5 min)

1. Gå til **facebook.com/pages/create**, og opret en side, fx **Hverdag med AI**. Siden behøver ikke bruges til noget.
2. Forbind @hverdag.med.ai til siden. Det gøres fx på siden under *Indstillinger → Tilknyttede konti → Instagram → Forbind*, eller i Instagram-appen under *Rediger profil → Side*.

## 5. Giv appen de rigtige tilladelser (3 min)

1. I Meta-appen: **Use cases → Customize** → **API setup with Facebook login**.
2. Tilføj tilladelserne `instagram_basic`, `instagram_content_publish`, `pages_show_list` og `pages_read_engagement`.

## 6. Hent en nøgle, der ikke udløber (10 min)

1. Åbn **Graph API Explorer**: developers.facebook.com/tools/explorer
2. Vælg appen `hverdag-med-ai-poster` øverst til højre og *User or Page* = **User Token**.
3. Tilføj de fire tilladelser fra trin 5, og tryk **Generate Access Token**. Vælg Facebook-siden og Instagram-kontoen, når du bliver spurgt.
4. Tryk på det lille **i** ud for nøglen → **Open in Access Token Tool** → **Extend Access Token**. Kopiér den forlængede nøgle.
5. Tilbage i Explorer: indsæt den forlængede nøgle i nøglefeltet, skriv denne forespørgsel og tryk **Submit**:
   `me/accounts?fields=name,access_token,instagram_business_account`
6. I svaret finder du din side. Notér:
   - `access_token` – sidens nøgle. Den udløber ikke.
   - `instagram_business_account` → `id` – Instagram-kontoens ID.

## 7. Gem nøglerne som hemmeligheder i GitHub (3 min)

Gå til repoets **Settings → Secrets and variables → Actions → New repository secret**, og opret to:

| Navn | Værdi |
|---|---|
| `IG_TOKEN` | Sidens `access_token` fra trin 6 |
| `IG_USER_ID` | Instagram-kontoens `id` fra trin 6 |

Hemmeligheder kan ingen se igen, heller ikke på et offentligt repo.

## 8. Test (2 min)

1. Gå til fanen **Actions**. Tillad workflows, hvis GitHub spørger.
2. Vælg **Post til Instagram → Run workflow**. Den skal blive grøn og skrive, at intet var klar til posting endnu.

Herefter poster systemet selv, når første opslag rammer sit tidspunkt.

**Hvis nøglen holder op med at virke** (fx hvis du skifter Facebook-adgangskode), viser kørslerne under Actions en fejl. Gentag så trin 6 og 7.

**Bemærk:** GitHub slår tidsstyrede workflows fra i offentlige repos uden aktivitet i 60 dage. Den ugentlige levering fra Claude holder repoet aktivt.
