# English Course Levels 2+ — overview page, one page per week, progress checks (runs inside build.py after english_weeks.py).
# Content: course/levelN/week1..12.json, progress_check_1..3.json, meta.json. Answers live inside each exercise ("answers").
# Only levels listed in PUBLISHED_LEVELS are put on the site. To publish a level, add its number here and rebuild.
# (Set the environment variable PREVIEW_ALL_LEVELS=1 to build every level that has content, for checking before publishing.)
import json as _j2, os as _o2, urllib.parse as _up

PUBLISHED_LEVELS = [2, 3, 4, 5]
_LVL_ROOT = _o2.path.join(_o2.path.dirname(PAGES_DIR), "course")
if _o2.environ.get("PREVIEW_ALL_LEVELS"):
    PUBLISHED_LEVELS = [n for n in range(2, 10) if _o2.path.exists(_o2.path.join(_LVL_ROOT, f"level{n}", "meta.json"))]

def _lj(L, name):
    return _j2.load(open(_o2.path.join(_LVL_ROOT, f"level{L}", name), encoding="utf-8"))

def _srch(t):
    return "https://www.google.com/search?q=" + _up.quote(t.replace("“", "").replace("”", ""))

def _listen(s):
    if "free day" in s.lower():
        return _E(s)
    return "<br>+ ".join(f'<a href="{_srch(p.strip())}" target="_blank" rel="noopener">{_E(p.strip())}</a>' for p in __import__("re").split(r"(?<=\)) \+ ", s))

def _lv_week(L, meta, d):
    n = d["week"]
    pre = f"english-level-{L}"
    plan = _table({"headers": ["Day", "Learn", "Listen / Watch", "Practise"], "rows": []}).replace("<tbody></tbody>",
        "<tbody>" + "".join(f'<tr><td>{_E(p["day"])}</td><td>{_E(p["learn"])}</td><td>{_listen(p["listen"])}</td><td>{_E(p["practise"])}</td></tr>' for p in d["plan"]) + "</tbody>")
    sets = "".join(f'<div class="set"><h3>{_E(s["name"])}</h3><ul>' +
                   "".join(f'<li><span class="en" lang="en">{_E(w[0])}</span><span class="ar" lang="ar">{_E(w[1])}</span></li>' for w in s["words"]) +
                   "</ul></div>" for s in d["word_sets"])
    sents = "".join(f'<li class="sent"><span class="n">{i}</span><span lang="en">{_E(s[0])}</span><span class="ar" lang="ar">{_E(s[1])}</span></li>'
                    for i, s in enumerate(d["sentences"], 1))
    g = d.get("grammar") or {}
    gp = []
    if g.get("intro_en"): gp += [f"<p>{_E(x)}</p>" for x in g["intro_en"].split("\n")]
    if g.get("intro_ar"): gp.append(f'<p class="ar" lang="ar">{_E(g["intro_ar"])}</p>')
    gp += [_table(t) for t in g.get("tables", [])]
    gp += [f"<p>{_E(x)}</p>" for x in g.get("notes", [])]
    exs = ""
    for ex in d["exercises"]:
        items = "".join(f'<li dir="auto">{_E(i)}</li>' for i in ex["items"])
        a = "\n".join(ex.get("answers", []))
        ans = f'<details><summary>Show the answers</summary><div class="ans">{_E(a)}</div></details>' if a else ""
        exs += f'<div class="ex"><h3>{_E(ex["title"])}</h3><ol>{items}</ol>{ans}</div>'
    ws = f'<div class="wk-sec"><h2>Write &amp; Speak · اكتب واتكلم</h2><p class="arhint" dir="rtl" lang="ar">اكتب الموضوع في الكشكول بنفسك، وبص على المثال لو احتجت، وبعدين اقراه بصوت عالي أو سجّل نفسك.</p><div class="ws">{_E(d["write_speak"])}</div></div>' if d.get("write_speak") else ""
    other = "".join(f'<p class="note">{_E(o)}</p>' for o in d.get("other", []))
    prev_link = f'<a href="{pre}-week-{n-1}.html">← Week {n-1}</a>' if n > 1 else f'<a href="{pre}.html">← Level {L} overview</a>'
    if n in (5, 9):
        prev_link = f'<a href="{pre}-check-{(n-1)//4}.html">← Progress Check {(n-1)//4}</a>'
    next_link = f'<a href="{pre}-check-{n//4}.html">Progress Check {n//4} →</a>' if n in (4, 8, 12) else f'<a href="{pre}-week-{n+1}.html">Week {n+1} →</a>'
    kick = f'English Course · Level {L} ({_E(meta["cefr"])}) · Week {n} of 12'
    body = AR_HINT_CSS + _WEEK_CSS + pagehead(kick, _E(d["title"]), _E(d.get("grammar_title", ""))) + f'''
<section class="block"><div class="wrap">
<div class="wk-sec"><h2>This week's plan · خطة الأسبوع</h2><p class="arhint" dir="rtl" lang="ar">كل يوم 30 دقيقة: نفّذ الصف بتاع اليوم. <b>Learn</b> = احفظ الكلمات والجمل المكتوبة، <b>Listen / Watch</b> = اسمع أو اتفرج على الدرس (دوس على اسمه)، <b>Practise</b> = حل التمرين. اليوم السابع راحة.</p>{plan}<p class="note">30 minutes a day: review, learn, listen, practise, speak. Day 7 is a free day. Tap a resource to find it.</p></div>
<div class="wk-sec" id="words"><h2>30 words to learn · كلمات الأسبوع</h2><p class="arhint" dir="rtl" lang="ar">احفظ مجموعة واحدة (6 كلمات) كل يوم. قول كل كلمة بصوت عالي واكتبها في الكشكول. دوس الزرار عشان تخفي العربي وتختبر نفسك.</p><button class="toggle" type="button" data-toggle-ar="words" aria-pressed="false">Hide the Arabic (test yourself)</button><div class="sets">{sets}</div></div>
<div class="wk-sec" id="sents"><h2>10 sentences to memorise · جمل تحفظها</h2><p class="arhint" dir="rtl" lang="ar">احفظ جملتين كل يوم، وقول كل جملة بصوت عالي 5 مرات لحد ما تطلع منك لوحدها.</p><button class="toggle" type="button" data-toggle-ar="sents" aria-pressed="false">Hide the Arabic (test yourself)</button><ol class="sents">{sents}</ol></div>
<div class="wk-sec"><h2>{_E(d.get("grammar_title", "Grammar"))}</h2><p class="arhint" dir="rtl" lang="ar">اقرا الشرح بالعربي الأول، وبعدين بص على الجدول والأمثلة. لو مش فاهم، اسمع درس الجرامر اللي في خطة الأسبوع.</p><div class="gbox">{"".join(gp)}</div></div>
<div class="wk-sec"><h2>Exercises · تمارين</h2><p class="arhint" dir="rtl" lang="ar">حل كل تمرين في يومه بالقلم الرصاص، وبعدين دوس «Show the answers» وصحّح لنفسك. اكتب أخطاءك في الكشكول وراجعها في اليوم السادس.</p>{exs}<p class="note">Do each exercise in pencil first, then open the answers to check.</p></div>
{ws}{other}
<nav class="wk-nav" aria-label="Weeks">{prev_link}{next_link}</nav>
</div></section>''' + _TOGGLE_JS
    page(f"{pre}-week-{n}.html", f"Level {L} Week {n}: {d['title']} — English Course | Abdelkriem Academy",
         f"Free English Level {L} ({meta['cefr']}), week {n}: {d['title']}. 30 words with Arabic, 10 key sentences, {d.get('grammar_title','grammar')}, exercises with answers.",
         body, "improve-english.html")
    EXTRA_PAGES.append(f"{pre}-week-{n}.html")

def _lv_check(L, meta, n, c):
    pre = f"english-level-{L}"
    secs = ""
    for s in c["sections"]:
        items = "".join(f'<li dir="auto">{_E(i)}</li>' for i in s.get("items", []))
        ins = f'<p>{_E(s["instructions"])}</p>' if s.get("instructions") and not s["title"].startswith("D") else ""
        a = "\n".join(s.get("answers", []))
        ans = f'<details><summary>Show the answers</summary><div class="ans">{_E(a)}</div></details>' if a else ""
        secs += f'<div class="ex"><h3>{_E(s["title"])}</h3>{ins}<ol>{items}</ol>{ans}</div>'
    nxt = f'<a href="{pre}-week-{n*4+1}.html">Week {n*4+1} →</a>' if n < 3 else (f'<a href="english-level-{L+1}.html">Level {L+1} →</a>' if (L + 1) in PUBLISHED_LEVELS else f'<a href="{pre}.html">Level {L} overview →</a>')
    body = AR_HINT_CSS + _WEEK_CSS + pagehead(f"English Course · Level {L} ({_E(meta['cefr'])}) · Weeks {n*4-3}–{n*4}", _E(c["title"]), _E(c.get("subtitle", ""))) + f'''
<section class="block"><div class="wrap">
<p class="note">{_E(c.get("score", "Score 16/20 or more to move on."))}</p>
{secs}
<nav class="wk-nav"><a href="{pre}-week-{n*4}.html">← Week {n*4}</a>{nxt}</nav>
</div></section>'''
    page(f"{pre}-check-{n}.html", f"Level {L} {c['title']} — English Course | Abdelkriem Academy",
         f"English Level {L} progress check: test weeks {n*4-3}–{n*4} in 20 minutes, with answers.", body, "improve-english.html")
    EXTRA_PAGES.append(f"{pre}-check-{n}.html")

def _lv_overview(L, meta, weeks):
    pre = f"english-level-{L}"
    pdf = f"files/English-Course-Level-{L}.pdf"
    pdf_name = f"English Course Level {L} - {meta['name_ar']}.pdf"
    wl = ""
    for w in weeks:
        n = w["week"]
        wl += f'<li class="wk"><span class="wn">Week {n}</span><div><h3><a href="{pre}-week-{n}.html">{_E(w["title"])}</a></h3><p>{_E(w["grammar_title"])}</p></div></li>'
        if n % 4 == 0:
            wl += f'<li class="chk"><a href="{pre}-check-{n//4}.html">✓ Progress Check {n//4} · Weeks {n-3}–{n}</a> — score 16/20 to move on</li>'
    can = "".join(f"<li>{_E(x)}</li>" for x in meta["can_do"])
    prev = "english-in-90-days.html" if L == 2 else f"english-level-{L-1}.html"
    title_html = f"English Course · Level {L}: {_E(meta['name_en'])}<span class='ar-title' lang='ar' dir='rtl'>{_E(meta['name_ar'])}</span>"
    body = pagehead(f"Free English course · Level {L} · {_E(meta['cefr'])} · 12 weeks · 30 minutes a day", title_html, _E(meta["tagline_en"])) + f'''
<section class="block"><div class="wrap split">
<div>
<ul class="stats dark"><li><b>360</b><span>words</span></li><li><b>120</b><span>key sentences</span></li><li><b>12</b><span>grammar points</span></li><li><b>48</b><span>exercises + answers</span></li></ul>
<div class="ctas"><a class="btn" href="{pre}-week-1.html">Start Week 1</a><a class="btn ghost" href="#plan">See the 12-week plan</a></div>
<p class="ar" dir="rtl" lang="ar">{_E(meta["intro_ar"])}</p>
<p class="note">New here? Start with <a href="english-in-90-days.html">Level 1: From Zero</a>. Finished the level before? Continue from <a href="{prev}">the previous level</a>.</p>
</div>
<div class="part"><h3>After this level you can…</h3><ul class="ticks">{can}</ul></div>
</div></section>
'''+AR_GUIDE.replace('block alt','block')+f'''
<section id="plan" class="block alt"><div class="wrap">
<h2>The 12-week plan</h2><p class="sub">Each week has 30 words, 10 sentences to memorise, one grammar point, daily listening and exercises with answers.</p>
<ol class="weeks">{wl}</ol>
<div class="ctas"><a class="btn" href="{pre}-week-1.html">Start Week 1</a></div>
</div></section>'''
    page(f"{pre}.html", f"English Course Level {L}: {meta['name_en']} ({meta['cefr']}) — {meta['name_ar']} | Abdelkriem Academy",
         f"Free English course Level {L} ({meta['cefr']}): 12 weeks, 30 minutes a day, 360 words, 120 sentences, grammar, exercises with answers and a daily listening plan, with Arabic.",
         body, "improve-english.html")
    EXTRA_PAGES.append(f"{pre}.html")

for _L in PUBLISHED_LEVELS:
    _meta = _lj(_L, "meta.json")
    _ws = [_lj(_L, f"week{i}.json") for i in range(1, 13)]
    _cs = [_lj(_L, f"progress_check_{i}.json") for i in (1, 2, 3)]
    _lv_overview(_L, _meta, _ws)
    for _w in _ws:
        _lv_week(_L, _meta, _w)
    for _i, _c in enumerate(_cs, 1):
        _lv_check(_L, _meta, _i, _c)

# Show all published levels at the bottom of the Level 1 page and the Improve Your English page.
if PUBLISHED_LEVELS:
    _cards = card("Level 1 · From Zero (A1)", "Start English from zero: 12 weeks, 30 minutes a day.", "english-in-90-days.html", "طوّر الإنجليزي من الصفر")
    for _L in PUBLISHED_LEVELS:
        _m = _lj(_L, "meta.json")
        _cards += card(f"Level {_L} · {_E(_m['name_en'])} ({_E(_m['cefr'])})", _E(_m["tagline_en"]), f"english-level-{_L}.html", _E(_m["name_ar"]))
    _strip = f'<section class="block alt"><div class="wrap"><h2>All levels of the English Course</h2><p class="sub">Finish a level, then move to the next one.</p><div class="grid3">{_cards}</div></div></section>'
    for _f in ("english-in-90-days.html", "improve-english.html"):
        _p = _o2.path.join(OUT, _f)
        if _o2.path.exists(_p):
            _h = open(_p, encoding="utf-8").read()
            open(_p, "w", encoding="utf-8").write(_h.replace("</main>", _strip + "</main>", 1))


# Stop browsers from auto-translating the Arabic explanations into English on the English course pages.
import glob as _eg
for _ep in _eg.glob(f"{OUT}/english-*.html") + [f"{OUT}/improve-english.html"]:
    _eh = open(_ep, encoding="utf-8").read()
    if 'name="google" content="notranslate"' not in _eh:
        open(_ep, "w", encoding="utf-8").write(_eh.replace("<head>", '<head>\n<meta name="google" content="notranslate">', 1))
