# Quran course — content spec (for writers)

Course: «القرآن الكريم من الألف للياء: قراءة وتجويد وحفظ» by Mohamed Abdelkriem (write the name exactly so, no "Mr./أستاذ").
Audience: Egyptian parents who follow their child (age ~5–14) at home, and adult beginners. Riwayat Hafs 'an 'Asim, Madinah mushaf.
Language: very simple, clear Modern Standard Arabic (short sentences, everyday words, no heavy terminology without explaining it).
Tone: warm, encouraging, practical. Never mention AI or that the material was generated.

## ABSOLUTE accuracy rules for Quran text
- NEVER type Quran text from memory. Every Quranic word you use must be copied from the verified data:
  - /tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/quran/tajweed_candidates.json (examples per tajweed rule, with surah/ayah)
  - or the Uthmani text via Python:  import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/quran'); import qdata; qdata.ayah_text(surah, ayah)
- Every example is given as {"surah": n, "ayah": n, "word": "<exact word(s) copied from qdata.ayah_text>", "note": "<what to notice>"}.
  The page builder shows the verified ayah and highlights the word, so "word" must appear in that ayah (check it in Python:
  qdata.skel(word) in qdata.skel(qdata.ayah_text(s,a))).
- Tajweed rulings must follow the standard Hafs/Shatibiyyah teaching found in common Egyptian/Al-Azhar beginner books
  (e.g. تحفة الأطفال، المقدمة الجزرية، "أحكام التلاوة" المبسطة). Mention counts (حركات) correctly: طبيعي 2، متصل 4–5، منفصل 4–5 (ويجوز 2 قصرًا)، عارض للسكون 2/4/6، لازم 6، لين 2/4/6 عند الوقف، صلة صغرى 2، صلة كبرى 4–5، بدل 2، عوض 2. Letters: الإظهار الحلقي (ء هـ ع ح غ خ)، الإدغام (يرملون: بغنة ينمو، بغير غنة ل ر)، الإقلاب (ب)، الإخفاء (15 حرفًا)، القلقلة (قطب جد)، حروف الاستعلاء (خص ضغط قظ)، اللام الشمسية/القمرية (ابغ حجك وخف عقيمه = القمرية).
- When unsure about a ruling, leave it out rather than guess.

## Output files (JSON, UTF-8, validate with json.load)
Lesson files: <folder>/lesson1.json … lessonN.json:
{"n":1,"title":"…","goal":"one sentence: what the child will be able to do",
 "explain":["short paragraph", …],               // 3–6 short paragraphs
 "table":{"headers":[…],"rows":[[…]]},             // optional summary table (letters, counts…) — no Quran text inside except single letters
 "examples":[{"surah":…,"ayah":…,"word":"…","note":"…"}, …],   // 6–10 examples
 "common_mistakes":["…"],                         // what children usually get wrong and how to fix it
 "parent_tips":["…"],                             // how the parent checks it at home in 5 minutes
 "plan":[{"day":"اليوم 1","task":"…"}, … 7 days, day 7 = مراجعة خفيفة / راحة],
 "exercises":[{"title":"…","items":["…"],"answers":["…"]}],  // 3 exercises, answers 1-to-1; Quran words in items must also be verified
 "listen":["<resource name exactly as published> (video|audio)"]   // from RESOURCES.json once it exists; else leave []
}
