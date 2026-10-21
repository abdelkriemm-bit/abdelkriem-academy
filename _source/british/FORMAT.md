# British courses — content format (for writers)

Site: Abdelkriem Academy (free, display-only study pages). Author: Mohamed Abdelkriem (exactly so, never "Mr.").
Audience: Egyptian students at British/international schools + their parents. Pages are in clear English (the exam language);
add a short Arabic tip only where it really helps a weak student (field "ar"). Never mention AI. Never copy past-paper texts or
mark-scheme wording at length (paraphrase the criteria; short quotes of a few words are fine). Every fact about the exam
(durations, marks, weightings, question types, task types, word counts, assessment objectives, themes) must come from the
research file for that course (<course>/SPEC.json) — if it is not there, do not state it.

## One page = one JSON file: <course>/<slug>.json
{"slug":"0510-email","title":"Informal Email (Exercise 5)","kicker":"Cambridge IGCSE ESL 0510 · Paper 1 · Writing",
 "summary":"one sentence shown under the title",
 "blocks":[ ...ordered blocks... ]}

Block types (use only these):
{"type":"h2","text":"…"}                                   section heading
{"type":"p","text":"…"}                                    paragraph (may contain **bold**)
{"type":"list","items":["…"],"ordered":false}              bullets / numbered steps
{"type":"table","headers":["…"],"rows":[["…"]]}            tables (mark breakdowns, structure, timing)
{"type":"box","style":"tip|warning|exam|ar","title":"…","text":"…" or "items":[…]}   highlighted box (style "ar" = Arabic tip, RTL)
{"type":"model","title":"…","task":"the exam-style prompt (original, not copied)","text":["paragraph 1","paragraph 2",…],
   "word_count":N,"marks":"e.g. 12/12 or Content 6/6 + Language 9/9","notes":["why it scores full marks: point → where in the answer", …]}
{"type":"qa","items":[{"q":"…","a":"…"}]}                  practice questions with answers (shown behind a "Show answer" button)
{"type":"vocab","items":[["word or phrase","meaning / when to use"]]}
{"type":"phrases","groups":[{"title":"Openings","items":["…"]}]}

Model answers must be ORIGINAL, exam-realistic, at the right length for the task (stated in SPEC.json; Year 8 Checkpoint samples
must be at least 350 words), and clearly full-mark quality with annotated notes explaining each mark criterion.
Validate every file with python json.load. Reply with the list of slugs you wrote.
