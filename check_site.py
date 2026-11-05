"""Проверяет страницы, локальные ссылки и подписи иллюстраций."""
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json

class Page(HTMLParser):
 def __init__(self):
  super().__init__(); self.refs=[]; self.ids=set(); self.h1=0; self.figures=0; self.captions=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='figure':self.figures+=1
  if tag=='figcaption':self.captions+=1
  if a.get('id'):self.ids.add(a['id'])
  for key in ('src','href'):
   if key in a:self.refs.append(a[key])
  if tag=='img':assert a.get('alt'), 'У изображения нет описания'

def check():
 import app
 folder=app.build(); pages={}
 for file in folder.glob('*.html'):
  p=Page();p.feed(file.read_text(encoding='utf-8'));pages[file]=p
  assert p.h1==1, f'{file.name}: должен быть один главный заголовок'
  assert p.figures==p.captions, f'{file.name}: не у всех иллюстраций есть подписи'
 for file,p in pages.items():
  for ref in p.refs:
   u=urlsplit(ref)
   if u.scheme or u.netloc:continue
   target=(file.parent/unquote(u.path)).resolve() if u.path else file
   assert target.exists(), f'{file.name}: не найден {ref}'
   if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids, f'{file.name}: нет якоря {ref}'
 meta=json.loads((folder/'assets/image-sources.json').read_text(encoding='utf-8'))
 for image in meta:assert (folder/'assets'/image['file']).exists(),f'Нет изображения {image["file"]}'
 print(f'OK: {len(app.PAGES)} страниц; локальные ссылки, якоря, изображения, описания и подписи проверены.')

if __name__=='__main__':check()
