"""Generate static case records, service entry pages and search metadata from bilingual sources."""
from pathlib import Path
from html import escape as e
import json,re,hashlib
from xml.etree.ElementTree import Element,SubElement,tostring
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.jielab.cc/'
def load(name):return json.loads((ROOT/name).read_text())
def url(file,lang):return BASE+('en/' if lang=='en' else '')+('' if file=='index.html' else file)
def strip(s):return re.sub(r'<!-- (SEO|SEARCH) START -->.*?<!-- \1 END -->','',s,flags=re.S)
def build():
 data=load('seo-content.json');cases=load('cases.json');reports=load('articles.json')
 translations=load('locales-en.json')
 def check_translations(value):
  if isinstance(value,dict):
   if 'zh' in value and 'en' in value:
    if translations.get(value['zh'])!=value['en']:raise ValueError('Missing or inconsistent SEO translation: '+value['zh'])
   else:
    for item in value.values():check_translations(item)
  elif isinstance(value,list):
   for item in value:check_translations(item)
 check_translations(data)
 # The locale build adds editorial English report titles to its generated data.
 titles=re.search(r'window.LAB_ARTICLES=(.*?);\n', (ROOT/'case-data.js').read_text()).group(1)
 reports=json.loads(titles)
 pages={}
 for lang in ('zh','en'):
  prefix='../' if lang=='en' else ''; folder=ROOT/'en' if lang=='en' else ROOT
  template=strip((folder/'case.html').read_text())
  before=template.split('<main id="main">')[0];after=template.split('</main>')[1]
  def shell(body,file):
   head=re.sub(r'(<a[^>]*class="language-switch"[^>]*href=")[^"]*',lambda m:m[1]+('en/'+file if lang=='zh' else '../'+file),before)
   return head+'<main id="main">'+body+'</main>'+after
  def link(file,label):return '<a class="text-link" href="'+e(file,quote=True)+'">'+e(label)+'</a>'
  def related(files):
   labels={p['slug']+'.html':p['title'][lang] for p in data['pages']}
   for key,items in cases.items():
    for i,c in enumerate(items,1):labels[f'case-{key}-{i}.html']=c['category'][lang]+' · '+c['client'][lang]
   return '<div class="search-links">'+''.join(link(f,labels[f]) for f in files)+'</div>'
  for key,items in cases.items():
   for i,c in enumerate(items,1):
    file=f'case-{key}-{i}.html';title=c['category'][lang]+' · '+c['client'][lang]
    notice=('示例案例：展示实验设计与拟交付物，非已实施的真实客户项目。' if lang=='zh' else 'Illustrative experiment design, not a completed client project.') if c.get('status')=='illustrative' else ''
    related_reports=[reports[j] for j in c['reports']]
    image=c.get('image') or (related_reports[0].get('localCover') if related_reports else None) or 'assets/methodology-'+lang+'.png'
    caption=('威高骨科工作坊现场 · 来源：无境创新' if lang=='zh' else 'Weigao Orthopaedics workshop · Source: Infynova') if c.get('image') else ('客户报道原图' if lang=='zh' else 'Photograph from the client report') if related_reports else ('问题 · 实验 · 价值' if lang=='zh' else 'Problem · Experiment · Value')
    body='<section class="screen case-detail"><div class="wrap">'+link('cases.html#'+key,'返回行业案例' if lang=='zh' else 'Back to industry cases')+'<div class="section-top"><h1 class="page-title">'+e(title)+'</h1><p>'+e(c['intro'][lang])+'</p></div>'
    if notice:body+='<p class="example-notice">'+e(notice)+'</p>'
    body+='<figure class="detail-cover"><img src="'+prefix+image+'" alt="'+e(caption,quote=True)+'"><figcaption>'+e(caption)+'</figcaption></figure><div class="detail-sections">'
    headings=['真实问题','实验过程','阶段成果'] if lang=='zh' else ['Real problem','Experiment','Stage outcomes']
    for h,p in zip(headings,c['details'][lang]):body+='<article><h2 class="detail-heading">'+h+'</h2><p>'+e(p)+'</p></article>'
    body+='</div>'
    if c.get('gallery'):
     body+='<div class="case-gallery">'+''.join('<figure><img loading="lazy" src="'+prefix+g['src']+'" alt="'+e(g['caption'][lang],quote=True)+'"><figcaption>'+e(g['caption'][lang])+'</figcaption></figure>' for g in c['gallery'])+'</div>'
    if related_reports:
     body+='<section class="related-reports"><h2>'+('事实来源与关联说明' if lang=='zh' else 'Sources and attribution')+'</h2>'
     for a in related_reports:
      title_report=a['title'] if lang=='zh' else a['titleEn']
      note=a['association']['verificationNote'] if lang=='zh' else ('Verified against a locally saved original. The report names Infynova, Weigao Orthopaedics and Jie’s AI Lab. Outputs are workshop-stage results, not proof of production deployment.' if a['association']['labNameExplicitlyMentioned'] else 'The original report does not explicitly name Jie’s AI Lab. The client relationship comes from supplied collaboration records; the original reporting organisation is preserved.')
      body+='<a class="report-row" href="'+e(a['url'],quote=True)+'" target="_blank" rel="noopener noreferrer"><span><small>'+e(a['source'])+' · '+e(a['published'])+'</small><strong>'+e(title_report)+'</strong>'+(('<span class="original-title" lang="zh-CN">'+e(a['title'])+'</span>') if lang=='en' else '')+'</span></a><p>'+e(note)+'</p>'
     body+='</section>'
    body+=related(['pharma-ai.html','medical-device-ai.html','ai-training.html'])+'</div></section>'
    pages[(file,lang)]={'html':shell(body,file),'title':title+' | '+('杰哥 AI 实验室' if lang=='zh' else 'Jie’s AI Lab'),'description':c['intro'][lang], 'citation':[a['url'] for a in related_reports],'illustrative':bool(notice)}
  for p in data['pages']:
   file=p['slug']+'.html';title=p['title'][lang]
   body='<section class="screen case-detail search-detail"><div class="wrap">'+link('index.html','杰哥 AI 实验室首页' if lang=='zh' else 'Jie’s AI Lab home')+'<div class="section-top"><h1 class="page-title">'+e(title)+'</h1><p>'+e(p['intro'][lang])+'</p></div><div class="search-copy"><p>'+e(data['identity'][lang])+'</p>'
   for section in p['sections']:
    body+='<article><h2 class="detail-heading">'+e(section['heading'][lang])+'</h2><p>'+e(section['text'][lang])+'</p>'
    if section.get('sources'):
     body+='<div class="search-links">'+''.join(link(reports[j]['url'],('原文：' if lang=='zh' else 'Source: ')+reports[j]['source']+' · '+reports[j]['published']) for j in section['sources'])+'</div>'
    body+='</article>' 
   body+='<article><h2 class="detail-heading">'+('选择合适的服务形式' if lang=='zh' else 'Choose a service format')+'</h2><ul>'+''.join('<li>'+e(item[lang])+'</li>' for item in data['products'])+'</ul></article>'
   body+='<section><h2 class="detail-heading">'+('常见问题' if lang=='zh' else 'Common questions')+'</h2>'
   faq=p['faq']+data['commonFaq']
   for q,a in zip(faq[::2],faq[1::2]):body+='<article><h3>'+e(q[lang])+'</h3><p>'+e(a[lang])+'</p></article>'
   body+='</section></div>'+related(p['related'])+link('index.html#contact','查看合作咨询与登记状态' if lang=='zh' else 'View consultation and registration status')+'</div></section>'
   pages[(file,lang)]={'html':shell(body,file),'title':title+' | '+('杰哥 AI 实验室' if lang=='zh' else 'Jie’s AI Lab'),'description':p['description'][lang],'service':title}
  for file,m in data['metadata'].items():
   s=strip((folder/file).read_text())
   if file!='case.html':
    addition='<aside class="search-entry wrap" aria-label="'+('服务与行业入口' if lang=='zh' else 'Services and industries')+'"><h2>'+('从业务需求开始' if lang=='zh' else 'Start with a business need')+'</h2>'+related([p['slug']+'.html' for p in data['pages']])+'</aside>'
    if file=='index.html':addition='<section class="search-entry wrap"><h2>'+('AI 培训与行业解决方案' if lang=='zh' else 'AI training and industry solutions')+'</h2><p>'+e(data['identity'][lang])+'</p>'+related([p['slug']+'.html' for p in data['pages']])+'</section>'
    block='<!-- SEARCH START -->'+addition+'<!-- SEARCH END -->'
    if file=='index.html':s=re.sub(r'(<section[^>]*id="contact"[^>]*>)',lambda m:block+m[1],s,count=1)
    else:s=s.replace('</main>',block+'</main>')
   pages[(file,lang)]={'html':s,'title':m['title'][lang],'description':m['description'][lang]}
 # Only explicit public editorial pages enter the sitemap. Templates and illustrative designs remain noindex.
 indexable=[]
 for (file,lang),p in pages.items():
  s=p['html'];canonical=url(file,lang);noindex=file=='case.html' or p.get('illustrative')
  s=re.sub(r'<title>.*?</title>','<title>'+e(p['title'])+'</title>',s,flags=re.S)
  s=re.sub(r'<meta\b(?=[^>]*\bname="description")[^>]*>','',s)
  org={'@type':'Organization','@id':BASE+'#organization','name':'杰哥 AI 实验室','alternateName':'Jie’s AI Lab','url':BASE,'logo':BASE+'assets/logo-bilingual.png'}
  if file=='index.html':org['description']=data['identity'][lang]
  web={'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':p['title'],'description':p['description'],'inLanguage':'en' if lang=='en' else 'zh-CN','publisher':{'@id':BASE+'#organization'}}
  if p.get('citation'):web['citation']=p['citation']
  graph=[org,web]
  if p.get('service'):graph.append({'@type':'Service','@id':canonical+'#service','name':p['service'],'description':p['description'],'url':canonical,'provider':{'@id':BASE+'#organization'}})
  if file!='index.html':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'首页' if lang=='zh' else 'Home','item':url('index.html',lang)},{'@type':'ListItem','position':2,'name':p['title'],'item':canonical}]})
  tags='<!-- SEO START --><meta name="description" content="'+e(p['description'],quote=True)+'">'
  if noindex:tags+='<meta name="robots" content="noindex,follow">'
  else:
   tags+='<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="'+canonical+'">'
   for code,l in [('zh-CN','zh'),('en','en'),('x-default','zh')]:tags+='<link rel="alternate" hreflang="'+code+'" href="'+url(file,l)+'">'
   indexable.append(canonical)
  for name,value in [('og:type','website'),('og:title',p['title']),('og:description',p['description']),('og:url',canonical),('og:site_name','杰哥 AI 实验室 · Jie’s AI Lab'),('og:locale','zh_CN' if lang=='zh' else 'en_US'),('og:locale:alternate','en_US' if lang=='zh' else 'zh_CN'),('og:image',BASE+'assets/logo-bilingual.png'),('og:image:alt','杰哥 AI 实验室 · Jie’s AI Lab')]:tags+='<meta property="'+name+'" content="'+e(value,quote=True)+'">'
  for name,value in [('twitter:card','summary'),('twitter:title',p['title']),('twitter:description',p['description']),('twitter:image',BASE+'assets/logo-bilingual.png')]:tags+='<meta name="'+name+'" content="'+e(value,quote=True)+'">'
  if not noindex:tags+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
  tags+='<!-- SEO END -->';s=s.replace('</head>',tags+'</head>')
  # Content hashes invalidate browser caches while retaining stable page URLs.
  s=re.sub(r'(href|src)="((?:\.\./)?(?:style.css|fonts.css|app.js|case-data.js))(?:\?v=[^"]*)?"',lambda m:m[1]+'="'+m[2]+'?v='+hashlib.sha256((ROOT/m[2].split('/')[-1]).read_bytes()).hexdigest()[:12]+'"',s)
  (ROOT/('en/' if lang=='en' else '')/file).write_text(s)
 root=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
 for loc in sorted(indexable):SubElement(SubElement(root,'url'),'loc').text=loc
 (ROOT/'sitemap.xml').write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+tostring(root,encoding='utf-8'))
 (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /.git/\nDisallow: /.env\nDisallow: /scripts/\nDisallow: /README.md\nDisallow: /*.json$\nDisallow: /*.py$\nDisallow: /*.md$\nSitemap: '+BASE+'sitemap.xml\n')
 print(f'Built {len(pages)} bilingual pages; {len(indexable)} public canonical URLs in sitemap.')
if __name__=='__main__':build()
