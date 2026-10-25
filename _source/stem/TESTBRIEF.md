# Practice-test writer brief (STEM). Read R/stem/BRIEF.md first (all its rules apply), then this.
R = /tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad

A practice-test page = one JSON page (slug and title from the plan) with:
1. h2 "Before you start" + list: what the test is, the two papers (minutes, marks, calculator rules, equipment — from SPEC section B),
   "write on paper first if you like", how marking works here (typed answers are checked automatically; written answers you mark
   yourself with the mark scheme), and that the score is a practice score, not an official Cambridge result. One Arabic help box.
   For Stage 8 courses say the test is an end-of-Stage-8 test in Checkpoint style (the Checkpoint itself is at the end of Stage 9).
2. ONE "test" block: "timed": true, two sections "Paper 1" and "Paper 2" with the real minutes, "calc": false/true as SPEC says
   (science: calc as SPEC says; if SPEC is unsure for Paper 2, set calc true only if SPEC confirms, else omit the field), and
   "pdf": [{"label":"Question paper (PDF)","href":"pdf/<slug>-paper.pdf"},{"label":"Mark scheme (PDF)","href":"pdf/<slug>-mark-scheme.pdf"}].
   Each paper's marks must add up EXACTLY to the real total (Stage 6: 40 per paper; Stage 8: 50 per paper — see SPEC).
3. box exam "After the test" — how to review, and which lessons to revisit (use the real lesson titles from the plan file).

Content and style:
- Cover the whole curriculum across the two papers in proportion (every sub-strand appears at least once per test; number/biology
  etc. weighted as in a real paper). Mix easy → hard. Paper 1 maths = no calculator (numbers chosen so they can be done by hand);
  Paper 2 maths = calculator problems, real-life contexts, multi-step.
- Real Checkpoint style (SPEC section B): numbered questions with parts (a), (b)… sharing a "p" stem; 1–2 marks per part (Stage 8 may
  use up to 3 for a long calculation or explanation); "show your working" for 2-mark calculations — give part-mark guidance in "e"
  (e.g. "M1 for 36 ÷ 4 seen; A1 for 9"); tick/ring items as MCQ; tables, graphs and diagrams as SVG in "img" or the stem.
- Science: include at least one investigation question per paper (variables, fair test, table of results, graph reading, conclusion,
  improvement), plus diagrams to label (use lettered labels A, B, C in the SVG and ask "which letter…" as text/MCQ).
- About 60–75% auto-marked (num/text/mcq); the rest "open" with a real mark scheme in "ms" (what earns each mark; accept/do not accept).
- Every question ORIGINAL; do not reuse questions or diagrams from the lesson pages (glance at british/<course>/ to avoid repeats) or
  from the other practice tests in the same course (check british/<course>/*practice-test*.json if they exist; pick different contexts).
- Diagrams: follow the SVG rules in BRIEF.md exactly (correct, computed, font-size ≥ 16, render and look at every one).
- Validate (BRIEF rules), and also print per paper: number of questions, total marks (must equal the real total), auto-marked share,
  MCQ key distribution, and topic coverage. Re-solve every question; an answer-key error is the worst possible mistake.
- Final reply: those counts + doubts.
