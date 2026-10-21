# Convert Level 1 (root course/ files) into the levelN format for make_pdf.py
import json,os,re,shutil
S='course'; D='course/level1_pdf'; os.makedirs(D,exist_ok=True)
K=json.load(open(f'{S}/answer_key.json'))
def splitans(s): return [x.strip() for x in re.split(r' · (?=\d+\))',s)] if re.match(r'\s*1\)',s) else [s]
for i in range(1,13):
    w=json.load(open(f'{S}/week{i}.json'))
    for ex in w['exercises']:
        k=re.split(r' [—·] ',ex['title'])[0].strip()
        a=K['weeks'][str(i)].get(k,'')
        ex['answers']=splitans(a)
    json.dump(w,open(f'{D}/week{i}.json','w'),ensure_ascii=False)
for n in (1,2,3):
    c=json.load(open(f'{S}/progress_check_{n}.json'))
    lines={l[0]:l[3:] for l in K['progress_checks'][str(n)].split('\n')[1:] if len(l)>2 and l[1]==':'}
    for s in c['sections']:
        L=s['title'][:1]
        if L in lines: s['answers']=splitans(lines[L])
    json.dump(c,open(f'{D}/progress_check_{n}.json','w'),ensure_ascii=False)
E=json.load(open(f'{S}/end_pages.json'))
steps=[]
for it in E['month4_plan']['items']:
    steps+= it if isinstance(it,list) else [it]
meta={"level":1,"cefr":"A1","name_en":"From Zero","name_ar":"طوّر الإنجليزي بتاعك من الصفر",
 "tagline_en":"Start English from zero at home: words, sentences to memorise, grammar, exercises with answers and a daily listening plan.",
 "tagline_ar":"كورس إنجليزي للمبتدئين — ٣ شهور، ٣٠ دقيقة يوميًا.",
 "intro_ar":"المستوى ده لأي حد بيبدأ الإنجليزي من الصفر أو حاسس إن أساسه ضعيف. في آخر الـ١٢ أسبوع هتقدر تعرّف نفسك، وتتكلم عن عيلتك وبيتك ويومك، وتشتري وتسأل وتطلب مساعدة بالإنجليزي.",
 "can_do":["After this level you can introduce yourself and talk about your family.","After this level you can describe your home, your town and your daily routine.","After this level you can shop, order food and ask about prices.","After this level you can talk about the past and make plans for the future.","After this level you can ask for help, explain a health problem and travel."],
 "links":[{"group":"Video lessons (male teachers)","items":[{"name":"engVid — Alex","url":"https://www.engvid.com/english-teacher/alex/"},{"name":"engVid — Adam","url":"https://www.engvid.com/english-teacher/adam/"},{"name":"engVid — Benjamin","url":"https://www.engvid.com/english-teacher/benjamin/"},{"name":"engVid — James","url":"https://www.engvid.com/english-teacher/james/"}]},
          {"group":"Listening with scripts (audio)","items":[{"name":"British Council LearnEnglish — A1 listening","url":"https://learnenglish.britishcouncil.org/free-resources/listening/a1"},{"name":"British Council LearnEnglish — A1 reading","url":"https://learnenglish.britishcouncil.org/free-resources/reading/a1"},{"name":"ELLLO — beginner audio lessons","url":"https://www.elllo.org/"}]},
          {"group":"Podcasts","items":[{"name":"Easy Stories in English (podcast)","url":"https://www.easystoriesinenglish.com/"}]}],
 "end":{"title":"You Finished Level 1! What Next?","intro":E['intro'],"next_steps":steps+["Then start Level 2: Elementary."],"tip_ar":E['tip_ar']}}
json.dump(meta,open(f'{D}/meta.json','w'),ensure_ascii=False)
print('ok')
