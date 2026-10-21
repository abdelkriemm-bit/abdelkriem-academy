#!/usr/bin/env python3
"""Build a course-level PDF (same look as the Level 1 book) from course/levelN/*.json.
Usage: python3 make_pdf.py course/level2 out.pdf"""
import json, os, sys, html, urllib.parse
from weasyprint import HTML

E = html.escape

def load_level(d):
    weeks = [json.load(open(os.path.join(d, f"week{i}.json"), encoding="utf-8")) for i in range(1, 13)]
    checks = [json.load(open(os.path.join(d, f"progress_check_{i}.json"), encoding="utf-8")) for i in (1, 2, 3)]
    meta = json.load(open(os.path.join(d, "meta.json"), encoding="utf-8"))
    return meta, weeks, checks

def srch(t):
    q = t.replace("“", "").replace("”", "")
    return "https://www.google.com/search?q=" + urllib.parse.quote(q)

def listen_html(s):
    import re as _re
    parts = [p.strip() for p in _re.split(r"(?<=\)) \+ ", s)]
    out = []
    for p in parts:
        low = p.lower()
        if "free day" in low or not p:
            out.append(E(p))
        else:
            out.append(f'<a href="{srch(p)}">{E(p)}</a>')
    return "<br>+ ".join(out)

CSS = """
@page{size:A4;margin:16mm 15mm 18mm 15mm;
 @bottom-left{content:"Mohamed Abdelkriem · " string(lvl);font:600 8pt Inter;color:#0f4c5c}
 @bottom-right{content:counter(page);font:600 8pt Inter;color:#0f4c5c}}
@page cover{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
html{font-family:Inter,'Noto Naskh Arabic',sans-serif;font-size:9.2pt;color:#1d2b33;line-height:1.42}
.lvl{string-set:lvl content();font-size:1pt;color:#0f4c5c}
.ar,[lang=ar]{font-family:'Noto Naskh Arabic',serif;direction:rtl;text-align:right}
a{color:#0f4c5c;text-decoration:none;font-weight:600}
h2{font-size:13pt;color:#0f4c5c;margin:14pt 0 6pt;padding-bottom:3pt;border-bottom:2pt solid #e0a63c}
h3{font-size:9.5pt;color:#0f4c5c;margin:8pt 0 4pt}
.cover{page:cover;background:#0f4c5c;color:#fff;height:297mm;padding:30mm 22mm;box-sizing:border-box;position:relative}
.cover .kick{color:#e0a63c;font-weight:800;letter-spacing:2pt;font-size:8.5pt;text-transform:uppercase}
.cover h1{font-size:40pt;line-height:1.05;margin:10pt 0 4pt;font-weight:800}
.cover .art{font-family:Cairo;font-size:22pt;font-weight:800;color:#e0a63c;margin:2pt 0 14pt;direction:rtl;text-align:left}
.cover p{font-size:11pt;max-width:150mm}
.pills span{display:inline-block;background:#e0a63c;color:#0f4c5c;border-radius:10pt;padding:3pt 9pt;margin:0 4pt 4pt 0;font-weight:800;font-size:8pt}
.cover .by{position:absolute;bottom:26mm;left:22mm;right:22mm;border-top:1pt solid #e0a63c;padding-top:8pt;font-weight:700}
table{width:100%;border-collapse:collapse;margin:4pt 0 6pt}
th{background:#0f4c5c;color:#fff;text-align:left;font-size:8.3pt;padding:4pt 6pt}
td{border:0.6pt solid #cfdde2;padding:3.5pt 6pt;vertical-align:top;font-size:8.6pt}
tr:nth-child(even) td{background:#f2f8fa}
td.d{font-weight:700;color:#0f4c5c;white-space:nowrap}
.band{background:#0f4c5c;color:#fff;border-radius:6pt;padding:10pt 12pt;margin-bottom:8pt}
.band .k{color:#e0a63c;font-weight:800;font-size:8pt;letter-spacing:1pt}
.band h1{font-size:17pt;margin:2pt 0;font-weight:800}
.band .g{font-size:8.8pt;color:#d5e6eb}
.week{page-break-before:always}
.sets{display:flex;flex-wrap:wrap;justify-content:space-between}
.set{width:49%}
.set td.en{font-weight:700;width:46%}
.sent,.set table{page-break-inside:avoid}
.sent td.n{width:14pt;color:#e0a63c;font-weight:800}
.sent td.e{width:47%}
.box{border:1pt solid #cfdde2;border-radius:5pt;padding:8pt 10pt;margin:4pt 0}
.arbox{background:#fbf1dc;border-radius:5pt;padding:7pt 10pt;margin:5pt 0;font-size:10pt}
.ex{margin:6pt 0 8pt;page-break-inside:avoid}
.ex h3{margin-bottom:3pt}
.ex ol{margin:0;padding:0;list-style:none;columns:2;column-gap:16pt}
.ex.one ol{columns:1}
.ex li{margin:0 0 3pt;break-inside:avoid}
.ws{border:1.2pt dashed #e0a63c;border-radius:6pt;padding:8pt 10pt;margin-top:8pt;page-break-inside:avoid}
.ws b{color:#0f4c5c}
.lines div{border-bottom:0.6pt solid #cfdde2;height:15pt}
.example{color:#5d6b72;font-size:8pt;margin-top:6pt}
.note{color:#5d6b72;font-size:8.3pt}
.key h3{margin:7pt 0 2pt}
.key td{font-size:8.2pt}
ul.t{margin:3pt 0;padding-left:14pt}
ul.t li{margin-bottom:2pt}
.tip{background:#fbf1dc;border-left:3pt solid #e0a63c;padding:6pt 9pt;margin:8pt 0;font-size:8.6pt}
"""

def tbl(headers, rows, cls=""):
    h = "".join(f"<th>{E(x)}</th>" for x in headers)
    r = "".join("<tr>" + "".join(f'<td{" class=d" if i==0 else ""}>{E(c)}</td>' for i, c in enumerate(row)) + "</tr>" for row in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'

def is_ar(s):
    return any("؀" <= ch <= "ۿ" for ch in s)

def cell(s):
    return f'<span lang="ar">{E(s)}</span>' if is_ar(s) and not any("a" <= c.lower() <= "z" for c in s) else E(s)

def week_html(w, label):
    n = w["week"]
    plan = "".join(f'<tr><td class=d>{E(p["day"])}</td><td>{E(p["learn"])}</td><td>{listen_html(p["listen"])}</td><td>{E(p["practise"])}</td></tr>' for p in w["plan"])
    sets = ""
    for s in w["word_sets"]:
        rows = "".join(f'<tr><td class=en>{E(a)}</td><td class=ar>{E(b)}</td></tr>' for a, b in s["words"])
        sets += f'<div class="set"><h3>{E(s["name"])}</h3><table>{rows}</table></div>'
    sets += '<div class="set"><h3>My extra words</h3><table>' + "<tr><td class=en>&nbsp;</td><td></td></tr>" * 6 + "</table></div>"
    sents = "".join(f'<tr><td class=n>{i}</td><td class=e>{E(a)}</td><td class=ar>{E(b)}</td></tr>' for i, (a, b) in enumerate(w["sentences"], 1))
    g = w["grammar"]
    gh = ""
    if g.get("intro_en"):
        gh += "".join(f"<p>{E(x)}</p>" for x in g["intro_en"].split("\n"))
    for t in g.get("tables", []):
        h = "".join(f"<th>{E(x)}</th>" for x in t["headers"])
        r = "".join("<tr>" + "".join(f"<td>{cell(c)}</td>" for c in row) + "</tr>" for row in t["rows"])
        gh += f"<table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>"
    if g.get("intro_ar"):
        gh += f'<div class="arbox ar" lang="ar">{E(g["intro_ar"])}</div>'
    gh += "".join(f"<p>{E(x)}</p>" for x in g.get("notes", []))
    exs = ""
    for ex in w["exercises"]:
        long_items = any(len(i) > 48 for i in ex["items"]) or is_ar("".join(ex["items"]))
        items = "".join(f'<li dir="auto"{" lang=ar" if is_ar(i) else ""}>{E(i)}</li>' for i in ex["items"])
        exs += f'<div class="ex{" one" if long_items else ""}"><h3>{E(ex["title"])}</h3><ol>{items}</ol></div>'
    ws = w.get("write_speak", "")
    head, _, rest = ws.partition("—")
    example = " ".join(w.get("other", []))
    wsh = f'<div class="ws"><b>{E(head.strip())}</b> — {E(rest.strip())}<div class="lines">' + "<div></div>" * 9 + f'</div><div class="example">{E(example)}</div></div>'
    return f'''<section class="week"><div class="band"><div class="k">WEEK {n} OF 12</div><h1>{E(w["title"])}</h1><div class="g">{E(w["grammar_title"])}</div></div>
<h2>This week's plan</h2><table><thead><tr><th>Day</th><th>Learn</th><th>Listen / Watch</th><th>Practise</th></tr></thead><tbody>{plan}</tbody></table>
<h2>30 words to learn</h2><div class="sets">{sets}</div>
<h2>10 sentences to memorise</h2><table class="sent">{sents}</table>
<h2>Grammar of the week</h2>{gh}
<h2>Exercises</h2>{exs}{wsh}</section>'''

def check_html(c):
    secs = ""
    for s in c["sections"]:
        items = "".join(f'<li dir="auto"{" lang=ar" if is_ar(i) else ""}>{E(i)}</li>' for i in s.get("items", []))
        one = " one" if s["title"].startswith(("B", "D")) else ""
        secs += f'<div class="ex{one}"><h3>{E(s["title"])}</h3><ol>{items}</ol></div>'
    return f'''<section class="week"><div class="band"><div class="k">PROGRESS CHECK</div><h1>{E(c["title"])}</h1><div class="g">{E(c.get("subtitle",""))}</div></div>
{secs}<p><b>{E(c.get("score",""))}</b></p></section>'''

def key_html(weeks, checks):
    out = '<section class="week key"><h2>Answer Key</h2><p class="note">Check your answers after you finish each exercise. Translations can have other correct forms — if you are not sure, ask your teacher.</p>'
    for i, w in enumerate(weeks):
        rows = [[ex["title"].split("·")[0].split("—")[0].strip(), " · ".join(ex.get("answers", []))] for ex in w["exercises"]]
        out += f'<h3>Week {w["week"]} · {E(w["title"])}</h3>' + tbl(["", "Answers"], rows)
        if (i + 1) % 4 == 0:
            c = checks[(i + 1) // 4 - 1]
            rows = [[s["title"][:1], " · ".join(s["answers"])] for s in c["sections"] if s.get("answers")]
            out += f'<h3>{E(c["title"])}</h3>' + tbl(["", "Answers"], rows)
    return out + "</section>"

def build(level_dir, out):
    meta, weeks, checks = load_level(level_dir)
    L = meta["level"]
    label = f'Level {L} · {meta["name_en"]}'
    lis = "".join(f'<h3>{E(g["group"])}</h3><ul class="t">' + "".join(f'<li><a href="{E(i["url"])}">{E(i["name"])}</a></li>' for i in g["items"]) + "</ul>" for g in meta["links"])
    body = f'''<div class="cover"><span class="lvl">{E(label)}</span><div class="kick">English Course · Level {L} · {E(meta["cefr"])} · 12 weeks · 30 minutes a day</div>
<h1>English Course<br>Level {L}: {E(meta["name_en"])}</h1><div class="art" lang="ar">{E(meta["name_ar"])}</div>
<p>{E(meta["tagline_en"])}</p><p class="ar" lang="ar" style="text-align:left">{E(meta["tagline_ar"])}</p>
<div class="pills"><span>360 words</span><span>120 key sentences</span><span>12 grammar points</span><span>48 exercises + answers</span><span>3 progress checks</span></div>
<div class="by">Mohamed Abdelkriem · English Course · Level {L} ({E(meta["cefr"])})</div></div>

<section><h2>How to Use This Course</h2>
<p>This book is all you need for the next 3 months. Every day has a clear job. Do 30 minutes, 6 days a week, and on day 7 just enjoy a story or a video. Don't skip days — 30 minutes every day is better than 3 hours once a week.</p>
<div class="arbox ar" lang="ar">الكتاب ده هو كل اللي محتاجه في الـ٣ شهور الجايين. ذاكر ٣٠ دقيقة في اليوم، ٦ أيام في الأسبوع، واليوم السابع استمتع بقصة أو فيديو بالإنجليزي.</div>
<h3>Who is this level for?</h3><div class="arbox ar" lang="ar">{E(meta["intro_ar"])}</div>
<h3>After this level you can…</h3><ul class="t">{"".join(f"<li>{E(x)}</li>" for x in meta["can_do"])}</ul>
<h3>Your 30 minutes every day</h3>
{tbl(["Time","What to do"],[["5 min","Review yesterday's words and sentences: cover the English and say it from the Arabic."],["8 min","Learn today's 6 words and 2 sentences. Say each one aloud 5 times and copy it into your notebook."],["10 min","Listen / watch today's resource from the weekly plan, using the 4-step method below."],["5 min","Practise: do today's exercise in pencil, then check the Answer Key at the end of the book."],["2 min","Speak: say 3 sentences about your day using today's words."]])}
<h3>The 4-step listening method</h3>
{tbl(["#","Step"],[["1","Listen only. Don't read. Try to catch the general idea."],["2","Listen and read the script or subtitles. Underline new words."],["3","Shadow: pause after each sentence and repeat it with the same sound and speed."],["4","Listen again without the text. You will understand much more!"]])}
<div class="tip">Too fast? On YouTube tap ⚙ Settings → Playback speed → 0.75 and turn on English subtitles (CC) — not Arabic. After Weeks 4, 8 and 12 there is a Progress Check: score 16/20 or more to move on.</div>
<section class="week" dir="rtl" lang="ar" style="direction:rtl;text-align:right;font-family:'Noto Naskh Arabic',serif;font-size:10.5pt"><h2>إزاي تذاكر الكورس ده؟ (اقرا الصفحة دي الأول)</h2>
<p>ذاكر <b>30 دقيقة كل يوم، 6 أيام في الأسبوع</b>، واليوم السابع راحة أو استماع لقصة. كل أسبوع فيه: كلمات بمعناها بالعربي، وجمل تحفظها، وقاعدة مشروحة بالعربي، وتمارين، وخطة استماع لكل يوم.</p>
<h3>الـ 30 دقيقة بتوع كل يوم</h3><table><tr><td class=d>5 دقايق</td><td>راجع كلمات وجمل امبارح: غطّي الإنجليزي وقول الكلمة من العربي.</td></tr>
<tr><td class=d>8 دقايق</td><td>احفظ 6 كلمات وجملتين جداد، وقول كل واحدة بصوت عالي 5 مرات واكتبها في الكشكول.</td></tr>
<tr><td class=d>10 دقايق</td><td>اسمع أو اتفرج على درس النهارده من خطة الأسبوع (عمود Listen / Watch).</td></tr>
<tr><td class=d>5 دقايق</td><td>حل تمرين النهارده بالقلم الرصاص، وصحّح من الإجابات في آخر الكتاب.</td></tr>
<tr><td class=d>2 دقيقة</td><td>اتكلم: قول 3 جمل عن يومك بكلمات النهارده.</td></tr></table>
<h3>طريقة الاستماع في 4 خطوات</h3><ol><li>اسمع بس من غير ما تقرا، وافهم الفكرة العامة.</li><li>اسمع واقرا النص أو الترجمة الإنجليزي، وحط خط تحت الكلمات الجديدة.</li><li>ردّد وراه: وقّف بعد كل جملة وقولها بنفس الصوت والسرعة.</li><li>اسمع تاني من غير النص.</li></ol>
<h3>إزاي تستخدم المصادر؟</h3><ul class="t"><li>دوس على اسم الدرس في خطة الأسبوع، أو اكتبه بالظبط في جوجل أو يوتيوب، وافتح النتيجة من الموقع نفسه.</li><li><b>(podcast)</b> أو <b>(audio)</b> = صوت بس، <b>(video)</b> = فيديو، <b>(reading)</b> = قراءة، <b>(listening)</b> = استماع بالنص.</li><li>لو الكلام سريع: في يوتيوب ⚙ ← Playback speed ← 0.75، وشغّل الترجمة الإنجليزي مش العربي.</li></ul>
<h3>قبل ما تبدأ</h3><ul class="t"><li>اعمل اختبار مستوى مجاني واكتب نتيجتك، وكرّره في آخر الكورس.</li><li>جهّز كشكول: الإنجليزي على الشمال والعربي على اليمين، صفحة لكل أسبوع.</li><li>نزّل تطبيق كروت مجاني زي Anki وحط فيه كلمات كل يوم.</li><li>بعد الأسبوع الرابع والثامن والثاني عشر فيه اختبار: لو جبت 16 من 20 أو أكتر كمّل، لو أقل راجع جمل الأسابيع دي 3 أيام وحاول تاني.</li><li><b>القاعدة الذهبية:</b> مش لازم تفهم كل كلمة. افهم الفكرة وكمّل.</li></ul></section>
<section class="week"><h2>All Your Links in One Place</h2><p>Every resource in this book is free. Tap a title in the weekly plan to find it, or use these main links:</p>{lis}
<div class="tip">If a link ever stops working, search the exact title in YouTube or Google — every lesson in this book has its exact name.</div></section>
'''
    for i, w in enumerate(weeks):
        body += week_html(w, label)
        if (i + 1) % 4 == 0:
            body += check_html(checks[(i + 1) // 4 - 1])
    end = meta["end"]
    tr = "".join(f"<tr><td class=d>Week {i}</td>" + "<td></td>" * 8 + "</tr>" for i in range(1, 13))
    body += f'''<section class="week"><h2>{E(end["title"])}</h2><p>{E(end["intro"])}</p><ul class="t">{"".join(f"<li>{E(x)}</li>" for x in end["next_steps"])}</ul>
<div class="arbox ar" lang="ar">{E(end["tip_ar"])}</div>
<h2>My progress tracker</h2><p class="note">Tick ✔ each day you finish your 30 minutes.</p>
<table><thead><tr><th>Week</th><th>D1</th><th>D2</th><th>D3</th><th>D4</th><th>D5</th><th>D6</th><th>D7</th><th>Notes</th></tr></thead><tbody>{tr}</tbody></table></section>'''
    body += key_html(weeks, checks)
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>English Course Level {L}: {E(meta["name_en"])} — Mohamed Abdelkriem</title><meta name="author" content="Mohamed Abdelkriem"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=doc, base_url=".").write_pdf(out)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
    print("ok", sys.argv[2])
