# English in 90 Days — one web page per week + progress checks (runs inside build.py).
# Content comes from course/weekN.json, progress_check_N.json and answer_key.json (transcribed from the course book).
import json as _json, os as _os, html as _html

_CDIR = _os.path.join(_os.path.dirname(PAGES_DIR), "course")
def _load(name):
    p = _os.path.join(_CDIR, name)
    return _json.load(open(p, encoding="utf-8")) if _os.path.exists(p) else None

_KEY = _load("answer_key.json") or {}
_E = _html.escape

_WEEK_CSS = """<style>
.wk-nav{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:8px 0 0}
.wk-nav a{text-decoration:none;font-weight:600;color:var(--gold-2)}
.wk-sec{margin-bottom:34px}
.wk-sec h2{margin-bottom:12px}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}
.tbl table{border-collapse:collapse;width:100%;min-width:520px}
.tbl th{background:var(--navy);color:#fff;text-align:left;font-weight:600;padding:10px 14px;font-size:.92rem}
.tbl td{padding:10px 14px;border-top:1px solid var(--line);vertical-align:top}
.tbl tr:nth-child(even) td{background:var(--paper)}
.sets{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.set{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.set h3{font-size:1rem;margin:0 0 10px;color:var(--gold-2);font-family:Inter,sans-serif}
.set ul{list-style:none;margin:0;padding:0}
.set li{display:flex;justify-content:space-between;gap:10px;padding:7px 0;border-top:1px dashed var(--line)}
.set li:first-child{border-top:0}
.set .en{font-weight:600}
.ar,.set .ar{font-family:Cairo,sans-serif;direction:rtl;text-align:right;color:var(--muted)}
.hide-ar .set .ar,.hide-ar .sent .ar{visibility:hidden}
.toggle{background:var(--card);border:2px solid var(--navy);color:var(--navy);border-radius:999px;padding:8px 16px;font-weight:700;cursor:pointer;margin-bottom:14px}
.toggle:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.sents{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.sent{display:grid;grid-template-columns:34px 1fr 1fr;gap:12px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px}
.sent .n{font-weight:800;color:var(--gold-2)}
.gbox{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;display:grid;gap:14px}
.gbox .ar{background:#fbf1dc;border-radius:10px;padding:12px 14px;color:var(--ink)}
.ex{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin-bottom:12px}
.ex h3{font-size:1.05rem;margin:0 0 10px;font-family:Inter,sans-serif;color:var(--navy)}
.ex ol{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.ex details{margin-top:12px;border-top:1px dashed var(--line);padding-top:10px}
.ex summary{cursor:pointer;font-weight:700;color:var(--gold-2)}
.ex .ans{white-space:pre-line;margin-top:8px;color:var(--ink)}
.ws{background:var(--navy);color:#fff;border-radius:14px;padding:18px 20px;white-space:pre-line}
.wk-list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.wk-list a{display:block;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.wk-list a:hover{border-color:var(--gold)}
@media (max-width:640px){.sent{grid-template-columns:28px 1fr}.sent .ar{grid-column:2}}
</style>"""

_TOGGLE_JS = """<script>
document.querySelectorAll('[data-toggle-ar]').forEach(function(b){b.addEventListener('click',function(){
var box=document.getElementById(b.getAttribute('data-toggle-ar'));var on=box.classList.toggle('hide-ar');
b.textContent=on?'Show the Arabic':'Hide the Arabic (test yourself)';b.setAttribute('aria-pressed',on?'true':'false');});});
</script>"""

def _table(t):
    head = "".join(f"<th>{_E(h)}</th>" for h in t.get("headers", []))
    rows = "".join("<tr>" + "".join(f"<td>{_E(c)}</td>" for c in r) + "</tr>" for r in t.get("rows", []))
    return f'<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'

def _answers(week, title):
    wk = (_KEY.get("weeks") or {}).get(str(week)) or {}
    for k, v in wk.items():
        if k and (title.startswith(k) or k.split("—")[0].strip() in title):
            return v if isinstance(v, str) else "\n".join(map(str, v))
    return None

def _week_page(d, total_pages):
    n = d["week"]
    plan = _table({"headers": ["Day", "Learn", "Listen / Watch", "Practise"],
                   "rows": [[p.get("day",""), p.get("learn",""), p.get("listen",""), p.get("practise","")] for p in d.get("plan", [])]})
    sets = "".join(f'<div class="set"><h3>{_E(s["name"])}</h3><ul>' +
                   "".join(f'<li><span class="en" lang="en">{_E(w[0])}</span><span class="ar" lang="ar">{_E(w[1])}</span></li>' for w in s["words"]) +
                   "</ul></div>" for s in d.get("word_sets", []))
    sents = "".join(f'<li class="sent"><span class="n">{i}</span><span lang="en">{_E(s[0])}</span><span class="ar" lang="ar">{_E(s[1])}</span></li>'
                    for i, s in enumerate(d.get("sentences", []), 1))
    g = d.get("grammar") or {}
    gparts = []
    if g.get("intro_en"): gparts.append(f'<p>{_E(g["intro_en"])}</p>')
    if g.get("intro_ar"): gparts.append(f'<p class="ar" lang="ar">{_E(g["intro_ar"])}</p>')
    gparts += [_table(t) for t in g.get("tables", [])]
    gparts += [f'<p>{_E(x)}</p>' for x in g.get("notes", [])]
    exs = ""
    for ex in d.get("exercises", []):
        items = "".join(f"<li dir=\"auto\">{_E(i)}</li>" for i in ex.get("items", []))
        a = _answers(n, ex.get("title", ""))
        ans = f'<details><summary>Show the answers</summary><div class="ans">{_E(a)}</div></details>' if a else ""
        exs += f'<div class="ex"><h3>{_E(ex.get("title",""))}</h3><ol>{items}</ol>{ans}</div>'
    ws = f'<div class="wk-sec"><h2>Write &amp; Speak</h2><div class="ws">{_E(d["write_speak"])}</div></div>' if d.get("write_speak") else ""
    other = "".join(f'<p class="note">{_E(o)}</p>' for o in d.get("other", []))
    prev_link = f'<a href="english-week-{n-1}.html">← Week {n-1}</a>' if n > 1 else '<a href="english-in-90-days.html">← Course overview</a>'
    next_link = f'<a href="english-week-{n+1}.html">Week {n+1} →</a>' if n < total_pages else '<a href="english-in-90-days.html">Course overview →</a>'
    if n in (4, 8, 12):
        next_link = f'<a href="english-progress-check-{n//4}.html">Progress Check {n//4} →</a>'
    body = _WEEK_CSS + pagehead(f"English Course: From Zero · Week {n} of 12", _E(d["title"]), _E(d.get("grammar_title",""))) + f'''
<section class="block"><div class="wrap">
<div class="wk-sec"><h2>This week's plan</h2>{plan}<p class="note">30 minutes a day: review, learn, listen, practise, speak. Day 7 is a free day.</p></div>
<div class="wk-sec" id="words"><h2>30 words to learn</h2><button class="toggle" type="button" data-toggle-ar="words" aria-pressed="false">Hide the Arabic (test yourself)</button><div class="sets">{sets}</div></div>
<div class="wk-sec" id="sents"><h2>10 sentences to memorise</h2><button class="toggle" type="button" data-toggle-ar="sents" aria-pressed="false">Hide the Arabic (test yourself)</button><ol class="sents">{sents}</ol></div>
<div class="wk-sec"><h2>{_E(d.get("grammar_title","Grammar"))}</h2><div class="gbox">{"".join(gparts)}</div></div>
<div class="wk-sec"><h2>Exercises</h2>{exs}<p class="note">Do each exercise in pencil first, then open the answers to check.</p></div>
{ws}{other}
<nav class="wk-nav" aria-label="Weeks">{prev_link}{next_link}</nav>
</div></section>''' + _TOGGLE_JS
    page(f"english-week-{n}.html", f"Week {n}: {d['title']} — English Course: From Zero | Abdelkriem Academy",
         f"Free beginner English, week {n}: {d['title']}. 30 words with Arabic, 10 key sentences, {d.get('grammar_title','grammar')}, exercises with answers.",
         body, "improve-english.html")
    EXTRA_PAGES.append(f"english-week-{n}.html")

def _check_page(n, d):
    secs = ""
    for s in d.get("sections", []):
        items = "".join(f"<li>{_E(i)}</li>" for i in s.get("items", []))
        ins = f'<p>{_E(s["instructions"])}</p>' if s.get("instructions") else ""
        secs += f'<div class="ex"><h3>{_E(s.get("title",""))}</h3>{ins}<ol>{items}</ol></div>'
    a = (_KEY.get("progress_checks") or {}).get(str(n))
    if a:
        a = a if isinstance(a, str) else "\n".join(map(str, a))
        secs += f'<div class="ex"><details><summary>Show the answers</summary><div class="ans">{_E(a)}</div></details></div>'
    nxt = f'<a href="english-week-{n*4+1}.html">Week {n*4+1} →</a>' if n < 3 else '<a href="english-in-90-days.html">Course overview →</a>'
    body = _WEEK_CSS + pagehead(f"English Course: From Zero · Weeks {n*4-3}–{n*4}", _E(d.get("title", f"Progress Check {n}")), _E(d.get("subtitle", "20 marks · no help · 20 minutes"))) + f'''
<section class="block"><div class="wrap">
<p class="note">Score 16/20 or more to move on. If not, repeat the sentences of these weeks for 3 days and try again.</p>
{secs}
<nav class="wk-nav"><a href="english-week-{n*4}.html">← Week {n*4}</a>{nxt}</nav>
</div></section>'''
    page(f"english-progress-check-{n}.html", f"Progress Check {n} — English Course: From Zero | Abdelkriem Academy",
         f"Progress Check {n} for the free English Course: From Zero: test weeks {n*4-3}–{n*4} in 20 minutes.", body, "improve-english.html")
    EXTRA_PAGES.append(f"english-progress-check-{n}.html")

_weeks_data = [d for d in (_load(f"week{i}.json") for i in range(1, 13)) if d]
for _d in _weeks_data:
    _week_page(_d, 12)
for _n in (1, 2, 3):
    _pc = _load(f"progress_check_{_n}.json")
    if _pc:
        _check_page(_n, _pc)
