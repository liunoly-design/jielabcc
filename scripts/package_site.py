"""Package only public site assets for Cloudflare static hosting."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
files = list(ROOT.glob('*.html')) + list((ROOT / 'en').glob('*.html'))
files += [ROOT / name for name in (
    'app.js', 'case-data.js', 'style.css', 'fonts.css',
    'favicon.ico', 'robots.txt', 'sitemap.xml',
)]
extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.ico', '.ttf', '.woff', '.woff2'}
tracked = subprocess.check_output(['git', 'ls-files', '-z', 'assets'], cwd=ROOT).decode().split('\0')
files += [ROOT / name for name in tracked if name and Path(name).suffix.lower() in extensions]
for source in files:
    if not source.is_file():
        raise SystemExit(f'Missing published asset: {source.relative_to(ROOT)}')
    target = OUT / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
(OUT / '_redirects').write_text('/ /index.html 200\n/en/ /en/index.html 200\n')
(OUT / '_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
/*.html
  Cache-Control: no-cache
/en/*.html
  Cache-Control: no-cache
/assets/*
  Cache-Control: public, max-age=3600
''')
print(f'Packaged {len(files)} public files into dist; source data and credentials excluded.')
