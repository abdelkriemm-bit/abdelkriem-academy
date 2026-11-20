"""Arabic (right-to-left) version of the practice/test engine.

The builder calls arabic(js) / arabic_css(css) for courses with "rtl": true in course.json, so test.js stays the single
source and English pages are unchanged. Every replacement must match: a missing match raises, so an engine update that
renames a string is noticed at build time instead of leaving English on an Arabic page.
"""

JS = [
    ("'ABCD'", "'أبجد'"),
    ("+' questions'", "+' سؤال'"),
    ("' marks'", "' درجة'"),
    ("+' min'", "+' دقيقة'"),
    ("' · Question '", "' · سؤال '"),
    ("' of '", "' من '"),
    ("+' mark'+(mk(Q)>1?'s':'')+", "+' درجة'+(mk(Q)>1?'':'')+"),
    ("'Start'", "'ابدأ'"),
    ("'Start '", "'ابدأ '"),
    ("'<p class=\"pt-prev\">Your best so far: <b>'", "'<p class=\"pt-prev\">أحسن نتيجة ليك: <b>'"),
    ("'%</b> · last try '", "'%</b> · آخر محاولة '"),
    ("✓ Passed", "✓ نجحت"),
    ("'<p class=\"pt-how\">Choose an answer to see straight away whether it is right — and why every choice is right or wrong.</p>'",
     "'<p class=\"pt-how\">اختار إجابة وهتعرف فورًا هي صح ولا غلط، وليه كل اختيار صح أو غلط.</p>'"),
    ("'✓ Correct!'", "'✓ إجابة صحيحة!'"),
    ("'✗ Not quite. The answer is '", "'✗ مش مظبوطة. الإجابة الصحيحة '"),
    ("'Write your answer here'", "'اكتب إجابتك هنا'"),
    ("'Type a number'", "'اكتب رقم'"),
    ("'Type your answer'", "'اكتب إجابتك'"),
    ("'Numbers only. Fractions like 3/4 are accepted.'", "'أرقام بس.'"),
    ("'You will mark this answer yourself against the mark scheme at the end.'",
     "'في الآخر هتقارن إجابتك بنموذج الإجابة وتدي نفسك الدرجة بنفسك.'"),
    ("'← Back'", "'→ السابق'"),
    ("'Marked for review'", "'متعلّم للمراجعة'"),
    ("'Mark for review'", "'علّم للمراجعة'"),
    ("'Next →'", "'التالي ←'"),
    ("'Finish this section'", "'إنهاء الجزء ده'"),
    ("'Finish test'", "'إنهاء الامتحان'"),
    ("'Finish'", "'إنهاء'"),
    ("'You have '", "'فاضل '"),
    ("' unanswered question'", "' سؤال من غير إجابة'"),
    ("'. Press the button again to finish anyway.'", "'. دوس الزرار تاني لو عايز تنهي برضه.'"),
    ("' finished.</b><p>Next: '", "' خلص.</b><p>اللي بعده: '"),
    ("'Other'", "'أخرى'"),
    ("'<div class=\"all\"><small>Total'", "'<div class=\"all\"><small>المجموع'"),
    ("'<div class=\"pt-res\"><h3>Your result</h3><div class=\"pt-scores\">'", "'<div class=\"pt-res\"><h3>نتيجتك</h3><div class=\"pt-scores\">'"),
    ("'<p class=\"pt-note\">This is a practice score, not an official Cambridge, College Board or ACT score.</p>'",
     "'<p class=\"pt-note\">دي نتيجة تدريب على الموقع، مش درجة رسمية من الوزارة.</p>'"),
    ("<h4>By skill</h4>", "<h4>حسب المهارة</h4>"),
    ("<th>Skill</th>", "<th>المهارة</th>"),
    ("'Marks'", "'الدرجات'"),
    ("'Correct'", "'الصح'"),
    ("<h4>Review every question</h4>", "<h4>راجع كل سؤال</h4>"),
    ("' ✗ your answer'", "' ✗ إجابتك'"),
    ("'<p class=\"pt-yours\">Your answer: '", "'<p class=\"pt-yours\">إجابتك: '"),
    ("'<i>none</i>'", "'<i>مفيش</i>'"),
    ("'<p class=\"pt-right\">Correct answer: <b>'", "'<p class=\"pt-right\">الإجابة الصحيحة: <b>'"),
    ("<b>Mark scheme:</b>", "<b>نموذج الإجابة:</b>"),
    ("Your mark: ", "درجتك: "),
    ("'<p class=\"pt-nb\">Not answered.</p>'", "'<p class=\"pt-nb\">متجاوبش.</p>'"),
    ("'Why'", "'ليه'"),
    ("'Solution'", "'الإجابة النموذجية'"),
    ("'<p class=\"pt-warn2\">Some answers are written answers. Scroll down, compare each with the mark scheme and tap the mark you earned — your total updates automatically.</p>'",
     "'<p class=\"pt-warn2\">فيه أسئلة مقالي. انزل تحت، قارن إجابتك بنموذج الإجابة، ودوس على الدرجة اللي تستحقها، والمجموع هيتحدث لوحده.</p>'"),
    ("<b>Study these again:</b>", "<b>ذاكر دول تاني:</b>"),
    ("'Retry the '", "'أعد حل الـ '"),
    ("' I got wrong'", "' سؤال اللي غلطت فيهم'"),
    ("'Try again'", "'حاول تاني'"),
]

CSS_EXTRA = """
.ptest{direction:rtl;text-align:right;font-family:Cairo,Inter,sans-serif}
.ptest .pt-c{text-align:right}
.ptest .pt-ch .pt-c>span{margin-left:.6rem;margin-right:0}
.ptest .pt-ce,.ptest .pt-rev,.ptest ul{padding-right:1.3rem;padding-left:0}
.ptest .pt-pass{direction:rtl;text-align:right;line-height:2}
.ptest .pt-qt{line-height:1.9}
"""


def arabic(js):
    for a, b in JS:
        if a not in js:
            raise ValueError(f"ar_engine: engine string not found: {a[:70]}")
        js = js.replace(a, b)
    return js


def arabic_css(css):
    return css + CSS_EXTRA
