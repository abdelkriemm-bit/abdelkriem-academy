# Quran course: "start here" page (how to use the site + tajweed order by age) and a practice + quiz on every tajweed lesson.
# Runs after quran_course.py. Data: quran/tajweed_quiz/lessonN.json · engine: quran/tj_quiz.js
import os as _zo, json as _zj
_ZQ = _zo.path.join(_zo.path.dirname(PAGES_DIR), "quran")
if (_zo.environ.get("PREVIEW_ALL_LEVELS") or QURAN_PUBLISHED) and "_qpage" in globals():
    _ZJS = open(_zo.path.join(_ZQ, "tj_quiz.js"), encoding="utf-8").read()
    _ZCSS = """<style>
.qwrap .tq{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:0 0 12px}
.qwrap .tq .qq{margin:6px 0}.qwrap .tops{display:flex;flex-wrap:wrap;gap:8px}
.qwrap .opt{font-family:Cairo;font-weight:700;border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 16px;cursor:pointer;font-size:1rem}
.qwrap .opt:hover{border-color:var(--gold)}.qwrap .opt.sel{background:var(--navy);color:#fff}
.qwrap .opt.right{background:#c9efd3;border-color:#2e7d32;color:#123}.qwrap .opt.wrong{background:#f6c9c9;border-color:#c62828;color:#123}
.qwrap .fb p{margin:10px 0 4px;line-height:1.9}.qwrap .tqbar{position:sticky;top:64px;background:var(--paper);padding:6px 0;z-index:3;margin:0}
.qwrap .qbox{border-radius:14px;padding:14px 18px;margin:12px 0}.qwrap .qbox.ok{background:#e3f4e7}.qwrap .qbox.no{background:#fde7e7}
.qwrap .warn{color:#b3261e}.qwrap .stepper{counter-reset:s;list-style:none;padding:0}
.qwrap .stepper li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 16px 12px 16px;margin:0 0 10px;position:relative;padding-right:58px}
.qwrap .stepper li:before{content:counter(s);position:absolute;right:14px;top:12px;width:32px;height:32px;border-radius:50%;background:var(--gold);color:var(--navy);font-weight:800;display:flex;align-items:center;justify-content:center}
.qwrap .howbox{background:#fbf1dc;border-radius:14px;padding:12px 18px;margin:0 0 18px}
</style>"""

    _n_ls = len(_tajweed) if "_tajweed" in globals() else 16
    _titles = {L["n"]: L["title"] for L in (_tajweed if "_tajweed" in globals() else [])}
    def _tl(n):
        return f'<a href="quran-tajweed-{n}.html">الدرس {_qr.ar(n)}: {_QE(_titles.get(n, ""))}</a>'

    # ---- 1) start-here page ----
    _st = (_ZCSS + "<p>تشرح هذه الصفحة كيف تستخدم الكورس خطوة بخطوة، وبماذا تبدأ مع ابنك أو ابنتك، وما الأحكام التي نؤجلها حتى يكبر الطفل.</p>"
           "<h2>كيف تستخدم الموقع؟</h2><ol class='stepper'>"
           "<li><b>اقرأ دليل ولي الأمر أولًا.</b> فيه متى تبدأ، وكيف تجهّز ابنك، وكيف تسمّع له وتصحّح بلطف. <a href='quran-guide.html'>افتح الدليل ←</a></li>"
           "<li><b>إذا كان الطفل لا يقرأ بعد:</b> ابدأ بالتمهيدي (الحروف والحركات)، وفي الوقت نفسه اجعله يستمع إلى السور القصيرة ويردّدها. <a href='quran-reading.html'>التمهيدي ←</a></li>"
           "<li><b>أحكام التجويد: درس كل أسبوع،</b> وكل درس يسير هكذا: "
           "(1) اقرأ الشرح مع ابنك واستمعا إلى الأمثلة من الشيخ. (2) <b>التدريب</b> في آخر الدرس: أسئلة اختيار من متعدد، وبعد كل إجابة يظهر السبب وزر للاستماع إلى الآية والترديد خلف الشيخ، ويمكن إعادته أكثر من مرة. "
           "(3) <b>اختبار الدرس</b>: 10 أسئلة تُصحَّح في النهاية، ويحتاج الطفل 8 من 10 لينتقل إلى الدرس التالي. (4) <b>التطبيق في القراءة:</b> افتح السورة التي يحفظها، واستخرجا الحكم منها، ثم يقرؤه قراءة صحيحة.</li>"
           "<li><b>الحفظ والتجويد معًا:</b> ابدأ مستويات الحفظ من جزء عمّ، وفي كل أسبوع خطة يومية: حفظ جديد ومراجعة قريبة ومراجعة بعيدة، مع زر «استمع وردّد» وزر «اعرض ألوان التجويد». <a href='quran-hifz-1.html'>المستوى الأول ←</a></li>"
           "<li><b>للمراجعة في أي وقت:</b> <a href='quran-tajweed-guide.html'>كل الأحكام في صفحة واحدة</a>، و<a href='quran-tajweed-practice.html'>تدريب عام على كل الأحكام</a>.</li></ol>"
           "<h2>بأي الأحكام نبدأ؟ (حسب السن)</h2>"
           "<p>القاعدة الذهبية: <b>النطق الصحيح قبل اسم الحكم.</b> الطفل الصغير يتعلّم التجويد بالسماع والتقليد، وتأتي أسماء الأحكام وتقسيماتها بعد ذلك. هذا ترتيب ننصح به، ولكل طفل سرعته.</p>"
           "<div class='tbl'><table><thead><tr><th>السن</th><th>ماذا يتعلّم؟</th><th>من الكورس</th></tr></thead><tbody>"
           "<tr><td class='d'>من ٣ إلى ٦ سنوات</td><td>السماع والترديد فقط، بلا أسماء أحكام: يقلّد الشيخ في الغنة والمد الطبيعي والقلقلة، ويتعلّم الاستعاذة والبسملة وآداب التلاوة. وعندما يبدأ القراءة يتعلّم الحروف والحركات.</td><td><a href='quran-reading.html'>التمهيدي</a>، و" + _tl(1) + " (شفهي)، ومستوى الحفظ الأول بالسماع</td></tr>"
           "<tr><td class='d'>من ٧ إلى ٩ سنوات</td><td>أسماء الأحكام السهلة التي تتكرر كثيرًا في جزء عمّ، حكم واحد كل أسبوع: الاستعاذة والبسملة، والمخارج المبسطة، والتفخيم والترقيق والقلقلة، وأحكام النون الساكنة والتنوين، والميم الساكنة، والغنة، واللام الشمسية والقمرية، والمد الطبيعي.</td><td>الدروس من ١ إلى ٩، والدرس ١١</td></tr>"
           "<tr><td class='d'>من ١٠ إلى ١٢ سنة</td><td>الأحكام التي تحتاج تركيزًا أكثر: الراء، والمد المتصل والمنفصل، والمد العارض واللين والبدل، والمد اللازم والحروف المقطعة، والوقف والابتداء.</td><td>الدروس ١٠ و١٢ و١٣ و١٤ و١٦</td></tr>"
           "<tr><td class='d'>من ١٣ سنة والكبار</td><td>الإدغام بين المتماثلين والمتجانسين والمتقاربين، وهمزة الوصل، ومراجعة شاملة لكل الأحكام.</td><td>الدرس ١٥، ثم مراجعة الدروس كلها</td></tr>"
           "</tbody></table></div>"
           "<h2>ما الذي يثقل على الطفل الصغير؟</h2><ul class='lst'>"
           "<li><b>حفظ التعريفات والتقسيمات</b> (زي «الإخفاء لغةً واصطلاحًا» أو متون التجويد): اتركها للكبار. يكفي الصغير أن يعرف «ماذا نفعل» ويطبّقه.</li>"
           "<li><b>عدّ الحركات بدقة</b> في المدود الطويلة (4 أو 5 أو 6 حركات): يتعلّمها الصغير بتقليد الشيخ، لا بالعدّ.</li>"
           "<li><b>تفاصيل أحوال الراء</b>، و<b>إدغام المتجانسين والمتقاربين</b>، و<b>تفاصيل الحروف المقطعة</b>: هذه للمرحلة الأكبر.</li>"
           "<li><b>الكثير في وقت واحد:</b> حكم واحد في الأسبوع، و10 إلى 15 دقيقة يوميًا تكفي الصغار. لا تنتقل إلى حكم جديد قبل أن يطبّق الطفل ما قبله في قراءته.</li>"
           "<li><b>الضغط والتصحيح القاسي:</b> صحّح بلطف وشجّع، حتى يحب الطفل الجلسة ويستمر.</li></ul>"
           "<p class='howbox'>التجويد يُتعلَّم بالسماع والتلقّي؛ فإذا تيسّر لابنك معلّم يقرأ عليه فهذا أفضل، وهذا الكورس يساعدك على متابعته في البيت.</p>"
           "<p><a class='btn' href='quran-tajweed-1.html'>ابدأ الدرس الأول</a> <a class='btn ghost' href='quran.html'>صفحة الكورس</a></p>")
    _qpage("quran-start-here.html", "ابدأ من هنا: طريقة استخدام كورس القرآن وترتيب أحكام التجويد حسب السن",
           "كيف تستخدم كورس القرآن المجاني مع ابنك: بأي أحكام التجويد نبدأ حسب السن، وما الذي نؤجله، وكيف تستخدم التدريب والاختبار في كل درس.",
           "القرآن الكريم من الألف للياء · ابدأ من هنا", "ابدأ من هنا: كيف تستخدم الكورس؟", "طريقة الاستخدام، وترتيب أحكام التجويد حسب سن الطفل", _st)

    # ---- 2) practice + quiz on every tajweed lesson ----
    _made = 0
    for _n in range(1, _n_ls + 1):
        _fp = _zo.path.join(_ZQ, "tajweed_quiz", f"lesson{_n}.json")
        _pp = _zo.path.join(OUT, f"quran-tajweed-{_n}.html")
        if not (_zo.path.exists(_fp) and _zo.path.exists(_pp)): continue
        _d = _qr.load(_fp)
        def _conv(q):
            o = {"q": _QE(q["q"]), "c": [_QE(x) for x in q["c"]], "a": q["a"], "e": _QE(q["e"])}
            if q.get("s"):
                h, ok = _qr.highlight(_qr.qdata.ayah_text(q["s"], q["ay"]), q["w"])
                o.update({"h": h, "s": q["s"], "ay": q["ay"], "ref": f"سورة {_qr.sname(q['s'])} – الآية {_qr.ar(q['ay'])}"})
            return o
        _data = {"n": _n, "practice": [_conv(q) for q in _d["practice"]], "quiz": [_conv(q) for q in _d["quiz"]],
                 "next": f"quran-tajweed-{_n+1}.html" if _n < _n_ls else "quran-hifz-1.html"}
        _sec = (_ZCSS + "<h2 id='practice'>تدريب على الدرس</h2>"
                "<p class='howbox'>أجب عن كل سؤال، وستعرف فورًا الإجابة الصحيحة وسببها. في الأسئلة التي فيها آية اضغط «استمع» واستمع إلى الشيخ الحصري وردّد خلفه. هذا التدريب للمذاكرة، فأعده كما تشاء.</p>"
                "<div id='tj-practice'></div>"
                "<h2 id='quiz'>اختبار الدرس</h2><p class='howbox'>10 أسئلة. أجب عنها كلها ثم اضغط «صحّح الاختبار». إذا حصلت على 8 من 10 أو أكثر فقد أتقنت الحكم، وتستطيع الانتقال إلى الدرس التالي.</p>"
                "<div id='tj-quiz'></div>"
                f"<script type='application/json' id='tj-data'>{_zj.dumps(_data, ensure_ascii=False).replace('</', '<' + chr(92) + '/')}</script><script>{_ZJS}</script>")
        _h = open(_pp, encoding="utf-8").read()
        _k = _h.rfind('<nav class="nav">')
        if _k > 0 and "tj-practice" not in _h:
            _jump = "<p class='howbox'>بعد مذاكرة الدرس: <a href='#practice'>التدريب ↓</a> ثم <a href='#quiz'>اختبار الدرس ↓</a></p>"
            _h = _h[:_k] + _sec + _h[_k:]
            _g = _h.find("<h2")  # jump links near the top of the lesson
            _w = _h.find('class="wrap qwrap')
            _w = _h.find(">", _w) + 1
            _h = _h[:_w] + _jump + _h[_w:]
            open(_pp, "w", encoding="utf-8").write(_h); _made += 1
    print("tajweed practice+quiz pages:", _made)

    # ---- 3) "start here" box on the Quran hub and tajweed hub ----
    _box = ("<div class='howbox'><b>أول مرة هنا؟</b> اقرأ <a href='quran-start-here.html'>«ابدأ من هنا»</a>: كيف تستخدم الكورس، وبأي الأحكام نبدأ حسب سن ابنك، "
            "وأن كل درس تجويد فيه شرح، ثم تدريب، ثم اختبار قصير لتطمئن أنه أتقن الحكم، ثم يطبّقه في القراءة.</div>")
    for _f in ("quran-tajweed.html",):
        _pp = _zo.path.join(OUT, _f)
        if _zo.path.exists(_pp):
            _h = open(_pp, encoding="utf-8").read()
            if "quran-start-here.html'>«ابدأ" not in _h:
                _w = _h.find('class="wrap qwrap'); _w = _h.find(">", _w) + 1
                open(_pp, "w", encoding="utf-8").write(_h[:_w] + _ZCSS + _box + _h[_w:])
    _pp = _zo.path.join(OUT, "quran.html")
    _h = open(_pp, encoding="utf-8").read()
    _h = _h.replace("<li><a href='quran-guide.html'><small>اقرأه أولًا</small>دليل ولي الأمر</a></li>",
                    "<li><a href='quran-start-here.html'><small>اقرأه أولًا</small>ابدأ من هنا: طريقة الاستخدام</a></li><li><a href='quran-guide.html'><small>اقرأه أولًا</small>دليل ولي الأمر</a></li>", 1)
    open(_pp, "w", encoding="utf-8").write(_h)

    for _f in ("quran-start-here.html",):
        _pp = _zo.path.join(OUT, _f)
        _h = open(_pp, encoding="utf-8").read()
        if 'content="notranslate"' not in _h:
            _h = _h.replace("<head>", '<head>\n<meta name="google" content="notranslate">', 1).replace('<section class="phead">', '<section class="phead notranslate" translate="no" dir="rtl" lang="ar">', 1)
            open(_pp, "w", encoding="utf-8").write(_h)
