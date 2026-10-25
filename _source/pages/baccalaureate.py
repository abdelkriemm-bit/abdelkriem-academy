# تانية بكالوريا English — skills map (runs inside build.py and replaces the first version of baccalaureate.html)
# Built from the Ministry textbook (Part 1: Units 1–5, Part 2: Units 6–10). Topics are titles only for now.

BAC_CSS = """<style>
.skillnav{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
.skillnav a{text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 16px;font-weight:600;color:var(--navy)}
.skillnav a:hover{border-color:var(--gold);color:var(--gold-2)}
.howto{background:#fbf1dc;border-radius:14px;padding:14px 18px;margin-bottom:26px}
.howto p{margin:0}
.skill{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:24px;margin-bottom:20px;scroll-margin-top:90px}
.skhead{display:flex;align-items:center;gap:16px;margin-bottom:14px}
.skhead h2{margin:0;font-family:Fraunces,serif}
.skhead p{margin:2px 0 0;color:var(--muted)}
.skhead .num{flex:none;width:44px;height:44px;border-radius:12px;background:var(--navy);color:var(--gold);display:grid;place-items:center;font-weight:800;font-size:1.2rem}
.skhead .count{margin-inline-start:auto;font-size:.85rem;color:var(--gold-2);background:#fbf1dc;border-radius:999px;padding:4px 12px;white-space:nowrap}
.topics{list-style:none;padding:0;margin:0 0 14px;display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.topics li{display:flex;justify-content:space-between;gap:12px;align-items:center;border:1px solid var(--line);border-radius:10px;padding:10px 14px;background:var(--paper);font-family:Inter,sans-serif}
.topics li.ready{padding:0}
.topics li.ready a{display:flex;justify-content:space-between;gap:12px;align-items:center;width:100%;padding:10px 14px;text-decoration:none;color:var(--navy)}
.topics li.ready{border-color:var(--gold);background:#fffaf0}
.topics li.ready:hover{box-shadow:0 2px 8px rgba(0,0,0,.08)}
.topics li.ready .tt::after{content:' ← الشرح';color:var(--gold-2);font-weight:700;font-size:.85rem;font-family:Cairo,sans-serif}
.topics .u{flex:none;font-size:.78rem;color:var(--muted);background:#fff;border:1px solid var(--line);border-radius:999px;padding:2px 8px}
.official ul{margin:6px 0;padding-right:20px}
.official a{color:var(--navy);font-weight:600}
.unit .sec{margin:12px 0 4px}
.unit ul{margin:0 0 6px;padding-left:20px;color:var(--muted)}
.unit .rv{color:#a3342b;font-weight:600;margin:8px 0 0}
@media (max-width:760px){.topics{grid-template-columns:1fr}.skhead{flex-wrap:wrap}}
</style>"""

BAC_SKILLS = [
 ("grammar", "Grammar", "القواعد اللي في الكتابين، بترتيب الوحدات.", [
  ("Participial Phrases (-ing / -ed)", "U1"), ("Relative Clauses (who, which, that)", "U1"),
  ("Conditionals (If… will / would / would have) + hedging", "U1"),
  ("Gerunds and Infinitives", "U2"), ("Narrative Tenses", "U2"),
  ("Prepositional Phrases of Place and Time", "U3"), ("Concession Clauses", "U3"), ("The Passive Voice for Formal Reporting", "U3"),
  ("The Present Perfect (since, for, just, already, yet, ever, never)", "U4"), ("Fronting for Emphasis", "U4"),
  ("Cause-and-Effect Structures", "U5"), ("Modal Verbs (could, should, may, must)", "U5"), ("Adverbials of Degree and Frequency", "U5"),
  ("Reported Speech", "U6"), ("Used to / Would (Past Habits)", "U7"), ("The Present Continuous", "U8"),
  ("Linking Words and Logical Connectors", "U4 · U8"),
  ("The Causative: have / get something done", "U9"), ("So… that / Such… that", "U9"),
  ("Stative Verbs vs Action Verbs", "U10"), ("Quantifiers (too much / too many, a large amount of, few / little)", "U10"),
 ]),
 ("language", "Vocabulary &amp; Language", "كلمات كل Unit، والـ Language اللي بيتقيّم عليها الطالب في القراية والكتابة.", [
  ("Well-being and Mental Health", "U1"), ("Leisure, Screen Time, Arts and Sport", "U2"), ("History, Heritage and Museums", "U3"),
  ("Brands, Food Waste and Sales Culture", "U4"), ("Climate Change and Renewable Energy", "U5"), ("Global Responsibility and Advocacy", "U6"),
  ("Passion, Hobbies and Community", "U7"), ("Vocational Education and Careers", "U8"), ("Belonging and Inclusion", "U9"),
  ("Hidden Costs and Fast Fashion", "U10"),
  ("Persuasive and Biased Language: intensifiers, rhetorical questions, absolute language", "U1"),
  ("Hedging and Neutral Language", "U1"), ("Tone, Evaluative Language and Selective Framing", "U3 · U6 · U9"),
  ("Concession Language", "U3 · U6 · U7"), ("Media Literacy: fact, opinion, bias and greenwashing", "U1 · U3 · U10"),
 ]),
 ("reading", "Reading", "مهارات القراية وأنواع النصوص اللي في الكتابين.", [
  ("Reading for Gist and Key Detail", "All units"), ("True / False / Not Given with justification", "All units"),
  ("Fact, Opinion and Biased Claims", "U1 · U2 · U4"), ("Identifying Bias in Media Texts", "U1"),
  ("Rhetorical Devices and Their Effects", "U1"), ("The Writer's Viewpoint and Tone", "U3 · U6"),
  ("Main Argument and Supporting Points", "U1 · U4"), ("Cause and Effect in Informational Texts", "U4 · U5"),
  ("Text Types: reports, articles, opinion articles, narratives and profiles", "All units"),
  ("Vocabulary in Context", "All units"), ("Evaluating the Reliability of Online Content", "U3 · U6 · U7 · U9"),
 ]),
 ("listening", "Listening", "أنواع التسجيلات والمهارات المطلوبة.", [
  ("Broadcasts, Podcasts, Radio Programmes and Media Reports", "All units"),
  ("Listening for Main Ideas and Specific Information", "U2 · U4 · U5"),
  ("Stated vs Unstated Information", "U3 · U6 · U7 · U8 · U9 · U10"),
  ("The Speaker's Perspective", "U1 · U5"), ("Technical Terms in Context", "U1 · U5"),
 ]),
 ("speaking", "Speaking", "كل مهام الـ Speaking والـ Presentations.", [
  ("Giving and Justifying an Opinion (JRE)", "All units"), ("Acknowledging an Opposing Viewpoint", "U2 · U3 · U6–U10"),
  ("Structured Presentations (3–5 minutes)", "U3 · U4 · U6–U10"), ("Pair and Group Discussions", "All units"),
  ("Debates", "U4 · U5 · U10"), ("Role-plays and Pitches", "U8 · U10"), ("Reporting Other People's Views", "U5 · U6"),
 ]),
 ("writing", "Writing", "كل أنواع الـ Writing اللي في الكتابين — أغلبها 150–180 كلمة.", [
  ("The JRE Analytical Paragraph", "U1"), ("Reflective Writing", "U1"), ("Opinion Paragraph", "U2 · U4"),
  ("Diary Entry", "U2 · U10"), ("Discursive Paragraph", "U3"), ("Opinion Article", "U4"), ("Review", "U4"),
  ("Argumentative Paragraph", "U5"), ("Informational Leaflet", "U5"), ("Formal Email", "U6"), ("Persuasive Email", "U6"),
  ("Proposal", "U7"), ("Discursive Essay", "U7 · U9 · U10"), ("Blog Post", "U8"), ("Recommendation Report", "U8"),
  ("Personal Development Plan", "U8"), ("Personal Narrative", "U9"), ("Problem-Solution Paragraph", "U10"),
 ]),
 ("literature", "Literature", "القصة المقررة والنصوص الأدبية اللي في الوحدات.", [
  ("The Lost World — the set novel", "Novel"),
  ("The Lost World · Chapter 1: A Dream of Adventure", "Novel"),
  ("The Lost World · Chapter 2: Professor Challenger's Secret", "Novel"),
  ("The Lost World · Chapter 3: The Expedition Is Chosen", "Novel"),
  ("The Lost World · Chapter 4: Into the Unknown", "Novel"),
  ("The Lost World · Chapter 5: Trapped in the Lost World", "Novel"),
  ("The Lost World · Chapter 6: Malone's Night Adventure", "Novel"),
  ("The Lost World · Chapter 7: Prisoners of the Ape-Men", "Novel"),
  ("The Lost World · Chapter 8: The Battle for the Plateau", "Novel"),
  ("The Lost World · Chapter 9: The Hidden Way Home", "Novel"),
  ("The Lost World · Chapter 10: Proof Before the World", "Novel"), ("Literary Extract: “Not Exactly a Relaxing Day”", "U2"),
  ("Narrative Techniques: simile, contrast and personal voice", "U2"), ("Mood, Tone and the Narrator's Shifting Feelings", "U2"),
  ("Characters, Themes and Key Events", "Novel"),
 ]),
]

BAC_UNITS = [
 ("الكتاب الأول", [
  (1, "Living Well in a Complex World", "Well-being", ("Social Reflection", ["Social Media and Self-Image", "Exploring Modern Lifestyles"]), ("Shared Responsibility", ["Whose Responsibility Is It?", "Understanding Mental Health"]), None),
  (2, "Leisure Time", "Experiences", ("Leisure in a Digital World", ["Screen Time and Young People", "Creative Arts as Leisure Activities"]), ("Lifelong Activity", ["Sport and Physical Activity as Leisure", "Not Exactly a Relaxing Day"]), "A"),
  (3, "Echoes of the Past", "Identity", ("Historical Landscape", ["Sites of Memory", "The Museum as a Storyteller"]), ("Documenting History", ["The Viral Past", "Social Media and Historical Events"]), None),
  (4, "The Power of Choice", "Consumption and Choice", ("Food Awareness", ["Food Waste", "Beyond the Brand"]), ("Online Consumption", ["Digital Consumption", "Black Friday and Sales Culture"]), "B"),
  (5, "The Greenhouse Effect", "Sharing the Planet", ("Climate Change", ["The Climate Crisis", "Renewable Energy – Powering a Sustainable Future"]), ("Egypt's Green Change Makers", ["Greening Projects in Egypt", "Individual and Collective Actions"]), None),
 ]),
 ("الكتاب التاني", [
  (6, "The Space We Share", "A World for All", ("Global Responsibility", ["A World We Borrow", "When Needs Compete"]), ("Speaking Up for Others", ["Voices for the Voiceless", "Global Citizens, Local Actions"]), "C"),
  (7, "Discovering Your Passion", "Passion &amp; Purpose", ("Where Passion Begins", ["From Hobby to Opportunity", "Building a Community Around Your Passion"]), ("What Passion Leaves Behind", ["Leaving Your Mark", "Time Well Spent: Balancing Passion and Priorities"]), None),
  (8, "Pathways to Progress", "Identity Across Time", ("Bridging Skills and Future Careers", ["Vocational Education in Egypt", "International Vocational Voices Online"]), ("Building Future Professionals", ["The Egyptian-Japanese Schools (EJS)", "The Skills Employers Really Want"]), "D"),
  (9, "Circles of Belonging", "Belonging &amp; Well-being", ("A Sense of Belonging", ["Finding My Place", "Relationships That Help Us Grow"]), ("Inclusion and Community Action", ["No One Left Out", "Community That Cares"]), None),
  (10, "Behind the Buy", "Invisible Consumption", ("What We Don't See", ["Hidden Cost of a Click", "Chasing Validation"]), ("The Price We Don't Count", ["True Price of Fast Fashion", "Rethinking What We Buy: A Community Response"]), "E"),
 ]),
]

def _skill_nav():
    return '<nav class="skillnav" dir="ltr">' + "".join(f'<a href="#{k}" dir="ltr">{t}</a>' for k, t, _, _ in BAC_SKILLS) + '</nav>'

import json as _bacj, os as _baco
_BAC_DIR = _baco.path.join(_baco.path.dirname(PAGES_DIR), "british", "bac")
_BAC_SLUG = {}
try:
    for _s, _v in _bacj.load(open(_baco.path.join(_BAC_DIR, "TOPICS.json"), encoding="utf-8")).items():
        if _baco.path.exists(_baco.path.join(_BAC_DIR, _s + ".json")) and not (_baco.environ.get("BRITISH_SKIP") and __import__("re").search(_baco.environ["BRITISH_SKIP"], _s)):
            _BAC_SLUG[(_v["skill"], _v["title"])] = _s
except FileNotFoundError:
    pass

def _topic_li(key, t, u):
    s = _BAC_SLUG.get((key, t.replace("&amp;", "&")))
    inner = f'<span class="tt">{t}</span><span class="u">{u}</span>'
    return f'<li dir="ltr" class="ready"><a href="{s}.html">{inner}</a></li>' if s else f'<li dir="ltr">{inner}</li>'

def _skills():
    out = ""
    for i, (key, title, sub, topics) in enumerate(BAC_SKILLS, 1):
        items = "".join(_topic_li(key, t, u) for t, u in topics)
        out += f'''<section id="{key}" class="skill"><div class="skhead"><span class="num">{i}</span><div><h2 dir="ltr">{title}</h2><p>{sub}</p></div><span class="count" dir="ltr">{len(topics)} topics</span></div>
<ul class="topics" dir="ltr">{items}</ul>{'<p class="howto" style="margin:0">دوس على أي Topic عشان تفتح الشرح بالعربي والتدريبات.</p>' if any((key, t.replace("&amp;", "&")) in _BAC_SLUG for t, _ in topics) else '<span class="soon">الشرح والتدريبات قريبًا</span>'}</section>'''
    return out

def _units():
    out = ""
    for book, units in BAC_UNITS:
        out += f'<h3 class="bk">{book}</h3><div class="grid2">'
        for n, name, concept, a, b, review in units:
            sec = "".join(f'<p class="sec" dir="ltr"><b>Section {s}: {t}</b></p><ul dir="ltr">' + "".join(f"<li>{l}</li>" for l in ls) + "</ul>" for s, (t, ls) in zip("AB", (a, b)))
            rv = f'<p class="rv" dir="ltr">+ Consolidation Review {review}</p>' if review else ""
            out += f'<details class="unit"><summary><b dir="ltr">Unit {n} · {name}</b><span dir="ltr">Concept: {concept}</span></summary>{sec}{rv}</details>'
        out += '</div>'
    return out

bac2 = BAC_CSS + '''<section class="phead"><div class="wrap"><p class="kicker">القسم التاني</p><h1>تانية بكالوريا مصرية English</h1>
<p class="lead">المنهج كتابين فيهم 10 Units، وكل Unit فيها Section A وSection B وأربع دروس. قسّمنا لك المنهج كله على 7 مهارات، وكل مهارة فيها التوبكس اللي محتاج تذاكرها.</p></div></section>''' + f'''
<section class="block"><div class="wrap">
{_skill_nav()}
<div class="howto"><p><b>إزاي تذاكر:</b> اختار المهارة، وذاكر التوبكس بالترتيب. الحروف اللي جنب كل Topic (U1, U2…) بتقولك هو في أنهي Unit في الكتاب.</p></div>
<div class="howto official"><p><b>كتب الوزارة الرسمية (PDF من موقع الوزارة):</b></p>
<ul>
<li><a href="https://egyptianbaccalaureate.blob.core.windows.net/egyptianbaccalaureate/Eng-L1-EB-Part1.pdf" target="_blank" rel="noopener" dir="ltr">English — Part 1 (Units 1–5)</a></li>
<li><a href="https://egyptianbaccalaureate.blob.core.windows.net/egyptianbaccalaureate/Eng-L1-EB-Part2.pdf" target="_blank" rel="noopener" dir="ltr">English — Part 2 (Units 6–10)</a></li>
<li><a href="https://egyptianbaccalaureate.blob.core.windows.net/egyptianbaccalaureate/Story-En-EB-L1.pdf" target="_blank" rel="noopener" dir="ltr">The Lost World — Adapted for Grade 11 (القصة)</a></li>
</ul>
<p>أسئلة التدريب في الدروس معمولة بنفس شكل أسئلة الـ Consolidation Reviews اللي في كتاب الوزارة.</p></div>
{_skills()}
</div></section>

<section class="block alt"><div class="wrap">
<h2>خريطة الكتابين</h2><p class="sub">كل Unit ودروسها زي ما هي في كتاب الوزارة.</p>
{_units()}
<p class="note">كل Unit بتعتمد على طريقة JRE: Justify – Reason – Evidence (+ Reflect and Act).</p>
</div></section>

<section class="block"><div class="wrap split"><div><h2>فيديوهات تانية بكالوريا</h2><p>المنهج، نصايح الامتحان، وشرح الدروس على قناة اليوتيوب.</p></div>{yt(PL["bac"],"تانية بكالوريا English")}</div></section>'''

page("baccalaureate.html", "تانية بكالوريا English — المنهج متقسم على 7 مهارات | Abdelkriem Academy",
     "منهج English تانية بكالوريا مصرية متقسم على 7 مهارات: Grammar وVocabulary وReading وListening وSpeaking وWriting وLiterature، مع خريطة الـ 10 Units.",
     bac2, "egyptian-baccalaureate.html", rtl=True)
