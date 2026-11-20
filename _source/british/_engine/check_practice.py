import sys,glob,collections
import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import practice_dsl as P
tot=0
for f in sorted(sys.argv[1:]):
    d=P.parse(open(f).read(),f)
    n=[len(s['questions']) for s in d['sets']];tot+=sum(n)
    warn=[]
    for s in d['sets']:
        for q in s['questions']:
            if len(set(q['c']))<4: warn.append('dup:'+q['c'][0])
            if 'p' in q and '______' not in q['p'] and 'Standard English' in q['q']: warn.append('noblank:'+q['p'][:40])
            if any(x in ' '.join(q['ce']) for x in ['Wait','x ||','see below','see the key']): warn.append('junk:'+q['p'][:40])
    print(f.split('/')[-1],n,warn[:3])
print('total',tot)
