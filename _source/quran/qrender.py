# Shared HTML fragments for the Quran course (site pages and PDFs). All Quran text comes from qdata (verified Tanzil Uthmani).
import os, sys, json, html, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import qdata
E = html.escape
AR_DIG = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
def ar(n): return str(n).translate(AR_DIG)

FIX = {"النبإ": "النبأ"}
def sname(s):
    n = re.sub(r'[ً-ْٰۡ۟-ۭ]', '', qdata.SURAH_AR[s-1]).replace('سورة ', '').replace('ٱ', 'ا').strip()
    return FIX.get(n, n)

def load(p):
    return json.load(open(p, encoding="utf-8"))

def highlight(text, word):
    """wrap the words of `text` that match `word` (skeleton match, may be 2+ words) in <mark>. Returns (html, found)."""
    tw = text.split(" ")
    target = [qdata.skel(x) for x in word.replace("‌", " ").split() if qdata.skel(x)]
    sk = [qdata.skel(x) for x in tw]
    n = len(target)
    for i in range(len(tw)):
        j, k = i, 0
        seq = []
        while j < len(tw) and k < n:
            if not sk[j]: seq.append(j); j += 1; continue  # waqf marks
            if sk[j] != target[k]: break
            seq.append(j); j += 1; k += 1
        if k == n and n:
            out = []
            for idx, w in enumerate(tw):
                if idx == seq[0]: out.append("<mark>")
                out.append(E(w))
                if idx == seq[-1]: out.append("</mark>")
            return " ".join(out).replace("<mark> ", "<mark>").replace(" </mark>", "</mark>"), True
    # fallback: partial (single word contained)
    for i, s in enumerate(sk):
        if target and target[0] and (target[0] in s or s in target[0]) and s:
            return " ".join(f"<mark>{E(w)}</mark>" if idx == i else E(w) for idx, w in enumerate(tw)), True
    return E(text), False

def ayah_block(s, a, word=None, note=None):
    t = qdata.ayah_text(s, a)
    h, ok = highlight(t, word) if word else (E(t), True)
    ref = f'<span class="ref">﴿سورة {E(sname(s))} – الآية {ar(a)}﴾</span>'
    nt = f'<div class="enote">{E(note)}</div>' if note else ""
    return f'<div class="ayah"><p class="q" lang="ar">{h} <span class="an">﴿{ar(a)}﴾</span></p>{ref}{nt}</div>', ok

def portion_text(s, a1, a2):
    return '<p class="q" lang="ar">' + " ".join(f'{E(qdata.ayah_text(s, a))} <span class="an">﴿{ar(a)}﴾</span>' for a in range(a1, a2 + 1)) + "</p>"

def linkify(x):
    m = re.search(r"(https?://\S+)", x)
    if not m: return E(x)
    u = m.group(1); t = x.replace(u, "").rstrip(" —-")
    return f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>'
def lesson_html(d, kind_label):
    parts = [f'<p class="goal"><b>الهدف:</b> {E(d.get("goal",""))}</p>']
    parts += [f"<p>{E(p)}</p>" for p in d.get("explain", [])]
    t = d.get("table")
    if t and t.get("rows"):
        parts.append('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{E(h)}</th>" for h in t["headers"]) + "</tr></thead><tbody>" +
                     "".join("<tr>" + "".join(f"<td>{E(str(c))}</td>" for c in r) + "</tr>" for r in t["rows"]) + "</tbody></table></div>")
    if d.get("examples"):
        parts.append("<h2>أمثلة من القرآن الكريم</h2>")
        for ex in d["examples"]:
            b, ok = ayah_block(ex["surah"], ex["ayah"], ex.get("word"), ex.get("note"))
            parts.append(b)
    if d.get("common_mistakes"):
        parts.append('<h2>أخطاء شائعة</h2><ul class="lst">' + "".join(f"<li>{E(x)}</li>" for x in d["common_mistakes"]) + "</ul>")
    if d.get("parent_tips"):
        parts.append('<h2>لولي الأمر: كيف تتابع؟</h2><ul class="lst">' + "".join(f"<li>{E(x)}</li>" for x in d["parent_tips"]) + "</ul>")
    if d.get("plan"):
        parts.append('<h2>خطة الأسبوع</h2><div class="tbl"><table><thead><tr><th>اليوم</th><th>المطلوب</th></tr></thead><tbody>' +
                     "".join(f'<tr><td class="d">{E(p["day"])}</td><td>{E(p["task"])}</td></tr>' for p in d["plan"]) + "</tbody></table></div>")
    if d.get("exercises"):
        parts.append("<h2>تمارين</h2>")
        for ex in d["exercises"]:
            items = "".join(f"<li>{E(i)}</li>" for i in ex.get("items", []))
            ans = "<br>".join(E(a) for a in ex.get("answers", []))
            parts.append(f'<div class="ex"><h3>{E(ex["title"])}</h3><ol>{items}</ol>' +
                         (f'<details><summary>اعرض الإجابات</summary><div class="ans">{ans}</div></details>' if ans else "") + "</div>")
    if d.get("listen"):
        parts.append('<h2>استمع وشاهد</h2><ul class="lst">' + "".join(f"<li>{linkify(x)}</li>" for x in d["listen"]) + "</ul>")
    return "\n".join(parts)

def check_examples(folder):
    """returns list of examples whose word was not found in the ayah"""
    bad = []
    for f in sorted(os.listdir(folder)):
        if f.startswith("lesson") and f.endswith(".json"):
            d = load(os.path.join(folder, f))
            for ex in d.get("examples", []):
                _, ok = highlight(qdata.ayah_text(ex["surah"], ex["ayah"]), ex.get("word", ""))
                if not ok: bad.append((f, ex["surah"], ex["ayah"], ex.get("word")))
    return bad
