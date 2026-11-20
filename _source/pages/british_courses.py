# British courses (Oxford ESL 9280, Cambridge IGCSE 0510, Checkpoint 8, Checkpoint 6) — display-only study pages.
# Content: british/<course>/course.json (hub page + ordered sections of page slugs) and british/<course>/<slug>.json
# (one page each, block format described in british/FORMAT.md). Each course hub REPLACES the old placeholder page
# (year-10-oxford.html, year-9-0510.html, checkpoint-8.html, checkpoint-6.html). Courses without course.json are skipped.
import json as _bj, os as _bo, re as _bre, html as _bh

_BR_ROOT = _bo.path.join(_bo.path.dirname(PAGES_DIR), "british")
def _beng(rtl=False):
    # inline engine assets; Arabic labels + RTL layout for rtl courses (see british/_engine/ar_engine.py)
    _e = _bo.path.join(_BR_ROOT, "_engine")
    css = open(_bo.path.join(_e, "test.css"), encoding="utf-8").read()
    js = open(_bo.path.join(_e, "test.js"), encoding="utf-8").read()
    if rtl:
        import importlib.util as _u
        _sp = _u.spec_from_file_location("ar_engine", _bo.path.join(_e, "ar_engine.py")); _m = _u.module_from_spec(_sp); _sp.loader.exec_module(_m)
        css, js = _m.arabic_css(css), _m.arabic(js)
    return "<style>" + css + "</style><script>" + js + "</script>"
_BR_COURSES = [c for c in _bo.environ.get("BRITISH_COURSES", "oxford,0510,cp8,cp6,bac,parents,sat,act,est,cp6m,cp6s,cp8m,cp8s,ebhist,ebar").split(",") if c]

_BR_CSS = """<style>
.bc{max-width:860px;margin:0 auto;overflow-wrap:break-word}
.bc li,.bc p,.bc td,.bc th,.bc summary{overflow-wrap:anywhere}
.bc h2{margin:2.2rem 0 .7rem;font-size:1.45rem}
.bc p{line-height:1.7}
.bc ul,.bc ol{line-height:1.7;padding-left:1.4rem}
.bc li{margin:.25rem 0}
.bc .tw{overflow-x:auto;margin:1rem 0}
.bc table{border-collapse:collapse;width:100%;font-size:.95rem}
.bc th,.bc td{border:1px solid #d9d4c7;padding:.55rem .7rem;text-align:start;vertical-align:top}
.bc th{background:#f3efe4}
.bc .bx{border-radius:12px;padding:1rem 1.2rem;margin:1.2rem 0;border-inline-start:5px solid}
.bc .bx b.t{display:block;margin-bottom:.35rem}
.bc .bx ul{margin:.3rem 0 0}
.bc .bx.tip{background:#eef7ee;border-color:#3f8f4f}
.bc .bx.warning{background:#fdf0ec;border-color:#c4553a}
.bc .bx.exam{background:#eef2fb;border-color:#3a5fc4}
.bc .bx.ar{background:#fbf6e8;border-color:#c49a3a;border-left:0;border-right:5px solid #c49a3a;font-family:Cairo,sans-serif;direction:rtl;text-align:right}
.bc .bx.ar ul{padding-left:0;padding-right:1.4rem}
.bc .model{border:1px solid #d9d4c7;border-radius:14px;margin:1.5rem 0;overflow:hidden;background:#fff}
.bc .model .mh{background:#1f3a5f;color:#fff;padding:.8rem 1.2rem}
.bc .model .mh>b{display:block;font-size:1.05rem}
.bc .model .mh span{font-size:.85rem;opacity:.85}
.bc .model .task{background:#f6f3ea;padding:.9rem 1.2rem;font-style:italic;border-bottom:1px solid #e6e0d0}
.bc .model .mt{padding:1rem 1.2rem}
.bc .model .mt p{margin:.0 0 .9rem;text-align:left}
.bc .model .task{text-align:left}
.bc .model .mn{background:#eef7ee;padding:.9rem 1.2rem;border-top:1px solid #d7e8d7}
.bc .model .mn>b{display:block;margin-bottom:.3rem}
.bc .qa{margin:1rem 0;padding:0;list-style:none;counter-reset:q}
.bc .qa>li{counter-increment:q;border:1px solid #e3ddcd;border-radius:10px;padding:.8rem 1rem;margin:.6rem 0;background:#fff}
.bc .qa>li>p:first-child::before{content:counter(q) ". ";font-weight:700}
.bc details summary{cursor:pointer;color:#1f5fa8;font-weight:600;margin-top:.3rem}
.bc details .a{background:#f3efe4;border-radius:8px;padding:.6rem .8rem;margin-top:.4rem;white-space:pre-line}
.bc .vocab td:first-child{font-weight:600;white-space:nowrap}
.bc .phr{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin:1rem 0}
.bc .phr div{border:1px solid #e3ddcd;border-radius:10px;padding:.8rem 1rem;background:#fff}
.bc .phr h3{font-size:1rem;margin:0 0 .4rem}
.bc .phr ul{margin:0}
.bc .crumb{font-size:.9rem;margin:0 0 1rem}
.bc .crumb a{color:#1f5fa8}
.bc .pnav{display:flex;justify-content:space-between;gap:1rem;margin:2.5rem 0 1rem;flex-wrap:wrap}
.bc .pnav a{border:1px solid #d9d4c7;border-radius:10px;padding:.7rem 1rem;text-decoration:none;max-width:48%}
.bc .pnav a small{display:block;opacity:.7;font-size:.8rem}
.bc .toc{margin:2rem 0;border:1px solid #e3ddcd;border-radius:12px;padding:.8rem 1.1rem;background:#faf8f2}
.bc .toc li.on{font-weight:700}
.bsec{margin:2rem 0;scroll-margin-top:80px}
.stiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:.6rem 0 1rem}
.stile{display:flex;flex-direction:column;justify-content:center;min-height:110px;background:#fff;border:2px solid #e6e0d4;border-radius:18px;padding:18px 20px;text-decoration:none;color:#0f1b33;box-shadow:0 10px 30px rgba(15,27,51,.06);transition:transform .15s,border-color .15s}
.stile:hover{transform:translateY(-2px);border-color:#d4a24c}.stile.on{border-color:#d4a24c;background:#fbf1dc}
.stile b{font-size:1.15rem;line-height:1.3}.stile span{color:#7f5c1c;font-weight:700;font-size:.9rem;margin-top:6px}
.pickh{margin:1.6rem 0 .2rem}.blist .ln{display:block;color:#7f5c1c;font-weight:700;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.2rem}
.blist a{transition:border-color .15s}.blist a:hover{border-color:#d4a24c}
.bsec h2{margin-bottom:.3rem}
.bsec>p{margin-top:0;opacity:.85}
.bc .blist,.blist{list-style:none;padding:0;margin:1rem 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.8rem}
.blist a{display:block;height:100%;border:1px solid #d9d4c7;border-radius:12px;padding:.9rem 1rem;text-decoration:none;background:#fff}
.blist a b{display:block;margin-bottom:.25rem}
.blist a span{font-size:.9rem;opacity:.8;line-height:1.5}
.bc[dir=rtl] ul,.bc[dir=rtl] ol{padding-left:1.3rem;padding-right:1.4rem}
.bc[dir=rtl]{font-family:Cairo,Inter,sans-serif}
.bc[dir=rtl] .bx.ar{border-right:0;border-inline-start:5px solid #c49a3a}
.bc .exs{list-style:none;padding:0!important;margin:1rem 0}
.bc .exs li{border:1px solid #e3ddcd;border-radius:10px;padding:.7rem 1rem;margin:.5rem 0;background:#fff}
.bc .exs .en{display:block;direction:ltr;text-align:left;font-family:Inter,sans-serif;font-weight:600;color:#1f3a5f}
.bc .exs .exar{display:block;margin-top:.25rem;color:#4a4a4a}
.bc .en-p{direction:ltr;text-align:left;font-family:Inter,sans-serif}
.blist .bgrp{grid-column:1/-1;margin:.9rem 0 -.1rem}
.blist .bgrp h3{margin:0;font-size:1.05rem;color:#7f5c1c;text-transform:uppercase;letter-spacing:.05em}
.blist.compact{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
.blist.compact a{display:flex;flex-direction:column;justify-content:center;min-height:84px;border:2px solid #e6e0d4;border-radius:16px}
.blist.compact a b{font-size:1.05rem;line-height:1.3;margin:0}
@media (max-width:600px){.bc .pnav a{max-width:100%;flex:1 1 100%}}
</style>"""

def _bE(s):
    s = _bh.escape(str(s))
    s = _bre.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = _bre.sub(r"\^\{(.+?)\}", r"<sup>\1</sup>", s)
    s = _bre.sub(r"_\{(.+?)\}", r"<sub>\1</sub>", s)
    s = _bre.sub(r"(https?://[^\s<]+[^\s<.,)])", r'<a href="\1" target="_blank" rel="noopener nofollow" dir="ltr">\1</a>', s)
    s = _bre.sub(r"\(((?:sat|act|est)-[a-z0-9-]+)\.html\)", r'(<a href="\1.html">open lesson</a>)', s)
    return s

def _bMix(s):
    # a cell mixing English and Arabic: keep English order (ltr) and isolate each Arabic run so it reads correctly
    h = _bE(s)
    if _bre.search(r"[\u0600-\u06FF]", str(s)) and _bre.search(r"[A-Za-z]", str(s)):
        h = _bre.sub(r"([\u0600-\u06FF][\u0600-\u06FF\s/()،]*[\u0600-\u06FF)])", r'<bdi dir="rtl" lang="ar">\1</bdi>', h)
        return f'<td dir="ltr">{h}</td>'
    return f'<td dir="auto">{h}</td>'

def _bAr(s):
    return f'<span dir="rtl" lang="ar">{_bE(s)}</span>'

def _bblock(b):
    t = b.get("type")
    if t == "h2":
        return f"<h2>{_bE(b['text'])}</h2>"
    if t == "p":
        return f'<p dir="auto">{_bE(b["text"])}</p>'
    if t == "list":
        tag = "ol" if b.get("ordered") else "ul"
        return f"<{tag}>" + "".join(f'<li dir="auto">{_bE(i)}</li>' for i in b["items"]) + f"</{tag}>"
    if t == "photo":
        src = str(b.get("src", ""))
        if not _bre.match(r"^images/[a-z0-9/_.-]+\.(webp|jpg|jpeg|png)$", src):
            return ""
        w, h = b.get("w"), b.get("h")
        wh = f' width="{int(w)}" height="{int(h)}"' if w and h else ""
        cap = _bE(b.get("caption", ""))
        cr = f'<small class="credit">{_bE(b["credit"])}</small>' if b.get("credit") else ""
        return f'<figure class="photo"><img src="{src}" alt="{_bh.escape(b.get("alt", ""))}" loading="lazy"{wh}><figcaption>{cap}{cr}</figcaption></figure>'
    if t == "svg":
        g = str(b.get("svg", ""))
        if not g.lstrip().lower().startswith("<svg") or "<script" in g.lower() or _bre.search(r"\son\w+=", g):
            return ""
        cap = f'<figcaption>{_bE(b["caption"])}</figcaption>' if b.get("caption") else ""
        return f'<figure class="dia">{g}{cap}</figure>'
    if t == "table":
        h = "".join(f"<th>{_bE(x)}</th>" for x in b.get("headers", []))
        r = "".join("<tr>" + "".join(f'<td dir="auto">{_bE(c)}</td>' for c in row) + "</tr>" for row in b.get("rows", []))
        return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
    if t == "box":
        st = b.get("style", "tip")
        ar = st == "ar"
        attrs = ' dir="rtl" lang="ar" translate="no"' if ar else ""
        title = f'<b class="t">{_bE(b["title"])}</b>' if b.get("title") else ""
        inner = ""
        if b.get("text"):
            inner += f"<p>{_bE(b['text'])}</p>"
        if b.get("items"):
            inner += "<ul>" + "".join(f"<li>{_bE(i)}</li>" for i in b["items"]) + "</ul>"
        return f'<div class="bx {st}{" notranslate" if ar else ""}"{attrs}>{title}{inner}</div>'
    if t == "model":
        meta = []
        if b.get("word_count"): meta.append(f"{b['word_count']} words")
        if b.get("marks"): meta.append(_bE(b["marks"]))
        task = f'<div class="task" dir="ltr" lang="en"><b>Task:</b> {_bE(b["task"])}</div>' if b.get("task") else ""
        text = "".join(f'<p dir="auto">{_bE(p).replace(chr(10), "<br>")}</p>' for p in b.get("text", []))
        notes = ""
        if b.get("notes"):
            notes = '<div class="mn"><b>' + _BR_STATE.get("why", "Why this gets the marks") + '</b><ul>' + "".join(f'<li dir="{_BR_STATE.get("ndir","auto")}">{_bE(n)}</li>' for n in b["notes"]) + "</ul></div>"
        return f'<div class="model"><div class="mh" dir="auto"><b>{_bE(b.get("title","Model answer"))}</b><span dir="auto">{" · ".join(meta)}</span></div>{task}<div class="mt" dir="ltr" lang="en">{text}</div>{notes}</div>'
    if t == "qa":
        return '<ol class="qa">' + "".join(
            f'<li><p dir="auto">{_bE(i["q"])}</p><details><summary>Show answer</summary><div class="a" dir="auto">{_bE(i["a"])}</div></details></li>'
            for i in b["items"]) + "</ol>"
    if t == "vocab":
        return '<div class="tw"><table class="vocab"><thead><tr><th>Word / phrase</th><th>Meaning / use</th></tr></thead><tbody>' + "".join(
            f'<tr><td>{_bE(w[0])}</td>{_bMix(w[1])}</tr>' for w in b["items"]) + "</tbody></table></div>"
    if t == "phrases":
        return '<div class="phr">' + "".join(
            f'<div><h3>{_bE(g["title"])}</h3><ul>' + "".join(f"<li>{_bE(i)}</li>" for i in g["items"]) + "</ul></div>"
            for g in b["groups"]) + "</div>"
    if t == "ex":
        return '<ul class="exs">' + "".join(
            f'<li><span class="en" lang="en">{_bE(i["en"])}</span>' + (f'<span class="exar" dir="rtl" lang="ar">{_bE(i["ar"])}</span>' if i.get("ar") else "") + "</li>"
            for i in b["items"]) + "</ul>"
    if t == "en":
        return "".join(f'<p class="en-p" lang="en">{_bE(x)}</p>' for x in b["text"])
    if t == "test":
        _BR_STATE["has_test"] = True
        data = _bj.dumps(b, ensure_ascii=False).replace("</", "<\\/")
        n = sum(len(x["questions"]) for x in b["sections"])
        return f'<div class="ptest"><script type="application/json">{data}</script><noscript><p>{_bE(b["title"])} · {n} questions. Turn on JavaScript to take this practice test.</p></noscript></div>'
    raise ValueError(f"unknown block type {t!r}")

def _bref(course, s):
    # "@act/act-commas" = a lesson that lives in another course (tile links to it, it is not rebuilt here)
    if s.startswith("@"):
        c, sl = s[1:].split("/", 1)
        return _bo.path.join(_BR_ROOT, c, sl + ".json")
    return _bo.path.join(_BR_ROOT, course, s + ".json")
def _bhref(s):
    return (s.split("/", 1)[1] if s.startswith("@") else s) + ".html"
def _bload(course, name):
    return _bj.load(open(_bo.path.join(_BR_ROOT, course, name), encoding="utf-8"))

_BR_BUILT = {}
_BR_STATE = {}
import importlib.util as _bil
_bspec = _bil.spec_from_file_location("practice_dsl", _bo.path.join(_BR_ROOT, "_engine", "practice_dsl.py"))
_BDSL = _bil.module_from_spec(_bspec); _bspec.loader.exec_module(_BDSL)
def _bpractice(course, slug):
    # topic practice sets: british/<course>/practice/<slug>.txt (shared lessons "@act/x" read from their own course)
    if slug.startswith("@"):
        course, slug = slug[1:].split("/", 1)
    fp = _bo.path.join(_BR_ROOT, course, "practice", slug + ".txt")
    if not _bo.path.exists(fp):
        return None
    return _BDSL.parse(open(fp, encoding="utf-8").read(), slug)
_BR_PCSS = """<style>
.ptabs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:1rem 0}
.ptab{font:inherit;text-align:left;border:2px solid #e6e0d4;border-radius:14px;padding:.7rem .9rem;background:#fff;cursor:pointer;display:flex;flex-direction:column;gap:.15rem;color:#0f1b33}
.ptab b{font-size:1.05rem}.ptab small{color:#7f5c1c;font-weight:700}.ptab em{font-style:normal;font-size:.85rem;opacity:.8}
.ptab.on{border-color:#d4a24c;background:#fbf1dc}.ptab.pass{border-color:#2e7d32}.ptab.pass em{color:#1b5e20;font-weight:700;opacity:1}
.pmast{border-radius:12px;padding:.8rem 1rem;background:#eef2fb;margin:1rem 0;font-weight:600}.pmast .bar{height:10px;border-radius:6px;background:#dbe3f3;margin-top:.5rem;overflow:hidden}.pmast .bar i{display:block;height:100%;background:#2e7d32;width:0}
.pcta{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.8rem;border:2px solid #d4a24c;background:#fbf1dc;border-radius:14px;padding:1rem 1.2rem;margin:1.6rem 0}
.pcta b{font-size:1.1rem}.pcta p{margin:.2rem 0 0}.pp{display:block;font-size:.8rem;font-weight:700;color:#1b5e20;margin-top:.3rem}
.studyflow{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:1rem 0}.studyflow div{border:1px solid #e3ddcd;border-radius:12px;padding:.7rem .9rem;background:#fff}.studyflow b{display:block;color:#7f5c1c}
</style>"""
_BR_PJS = """<script>(function(){function sc(k){try{return JSON.parse(localStorage.getItem('aa-score:'+k)||'null')}catch(e){return null}}
document.querySelectorAll('[data-pk]').forEach(function(x){var k=x.dataset.pk,n=+x.dataset.n,p=0,t=0;for(var i=1;i<=n;i++){var o=sc(k+'-p'+i);if(o){t++;if(o.best>=80)p++}}
if(t)x.textContent=p===n?'✓ Topic mastered':'Practice: '+p+' / '+n+' sets passed'});
var tabs=document.querySelectorAll('.ptab'),pan=document.querySelectorAll('.ppanel');if(!tabs.length)return;
function upd(){var p=0;tabs.forEach(function(t){var o=sc(t.dataset.k),e=t.querySelector('em');if(o){e.textContent='Best: '+o.best+'%'+(o.best>=80?' ✓':'');t.classList.toggle('pass',o.best>=80);if(o.best>=80)p++}});
var m=document.querySelector('.pmast');if(m){m.querySelector('span').textContent=p===tabs.length?'✓ You have mastered this topic!':p+' of '+tabs.length+' practice sets passed (80% or more)';m.querySelector('i').style.width=(p*100/tabs.length)+'%'}}
function show(i){tabs.forEach(function(t,j){t.classList.toggle('on',i===j)});pan.forEach(function(x,j){x.hidden=i!==j});try{history.replaceState(null,'','#practice-'+(i+1))}catch(e){}}
tabs.forEach(function(t,i){t.onclick=function(){show(i);pan[i].scrollIntoView({behavior:'smooth',block:'start'})}});
var h=+(location.hash.match(/practice-(\\d+)/)||[])[1];show(h&&h<=tabs.length?h-1:0);upd();document.addEventListener('pt-done',upd)})();</script>"""
_BR_PJS_AR = (_BR_PJS.replace("'✓ Topic mastered':'Practice: '+p+' / '+n+' sets passed'", "'✓ اتقنت الدرس':'التدريبات: عدّيت '+p+' من '+n")
    .replace("'Best: '+o.best+'%'", "'أحسن نتيجة: '+o.best+'%'")
    .replace("'✓ You have mastered this topic!':p+' of '+tabs.length+' practice sets passed (80% or more)'", "'✓ اتقنت الدرس ده!':'عدّيت '+p+' من '+tabs.length+' تدريبات (80% أو أكتر)'"))
assert _BR_PJS_AR.count("عدّيت") == 2 and "أحسن نتيجة" in _BR_PJS_AR
for _bc in _BR_COURSES:
    _cfp = _bo.path.join(_BR_ROOT, _bc, "course.json")
    if not _bo.path.exists(_cfp):
        continue
    _cfg = _bload(_bc, "course.json")
    for _sec in _cfg["sections"]:
        # a section may be split into named groups (e.g. Reading / Writing inside a paper)
        if _sec.get("groups"):
            _sec["pages"] = [p for g in _sec["groups"] for p in g["pages"]]
        _skip = _bo.environ.get("BRITISH_SKIP")
        _miss = [s for s in _sec["pages"] if not _bo.path.exists(_bref(_bc, s)) or (_skip and _bre.search(_skip, s))]
        if _miss:
            print(f"[british] {_bc}: skipping {len(_miss)} missing page(s): {', '.join(_miss)}")
        _sec["pages"] = [s for s in _sec["pages"] if s not in _miss]
        for _g in _sec.get("groups", []):
            _g["pages"] = [s for s in _g["pages"] if s not in _miss]
    _cfg["sections"] = [s for s in _cfg["sections"] if s["pages"]]
    if not _cfg["sections"]:
        continue
    # one page can sit in two sections (e.g. grammar lessons in Paper 1 and Paper 2): build/link it once
    _order = list(dict.fromkeys(s for sec in _cfg["sections"] for s in sec["pages"] if not s.startswith("@")))
    _refs = [s for sec in _cfg["sections"] for s in sec["pages"] if s.startswith("@")]
    _compact = bool(_cfg.get("compact"))
    _pages = {s: _bload(_bc, s + ".json") for s in _order}
    _pages.update({s: _bj.load(open(_bref(_bc, s), encoding="utf-8")) for s in _refs})
    _rtl = bool(_cfg.get("rtl"))
    _hub = _cfg["hub"] or _cfg.get("back", "index.html")
    _active = _cfg.get("active", "british.html")
    _L = _cfg.get("labels") or {"prev": "← Previous", "next": "Next →", "back": "← Back to", "done": "Finished! Back to",
                                 "toc": "All pages in this course", "start": "Start the course →",
                                 "crumb": '<a href="british.html">British &amp; IGCSE</a> › '}
    _cpn = {"cp6": 6, "cp6m": 6, "cp6s": 6, "cp8": 8, "cp8m": 8, "cp8s": 8}.get(_bc)
    _yh = {"0510": ("british-year-9.html", "Year 9"), "oxford": ("british-igcse.html", "Year 10 · 11 · 12")}.get(_bc)
    if _yh:
        _L = dict(_L); _L["crumb"] = f'<a href="british.html">British &amp; IGCSE</a> › <a href="{_yh[0]}">{_yh[1]}</a> › '
    if _cpn and not _cfg.get("labels"):
        _L["crumb"] = f'<a href="british.html">British &amp; IGCSE</a> › <a href="british-checkpoint-{_cpn}.html">Checkpoint {_cpn}</a> › '
    if _cfg["hub"]:
        _secs = ""; _stiles = ""; _num = 0
        _lw = "الدرس" if _rtl else "Lesson"
        for _si, sec in enumerate(_cfg["sections"], 1):
            if _compact:
                _num = 0  # lessons are numbered inside each section
            def _li(s):
                global _num
                _num += 1
                if _compact:
                    _pp = _bpractice(_bc, s)
                    _ps = f'<small class="pp" data-pk="{s.split("/")[-1]}" data-n="{len(_pp["sets"])}">{len(_pp["sets"])} practice sets</small>' if _pp else ""
                    _lab = "Full test" if (not _rtl and _bre.search(r"-test-\d+$", s)) else f"{_lw} {_num}"
                    return f'<li><a href="{_bhref(s)}"><small class="ln">{_lab}</small><b>{_bE(_pages[s].get("nav") or _pages[s]["title"])}</b>{_ps}</a></li>'
                return f'<li><a href="{s}.html"><small class="ln">{_lw} {_num}</small><b>{_bE(_pages[s]["title"])}</b><span>{_bE(_pages[s].get("summary",""))}</span></a></li>'
            if sec.get("groups"):
                items = "".join(f'<li class="bgrp"><h3>{_bE(g["title"])}</h3></li>' + "".join(_li(s) for s in g["pages"]) for g in sec["groups"] if g["pages"])
            else:
                items = "".join(_li(s) for s in sec["pages"])
            _n = len(sec["pages"])
            _cnt = (f"{_n} دروس" if 3 <= _n <= 10 else f"{_n} درس") if _rtl else (f"{_n} lesson" + ("s" if _n != 1 else ""))
            if not _rtl and _bre.search(r"test|exam", sec["title"], _bre.I):
                _cnt = f"{_n} test" + ("s" if _n != 1 else "")
            _stiles += f'<a class="stile" href="#s{_si}" data-s="s{_si}"><b>{_bE(sec["title"])}</b><span>{_bE(sec["tag"]) + " · " if sec.get("tag") else ""}{_cnt}</span></a>'
            _secs += f'<div class="bsec" id="s{_si}"><h2>{_bE(sec["title"])}</h2>' + (f'<p>{_bE(sec["desc"])}</p>' if sec.get("desc") and not _compact else "") + f'<ul class="blist{" compact" if _compact else ""}">{items}</ul></div>'
        _intro = "".join(_bblock(b) for b in _cfg.get("intro_blocks", []))
        _first = _order[0]
        _all = "→ كل الأقسام" if _rtl else "← All sections"
        _pick = "اختار القسم:" if _rtl else "Choose a section:"
        _secjs = """<script>(function(){var t=document.querySelectorAll('.stile'),b=document.querySelectorAll('.bsec'),a=document.getElementById('sall');
function show(){var h=location.hash.slice(1);var ok=false;b.forEach(function(x){if(x.id===h)ok=true});
b.forEach(function(x){x.hidden=x.id!==h});t.forEach(function(x){x.classList.toggle('on',ok&&x.dataset.s===h)});if(a)a.hidden=!ok;
if(ok){var e=document.getElementById(h);if(e)e.scrollIntoView({behavior:'smooth',block:'start'})}}
if(b.length){b.forEach(function(x){x.hidden=true});document.querySelector('.bsecs').classList.add('js');}
window.addEventListener('hashchange',show);show();})();</script>"""
        _body = _BR_CSS + pagehead(_cfg["kicker"], _cfg["title"], _bE(_cfg["summary"])) + f'''
<section class="block"><div class="wrap"><div class="bc"{' dir="rtl" lang="ar"' if _rtl else ''}>{_intro}
<p><a class="btn" href="{_first}.html">{_L["start"]}</a></p>
<h2 class="pickh">{_pick}</h2><div class="stiles">{_stiles}</div>
<p id="sall" hidden><a href="#">{_all}</a></p>
<div class="bsecs">{_secs}</div></div></div></section>{_secjs}''' + _BR_PCSS + _BR_PJS
        page(_hub, f'{_cfg["title"]} — Abdelkriem Academy', _cfg.get("meta_desc", _cfg["summary"]), _body, _active)
    _dir = ' dir="rtl" lang="ar"' if _rtl else ""
    _BR_STATE.clear()
    if _rtl:
        _BR_STATE.update({"ndir": "rtl", "why": "ليه النموذج ده قوي؟"})
    for i, s in enumerate(_order):
        d = _pages[s]
        assert d["slug"] == s, (s, d["slug"])
        prev = _order[i-1] if i else None
        nxt = _order[i+1] if i + 1 < len(_order) else None
        pn = '<nav class="pnav" aria-label="Pages">'
        pn += f'<a href="{prev}.html"><small>{_L["prev"]}</small>{_bE(_pages[prev]["title"])}</a>' if prev else f'<a href="{_hub}"><small>{_L["back"]}</small>{_bE(_cfg["title"])}</a>'
        pn += f'<a href="{nxt}.html" style="text-align:end;margin-inline-start:auto"><small>{_L["next"]}</small>{_bE(_pages[nxt]["title"])}</a>' if nxt else f'<a href="{_hub}" style="text-align:end;margin-inline-start:auto"><small>{_L["done"]}</small>{_bE(_cfg["title"])}</a>'
        pn += "</nav>"
        toc = f'<details class="toc"><summary>{_L["toc"]}</summary>'
        for sec in _cfg["sections"]:
            toc += f'<p><b>{_bE(sec["title"])}</b></p><ul>' + "".join(
                f'<li{" class=on" if x == s else ""}><a href="{_bhref(x)}" dir="auto">{_bE(_pages[x]["title"])}</a></li>' for x in sec["pages"]) + "</ul>"
        toc += "</details>"
        _BR_STATE.pop("has_test", None)
        _pr = _bpractice(_bc, s)
        _bl = list(d["blocks"])
        if _pr:
            _cta = {"type": "_cta"}
            _ix = next((k for k in range(len(_bl) - 1, -1, -1) if _bl[k]["type"] == "test"), None)
            _bl.insert(_ix + 1 if _ix is not None else len(_bl), _cta)
        blocks = "".join(_bblock(b) if b["type"] != "_cta" else
                         (f'<div class="pcta"><div><b>اتقن الدرس: {len(_pr["sets"])} تدريبات تفاعلية</b><p>{sum(len(x["questions"]) for x in _pr["sets"])} سؤال من السهل للصعب، بتتصحح أونلاين، ومع كل اختيار شرح ليه صح أو غلط.</p><small class="pp" data-pk="{s}" data-n="{len(_pr["sets"])}"></small></div><a class="btn" href="{s}-practice.html">ابدأ التدريب الأول ←</a></div>' if _rtl else f'<div class="pcta"><div><b>Master this topic: {len(_pr["sets"])} more practice sets</b><p>{sum(len(x["questions"]) for x in _pr["sets"])} new questions, from Foundation to Challenge level, with an explanation for every choice.</p><small class="pp" data-pk="{s}" data-n="{len(_pr["sets"])}"></small></div><a class="btn" href="{s}-practice.html">Start Practice 1 →</a></div>')
                         for b in _bl)
        if _pr:
            blocks = _BR_PCSS + blocks + _BR_PJS
        if _BR_STATE.get("has_test"):
            blocks += _beng(_rtl)
        body = _BR_CSS + pagehead(_bE(d["kicker"]), _bE(d["title"]), _bE(d.get("summary", ""))) + f'''
<section class="block"><div class="wrap"><div class="bc"{_dir}>
<p class="crumb">{_L["crumb"]}<a href="{_hub}">{_bE(_cfg["title"])}</a></p>
{blocks}{pn}{toc}</div></div></section>'''
        page(s + ".html", f'{d["title"]} — {_cfg["short"]} — Abdelkriem Academy', d.get("summary", _cfg["summary"]), body, _active, rtl=_rtl)
        EXTRA_PAGES.append(s + ".html")
        if _pr:
            _nm = d.get("nav") or d["title"]
            _tabs = "".join(f'<button type="button" class="ptab" data-k="{s}-p{n}"><b>{_bE(st["title"])}</b><small>{_bE(st["level"])}</small><em>{len(st["questions"])} {"سؤال · لسه متحلّش" if _rtl else "questions · not tried yet"}</em></button>' for n, st in enumerate(_pr["sets"], 1))
            _pans = ""
            for n, st in enumerate(_pr["sets"], 1):
                tb = {"type": "test", "mode": "practice", "timed": False, "id": f"{s}-p{n}",
                      "title": f'{_nm} — {st["title"]} ({st["level"]})',
                      "intro": "من غير وقت. بعد كل سؤال هتعرف الصح وليه. لازم تجيب 80% أو أكتر علشان تعدّي التدريب ده." if _rtl else "Untimed. You get feedback after every question. Score 80% or more to pass this set.",
                      "sections": [{"name": st["title"], "minutes": 0, "questions": st["questions"]}]}
                _pans += f'<div class="ppanel" id="practice-{n}">' + _bblock(tb) + "</div>"
            _eng = _bo.path.join(_BR_ROOT, "_engine")
            if _rtl:
                _pbody = _BR_CSS + _BR_PCSS + pagehead(_bE(d["kicker"]) + " · تدريبات", f'{_bE(_nm)} — التدريبات', f'{len(_pr["sets"])} تدريبات على الدرس ده بس، من السهل للصعب، وكل إجابة متشرحة.') + f'''
<section class="block"><div class="wrap"><div class="bc" dir="rtl" lang="ar">
<p class="crumb">{_L["crumb"]}<a href="{_hub}">{_bE(_cfg["title"])}</a> › <a href="{s}.html">{_bE(_nm)}</a></p>
<div class="studyflow"><div><b>1 · أساسي</b>اتأكد إنك فاهم الدرس.</div><div><b>2 · مستوى الامتحان</b>أسئلة بنفس صعوبة الامتحان.</div><div><b>3 · تحدي</b>أصعب أشكال الأسئلة.</div></div>
<div class="bx ar notranslate" dir="rtl" lang="ar" translate="no"><b class="t">إزاي تستخدم التدريبات دي؟</b><ul><li>ذاكر الدرس الأول، وبعدين حل التدريبات بالترتيب من 1 لحد الآخر.</li><li>بعد كل سؤال هتعرف فورًا إجابتك صح ولا غلط، وليه كل اختيار صح أو غلط. اقرا الشرح كله حتى لو جاوبت صح.</li><li>لو جبت أقل من 80% في أي تدريب، دوس «أعد حل اللي غلطت فيهم» وبعدين ارجع للدرس.</li></ul></div>
<div class="pmast"><span>عدّيت 0 من {len(_pr["sets"])} تدريبات (80% أو أكتر)</span><div class="bar"><i></i></div></div>
<div class="ptabs">{_tabs}</div>{_pans}
<p><a class="btn" href="{s}.html">→ ارجع للدرس</a></p></div></div></section>''' + _beng(_rtl) + _BR_PJS_AR
            else:
                _pbody = _BR_CSS + _BR_PCSS + pagehead(_bE(d["kicker"]) + " · Practice", f'{_bE(_nm)} — Practice Sets', f'{len(_pr["sets"])} practice sets on this topic only, from Foundation to Challenge. Every answer is explained.') + f'''
    <section class="block"><div class="wrap"><div class="bc">
    <p class="crumb">{_L["crumb"]}<a href="{_hub}">{_bE(_cfg["title"])}</a> › <a href="{s}.html">{_bE(_nm)}</a></p>
    <div class="studyflow"><div><b>1 · Foundation</b>Check you know the rule.</div><div><b>2 · Exam level</b>Real test difficulty and traps.</div><div><b>3 · Challenge</b>The hardest versions the test uses.</div></div>
    <div class="bx ar notranslate" dir="rtl" lang="ar" translate="no"><b class="t">إزاي تستخدم التدريبات دي؟</b><ul><li>ذاكر الدرس الأول، وبعدين حل التدريبات بالترتيب من 1 لحد الآخر.</li><li>بعد كل سؤال هتعرف فورًا إجابتك صح ولا غلط، وليه كل اختيار صح أو غلط — اقرا الشرح كله حتى لو جاوبت صح.</li><li>لو جبت أقل من 80% في أي تدريب، دوس "Retry the ones I got wrong" وبعدين ارجع للدرس.</li></ul></div>
    <div class="pmast"><span>0 of {len(_pr["sets"])} practice sets passed (80% or more)</span><div class="bar"><i></i></div></div>
    <div class="ptabs">{_tabs}</div>{_pans}
    <p><a class="btn" href="{s}.html">← Back to the lesson</a></p></div></div></section>''' + _beng(_rtl) + _BR_PJS
            page(s + "-practice.html", (f'تدريبات {_nm} — {_cfg["short"]} — Abdelkriem Academy' if _rtl else f'{_nm} Practice — {_cfg["short"]} — Abdelkriem Academy'), (f'{len(_pr["sets"])} تدريبات تفاعلية على {_nm} بتتصحح فورًا مع شرح كل اختيار.' if _rtl else f'{len(_pr["sets"])} practice sets on {_nm} with instant feedback and an explanation for every answer choice.'), _pbody, _active, rtl=_rtl)
            EXTRA_PAGES.append(s + "-practice.html")
    _BR_BUILT[_bc] = len(_order)
