# British courses (Oxford ESL 9280, Cambridge IGCSE 0510, Checkpoint 8, Checkpoint 6) — display-only study pages.
# Content: british/<course>/course.json (hub page + ordered sections of page slugs) and british/<course>/<slug>.json
# (one page each, block format described in british/FORMAT.md). Each course hub REPLACES the old placeholder page
# (year-10-oxford.html, year-9-0510.html, checkpoint-8.html, checkpoint-6.html). Courses without course.json are skipped.
import json as _bj, os as _bo, re as _bre, html as _bh

_BR_ROOT = _bo.path.join(_bo.path.dirname(PAGES_DIR), "british")
_BR_COURSES = [c for c in _bo.environ.get("BRITISH_COURSES", "oxford,0510,cp8,cp6").split(",") if c]

_BR_CSS = """<style>
.bc{max-width:860px;margin:0 auto}
.bc h2{margin:2.2rem 0 .7rem;font-size:1.45rem}
.bc p{line-height:1.7}
.bc ul,.bc ol{line-height:1.7;padding-left:1.4rem}
.bc li{margin:.25rem 0}
.bc .tw{overflow-x:auto;margin:1rem 0}
.bc table{border-collapse:collapse;width:100%;font-size:.95rem}
.bc th,.bc td{border:1px solid #d9d4c7;padding:.55rem .7rem;text-align:left;vertical-align:top}
.bc th{background:#f3efe4}
.bc .bx{border-radius:12px;padding:1rem 1.2rem;margin:1.2rem 0;border-left:5px solid}
.bc .bx b.t{display:block;margin-bottom:.35rem}
.bc .bx ul{margin:.3rem 0 0}
.bc .bx.tip{background:#eef7ee;border-color:#3f8f4f}
.bc .bx.warning{background:#fdf0ec;border-color:#c4553a}
.bc .bx.exam{background:#eef2fb;border-color:#3a5fc4}
.bc .bx.ar{background:#fbf6e8;border-color:#c49a3a;border-left:0;border-right:5px solid #c49a3a;font-family:Cairo,sans-serif;direction:rtl;text-align:right}
.bc .bx.ar ul{padding-left:0;padding-right:1.4rem}
.bc .model{border:1px solid #d9d4c7;border-radius:14px;margin:1.5rem 0;overflow:hidden;background:#fff}
.bc .model .mh{background:#1f3a5f;color:#fff;padding:.8rem 1.2rem}
.bc .model .mh b{display:block;font-size:1.05rem}
.bc .model .mh span{font-size:.85rem;opacity:.85}
.bc .model .task{background:#f6f3ea;padding:.9rem 1.2rem;font-style:italic;border-bottom:1px solid #e6e0d0}
.bc .model .mt{padding:1rem 1.2rem}
.bc .model .mt p{margin:.0 0 .9rem}
.bc .model .mn{background:#eef7ee;padding:.9rem 1.2rem;border-top:1px solid #d7e8d7}
.bc .model .mn b{display:block;margin-bottom:.3rem}
.bc .qa{margin:1rem 0;padding-left:0;list-style:none;counter-reset:q}
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
.bsec{margin:2rem 0}
.bsec h2{margin-bottom:.3rem}
.bsec>p{margin-top:0;opacity:.85}
.bc .blist,.blist{list-style:none;padding:0;margin:1rem 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.8rem}
.blist a{display:block;height:100%;border:1px solid #d9d4c7;border-radius:12px;padding:.9rem 1rem;text-decoration:none;background:#fff}
.blist a b{display:block;margin-bottom:.25rem}
.blist a span{font-size:.9rem;opacity:.8;line-height:1.5}
@media (max-width:600px){.bc .pnav a{max-width:100%;flex:1 1 100%}}
</style>"""

def _bE(s):
    s = _bh.escape(str(s))
    s = _bre.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s

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
        task = f'<div class="task"><b>Task:</b> {_bE(b["task"])}</div>' if b.get("task") else ""
        text = "".join(f'<p dir="auto">{_bE(p).replace(chr(10), "<br>")}</p>' for p in b.get("text", []))
        notes = ""
        if b.get("notes"):
            notes = '<div class="mn"><b>Why this gets the marks</b><ul>' + "".join(f"<li>{_bE(n)}</li>" for n in b["notes"]) + "</ul></div>"
        return f'<div class="model"><div class="mh"><b>{_bE(b.get("title","Model answer"))}</b><span>{" · ".join(meta)}</span></div>{task}<div class="mt">{text}</div>{notes}</div>'
    if t == "qa":
        return '<ol class="qa">' + "".join(
            f'<li><p dir="auto">{_bE(i["q"])}</p><details><summary>Show answer</summary><div class="a" dir="auto">{_bE(i["a"])}</div></details></li>'
            for i in b["items"]) + "</ol>"
    if t == "vocab":
        return '<div class="tw"><table class="vocab"><thead><tr><th>Word / phrase</th><th>Meaning / use</th></tr></thead><tbody>' + "".join(
            f'<tr><td>{_bE(w[0])}</td><td dir="auto">{_bE(w[1])}</td></tr>' for w in b["items"]) + "</tbody></table></div>"
    if t == "phrases":
        return '<div class="phr">' + "".join(
            f'<div><h3>{_bE(g["title"])}</h3><ul>' + "".join(f"<li>{_bE(i)}</li>" for i in g["items"]) + "</ul></div>"
            for g in b["groups"]) + "</div>"
    raise ValueError(f"unknown block type {t!r}")

def _bload(course, name):
    return _bj.load(open(_bo.path.join(_BR_ROOT, course, name), encoding="utf-8"))

_BR_BUILT = {}
for _bc in _BR_COURSES:
    _cfp = _bo.path.join(_BR_ROOT, _bc, "course.json")
    if not _bo.path.exists(_cfp):
        continue
    _cfg = _bload(_bc, "course.json")
    for _sec in _cfg["sections"]:
        _miss = [s for s in _sec["pages"] if not _bo.path.exists(_bo.path.join(_BR_ROOT, _bc, s + ".json"))]
        if _miss:
            print(f"[british] {_bc}: skipping {len(_miss)} missing page(s): {', '.join(_miss)}")
        _sec["pages"] = [s for s in _sec["pages"] if s not in _miss]
    _cfg["sections"] = [s for s in _cfg["sections"] if s["pages"]]
    if not _cfg["sections"]:
        continue
    _order = [s for sec in _cfg["sections"] for s in sec["pages"]]
    _pages = {s: _bload(_bc, s + ".json") for s in _order}
    _hub = _cfg["hub"]
    # hub page
    _secs = ""
    for sec in _cfg["sections"]:
        items = "".join(f'<li><a href="{s}.html"><b>{_bE(_pages[s]["title"])}</b><span>{_bE(_pages[s].get("summary",""))}</span></a></li>' for s in sec["pages"])
        _secs += f'<div class="bsec"><h2>{_bE(sec["title"])}</h2>' + (f'<p>{_bE(sec["desc"])}</p>' if sec.get("desc") else "") + f'<ul class="blist">{items}</ul></div>'
    _intro = "".join(_bblock(b) for b in _cfg.get("intro_blocks", []))
    _first = _order[0]
    _body = _BR_CSS + pagehead(_cfg["kicker"], _cfg["title"], _bE(_cfg["summary"])) + f'''
<section class="block"><div class="wrap"><div class="bc">{_intro}
<p><a class="btn" href="{_first}.html">Start the course →</a></p>
{_secs}</div></div></section>'''
    page(_hub, f'{_cfg["title"]} — Abdelkriem Academy', _cfg.get("meta_desc", _cfg["summary"]), _body, "british.html")
    # content pages
    for i, s in enumerate(_order):
        d = _pages[s]
        assert d["slug"] == s, (s, d["slug"])
        prev = _order[i-1] if i else None
        nxt = _order[i+1] if i + 1 < len(_order) else None
        pn = '<nav class="pnav" aria-label="Pages">'
        pn += f'<a href="{prev}.html"><small>← Previous</small>{_bE(_pages[prev]["title"])}</a>' if prev else f'<a href="{_hub}"><small>← Back to</small>{_bE(_cfg["title"])}</a>'
        pn += f'<a href="{nxt}.html" style="text-align:right;margin-left:auto"><small>Next →</small>{_bE(_pages[nxt]["title"])}</a>' if nxt else f'<a href="{_hub}" style="text-align:right;margin-left:auto"><small>Finished! Back to</small>{_bE(_cfg["title"])}</a>'
        pn += "</nav>"
        toc = '<details class="toc"><summary>All pages in this course</summary>'
        for sec in _cfg["sections"]:
            toc += f'<p><b>{_bE(sec["title"])}</b></p><ul>' + "".join(
                f'<li{" class=on" if x == s else ""}><a href="{x}.html">{_bE(_pages[x]["title"])}</a></li>' for x in sec["pages"]) + "</ul>"
        toc += "</details>"
        blocks = "".join(_bblock(b) for b in d["blocks"])
        body = _BR_CSS + pagehead(_bE(d["kicker"]), _bE(d["title"]), _bE(d.get("summary", ""))) + f'''
<section class="block"><div class="wrap"><div class="bc">
<p class="crumb"><a href="british.html">British &amp; IGCSE</a> › <a href="{_hub}">{_bE(_cfg["title"])}</a></p>
{blocks}{pn}{toc}</div></div></section>'''
        page(s + ".html", f'{d["title"]} — {_cfg["short"]} — Abdelkriem Academy', d.get("summary", _cfg["summary"]), body, "british.html")
        EXTRA_PAGES.append(s + ".html")
    _BR_BUILT[_bc] = len(_order)
