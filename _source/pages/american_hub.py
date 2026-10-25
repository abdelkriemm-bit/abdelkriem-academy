# American Diploma hub (american.html): SAT, ACT and EST English courses.
_am = pagehead("Section 2", "American Diploma English: SAT · ACT · EST",
  "Complete free courses for the English parts of the Digital SAT, the ACT and the EST: every question type taught step by step, a quiz on every page, and full timed practice tests with explanations.") + f'''
<section class="block"><div class="wrap grid3">
{card("Digital SAT Reading and Writing","The whole RW section: all four content domains, every question type, every grammar rule tested, a vocabulary toolkit and three full adaptive-style practice tests (2 modules × 32 minutes).","digital-sat.html","SAT")}
{card("ACT English and Reading","The enhanced ACT: English (50 questions, 35 minutes) and Reading (36 questions, 40 minutes) — punctuation, grammar, style, organisation, reading strategy, and full timed tests.","act-english.html","ACT")}
{card("EST English (Literacy 1 and 2)","The Egyptian Scholastic Test explained, with a guide to each Literacy test, a map to the lessons you need and a full timed practice test.","est-exam.html","EST")}
</div></section>
<section class="block alt"><div class="wrap prose">
<h2>Which test should I take?</h2>
<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;background:#fff;font-size:.95rem;min-width:640px;vertical-align:top">
<thead><tr style="background:var(--navy);color:#fff"><th style="padding:10px;text-align:left">&nbsp;</th><th style="padding:10px;text-align:left">Digital SAT</th><th style="padding:10px;text-align:left">ACT</th><th style="padding:10px;text-align:left">EST I</th></tr></thead>
<tbody>
<tr><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee"><b>English parts</b></td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Reading and Writing: 54 questions, 64 minutes (2 modules)</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">English 50 q / 35 min + Reading 36 q / 40 min</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Literacy 1: 44 q / 35 min + Literacy 2: 52 q / 65 min*</td></tr>
<tr><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee"><b>Passages</b></td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Very short (25–150 words), one question each</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Long essays and passages, many questions each</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Passage-based</td></tr>
<tr><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee"><b>Adaptive?</b></td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Yes, by module</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">No</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">—</td></tr>
<tr><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee"><b>Wrong-answer penalty</b></td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">None</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">None</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">—</td></tr>
<tr><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee"><b>Good for</b></td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Students who like short texts and more time per question</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Fast readers who are comfortable with long passages</td><td style="vertical-align:top;padding:10px;border-top:1px solid #e3e6ee">Students applying inside Egypt who prefer the Ministry's test</td></tr>
</tbody></table></div>
<p style="font-size:.88rem">*EST figures are as published by schools; check the latest official EST candidate guide on est.moe.gov.eg before your test. Always check which tests your target universities accept.</p>
<div dir="rtl" lang="ar" style="background:#fff8e8;border-inline-start:4px solid var(--gold);padding:14px 18px;border-radius:10px;margin-top:18px">
<p><b>لولي الأمر:</b> المهارات اللي بتتقاس في الإنجليزي في الامتحانات التلاتة متشابهة جدًا: قراءة وفهم، وجرامر، وعلامات ترقيم، وأسلوب كتابة. ابدأ بكورس الـ SAT لأنه بيشرح كل قاعدة بالتفصيل، وبعدين لو ابنك هيمتحن ACT أو EST يدخل على الكورس بتاعه يتعود على شكل الامتحان. وقبل ما تختار، اسأل الجامعات اللي عايز تقدم فيها بتقبل أنهي امتحان.</p>
</div>
<h2>How to use these courses</h2>
<ol><li>Read the overview page of your test first.</li><li>Work through the lessons in order and do the quiz at the end of each page.</li><li>Take a full timed practice test, then review every explanation, not only the wrong ones.</li><li>Go back to the lessons for the skills where you lost the most marks, then take the next test.</li></ol>
<p style="font-size:.88rem">Abdelkriem Academy is independent and not affiliated with College Board, ACT or the Egyptian Ministry of Education. All lessons, passages and questions are original.</p>
</div></section>'''
page("american.html", "American Diploma English: SAT, ACT and EST — Abdelkriem Academy",
     "Free complete English courses for the Digital SAT Reading and Writing, ACT English and Reading, and the EST Literacy tests, with full timed practice tests.", _am, "american.html")
EXTRA_PAGES.append("american.html")
