# Photo + fact-check brief (Science lessons, Abdelkriem Academy)
R = /tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad
Lessons: R/british/<course>/<slug>.json (block format in R/british/FORMAT.md; extra block types: svg, test, photo).

## Part 1 — add real photos
For each of your lessons add 2–4 real photographs where a photo truly helps a student (real rocks, fossils, soils, the Moon and
planets, components and circuits, magnets and iron filings, prisms and spectra, chromatography paper, metals reacting, crystals,
apparatus, animals, plants, habitats and ecosystems (Egyptian ones when possible: Red Sea reef, Nile, desert, Sinai), micrographs of
blood cells or alveoli, an X-ray of a joint, a solar farm, a wind farm, a galaxy, an asteroid…). Skip a lesson only if no photo helps.
- Source: Wikimedia Commons only (NASA / ESA public-domain images are on Commons too). Licence must be Public domain, CC0, CC BY or
  CC BY-SA — read the licence and author from the file page / API (extmetadata: LicenseShortName, Artist). Never use "fair use" or
  non-free files.
- Use the API from the shell with a User-Agent header, e.g.
  curl -s -A "AbdelkriemAcademy/1.0 (abdelkriemacademy@gmail.com)" "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=filetype:bitmap%20granite&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=800&format=json"
  then download the thumburl (same User-Agent). If you get HTTP 429, wait and retry slowly (sleep between requests is fine inside
  a script; keep it to a few requests per second at most).
- Convert to WebP with Pillow: max width 800 px, quality ~78, under 130 KB. Save as R/abdelkriem-academy/images/sci/<slug>-<n>.webp.
- LOOK at every downloaded image (Read the file) before using it. It must clearly show what the caption says and be correct science.
  STRICT content rules: NO people at all (no faces, no bodies, no hands holding things if avoidable — never any woman or girl), no
  nudity, no medical/surgical photos, no brand logos, no visible text in other languages. For the lesson cp6s-growing-up add NO photos.
- Block to insert (in a sensible place in the lesson, right after the paragraph/section it illustrates; never inside quizzes/tests):
  {"type":"photo","src":"images/sci/<file>.webp","alt":"short description","caption":"what the student should notice (1 sentence)",
   "credit":"Photo: <Author> / Wikimedia Commons, <Licence>","w":<width>,"h":<height>}
  (credit is required for CC BY/BY-SA; for public domain write "Photo: <Author or NASA> / Wikimedia Commons, public domain").
- Keep every other block of the lesson unchanged. Validate the JSON after editing.

## Part 2 — fact-check
Read each of your lessons and list every specific factual claim that is not pure curriculum definition: numbers (melting/boiling
points, gravity on planets, composition of air, planet data, speeds of light, solubility values, percentages, dates), named examples
(places, species, events). Verify each one with WebSearch/WebFetch (reputable sources: encyclopaedias, NASA, universities, museums,
government sites). Fix anything wrong or misleading in the lesson text AND in quiz questions/answers/explanations that depend on it
(keep answer keys consistent!). If a figure is an approximation, say "about". Do not rewrite content that is correct.

## Output
- Log file R/stem/photos_<your-first-slug>.json: [{"slug","file","source_url","author","licence","caption"}] for every photo.
- Final reply: per lesson — photos added (with what they show) and the fact-check results (claims checked, any fixes made, with source URLs).
