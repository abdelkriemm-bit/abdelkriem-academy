# Arabic & History hub (identity-subjects.html): the Ministry's "identity subjects" for international-certificate students
# (IG, American Diploma...) and the Egyptian Baccalaureate Year 2 — same official curriculum, so one course serves both.
_is = TILE_CSS + pagehead("Arabic &amp; History", "Arabic &amp; History · العربي والتاريخ",
  "For IG and American Diploma students in Egypt, and for تانية بكالوريا. Choose your subject.") + f'''
<section class="block"><div class="wrap"><div class="tiles">
{tile("Arabic<span class='tar' style='display:block;font-size:1.3rem;color:var(--navy);font-weight:800;margin-top:6px;text-align:left' dir='rtl'>اللغة العربية</span>","eb-arabic.html","IG · American · تانية بكالوريا","النصوص والنحو والبلاغة والإملاء")}
{tile("History<span class='tar' style='display:block;font-size:1.3rem;color:var(--navy);font-weight:800;margin-top:6px;text-align:left' dir='rtl'>التاريخ الوطني</span>","eb-history.html","IG · American · تانية بكالوريا","شرح كل درس + تدريبات + امتحانات")}
</div></div></section>
<section class="block alt"><div class="wrap prose notranslate" dir="rtl" lang="ar" translate="no">
<h2>المنهج ده لمين؟</h2>
<ul>
<li><b>طلبة الشهادات الدولية</b> في مصر (IG والدبلومة الأمريكية وغيرها): الوزارة ألزمت المدارس الدولية بتدريس العربي والتاريخ والتربية الدينية من الصف العاشر للثاني عشر، ودرجات <b>العربي والتاريخ ليها 20% من المجموع</b> (10% لكل مادة) بامتحان عام بتنظمه الوزارة. وفي الدبلومة الأمريكية: 40% GPA و40% الاختبارات الأمريكية و20% العربي والتاريخ.</li>
<li>والمحكمة الإدارية العليا <b>أيّدت القرار</b> في مايو 2025.</li>
<li>ويوم 30 أغسطس 2026 نقلت الصحف عن مصدر مسؤول بالوزارة إن طلبة الشهادات الدولية بيدرسوا <b>نفس منهج العربي والتاريخ بتاع الصف الثاني بكالوريا</b> من سنة 2026-2027.</li>
<li><b>وطلبة تانية بكالوريا</b> في المدارس المصرية بيدرسوا نفس المنهج بالظبط.</li>
</ul>
<p>الشرح هنا مبني على <b>كتب الوزارة الرسمية</b> لسنة 2026-2027 (العربي جزءين + كتاب القصة، والتاريخ الوطني جزءين). والكتب الأصلية موجودة مجانًا على <a href="https://ellibrary.moe.gov.eg/EgyptianBaccalaureate/" rel="noopener" target="_blank">المكتبة الإلكترونية لوزارة التربية والتعليم</a>. الشرح والأسئلة والامتحانات <b>من تأليفنا</b> على نفس أسلوب أسئلة الوزارة.</p>
<p style="font-size:.95rem"><b>مهم:</b> تفاصيل شكل الامتحان العام لطلبة الدولي بتعلنها الوزارة والمدرسة، فتابع التعليمات الرسمية من مدرستك. ونحن بنضيف الدروس وحدة وحدة.</p>
<p style="font-size:.88rem">المصادر: <a href="https://www.youm7.com/story/2025/5/15/%D9%83%D9%8A%D9%81-%D9%86%D9%81%D9%87%D9%85-%D9%82%D8%B1%D8%A7%D8%B1-%D8%A5%D8%B6%D8%A7%D9%81%D8%A9-20-%D9%85%D9%86-%D8%AF%D8%B1%D8%AC%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%89-%D9%88%D8%A7%D9%84%D8%AA%D8%A7%D8%B1%D9%8A%D8%AE-%D9%84%D9%85%D8%AC%D9%85%D9%88%D8%B9/6987499" rel="noopener" target="_blank">اليوم السابع (القرار)</a> · <a href="https://gate.ahram.org.eg/News/5897604.aspx" rel="noopener" target="_blank">بوابة الأهرام (منهج البكالوريا)</a> · <a href="https://www.elwatannews.com/news/details/8348692" rel="noopener" target="_blank">الوطن</a>. Abdelkriem Academy is independent and not affiliated with the Egyptian Ministry of Education.</p>
</div></section>'''
page("identity-subjects.html", "Arabic & History for IG, American Diploma and Baccalaureate · العربي والتاريخ — Abdelkriem Academy",
     "شرح منهج العربي والتاريخ الرسمي لطلبة IG والدبلومة الأمريكية وتانية بكالوريا 2026-2027: دروس وتدريبات تفاعلية وامتحانات تجريبية.", _is, "egyptian-baccalaureate.html")
EXTRA_PAGES.append("identity-subjects.html")
