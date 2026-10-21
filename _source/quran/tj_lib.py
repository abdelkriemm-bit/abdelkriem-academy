import sys, re, json, unicodedata
sys.path.insert(0, '/tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/quran')
import qdata

DIAC = re.compile('[ً-ٰٟۖ-ۭـ]')
def plain(t):
    return DIAC.sub('', t)

def sname(s):
    n = plain(qdata.SURAH_AR[s - 1]).replace('ٱ', 'ا').replace('سورة ', '').strip()
    n = {'النبإ': 'النبأ'}.get(n, n)
    return n

def toks(s, a):
    t = qdata.ayah_text(s, a)
    w = t.split()
    off = 0
    if s not in (1, 9) and a == 1 and [qdata.skel(x) for x in w[:4]] == ['بسم', 'الله', 'الرحمن', 'الرحيم']:
        off = 4
    return w, off

def find(s, a, key):
    """return exact text copied from qdata.ayah_text for the key (skeleton words or #index)"""
    w, off = toks(s, a)
    if key.startswith('#'):
        parts = key[1:].split('-')
        i = int(parts[0]) + off
        j = int(parts[-1]) + off
        return ' '.join(w[i:j + 1])
    ks = [qdata.skel(k) for k in key.split()]
    idx = [i for i in range(off, len(w)) if qdata.skel(w[i])]
    for p in range(len(idx) - len(ks) + 1):
        if all(qdata.skel(w[idx[p + q]]) == ks[q] for q in range(len(ks))):
            return ' '.join(w[idx[p]:idx[p + len(ks) - 1] + 1])
    raise ValueError(f'NOT FOUND {s}:{a} {key!r} in {qdata.ayah_text(s, a)}  skels={[qdata.skel(x) for x in w]}')

def E(s, a, key, note):
    return {'surah': s, 'ayah': a, 'word': find(s, a, key), 'note': note}

PH = re.compile(r'⟦(\d+):(\d+):([^⟧]+)⟧')
def fill(text):
    return PH.sub(lambda m: f'«{find(int(m.group(1)), int(m.group(2)), m.group(3))}» ({sname(int(m.group(1)))}: {m.group(2)})', text)

def deep_fill(o):
    if isinstance(o, str):
        return fill(o)
    if isinstance(o, list):
        return [deep_fill(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in ('word',) else deep_fill(v)) for k, v in o.items()}
    return o
