# Writer brief — practice expansion (Nov 2026). Read fully before writing anything.

Repo: /home/claude/abdelkriem-academy  (site source in _source/, B = _source/british)
Read first: B/american/PRACTICE_PLAN.md (goal + DSL), B/american/BRIEF.md (audience, teacher's punctuation rules),
B/american/SPEC.md (the ONLY exam facts you may state), B/american/TESTBRIEF.md (full practice tests).
House-style examples you MUST open and copy the format of:
- SAT topic practice: B/sat/practice/sat-semicolons.txt, sat-evidence-quantitative.txt, sat-cross-text.txt
- ACT English topic practice: B/act/practice/act-commas.txt
- Full tests: B/sat/sat-practice-test-1.json, B/act/act-english-test-1.json, B/act/act-reading-test-1.json,
  B/est/est-practice-test-1.json

## Your job
Write ONLY the files you are given. Never edit course.json, the engine, build scripts, other writers' files, or git
(no commits, no pushes). Helper scripts go only in /tmp/claude-0/work_<your-first-slug>/.

## Topic practice files (DSL .txt) — B/<course>/practice/<lesson-slug>.txt
- Exactly 5 sets: "## Practice 1 | Foundation", "## Practice 2 | Foundation", "## Practice 3 | Exam level",
  "## Practice 4 | Exam level", "## Practice 5 | Challenge". 10 questions per set (ACT Reading: 8 per set).
- Open the lesson JSON (B/<course>/<slug>.json) first: practise exactly what it teaches, at the right level.
- ACT English: ONE original essay per set (~280–340 words, with a title) holding 10 underlined portions
  `__text__ [n]`; first question gives the essay in `P:`, the rest use `P: @`; `Q: [n]` (the stem is added
  automatically). Choice A is always "NO CHANGE" for underlined-portion items; NO CHANGE should be the key in only
  2–3 of the 10 questions. Rhetorical items (add/delete, placement, writer's goal, transitions where relevant) get a
  full `Q: [n] …question…` line and no NO CHANGE choice (the stem then is the Q line).
  Every question in a set must test THIS lesson's skill (one or two may mix in an earlier skill as a distractor).
- ACT Reading: ONE original passage per set (~420–500 words; literary narrative, social science, humanities or
  natural science; paired-passage lesson: Passage A + Passage B ~250 words each; charts lesson: include a small
  text table using "a | b" lines) with 8 questions mostly on THIS lesson's skill; `P: @` for questions 2–8; each
  question has its own `Q:` line. Use line-free references ("in the third paragraph", "the phrase '…'").
- Each choice: `A) text || reason` — the reason says why that choice is right or wrong in plain English,
  NEVER mentioning a letter (choices are reshuffled at build time). Mark the key with `*`.

## Full practice tests (JSON pages) — B/<course>/<slug>.json
- Copy the exact structure of the existing test files (same blocks: h2 "Before you start" + text + Arabic box,
  ONE "test" block with "timed": true and the real sections/minutes, box exam "After the test").
- SAT: 2 modules × 27 questions, 32 minutes each; Module 2 slightly harder. ACT English: 50 questions / 35 min,
  5 essays (3 × 10 questions ~340 words, 2 × 5 questions ~185 words). ACT Reading: 36 questions / 40 min,
  4 passages × 9 (one literary narrative; one paired set or one with a chart). EST: Literacy Test 1 (Writing and
  Language) 44 questions / 35 min (4 passages × 11, underlined portions with NO CHANGE) + Literacy Test 2 (Reading)
  52 questions / 65 min (5 passages, about 10–11 questions each, one paired set, one with a table).
- Every question: "q", "c" (4), "a" (0–3), "e" (why the key is right AND why the strongest wrong choice fails),
  "ce" (array of 4 short reasons, one per choice, no letters), "s" (official skill name as in TESTBRIEF.md).
- Add to the test block: "links": {skill name → lesson page html} using lessons in that course's course.json
  (e.g. "Boundaries": "sat-sentence-boundaries.html"), so results can send students back to weak topics.
- Answer positions: each of A–D 22–28% per test, no run longer than 3. Topics must not repeat passages or topics of
  existing tests (open them and list their topics first).

## Quality rules (these are where errors happen — check every item)
1. Exactly ONE defensible answer. Before saving each item, read every wrong choice back into the sentence: if it is
   grammatical AND makes sense, it is NOT a wrong answer — change it. Classic traps to avoid: wrong options that are
   actually correct ("than it is", "which was…", appositive commas, "and yet", optional serial comma, singular
   "they", collective nouns that could be plural, "data suggest/suggests", starting a sentence with "But/Yet").
2. Never leave placeholders ("x", "Wait", "see below", "?") — finish every item properly before writing it down.
3. Teacher's rules (BRIEF.md): semicolon = joins two independent clauses (+ SAT/ACT extra rule: list items that
   contain commas); never "shows contrast". Colon after a complete sentence only. Matching pairs of dashes/commas/
   brackets for extra information.
4. Facts: use only real facts you are sure of; otherwise fictional people/places that are clearly generic
   ("a team of researchers", "one coastal town"). No invented quotes from real people. No mention of AI.
   Egyptian/Arab/world contexts welcome. Content must be suitable for teenagers.
5. ACT/EST style: British or American spelling consistently within a file (house style so far: British).

## Validate before you finish
python3 B/_engine/check_practice.py B/<course>/practice/*.txt   (topic files: must print [10,10,10,10,10] or [8,…])
For JSON tests: python3 -c "import json,sys;d=json.load(open(sys.argv[1]));t=[b for b in d['blocks'] if b['type']=='test'][0];q=[x for s in t['sections'] for x in s['questions']];assert all(len(x['c'])==4 and x['a'] in range(4) and len(x.get('ce',[]))==4 for x in q);import collections;print(d['slug'],[len(s['questions']) for s in t['sections']],collections.Counter('ABCD'[x['a']] for x in q))" FILE
Then re-read every key once more. Final reply: files written, counts, answer distribution, any doubts. Keep it short.
