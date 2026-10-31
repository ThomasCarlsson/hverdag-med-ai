# Billedstil til AI-billedgeneratoren

Stilbeskrivelsen sættes foran hver scene-beskrivelse, så alle billeder får samme udtryk.
Den er skrevet på engelsk, fordi de fleste billedgeneratorer forstår engelsk bedst.

Opbygning af en prompt:  **[STIL]** + **[SCENE]** + **[FASTE REGLER]**

---

## Variant A – Flad tegnestil (som hunden i uge 1)

**STIL**

> Flat vector illustration, soft rounded shapes, no outlines, gentle shading with at most two tones per shape. Cute, friendly characters with big round eyes, small rosy cheeks and simple happy expressions. Calm Scandinavian color palette: sage green, deep forest green (#2E5E4E), warm mustard yellow (#F2B544), terracotta (#C8643F), soft sky blue and warm cream (#F5F0E8). Clean, uncluttered composition with plenty of breathing room. Cozy, optimistic, everyday mood.

## Variant B – Blød 3D (tættere på "rigtige" dyr, men stadig tegnet)

**STIL**

> Soft 3D character render in a cozy storybook style. Animals look plush and huggable, with slightly exaggerated proportions, big expressive eyes and soft fur texture, clearly illustrated rather than photographic. Warm, diffused natural light, shallow depth of field, gentle pastel background. Color palette leaning on sage green, deep forest green, mustard yellow, terracotta and warm cream. Cozy, heartwarming, everyday mood.

## Variant C – Realistisk 3D-karikatur (humor, stopper scrollet)

**STIL**

> Hyper-detailed 3D caricature of an animal with realistic textures (individual fur strands, skin wrinkles, wet nose, detailed teeth) but strongly exaggerated cartoon proportions: oversized head and facial features, huge expressive grin or dramatic facial expression, human-like emotions. Soft studio lighting from the front, plain muted beige or warm neutral background, shallow depth of field. Funny, absurd and charming, never scary or grotesque.

Bedst til: humoristiske opslag og korte Reels, hvor dyrets udtryk er pointen. Fx "Mig, når madplanen for hele ugen er klar på 2 minutter".

---

## FASTE REGLER (bruges med begge varianter)

> Portrait format 4:5 (1080x1350). Keep the bottom 35% of the image calm and simple (grass, path, floor or plain background), because a text card will be placed there. Main character in the upper-middle part of the frame. No text, letters, logos or watermarks in the image. Original characters only, not resembling any known cartoon, mascot or brand character. Animals and people are always stylized cartoon characters, never photorealistic.

---

## Eksempler på SCENE-beskrivelser

- **Gåtur:** A small fluffy golden puppy with floppy brown ears on a leash, standing happily on a winding path through green rolling hills, round trees and a soft sun.
- **Morgenrutine:** A sleepy cartoon cat stretching on a windowsill next to a steaming cup of coffee, morning light through the window.
- **Madpakke:** A cheerful cartoon hedgehog packing a neat lunch box with sandwiches, carrots and apple slices on a kitchen table.
- **Søvn:** A tiny cartoon bear tucked into a cozy bed under a knitted blanket, a small lamp glowing, phone placed far away on a shelf.
- **Oprydning:** A cartoon raccoon happily sorting things into neat labeled boxes in a bright living room.
- **Regnvejr:** A cartoon duck in a yellow raincoat jumping in a puddle on a cozy city street with colorful houses.

## Sådan bruges den i maskinen

1. AI'en skriver ugens tip og en kort SCENE-beskrivelse på engelsk til hvert billedopslag.
2. Maskinen sætter STIL + SCENE + FASTE REGLER sammen til én prompt og sender den til billedgeneratoren.
3. Det færdige billede bruges som `scene`, og tippet sættes på i kortet nederst.
4. Ved godkendelsen tjekker du især: ser figuren sød og "rigtig" ud, er der ingen mærkelige poter, øjne eller tekst i billedet?

## Om mærkning

Med tydeligt tegnede figurer er der lille risiko for, at nogen tror, billedet er ægte. Vælger du Variant B eller C, eller bliver billederne meget livagtige, så slå "AI info"-mærkatet til på opslaget. Det tager få sekunder og koster ikke rækkevidde.
