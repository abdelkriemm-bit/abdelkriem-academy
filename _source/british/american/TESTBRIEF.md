# Practice-test writer brief (add-on to BRIEF.md — read BRIEF.md, SPEC.md and FORMAT.md first)

A practice-test page = one JSON page (same page format as lessons) containing:
1. h2 "Before you start" + short p/list: what the test is, timing, how to use it (quiet place, timer on, no going back after a
   module/section ends in the real test), a note that the score shown is a practice percentage, not an official scaled score.
   Add one Arabic help box (style "ar") with the same advice in simple Egyptian Arabic.
2. ONE "test" block with "timed": true, real section timing, all items ORIGINAL.
3. box exam "After the test" — how to review: every explanation, list your weak skills, go back to the matching lessons
   (name the lesson titles from the course.json of your course).

Quality rules (critical):
- Every item has exactly one defensible answer. Wrong choices must be plausible but clearly wrong for a nameable reason.
- The "e" explanation says why the key is right AND names why the strongest wrong choice fails.
- The "s" skill tag must use the official skill names (SAT: Words in Context, Text Structure and Purpose, Cross-Text Connections,
  Central Ideas and Details, Command of Evidence — Textual, Command of Evidence — Quantitative, Inferences, Boundaries,
  Form, Structure, and Sense, Transitions, Rhetorical Synthesis. ACT English: Production of Writing, Knowledge of Language,
  Conventions of Standard English. ACT Reading: Key Ideas and Details, Craft and Structure, Integration of Knowledge and Ideas).
- Answer positions: count them at the end; each of A/B/C/D between 22% and 28% of the test, no runs longer than 3.
- Topics: varied (science, history incl. Egyptian/Arab/world history, arts, social science, literature). Use real-world facts only
  if you are sure they are true; otherwise use clearly fictional researchers/places (e.g. "a team led by biologist Dana Ruiz").
  Literary excerpts: write ORIGINAL texts in the style of older literature; do not quote real books or poems.
- Do not reuse passages or items from the lesson pages in british/<course>/ (you may glance at them to match house style).
- Different tests must not share passages; the topics list of each existing test file in the course folder must be avoided
  (check british/<course>/*test*.json before writing).
- Validate JSON, count questions per section, count answer distribution, and print them in your final reply.
- Helper scripts only in your own folder B/../work_<slug>/.
