# American Diploma practice expansion (requested 20 Nov 2026 by Mohamed Abdelkriem)

Goal: make SAT / ACT / EST practice stronger than Khan Academy and the big prep sites.
1. Every topic lesson gets its own practice page `<slug>-practice.html` with Practice 1–5 (10 questions each),
   rising difficulty: 1–2 Foundation, 3–4 Exam level, 5 Challenge. Instant feedback after every answer,
   with a reason for EVERY choice (why right / why wrong), best score saved, "retry my mistakes", mastery badge.
2. 10 full practice exams per test, exactly in the real format:
   - Digital SAT RW: 2 modules × 27 q × 32 min (tests 1–3 exist → add 4–10)
   - ACT English: 50 q / 35 min, 5 essays (3×10 q ~340 words, 2×5 q ~185 words) (tests 1–2 exist → add 3–10)
   - ACT Reading: 36 q / 40 min, 4 passages × 9 q (tests 1–2 exist → add 3–10)
   - EST: Literacy 1 44 q / 35 min + Literacy 2 52 q / 65 min (test 1 exists → add 2–10)
3. Hubs reorganised: clear "Practice exams" section, lesson tiles show practice progress.

## Files
- Topic practice source: `british/<course>/practice/<slug>.txt` (compact DSL, see `_engine/practice_dsl.py`)
  → built into `<slug>-practice.html` by pages/british_courses.py.
- Full exams: normal page JSON in `british/<course>/` (like sat-practice-test-1.json) + listed in course.json.
- Facts: only from american/SPEC.md. Teacher's punctuation rules: american/BRIEF.md. All items ORIGINAL.

## DSL (one file per topic)
```
STEM: default question stem for the topic (SAT)
## Practice 1 | Foundation
### Skill tag            (optional; sticky until changed)
P: passage text (can continue on following lines until a choice/Q line). Use ______ for blanks, __x__ underline.
Q: question stem (optional, else STEM)
A) choice || why it is right/wrong
*B) key choice || why it is right
C) ...
D) ...
(blank line between questions)
```
`P: @` reuses the previous passage. Choices are re-ordered by the build to balance A–D unless a choice is
"NO CHANGE" (stays A) or the question line has `[fixed]`.

## Progress (update after every batch)
- [x] engine + generator (practice pages, lesson buttons, hub badges) — published 20 Nov
- SAT topics: ALL 25 done (1,250 questions) — published 20 Nov
- Hubs: study-path intro boxes (English + Arabic) added to SAT/ACT/EST
- ACT English topics: (none yet)
- ACT Reading topics: (none yet)
- Full exams: SAT 1–3 ✓; ACT Eng 1–2 ✓; ACT Read 1–2 ✓; EST 1 ✓

## Next steps (in this order)
1. ACT English topics (26 lessons in act/course.json "ACT English" groups, skip act-overview/act-english-strategy):
   per set 2 short ACT essays (~180–220 words) × 5 questions, underlined __portion__ [n], "NO CHANGE" as first choice
   (STEM: "Choose the best version of the underlined portion. If the original is best, choose NO CHANGE.");
   whole essay repeated via `P: @` for its 2nd–5th questions. Rhetorical questions (add/delete, placement, writer's goal)
   get their own Q: line and no NO CHANGE.
2. ACT Reading topics (10 lessons): per set ONE passage (~400–450 words) × 6–8 questions on that skill.
3. Full exams: SAT 4–10, ACT English 3–10, ACT Reading 3–10, EST 2–10 (see top of this file for formats);
   add each to course.json "Full practice tests"/"Practice tests" groups; give test blocks "links" (skill → lesson) so
   results show "Study these again".
Publishing: build with the tolerant build (skips missing course/eng_exam.css and quran/tj_quiz.js), copy only
sat-/act-/est-/digital-sat/american pages to the repo root, push via GitHub API (Drive tgz → Composio workbench).
