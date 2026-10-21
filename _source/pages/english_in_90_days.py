# English in 90 Days — free beginner course page (runs inside build.py)
PDF = "files/English-Course-From-Zero.pdf"
PDF_NAME = "English Course From Zero - طوّر الإنجليزي من الصفر.pdf"
WEEKS = [
 (1, "Hello! This Is Me", "Verb to be (am / is / are)"),
 (2, "My Family and Friends", "have / has · my, your, his, her · 's"),
 (3, "My Home and My Town", "there is / there are · in, on, under, next to · a / an"),
 (4, "My Day", "Present simple (I / you / we / they) · at, on, in · telling the time"),
 (5, "Free Time and Habits", "Present simple: he / she + s · does / doesn't · always, usually, never"),
 (6, "Food and Shopping", "Countable / uncountable · some / any · How much? How many? · I'd like…"),
 (7, "Work and Skills", "can / can't · Wh- questions"),
 (8, "Right Now: Weather and Clothes", "Present continuous (am / is / are + -ing)"),
 (9, "Yesterday and Long Ago", "was / were · there was / there were"),
 (10, "What Happened?", "Past simple: regular and irregular verbs · didn't · Did…?"),
 (11, "Plans and Invitations", "be going to · will / won't · Would you like…? Let's…"),
 (12, "Health, Travel and Asking for Help", "should / shouldn't · Could you…? May I…? · instructions"),
]
CHECKS = {4: "Progress Check 1 · Weeks 1–4", 8: "Progress Check 2 · Weeks 5–8", 12: "Progress Check 3 · Weeks 9–12"}

def _weeks():
    out = ""
    for n, title, grammar in WEEKS:
        out += f'<li class="wk"><span class="wn">Week {n}</span><div><h3><a href="english-week-{n}.html">{title}</a></h3><p>Grammar: {grammar}</p></div></li>'
        if n in CHECKS:
            out += f'<li class="chk"><a href="english-progress-check-{n//4}.html">✓ {CHECKS[n]}</a> — score 16/20 to move on</li>'
    return out


AR_HINT_CSS = """<style>.arhint{font-family:Cairo,sans-serif;direction:rtl;text-align:right;background:#fbf1dc;border-radius:12px;padding:10px 14px;margin:6px 0 14px;line-height:1.9}
.arguide{direction:rtl;text-align:right;font-family:Cairo,sans-serif}.arguide h2,.arguide h3{font-family:Cairo,sans-serif}.arguide table{width:100%;border-collapse:collapse}
.arguide td,.arguide th{border:1px solid var(--line);padding:9px 12px;vertical-align:top;text-align:right}.arguide th{background:var(--navy);color:#fff}
.arguide ol,.arguide ul{padding-right:22px}.arguide li{margin-bottom:6px}</style>"""
AR_GUIDE = AR_HINT_CSS + """<section class="block alt"><div class="wrap arguide" dir="rtl" lang="ar">
<h2>إزاي تذاكر الكورس ده؟ (اقرا الجزء ده الأول)</h2>
<p>الكورس معمول لأي حد بيبدأ من الصفر. كل أسبوع له صفحة فيها كل اللي محتاجه: الكلمات بمعناها بالعربي، وجمل تحفظها، وقاعدة جرامر مشروحة بالعربي، وتمارين بالإجابات، وخطة استماع لكل يوم. ذاكر <b>30 دقيقة كل يوم، 6 أيام في الأسبوع</b>، واليوم السابع راحة أو استماع لقصة.</p>
<h3>الـ 30 دقيقة بتوع كل يوم</h3>
<table><thead><tr><th>الوقت</th><th>هتعمل إيه</th></tr></thead><tbody>
<tr><td>5 دقايق</td><td><b>راجع</b> كلمات وجمل امبارح: غطّي الإنجليزي وحاول تقول الكلمة من العربي.</td></tr>
<tr><td>8 دقايق</td><td><b>احفظ</b> 6 كلمات وجملتين جداد. قول كل واحدة بصوت عالي 5 مرات واكتبها في الكشكول.</td></tr>
<tr><td>10 دقايق</td><td><b>اسمع أو اتفرج</b> على درس النهارده من خطة الأسبوع (عمود Listen / Watch) بطريقة الأربع خطوات اللي تحت.</td></tr>
<tr><td>5 دقايق</td><td><b>حل التمرين</b> بتاع النهارده بالقلم الرصاص، وبعدين دوس «Show the answers» وصحّح لنفسك.</td></tr>
<tr><td>2 دقيقة</td><td><b>اتكلم</b>: قول 3 جمل عن يومك بكلمات النهارده.</td></tr>
</tbody></table>
<h3>طريقة الاستماع في 4 خطوات</h3>
<ol><li><b>اسمع بس</b> من غير ما تقرا، وحاول تفهم الفكرة العامة.</li>
<li><b>اسمع واقرا</b> النص أو الترجمة الإنجليزي، وحط خط تحت الكلمات الجديدة.</li>
<li><b>ردّد وراه</b>: وقّف بعد كل جملة وقولها بنفس الصوت والسرعة.</li>
<li><b>اسمع تاني</b> من غير النص… هتلاقي نفسك فاهم أكتر بكتير.</li></ol>
<h3>إزاي تستخدم المصادر؟</h3>
<ul><li>في جدول خطة الأسبوع، دوس على اسم الدرس في عمود <b>Listen / Watch</b> هيفتح لك بحث بالاسم بالظبط، افتح أول نتيجة من الموقع نفسه (engVid أو BBC أو British Council…).</li>
<li>جنب كل مصدر مكتوب نوعه: <b>(podcast)</b> أو <b>(audio)</b> يعني صوت بس تسمعه في الموبايل أو العربية، <b>(video)</b> فيديو، <b>(reading)</b> قراءة، <b>(listening)</b> استماع بالنص.</li>
<li>لو الكلام سريع: في يوتيوب دوس ⚙ ← Playback speed ← 0.75، وشغّل الترجمة <b>الإنجليزي</b> مش العربي.</li></ul>
<h3>قبل ما تبدأ</h3>
<ul><li>اعمل اختبار مستوى مجاني النهارده واكتب نتيجتك، وكرّره في آخر الكورس عشان تشوف الفرق.</li>
<li>جهّز كشكول: الإنجليزي على الشمال والعربي على اليمين، وصفحة لكل أسبوع.</li>
<li>نزّل تطبيق كروت مجاني زي Anki وحط فيه كلمات كل يوم، وراجعها 5 دقايق الصبح.</li>
<li>خلّي الإنجليزي جزء من يومك: غيّر لغة الموبايل لإنجليزي، كلّم نفسك بالإنجليزي، وابعت لنفسك فويس نوت كل جمعة.</li>
<li>بعد الأسبوع الرابع والثامن والثاني عشر فيه <b>اختبار (Progress Check)</b>: لو جبت 16 من 20 أو أكتر كمّل، لو أقل راجع جمل الأسابيع دي 3 أيام وحاول تاني.</li>
<li><b>القاعدة الذهبية:</b> مش لازم تفهم كل كلمة. افهم الفكرة وكمّل، والباقي هييجي مع الوقت.</li></ul>
</div></section>"""

course = pagehead("Free beginner course · 12 weeks · 30 minutes a day", "English Course: From Zero<span class='ar-title' lang='ar' dir='rtl'>طوّر الإنجليزي بتاعك من الصفر</span>",
    "Start English from zero at home: 12 weeks, 30 minutes a day. Words, sentences to memorise, grammar, exercises with answers and a daily listening plan — explained in English and Arabic.") + f'''
<section class="block"><div class="wrap split">
<div>
<ul class="stats dark"><li><b>360</b><span>words</span></li><li><b>120</b><span>key sentences</span></li><li><b>12</b><span>grammar points</span></li><li><b>48</b><span>exercises + answers</span></li></ul>
<div class="ctas"><a class="btn" href="english-week-1.html">Start Week 1</a><a class="btn ghost" href="{PDF}" download="{PDF_NAME}">Download the PDF · حمّل الكورس PDF</a></div>
<p class="ar" dir="rtl" lang="ar">كورس إنجليزي للمبتدئين — ٣ شهور، ٣٠ دقيقة يوميًا. الكتاب فيه كل اللي محتاجه: الكلمات والجمل والقواعد والتمارين بالإجابات، وخطة استماع لكل يوم بالروابط.</p>
</div>
<div class="part">
<h3>Your 30 minutes every day</h3>
<ol class="steps">
<li><b>5 min · Review</b> yesterday's words and sentences.</li>
<li><b>8 min · Learn</b> today's 6 words and 2 sentences — say each one aloud 5 times.</li>
<li><b>10 min · Listen</b> to today's lesson using the 4-step method.</li>
<li><b>5 min · Practise</b> today's exercise, then check the answer key.</li>
<li><b>2 min · Speak</b>: say 3 sentences about your day.</li>
</ol>
<p class="note">6 days a week, and on day 7 just enjoy a story or a podcast. 30 minutes every day beats 3 hours once a week.</p>
</div>
</div></section>
{AR_GUIDE}
<section class="block alt"><div class="wrap">
<h2>The 4-step listening method</h2>
<div class="grid4">
{card("1 · Listen only","Don't read. Try to catch the general idea.")}
{card("2 · Listen and read","Follow the script or subtitles and underline new words.")}
{card("3 · Shadow","Pause after each sentence and repeat it with the same sound and speed.")}
{card("4 · Listen again","No text this time — you will understand much more.")}
</div>
<p class="note">Too fast? On YouTube tap Settings → Playback speed → 0.75 and turn on English subtitles, not Arabic.</p>
</div></section>

<section id="plan" class="block"><div class="wrap">
<h2>The 12-week plan</h2><p class="sub">Each week has 30 words, 10 sentences to memorise, one grammar point, daily listening and exercises.</p>
<ol class="weeks">{_weeks()}</ol>
<div class="ctas"><a class="btn" href="english-week-1.html">Start Week 1 · ابدأ الأسبوع الأول</a></div>
</div></section>

<section class="block alt"><div class="wrap prose">
<h2>Before you start</h2>
<ul class="ticks">
<li>Take a free online English level test today, and again at the end of Week 12 to see your progress.</li>
<li>Get a notebook: English on the left, Arabic on the right — one page per week.</li>
<li>Use a free flashcard app for the 6 words of each day, 5 minutes every morning.</li>
<li>Make English part of your day: change your phone language, talk to yourself in English, and send yourself a voice note every Friday.</li>
</ul>
<p><b>The golden rule:</b> don't try to understand every word. Understand the idea, keep listening, and the rest comes with time.</p>
</div></section>'''
page("english-in-90-days.html", "English Course: From Zero — طوّر الإنجليزي بتاعك من الصفر | Abdelkriem Academy",
     "Free beginner English course: 12 weeks, 30 minutes a day, 360 words, 120 key sentences, grammar, exercises with answers and a daily listening plan in English and Arabic.",
     course, "improve-english.html")
EXTRA_PAGES.append("english-in-90-days.html")
