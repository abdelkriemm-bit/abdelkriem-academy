# Social links — runs last inside build.py and adds the accounts to every page (footer, home strip, contact page).
# To add or change an account, edit SOCIAL only. An empty link is skipped.
import glob as _glob, re as _re

SOCIAL = [
 ("YouTube", "https://www.youtube.com/@mr.mohamedabdelkriem", "@mr.mohamedabdelkriem", "Video lessons and story summaries"),
 ("Facebook", "https://www.facebook.com/educatemeup", "Mr.Mohamed Abdelkriem", "Tips and news for parents"),
 ("Instagram", "https://www.instagram.com/mr.mohamedabdelkriem/", "@mr.mohamedabdelkriem", "Daily posts and reels"),
 ("TikTok", "https://www.tiktok.com/search/user?q=Mr%20Mohamed%20Abdelkriem", "Mr Mohamed Abdelkriem", "Short lessons and exam tips"),
]
_LIVE = [s for s in SOCIAL if s[1]]
EMAIL = "abdelkriemacademy@gmail.com"

_ICONS = {
 "YouTube": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15.1V8.9L15.5 12z"/></svg>',
 "Facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.4 1.5-1.4h1.5V4.5c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2.3H8v3h2.6V21z"/></svg>',
 "Instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 16.7 12 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 3-3 3 3 0 0 1-3 3zm6-7.9a1.1 1.1 0 1 1-1.1-1.1A1.1 1.1 0 0 1 18 7.1zM21.5 7a5.5 5.5 0 0 0-1.5-3.9A5.5 5.5 0 0 0 16.1 1.6C14.5 1.5 9.5 1.5 7.9 1.6A5.5 5.5 0 0 0 4 3.1 5.5 5.5 0 0 0 2.5 7c-.1 1.6-.1 6.5 0 8.1A5.5 5.5 0 0 0 4 19a5.5 5.5 0 0 0 3.9 1.5c1.6.1 6.6.1 8.2 0A5.5 5.5 0 0 0 20 19a5.5 5.5 0 0 0 1.5-3.9c.1-1.6.1-6.5 0-8.1zm-2.1 9.8a3.2 3.2 0 0 1-1.8 1.8c-1.3.5-4.3.4-5.6.4s-4.3.1-5.6-.4a3.2 3.2 0 0 1-1.8-1.8c-.5-1.3-.4-4.3-.4-5.6s-.1-4.3.4-5.6a3.2 3.2 0 0 1 1.8-1.8c1.3-.5 4.3-.4 5.6-.4s4.3-.1 5.6.4a3.2 3.2 0 0 1 1.8 1.8c.5 1.3.4 4.3.4 5.6s.1 4.3-.4 5.6z"/></svg>',
 "TikTok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.2v12.4a2.6 2.6 0 1 1-2.6-2.6 2.7 2.7 0 0 1 .8.1V9.6a5.8 5.8 0 0 0-.8-.1 5.9 5.9 0 1 0 5.9 5.9V9a7.5 7.5 0 0 0 4.4 1.4V7.2a4.3 4.3 0 0 1-3.4-1.4z"/></svg>',
}

_SOCIAL_CSS = """<style>
.social-strip{background:var(--navy);color:#fff;padding:56px 0}
.social-strip h2{color:#fff;margin-bottom:6px}
.social-strip .sub{color:#c9d1e3;margin:0 0 24px}
.soc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.soc{display:flex;align-items:center;gap:14px;text-decoration:none;background:rgba(255,255,255,.06);border:1px solid rgba(212,162,76,.35);border-radius:16px;padding:16px 18px;color:#fff;transition:transform .15s,border-color .15s}
.soc:hover{transform:translateY(-3px);border-color:var(--gold)}
.soc svg{flex:none;width:36px;height:36px;fill:var(--gold)}
.soc b{display:block;font-size:1.05rem}
.soc span{display:block;color:#c9d1e3;font-size:.88rem}
.soc small{display:block;color:var(--gold);font-size:.8rem}
.foot .fsoc{display:flex;gap:10px;margin-top:8px}
.foot .fsoc a{display:grid;place-items:center;width:36px;height:36px;border-radius:10px;background:rgba(255,255,255,.08);padding:0}
.foot .fsoc svg{width:18px;height:18px;fill:#c9d1e3}
.foot .fsoc a:hover svg{fill:var(--gold)}
.contact-soc{display:grid;gap:10px;margin-top:18px}
.contact-soc a{display:flex;align-items:center;gap:12px;text-decoration:none;border:1px solid var(--line);background:var(--card);border-radius:12px;padding:12px 16px}
.contact-soc svg{width:24px;height:24px;fill:var(--gold-2);flex:none}
</style>"""

def _strip():
    cards = "".join(f'<a class="soc" href="{u}" target="_blank" rel="noopener">{_ICONS[n]}<span><b>{n}</b><small>{h}</small><span>{d}</span></span></a>' for n, u, h, d in _LIVE)
    return f'<section class="social-strip" dir="ltr"><div class="wrap"><h2>Follow Mohamed Abdelkriem</h2><p class="sub">New lessons, tips and exam updates on every platform.</p><div class="soc-grid">{cards}</div></div></section>'

_foot_links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u, _, _ in _LIVE)
_foot_icons = '<div class="fsoc">' + "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{_ICONS[n]}</a>' for n, u, _, _ in _LIVE) + '</div>'
_contact = '<div class="contact-soc">' + "".join(f'<a href="{u}" target="_blank" rel="noopener">{_ICONS[n]}<span><b>{n}</b> · {h}</span></a>' for n, u, h, _ in _LIVE) + '</div>'

for _path in _glob.glob(f"{OUT}/*.html"):
    _h = open(_path, encoding="utf-8").read()
    _h = _re.sub(r'<div><b>Follow</b>.*?</div>\n</div><p class="copy">', f'<div><b>Follow</b>{_foot_links}{_foot_icons}</div>\n</div><p class="copy">', _h, count=1, flags=_re.S)
    _h = _h.replace("</main>", "</main>" + _SOCIAL_CSS, 1) if _SOCIAL_CSS not in _h else _h
    if _path.endswith("/index.html"):
        _h = _h.replace("</main>", _strip() + "</main>", 1)
    if _path.endswith("/contact.html"):
        _h = _re.sub(r'<p><b>YouTube:</b>.*?</p>', '<p><b>Follow us:</b> leave a comment on any post or video to request a topic.</p>' + _contact, _h, count=1, flags=_re.S)
    _h = _h.replace("contact@abdelkriemacademy.com", EMAIL)
    open(_path, "w", encoding="utf-8").write(_h)
