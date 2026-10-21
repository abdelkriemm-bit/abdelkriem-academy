# 404 page (Cloudflare Pages serves 404.html for missing URLs). Not listed in the sitemap.
page("404.html", "Page not found — Abdelkriem Academy", "This page does not exist.",
     pagehead("404", "Page not found · الصفحة غير موجودة", "The page you are looking for has moved or no longer exists.") +
     '<section class="block"><div class="wrap"><div class="ctas"><a class="btn" href="index.html">Go to the home page</a><a class="btn ghost" href="english-in-90-days.html">English Course</a><a class="btn ghost" href="quran.html">Quran Course</a></div></div></section>')
