# @hverdag.med.ai – automatisk posting

Dette repository poster opslagene til Instagram-profilen **@hverdag.med.ai** helt automatisk.

**Sådan kører det:**
- Hver fredag laver Claude næste uges fem opslag og lægger dem i mappen `queue/`. Du får besked i chatten.
- Hver time tjekker GitHub, om et opslag skal ud, og poster det på Instagram.
- Tidspunkter: mandag, onsdag og fredag kl. 19:00, lørdag og søndag kl. 10:00 (dansk tid).

## Din kontrol

Alt kan gøres direkte på github.com eller i GitHub-appen: åbn filen, tryk på blyanten, ret og tryk **Commit changes**.

| Det vil du | Sådan gør du |
|---|---|
| **Stoppe al posting** | Åbn `config.json`, og ret `"pause": false` til `"pause": true`. Ret tilbage til `false` for at starte igen. |
| **Stoppe ét opslag** | Åbn `queue/<opslag>/opslag.json`, og ret `"status": "klar"` til `"status": "stop"`. |
| **Ændre teksten** | Ret `"billedtekst"` i opslagets `opslag.json`. Brug `\n` for linjeskift. |
| **Flytte tidspunktet** | Ret `"tidspunkt"`, fx `"2026-11-02T20:30:00+01:00"`. |
| **Ændre faste tidspunkter** | Ret `tid_hverdag` og `tid_weekend` i `config.json`. Gælder nye uger. |
| **Poste med det samme** | Sæt tidspunktet til nu, og kør *Actions → Post til Instagram → Run workflow*. |
| **Ændre et billede** | Skriv i chatten med Claude, hvad der skal ændres. |

Ændringer skal være gemt før opslagets tidspunkt. Opslagene ligger her senest fredag, så du har hele weekenden.

## Status på et opslag

Se `"status"` i hvert opslags `opslag.json`:

- `klar` – venter på sit tidspunkt
- `stop` – bliver ikke postet
- `postet` – ligger på Instagram (se `instagram_id`)
- `udløbet` – blev ikke postet inden for 12 timer efter tidspunktet, fx under en pause, og springes over
- `fejl` – fejlede tre gange; se `"note"` for grunden

Du kan også se hver kørsel under fanen **Actions**. En rød kørsel betyder, at noget fejlede.

## Mapper

- `queue/` – køen af opslag, én mappe pr. opslag med billeder og `opslag.json`
- `maskine/` – indholdsmaskinen, der laver billederne (se `maskine/LAESMIG.md`)
- `scripts/` – posting og kø
- `OPSÆTNING.md` – engangsopsætning af Instagram-adgang
