# Split brief — one topic = one lesson (Nov 2026)

The site owner (Mohamed Abdelkriem) wants every SAT/ACT topic as its OWN lesson page, shown as a tile "Lesson N + short name".
Some current pages lump many topics together (e.g. act-grammar-usage teaches 9 topics on one page). You are rewriting such
content into several focused, complete, stand-alone lessons.

Folder B = /home/claude/abdelkriemm-bit/abdelkriem-academy/_source/british
Read first: B/FORMAT.md (block format), B/american/BRIEF.md (writer brief: audience, lesson shape, test block, the teacher's
punctuation rules, rules), B/american/SPEC.md (the ONLY exam facts you may state), then the SOURCE page(s) named in your task.

## What to write
For each slug you are given, write B/<course>/<slug>.json (course = act or sat) — a complete lesson on THAT topic only:
- Top-level fields: "slug", "nav" (the short tile name, 1–4 words, e.g. "Semicolons", "Pronoun Case"), "title" (full title),
  "kicker" (e.g. "American Diploma · ACT · English: Punctuation" / "American Diploma · ACT · Reading: Key Ideas and Details" /
  "American Diploma · Digital SAT · Grammar: Boundaries"), "summary" (one sentence), "blocks".
- Follow the lesson shape in BRIEF.md: what it tests → rules/method with ✓/✗ pairs → 3–4 worked examples with trap analysis
  for every wrong choice → box warning "Classic traps" → box tip "Fast strategy for test day" → 1–2 Arabic boxes (style "ar",
  simple Egyptian-friendly Arabic) → h2 "Practice" + ONE "test" block, "timed": false → box exam "Remember" (3–5 bullets).
- Length about 1,300–2,500 words of teaching (not counting the quiz). Go deeper than the source on THIS topic: more rules
  detail, more ✓/✗ pairs, the subtle cases the test likes.
- REUSE the source's good teaching, examples and questions that belong to your topic (adapt them), then add new ORIGINAL
  material so the page is complete. Never copy any book or official question.
- Practice quiz: 10 questions for grammar/English-skill pages, all on this topic (a few may mix in one earlier-taught skill as
  a distractor, but the key must test this topic).
  * ACT English pages: 2 short ACT-style essays (each ~185–250 words), 5 questions each, underlined portions __like this__
    numbered [1]…; choices usually start with "NO CHANGE"; the full essay text repeated in "p" for each of its questions
    (see the source page for exactly how existing ACT pages do this — copy that technique). Section name e.g. "Passages I–II",
    minutes ~ 8.
  * SAT pages: Digital SAT format, one short passage (25–150 words) per question, real SAT stems, section name "Quiz",
    minutes 13.
  * ACT Reading pages: ONE original passage of 600–750 words (in "p" of every question, as the source page does) with
    9 questions mostly on this question type; section "Passage 1", minutes 10. Choose a passage type (literary narrative,
    social science, humanities, natural science) that suits the skill; for paired-passage lessons use Passage A + Passage B
    (~350 words each); for charts lessons include a small text table in the passage.
- Exactly 4 choices, "a" index 0–3, answers spread roughly evenly over A–D, every key unambiguous, each "e" explains why
  right + why the main wrong choices fail, "s" = skill tag. Re-check every item yourself before saving.
- Do NOT edit or delete any other file (not the source pages, not course.json). Only write your own slugs. Helper scripts, if
  any, in a new folder /tmp/claude-0/work_<your-first-slug>/.
- Validate each file: python3 -c "import json,sys;d=json.load(open(sys.argv[1]));t=[b for b in d['blocks'] if b['type']=='test'];assert len(t)==1;q=[x for s in t[0]['sections'] for x in s['questions']];assert all(len(x['c'])==4 and x['a'] in range(4) for x in q);print(d['slug'],d['nav'],len(q))" FILE
- Final reply: slugs written, nav names, question count, answer-letter distribution, and any doubt. Keep it short.
