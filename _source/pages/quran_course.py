# Quran course (reading, tajweed, memorisation of the whole Quran, parent guide) — runs inside build.py.
# Content: quran/ folder next to build.py (verified Quran data + lesson JSON + generated plan).
# Not on the site until QURAN_PUBLISHED = True (or PREVIEW_ALL_LEVELS=1 for a private preview build).
import os as _qo, sys as _qs
QURAN_PUBLISHED = True
_QDIR = _qo.path.join(_qo.path.dirname(PAGES_DIR), "quran")
if (_qo.environ.get("PREVIEW_ALL_LEVELS") or QURAN_PUBLISHED) and _qo.path.exists(_qo.path.join(_QDIR, "plan", "level1.json")):
    _qs.path.insert(0, _QDIR)
    import qrender as _qr
    _QE = _qr.E
    _Q_CSS = """<style>
.qwrap{direction:rtl;text-align:right;font-family:Cairo,sans-serif}
.qwrap h2{font-family:Cairo,sans-serif;font-weight:800;margin:28px 0 12px}
.qwrap .q{font-family:'Amiri Quran','Amiri',serif;font-size:1.65rem;line-height:2.5;margin:0;color:var(--ink)}
.qwrap .an{font-family:'Amiri Quran',serif;color:var(--gold-2);font-size:1.1rem}
.qwrap mark{background:#fbe3a6;border-radius:6px;padding:0 4px}
.qwrap .ayah{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:10px 0}
.qwrap .ref{display:block;color:var(--muted);font-size:.9rem;margin-top:4px}
.qwrap .enote{margin-top:6px;font-weight:600}
.qwrap .tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}
.qwrap table{border-collapse:collapse;width:100%;min-width:560px}
.qwrap th{background:var(--navy);color:#fff;padding:10px 12px;text-align:right}
.qwrap td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top}
.qwrap td.d{font-weight:800;color:var(--gold-2);white-space:nowrap}
.qwrap .ex{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:12px}
.qwrap .ex ol{margin:0;padding-right:20px}
.qwrap summary{cursor:pointer;font-weight:700;color:var(--gold-2)}
.qwrap .lst li{margin-bottom:6px}
.qwrap .goal{background:#fbf1dc;border-radius:12px;padding:12px 16px}
.qwrap .por{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 18px;margin:8px 0}
.qwrap .por h3{margin:0 0 6px;font-size:1rem;color:var(--gold-2)}
.qwrap .nav{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-top:24px}
.qwrap .nav a{font-weight:700;color:var(--gold-2);text-decoration:none}
.qwrap .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;list-style:none;padding:0}
.qwrap .grid a{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:inherit}
.qwrap .grid a:hover{border-color:var(--gold)}
.qwrap .grid small{display:block;color:var(--muted)}
</style><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri+Quran&display=swap">"""

    def _qpage(fname, title, desc, kicker, h1, sub, inner):
        body = _Q_CSS + pagehead(kicker, h1, sub) + f'<section class="block"><div class="wrap qwrap" dir="rtl" lang="ar">{inner}</div></section>'
        page(fname, title + " | Abdelkriem Academy", desc, body, "quran.html")
        if fname != "quran.html": EXTRA_PAGES.append(fname)

    _RES = _qr.load(_qo.path.join(_QDIR, "RESOURCES.json")) if _qo.path.exists(_qo.path.join(_QDIR, "RESOURCES.json")) else {}

    # ---- lessons (reading + tajweed) ----
    def _lessons(folder, prefix, part_name):
        d = _qo.path.join(_QDIR, folder)
        if not _qo.path.exists(_qo.path.join(d, "meta.json")): return []
        files = sorted([f for f in _qo.listdir(d) if f.startswith("lesson")], key=lambda x: int(x[6:-5]))
        ls = [_qr.load(_qo.path.join(d, f)) for f in files]
        for i, L in enumerate(ls):
            n = L["n"]
            prev = f'<a href="{prefix}-{n-1}.html">→ الدرس {_qr.ar(n-1)}</a>' if i else f'<a href="{prefix}.html">→ صفحة {part_name}</a>'
            nxt = f'<a href="{prefix}-{n+1}.html">الدرس {_qr.ar(n+1)} ←</a>' if i < len(ls) - 1 else f'<a href="quran.html">الكورس ←</a>'
            inner = _qr.lesson_html(L, part_name) + f'<nav class="nav">{prev}{nxt}</nav>'
            _qpage(f"{prefix}-{n}.html", f"{part_name} – الدرس {n}: {L['title']}", f"{part_name}، الدرس {n}: {L['title']} — شرح مبسط بأمثلة من القرآن وتمارين بالإجابات.",
                   f"القرآن الكريم من الألف للياء · {part_name} · الدرس {_qr.ar(n)} من {_qr.ar(len(ls))}", _QE(L["title"]), _QE(L.get("goal", "")), inner)
        m = _qr.load(_qo.path.join(d, "meta.json"))
        lst = "".join(f'<li><a href="{prefix}-{L["n"]}.html"><small>الدرس {_qr.ar(L["n"])}</small>{_QE(L["title"])}</a></li>' for L in ls)
        inner = "".join(f"<p>{_QE(p)}</p>" for p in ([m.get("intro", "")] if isinstance(m.get("intro"), str) else m.get("intro", [])))
        if m.get("how_to_use"): inner += "<h2>طريقة الاستخدام</h2><ul class='lst'>" + "".join(f"<li>{_QE(x)}</li>" for x in m["how_to_use"]) + "</ul>"
        if m.get("can_do"): inner += "<h2>في نهاية هذا الجزء</h2><ul class='lst'>" + "".join(f"<li>{_QE(x)}</li>" for x in m["can_do"]) + "</ul>"
        inner += f"<h2>الدروس</h2><ul class='grid'>{lst}</ul>"
        _qpage(f"{prefix}.html", f"{part_name} — القرآن الكريم من الألف للياء", f"{part_name}: دروس أسبوعية مبسطة لولي الأمر والطفل بأمثلة من القرآن وتمارين.",
               "القرآن الكريم من الألف للياء", _QE(m.get("title", part_name)), "دروس أسبوعية مبسطة بأمثلة من القرآن الكريم وتمارين بالإجابات", inner)
        return ls

    _reading = _lessons("reading", "quran-reading", "التمهيدي: تعلّم القراءة")
    _tajweed = _lessons("tajweed", "quran-tajweed", "أحكام التجويد")

    # ---- memorisation levels ----
    _levels = []
    for _n in range(1, 13):
        _p = _qo.path.join(_QDIR, "plan", f"level{_n}.json")
        if _qo.path.exists(_p): _levels.append(_qr.load(_p))

    def _week_page(lv, w):
        n, k = lv["level"], w["week"]
        rows = "".join(
            f'<tr><td class="d">{_QE(_qr.ar(d["day"]))}</td><td>{_QE(_qr.ar(d["new"]))}<br>' +
            " ".join(f'<a href="{u}" target="_blank" rel="noopener">استمع ←</a>' for u in d["links"]) +
            f'</td><td>{_qr.ar(d["page"])}</td><td>{_QE(_qr.ar(d["recent"] or "—"))}</td><td>{_QE(_qr.ar(d["far"] or "—"))}</td></tr>' for d in w["days"])
        rows += f'<tr><td class="d">اليوم 6</td><td colspan="4">{_QE(_qr.ar(w["day6"]))}</td></tr><tr><td class="d">اليوم 7</td><td colspan="4">{_QE(_qr.ar(w["day7"]))}</td></tr>'
        tbl = f'<div class="tbl"><table><thead><tr><th>اليوم</th><th>الحفظ الجديد</th><th>صفحة المصحف</th><th>المراجعة القريبة</th><th>المراجعة البعيدة</th></tr></thead><tbody>{rows}</tbody></table></div>'
        text = ""
        if n <= 3:
            text = "<h2>نص الحفظ الجديد</h2>" + "".join(f'<div class="por"><h3>{_QE(_qr.ar(d["day"]))}: {_QE(_qr.ar(d["new"]))}</h3>' + "".join(_qr.portion_text(*g) for g in d["parts"]) + "</div>" for d in w["days"])
        taj = ""
        if w.get("tajweed"):
            taj = "<h2>تجويد في حفظ هذا الأسبوع</h2><p>اطلب من ابنك أن يقرأ الكلمة الملوّنة ويطبّق الحكم:</p>" + "".join(_qr.ayah_block(e["surah"], e["ayah"], e["word"], "الحكم: " + e["rule"])[0] for e in w["tajweed"])
        how = ("<h2>طريقة اليوم (20–30 دقيقة)</h2><ol class='lst'><li>استمع للحفظ الجديد بصوت القارئ 3 مرات مع النظر في المصحف.</li>"
               "<li>اقرأ الآية الأولى من المصحف 5 مرات، ثم سمّعها دون نظر 3 مرات، ثم الثانية وهكذا، واربط كل آيتين معًا.</li>"
               "<li>سمّع الحفظ الجديد كاملًا لولي الأمر.</li><li>راجع «المراجعة القريبة» مرة واحدة من الذاكرة.</li><li>راجع «المراجعة البعيدة» مرة واحدة (يمكن أن تكون في وقت آخر من اليوم أو في الصلاة).</li></ol>")
        pre = f"quran-hifz-{n}"
        nw = len(lv["weeks"])
        prev = f'<a href="{pre}-week-{k-1}.html">→ الأسبوع {_qr.ar(k-1)}</a>' if k > 1 else f'<a href="{pre}.html">→ صفحة المستوى</a>'
        nxt = f'<a href="{pre}-week-{k+1}.html">الأسبوع {_qr.ar(k+1)} ←</a>' if k < nw else f'<a href="{pre}-test.html">اختبار المستوى ←</a>'
        inner = tbl + how + text + taj + f'<nav class="nav">{prev}{nxt}</nav>'
        _qpage(f"{pre}-week-{k}.html", f"{lv['title']} – الأسبوع {k}", f"خطة حفظ يومية: {w['title']} — الحفظ الجديد والمراجعة القريبة والبعيدة مع رابط الاستماع.",
               f"القرآن الكريم من الألف للياء · {lv['title']} · الأسبوع {_qr.ar(k)} من {_qr.ar(nw)}", _QE(_qr.ar(w["title"])), "٥ أيام حفظ + يوم تسميع + يوم راحة", inner)

    def _test_page(lv):
        pre = f"quran-hifz-{lv['level']}"
        inner = "<p>اختبار تسميع في نهاية كل جزء. يقرأ ولي الأمر بداية الآية، ويُكمل الطفل ثلاث آيات من حفظه دون النظر في المصحف.</p>"
        for t in lv["tests"]:
            inner += f"<h2>اختبار الجزء {_qr.ar(t['juz'])}</h2>"
            for i, q in enumerate(t["questions"], 1):
                inner += f'<div class="ayah"><b>السؤال {_qr.ar(i)}:</b> {_QE(_qr.ar(q["ask"]))}<p class="q" lang="ar">{_QE(q["start"])} …</p></div>'
            inner += "<h3>طريقة التصحيح</h3><ul class='lst'>" + "".join(f"<li>{_QE(r)}</li>" for r in t["rubric"]) + "</ul>"
        inner += f'<nav class="nav"><a href="{pre}.html">→ صفحة المستوى</a>' + (f'<a href="quran-hifz-{lv["level"]+1}.html">المستوى التالي ←</a>' if lv["level"] < 12 else '<a href="quran.html">الكورس ←</a>') + "</nav>"
        _qpage(f"{pre}-test.html", f"{lv['title']} – اختبار التسميع", f"اختبار تسميع {lv['title']} مع طريقة التصحيح.", f"القرآن الكريم من الألف للياء · {lv['title']}", "اختبار التسميع", "١٠ أسئلة لكل جزء · من ٢٠ درجة", inner)

    for _lv in _levels:
        for _w in _lv["weeks"]: _week_page(_lv, _w)
        _test_page(_lv)
        _pre = f"quran-hifz-{_lv['level']}"
        _lst = "".join(f'<li><a href="{_pre}-week-{w["week"]}.html"><small>الأسبوع {_qr.ar(w["week"])}</small>{_QE(_qr.ar(w["title"]))}</a></li>' for w in _lv["weeks"])
        _pdf = f"files/Quran-Hifz-Level-{_lv['level']}.pdf"
        _inner = (f"<p><b>المقدار اليومي:</b> {_QE(_lv['pace'])}. خمسة أيام حفظ، ويوم تسميع، ويوم راحة واستماع. كل يوم: حفظ جديد + مراجعة قريبة (آخر ٥ أيام) + مراجعة بعيدة (من الحفظ القديم بالتناوب).</p>"
                  f"<p>أرقام الصفحات حسب مصحف المدينة النبوية (٦٠٤ صفحة) برواية حفص عن عاصم.</p>"
                  f'<p><a class="btn" href="{_pre}-week-1.html">ابدأ الأسبوع الأول</a></p>'
                  f"<h2>أسابيع المستوى</h2><ul class='grid'>{_lst}<li><a href='{_pre}-test.html'><small>بعد كل جزء</small>اختبار التسميع</a></li></ul>")
        _qpage(f"{_pre}.html", f"{_lv['title']} — حفظ القرآن الكريم", f"خطة حفظ {_lv['title']}: {len(_lv['weeks'])} أسبوعًا مع المراجعة اليومية واختبار التسميع.",
               "القرآن الكريم من الألف للياء · الحفظ", _QE(_lv["title"]), f"{_qr.ar(len(_lv['weeks']))} أسبوعًا · {_QE(_lv['pace'])}", _inner)

    # ---- parent guide ----
    _gp = _qo.path.join(_QDIR, "guide.json")
    if _qo.path.exists(_gp):
        _g = _qr.load(_gp)
        _inner = ""
        for _s in _g["sections"]:
            _inner += f"<h2>{_QE(_s['title'])}</h2>" + "".join(f"<p>{_QE(p)}</p>" for p in _s.get("paragraphs", []))
            if _s.get("bullets"): _inner += "<ul class='lst'>" + "".join(f"<li>{_QE(b)}</li>" for b in _s["bullets"]) + "</ul>"
        _qpage("quran-guide.html", "دليل ولي الأمر لتحفيظ القرآن", "دليل عملي مبسط لولي الأمر: كيف يحفّظ ابنه القرآن ويراجع معه ويسمّع له ويحفّزه.",
               "القرآن الكريم من الألف للياء", _QE(_g.get("title", "دليل ولي الأمر")), "كيف تحفّظ ابنك القرآن خطوة بخطوة", _inner)

    # ---- resources + hub ----
    _rhtml = ""
    for _r in _RES.get("reciters", []):
        _rhtml += f'<li><a href="{_QE(_r["url"])}" target="_blank" rel="noopener">{_QE(_r["name"])}</a> — {_QE(_r.get("note",""))}</li>'
    for _key in ("tajweed_videos", "reading_videos"):
        _v = _RES.get(_key) or {}
        if _v.get("url"): _rhtml += f'<li><a href="{_QE(_v["url"])}" target="_blank" rel="noopener">{_QE(_v.get("series",""))}</a> — {_QE(_v.get("presenter",""))}</li>'
    for _r in _RES.get("mushaf_tools", []):
        _rhtml += f'<li><a href="{_QE(_r["url"])}" target="_blank" rel="noopener">{_QE(_r["name"])}</a> — {_QE(_r.get("note",""))}</li>'
    _lv_list = "".join(f'<li><a href="quran-hifz-{l["level"]}.html"><small>{_qr.ar(len(l["weeks"]))} أسبوعًا</small>{_QE(l["title"])}</a></li>' for l in _levels)
    _hub = ("<p>كورس مجاني كامل لتعليم القرآن الكريم للأطفال والكبار: من تعلّم الحروف، إلى أحكام التجويد، إلى حفظ القرآن كاملًا بخطة يومية واضحة يتابعها ولي الأمر في البيت.</p>"
            "<h2>ابدأ من هنا</h2><ul class='grid'>"
            "<li><a href='quran-guide.html'><small>اقرأه أولًا</small>دليل ولي الأمر</a></li>"
            + (f"<li><a href='quran-reading.html'><small>{_qr.ar(len(_reading))} درسًا</small>التمهيدي: تعلّم القراءة</a></li>" if _reading else "")
            + (f"<li><a href='quran-tajweed.html'><small>{_qr.ar(len(_tajweed))} درسًا</small>أحكام التجويد من الألف للياء</a></li>" if _tajweed else "")
            + "</ul><h2>مستويات الحفظ (القرآن كاملًا)</h2>"
            f"<p>نبدأ بجزء عمّ ثم تبارك ثم قد سمع، ثم باقي القرآن ثلاثة أجزاء في كل مستوى حتى سورة البقرة.</p><ul class='grid'>{_lv_list}</ul>"
            + (f"<h2>مصادر الاستماع والتعلّم</h2><ul class='lst'>{_rhtml}</ul>" if _rhtml else ""))
    _qpage("quran.html", "القرآن الكريم من الألف للياء: قراءة وتجويد وحفظ", "كورس قرآن مجاني للأطفال وأولياء الأمور: تعلّم القراءة، أحكام التجويد، وخطة حفظ القرآن كاملًا مع المراجعة.",
           "كورس مجاني · لولي الأمر والطفل", "القرآن الكريم من الألف للياء", "قراءة · تجويد · حفظ القرآن كاملًا بخطة يومية", _hub)
