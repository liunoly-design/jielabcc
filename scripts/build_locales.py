"""Build shareable English routes from Chinese HTML and explicit editorial translations."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
TRANS=json.loads((ROOT/'locales-en.json').read_text())
CASES=json.loads((ROOT/'cases.json').read_text())
ARTICLES=json.loads((ROOT/'articles.json').read_text())
CLIENTS=json.loads((ROOT/'clients.json').read_text())
CONSULTATION=json.loads((ROOT/'consultation-config.json').read_text())
ARROW='<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14"/></svg>'
TITLE_EN=[
 'From learning to practice: Baoyuxin Medical completes its AI workshop for healthcare supply-chain innovation',
 'Learning AI together: Guoyao Shuke explores collaborative innovation in its AI workshop',
 'Guoyao Shuke holds an AI innovation workshop to explore AI in business',
 'Guorun Medical runs an AI workshop for middle and senior managers',
 'Weigao Orthopaedics creates 39 AI business outputs in two days, turning training into business action'
]
ARTICLE_TITLES={a['title']:t for a,t in zip(ARTICLES,TITLE_EN) if not a.get('titleIsEditorialLabel')}
def case_links(key):
 out=[]
 for i in range(1,4):
  c=CASES.get(key,[])[i-1] if len(CASES.get(key,[]))>=i else None
  label=f'<span class="case-link-label"><strong>{c["category"]["zh"]}</strong><small>{c["client"]["zh"]}</small></span>' if c else f'案例 {i}<small>资料待整理</small>'
  out.append(f'<a href="case.html?industry={key}&amp;case={i}">{label}{ARROW}</a>')
 return ''.join(out)
class Translator(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=False); self.out=[]
 def handle_decl(self,d): self.out.append('<!'+d+'>')
 def handle_starttag(self,tag,attrs):
  a=[]
  for k,v in attrs:
   if k=='lang' and v=='zh-CN': v='en'
   if k in ('alt','aria-label','placeholder','content'): v=TRANS.get(v,v)
   if k in ('src','href','data-fallback') and v and (v.startswith('assets/') or v in ('app.js','fonts.css','style.css','case-data.js')): v='../'+v
   if k=='src' and v=='../assets/methodology-zh.png': v='../assets/methodology-en.png'
   if k=='href' and v and v.startswith('en/'): v='../'+v[3:]
   if k=='hreflang' and v=='en': v='zh-CN'
   a.append(k if v is None else k+'="'+escape(v,quote=True)+'"')
  self.out.append('<'+tag+(' '+ ' '.join(a) if a else '')+'>')
 def handle_endtag(self,t): self.out.append('</'+t+'>')
 def handle_data(self,s):
  if s in ARTICLE_TITLES:
   self.out.append(escape(ARTICLE_TITLES[s])+'<span class="original-title" lang="zh-CN">'+escape(s)+'</span>')
  elif s=='EN': self.out.append('中文')
  else:
   if re.search('[\u4e00-\u9fff]',s) and s not in TRANS: raise ValueError('Missing translation: '+repr(s))
   self.out.append(escape(TRANS.get(s,s)))
 def handle_entityref(self,s): self.out.append('&'+s+';')
 def handle_charref(self,s): self.out.append('&#'+s+';')
 def handle_comment(self,s): self.out.append('<!--'+s+'-->')
for page in ('index.html','cases.html','case.html','articles.html','clients.html'):
 p=ROOT/page
 s=p.read_text()
 s=re.sub(r'<svg viewBox="91 633 354 96".*?</svg>','<img src="assets/logo-bilingual.png" width="1032" height="256" alt="杰哥与黄猫规范横版 Logo">',s,count=1)
 if 'class="language-switch"' not in s:
  s=s.replace('</nav></div></header>',f'</nav><a class="language-switch" href="en/{page}" hreflang="en" lang="en" aria-label="English version">EN</a></div></header>')
 s=s.replace('© 2026 JEGE AI LAB',"© 2026 JIE'S ARTIFICIAL INTELLIGENCE LAB")
 if page=='index.html':
  url=CONSULTATION.get('url','').strip()
  if url:
   from urllib.parse import urlsplit
   if urlsplit(url).scheme!='https' or not urlsplit(url).netloc: raise ValueError('Consultation URL must be a complete HTTPS URL.')
   action='<a class="button" data-consultation href="'+escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer">填写合作需求 '+ARROW+'</a>'
   status='前往飞书填写需求。'
  else:
   action='<button class="button" data-consultation disabled>填写合作需求 '+ARROW+'</button>'
   status='合作登记入口即将开放。'
  s=re.sub(r'<(?:button|a)[^>]*data-consultation(?:\s|>).*?</(?:button|a)>',lambda m:action,s,count=1)
  s=re.sub(r'(<p[^>]*data-consultation-status[^>]*>).*?(</p>)',lambda m:m[1]+status+m[2],s,count=1)
  s=re.sub(r'(<div class="case-links" id="case-links">|<div id="case-links" class="case-links">).*?(</div>)',lambda m:m[1]+case_links('pharma')+m[2],s,count=1)
 if page=='cases.html':
  head,tail=s.split('</section>',1)
  head=head.replace('案例资料逐步补充','从客户出发，记录真实实践。').replace('每个案例都记录真实问题、实验过程、可确认的成果与下一步。','按医药流通、医药科技与医疗器械生产企业，收集问题、实验与阶段成果。')
  tail=tail.replace('从客户出发，记录真实实践。','案例资料逐步补充').replace('按医药流通、医药科技与医疗器械生产企业，收集问题、实验与阶段成果。','每个案例都记录真实问题、实验过程、可确认的成果与下一步。')
  s=head+'</section>'+tail
  for key in ('pharma','valuation','legal','education'):
   pattern=r'(<section\b[^>]*id="'+key+r'".*?<div class="case-links">).*?(</div>)'
   s=re.sub(pattern,lambda m:m[1]+case_links(key)+m[2],s,count=1,flags=re.S)
 if 'case-data.js' not in s: s=s.replace('<script src="app.js">','<script src="case-data.js"></script><script src="app.js">')
 # Keep values stable across languages; labels are translated.
 s=re.sub(r'<option>([^<]+)</option>',lambda m:'<option value="'+escape(m[1],quote=True)+'">'+m[1]+'</option>',s)
 p.write_text(s)
 t=Translator();t.feed(s);en=''.join(t.out)
 en=en.replace('aria-label="English version"','aria-label="中文版"').replace('hreflang="zh-CN" lang="en"','hreflang="zh-CN" lang="zh-CN"')
 if page=='index.html':
  en=re.sub(r'<h1>.*?</h1>','<h1>See the value of AI<br>for your business<br>in <span class="hero-value">1–5 days.</span></h1>',en,count=1)
 (ROOT/'en'/page).write_text(en)
for article,title in zip(ARTICLES,TITLE_EN): article['titleEn']=title
(ROOT/'case-data.js').write_text('window.LAB_CASES='+json.dumps(CASES,ensure_ascii=False)+';\nwindow.LAB_ARTICLES='+json.dumps(ARTICLES,ensure_ascii=False)+';\nwindow.LAB_CLIENTS='+json.dumps(CLIENTS,ensure_ascii=False)+';\n')
print('Built all five Chinese / English page pairs.')
