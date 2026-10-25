(function(){
function el(t,c,h){var e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]}).replace(/_{3,}/g,'\u0001').replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/__(.+?)__/g,'<u>$1</u>').replace(/\u0001/g,'<span class="pt-blank">&nbsp;</span>').replace(/\n/g,'<br>')}
function fmt(s){var m=Math.floor(s/60),x=s%60;return m+':'+(x<10?'0':'')+x}
document.querySelectorAll('.ptest').forEach(function(box){
 var T=JSON.parse(box.querySelector('script[type="application/json"]').textContent);
 var timed=T.timed!==false, si=0, qi=0, ans=[], left=0, tick=null, flags=[];
 T.sections.forEach(function(s){ans.push(new Array(s.questions.length).fill(-1));flags.push(new Array(s.questions.length).fill(false))});
 var stage=el('div','pt-stage');box.appendChild(stage);
 function intro(){
  stage.innerHTML='';
  var n=T.sections.reduce(function(a,s){return a+s.questions.length},0);
  var h='<div class="pt-intro"><b>'+esc(T.title)+'</b><p>'+n+' questions'+(timed?' · '+T.sections.map(function(s){return esc(s.name)+': '+s.minutes+' min'}).join(' · '):'')+'</p>';
  if(T.intro)h+='<p>'+esc(T.intro)+'</p>';
  h+='</div>';stage.innerHTML=h;
  var b=el('button','btn pt-go','Start');b.type='button';b.onclick=function(){si=0;qi=0;startSection()};stage.appendChild(b);
 }
 function startSection(){
  left=T.sections[si].minutes*60; render();
  clearInterval(tick); if(timed){tick=setInterval(function(){left--;var c=stage.querySelector('.pt-clock');if(c){c.textContent=fmt(Math.max(left,0));if(left<=60)c.classList.add('low')}if(left<=0){clearInterval(tick);endSection(true)}},1000)}
 }
 function render(){
  var S=T.sections[si],Q=S.questions[qi];var op=stage.querySelector('.pt-pass'),ok=stage.getAttribute('data-k'),nk=si+':'+qi,ost=op?op.scrollTop:0,wy=window.scrollY;stage.style.minHeight=stage.offsetHeight+'px';stage.innerHTML='';stage.setAttribute('data-k',nk);
  var top=el('div','pt-top','<span>'+esc(S.name)+' · Question '+(qi+1)+' of '+S.questions.length+'</span>'+(timed?'<span class="pt-clock">'+fmt(left)+'</span>':''));stage.appendChild(top);
  var body=el('div','pt-body'+(Q.p?' two':''));
  if(Q.p)body.appendChild(el('div','pt-pass',esc(Q.p)));
  var right=el('div','pt-q');right.appendChild(el('p','pt-qt',esc(Q.q)));
  var ul=el('div','pt-ch');
  Q.c.forEach(function(c,i){var b=el('button','pt-c'+(ans[si][qi]===i?' on':''),'<span>'+'ABCD'[i]+'</span><div>'+esc(c)+'</div>');b.type='button';b.onclick=function(){ans[si][qi]=i;render()};ul.appendChild(b)});
  right.appendChild(ul);body.appendChild(right);stage.appendChild(body);
  var nav=el('div','pt-nav');
  var pr=el('button','pt-b','← Back');pr.type='button';pr.disabled=qi===0;pr.onclick=function(){qi--;render()};
  var fl=el('button','pt-b'+(flags[si][qi]?' fl':''),flags[si][qi]?'Marked for review':'Mark for review');fl.type='button';fl.onclick=function(){flags[si][qi]=!flags[si][qi];render()};
  var nx=el('button','pt-b pt-p',qi<S.questions.length-1?'Next →':(si<T.sections.length-1?'Finish this section':'Finish test'));nx.type='button';
  nx.onclick=function(){if(qi<S.questions.length-1){qi++;render()}else endSection(false)};
  nav.appendChild(pr);nav.appendChild(fl);nav.appendChild(nx);stage.appendChild(nav);
  var grid=el('div','pt-grid');S.questions.forEach(function(_,i){var g=el('button','pt-g'+(i===qi?' cur':'')+(ans[si][i]>-1?' ans':'')+(flags[si][i]?' fl':''),String(i+1));g.type='button';g.onclick=function(){qi=i;render()};grid.appendChild(g)});stage.appendChild(grid);stage.style.minHeight='';
  var np=stage.querySelector('.pt-pass');if(np){if(ok===nk)np.scrollTop=ost;else{var u=np.querySelector('u');np.scrollTop=u?Math.max(0,u.offsetTop-np.offsetTop-60):0}}if(ok===nk)window.scrollTo(0,wy);
 }
 function endSection(auto){
  var S=T.sections[si];var blank=ans[si].filter(function(a){return a<0}).length;
  if(!auto&&blank&&!stage.querySelector('.pt-warn')){var w=el('p','pt-warn','You have '+blank+' unanswered question'+(blank>1?'s':'')+'. Press the button again to finish anyway.');stage.appendChild(w);return}
  clearInterval(tick);
  if(si<T.sections.length-1){si++;qi=0;stage.innerHTML='';stage.appendChild(el('div','pt-intro','<b>'+esc(T.sections[si-1].name)+' finished.</b><p>Next: '+esc(T.sections[si].name)+(timed?' ('+T.sections[si].minutes+' minutes)':'')+'</p>'));var b=el('button','btn pt-go','Start '+esc(T.sections[si].name));b.type='button';b.onclick=startSection;stage.appendChild(b);return}
  results();
 }
 function results(){
  stage.innerHTML='';var tot=0,cor=0,sk={};
  var h='<div class="pt-res"><h3>Your result</h3><div class="pt-scores">';
  T.sections.forEach(function(S,k){var c=0;S.questions.forEach(function(Q,i){var ok=ans[k][i]===Q.a;if(ok)c++;var s=Q.s||'Other';sk[s]=sk[s]||[0,0];sk[s][1]++;if(ok)sk[s][0]++});tot+=S.questions.length;cor+=c;h+='<div><small>'+esc(S.name)+'</small><b>'+c+' / '+S.questions.length+'</b></div>'});
  h+='<div class="all"><small>Total</small><b>'+cor+' / '+tot+'</b><small>'+Math.round(cor*100/tot)+'%</small></div></div>';
  h+='<p class="pt-note">This is a practice score (number correct), not an official scaled score.</p>';
  h+='<h4>By skill</h4><div class="tw"><table><thead><tr><th>Skill</th><th>Correct</th></tr></thead><tbody>';
  Object.keys(sk).forEach(function(s){h+='<tr><td>'+esc(s)+'</td><td>'+sk[s][0]+' / '+sk[s][1]+'</td></tr>'});
  h+='</tbody></table></div><h4>Review every question</h4>';
  T.sections.forEach(function(S,k){h+='<h5>'+esc(S.name)+'</h5><ol class="pt-rev">';S.questions.forEach(function(Q,i){var a=ans[k][i],ok=a===Q.a;
   h+='<li class="'+(ok?'ok':'no')+'">'+(Q.p?'<div class="pt-pass sm">'+esc(Q.p)+'</div>':'')+'<p><b>'+esc(Q.q)+'</b></p><ul>';
   Q.c.forEach(function(c,j){h+='<li class="'+(j===Q.a?'right':'')+(j===a&&!ok?' wrong':'')+'">'+'ABCD'[j]+') '+esc(c)+(j===Q.a?' ✓':'')+(j===a&&!ok?' ✗ your answer':'')+'</li>'});
   h+='</ul>'+(a<0?'<p class="pt-nb">Not answered.</p>':'')+'<div class="pt-ex"><b>Why:</b> '+esc(Q.e)+'</div>'+(Q.s?'<small class="pt-sk">'+esc(Q.s)+'</small>':'')+'</li>'});h+='</ol>'});
  h+='</div>';stage.innerHTML=h;
  var again=el('button','btn pt-go','Try again');again.type='button';again.onclick=function(){ans=T.sections.map(function(s){return new Array(s.questions.length).fill(-1)});flags=T.sections.map(function(s){return new Array(s.questions.length).fill(false)});intro();box.scrollIntoView()};stage.appendChild(again);
  box.scrollIntoView();
 }
 intro();
});
})();
