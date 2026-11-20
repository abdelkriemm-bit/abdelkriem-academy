"""Blind-check helper.
make:    python3 blind.py make FILE OUTDIR   -> OUTDIR/<name>.blind.txt (no keys) + OUTDIR/<name>.key.json
compare: python3 blind.py compare OUTDIR/<name>.key.json ANSWERS.json  (answers: {"id": "B", ...})
"""
import sys, json, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import practice_dsl as P

def items(fn):
    if fn.endswith('.txt'):
        d = P.parse(open(fn).read(), os.path.basename(fn))
        for si, st in enumerate(d['sets'], 1):
            for qi, q in enumerate(st['questions'], 1):
                yield f"P{si}-{qi}", q
    else:
        d = json.load(open(fn))
        t = [b for b in d['blocks'] if b['type'] == 'test'][0]
        for si, sec in enumerate(t['sections'], 1):
            for qi, q in enumerate(sec['questions'], 1):
                yield f"S{si}-{qi}", q

if sys.argv[1] == 'make':
    fn, out = sys.argv[2], sys.argv[3]
    name = os.path.basename(fn).rsplit('.', 1)[0]
    lines, key, lastp = [], {}, None
    for i, q in items(fn):
        p = q.get('p', '')
        if p and p != lastp:
            lines.append('=' * 60 + '\nPASSAGE\n' + p + '\n' + '=' * 60)
            lastp = p
        lines.append(f"[{i}] {q['q']}\n" + '\n'.join(f"  {'ABCD'[j]}) {c}" for j, c in enumerate(q['c'])))
        key[i] = 'ABCD'[q['a']]
    open(f"{out}/{name}.blind.txt", 'w').write('\n\n'.join(lines))
    json.dump(key, open(f"{out}/{name}.key.json", 'w'))
    print(name, len(key))
else:
    key = json.load(open(sys.argv[2])); ans = json.load(open(sys.argv[3]))
    bad = [(k, key[k], ans.get(k)) for k in key if (ans.get(k) or '').strip()[:1].upper() != key[k]]
    print(f"{len(key)-len(bad)}/{len(key)} agree")
    for k, a, b in bad: print('  MISMATCH', k, 'key', a, 'reviewer', b)
