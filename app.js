const english=document.documentElement.lang==='en';
const lang=english?'en':'zh';
const assets=english?'../assets/':'assets/';
const names=english?{pharma:'Healthcare',valuation:'Valuation',legal:'Legal',education:'Education'}:{pharma:'医药',valuation:'资产评估',legal:'法律',education:'教育'};
const arrow='<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14"/></svg>';
const escapeHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const menu=document.querySelector('.menu'),nav=document.querySelector('nav');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',open);nav.classList.toggle('open',open)});
nav?.addEventListener('click',e=>{if(e.target.closest('a')){nav.classList.remove('open');menu?.setAttribute('aria-expanded','false')}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('open')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus()}});
function updateLanguageLink(){const file=location.pathname.split('/').pop()||'index.html';const a=document.querySelector('.language-switch');if(a)a.href=(english?'../':'en/')+file+location.search+location.hash}
updateLanguageLink();window.addEventListener('hashchange',updateLanguageLink);
// Restore the requested section after fonts and images establish final layout.
const arrivalHash=location.hash;
if(arrivalHash){
 let userNavigated=false;
 const noteNavigation=()=>{userNavigated=true};
 const noteKey=e=>{if(['ArrowUp','ArrowDown','PageUp','PageDown','Home','End',' '].includes(e.key))noteNavigation()};
 ['pointerdown','touchstart','wheel'].forEach(type=>window.addEventListener(type,noteNavigation,{passive:true}));
 window.addEventListener('keydown',noteKey);
 const restoreArrival=async()=>{
  const localImages=[...document.images].filter(img=>new URL(img.currentSrc||img.src,location.href).origin===location.origin);
  await Promise.all([document.fonts.ready,...localImages.map(img=>img.decode().catch(()=>{}))]);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
   if(!userNavigated&&location.hash===arrivalHash){
    let id;try{id=decodeURIComponent(arrivalHash.slice(1))}catch{}
    if(id)document.getElementById(id)?.scrollIntoView({block:'start',behavior:'instant'});
   }
   ['pointerdown','touchstart','wheel'].forEach(type=>window.removeEventListener(type,noteNavigation));
   window.removeEventListener('keydown',noteKey);
  }));
 };
 restoreArrival();
}
const cases=window.LAB_CASES||{};
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)');
function clientLogo(c){
 if(!c.logo)return '<div class="client-logo-placeholder"><strong>'+escapeHtml(c.name[lang])+'</strong><span>'+(english?'Official logo pending':'Logo 待整理')+'</span></div>';
 const src=escapeHtml((english?'../':'')+c.logo), alt=escapeHtml(c.name[lang])+' Logo';
 if(c.logoCrop){const b=c.logoCrop,s=240/b.width;return '<div class="client-logo-crop" style="width:240px;height:'+b.height*s+'px"><img src="'+src+'" alt="'+alt+'" style="width:'+b.imageWidth*s+'px;left:-'+b.x*s+'px;top:-'+b.y*s+'px"></div>'}
 return '<img src="'+src+'" alt="'+alt+'" width="240" height="88">';
}
const clientGrid=document.querySelector('#client-logo-grid');
if(clientGrid){
 clientGrid.innerHTML=(window.LAB_CLIENTS||[]).map(c=>'<article class="client-logo-item"><div class="client-logo-stage">'+clientLogo(c)+'</div><div class="client-logo-meta"><div><h2>'+escapeHtml(c.name[lang])+'</h2><p>'+escapeHtml(c.category[lang])+'</p></div>'+(c.report?'<a class="text-link" href="'+escapeHtml(c.report)+'">'+(english?'View stories':'查看报道')+' '+arrow+'</a>':'')+'</div></article>').join('');
 clientGrid.querySelectorAll('img').forEach(img=>img.addEventListener('error',()=>{const replacement=document.createElement('span');replacement.className='client-logo-unavailable';replacement.textContent=english?'Official logo unavailable':'Logo 暂无法加载';img.replaceWith(replacement)},{once:true}));
}
function caseLinks(key){return [1,2,3].map(i=>{const c=cases[key]?.[i-1];return '<a href="case.html?industry='+key+'&amp;case='+i+'">'+(c?'<span class="case-link-label"><strong>'+escapeHtml(c.category[lang])+'</strong><small>'+escapeHtml(c.client[lang])+'</small></span>':(english?'Case ':'案例 ')+i+'<small>'+(english?'Material being prepared':'资料待整理')+'</small>')+arrow+'</a>'}).join('')}
const tabs=[...document.querySelectorAll('[role=tab]')];
function selectTab(tab){tabs.forEach(t=>{t.setAttribute('aria-selected',String(t===tab));t.tabIndex=t===tab?0:-1});const key=tab.dataset.industry;document.querySelector('#industry-title').textContent=names[key]+(english?' cases':'行业案例');document.querySelector('#case-panel').setAttribute('aria-labelledby',tab.id);const img=document.querySelector('#case-image');img.src=assets+'methodology-'+lang+'.png';img.alt=english?'Methodology: define the problem, gather evidence and make results useful. Confirm an outcome at every stage.':'方法论：问题明确、实验有据、成果可用。每一步都留下可确认的成果。';document.querySelector('#case-links').innerHTML=caseLinks(key)}
function changeTab(tab){selectTab(tab);if(!reduceMotion.matches)document.querySelector('.case-feature-copy').animate([{opacity:.6,clipPath:'inset(0 0 0 3%)'},{opacity:1,clipPath:'inset(0 0 0 0)'}],{duration:300,easing:'cubic-bezier(.16,1,.3,1)'})}
tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>changeTab(tab));tab.addEventListener('keydown',e=>{let target;if(e.key==='ArrowRight')target=tabs[(i+1)%tabs.length];if(e.key==='ArrowLeft')target=tabs[(i+tabs.length-1)%tabs.length];if(e.key==='Home')target=tabs[0];if(e.key==='End')target=tabs.at(-1);if(target){e.preventDefault();changeTab(target);target.focus()}})});
if(tabs.length)selectTab(tabs[0]);
function bindFallback(img){function useFallback(){const caption=img.parentElement.querySelector('figcaption,.image-caption');if(caption){caption.hidden=false;caption.textContent=english?'Photograph unavailable':'现场图片暂无法加载'}img.style.visibility='hidden';delete img.dataset.fallback}img.addEventListener('error',useFallback,{once:true});if(img.complete&&img.naturalWidth===0)useFallback()}
if(document.querySelector('#detail-title')){
 const query=new URLSearchParams(location.search);const key=Object.hasOwn(names,query.get('industry'))?query.get('industry'):'pharma';const number=['1','2','3'].includes(query.get('case'))?query.get('case'):'1';const c=cases[key]?.[Number(number)-1];
 const title=c?c.category[lang]+' · '+c.client[lang]:names[key]+(english?' · Case ':'行业 · 案例 ')+number;
 document.querySelector('#detail-title').textContent=title;
 document.title=title+' · '+(english?"Jie's AI Lab":'杰哥 AI 实验室');
 const img=document.querySelector('#detail-image');img.src=assets+'methodology-'+lang+'.png';img.classList.add('methodology-image');img.alt=english?'Problem, experiment and value methodology':'问题、实验与价值方法图';img.parentElement.querySelector('figcaption').textContent=english?'Problem · Experiment · Value':'问题 · 实验 · 价值';document.querySelector('#back-cases').href='cases.html#'+key;
 if(c){
  document.querySelector('.case-detail .section-top p').textContent=c.intro[lang];
  document.querySelectorAll('.detail-sections article p').forEach((p,i)=>p.textContent=c.details[lang][i]);
  if(c.status==='illustrative'){
   document.querySelector('.case-detail').classList.add('illustrative-case');
   const notice=document.createElement('p');notice.className='example-notice';notice.textContent=english?'Illustrative experiment design. This is not a completed client project.':'示例案例：展示实验设计与拟交付物，非已实施的真实客户项目。';document.querySelector('.section-top').after(notice);
  }
  if(c.image){img.src=(english?'../':'')+c.image;img.classList.remove('methodology-image');img.alt=english?'Weigao Orthopaedics workshop photograph':'威高骨科工作坊现场';img.parentElement.querySelector('figcaption').textContent=english?'Weigao Orthopaedics workshop · Source: Infynova':'威高骨科工作坊现场 · 来源：无境创新'}
  if(c.gallery){const gallery=document.createElement('div');gallery.className='case-gallery';gallery.innerHTML=c.gallery.map(g=>'<figure><img src="'+escapeHtml((english?'../':'')+g.src)+'" alt="'+escapeHtml(g.caption[lang])+'" loading="eager"><figcaption>'+escapeHtml(g.caption[lang])+'</figcaption></figure>').join('');document.querySelector('.detail-sections').after(gallery)}
  if(c.reports.length){
   const reports=c.reports.map(i=>window.LAB_ARTICLES[i]);
   if(!c.image&&reports[0].localCover){img.src=(english?'../':'')+reports[0].localCover;img.classList.remove('methodology-image');img.alt=reports[0].source+(english?' workshop report photograph':'工作坊报道图片');img.parentElement.querySelector('figcaption').textContent=english?'Image from the client report':'客户报道原图';}
   const section=document.createElement('section');section.className='related-reports';section.innerHTML='<h2>'+(english?'Client reports':'相关客户报道')+'</h2>'+reports.map(a=>'<a class="report-row" href="'+escapeHtml(a.url)+'" target="_blank" rel="noopener noreferrer"><span><small>'+escapeHtml(a.source)+' · '+(a.published||(english?'Publication date pending':'发布日期待核对'))+'</small><strong lang="'+(english?'en':'zh-CN')+'">'+escapeHtml(english?a.titleEn:a.title)+(english&&!a.titleIsEditorialLabel?'<span class="original-title" lang="zh-CN">'+escapeHtml(a.title)+'</span>':'')+'</strong></span>'+arrow+'</a>').join('');
   document.querySelector('.detail-sections').after(section);
  }
 }
 else{document.querySelector('.case-detail .section-top p').textContent=english?'Case material is being prepared.':'案例资料待整理。';document.querySelectorAll('.detail-sections article p').forEach(p=>p.textContent=english?'Material being prepared.':'资料待整理。')}
}
document.querySelectorAll('[data-fallback]').forEach(bindFallback);
if(english)document.querySelectorAll('time[datetime]').forEach(t=>{t.textContent=new Intl.DateTimeFormat('en',{year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}).format(new Date(t.dateTime+'T00:00:00Z'))});
// Keep scroll native; show continuity and active destinations without hijacking input.
const progress=document.createElement('div');progress.className='reading-progress';progress.setAttribute('aria-hidden','true');document.querySelector('.site-header')?.append(progress);
let scrollFrame;
function updateProgress(){scrollFrame=null;const max=document.documentElement.scrollHeight-innerHeight;progress.style.transform='scaleX('+(max>0?Math.min(1,Math.max(0,scrollY/max)):0)+')'}
addEventListener('scroll',()=>{if(!scrollFrame)scrollFrame=requestAnimationFrame(updateProgress)},{passive:true});addEventListener('resize',updateProgress);updateProgress();
if('IntersectionObserver' in window){const sections=[...document.querySelectorAll('main>section[id]')];const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){nav?.querySelectorAll('a').forEach(a=>{if(new URL(a.href).pathname===location.pathname&&new URL(a.href).hash==='#'+entry.target.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})}},{rootMargin:'-25% 0px -45% 0px'});sections.forEach(s=>observer.observe(s))}
