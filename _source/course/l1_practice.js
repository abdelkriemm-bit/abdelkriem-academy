(function(){
/* Level 1 interactive practice: flashcards with sound, word quiz, sentence builder, dictation, auto-checked exercises.
   Data: <script type="application/json" id="l1-data"> {week, words:[[en,ar]], sentences:[[en,ar]], exercises:[{title, items, answers:[[alts]]|null, mode}]} */
var D;try{D=JSON.parse(document.getElementById('l1-data').textContent)}catch(e){return}
function $(s,r){return (r||document).querySelector(s)}
function el(t,c,h){var e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function norm(s){return String(s).replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').toLowerCase().replace(/[’‘`]/g,"'").replace(/[“”]/g,'"').replace(/\s+([,.!?;:])/g,'$1').replace(/[.!?]+$/,'').replace(/[,]/g,'').replace(/\s+/g,' ').trim()}
function exp(s){s=norm(s);return s.replace(/\bcan't\b/g,'cannot').replace(/\bcan not\b/g,'cannot').replace(/\bwon't\b/g,'will not').replace(/\bshan't\b/g,'shall not').replace(/n't\b/g,' not').replace(/\b(i)'m\b/g,'$1 am').replace(/\b(he|she|it|that|what|where|who|there|here|how|this)'s\b/g,'$1 is').replace(/'re\b/g,' are').replace(/'ll\b/g,' will').replace(/'ve\b/g,' have').replace(/'d\b/g,' would').replace(/\s+/g,' ')}
function same(a,b,strict){return strict?norm(a)===norm(b):exp(a)===exp(b)}
var KEY='abdelkriem-l1-w'+D.week;
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return{}}}
function save(k,v){try{var s=load();s[k]=Math.max(s[k]||0,v);localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}}
var voice=null;
function pickVoice(){try{var v=speechSynthesis.getVoices();voice=v.find(function(x){return /en-GB/i.test(x.lang)})||v.find(function(x){return /^en/i.test(x.lang)})||null}catch(e){}}
if('speechSynthesis' in window){pickVoice();try{speechSynthesis.onvoiceschanged=pickVoice}catch(e){}}
function say(t,rate){if(!('speechSynthesis' in window))return;try{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t.replace(/—/g,','));u.lang='en-GB';if(voice)u.voice=voice;u.rate=rate||0.9;speechSynthesis.speak(u)}catch(e){}}
var canSay='speechSynthesis' in window;
function spk(t){return canSay?'<button type="button" class="l1-say" data-say="'+esc(t)+'" aria-label="Listen">🔊</button>':''}
document.addEventListener('click',function(e){var b=e.target.closest('.l1-say');if(b){e.preventDefault();say(b.getAttribute('data-say'))}});
var root=$('#l1-practice');
var tabs=[['cards','Flashcards','بطاقات الكلمات'],['quiz','Word quiz','اختبار الكلمات'],['build','Build the sentence','رتّب الجملة'],['dict','Listen and write','اسمع واكتب']];
if(!canSay)tabs=tabs.filter(function(t){return t[0]!=='dict'});
var bar=el('div','l1-tabs');var pane=el('div','l1-pane');if(root){root.appendChild(bar);root.appendChild(pane);}
if(root)tabs.forEach(function(t,i){var b=el('button','l1-tab','<b>'+t[1]+'</b><span lang="ar">'+t[2]+'</span>');b.type='button';b.onclick=function(){bar.querySelectorAll('.l1-tab').forEach(function(x){x.classList.toggle('on',x===b)});MODES[t[0]]()};bar.appendChild(b);if(!i)setTimeout(function(){b.click()},0)});
function done(name,score,max,again){var p=Math.round(score*100/max);save(name,p);var h='<div class="l1-done"><b>'+score+' / '+max+'</b><p>'+(p===100?'Excellent! ممتاز 👏':p>=70?'Very good! كويس جدًا — راجع اللي غلطت فيه':'Keep practising. راجع الكلمات وجرّب تاني')+'</p></div>';pane.innerHTML=h;var b=el('button','btn','Try again · جرّب تاني');b.type='button';b.onclick=again;pane.appendChild(b)}
var MODES={
 cards:function(){var deck=D.words.slice(),i=0,showAr=false,known=0;
  function draw(){if(i>=deck.length){done('cards',known,deck.length,MODES.cards);return}var w=deck[i];
   pane.innerHTML='<p class="l1-help" lang="ar" dir="rtl">اسمع الكلمة وقولها بصوت عالي، وفكّر في معناها، وبعدين دوس على البطاقة عشان تشوف المعنى.</p><div class="l1-count">'+(i+1)+' / '+deck.length+'</div>';
   var c=el('button','l1-card'+(showAr?' flip':''),'<span class="en" lang="en">'+esc(w[0])+'</span>'+(showAr?'<span class="ar" lang="ar">'+esc(w[1])+'</span>':'<small>Tap to see the meaning · دوس تشوف المعنى</small>'));c.type='button';c.onclick=function(){showAr=!showAr;draw()};pane.appendChild(c);
   var r=el('div','l1-row');r.innerHTML=spk(w[0]);
   var no=el('button','l1-b','Again · لسه');no.type='button';no.onclick=function(){deck.push(w);i++;showAr=false;draw()};
   var yes=el('button','l1-b l1-p','I knew it ✓ · عرفتها');yes.type='button';yes.onclick=function(){known++;i++;showAr=false;draw()};
   r.appendChild(no);r.appendChild(yes);pane.appendChild(r);if(!showAr)say(w[0])}
  deck=shuffle(deck);draw()},
 quiz:function(){var qs=shuffle(D.words).slice(0,Math.min(10,D.words.length)),i=0,sc=0;
  function draw(){if(i>=qs.length){done('quiz',sc,qs.length,MODES.quiz);return}var w=qs[i],rev=i%2===1;
   var others=shuffle(D.words.filter(function(x){return x!==w})).slice(0,3);var opts=shuffle([w].concat(others));
   pane.innerHTML='<div class="l1-count">'+(i+1)+' / '+qs.length+' · Score '+sc+'</div><p class="l1-qq">'+(rev?'<span lang="ar" dir="rtl">'+esc(w[1])+'</span><small>Choose the English word · اختار الكلمة الإنجليزي</small>':'<span lang="en">'+esc(w[0])+'</span> '+spk(w[0])+'<small>What does it mean? · معناها إيه؟</small>')+'</p>';
   var g=el('div','l1-opts');opts.forEach(function(o){var b=el('button','l1-opt',esc(rev?o[0]:o[1]));b.type='button';if(!rev)b.lang='ar';b.onclick=function(){if(g.dataset.done)return;g.dataset.done=1;var ok=o===w;if(ok)sc++;b.classList.add(ok?'ok':'no');g.querySelectorAll('.l1-opt').forEach(function(x,k){if(opts[k]===w)x.classList.add('ok')});if(rev||ok)say(w[0]);var n=el('button','l1-b l1-p','Next →');n.type='button';n.onclick=function(){i++;draw()};pane.appendChild(n)};g.appendChild(b)});pane.appendChild(g)}
  draw()},
 build:function(){var ss=shuffle(D.sentences),i=0,sc=0;
  function draw(){if(i>=ss.length){done('build',sc,ss.length,MODES.build);return}var s=ss[i];var words=s[0].split(/\s+/);var pool=shuffle(words.map(function(w,k){return{w:w,k:k}}));var line=[];
   pane.innerHTML='<div class="l1-count">'+(i+1)+' / '+ss.length+' · Score '+sc+'</div><p class="l1-help" lang="ar" dir="rtl">رتّب الكلمات عشان تعمل الجملة دي: <b>'+esc(s[1])+'</b></p>';
   var ln=el('div','l1-line');var pl=el('div','l1-pool');var fb=el('div','l1-fb');pane.appendChild(ln);pane.appendChild(pl);
   function upd(){ln.innerHTML='';pl.innerHTML='';line.forEach(function(t,k){var b=el('button','l1-w on',esc(t.w));b.type='button';b.onclick=function(){line.splice(k,1);pool.push(t);upd()};ln.appendChild(b)});if(!line.length)ln.innerHTML='<span class="l1-ph">Tap the words below in the right order · دوس على الكلمات بالترتيب</span>';pool.forEach(function(t,k){var b=el('button','l1-w',esc(t.w));b.type='button';b.onclick=function(){pool.splice(k,1);line.push(t);upd()};pl.appendChild(b)})}
   upd();var r=el('div','l1-row');var c=el('button','l1-b l1-p','Check · صحّح');c.type='button';
   c.onclick=function(){var got=line.map(function(t){return t.w}).join(' ');var ok=norm(got)===norm(s[0]);fb.className='l1-fb '+(ok?'ok':'no');fb.innerHTML=(ok?'✓ Correct! صح':'✗ The right order is · الترتيب الصح:')+'<br><b lang="en">'+esc(s[0])+'</b> '+spk(s[0]);if(ok&&!c.dataset.done)sc++;c.dataset.done=1;say(s[0]);c.style.display='none';var n=el('button','l1-b l1-p','Next →');n.type='button';n.onclick=function(){i++;draw()};r.appendChild(n)};
   r.appendChild(c);pane.appendChild(r);pane.appendChild(fb)}
  draw()},
 dict:function(){var ss=shuffle(D.sentences).slice(0,6),i=0,sc=0;
  function draw(){if(i>=ss.length){done('dict',sc,ss.length,MODES.dict);return}var s=ss[i];
   pane.innerHTML='<div class="l1-count">'+(i+1)+' / '+ss.length+' · Score '+sc+'</div><p class="l1-help" lang="ar" dir="rtl">اسمع الجملة (تقدر تسمعها كذا مرة، أو أبطأ) واكتبها بالإنجليزي.</p>';
   var r=el('div','l1-row');var p1=el('button','l1-b','🔊 Listen');p1.type='button';p1.onclick=function(){say(s[0])};var p2=el('button','l1-b','🐢 Slower');p2.type='button';p2.onclick=function(){say(s[0],0.6)};r.appendChild(p1);r.appendChild(p2);pane.appendChild(r);
   var inp=el('input','l1-in');inp.type='text';inp.autocomplete='off';inp.setAttribute('autocapitalize','off');inp.placeholder='Write what you hear';pane.appendChild(inp);
   var fb=el('div','l1-fb');var c=el('button','l1-b l1-p','Check · صحّح');c.type='button';var r2=el('div','l1-row');r2.appendChild(c);pane.appendChild(r2);pane.appendChild(fb);
   c.onclick=function(){var ok=same(inp.value,s[0]);if(ok&&!c.dataset.done)sc++;c.dataset.done=1;fb.className='l1-fb '+(ok?'ok':'no');fb.innerHTML=(ok?'✓ Correct! صح':'✗ Not quite · قريب، بص على الصح:')+'<br><b lang="en">'+esc(s[0])+'</b><br><span lang="ar" dir="rtl">'+esc(s[1])+'</span>';c.style.display='none';var n=el('button','l1-b l1-p','Next →');n.type='button';n.onclick=function(){i++;draw()};r2.appendChild(n)};
   inp.onkeydown=function(e){if(e.key==='Enter')c.click()};setTimeout(function(){say(s[0])},300)}
  draw()}
};
/* exercises: auto-check */
document.querySelectorAll('.ex[data-ex]').forEach(function(box){var X=D.exercises[+box.dataset.ex];if(!X||!X.answers)return;
 var ol=box.querySelector('ol');if(!ol)return;var lis=ol.querySelectorAll('li');
 lis.forEach(function(li,k){if(!X.answers[k])return;var inp=el('input','l1-in sm');inp.type='text';inp.autocomplete='off';inp.setAttribute('autocapitalize','off');inp.setAttribute('aria-label','Answer '+(k+1));inp.dir='auto';inp.placeholder=X.mode==='open'?'Write the full sentence':'Your answer';var fb=el('div','l1-ifb');li.appendChild(inp);li.appendChild(fb)});
 var r=el('div','l1-row');var c=el('button','l1-b l1-p','Check my answers · صحّح');c.type='button';var sco=el('span','l1-score');r.appendChild(c);r.appendChild(sco);
 var det=box.querySelector('details');box.insertBefore(r,det||null);
 c.onclick=function(){var sc=0,n=0;lis.forEach(function(li,k){var A=X.answers[k];if(!A)return;n++;var inp=li.querySelector('.l1-in'),fb=li.querySelector('.l1-ifb');var v=inp.value;var ok=v.trim()&&A.some(function(a){return same(a,v,X.strict)});
   li.classList.remove('ok','no','self');
   if(ok){sc++;li.classList.add('ok');fb.innerHTML='✓'}
   else if(X.mode==='open'&&v.trim()){li.classList.add('self');fb.innerHTML='Model answer: <b lang="en">'+esc(A[0])+'</b> <span lang="ar" dir="rtl">— لو إجابتك نفس المعنى ومن غير أخطاء، اعتبرها صح</span> <button type="button" class="l1-b sm">Mine is correct ✓</button>';var bb=fb.querySelector('button');bb.onclick=function(){li.classList.remove('self');li.classList.add('ok');fb.innerHTML='✓';recount()}}
   else{li.classList.add('no');fb.innerHTML='✗ Correct answer: <b lang="en">'+esc(A.join(' / '))+'</b>'}});
  function recount(){var s=box.querySelectorAll('li.ok').length;sco.textContent=s+' / '+n;save('ex'+box.dataset.ex,Math.round(s*100/n));var T=$('#l1-total');if(T){var all=0,ok=0;document.querySelectorAll('.ex[data-ex]').forEach(function(b){var Y=D.exercises[+b.dataset.ex];if(Y&&Y.answers){all+=Y.answers.length;ok+=b.querySelectorAll('li.ok').length}});T.innerHTML='Your score · درجتك: <b>'+ok+' / '+all+'</b>'+(ok>=Math.round(all*0.8)?' — ممتاز، تقدر تكمّل 👏':' — راجع جمل الأسابيع دي 3 أيام وجرّب تاني')}}
  recount()};
});
})();
