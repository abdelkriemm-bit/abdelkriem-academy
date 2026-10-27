# English Course: placement test, Level 1 final test (pass -> certificate + Level 2), and the "new" strip on the course pages.
# Runs inside build.py after english_weeks_levels.py. Data: course/exams/*.json · engine: course/eng_exam.js + eng_exam.css
import json as _jx, os as _ox
_XD = _ox.path.join(_ox.path.dirname(PAGES_DIR), "course")
_xcss = open(_ox.path.join(_XD, "eng_exam.css"), encoding="utf-8").read()
_xjs = open(_ox.path.join(_XD, "eng_exam.js"), encoding="utf-8").read()

_LVS = [{"en": "From Zero", "cefr": "A1", "ar": "الليفل الأول: من الصفر", "href": "english-in-90-days.html"}]
for _n in range(2, 6):
    _m = _jx.load(open(_ox.path.join(_XD, f"level{_n}", "meta.json"), encoding="utf-8"))
    _LVS.append({"en": _m["name_en"], "cefr": _m["cefr"], "ar": _m["name_ar"], "href": f"english-level-{_n}.html"})

def _xpage(fname, title, desc, head_html, howto_ar, data):
    data = dict(data); data["levels"] = _LVS
    blob = _jx.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    body = head_html + f'''<style>{_xcss}</style>
<section class="block"><div class="wrap" style="max-width:900px">
<div class="ex-howto" lang="ar">{howto_ar}</div>
<div id="ex-app"></div><div id="ex-result" hidden></div>
</div></section>
<script type="application/json" id="ex-data">{blob}</script><script>{_xjs}</script>'''
    page(fname, title, desc, body, "improve-english.html")
    EXTRA_PAGES.append(fname)

_pl = {"mode": "placement", "need": 6, "forms": [_jx.load(open(_ox.path.join(_XD, "exams", f), encoding="utf-8")) for f in ("placement.json", "placement_b.json")]}
_xpage("english-placement-test.html",
       "Free English Placement Test — امتحان تحديد المستوى | Abdelkriem Academy",
       "Free English placement test: 40 questions, about 20 minutes. Find your level (A1–B2) and start the free English course at the right level.",
       pagehead("Free English Course · Placement test · 40 questions · about 20 minutes",
                "English Placement Test<span class='ar-title' lang='ar' dir='rtl'>امتحان تحديد المستوى</span>",
                "Find your level in 20 minutes, then start the free course at the level that fits you."),
       '<h2>إزاي تمتحن؟</h2><ol><li>40 سؤال، من السهل للصعب. جاوب لوحدك من غير ترجمة ومن غير ما تسأل حد، عشان النتيجة تبقى حقيقية.</li>'
       '<li>لو مش عارف الإجابة سيبها فاضية، ما تخمّنش.</li><li>لو امتحنت تاني هتلاقي أسئلة مختلفة.</li><li>في الآخر دوس «خلّصت، وريني النتيجة»، والموقع هيقولك تبدأ من أنهي ليفل، ويوريك الإجابات الصح.</li></ol>',
       _pl)

_fn = {"mode": "final", "pass": 28, "forms": [_jx.load(open(_ox.path.join(_XD, "exams", f), encoding="utf-8")) for f in ("level1_final.json", "level1_final_b.json")]}
_xpage("english-level-1-final-test.html",
       "Level 1 Final Test and Certificate — امتحان نهاية الليفل الأول | Abdelkriem Academy",
       "English Course Level 1 final test: 40 questions on all 12 weeks. Score 28/40 to pass, get your certificate and move on to Level 2.",
       pagehead("English Course · Level 1 · Final test · 40 questions · about 25 minutes",
                "Level 1 Final Test<span class='ar-title' lang='ar' dir='rtl'>امتحان نهاية الليفل الأول + الشهادة</span>",
                "Finished the 12 weeks? Score 28 out of 40 to pass, download your certificate and move on to Level 2."),
       '<h2>قبل ما تبدأ</h2><ol><li>الامتحان على الـ 12 أسبوع كلهم: جرامر، كلمات، إنجليزي الحياة اليومية، وقطعة قراءة صغيرة.</li>'
       '<li>عشان تنجح لازم تجيب <b>28 من 40</b> على الأقل.</li><li>لو نجحت: اكتب اسمك وخد شهادتك، وكمّل على الليفل التاني. لو ما نجحتش: الموقع هيقولك تراجع أنهي أسابيع، وتقدر تمتحن تاني في أي وقت بأسئلة جديدة.</li><li>الشهادة دي شهادة تحفيزية مجانية من Abdelkriem Academy، بتثبت إنك نجحت في امتحان الليفل على موقعنا. هي مش شهادة معتمدة من أي جهة رسمية.</li></ol>',
       _fn)

# "New" strip on the English hub, Level 1 page and home page
_STRIP = f'''<style>{_xcss}</style><section class="block"><div class="wrap"><div class="new-strip">
<div><span class="pill">NEW · جديد</span><h2>Test your level, study for free, get a certificate</h2>
<p>Take the placement test → start at your level → pass the end-of-level test → get your certificate and move to the next level.</p>
<p class="ar" lang="ar">امتحن تحديد مستوى ← ابدأ الليفل بتاعك ببلاش ← امتحن في آخر الليفل ← لو نجحت خد شهادتك وكمّل على الليفل اللي بعده.</p></div>
<div class="ctas"><a class="btn" href="english-placement-test.html">Placement test · حدّد مستواك</a><a class="btn ghost" href="english-level-1-final-test.html">Level 1 final test</a></div>
</div></div></section>'''
for _f, _anchor in (("english-in-90-days.html", "</section>"), ("index.html", "</section>")):
    _p = _ox.path.join(OUT, _f)
    if _ox.path.exists(_p):
        _h = open(_p, encoding="utf-8").read()
        if "new-strip" not in _h:
            _i = _h.find("<main>"); _j = _h.find(_anchor, _i) + len(_anchor)
            open(_p, "w", encoding="utf-8").write(_h[:_j] + _STRIP + _h[_j:])

# Level 1 plan: add the final test after Progress Check 3
_p = _ox.path.join(OUT, "english-in-90-days.html")
_h = open(_p, encoding="utf-8").read()
_k = _h.find('english-progress-check-3.html')
if _k > 0 and "english-level-1-final-test.html\">🎓" not in _h:
    _e = _h.find("</li>", _k) + 5
    _h = _h[:_e] + '<li class="chk"><a href="english-level-1-final-test.html">🎓 Final Test · Weeks 1–12</a> — score 28/40 to get your certificate and move to Level 2</li>' + _h[_e:]
    open(_p, "w", encoding="utf-8").write(_h)
