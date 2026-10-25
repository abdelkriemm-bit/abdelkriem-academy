# Writer brief — Checkpoint 6 & 8 Maths and Science (Abdelkriem Academy)

Root R = /tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad
Read first: R/british/FORMAT.md (page/block format), R/stem/PLAN_<course>.json (your pages, titles, objective codes),
R/stem/SPEC_<...>.md named in the plan (the ONLY source of curriculum and exam facts), this brief.
Write ONE JSON file per page: R/british/<course>/<slug>.json with keys slug, title (use the plan title), kicker, summary, blocks.
Helper scripts only in your own folder R/work_<your-first-slug>/.

## Goal and quality bar
Egyptian students in British/international schools (Stage 6 ≈ age 11, Stage 8 ≈ age 13) and their parents. A student must be able
to learn the whole topic from the page alone and be ready for Cambridge Checkpoint-style questions. Quality bar: better than the
best commercial Checkpoint books — clearer explanations, more worked examples, exam technique, common mistakes, full solutions.
Cover EVERY objective code listed for your page completely and at the right stage level (not above it, not below it).
Everything is ORIGINAL: never copy Cambridge past-paper or textbook questions, diagrams or wording. You may write questions in the
same STYLE as Checkpoint (short answers, "show your working", tick/ring, complete the table, explain, read a graph, etc. — see
SPEC section B for styles and mark-scheme conventions).

## Extra block types for these courses
{"type":"svg","svg":"<svg ...>...</svg>","caption":"…"}   a diagram (see SVG rules below)
Text in any block may use **bold**, x^{2} (superscript), H_{2}O (subscript). Use × ÷ − ≤ ≥ ≠ ° π √ as Unicode characters.

## Lesson page shape (about 1,500–3,000 words + quiz)
1. box style "exam" titled "In the curriculum" — the objective(s) in student-friendly words, each followed by its code in brackets.
2. h2 sections teaching the topic step by step: key words (vocab block with the Arabic word, e.g. ["numerator","البسط — the top number"]),
   rules, methods as numbered steps, tables, and DIAGRAMS (svg) wherever a picture helps (number lines, shapes, angles, graphs,
   circuits, food webs, organs as simple labelled outlines, apparatus, ray diagrams, particle diagrams…).
3. Worked examples: 4–6 Checkpoint-style questions, each with the question (marks in brackets), full step-by-step working and the
   answer, and a "common mistake" line where useful. Use p/list/table blocks; label them "Worked example 1" etc. in bold.
4. box warning "Common mistakes" and box tip "How Checkpoint asks this" (question styles and exam technique for this topic).
5. 1–2 Arabic help boxes (style "ar", simple Egyptian-friendly Arabic) for the key idea — especially for terms and the one rule to remember.
6. h2 "Practice" + ONE "test" block, "timed": false, 10–14 ORIGINAL questions mixing types (see engine below), with marks,
   from easy to Checkpoint-hard, each with a full solution in "e".
7. box exam "Remember" — 3–6 bullet summary.
Overview pages (…-overview): explain the real test from SPEC section B (papers, minutes, marks, calculator rules, question styles,
mark-scheme words like "show your working", "oe", "follow through" explained simply), how results are reported, how to use this
course (study plan), Thinking and Working Mathematically/Scientifically explained with examples, and an untimed 8-question quiz.
For Stage 8: say clearly that the Lower Secondary Checkpoint test is taken at the end of Stage 9 (per SPEC) and that this course
prepares Stage 8 students for their end-of-year tests in the same style and builds the base for Checkpoint.
Working-scientifically pages: variables (independent/dependent/control), fair tests, predictions, hypotheses, choosing equipment,
risks, repeat readings, anomalous results, tables, bar charts vs line graphs, drawing conclusions, evaluating — with many examples.
Sensitive topic (cp6s-growing-up): factual, brief, respectful, age-appropriate for 11-year-olds in a conservative community; name
the parts and the changes only as the objective requires; no diagrams of the reproductive organs; no images of people.

## The interactive "test" block (engine)
{"type":"test","title":"…","timed":false,"intro":"…","sections":[{"name":"Practice","minutes":20,"calc":true|false,"questions":[ … ]}]}
Question types (field "t"; omit for multiple choice):
- MCQ: {"q":"…","c":["A","B","C","D"],"a":2, …}  exactly 4 choices, a = index of the key. Use for tick/ring-style items.
- Number: {"t":"num","q":"…","ans":[90],"tol":0,"unit":"cm^{2}", …}  ans = accepted values (numbers, or fraction strings like "3/4";
  list equivalent forms if needed, e.g. [0.75,"3/4"]); tol = allowed absolute error (use for measurements/rounding, e.g. 0.05). The
  box accepts "28", "28 cm", "3/4". Never use num when the answer is not a single number (use text or open).
- Text: {"t":"text","q":"…","ans":["evaporation","evaporating"], …}  short exact answers: a word, coordinates "(3, -2)", a ratio "3:2",
  a letter. List every acceptable spelling/form (spacing and capitals are ignored automatically).
- Open: {"t":"open","q":"…","ms":"mark scheme: 1 mark for …; 1 mark for …", …}  explanations, drawings, constructions, "show that",
  sketches — the student self-marks against "ms" after finishing. Write the ms like a real mark scheme (what earns each mark,
  accept/do not accept).
Common fields: "p" (stem text, shared context for parts: e.g. "Question 5\nA shop sells…"), "img" (an SVG diagram string, same rules),
"m" (marks: 1–3; most 1–2), "e" (full worked solution — always), "s" (topic/skill tag, e.g. "Fractions", "Forces").
Multi-part Checkpoint questions: write each part as its own question with the same "p" stem and q starting "(a)", "(b)"…
At least 60% of questions should be auto-marked (num/text/mcq). Spread MCQ keys over A–D.

## SVG rules (diagrams must be CORRECT — compute coordinates with a script, never eyeball)
- Start with <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" width="W"> with W ≤ 560; no scripts, no event handlers,
  no external images/fonts/links; font-family="Arial, sans-serif"; font-size ≥ 16 (diagrams shrink on phones — a 560-wide diagram is shown about 350 px wide), keep W ≤ 480 when possible; stroke "#0f1b33", light fills (#eaf1fb, #fff4d6,
  #e3f4e5); labels never overlapping lines.
- Measurements shown must match the numbers in the question; angles drawn at the stated size (or say "not drawn to scale" — Checkpoint
  does this too); graphs: axes with labelled scales, points plotted exactly; grids for coordinates/transformations.
- Keep each SVG under ~6 KB. Render every SVG to PNG with Playwright/cairosvg and LOOK at it before finishing (Read the PNG).

## Facts, language, rules
- Curriculum and exam facts only from the SPEC file; never invent dates, grade boundaries, percentages of marks, or school rules.
- Science facts must be correct and at the right level; use SI units and the symbols listed in SPEC (appendix).
- British English spelling (metre, colour, centre). Numbers: thousands with a space or comma consistently (10 000 as Cambridge does).
- Never mention AI or "generated". Author: Mohamed Abdelkriem (no "Mr."). No external links except official Cambridge pages from SPEC.
- Validate: every file loads with json.load; only allowed block types (h2, p, list, table, box, model, qa, vocab, phrases, svg, test);
  every MCQ has 4 choices and a in 0–3; every num has a numeric ans; every open has ms; every question has e and m.
  Re-solve every question yourself before saving — an answer key error is the worst possible mistake.
- Final reply: slugs written, one line each, question counts, and any doubts.
- Number boxes accept mixed numbers like "1 3/4" (read as 1.75). Text answers keep spaces meaningful ("1 3/4" is not "13/4"); simplest-form answers should be text questions.
- Small tables inside "p" or "q": write each row on its own line with cells separated by " | " (first row = headings); the engine shows them as real tables.
