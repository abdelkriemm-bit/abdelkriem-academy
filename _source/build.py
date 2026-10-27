import os, html
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abdelkriem-academy")
os.makedirs(OUT + "/images", exist_ok=True)
YT = "https://www.youtube.com/@mr.mohamedabdelkriem"
PL = {
 "bac": "PLcAEKD1OcKI0", "writing": "PLYR70OePGs18",
 "checkpoint": "PLZn-QO9NSjZTrZb7fMRL7anhccpJmdnlR", "lit": "PLbtVCSg0ED3s",
 "parents": "PLZn-QO9NSjZSQsQLpm2O2QVnymKTOJ-hD", "tips": "PLZn-QO9NSjZQhhfkg0HBadGcs9Kfn0IRv",
 "ielts": "PLZn-QO9NSjZSuQZSRDvkmDOOnINQqF56t", "situations": "PLZn-QO9NSjZTVogFkUdSRhjTNpm7PjPLX",
}
NAV = [("index.html","Home","الرئيسية"),("british.html","British &amp; IGCSE",""),("american.html","American Diploma",""),("egyptian-baccalaureate.html","Egyptian Baccalaureate","SUB:البكالوريا المصرية"),
       ("quran.html","Quran · حفظ قرآن",""),("improve-english.html","English from Zero","SUB:إنجليزي من الصفر"),("about.html","About","")]

def head(title, desc, rtl=False):
    d = 'dir="rtl" lang="ar"' if rtl else 'lang="en"'
    return f'''<!doctype html>
<html {d}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="images/mohamed-abdelkriem.jpg">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=20261026a">
<meta name="google-adsense-account" content="ca-pub-8885402561273130">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8885402561273130" crossorigin="anonymous"></script>
</head>
<body>
'''

def header(active):
    def _nl(h,n,x):
        cls=(["two"] if x.startswith("SUB:") else [])+(["on"] if h==active else [])
        c=f' class="{" ".join(cls)}"' if cls else ""
        inner=f'<span>{n}</span><small lang="ar">{x[4:]}</small>' if x.startswith("SUB:") else n
        return f'<a href="{h}"{c}>{inner}</a>'
    links = "".join(_nl(h,n,x) for h,n,x in NAV)
    return f'''<header class="top"><div class="wrap bar">
<a class="brand" href="index.html"><span class="mark">AA</span><span><b>Abdelkriem Academy</b><small>Educate Me Up</small></span></a>
<button class="menu" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')">☰</button>
<nav dir="ltr">{links}</nav></div></header>
'''

FOOT = f'''<footer class="foot" dir="ltr"><div class="wrap fgrid">
<div><b>Abdelkriem Academy</b><p>Free educational resources for students and parents — Cambridge and Oxford English, the Egyptian Baccalaureate, Quran and more — by Mohamed Abdelkriem.</p></div>
<div><b>Sections</b><a href="british.html">British &amp; IGCSE</a><a href="american.html">American Diploma · SAT · ACT · EST</a><a href="egyptian-baccalaureate.html">Egyptian Baccalaureate · البكالوريا المصرية</a><a href="quran.html">Quran · حفظ القرآن</a><a href="improve-english.html">English · من الصفر للاحتراف</a></div>
<div><b>Academy</b><a href="about.html">About</a><a href="contact.html">Contact</a><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Use</a></div>
<div><b>Follow</b><a href="{YT}" target="_blank" rel="noopener">YouTube</a><a href="https://www.facebook.com/" target="_blank" rel="noopener">Facebook</a><a href="https://www.tiktok.com/" target="_blank" rel="noopener">TikTok</a></div>
</div><p class="copy">© 2026 Abdelkriem Academy · No English exam left standing.</p></footer>
</body></html>'''

def page(fname, title, desc, body, active=None, rtl=False):
    with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f:
        f.write(head(title, desc, rtl) + header(active or fname) + "<main>" + body + "</main>" + FOOT)

def yt(pl, label="Watch the playlist"):
    return f'<div class="video"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/videoseries?list={pl}" title="{label}" allowfullscreen></iframe></div>'

def soon(t="Resources coming soon"):
    return f'<span class="soon">{t}</span>'

def card(title, text, href=None, tag=None):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    inner = f'{t}<h3>{title}</h3><p>{text}</p>'
    return f'<a class="card" href="{href}">{inner}<span class="go">Open →</span></a>' if href else f'<div class="card">{inner}</div>'

def pagehead(kicker, title, sub):
    return f'<section class="phead"><div class="wrap"><p class="kicker">{kicker}</p><h1>{title}</h1><p class="lead">{sub}</p></div></section>'

# ---------- HOME ----------
COURSES = [
 ("English Course: From Zero","Beginner English in 12 weeks, 30 minutes a day, with Arabic explanations — words, sentences, grammar and exercises with answers.","english-in-90-days.html","طوّر الإنجليزي من الصفر"),
 ("Egyptian Baccalaureate: English","تانية بكالوريا English — 92 lessons covering the whole Ministry curriculum, explained in simple English and Arabic: grammar, vocabulary, reading, listening, speaking, writing and The Lost World chapter by chapter.","baccalaureate.html","البكالوريا المصرية"),
 ("Checkpoint 8 English","48 lessons: every grammar, punctuation and reading topic, plus a writing pack for every fiction and non-fiction genre with strong 350+ word samples.","checkpoint-8.html","Cambridge 0861"),
 ("Checkpoint 6 English","43 lessons for Year 6: grammar, punctuation and reading skills, and a writing pack for every fiction and non-fiction genre with model samples.","checkpoint-6.html","Cambridge Primary 0058"),
 ("IGCSE English 0510","The complete course: the exam explained, Exercises 1-6 step by step, a pack for every writing genre, listening and speaking, with full-mark models.","year-9-0510.html","Cambridge IGCSE"),
 ("Oxford International GCSE","The complete 9280 course: reading question types, every writing task from the picture to the article, listening and speaking with model answers.","year-10-oxford.html","OxfordAQA 9280"),
("American Diploma: SAT · ACT · EST","Complete English courses for the Digital SAT Reading and Writing, ACT English and Reading, and the EST Literacy tests, with full timed practice tests.","american.html","SAT · ACT · EST"),
 ("Quran: Reading, Tajweed &amp; Memorisation","A complete free Quran course for children and parents: learning to read, all the tajweed rules, and a daily plan to memorise the whole Quran.","quran.html","القرآن الكريم من الألف للياء"),
 ("English: From Zero to Pro","A complete free English course in 5 levels, from your first word to fluent English, with Arabic explanations.","improve-english.html","إنجليزي من الصفر للاحتراف"),
]
PARENTS = [
 ("Choosing a school system","IGCSE, American, National or the new Baccalaureate — what each one means for your child.","parents-choosing-a-school-system.html"),
 ("Preparing for Checkpoint","What the Cambridge Checkpoint exams test and how to support your child at home.","parents-preparing-for-checkpoint.html"),
 ("The new Baccalaureate","How English is taught and assessed in تانية بكالوريا, explained simply.","parents-the-new-baccalaureate.html"),
 ("Universities and careers","Entry requirements, equivalency rules and choosing a major after school.","parents-universities-and-careers.html"),
]
home = f'''
<section class="hero"><div class="wrap hgrid">
<div class="htext">
<p class="kicker">Abdelkriem Academy · Educate Me Up</p>
<h1>Free educational resources that get students <em>exam-ready.</em></h1>
<p class="lead">Free courses, notes, practice and model answers for students and parents: Cambridge and Oxford English, تانية بكالوريا, a complete Quran course (reading, tajweed and memorisation) and English from zero to pro — prepared by Mohamed Abdelkriem, a British-curriculum teacher with 14 years in the classroom.</p>
<div class="ctas"><a class="btn" href="#courses">Browse the courses</a><a class="btn ghost" href="#parents">For parents</a></div>
<ul class="stats"><li><b>14</b><span>years teaching</span></li><li><b>11</b><span>free courses</span></li><li><b>100%</b><span>free to use</span></li></ul>
</div>
<figure class="portrait"><img src="images/mohamed-abdelkriem.jpg" width="1294" height="1618" alt="Mohamed Abdelkriem, teacher" onerror="this.parentNode.classList.add('noimg')"><span class="ph">Mohamed<br>Abdelkriem</span>
<figcaption>“No English exam left standing — my students are on a mission to conquer all.”</figcaption></figure>
</div></section>

<section id="courses" class="block"><div class="wrap">
<h2>Our courses</h2><p class="sub">Pick a course and start today. Everything inside is free.</p>
<div class="grid4">{"".join(card(t,d,h,g) for t,d,h,g in COURSES)}</div>
</div></section>

<section id="parents" class="block alt"><div class="wrap">
<p class="kicker">For parents</p><h2>Know exactly what your child needs</h2>
<p class="sub">Short, honest guidance in Egyptian Arabic — no jargon.</p>
<div class="grid4">{"".join(card(t,d,h if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"british","parents",h[:-5]+".json")) else None,"دليل بالعربي") for t,d,h in PARENTS)}</div>
</div></section>

<section class="block"><div class="wrap split">
<div><p class="kicker">Meet your teacher</p><h2>Mohamed Abdelkriem</h2>
<p>A British-curriculum teacher in Cairo, teaching Cambridge Checkpoint, IGCSE and Oxford courses in schools and learning centres.</p>
<ul class="ticks"><li>CELTA (Cambridge)</li><li>Professional Educator Diploma — The American University in Cairo</li><li>Professional Educational Diploma — Ain Shams University</li><li>TEFL Diploma</li></ul>
<a class="btn ghost" href="about.html">More about the academy</a></div>
<img class="banner" onerror="this.remove()" src="images/mohamed-abdelkriem-banner.jpg" width="1942" height="809" alt="Mohamed Abdelkriem — No English exam left standing, my students on a mission to conquer all." loading="lazy">
</div></section>
'''
page("index.html","Abdelkriem Academy — Free Educational Resources | Checkpoint, IGCSE, Baccalaureate, Quran",
     "Free educational resources by Mohamed Abdelkriem: notes, practice and video lessons for Cambridge Checkpoint 6 & 8, IGCSE 0510, Oxford GCSE, تانية بكالوريا, a complete Quran course and English from zero to pro.", home)

# ---------- BRITISH HUB ----------
TILE_CSS = """<style>.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin:6px 0 30px}
.tile{display:flex;flex-direction:column;justify-content:center;min-height:170px;background:var(--card);border:2px solid var(--line);border-radius:22px;padding:26px 24px;text-decoration:none;color:var(--navy);box-shadow:var(--shadow);transition:transform .15s,border-color .15s}
.tile:hover{transform:translateY(-3px);border-color:var(--gold)}.tile .ty{font-size:.85rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#7f5c1c;margin-bottom:6px}
.tile b{font-family:Fraunces,Georgia,serif;font-size:1.7rem;line-height:1.15}.tile .tar{font-family:Cairo,sans-serif;color:var(--muted);margin-top:6px;font-size:1rem}
.tile .go{margin-top:14px;font-weight:700;color:#7f5c1c}</style>"""
def tile(title, href, top="", sub=""):
    return f'<a class="tile" href="{href}">' + (f'<span class="ty">{top}</span>' if top else "") + f'<b>{title}</b>' + (f'<span class="tar">{sub}</span>' if sub else "") + '<span class="go">Open →</span></a>'
brit = TILE_CSS + pagehead("Section 1","British &amp; IGCSE","Choose your year.") + f'''
<section class="block"><div class="wrap"><div class="tiles">
{tile("Checkpoint 6","british-checkpoint-6.html","Year 6","English · Maths · Science")}
{tile("Checkpoint 8","british-checkpoint-8.html","Year 8","English · Maths · Science")}
{tile("IGCSE 0510","year-9-0510.html","Year 9","English as a Second Language")}
{tile("Oxford International GCSE","year-10-oxford.html","Year 10","English as a Second Language")}
</div></div></section>
<section class="block alt"><div class="wrap split"><div><h2>Writing skills</h2><p>Step-by-step lessons for every text type: persuasive writing, articles, reports, biographies and more.</p></div>{yt(PL["writing"],"Writing skills playlist")}</div></section>'''
for _n, _y, _st, _codes in ((6, "Year 6", "Cambridge Primary Checkpoint", ("0058", "0096", "0097")), (8, "Year 8", "Cambridge Lower Secondary Checkpoint", ("0861", "0862", "0893"))):
    _b = TILE_CSS + f'<section class="phead"><div class="wrap"><p class="kicker"><a href="british.html" style="color:inherit">British &amp; IGCSE</a> › {_y}</p><h1>Checkpoint {_n}</h1><p class="lead">{_st}. Choose your subject.</p></div></section>' + f'''
<section class="block"><div class="wrap"><div class="tiles">
{tile("English",f"checkpoint-{_n}.html",f"Checkpoint {_n} · {_codes[0]}","Full course + practice")}
{tile("Maths",f"checkpoint-{_n}-maths.html",f"Checkpoint {_n} · {_codes[1]}","Full course + practice tests")}
{tile("Science",f"checkpoint-{_n}-science.html",f"Checkpoint {_n} · {_codes[2]}","Full course + practice tests")}
</div></div></section>'''
    page(f"british-checkpoint-{_n}.html", f"Checkpoint {_n} — English, Maths and Science — Abdelkriem Academy", f"Free Cambridge Checkpoint {_n} courses ({_y}): English, Maths and Science with lessons, quizzes and practice tests.", _b, "british.html")
page("british.html","British & IGCSE — English, Maths and Science — Abdelkriem Academy","Free courses for Cambridge Checkpoint 6 and 8 English, Maths and Science, IGCSE 0510 and Oxford International GCSE English, with practice tests.", brit)

def checkpoint(fname, n, code, active="british.html"):
    def part(title, desc):
        return f'''<div class="part"><h3>{title}</h3><p>{desc}</p><div class="chips"><span class="chip">Reading</span><span class="chip">Writing</span></div>{soon()}</div>'''
    b = pagehead(f"British &amp; IGCSE · Year {n}", f"Checkpoint {n} English Resources", f"Everything for Cambridge Checkpoint {n} English ({code}), split the way the exam is: fiction and non-fiction, then exam skills and full practice papers.") + f'''
<section class="block"><div class="wrap">
<div class="grid2">
{part("Fiction","Stories and extracts: characterisation, imagery, writer's effects — and writing your own fiction.")}
{part("Non-fiction","Articles, reports, leaflets and persuasive texts — reading for meaning and writing for purpose.")}
</div>
<div class="grid2">
<div class="part"><h3>Exam Skills</h3><p>How to read the question, timing, and the tools examiners reward.</p>{soon()}</div>
<div class="part"><h3>Practice Exams + Model Answers</h3><p>Full papers to try at home, with marked model answers to compare against.</p>{soon()}</div>
</div></div></section>
<section class="block alt"><div class="wrap split"><div><h2>Video lessons</h2><p>Types of sentences, figures of speech, punctuation, author's purpose and more.</p></div>{yt(PL["checkpoint"],"Checkpoint lessons playlist")}</div></section>'''
    page(fname, f"Checkpoint {n} English Resources ({code}) — Abdelkriem Academy",
         f"Free Cambridge Checkpoint {n} English resources: fiction and non-fiction reading and writing, exam skills and practice papers with model answers.", b, active)
checkpoint("checkpoint-8.html", 8, "0861")
checkpoint("checkpoint-6.html", 6, "Cambridge Primary")

def skills(fname, kicker, title, code, desc, parts):
    ps = "".join(f'<div class="part"><h3>{t}</h3><p>{d}</p>{soon()}</div>' for t,d in parts)
    b = pagehead(kicker, title, desc) + f'<section class="block"><div class="wrap grid2">{ps}</div></section>'
    page(fname, f"{title} — Abdelkriem Academy", desc, b, "british.html")
skills("year-9-0510.html","British &amp; IGCSE · Year 9","IGCSE English 0510","0510",
 "Cambridge IGCSE English as a Second Language (0510) — skills, practice and exam technique for Year 9.",
 [("Reading Skills","Skimming, scanning, inference and answering exam-style questions."),
  ("Reading &amp; Writing","Exam-style reading tasks plus emails, articles and reports, with model answers."),
  ("Listening","Listening practice with transcripts and answer keys.")])
skills("year-10-oxford.html","British &amp; IGCSE · Year 10","Oxford International GCSE English","9280",
 "OxfordAQA International GCSE English as a Second Language (9280) — all four skills for Year 10.",
 [("Reading","Reading strategies and exam-style practice."),("Writing","Task types, structure and model answers."),
  ("Speaking","Speaking test format, useful language and practice prompts."),("Listening","Listening practice with answer keys.")])

# ---------- BACCALAUREATE (Arabic) ----------
units = ""
for book, rng in (("الكتاب الأول", range(1,6)), ("الكتاب التاني", range(6,11))):
    units += f'<h2 class="bk">{book}</h2><div class="grid2">'
    for u in rng:
        topics = "".join(f'<li>Topic {t}</li>' for t in range(1,8))
        units += f'<details class="unit"><summary><b>Unit {u}</b><span dir="ltr">7 Topics</span></summary><ol>{topics}</ol>{soon("الشرح والملخصات قريبًا")}</details>'
    units += '</div>'
bac = '<section class="phead"><div class="wrap"><p class="kicker">القسم التاني</p><h1>تانية بكالوريا مصرية English</h1><p class="lead">كل اللي تحتاجه في منهج English تانية بكالوريا: المنهج كتابين، 10 Units، وكل Unit فيها 7 Topics. هنا هتلاقي الشرح والملخصات والتدريبات لكل Topic، ونصايح الامتحان والتقييمات.</p></div></section>' + f'''
<section class="block"><div class="wrap">
<div class="grid3">
<div class="part"><h3>المنهج ماشي إزاي؟</h3><p>كتابين، 10 Units، وكل Topic بيستهدف 6 عناصر أساسية لازم تكون فاهمها ومتدرب عليها.</p></div>
<div class="part"><h3>الامتحان والتقييمات</h3><p>شكل الأسئلة وطريقة التقييم وإزاي تذاكر صح من أول السنة.</p>{soon("قريبًا")}</div>
<div class="part"><h3>لأولياء الأمور</h3><p>إزاي تتابع مع ابنك أو بنتك، وإيه المطلوب بالظبط في كل Unit.</p>{soon("قريبًا")}</div>
</div>
{units}
</div></section>
<section class="block alt"><div class="wrap split"><div><h2>فيديوهات تانية بكالوريا</h2><p>المنهج، نصايح الامتحان، وشرح الدروس على قناة اليوتيوب.</p></div>{yt(PL["bac"],"تانية بكالوريا English")}</div></section>'''
page("baccalaureate.html","تانية بكالوريا English — شرح وملخصات ونصايح | Abdelkriem Academy",
     "شرح منهج English تانية بكالوريا مصرية: 10 Units و70 Topic، ملخصات وتدريبات ونصايح الامتحان والتقييمات مع محمد عبد الكريم.", bac, rtl=True)

# ---------- QURAN ----------
lv = [("Level 1","Arabic letters and their sounds — the foundation for reading."),
      ("Level 2","Joining letters, short vowels and reading simple words."),
      ("Level 3","Tajweed basics and reading short surahs correctly."),
      ("Level 4","Memorisation with revision plans and confident recitation.")]
q = pagehead("Section 3","Quran by Levels","A calm, step-by-step path. Start at the level that fits you and move up at your own pace.") + \
    '<section class="block"><div class="wrap grid2">' + "".join(f'<div class="part"><span class="tag">{a}</span><p>{b}</p>{soon()}</div>' for a,b in lv) + '</div></section>'
page("quran.html","Quran by Levels — Abdelkriem Academy","Learn Quran step by step, organised by level: letters, reading, tajweed basics and memorisation.", q)

# ---------- IMPROVE ENGLISH ----------
IE_CSS = """<style>.start2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:0 0 10px}.st{border-radius:22px;padding:26px 26px;text-decoration:none;display:flex;flex-direction:column;gap:6px;box-shadow:var(--shadow)}
.st.a{background:var(--navy);color:#fff}.st.b{background:#fff;border:2px solid var(--line);color:var(--navy)}.st .n{font-weight:800;color:var(--gold);letter-spacing:.08em;text-transform:uppercase;font-size:.85rem}
.st b{font-family:Fraunces,serif;font-size:1.6rem;line-height:1.2}.st .ar{font-family:Cairo,sans-serif;direction:rtl;text-align:right;line-height:1.8;color:inherit;opacity:.92}.st .go{font-weight:800;color:var(--gold);margin-top:6px}.st.b .go{color:#7f5c1c}
@media (max-width:760px){.start2{grid-template-columns:1fr}}</style>"""
ie = TILE_CSS + pagehead("Section 4","English: From Zero to Pro<span class='ar-title' lang='ar' dir='rtl'>إنجليزي من الصفر للاحتراف</span>","A free English course in 5 levels, from your first word to fluent English, explained in Arabic.") + f'''
{IE_CSS}
<section class="block"><div class="wrap">
<h2>Where do I start? <span lang="ar" dir="rtl" style="font-family:Cairo,sans-serif">أبدأ منين؟</span></h2>
<div class="start2">
<a class="st a" href="english-placement-test.html"><span class="n">Step 1 · recommended</span><b>Find your level</b><span>A free 20-minute placement test tells you which level to start.</span><span class="ar">اعرف مستواك الأول: امتحان تحديد مستوى ببلاش في 20 دقيقة، وهيقولك تبدأ من أنهي ليفل.</span><span class="go">Take the placement test →</span></a>
<a class="st b" href="english-in-90-days.html"><span class="n">Complete beginner?</span><b>Start from zero</b><span>Never studied English, or forgot everything? Start Level 1.</span><span class="ar">لو بتبدأ من الصفر خالص، ابدأ الليفل الأول على طول.</span><span class="go">Start Level 1 →</span></a>
</div>
<p class="note">Every level has progress checks with answers. Level 1 ends with a final test: pass it, get your certificate and move on to Level 2. <span lang="ar" dir="rtl">كل ليفل فيه اختبارات قصيرة بالإجابات، والليفل الأول في آخره امتحان: لو نجحت تاخد شهادة وتكمّل على الليفل التاني.</span></p>
<h2 style="margin-top:34px">The 5 levels <span lang="ar" dir="rtl" style="font-family:Cairo,sans-serif">الليفلات الخمسة</span></h2>
<div class="tiles">
{tile("Level 1 · From Zero","english-in-90-days.html","A1 · Beginner","الليفل الأول: من الصفر")}
{tile("Level 2 · Elementary","english-level-2.html","A2","المستوى التاني: ابني أساس قوي")}
{tile("Level 3 · Pre-Intermediate","english-level-3.html","B1","المستوى التالت: اتكلم بثقة")}
{tile("Level 4 · Intermediate","english-level-4.html","B1+","المستوى الرابع: اتكلم براحتك في أي موقف")}
{tile("Level 5 · Upper-Intermediate","english-level-5.html","B2","المستوى الخامس: إنجليزي بطلاقة")}
</div></div></section>
<section class="block alt"><div class="wrap split"><div><h2>Classic stories, retold</h2><p>Famous short stories told as cinematic summaries — great listening practice and literature revision.</p></div>{yt(PL["lit"],"Literature stories playlist")}</div></section>'''
page("improve-english.html","English: From Zero to Pro — إنجليزي من الصفر للاحتراف | Abdelkriem Academy","A free English course from zero to fluent in 5 levels (A1–B2): words, sentences, grammar, exercises with answers and daily listening, with Arabic explanations.", ie)

# ---------- ABOUT / CONTACT / PRIVACY / TERMS ----------
about = pagehead("About","About Abdelkriem Academy","Free educational resources made by a working classroom teacher.") + '''
<section class="block"><div class="wrap prose">
<p>Abdelkriem Academy is a free educational resources website by Mohamed Abdelkriem, an English teacher with 14 years of experience in British-system schools and learning centres in Cairo. He teaches Cambridge Checkpoint, Cambridge IGCSE English as a Second Language (0510) and OxfordAQA International GCSE courses, and creates English video lessons for students and parents.</p>
<h2>Qualifications</h2>
<ul class="ticks"><li>CELTA — Cambridge English</li><li>Professional Educator Diploma — The American University in Cairo</li><li>Professional Educational Diploma — Ain Shams University</li><li>TEFL Diploma — AIPS Academy, USA</li><li>Bachelor's degree in Management — dual certificate (Egypt and the UK)</li></ul>
<h2>Our promise</h2>
<p>Every resource here is written for real classrooms: clear notes, honest exam advice and model answers you can learn from. Everything is free to use for personal study.</p>
</div></section>'''
page("about.html","About — Abdelkriem Academy","About Abdelkriem Academy and English teacher Mohamed Abdelkriem: experience, qualifications and mission.", about)

contact = pagehead("Contact","Get in touch","Questions about a resource, a correction, or a request for a new topic? Reach us here.") + f'''
<section class="block"><div class="wrap prose">
<p><b>Email:</b> <a href="mailto:contact@abdelkriemacademy.com">contact@abdelkriemacademy.com</a></p>
<p><b>YouTube:</b> <a href="{YT}" target="_blank" rel="noopener">Mohamed Abdelkriem</a> — leave a comment on any video to request a topic.</p>
<p>We usually reply within a few days.</p></div></section>'''
page("contact.html","Contact — Abdelkriem Academy","Contact Abdelkriem Academy.", contact, "about.html")

priv = pagehead("Legal","Privacy Policy","Last updated: October 2026") + '''
<section class="block"><div class="wrap prose">
<p>Abdelkriem Academy ("we") respects your privacy. This policy explains what information is collected when you use this website.</p>
<h2>Information we collect</h2><p>We do not ask you to create an account. If you email us, we receive your email address and message and use them only to reply.</p>
<h2>Cookies and advertising</h2><p>This website may display advertising served by Google AdSense. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on visits to this site and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>. You can also learn more at <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">How Google uses information from sites that use its services</a>.</p>
<h2>Analytics</h2><p>We may use privacy-friendly analytics to understand which resources are useful. This data is aggregated and does not identify you.</p>
<h2>Saved progress on your device</h2><p>Some practice tests remember your progress, your last score or the name you typed for a certificate. This information is saved only in your own browser on your device (local storage). It is not sent to us, and you can delete it at any time by clearing your browser data.</p>
<h2>Embedded videos and audio</h2><p>Video lessons are embedded from YouTube in privacy-enhanced mode, and Quran recitations are played from a public recitation library when you press a play button. The privacy policies of those services apply when you play them.</p>
<h2>Children</h2><p>Our resources are designed for students, parents and teachers. Younger children (for example, in the Quran course and the Checkpoint 6 courses) should use the website with a parent. We do not ask children for personal information and we do not knowingly collect it.</p>
<h2>Contact</h2><p>Questions about this policy? See our <a href="contact.html">contact page</a>.</p>
</div></section>'''
page("privacy.html","Privacy Policy — Abdelkriem Academy","Privacy policy for Abdelkriem Academy, including cookies and Google AdSense advertising.", priv, "about.html")

terms = pagehead("Legal","Terms of Use","Last updated: October 2026") + '''
<section class="block"><div class="wrap prose">
<p>All notes, worksheets and model answers on Abdelkriem Academy are free for personal study and classroom use. Please do not resell them or republish them as your own.</p>
<p>Resources are provided for learning. We work hard to keep them accurate, but always check official syllabus documents from your exam board.</p>
<p>Links to external websites are provided for convenience; we are not responsible for their content.</p>
<h2>Our content</h2><p>Every lesson, explanation, practice question, practice test, model answer, worksheet and PDF on Abdelkriem Academy is written and designed by Abdelkriem Academy (Mohamed Abdelkriem). We follow the topics listed in each official syllabus, but we do not copy textbooks, past papers or other publishers' material. &copy; Abdelkriem Academy. All rights reserved.</p>
<p>A few items come from other sources and are always credited or linked: the text of the Holy Quran and the recitations we play are taken from trusted, published sources; some science photographs come from Wikimedia Commons under the licence shown under each photo; and some pages link to or embed videos and audio from other creators, which remain the property of their owners.</p>
<h2>Independence</h2><p>Abdelkriem Academy is an independent educational website. It is not affiliated with, endorsed by or connected to Cambridge University Press &amp; Assessment, OxfordAQA, Pearson, the College Board (SAT), ACT, Inc., the organisers of the EST, or the Egyptian Ministry of Education. Exam names and codes are used only to describe what each resource helps students prepare for. Our practice tests are written in the style of these exams; they are not official papers, and their scores are practice scores.</p>
<h2>Certificates</h2><p>Course certificates on this website (for example, after the English Course Level 1 final test) are free certificates of completion from Abdelkriem Academy. They show that the learner passed our own online test; they are not official qualifications.</p>
</div></section>'''
page("terms.html","Terms of Use — Abdelkriem Academy","Terms of use for Abdelkriem Academy.", terms, "about.html")

with open(f"{OUT}/images/favicon.svg","w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f1b33"/><text x="32" y="42" font-family="Georgia,serif" font-size="28" font-weight="700" text-anchor="middle" fill="#d4a24c">AA</text></svg>')
with open(f"{OUT}/ads.txt","w") as f: f.write("google.com, pub-8885402561273130, DIRECT, f08c47fec0942fa0\n")
with open(f"{OUT}/robots.txt","w") as f: f.write("User-agent: *\nAllow: /\nSitemap: https://abdelkriemacademy.com/sitemap.xml\n")
EXTRA_PAGES = []
PAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
if os.path.isdir(PAGES_DIR):
    for _f in sorted(os.listdir(PAGES_DIR)):
        if _f.endswith(".py"):
            exec(open(os.path.join(PAGES_DIR, _f), encoding="utf-8").read())
pages = ["index.html","british.html","british-checkpoint-6.html","british-checkpoint-8.html","checkpoint-6.html","checkpoint-8.html","year-9-0510.html","year-10-oxford.html","baccalaureate.html","quran.html","improve-english.html","about.html","contact.html","privacy.html","terms.html"] + EXTRA_PAGES
with open(f"{OUT}/sitemap.xml","w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>https://abdelkriemacademy.com/{p[:-5] if p!='index.html' else ''}</loc></url>\n" for p in pages) + "</urlset>\n")
print("built", len(pages))
