#!/usr/bin/env python3
"""Generate the memorisation plan (levels, weeks, daily portions, reviews, juz tests) from verified Quran data.
Output: plan/level1.json … plan/level12.json"""
import sys, os, json, re, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import qdata

FIX = {"النبإ": "النبأ"}
def sname(s):
    n = re.sub(r'[ً-ْٰۡ۟-ۭ]', '', qdata.SURAH_AR[s-1]).replace('سورة ', '').replace('ٱ', 'ا').strip()
    return FIX.get(n, n)

def L(s): return len(qdata.ayah_text(s, 0 + 1)) if False else None

def ayah_len(s, a): return len(qdata.ayah_text(s, a))
def page(s, a): return qdata.meta(s, a)['page']
def juz(s, a): return qdata.meta(s, a)['juz']

def label(p):  # portion = (s, a1, a2)
    s, a1, a2 = p
    full = a1 == 1 and a2 == qdata.nayahs(s)
    return f"سورة {sname(s)} كاملة ({a1}–{a2})" if full else f"سورة {sname(s)} ({a1}–{a2})"

def chunk_surah(s, target, a_from=1, a_to=None):
    a_to = a_to or qdata.nayahs(s)
    out, start, size = [], a_from, 0
    for a in range(a_from, a_to + 1):
        size += ayah_len(s, a)
        if size >= target and a < a_to:
            out.append((s, start, a)); start, size = a + 1, 0
    out.append((s, start, a_to))
    # merge a tiny tail into previous chunk
    if len(out) > 1 and sum(ayah_len(s, a) for a in range(out[-1][1], out[-1][2] + 1)) < target * 0.35:
        last = out.pop(); prev = out.pop(); out.append((s, prev[1], last[2]))
    return out

def portions_by_surah(surahs, target):
    res = []
    for s in surahs:
        res += chunk_surah(s, target)
    return res

def portions_by_page(juz_no):
    pages = {}
    for s in range(1, 115):
        for a in range(1, qdata.nayahs(s) + 1):
            if juz(s, a) == juz_no:
                pages.setdefault(page(s, a), []).append((s, a))
    res = []
    for p in sorted(pages):
        items = pages[p]
        # split a page that spans two surahs into separate labels but keep one day
        groups = []
        for s, a in items:
            if groups and groups[-1][0] == s and groups[-1][2] == a - 1:
                groups[-1] = (s, groups[-1][1], a)
            else:
                groups.append((s, a, a))
        res.append({"page": p, "parts": groups})
    return res

def span(a, b):
    s1, a1 = a[0], a[1]; s2, a2 = b[0], b[2]
    if s1 == s2: return label((s1, a1, a2))
    return f"من سورة {sname(s1)} آية {a1} إلى سورة {sname(s2)} آية {a2}"
def fmt_parts(parts): return " + ".join(label(g) for g in parts)
def qlink(g): s, a1, a2 = g; return f"https://quran.com/{s}/{a1}-{a2}" if not (a1 == 1 and a2 == qdata.nayahs(s)) else f"https://quran.com/{s}"

TAJ_TOPIC = {"f": "الإخفاء الحقيقي", "a": "الإدغام بغنة", "u": "الإدغام بغير غنة", "i": "الإقلاب", "c": "الإخفاء الشفوي", "w": "الإدغام الشفوي",
             "g": "الغنة (النون والميم المشددتان)", "q": "القلقلة", "l": "اللام الشمسية", "o": "المد المتصل", "m": "المد اللازم", "d": "إدغام المتجانسين"}

def tajweed_examples(parts, used, k=3):
    ex = []
    for code in random.Random(sum(g[0] * 1000 + g[1] for g in parts)).sample(list(TAJ_TOPIC), len(TAJ_TOPIC)):
        if code in used: continue
        for (s, a1, a2) in parts:
            for a in range(a1, a2 + 1):
                for c, w, n in qdata.tajweed_marks(s, a):
                    if c == code:
                        ex.append({"rule": TAJ_TOPIC[code], "code": code, "surah": s, "ayah": a, "word": w}); break
                if len(ex) and ex[-1]["code"] == code: break
            if len(ex) and ex[-1]["code"] == code: break
        if len(ex) >= k: break
    return ex

def build_level(n, title, days, review_unit, prior=()):
    prior = list(prior); state = {"far_ptr": 0}
    """days: list of dicts with key parts (list of (s,a1,a2)) and optional page; returns level json with weeks of 5 new days."""
    weeks, done_parts = [], []
    old_pool = []          # completed portions before this level (labels) for far review
    for i in range(0, len(days), 5):
        wk_days = days[i:i + 5]
        week = {"week": len(weeks) + 1, "days": []}
        used = set()
        for j, d in enumerate(wk_days):
            parts = d["parts"]
            recent = done_parts[-5:]
            far = None
            pool = prior + done_parts[:-5]
            if len(pool) >= 2:
                blocks, cur, sz = [], [], 0
                for pp in pool:
                    cur.append(pp); sz += sum(ayah_len(g[0], a) for g in pp for a in range(g[1], g[2] + 1))
                    if sz >= review_unit: blocks.append(cur); cur, sz = [], 0
                if cur: blocks.append(cur)
                blk = blocks[state["far_ptr"] % len(blocks)]; state["far_ptr"] += 1
                far = span(blk[0][0], blk[-1][-1])
            rec = None
            if recent:
                rec = span(recent[0][0], recent[-1][-1])
            week["days"].append({"day": f"اليوم {j + 1}", "new": fmt_parts(parts), "page": d.get("page") or page(parts[0][0], parts[0][1]),
                                 "links": [qlink(g) for g in parts], "parts": parts, "recent": rec, "far": far})
            done_parts.append(parts)
        allp = [g for d in wk_days for g in d["parts"]]
        week["title"] = "، ".join(dict.fromkeys(f"سورة {sname(g[0])}" for g in allp))
        week["day6"] = "تسميع كل حفظ الأسبوع لولي الأمر مرة واحدة دون النظر في المصحف + تصحيح الأخطاء وتكرار مواضعها 3 مرات."
        week["day7"] = "راحة: استماع لحفظ الأسبوع بصوت القارئ مرتين (في السيارة أو قبل النوم)."
        week["tajweed"] = tajweed_examples(allp, used)
        weeks.append(week)
    return {"level": n, "title": title, "weeks": weeks}

def juz_test(juz_no, seed):
    ay = [(s, a) for s in range(1, 115) for a in range(1, qdata.nayahs(s) + 1) if juz(s, a) == juz_no]
    rnd = random.Random(seed)
    step = len(ay) // 10
    qs = []
    for k in range(10):
        s, a = ay[min(len(ay) - 1, k * step + rnd.randrange(max(1, step)))]
        if a == qdata.nayahs(s) and a > 1: a -= 1
        words = qdata.ayah_text(s, a).split()
        qs.append({"surah": s, "ayah": a, "start": " ".join(words[:min(4, len(words))]), "ask": (f"أكمل من سورة {sname(s)} الآية {a} ثلاث آيات" if qdata.nayahs(s) - a >= 2 else f"أكمل من سورة {sname(s)} الآية {a} إلى نهاية السورة")})
    return {"juz": juz_no, "questions": qs,
            "rubric": ["لكل سؤال درجتان: بدون خطأ = 2، خطأ واحد صحّحه بنفسه = 1.5، خطأ نبّهته عليه = 1، أكثر من خطأ أو توقف طويل = 0.5",
                       "الدرجة من 20: 18 فأكثر ممتاز ← انتقل للجزء التالي · 15–17 جيد جدًا ← راجع مواضع الخطأ أسبوعًا مع الحفظ الجديد · أقل من 15 ← أسبوعان مراجعة فقط ثم أعد الاختبار"]}

def main():
    os.makedirs(os.path.join(HERE, "plan"), exist_ok=True)
    avg_page = 1184
    levels = []
    # Level 1: Juz 30, surahs An-Nas -> An-Naba, ~0.3 page per day
    j30 = list(range(114, 77, -1))
    days = [{"parts": [p]} for p in portions_by_surah(j30, avg_page * 0.3)]
    levels.append((1, "المستوى الأول: جزء عمّ (الجزء ٣٠)", days, 1200, [30]))
    j29 = list(range(77, 66, -1)); days = [{"parts": [p]} for p in portions_by_surah(j29, avg_page * 0.5)]
    levels.append((2, "المستوى الثاني: جزء تبارك (الجزء ٢٩)", days, 2400, [29]))
    j28 = list(range(66, 57, -1)); days = [{"parts": [p]} for p in portions_by_surah(j28, avg_page * 0.5)]
    levels.append((3, "المستوى الثالث: جزء قد سمع (الجزء ٢٨)", days, 2400, [28]))
    groups = [(27, 26, 25), (24, 23, 22), (21, 20, 19), (18, 17, 16), (15, 14, 13), (12, 11, 10), (9, 8, 7), (6, 5, 4), (3, 2, 1)]
    names = ["الرابع", "الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]
    for k, g in enumerate(groups):
        days = []
        for jz in g:
            days += [{"parts": d["parts"], "page": d["page"], "juz": jz} for d in portions_by_page(jz)]
        levels.append((4 + k, f"المستوى {names[k]}: الأجزاء من {str(g[0]).translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))} إلى {str(g[2]).translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))}", days, 6000, list(g)))
    summary = []; prior = []
    for n, title, days, unit, juzs in levels:
        lv = build_level(n, title, days, unit, prior)
        prior = prior + [d["parts"] for d in days]
        lv["juz"] = juzs
        lv["pace"] = "نحو ثلث صفحة يوميًا (مناسب للأطفال 5–9 سنوات)" if n == 1 else ("نصف صفحة يوميًا" if n <= 3 else "صفحة واحدة يوميًا (للأكبر سنًا؛ الأصغر: نصف صفحة ويتضاعف عدد الأسابيع)")
        lv["tests"] = [juz_test(j, n * 100 + j) for j in juzs]
        json.dump(lv, open(os.path.join(HERE, "plan", f"level{n}.json"), "w"), ensure_ascii=False)
        summary.append((n, title, len(lv["weeks"]), len(days)))
    for s in summary: print(s)

if __name__ == "__main__":
    main()
