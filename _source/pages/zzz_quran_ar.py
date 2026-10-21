# Quran section pages: whole page in Arabic (header, footer, titles). Only the word "Quran" stays in English in the menu.
import glob as _g3
_AR = [
 ('<html lang="en">', '<html lang="ar" dir="rtl">'),
 ('<b>Abdelkriem Academy</b><small>Educate Me Up</small>', '<b>أكاديمية عبد الكريم</b><small>مصادر تعليمية مجانية</small>'),
 ('<nav dir="ltr">', '<nav dir="rtl">'),
 ('>Home</a>', '>الرئيسية</a>'),
 ('>British & IGCSE</a>', '>المناهج البريطانية</a>'),
 ('>British &amp; IGCSE</a>', '>المناهج البريطانية</a>'),
 ('>English · من الصفر للاحتراف</a>', '>الإنجليزي من الصفر للاحتراف</a>'),
 ('>About</a>', '>من نحن</a>'),
 ('حمّل خطة المستوى PDF', 'حمّل خطة المستوى للطباعة'), ('حمّل الدروس كاملة PDF', 'حمّل الدروس كاملة للطباعة'), ('حمّل الدليل PDF (مع جدول متابعة للطباعة)', 'حمّل الدليل للطباعة (مع جدول متابعة)'),
 ('>تانية بكالوريا English</a>', '>إنجليزي تانية بكالوريا</a>'),
 ('<footer class="foot" dir="ltr">', '<footer class="foot" dir="rtl">'),
 ('<b>Abdelkriem Academy</b><p>Free educational resources for students and parents — Cambridge and Oxford English, the Egyptian Baccalaureate, Quran and more — by Mohamed Abdelkriem.</p>',
  '<b>أكاديمية عبد الكريم</b><p>مصادر تعليمية مجانية للطلاب وأولياء الأمور: الإنجليزي للمناهج البريطانية، والثانوية المصرية، والقرآن الكريم وغيرها — إعداد محمد عبد الكريم.</p>'),
 ('<b>Sections</b>', '<b>الأقسام</b>'), ('<b>Academy</b>', '<b>الأكاديمية</b>'), ('<b>Follow</b>', '<b>تابعنا</b>'),
 ('>Contact</a>', '>تواصل معنا</a>'), ('>Privacy Policy</a>', '>سياسة الخصوصية</a>'), ('>Terms of Use</a>', '>شروط الاستخدام</a>'),
 ('© 2026 Abdelkriem Academy · No English exam left standing.', '© 2026 أكاديمية عبد الكريم'),
 (' | Abdelkriem Academy</title>', ' | أكاديمية عبد الكريم</title>'),
 (' | Abdelkriem Academy">', ' | أكاديمية عبد الكريم">'),
 ('<span class="mark">AA</span>', '<span class="mark">ع</span>'),
] + [(f'rel="noopener">{a}</a>', f'rel="noopener">{b}</a>') for a, b in (("YouTube","يوتيوب"),("Facebook","فيسبوك"),("Instagram","إنستجرام"),("TikTok","تيك توك"))]
for _p in _g3.glob(f"{OUT}/quran*.html"):
    _h = open(_p, encoding="utf-8").read()
    for _a, _b in _AR: _h = _h.replace(_a, _b)
    open(_p, "w", encoding="utf-8").write(_h)
