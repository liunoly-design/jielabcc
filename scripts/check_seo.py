"""Check public search metadata, local links and bilingual generation without network access."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
import json,re,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];BASE='https://www.jielab.cc/'
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.links=[];self.meta={};self.canonical=[];self.alternates={};self.ids=set();self.lang=None;self.h1=0;self.consultation=[];self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'data-consultation' in a:self.consultation.append((tag,a))
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if a.get('id'):self.ids.add(a['id'])
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='link' and a.get('rel')=='alternate':self.alternates[a['hreflang']]=a['href']
  if tag in ('a','link','script','img'):
   attr='href' if tag in ('a','link') else 'src'
   if a.get(attr):self.links.append(a[attr])
files=sorted(list(ROOT.glob('*.html'))+list((ROOT/'en').glob('*.html')))
parsed={p:Page(p.read_text()) for p in files};public=set();structured=0
for p,doc in parsed.items():
 assert doc.h1==1,(p,'h1')
 assert doc.lang==('en' if p.parent.name=='en' else 'zh-CN'),(p,'lang')
 assert doc.meta.get('description') and doc.meta.get('og:title') and doc.meta.get('twitter:card'),(p,'meta')
 assert len(re.findall(r'<title>.+?</title>',p.read_text()))==1,(p,'title')
 if 'noindex' not in doc.meta.get('robots',''):
  assert len(doc.canonical)==1,(p,'canonical')
  expected=BASE+str(p.relative_to(ROOT)).replace('index.html','')
  assert doc.canonical==[expected],(p,doc.canonical,expected)
  assert set(doc.alternates)=={'zh-CN','en','x-default'},(p,'hreflang')
  for code,url in doc.alternates.items():
   f=ROOT/url.removeprefix(BASE)
   if f.is_dir():f=f/'index.html'
   assert f in parsed,(p,url)
   assert parsed[f].alternates==doc.alternates,(p,'reciprocity')
  public.add(expected)
  blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',p.read_text(),re.S)
  assert len(blocks)==1,(p,'JSON-LD')
  graph=json.loads(blocks[0]);assert graph['@context']=='https://schema.org'
  types={n['@type'] for n in graph['@graph']};assert {'Organization','WebPage'}<=types
  web=next(n for n in graph['@graph'] if n['@type']=='WebPage')
  assert web['url']==expected and web['description']==doc.meta['description']
  assert not any(t in types for t in ('Review','AggregateRating','MedicalOrganization','FAQPage'))
  structured+=1
 else:assert not doc.canonical,(p,'noindex canonical')
 for target in doc.links:
  u=urlsplit(target)
  if u.scheme or u.netloc:continue
  f=(ROOT/unquote(u.path.lstrip('/'))) if u.path.startswith('/') else (p.parent/unquote(u.path)) if u.path else p
  f=f.resolve()
  if f.is_dir():f=f/'index.html'
  assert f.exists(),(p,target,'missing')
  if u.fragment and f in parsed:assert unquote(u.fragment) in parsed[f].ids,(p,target,'fragment')
  assert '.git' not in target and '/admin' not in target,(p,target,'private')
locs={n.text for n in ET.parse(ROOT/'sitemap.xml').findall('{*}url/{*}loc')}
assert locs==public,(locs^public,'sitemap')
robots=(ROOT/'robots.txt').read_text();assert 'Disallow: /admin/' in robots and 'Disallow: /.git/' in robots
# Verify the source generator is stable across repeat builds.
before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
subprocess.run(['python3','scripts/build_locales.py'],cwd=ROOT,check=True)
assert before=={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'Build is not reproducible'
consultation_url=json.loads((ROOT/'consultation-config.json').read_text()).get('url','').strip()
for homepage in (ROOT/'index.html',ROOT/'en/index.html'):
 actions=parsed[homepage].consultation
 assert len(actions)==1,(homepage,'consultation action')
 tag,attrs=actions[0]
 if consultation_url:
  assert tag=='a' and attrs.get('href')==consultation_url and 'disabled' not in attrs,(homepage,'consultation link')
  assert attrs.get('target')=='_blank' and {'noopener','noreferrer'}<=set(attrs.get('rel','').split()),(homepage,'external link')
 else:assert tag=='button' and 'disabled' in attrs,(homepage,'unconfigured consultation')
print(f'PASS: {len(files)} pages, {len(public)} sitemap URLs, {structured} JSON-LD graphs; links, fragments, reciprocal locales, noindex and repeat build checked.')
