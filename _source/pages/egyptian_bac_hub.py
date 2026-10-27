# Egyptian Baccalaureate hub (egyptian-baccalaureate.html): one card per subject; English is the first subject.
_eb = TILE_CSS + pagehead("Section 3", "Egyptian Baccalaureate · البكالوريا المصرية",
  "Free study material for the new Egyptian Baccalaureate (البكالوريا المصرية), organised by subject and year.") + f'''
<section class="block"><div class="wrap"><div class="tiles">
{tile("English","baccalaureate.html","تانية بكالوريا","92 lessons · the whole curriculum")}
{tile("Parents' guide","parents-the-new-baccalaureate.html","دليل لولي الأمر","The new Baccalaureate explained")}
</div></div></section>
<section class="block alt"><div class="wrap prose" dir="rtl" lang="ar">
<h2>البكالوريا المصرية</h2>
<p>هنا هتلاقي شرح مواد البكالوريا المصرية مادة مادة. ابدأ بكورس الإنجليزي لتانية بكالوريا: كل درس فيه شرح بالعربي والإنجليزي، وأمثلة، وأسئلة بالإجابات.</p>
</div></section>'''
page("egyptian-baccalaureate.html", "Egyptian Baccalaureate · البكالوريا المصرية — Abdelkriem Academy",
     "Free study material for the Egyptian Baccalaureate (البكالوريا المصرية): the complete English course for the second year and a guide for parents.", _eb, "egyptian-baccalaureate.html")
EXTRA_PAGES.append("egyptian-baccalaureate.html")
