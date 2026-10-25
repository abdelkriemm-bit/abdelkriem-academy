(function(){
/* Practice-test engine. Question types (field "t"):
   mcq (default): c[] choices, a = index of key
   num: typed number; ans = [accepted values] (numbers or "a/b" strings), tol = absolute tolerance, unit = shown after the box
   text: typed word/short answer; ans = [accepted answers] (case and extra spaces ignored)
   open: written answer marked by the student against the mark scheme "ms"
   Common: p (stem/passage), q (question), img (inline SVG), m (marks, default 1), e (explanation / worked solution), s (skill) */
function el(t,c,h){var e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]}).replace(/_{3,}/g,'\u0001').replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/__(.+?)__/g,'<u>$1</u>').replace(/\^\{(.+?)\}/g,'<sup>$1</sup>').replace(/_\{(.+?)\}/g,'<sub>$1</sub>').replace(/\u0001/g,'<span class="pt-blank">&nbsp;</span>').replace(/\n/g,'<br>')}
function svg(s){return s&&/^\s*<svg[\s>]/i.test(s)&&!/<script|on\w+=/i.test(s)?'<div class="pt-img">'+s+'</div>':''}
function fmt(s){var m=Math.floor(s/60),x=s%60;return m+':'+(x<10?'0':'')+x}
function ty(Q){return Q.t||'mcq'}
function mk(Q){return Q.m||1}
function blank(Q,a){return ty(Q)==='mcq'?!(a>=0):(a==null||String(a).trim()==='')}
function toNum(v){v=String(v).replace(/[,\s]/g,'').replace(/[−–]/g,'-').replace(/[^0-9.\/\-]/g,'');if(!v)return NaN;var f=v.split('/');if(f.length===2){var n=parseFloat(f[0]),d=parseFloat(f[1]);return d?n/d:NaN}return f.length>2?NaN:Number(v)}
function norm(v){return String(v).toLowerCase().replace(/[.,;:!?"'’]/g,'').replace(/\s+/g,' ').trim()}
function auto(Q,a){var t=ty(Q);if(blank(Q,a))return false;
 if(t==='mcq')return a===Q.a;
 if(t==='num'){var x=toNum(a);if(isNaN(x))return false;var tol=Q.tol||1e-9;return (Q.ans||[]).some(function(v){var y=typeof v==='number'?v:toNum(v);return Math.abs(x-y)<=tol+1e-9})}
 if(t==='text'){var n=norm(a);return (Q.ans||[]).some(function(v){return norm(v)===n})}
 return false}
document.querySelectorAll('.ptest').forEach(function(box){
 var T=JSON.parse(box.querySelector('script[type="application/json"]').textContent);
 var timed=T.timed!==false, si=0, qi=0, ans=[], left=0, tick=null, flags=[], self=[];
 var hasMarks=T.sections.some(function(s){return s.questions.some(function(Q){return Q.m||Q.t})});
 function reset(){ans=T.sections.map(function(s){return s.questions.map(function(Q){return ty(Q)==='mcq'?-1:''})});flags=T.sections.map(function(s){return s.questions.map(function(){return false})});self=T.sections.map(function(s){return s.questions.map(function(){return 0})})}
 reset();
 var stage=el('div','pt-stage');box.appendChild(stage);
 function intro(){
  stage.innerHTML='';
  var n=T.sections.reduce(function(a,s){return a+s.questions.length},0);
  var mt=T.sections.reduce(function(a,s){return a+s.questions.reduce(function(b,Q){return b+mk(Q)},0)},0);
  var h='<div class="pt-intro"><b>'+esc(T.title)+'</b><p>'+n+' questions'+(hasMarks?' · '+mt+' marks':'')+(timed?' · '+T.sections.map(function(s){return esc(s.name)+': '+s.minutes+' min'+(s.calc===false?' (no calculator)':s.calc===true?' (calculator allowed)':'')}).join(' · '):'')+'</p>';
  if(T.intro)h+='<p>'+esc(T.intro)+'</p>';
  if(T.pdf)h+='<p class="pt-pdf">'+T.pdf.map(function(x){return '<a href="'+esc(x.href)+'" target="_blank" rel="noopener">'+esc(x.label)+'</a>'}).join(' · ')+'</p>';
  h+='</div>';stage.innerHTML=h;
  var b=el('button','btn pt-go','Start');b.type='button';b.onclick=function(){si=0;qi=0;startSection()};stage.appendChild(b);
 }
 function startSection(){
  left=T.sections[si].minutes*60; render();
  clearInterval(tick); if(timed){tick=setInterval(function(){left--;var c=stage.querySelector('.pt-clock');if(c){c.textContent=fmt(Math.max(left,0));if(left<=60)c.classList.add('low')}if(left<=0){clearInterval(tick);endSection(true)}},1000)}
 }
 function render(){
  var S=T.sections[si],Q=S.questions[qi];var op=stage.querySelector('.pt-pass'),ok=stage.getAttribute('data-k'),nk=si+':'+qi,ost=op?op.scrollTop:0,wy=window.scrollY;stage.style.minHeight=stage.offsetHeight+'px';stage.innerHTML='';stage.setAttribute('data-k',nk);
  var top=el('div','pt-top','<span>'+esc(S.name)+' · Question '+(qi+1)+' of '+S.questions.length+(hasMarks?' · ['+mk(Q)+' mark'+(mk(Q)>1?'s':'')+']':'')+'</span>'+(timed?'<span class="pt-clock">'+fmt(left)+'</span>':''));stage.appendChild(top);
  var two=Q.p&&String(Q.p).length>400;
  var body=el('div','pt-body'+(two?' two':''));
  if(Q.p)body.appendChild(el('div','pt-pass'+(two?'':' stem'),esc(Q.p)));
  var right=el('div','pt-q');if(Q.img)right.appendChild(el('div','',svg(Q.img)));right.appendChild(el('p','pt-qt',esc(Q.q)));
  var t=ty(Q);
  if(t==='mcq'){var ul=el('div','pt-ch');
   Q.c.forEach(function(c,i){var b=el('button','pt-c'+(ans[si][qi]===i?' on':''),'<span>'+'ABCD'[i]+'</span><div>'+esc(c)+'</div>');b.type='button';b.onclick=function(){ans[si][qi]=i;render()};ul.appendChild(b)});
   right.appendChild(ul)}
  else{var w=el('div','pt-in');var inp;
   if(t==='open'){inp=el('textarea','pt-ta');inp.rows=4;inp.placeholder='Write your answer here'}
   else{inp=el('input','pt-tx');inp.type='text';inp.autocomplete='off';inp.placeholder=t==='num'?'Type a number':'Type your answer';if(t==='num')inp.inputMode='decimal'}
   inp.value=ans[si][qi];inp.oninput=function(){ans[si][qi]=inp.value;var g=stage.querySelectorAll('.pt-g')[qi];if(g)g.classList.toggle('ans',!blank(Q,inp.value))};
   w.appendChild(inp);if(Q.unit)w.appendChild(el('span','pt-unit',esc(Q.unit)));right.appendChild(w);
   if(t==='num')right.appendChild(el('small','pt-hint','Numbers only. Fractions like 3/4 are accepted.'));
   if(t==='open')right.appendChild(el('small','pt-hint','You will mark this answer yourself against the mark scheme at the end.'))}
  body.appendChild(right);stage.appendChild(body);
  var nav=el('div','pt-nav');
  var pr=el('button','pt-b','← Back');pr.type='button';pr.disabled=qi===0;pr.onclick=function(){qi--;render()};
  var fl=el('button','pt-b'+(flags[si][qi]?' fl':''),flags[si][qi]?'Marked for review':'Mark for review');fl.type='button';fl.onclick=function(){flags[si][qi]=!flags[si][qi];render()};
  var nx=el('button','pt-b pt-p',qi<S.questions.length-1?'Next →':(si<T.sections.length-1?'Finish this section':'Finish test'));nx.type='button';
  nx.onclick=function(){if(qi<S.questions.length-1){qi++;render()}else endSection(false)};
  nav.appendChild(pr);nav.appendChild(fl);nav.appendChild(nx);stage.appendChild(nav);
  var grid=el('div','pt-grid');S.questions.forEach(function(G,i){var g=el('button','pt-g'+(i===qi?' cur':'')+(!blank(G,ans[si][i])?' ans':'')+(flags[si][i]?' fl':''),String(i+1));g.type='button';g.onclick=function(){qi=i;render()};grid.appendChild(g)});stage.appendChild(grid);stage.style.minHeight='';
  var np=stage.querySelector('.pt-pass');if(np){if(ok===nk)np.scrollTop=ost;else{var u=np.querySelector('u');np.scrollTop=u?Math.max(0,u.offsetTop-np.offsetTop-60):0}}if(ok===nk)window.scrollTo(0,wy);
 }
 function endSection(auto_){
  var S=T.sections[si];var bl=S.questions.filter(function(Q,i){return blank(Q,ans[si][i])}).length;
  if(!auto_&&bl&&!stage.querySelector('.pt-warn')){var w=el('p','pt-warn','You have '+bl+' unanswered question'+(bl>1?'s':'')+'. Press the button again to finish anyway.');stage.appendChild(w);return}
  clearInterval(tick);
  if(si<T.sections.length-1){si++;qi=0;stage.innerHTML='';stage.appendChild(el('div','pt-intro','<b>'+esc(T.sections[si-1].name)+' finished.</b><p>Next: '+esc(T.sections[si].name)+(timed?' ('+T.sections[si].minutes+' minutes)':'')+'</p>'));var b=el('button','btn pt-go','Start '+esc(T.sections[si].name));b.type='button';b.onclick=startSection;stage.appendChild(b);return}
  results();
 }
 function score(k,i){var Q=T.sections[k].questions[i];return ty(Q)==='open'?self[k][i]:(auto(Q,ans[k][i])?mk(Q):0)}
 function totals(){var out={sec:[],tot:0,max:0,sk:{}};T.sections.forEach(function(S,k){var c=0,m=0;S.questions.forEach(function(Q,i){var g=score(k,i);c+=g;m+=mk(Q);var s=Q.s||'Other';out.sk[s]=out.sk[s]||[0,0];out.sk[s][0]+=g;out.sk[s][1]+=mk(Q)});out.sec.push([c,m]);out.tot+=c;out.max+=m});return out}
 function scoreHtml(){var o=totals(),u=hasMarks?' marks':'';var h='';T.sections.forEach(function(S,k){h+='<div><small>'+esc(S.name)+'</small><b>'+o.sec[k][0]+' / '+o.sec[k][1]+'</b></div>'});
  h+='<div class="all"><small>Total'+u+'</small><b>'+o.tot+' / '+o.max+'</b><small>'+Math.round(o.tot*100/o.max)+'%</small></div>';
  var t='';Object.keys(o.sk).forEach(function(s){t+='<tr><td>'+esc(s)+'</td><td>'+o.sk[s][0]+' / '+o.sk[s][1]+'</td></tr>'});return [h,t]}
 function refresh(){var r=scoreHtml();var a=stage.querySelector('.pt-scores'),b=stage.querySelector('.pt-sktab');if(a)a.innerHTML=r[0];if(b)b.innerHTML=r[1]}
 function results(){
  stage.innerHTML='';var r=scoreHtml();var anyOpen=false;
  var h='<div class="pt-res"><h3>Your result</h3><div class="pt-scores">'+r[0]+'</div>';
  h+='<p class="pt-note">This is a practice score, not an official Cambridge, College Board or ACT score.</p>';
  h+='<div id="pt-open-note"></div><h4>By skill</h4><div class="tw"><table><thead><tr><th>Skill</th><th>'+(hasMarks?'Marks':'Correct')+'</th></tr></thead><tbody class="pt-sktab">'+r[1]+'</tbody></table></div><h4>Review every question</h4>';
  T.sections.forEach(function(S,k){h+='<h5>'+esc(S.name)+'</h5><ol class="pt-rev">';S.questions.forEach(function(Q,i){var a=ans[k][i],t=ty(Q),okk=auto(Q,a);
   h+='<li class="'+(t==='open'?'op':okk?'ok':'no')+'">'+(Q.p?'<div class="pt-pass sm">'+esc(Q.p)+'</div>':'')+svg(Q.img)+'<p><b>'+esc(Q.q)+'</b>'+(hasMarks?' <small>['+mk(Q)+']</small>':'')+'</p>';
   if(t==='mcq'){h+='<ul>';Q.c.forEach(function(c,j){h+='<li class="'+(j===Q.a?'right':'')+(j===a&&!okk?' wrong':'')+'">'+'ABCD'[j]+') '+esc(c)+(j===Q.a?' ✓':'')+(j===a&&!okk?' ✗ your answer':'')+'</li>'});h+='</ul>'}
   else{h+='<p class="pt-yours">Your answer: '+(blank(Q,a)?'<i>none</i>':esc(a)+(Q.unit?' '+esc(Q.unit):''))+(t!=='open'?(okk?' ✓':' ✗'):'')+'</p>';
    if(t!=='open')h+='<p class="pt-right">Correct answer: <b>'+esc((Q.ans||[]).slice(0,1).join(''))+(Q.unit?' '+esc(Q.unit):'')+'</b></p>';
    else{anyOpen=true;h+='<div class="pt-ms"><b>Mark scheme:</b> '+esc(Q.ms||'')+'</div><p class="pt-self">Your mark: '+(function(){var s='';for(var x=0;x<=mk(Q);x++)s+='<button type="button" class="pt-sm'+(self[k][i]===x?' on':'')+'" data-k="'+k+'" data-i="'+i+'" data-v="'+x+'">'+x+'</button>';return s})()+' / '+mk(Q)+'</p>'}}
   h+=(blank(Q,a)?'<p class="pt-nb">Not answered.</p>':'')+(Q.e?'<div class="pt-ex"><b>'+(t==='mcq'?'Why':'Solution')+':</b> '+esc(Q.e)+'</div>':'')+(Q.s?'<small class="pt-sk">'+esc(Q.s)+'</small>':'')+'</li>'});h+='</ol>'});
  h+='</div>';stage.innerHTML=h;
  if(anyOpen)stage.querySelector('#pt-open-note').innerHTML='<p class="pt-warn2">Some answers are written answers. Scroll down, compare each with the mark scheme and tap the mark you earned — your total updates automatically.</p>';
  stage.querySelectorAll('.pt-sm').forEach(function(b){b.onclick=function(){var k=+b.dataset.k,i=+b.dataset.i;self[k][i]=+b.dataset.v;b.parentNode.querySelectorAll('.pt-sm').forEach(function(x){x.classList.toggle('on',x===b)});refresh()}});
  var again=el('button','btn pt-go','Try again');again.type='button';again.onclick=function(){reset();intro();box.scrollIntoView()};stage.appendChild(again);
  box.scrollIntoView();
 }
 intro();
});
})();
