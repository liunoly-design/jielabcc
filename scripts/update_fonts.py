from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
import re,concurrent.futures
root=Path(__file__).resolve().parents[1]
texts=''.join(p.read_text() for p in root.rglob('*.html'))+(root/'app.js').read_text()+(root/'cases.json').read_text()+(root/'clients.json').read_text()
chars=''.join(sorted(set(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]',texts))))+''.join(chr(i) for i in range(32,127))+'–×→·。'
url='https://fonts.googleapis.com/css2?'+urlencode({'family':'Noto Sans SC:wght@400;500;600;700;800','display':'swap','text':chars})
css=urlopen(url).read().decode()
urls=list(dict.fromkeys(re.findall(r'url\(([^)]+)\)',css)))
def fetch(item):
 i,url=item
 ext='woff2' if '.woff2' in url else 'ttf'
 name='lab-chinese-'+str(i)+'.'+ext
 (root/'assets'/name).write_bytes(urlopen(url).read())
 return url,'assets/'+name
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for url,name in pool.map(fetch,enumerate(urls)):
  css=css.replace(url,name)
css=css.replace("'Noto Sans SC'","'LabChinese'")
latin='https://fonts.googleapis.com/css2?'+urlencode({'family':'Inter:wght@400;500;600;700;800','display':'swap','text':''.join(chr(i) for i in range(32,127))+'–×→·’'})
lcss=urlopen(latin).read().decode()
for i,url in enumerate(dict.fromkeys(re.findall(r'url\(([^)]+)\)',lcss))):
 name='lab-inter-'+str(i)+'.ttf'
 (root/'assets'/name).write_bytes(urlopen(url).read());lcss=lcss.replace(url,'assets/'+name)
(root/'fonts.css').write_text(css+lcss.replace("'Inter'","'LabLatin'"))
print('Chinese glyphs',len(chars),'font files',len(urls),'self-hosted exact weights')
