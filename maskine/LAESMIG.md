# Hverdag med AI – indholdsmaskine (prototype)

Gør en uges indhold (én JSON-fil) til færdige Instagram-karruseller i 1080x1350.

## Sådan bruges den

1. Læg ugens indhold i `content/uge-XX.json` (se `uge-01.json` som skabelon).
2. Kør: `python3 render.py content/uge-XX.json`
3. Find billederne i `out/uge-XX/`, én mappe pr. opslag med billeder og `billedtekst.txt`, plus `oversigt.png` til hurtig godkendelse.

Kræver Python 3 med Pillow og skrifttypen Inter.

## Slide-typer

`step` (trin), `prompt` (kopiér-boks), `compare` (Før/Nu), `tip`, `mistake` (fejl) og `cta` (sidste slide). Forsiden laves automatisk ud fra `cover`.

## Farver og illustrationer

Hvert opslag har `theme` (green, navy, mustard eller terracotta) og `illustration` (navnet på en SVG i mappen `illustrations/`). Illustrationen bruges på forsiden og sidste slide. Nye illustrationer tilføjes som SVG-filer i samme mappe. Kræver `rsvg-convert`.

## Billedopslag

Et opslag med `"type": "image"` bliver ét billede: en tegnet scene i fuld størrelse (`scene`, en SVG eller senere et AI-genereret billede) med tippet (`tip_label` og `tip`) i et kort nederst. Dyr og mennesker tegnes altid som tegneseriefigurer.

## Næste skridt mod fuld automatik

1. **Indhold:** Lad en AI skrive ugens JSON-fil ud fra de fire søjler (AI-trick, prompts, før/efter, fejl og myter) via et API-kald.
2. **Godkendelse:** Kig `oversigt.png` igennem én gang om ugen, ret eller slet det, der ikke holder.
3. **Posting:** Upload de godkendte karruseller med et planlægningsværktøj eller direkte via Instagrams officielle API (kræver en creator- eller businesskonto).

Svar på kommentarer manuelt.

## Prompt-siden

Instagram kan ikke kopiere tekst fra billeder, så alle prompts ligger også på
https://hverdag-med-ai.github.io/hverdag-med-ai/prompts/ med en kopier-knap pr. prompt.
Linket står i Instagram-bioen. Siden bygges af `scripts/build_prompts.py` og viser kun
prompts fra opslag, der er postet, nyeste først. Den opdateres automatisk efter hver posting.
Prompt-slides skal have label "Prøv prompten" (ikke "Kopiér"), og billedteksten skal have
linjen "🔗 Kopiér prompten med ét tryk via linket i bio."
