import sys, json, os, re, importlib
sys.path.insert(0, '/tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/quran')
import qdata
from tj_lib import deep_fill, plain
OUT = '/tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/quran/tajweed'
os.makedirs(OUT, exist_ok=True)
parts = [p for p in sys.argv[1:]] or ['tj_part1', 'tj_part2', 'tj_part3', 'tj_part4']
lessons = []
for p in parts:
    lessons += importlib.import_module(p).L
errs = []
HARAKA = re.compile('[ً-ْ]')
for L in lessons:
    L = deep_fill(L)
    n = L['n']
    if not 3 <= len(L['explain']) <= 6: errs.append(f'{n} explain count {len(L["explain"])}')
    if not 6 <= len(L['examples']) <= 10: errs.append(f'{n} examples count {len(L["examples"])}')
    if len(L['plan']) != 7: errs.append(f'{n} plan')
    if len(L['exercises']) != 3: errs.append(f'{n} exercises count')
    for ex in L['exercises']:
        if len(ex['items']) != len(ex['answers']): errs.append(f'{n} ex {ex["title"]} items/answers mismatch')
    for e in L['examples']:
        if qdata.skel(e['word']) not in qdata.skel(qdata.ayah_text(e['surah'], e['ayah'])):
            errs.append(f'{n} example not in ayah {e}')
        if e['word'] not in qdata.ayah_text(e['surah'], e['ayah']):
            errs.append(f'{n} example not exact substring {e}')
    for row in L.get('table', {}).get('rows', []):
        for c in row:
            pass
    if '⟦' in json.dumps(L, ensure_ascii=False): errs.append(f'{n} unfilled placeholder')
    s = json.dumps(L, ensure_ascii=False, indent=1)
    for bad in ['Claude', 'AI', 'ذكاء اصطناعي', 'أستاذ', 'Mr.']:
        if bad in s: errs.append(f'{n} contains {bad}')
    path = f'{OUT}/lesson{n}.json'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    json.load(open(path, encoding='utf-8'))
print('lessons:', [L['n'] for L in lessons])
print('ERRORS:', *errs, sep='\n') if errs else print('OK no errors')

# attach listening resources from RESOURCES.json
R = json.load(open('/tmp/claude-0/-home-claude/a1e5b1ed-f2bf-5151-9b67-9108ca954997/scratchpad/quran/RESOURCES.json'))
ep = R['tajweed_videos']['episodes']
M = {1:[0],2:[1],3:[2,3],4:[4,5],5:[6],6:[7,8],7:[9],8:[10],9:[11],10:[12],11:[13,18],12:[14,18],13:[15,16,17],14:[19,20],15:[21],16:[22,23]}
for n, ix in M.items():
    p = f'{OUT}/lesson{n}.json'
    if not os.path.exists(p): continue
    L = json.load(open(p))
    L['listen'] = [ep[i]['title'] + ' (video)' for i in ix] + [R['reciters'][0]['name'] + ' (audio)']
    open(p, 'w', encoding='utf-8').write(json.dumps(L, ensure_ascii=False, indent=1))
