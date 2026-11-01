# English course navigation — runs inside build.py after the English pages are written (and before zz_social.py).
# It can also run on its own:  python3 _source/pages/zy_course_nav.py <site folder>
# 1) Level pages: a short 3-step path + one box per week / progress check / final test; the long study guide is folded away.
# 2) Week pages: Day 1–7 boxes; each day shows exactly what to do today (words, sentences, listening, exercise, speaking).
# Idempotent: pages already processed carry the marker <!--cnav-->.
import re as _cr, os as _co, glob as _cg, html as _ch

try:
    _CN_OUT = OUT  # noqa: F821  (inside build.py)
except NameError:
    import sys as _cs
    _CN_OUT = _cs.argv[1]

_CN_MARK = "<!--cnav-->"
_CN_CSS = """<style>
.cn-path{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:4px 0 26px}
.cn-step{background:var(--card);border:2px solid var(--line);border-radius:18px;padding:16px 18px}
.cn-step .k{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--navy);color:#fff;font-weight:800;margin-bottom:8px}
.cn-step>b{display:block;font-size:1.05rem;color:var(--navy)}
.cn-step p{margin:.35rem 0 0;font-size:.95rem}
.cn-step .ar{display:block;font-family:Cairo,sans-serif;direction:rtl;text-align:right;color:var(--muted);margin-top:6px;font-size:.92rem}
.cn-step a{font-weight:700}
.cn-go{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 22px}
.cn-tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px;margin:10px 0 8px}
.cn-tile{position:relative;display:flex;flex-direction:column;justify-content:center;min-height:118px;background:var(--card);border:2px solid var(--line);border-radius:18px;padding:14px 16px;text-decoration:none;color:var(--navy);box-shadow:var(--shadow);transition:transform .15s,border-color .15s}
.cn-tile:hover{transform:translateY(-2px);border-color:var(--gold)}
.cn-tile .n{font-size:.78rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:#7f5c1c}
.cn-tile b{font-size:1.08rem;line-height:1.25;margin-top:4px}
.cn-tile small{color:var(--muted);margin-top:5px;font-size:.84rem;line-height:1.35}
.cn-tile.chk{background:#eef7ee;border-color:#bfe0c6}.cn-tile.chk .n{color:#2f7a43}
.cn-tile.fin{background:#fbf1dc;border-color:var(--gold)}
.cn-tile.done::after{content:"✓";position:absolute;top:10px;right:12px;width:26px;height:26px;border-radius:50%;background:#2f7a43;color:#fff;display:grid;place-items:center;font-weight:800}
.cn-tile.next{border-color:var(--navy);box-shadow:0 0 0 3px rgba(15,27,51,.12)}
details.cn-howto{margin:0}
details.cn-howto>summary{list-style:none;cursor:pointer}
details.cn-howto>summary::-webkit-details-marker{display:none}
details.cn-howto>summary .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-top:18px;padding-bottom:18px;font-weight:700;color:var(--navy)}
details.cn-howto>summary .wrap span:last-child{font-family:Cairo,sans-serif}
details.cn-howto>summary .plus{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;border:2px solid var(--navy)}
details.cn-howto[open]>summary .plus{transform:rotate(45deg)}
.cn-days{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin:6px 0 16px}
.cn-day{position:relative;border:2px solid var(--line);background:var(--card);border-radius:14px;padding:12px 6px;text-align:center;cursor:pointer;font-weight:800;color:var(--navy);font-size:1rem}
.cn-day small{display:block;font-weight:600;color:var(--muted);font-size:.72rem;margin-top:3px}
.cn-day.on{border-color:var(--navy);background:var(--navy);color:#fff}.cn-day.on small{color:#c9d1e3}
.cn-day.done::after{content:"✓";position:absolute;top:-8px;right:-6px;width:22px;height:22px;border-radius:50%;background:#2f7a43;color:#fff;display:grid;place-items:center;font-size:.8rem}
.cn-panel{background:var(--card);border:2px solid var(--line);border-radius:18px;padding:16px 18px}
.cn-panel h3{margin:0 0 10px;font-family:Inter,sans-serif;font-size:1.15rem;color:var(--navy)}
.cn-todo{list-style:none;margin:0;padding:0;display:grid;gap:10px;counter-reset:t}
.cn-todo>li{counter-increment:t;display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:start;border-top:1px dashed var(--line);padding-top:10px}
.cn-todo>li:first-child{border-top:0;padding-top:0}
.cn-todo>li::before{content:counter(t);display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#fbf1dc;color:#7f5c1c;font-weight:800}
.cn-todo b.t{display:block;color:var(--navy)}
.cn-todo .ar{display:block;font-family:Cairo,sans-serif;direction:rtl;text-align:right;color:var(--muted);font-size:.9rem}
.cn-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.cn-chips span{background:var(--paper);border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:.9rem}
.cn-chips span i{font-style:normal;font-family:Cairo,sans-serif;color:var(--muted);margin-inline-start:6px}
.cn-sl{margin:6px 0 0;padding:0;list-style:none;display:grid;gap:4px}
.cn-sl li{background:var(--paper);border-radius:10px;padding:6px 10px}
.cn-sl li i{display:block;font-style:normal;font-family:Cairo,sans-serif;direction:rtl;text-align:right;color:var(--muted);font-size:.9rem}
.cn-done{margin-top:14px;background:#2f7a43;color:#fff;border:0;border-radius:999px;padding:10px 18px;font-weight:800;cursor:pointer}
.cn-done.is{background:var(--card);color:#2f7a43;border:2px solid #2f7a43}
details.cn-table{margin-top:12px}details.cn-table summary{cursor:pointer;font-weight:700;color:var(--gold-2)}
@media (max-width:640px){.cn-days{grid-template-columns:repeat(4,1fr)}}
</style>"""

_CN_STORE = """function cnGet(k){try{return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return {}}}
function cnSet(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}"""


def _cn_text(s):
    return _ch.unescape(_cr.sub(r"<[^>]+>", "", s)).strip()


def _cn_level(path):
    h = open(path, encoding="utf-8").read()
    if _CN_MARK in h or 'class="weeks"' not in h:
        return False
    fname = _co.path.basename(path)
    i0 = h.index("<main>") + len("<main>")
    i1 = h.index("</main>")
    main = h[i0:i1]
    ph_end = main.index("</section>", main.index('class="phead"')) + len("</section>")
    head, rest = main[:ph_end], main[ph_end:]
    # pull the week list out of the plan section, and drop that section
    plan = _cr.search(r'<section id="plan".*?</section>', rest, _cr.S)
    weeks_html = _cr.search(r'<ol class="weeks">(.*?)</ol>', plan.group(0), _cr.S).group(1)
    rest = rest.replace(plan.group(0), "")
    tiles, first = [], None
    for li in _cr.findall(r"<li class=\"(?:wk|chk)\">.*?</li>", weeks_html, _cr.S):
        if 'class="wk"' in li:
            n = _cn_text(_cr.search(r'<span class="wn">(.*?)</span>', li).group(1))
            a = _cr.search(r'<a href="([^"]+)">(.*?)</a>', li)
            sub = _cr.search(r"<p>(.*?)</p>", li, _cr.S)
            first = first or a.group(1)
            tiles.append(f'<a class="cn-tile" data-wk="{a.group(1)}" href="{a.group(1)}"><span class="n">{n}</span><b>{a.group(2)}</b>'
                         + (f"<small>{sub.group(1)}</small>" if sub else "") + "</a>")
        else:
            a = _cr.search(r'<a href="([^"]+)">(.*?)</a>(.*)</li>', li, _cr.S)
            label = _cn_text(a.group(2)).lstrip("✓🎓 ").strip()
            nm, _, wk = label.partition("·")
            cls = "fin" if "final" in label.lower() or "final" in a.group(1) else "chk"
            tiles.append(f'<a class="cn-tile {cls}" href="{a.group(1)}"><span class="n">{_ch.escape(nm.strip())}</span><b>{_ch.escape(wk.strip() or nm.strip())}</b><small>{_ch.escape(_cn_text(a.group(3)).lstrip("— ").strip())}</small></a>')
    level1 = fname == "english-in-90-days.html"
    pdf = _cr.search(r'<a class="btn ghost" href="(files/[^"]+\.pdf)"[^>]*>', rest)
    pdf_btn = f'<a class="btn ghost" href="{pdf.group(1)}" download>Download the PDF · حمّل الكورس PDF</a>' if pdf else ""
    step3 = ("Every 4 weeks take the <b>Progress Check</b>. After Week 12, take the <b>Level 1 final test</b> and get your certificate.",
             "كل 4 أسابيع امتحن الـ Progress Check، وفي الآخر امتحن امتحان الليفل وخد شهادتك.") if level1 else \
            ("Every 4 weeks take the <b>Progress Check</b> (score 16/20 to move on). Then go to the next level.",
             "كل 4 أسابيع امتحن الـ Progress Check، ولما تخلص الـ 12 أسبوع روح على الليفل اللي بعده.")
    path_html = f'''<div class="cn-path">
<div class="cn-step"><span class="k">1</span><b>Start at your level</b><p>Not sure? Take the free <a href="english-placement-test.html">placement test</a> (20 minutes).</p><span class="ar" dir="rtl">مش متأكد من مستواك؟ امتحن امتحان تحديد المستوى الأول.</span></div>
<div class="cn-step"><span class="k">2</span><b>One week at a time</b><p>Open your week, pick <b>today</b> (Day 1–7) and do the 5 short steps. 30 minutes a day.</p><span class="ar" dir="rtl">افتح الأسبوع، اختار يوم النهارده، واعمل الخطوات بالترتيب.</span></div>
<div class="cn-step"><span class="k">3</span><b>Check your progress</b><p>{step3[0]}</p><span class="ar" dir="rtl">{step3[1]}</span></div>
</div>'''
    weeks = (f'<section class="block">{_CN_CSS}<div class="wrap">{path_html}'
             f'<div class="cn-go"><a class="btn" id="cn-cont" href="{first}">Start Week 1 →</a>{pdf_btn}</div>'
             f'<h2>Your 12 weeks <span lang="ar" dir="rtl" style="font-family:Cairo,sans-serif">· الأسابيع</span></h2>'
             f'<div class="cn-tiles">{"".join(tiles)}</div></div></section>')
    howto = ('<details class="cn-howto"><summary><div class="wrap"><span>How to study this course (read once)</span>'
             '<span>إزاي تذاكر الكورس؟ <span class="plus">+</span></span></div></summary>' + rest + "</details>")
    js = ("<script>(function(){" + _CN_STORE + """
var t=document.querySelectorAll('.cn-tile[data-wk]'),next=null;
t.forEach(function(a){var d=cnGet('cnav:'+a.dataset.wk),n=0;for(var k in d)if(d[k])n++;if(n>=6)a.classList.add('done');else if(!next)next=a;});
if(next&&document.querySelector('.cn-tile.done')){next.classList.add('next');var b=document.getElementById('cn-cont');if(b){b.href=next.getAttribute('href');b.textContent='Continue: '+next.querySelector('.n').textContent+' →';}}
})();</script>""")
    h = h[:i0] + _CN_MARK + head + weeks + howto + js + h[i1:]
    open(path, "w", encoding="utf-8").write(h)
    return True


def _cn_week(path):
    h = open(path, encoding="utf-8").read()
    if _CN_MARK in h or "This week&#x27;s plan" not in h and "This week's plan" not in h:
        return False
    fname = _co.path.basename(path)
    # anchors
    n = [0]
    def _exid(m):
        n[0] += 1
        return m.group(0)[:-1] + f' id="ex{n[0]}">'
    h = _cr.sub(r'<div class="ex"(?: data-ex="\d+")?>', _exid, h)
    h = h.replace('<div class="wk-sec"><h2>Grammar', '<div class="wk-sec" id="grammar"><h2>Grammar', 1)
    h = h.replace('<div class="wk-sec"><h2>Exercises', '<div class="wk-sec" id="exercises"><h2>Exercises', 1)
    h = h.replace('<div class="wk-sec"><h2>Write &amp; Speak', '<div class="wk-sec" id="write"><h2>Write &amp; Speak', 1)
    # data
    sets = []
    for s in _cr.findall(r'<div class="set"><h3>(.*?)</h3><ul>(.*?)</ul></div>', h, _cr.S):
        name = _cn_text(s[0]).split("·", 1)[-1].strip()
        words = _cr.findall(r'<span class="en" lang="en">(.*?)</span><span class="ar" lang="ar">(.*?)</span>', s[1])
        sets.append((name, words))
    sents = _cr.findall(r'<li class="sent"><span class="n">(\d+)</span><span lang="en">(.*?)</span><span class="ar" lang="ar">(.*?)</span></li>', h)
    sec = _cr.search(r'<div class="wk-sec"><h2>This week(?:&#x27;|\')s plan.*?</table></div>(?:<p class="note">.*?</p>)?</div>', h, _cr.S)
    if not sec:
        return False
    table = _cr.search(r"<table>.*?</table>", sec.group(0), _cr.S).group(0)
    rows = _cr.findall(r"<tr><td>(Day \d+)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", table, _cr.S)
    gtitle = _cr.search(r'<div class="wk-sec" id="grammar"><h2>(.*?)</h2>', h)
    days, panels = [], []
    for di, (day, learn, listen, prac) in enumerate(rows, 1):
        steps = []
        lt = _cn_text(learn)
        m = _cr.match(r"Words:\s*(.*?)\s*·\s*Sentences\s*(\d+)\s*[–-]\s*(\d+)", lt)
        if m:
            nm, a, b = m.group(1), int(m.group(2)), int(m.group(3))
            ws = next((w for s_, w in sets if s_.lower() == nm.lower()), None) or (sets[di - 1][1] if di <= len(sets) else None)
            chips = "".join(f"<span>{e}<i>{ar}</i></span>" for e, ar in (ws or []))
            steps.append(f'<li><div><b class="t">Learn 6 new words · {_ch.escape(nm)}</b><span class="ar" dir="rtl">قول كل كلمة بصوت عالي واكتبها في الكشكول.</span><div class="cn-chips">{chips}</div></div></li>')
            sl = "".join(f"<li>{e}<i>{ar}</i></li>" for k, e, ar in sents if a <= int(k) <= b)
            steps.append(f'<li><div><b class="t">Memorise sentences {a}–{b}</b><span class="ar" dir="rtl">قول كل جملة 5 مرات لحد ما تطلع منك لوحدها.</span><ul class="cn-sl">{sl}</ul></div></li>')
            if di == 1 and gtitle:
                steps.append(f'<li><div><b class="t">Read this week\'s grammar</b><a href="#grammar">{gtitle.group(1)}</a></div></li>')
        elif day != "Day 7":
            steps.append(f'<li><div><b class="t">{learn}</b><span class="ar" dir="rtl">راجع كل كلمات وجمل الأسبوع: <a href="#words">الكلمات</a> · <a href="#sents">الجمل</a></span></div></li>')
        steps.append(f'<li><div><b class="t">{"Enjoy a story or a podcast" if day == "Day 7" else "Listen / Watch"}</b>{listen}</div></li>')
        pt = _cn_text(prac)
        me = _cr.match(r"Exercise (\d+)", pt)
        if me:
            steps.append(f'<li><div><b class="t">Practise</b><a href="#ex{me.group(1)}">Do {pt} →</a> <span class="ar" dir="rtl">حل التمرين وبعدين صحّح لنفسك.</span></div></li>')
        elif pt.startswith("Write"):
            steps.append('<li><div><b class="t">Write &amp; Speak</b><a href="#write">Open the writing task →</a> <span class="ar" dir="rtl">اكتب في الكشكول وبعدين اقرا بصوت عالي.</span></div></li>')
        elif pt.startswith("Redo"):
            steps.append('<li><div><b class="t">Redo your mistakes</b><a href="#exercises">Go to the exercises →</a> <span class="ar" dir="rtl">حل تاني الأسئلة اللي غلطت فيها.</span></div></li>')
        if day != "Day 7":
            steps.append('<li><div><b class="t">Speak</b>Say 3 sentences about your day with today\'s words. <span class="ar" dir="rtl">قول 3 جمل عن يومك بكلمات النهارده.</span></div></li>')
        sub = "Free day" if day == "Day 7" else ("Review" if pt.startswith("Redo") else "30 min")
        days.append(f'<button type="button" class="cn-day" data-d="{di}">{day}<small>{sub}</small></button>')
        panels.append(f'<div class="cn-panel" data-d="{di}" hidden><h3>{day} · {"Free day ☺" if day == "Day 7" else "do these steps in order"}</h3><ol class="cn-todo">{"".join(steps)}</ol>'
                      f'<button type="button" class="cn-done" data-d="{di}">✓ I finished {day}</button></div>')
    block = (f'{_CN_CSS}<div class="wk-sec" id="today"><h2>What to do today · تعمل إيه النهارده؟</h2>'
             f'<p class="arhint" dir="rtl" lang="ar">اختار اليوم اللي إنت فيه، واعمل الخطوات بالترتيب. ولما تخلص دوس على الزرار الأخضر.</p>'
             f'<div class="cn-days">{"".join(days)}</div>{"".join(panels)}'
             f'<details class="cn-table"><summary>See the whole week in one table</summary>{table}</details></div>')
    js = ("<script>(function(){" + _CN_STORE + f"""
var K='cnav:{fname}',S=cnGet(K),B=document.querySelectorAll('.cn-day'),P=document.querySelectorAll('.cn-panel');
function paint(){{B.forEach(function(b){{b.classList.toggle('done',!!S[b.dataset.d])}});document.querySelectorAll('.cn-done').forEach(function(x){{var on=!!S[x.dataset.d];x.classList.toggle('is',on);x.textContent=on?'✓ Done — tap to undo':'✓ I finished Day '+x.dataset.d}})}}
function show(d){{B.forEach(function(b){{b.classList.toggle('on',b.dataset.d==d)}});P.forEach(function(p){{p.hidden=p.dataset.d!=d}})}}
B.forEach(function(b){{b.onclick=function(){{show(b.dataset.d)}}}});
document.querySelectorAll('.cn-done').forEach(function(x){{x.onclick=function(){{S[x.dataset.d]=!S[x.dataset.d];cnSet(K,S);paint();if(S[x.dataset.d]&&+x.dataset.d<7){{show(+x.dataset.d+1);document.getElementById('today').scrollIntoView({{behavior:'smooth'}})}}}}}});
var first=1;for(var i=1;i<=B.length;i++){{if(!S[i]){{first=i;break}}}}paint();show(first);
}})();</script>""")
    h = h.replace(sec.group(0), block + js, 1)
    h = h.replace("<main>", "<main>" + _CN_MARK, 1)
    open(path, "w", encoding="utf-8").write(h)
    return True


_cn_l = _cn_w = 0
for _p in sorted(_cg.glob(_co.path.join(_CN_OUT, "english-*.html"))):
    _b = _co.path.basename(_p)
    if _b == "english-in-90-days.html" or _cr.fullmatch(r"english-level-\d\.html", _b):
        _cn_l += _cn_level(_p)
    elif _cr.fullmatch(r"english-(?:level-\d-)?week-\d+\.html", _b):
        _cn_w += _cn_week(_p)
print(f"[course-nav] level pages {_cn_l}, week pages {_cn_w}")
