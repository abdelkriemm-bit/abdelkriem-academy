import json,re,unicodedata
_U=json.load(open(__file__.rsplit('/',1)[0]+'/uthmani.json'))['data']['surahs']
_T=json.load(open(__file__.rsplit('/',1)[0]+'/tajweed.json'))['data']['surahs']
B='بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ'
MK=re.compile(r'\[([a-z])(?::\d+)?\[([^\]]*)\]')
def ayah_text(s,a):
    t=_U[s-1]['ayahs'][a-1]['text'].replace('﻿','')
    if s not in (1,9) and a==1:
        w=t.split(' ')
        if skel(w[0])=='بسم' and len(w)>4: t=' '.join(w[4:])
    return t
def meta(s,a): return _U[s-1]['ayahs'][a-1]
def surah(s): return _U[s-1]
def nayahs(s): return len(_U[s-1]['ayahs'])
def skel(w):  # base letters only for fuzzy matching
    w=unicodedata.normalize('NFKD',w)
    return ''.join(c for c in w if 'ء'<=c<='ي' or c=='ٱ').replace('ٱ','ا').replace('ى','ي').replace('ة','ه')
def parse_tajweed(t):
    """returns plain text and list of (code,start,end) spans"""
    out=[];spans=[];i=0
    while i<len(t):
        if t[i]=='[' and i+1<len(t) and t[i+1].isalpha() and t[i+1].islower():
            j=t.index('[',i+1); code=t[i+1]; k=t.index(']',j); start=len(out)
            out.extend(t[j+1:k]); spans.append((code,start,len(out))); i=k+1
        else:
            out.append(t[i]); i+=1
    return ''.join(out),spans
def tajweed_marks(s,a):
    plain,spans=parse_tajweed(_T[s-1]['ayahs'][a-1]['text'])
    res=[]
    for code,st,en in spans:
        ws=plain.rfind(' ',0,st)+1; we=plain.find(' ',en); we=len(plain) if we<0 else we
        if code in 'fiawucbdg' and plain[en:en+1]!=' ' and en==we: pass
        # include next word for rules that span a word boundary
        nx=plain.find(' ',we+1); nx=len(plain) if nx<0 else nx
        res.append((code,plain[ws:we],plain[we+1:nx] if we<len(plain) else ''))
    return res
def _old_tajweed_marks(s,a):
    """list of (code, chunk_word_skeleton) for this ayah from the tajweed edition"""
    t=_T[s-1]['ayahs'][a-1]['text']
    out=[]
    words=t.split(' ')
    for i,w in enumerate(words):
        for m in MK.finditer(w):
            plain=MK.sub(lambda x:x.group(2),w)
            nxt=MK.sub(lambda x:x.group(2),words[i+1]) if i+1<len(words) else ''
            out.append((m.group(1),plain,nxt))
    return out
SURAH_AR=[x['name'] for x in _U]
