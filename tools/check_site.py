from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.language='';self.h1=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='html':self.language=d.get('lang','')
  if tag=='h1':self.h1+=1
  if 'id' in d:self.ids.add(d['id'])
  for name in ('src','href'):
   if name in d:self.links.append(d[name])
root=Path('site');a=Audit();a.feed((root/'index.html').read_text());assert a.language=='en' and a.h1==1
for link in a.links:
 if link.startswith('#'):assert link[1:] in a.ids,link
 elif '://' not in link:assert (root/link).is_file(),link
for p in (root/'assets').glob('*.svg'):ET.parse(p)
print('PASS English, heading structure, local links/anchors and SVG parsing')
