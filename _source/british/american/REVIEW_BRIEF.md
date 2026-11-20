# Reviewer brief — blind answer check (Nov 2026)

You are the independent checker for practice questions on an English-teacher's study website. Accuracy matters more
than speed: every published question must have exactly ONE defensible answer and a correct explanation.

Repo: /home/claude/abdelkriem-academy ; B = _source/british ; tools in B/_engine/. Read B/american/AGENT_BRIEF.md
(quality rules) and B/american/BRIEF.md (the teacher's punctuation rules) first.
Your working folder: /tmp/claude-0/review_<first file name>/ (create it; keep everything there).

For EACH file you are given:
1. Make the blind copy:  python3 B/_engine/blind.py make FILE WORKDIR
   Open ONLY WORKDIR/<name>.blind.txt (do NOT open the key or the source yet).
2. Answer every question yourself as a strong test-taker would. Write WORKDIR/<name>.answers.json as
   {"P1-1": "B", ...}. Also note any item where you think two choices could be defended, or none, or the passage
   has an error, in WORKDIR/<name>.notes.txt.
3. Compare:  python3 B/_engine/blind.py compare WORKDIR/<name>.key.json WORKDIR/<name>.answers.json
4. Now open the source file. For every mismatch and every item in your notes, decide honestly who is right.
   - If the key is wrong, or a wrong choice is also defensible, or the item is unclear: FIX THE SOURCE FILE with the
     smallest change that leaves exactly one defensible answer (usually rewrite the weak wrong choice or tighten the
     passage), and update that choice's reason / the "e" and "ce" texts so they stay true. Keep the file format exact.
   - If you were simply wrong, leave it.
   Also fix any factual error, typo, placeholder text, letter references inside reasons ("A is…"), or a reason that
   does not match its choice.
5. Re-validate: topic .txt files with `python3 B/_engine/check_practice.py FILE`; JSON tests with the checker in
   AGENT_BRIEF.md. Never change the number of questions, sets or sections.

Do not touch files you were not given, do not edit course.json/engine/build files, and do not use git.
Final reply (short): per file — agreement score before fixes, list of items changed (id + one-line why), anything
you were unsure about.
