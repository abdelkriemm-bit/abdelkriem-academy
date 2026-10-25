"""Make printable exam papers + mark schemes (PDF) from the 'test' blocks of course pages.
usage: python3 make_pdf.py OUTDIR page1.json [page2.json ...]
Writes OUTDIR/<slug>-paper.pdf and OUTDIR/<slug>-mark-scheme.pdf"""
import json, sys, os, re, html
from playwright.sync_api import sync_playwright

def fmt(s):
    s = html.escape(str(s))
    s = re.sub(r"_{3,}", '<span class="blank"></span>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)
    s = re.sub(r"\^\{(.+?)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"_\{(.+?)\}", r"<sub>\1</sub>", s)
    out = []
    for l in s.split("\n"):
        if re.search(r"\S\s*\|\s*\S", l):
            cells = [c.strip() for c in l.split("|")]
            if out and isinstance(out[-1], list): out[-1].append(cells)
            else: out.append([cells])
        else: out.append(l)
    res = []
    for x in out:
        if isinstance(x, list):
            res.append('<table class="tb">' + "".join("<tr>" + "".join(f"<{'th' if i == 0 else 'td'}>{c}</{'th' if i == 0 else 'td'}>" for c in r) + "</tr>" for i, r in enumerate(x)) + "</table>")
        else: res.append(x + "<br>")
    return re.sub(r"(<br>)+$", "", "".join(res))

def svg(s):
    return f'<div class="img">{s}</div>' if s and s.lstrip().lower().startswith("<svg") and "<script" not in s.lower() else ""

CSS = """
@page{size:A4;margin:16mm 15mm 18mm}
body{font-family:Arial,Helvetica,sans-serif;font-size:11pt;color:#111;line-height:1.45}
.cover{border:2px solid #0f1b33;border-radius:8px;padding:14px 18px;margin-bottom:14px}
.cover h1{font-size:17pt;margin:0 0 4px}.cover p{margin:4px 0}
.fields{display:flex;gap:18px;margin-top:10px}.fields span{flex:1;border-bottom:1px solid #333;padding-top:16px;font-size:9.5pt}
.sec{page-break-before:always}.sec.first{page-break-before:auto}
h2{font-size:13pt;background:#0f1b33;color:#fff;padding:5px 9px;border-radius:4px}
.q{page-break-inside:avoid;margin:0 0 12px;padding-bottom:6px;position:relative}.q:not(.part){border-top:1px solid #999;padding-top:8px;margin-top:6px}.part{margin-left:18px}.gq{margin:0 0 4px}
.qn{font-weight:bold;margin-right:6px}.mk{float:right;font-weight:bold;font-size:10pt}
.stem{background:#f4f4f4;padding:6px 9px;border-radius:4px;margin:4px 0}
.img{text-align:center;margin:6px 0}.img svg{max-width:100%;height:auto}
.ch{margin:4px 0 0 18px;padding:0;list-style:none}.ch li{margin:2px 0}.ch li:before{content:"\\25A2  "}
.line{border-bottom:1px solid #777;height:24px}
.box{display:inline-block;border:1px solid #333;min-width:120px;height:26px;vertical-align:middle;margin-left:6px}
.work{border:1px dashed #aaa;height:56px;margin:6px 0;color:#999;font-size:9pt;padding:3px}
.ans{color:#0b4f1e}.ms{background:#f2f7f2;border-left:4px solid #2e7d32;padding:5px 8px;margin-top:4px}
.foot{font-size:8.5pt;color:#555;margin-top:20px}
.tb{border-collapse:collapse;margin:4px 0}.tb th,.tb td{border:1px solid #666;padding:2px 7px}.tb th{background:#eee}
.blank{display:inline-block;min-width:60px;border-bottom:1px solid #111}
"""

def paper(T, title, scheme=False):
    marks = sum(q.get("m", 1) for s in T["sections"] for q in s["questions"])
    h = [f'<div class="cover"><h1>{fmt(title)}{" — Mark Scheme" if scheme else ""}</h1>']
    h.append("<p>" + " · ".join(f'{fmt(s["name"])}: {s["minutes"]} minutes' + (" · no calculator" if s.get("calc") is False else " · calculator allowed" if s.get("calc") else "") for s in T["sections"]) + f" · Total {marks} marks</p>")
    if not scheme:
        h.append("<p>Answer all questions. Write your answers in the spaces provided. Show your working where there is space for it. The number of marks for each question is shown in brackets [ ].</p>")
        h.append('<div class="fields"><span>Name</span><span>Class</span><span>Date</span><span>Mark: ____ / ' + str(marks) + "</span></div>")
    h.append("<p style='font-size:9pt'>Abdelkriem Academy · practice paper written in the style of Cambridge Checkpoint. Not an official Cambridge paper.</p></div>")
    for si, s in enumerate(T["sections"]):
        sm = sum(q.get("m", 1) for q in s["questions"])
        h.append(f'<div class="sec{" first" if si == 0 else ""}"><h2>{fmt(s["name"])} — {s["minutes"]} minutes — {sm} marks</h2>')
        g = 0; prev_p = None; prev_img = None
        for i, q in enumerate(s["questions"], 1):
            t = q.get("t", "mcq"); m = q.get("m", 1)
            p = q.get("p") or ""; im = q.get("img") or ""
            new_group = (not p) or p != prev_p
            if new_group: g += 1
            stem_txt = re.sub(r"^\s*Question\s+\d+\s*\n?", "", p) if p else ""
            h.append(f'<div class="q{"" if new_group else " part"}"><span class="mk">[{m}]</span>')
            if new_group:
                h.append(f'<p class="gq"><span class="qn">{g}</span>{fmt(stem_txt) if stem_txt else ""}</p>')
            if im and (new_group or im != prev_img): h.append(svg(im))
            h.append(f'<p>{"" if (new_group and p) or not new_group else ""}{fmt(q["q"]) if (p or not new_group) else "<span class=qn></span>" + fmt(q["q"])}</p>')
            prev_p = p; prev_img = im
            if t == "mcq":
                h.append('<ul class="ch">' + "".join(f"<li>{'ABCD'[j]}) {fmt(c)}</li>" for j, c in enumerate(q["c"])) + "</ul>")
            if scheme:
                if t == "mcq": a = f"{'ABCD'[q['a']]}) {fmt(q['c'][q['a']])}"
                elif t == "open": a = fmt(q.get("ms", ""))
                else: a = " or ".join(fmt(x) for x in q.get("ans", [])) + (" " + fmt(q["unit"]) if q.get("unit") else "")
                h.append(f'<div class="ms"><b class="ans">Answer:</b> {a}' + (f'<br><b>Notes / working:</b> {fmt(q["e"])}' if q.get("e") else "") + "</div>")
            else:
                if t == "num":
                    h.append('<div class="work">Working</div><p style="text-align:right">Answer <span class="box"></span> ' + (fmt(q["unit"]) if q.get("unit") else "") + "</p>")
                elif t == "text":
                    h.append('<div class="line"></div>')
                elif t == "open":
                    h.append('<div class="line"></div>' * max(2, 2 * m))
            h.append("</div>")
        h.append("</div>")
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(h)}</body></html>"

def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for f in sys.argv[2:]:
            d = json.load(open(f))
            for blk in d["blocks"]:
                if blk.get("type") != "test": continue
                for scheme, suf in ((False, "paper"), (True, "mark-scheme")):
                    pg.set_content(paper(blk, d["title"], scheme), wait_until="load")
                    pg.pdf(path=f'{out}/{d["slug"]}-{suf}.pdf', format="A4", print_background=True,
                           display_header_footer=True, header_template="<span></span>",
                           footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#666">Abdelkriem Academy · abdelkriemacademy.com · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
                           margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
                    print("wrote", f'{d["slug"]}-{suf}.pdf')
                break
        b.close()

if __name__ == "__main__":
    main()
