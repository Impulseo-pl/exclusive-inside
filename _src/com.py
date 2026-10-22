import json, urllib.request, urllib.parse, sys, os
from PIL import Image, ImageDraw
T = [l.strip() for l in open('com_list.txt', encoding='utf-8') if l.strip()]
UA = {'User-Agent': 'ImpulseoDemo/1.0 (kontakt@impulseo.pl)'}
meta = {}
for i in range(0, len(T), 20):
    q = urllib.parse.urlencode({'action':'query','titles':'|'.join(T[i:i+20]),'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':'420','format':'json'})
    d = json.load(urllib.request.urlopen(urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+q, headers=UA)))
    for p in d['query']['pages'].values():
        if 'imageinfo' not in p: continue
        ii = p['imageinfo'][0]; em = ii.get('extmetadata', {})
        meta[p['title']] = dict(url=ii['url'], thumb=ii['thumburl'], w=ii['width'], h=ii['height'],
            lic=em.get('LicenseShortName',{}).get('value',''), artist=em.get('Artist',{}).get('value',''))
json.dump(meta, open('com/meta.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
W, H, cols = 300, 240, 5
sh = Image.new('RGB', (cols*W, ((len(T)+cols-1)//cols)*(H+30)), 'white'); dr = ImageDraw.Draw(sh)
for k, t in enumerate(T):
    m = meta.get(t)
    if not m: continue
    fn = f'com/t{k}.jpg'
    if not os.path.exists(fn):
        open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(m['thumb'], headers=UA)).read())
    im = Image.open(fn).convert('RGB'); im.thumbnail((W-6, H-6))
    x, y = (k%cols)*W, (k//cols)*(H+30)
    sh.paste(im, (x+3, y+3)); dr.text((x+3, y+H), f"{k} {m['w']}x{m['h']} {m['lic'][:14]}", fill='black'); dr.text((x+3,y+H+12), t[5:45], fill='black')
sh.save('com/sheet.jpg', quality=82)
