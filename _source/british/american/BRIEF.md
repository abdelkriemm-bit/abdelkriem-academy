# Writer brief — American Diploma (SAT · ACT · EST) English course, Abdelkriem Academy

Folder B = /tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/british
Read first: B/FORMAT.md (block format), B/american/SPEC.md (the ONLY exam facts you may state), this brief.
Write ONE JSON file per page: B/<course>/<slug>.json (course = sat, act or est), exactly the slugs you are given.
Helper scripts ONLY in your own new folder B/../work_<your-first-slug>/.

## Audience and goal
Egyptian American-Diploma students (Grades 10–12) and their parents. Many are not native speakers. The site must let a student
prepare 100% from it: every topic fully taught, then practised. Quality bar: better than the best commercial prep books
(Erica Meltzer, The College Panda, official guides) — clearer rules, more worked examples, smarter traps analysis.
NEVER copy or closely paraphrase any book, official test question or passage. Everything (rules wording, examples, passages,
questions) must be ORIGINAL. You may teach the same standard grammar/reading concepts.

## Page language
Clear, simple English (the test language). Add 1–3 Arabic help boxes per page ({"type":"box","style":"ar",...}) in simple
Egyptian-friendly Arabic for the key "how to" ideas (e.g. the one rule to remember, the classic trap). Don't translate the page.

## Lesson page shape (about 1,800–3,500 words)
1. h2 "What this question type tests" — how it appears on the test (with the exact question stem style, in your own words), how many
   questions (only from SPEC), where it sits.
2. The rules / the method, step by step (list, table). Grammar: each rule with ✓/✗ example pairs. Reading: a numbered method.
3. Worked examples: 3–5 ORIGINAL test-style items, each shown as: passage (blockquote-like "p"), question, 4 choices, answer,
   then WHY the answer is right and WHY EACH wrong choice is wrong (name the trap: too broad, too extreme, half-right, off-topic,
   reversed, comma splice, etc.).
4. box warning "Classic traps" and box tip "Fast strategy for test day".
5. h2 "Practice" + a "test" block in QUIZ mode (untimed, "timed": false) with 10–12 ORIGINAL questions in true test format.
6. box exam "Remember" — 3–5 bullet summary.

## The "test" block (interactive engine)
{"type":"test","title":"…","timed":false|true,"intro":"…",
 "sections":[{"name":"Module 1","minutes":32,"questions":[
   {"p":"passage text (optional; \n for line breaks; use __text__ to underline, **text** bold)",
    "q":"question stem",
    "c":["choice A","choice B","choice C","choice D"],
    "a":0,                      // index of the correct choice 0–3
    "e":"explanation: why correct + why the main wrong choices fail (1–3 sentences)",
    "s":"skill tag, e.g. Words in Context / Boundaries / Transitions / Subject–verb agreement"}]}]}
- Exactly 4 choices. Spread correct answers evenly over A/B/C/D (no pattern; roughly 25% each per test).
- SAT items: one short passage (25–150 words) per question, real SAT style stems, e.g. "Which choice completes the text with the
  most logical and precise word or phrase?", "Which choice completes the text so that it conforms to the conventions of Standard
  English?", "Which choice best states the main purpose of the text?", "Which choice most effectively uses data from the table to
  complete the example?", "Which choice most logically completes the text?", "The student wants to … Which choice most effectively
  uses relevant information from the notes to accomplish this goal?" For blanks write ______ in the passage.
  Tables/graphs: render data as a small text table inside "p" using lines (e.g. "Year | Visitors\n2019 | 1.2 million").
- ACT English items: a longer essay passage (~185–340 words) repeated in "p" for each of its questions, with the tested portion
  underlined (__like this__) and numbered [1], [2]…; choices usually start with "NO CHANGE".
- ACT Reading: 650–750-word passages, 9 questions each.
- Every key must be unambiguous: exactly one defensible answer. Double-check every item yourself before saving.

## The teacher's punctuation rules (Mohamed Abdelkriem) — follow them, they match the test
- Semicolon: joins two independent, closely related clauses. ONE exam-specific extra use exists and must be taught on SAT/ACT
  pages only, labelled clearly "SAT/ACT extra rule": semicolons can separate items in a list when the items already contain commas.
  Never teach that a semicolon "shows contrast".
- Colon: after a complete sentence, to introduce a list, an explanation, emphasis or extra information.
- A pair of dashes / a pair of commas / brackets = extra (non-essential) information; must match (dash…dash, comma…comma).
  Single dash = emphasis or an interruption.
- Never put a single comma between a subject and its verb or between a verb and its object.

## Rules
- Facts about the tests only from SPEC.md. Never invent scores, percentiles, dates, prices or university requirements.
- Never mention AI, Claude, ChatGPT or "generated". Author: Mohamed Abdelkriem (no "Mr."). No videos, images or external links
  except the official sites named in SPEC.md.
- Validate: python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(d['slug'])" file. Block types allowed: h2, p, list,
  table, box, model, qa, vocab, phrases, ex, en, test. Check each test item has 4 choices and a in 0–3.
- Final reply: slugs written + one line each + any doubt.
