#!/usr/bin/env python3
"""PDFs for the Quran course. Usage: python3 make_quran_pdf.py OUTDIR"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import qrender as R, qdata
R.WEB = False
from weasyprint import HTML
E = R.E; ar = R.ar

CSS = """
@page{size:A4;margin:16mm 15mm 18mm 15mm;
 @bottom-right{content:"Mohamed Abdelkriem · " string(lvl);font:600 8pt Cairo;color:#0f4c5c}
 @bottom-left{content:counter(page);font:600 8pt Cairo;color:#0f4c5c}}
@page cover{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
html{direction:rtl;font-family:Cairo,'Noto Naskh Arabic',sans-serif;font-size:10pt;color:#1d2b33;line-height:1.6}
.lvl{string-set:lvl content();font-size:1pt;color:#0f4c5c}
h1{font-weight:800}
h2{font-size:13pt;color:#0f4c5c;margin:14pt 0 6pt;padding-bottom:3pt;border-bottom:2pt solid #e0a63c;font-weight:800}
h3{font-size:10.5pt;color:#0f4c5c;margin:8pt 0 4pt}
a{color:#0f4c5c;text-decoration:none;font-weight:700}
.cover{page:cover;background:#0f4c5c;color:#fff;height:297mm;padding:34mm 22mm;box-sizing:border-box;position:relative}
.cover .kick{color:#e0a63c;font-weight:800;font-size:10pt}
.cover h1{font-size:30pt;line-height:1.3;margin:12pt 0 8pt}
.cover .sub{font-size:14pt;color:#e0a63c;font-weight:700}
.cover p{font-size:11pt}
.cover .by{position:absolute;bottom:26mm;right:22mm;left:22mm;border-top:1pt solid #e0a63c;padding-top:8pt;font-weight:700}
.band{background:#0f4c5c;color:#fff;border-radius:6pt;padding:10pt 12pt;margin-bottom:8pt}
.band .k{color:#e0a63c;font-weight:800;font-size:8.5pt}
.band h1{font-size:16pt;margin:2pt 0}
.band .g{font-size:9pt;color:#d5e6eb}
.sec{page-break-before:always}
table{width:100%;border-collapse:collapse;margin:4pt 0 6pt}
th{background:#0f4c5c;color:#fff;text-align:right;font-size:8.6pt;padding:4pt 6pt}
td{border:0.6pt solid #cfdde2;padding:4pt 6pt;vertical-align:top;font-size:8.8pt}
tr:nth-child(even) td{background:#f2f8fa}
td.d{font-weight:800;color:#0f4c5c;white-space:nowrap}
.q{font-family:'Amiri Quran',serif;font-size:15pt;line-height:2.3;margin:0;text-align:justify}
.an{font-family:'Amiri Quran',serif;color:#b7832a;font-size:11pt}
mark{background:#fbe3a6;border-radius:3pt;padding:0 2pt}
.ayah{border:0.8pt solid #cfdde2;border-radius:5pt;padding:5pt 9pt;margin:5pt 0;page-break-inside:avoid}
.ref{display:block;color:#5d6b72;font-size:8.5pt}
.enote{font-weight:700;font-size:9pt}
.goal{background:#fbf1dc;border-radius:5pt;padding:6pt 9pt}
.ex{margin:6pt 0;page-break-inside:avoid}
.ex ol{margin:0;padding-right:16pt}
details summary{display:none}
details .ans{display:none}
.por{border:0.8pt solid #cfdde2;border-radius:5pt;padding:5pt 9pt;margin:5pt 0;page-break-inside:avoid}
.por h3{margin:0 0 2pt;font-size:9pt;color:#b7832a}
ul.lst{margin:3pt 0;padding-right:14pt}
ul.lst li{margin-bottom:2pt}
.tip{background:#fbf1dc;border-right:3pt solid #e0a63c;padding:6pt 9pt;margin:8pt 0}
.key td{font-size:8.6pt}
.lines div{border-bottom:0.6pt solid #cfdde2;height:16pt}
"""

def cover(label, kick, title, sub, para):
    return (f'<div class="cover"><span class="lvl">{E(label)}</span><div class="kick">{E(kick)}</div><h1>{E(title)}</h1>'
            f'<div class="sub">{E(sub)}</div><p>{E(para)}</p><div class="by">Mohamed Abdelkriem · القرآن الكريم من الألف للياء</div></div>')

def doc(body, title, out):
    HTML(string=f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{E(title)}</title><meta name="author" content="Mohamed Abdelkriem"><style>{CSS}</style></head><body>{body}</body></html>', base_url=HERE).write_pdf(out)

def lessons_pdf(folder, part, out):
    d = os.path.join(HERE, folder)
    m = R.load(os.path.join(d, "meta.json"))
    files = sorted([f for f in os.listdir(d) if f.startswith("lesson")], key=lambda x: int(x[6:-5]))
    ls = [R.load(os.path.join(d, f)) for f in files]
    intro = m.get("intro", ""); intro = intro if isinstance(intro, str) else " ".join(intro)
    body = cover(part, "القرآن الكريم من الألف للياء · كورس مجاني لولي الأمر والطفل", m.get("title", part), f"{ar(len(ls))} درسًا أسبوعيًا", intro)
    body += '<section><h2>طريقة الاستخدام</h2><ul class="lst">' + "".join(f"<li>{E(x)}</li>" for x in m.get("how_to_use", [])) + "</ul>"
    if m.get("can_do"): body += '<h2>في نهاية هذا الجزء</h2><ul class="lst">' + "".join(f"<li>{E(x)}</li>" for x in m["can_do"]) + "</ul>"
    body += "<h2>الفهرس</h2><table>" + "".join(f"<tr><td class=d>الدرس {ar(L['n'])}</td><td>{E(L['title'])}</td></tr>" for L in ls) + "</table></section>"
    key = ""
    for L in ls:
        body += f'<section class="sec"><div class="band"><div class="k">{E(part)} · الدرس {ar(L["n"])} من {ar(len(ls))}</div><h1>{E(L["title"])}</h1></div>{R.lesson_html(L, part)}</section>'
        rows = "".join(f"<tr><td class=d>{E(ex['title'])}</td><td>{' · '.join(E(a) for a in ex.get('answers', []))}</td></tr>" for ex in L.get("exercises", []))
        if rows: key += f"<h3>الدرس {ar(L['n'])}: {E(L['title'])}</h3><table class='key'>{rows}</table>"
    body += f'<section class="sec"><h2>إجابات التمارين</h2>{key}</section>'
    doc(body, m.get("title", part), out)

def guide_pdf(out):
    g = R.load(os.path.join(HERE, "guide.json"))
    body = cover("دليل ولي الأمر", "القرآن الكريم من الألف للياء", g.get("title", "دليل ولي الأمر"), "كيف تحفّظ ابنك القرآن خطوة بخطوة", "اقرأ هذا الدليل قبل أن تبدأ، وارجع إليه كلما احتجت.")
    body += "<section>"
    for s in g["sections"]:
        body += f"<h2>{E(s['title'])}</h2>" + "".join(f"<p>{E(p)}</p>" for p in s.get("paragraphs", []))
        if s.get("bullets"): body += '<ul class="lst">' + "".join(f"<li>{E(b)}</li>" for b in s["bullets"]) + "</ul>"
    res = os.path.join(HERE, "RESOURCES.json")
    if os.path.exists(res):
        r = R.load(res)
        body += '<h2>مصادر الاستماع والتعلّم</h2><ul class="lst">'
        for x in r.get("reciters", []) + r.get("mushaf_tools", []):
            body += f'<li><a href="{E(x["url"])}">{E(x["name"])}</a> — {E(x.get("note",""))}</li>'
        for k in ("tajweed_videos", "reading_videos"):
            v = r.get(k) or {}
            if v.get("url"): body += f'<li><a href="{E(v["url"])}">{E(v.get("series",""))}</a> — {E(v.get("presenter",""))}</li>'
        body += "</ul>"
    tr = "".join(f"<tr><td class=d>الأسبوع {ar(i)}</td>" + "<td></td>" * 8 + "</tr>" for i in range(1, 13))
    body += ('<h2>جدول المتابعة الأسبوعي (اطبعه)</h2><p>ضع ✔ أو نجمة لكل يوم أتمّ فيه ابنك الحفظ والمراجعة.</p>'
             '<table><thead><tr><th>الأسبوع</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>تسميع</th><th>استماع</th><th>ملاحظات</th></tr></thead>'
             f"<tbody>{tr}</tbody></table></section>")
    doc(body, g.get("title", "دليل ولي الأمر"), out)

def hifz_pdf(n, out):
    lv = R.load(os.path.join(HERE, "plan", f"level{n}.json"))
    body = cover(lv["title"], "القرآن الكريم من الألف للياء · خطة الحفظ", lv["title"], f"{ar(len(lv['weeks']))} أسبوعًا · {lv['pace']}",
                 "كل يوم: حفظ جديد + مراجعة قريبة (آخر ٥ أيام) + مراجعة بعيدة من الحفظ القديم. أرقام الصفحات حسب مصحف المدينة النبوية (٦٠٤ صفحات) برواية حفص عن عاصم.")
    body += ('<section><h2>طريقة اليوم (٢٠–٣٠ دقيقة)</h2><ol class="lst"><li>استمع للحفظ الجديد بصوت القارئ ٣ مرات مع النظر في المصحف.</li>'
             '<li>اقرأ الآية الأولى من المصحف ٥ مرات، ثم سمّعها دون نظر ٣ مرات، ثم الثانية وهكذا، واربط كل آيتين معًا.</li>'
             '<li>سمّع الحفظ الجديد كاملًا لولي الأمر.</li><li>راجع «المراجعة القريبة» مرة واحدة من الذاكرة.</li><li>راجع «المراجعة البعيدة» مرة واحدة في أي وقت من اليوم.</li></ol>'
             '<div class="tip">اليوم السادس: تسميع حفظ الأسبوع كاملًا. اليوم السابع: راحة واستماع. لا تنتقل لحفظ جديد إذا كان التسميع ضعيفًا — زد المراجعة يومين.</div>'
             '<h2>الفهرس</h2><table>' + "".join(f"<tr><td class=d>الأسبوع {ar(w['week'])}</td><td>{E(ar(w['title']))}</td></tr>" for w in lv["weeks"]) + "</table></section>")
    for w in lv["weeks"]:
        rows = "".join(f"<tr><td class=d>{E(ar(d['day']))}</td><td>{E(ar(d['new']))}</td><td>{ar(d['page'])}</td><td>{E(ar(d['recent'] or '—'))}</td><td>{E(ar(d['far'] or '—'))}</td><td>☐</td></tr>" for d in w["days"])
        rows += f"<tr><td class=d>اليوم ٦</td><td colspan=4>{E(ar(w['day6']))}</td><td>☐</td></tr><tr><td class=d>اليوم ٧</td><td colspan=4>{E(ar(w['day7']))}</td><td>☐</td></tr>"
        sec = (f'<section class="sec"><div class="band"><div class="k">{E(lv["title"])} · الأسبوع {ar(w["week"])} من {ar(len(lv["weeks"]))}</div><h1>{E(ar(w["title"]))}</h1></div>'
               f"<table><thead><tr><th>اليوم</th><th>الحفظ الجديد</th><th>الصفحة</th><th>المراجعة القريبة</th><th>المراجعة البعيدة</th><th>تم</th></tr></thead><tbody>{rows}</tbody></table>")
        if n <= 3:
            sec += "<h2>نص الحفظ الجديد</h2>" + "".join(f'<div class="por"><h3>{E(ar(d["day"]))}: {E(ar(d["new"]))}</h3>' + "".join(R.portion_text(*g) for g in d["parts"]) + "</div>" for d in w["days"])
        if w.get("tajweed"):
            sec += "<h2>تجويد في حفظ هذا الأسبوع</h2>" + "".join(R.ayah_block(e["surah"], e["ayah"], e["word"], "الحكم: " + e["rule"])[0] for e in w["tajweed"])
        body += sec + "</section>"
    for t in lv["tests"]:
        body += f'<section class="sec"><div class="band"><div class="k">اختبار التسميع</div><h1>اختبار الجزء {ar(t["juz"])}</h1><div class="g">يقرأ ولي الأمر بداية الآية، ويكمل الطفل ثلاث آيات دون النظر في المصحف.</div></div>'
        body += "".join(f'<div class="ayah"><b>السؤال {ar(i)}:</b> {E(ar(q["ask"]))}<p class="q">{E(q["start"])} …</p><span class="ref">الدرجة: ____ / ٢</span></div>' for i, q in enumerate(t["questions"], 1))
        body += '<h3>طريقة التصحيح</h3><ul class="lst">' + "".join(f"<li>{E(ar(r))}</li>" for r in t["rubric"]) + "</ul><p><b>الدرجة الكلية: ______ / ٢٠</b></p></section>"
    doc(body, lv["title"], out)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    which = sys.argv[2:] or ["all"]
    if "all" in which or "guide" in which: guide_pdf(os.path.join(out, "Quran-Parent-Guide.pdf"))
    if "all" in which or "reading" in which: lessons_pdf("reading", "التمهيدي: تعلّم القراءة", os.path.join(out, "Quran-Reading.pdf"))
    if "all" in which or "tajweed" in which: lessons_pdf("tajweed", "أحكام التجويد", os.path.join(out, "Quran-Tajweed.pdf"))
    for n in range(1, 13):
        if "all" in which or f"hifz{n}" in which: hifz_pdf(n, os.path.join(out, f"Quran-Hifz-Level-{n}.pdf"))
    print("done")
