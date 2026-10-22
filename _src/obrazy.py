# -*- coding: utf-8 -*-
"""Przygotowanie zdjęć: realizacje z Oferteo (bez znaku wodnego) + poglądowe z Wikimedia Commons."""
import os, re, json, urllib.request
from PIL import Image, ImageOps
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), 'img'); os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'ImpulseoDemo/1.0 (kontakt@impulseo.pl)'}

# nazwa -> (plik w orig, czy ma znak wodny Redmi)
KLIENT = {
 'schody-krecone-budowa': ('1740685801399-crop-img-20241217-191726.jpg', 1),
 'lazienka-zielona-oktagon': ('1747033863310-1747033837674_avatar.jpg', 1),
 'wanna-narozna-odplyw': ('1749119047576-crop-img-20230114-122131.jpg', 1),
 'plyty-wielkoformatowe-podloga': ('1749119246641-crop-img-20210422-114021.jpg', 1),
 'wyspa-spiek-marmur': ('223905847-crop-img-20220719-083845.jpg', 1),
 'bateria-podtynkowa-beton': ('223911080-crop-img-20210621-095507.jpg', 1),
 'schody-zewnetrzne-szklo': ('223916899-crop-img-20210510-200637.jpg', 1),
 'schody-zewnetrzne-klinkier': ('223919958-crop-img-20210510-192444.jpg', 1),
 'heksagony-3d': ('223922283-crop-img-20210410-124258.jpg', 1),
 'zabudowa-wc-marmur': ('crop-img-20210306-153802.jpg', 1),
 'projekt-wizualizacja': ('crop-img-20210917-174348.jpg', 1),
 'korytarz-cegla': ('crop-img-20211013-163119.jpg', 1),
 'lazienka-drewno-geometria': ('crop-img-20211019-121004.jpg', 1),
 'sciana-ramy-dekor': ('crop-img-20220211-181149.jpg', 1),
 'bus-firmowy': ('crop-img-20220808-wa0000.jpg', 0),
 'fototapeta-las': ('crop-img-20221012-173328.jpg', 1),
 'prysznic-meander': ('crop-img-20230702-195811.jpg', 1),
 'prysznic-meander-2': ('crop-img-20230702-195841.jpg', 1),
 'lazienka-zielona-oktagon-2': ('crop-img-20230702-200730.jpg', 1),
 'schody-czarne-prety': ('crop-img-20230816-163418.jpg', 1),
 'lazienka-czarny-marmur': ('crop-img-20230908-wa0013.jpg', 0),
 'lazienka-czarny-marmur-2': ('crop-img-20230908-wa0018.jpg', 0),
 'lazienka-led-prysznic': ('op_4854063_0.jpg', 0),
 'lazienka-led-umywalka': ('op_4854063_1.jpg', 0),
 'lazienka-led-zabudowa': ('op_4854063_2.jpg', 0),
 'lazienka-czarny-marmur-zloto': ('op_4854063_3.3.jpg', 0),
 'schody-spiek-prety': ('op_4854063_img_20230610_180937.jpg', 0),
 'schody-spiek-prety-2': ('op_4854063_img_20230804_195148.jpg', 0),
 'schody-spiek-prety-3': ('op_4854063_img_20230804_195402.jpg', 0),
 'lazienka-szara-umywalka': ('op_4854063_received_1682564888902409.jpeg', 0),
 'lazienka-szara-prysznic': ('op_4854063_received_2269820973219859.jpeg', 0),
 'lazienka-szara-wc': ('op_4854063_received_2431840450331458.jpeg', 0),
 'lazienka-szara-kabina': ('op_4854063_received_2564969940334206.jpeg', 0),
}
COMMONS = {
 'spawanie-wlokien': 'File:Optical fiber fusion splicing - USDA.jpg',
 'spawarka-szafa': 'File:Splicing of the fiber optic cables for a system for a power substation in Queens. (49363966412).jpg',
 'kaseta-spawow': 'File:Fiber Splice.jpg',
 'mikrorurki': 'File:Microduct cabling.jpg',
 'wykop-mikrorurki': 'File:20201012 SpeedPipes HorizontalDirectionalDrilling DSC04955 PtrQs.jpg',
 'szafa-uliczna': 'File:2018-09-02 - Glasfaser Hauptverteiler Klein Waabs.jpg',
 'puszka-abonencka': 'File:Optical fiber connectors-Splice box-01ASD.jpg',
 'beben-kabla': 'File:Construction site with large wooden cable drums and orange conduit for fibre-optic installation, Germany.jpg',
 'przecinarka-wlokna': 'File:Easton Utilities Fiber Optic Cable Work Demonstration (20230920-USDA-RD-CDP-4778).jpg',
 'zlacze-sc-apc': 'File:SC-APC fiber optic cable.jpg',
 'monter-szafa': 'File:Splicing fiber optic cables in a communications cabinet in a power facility in Queens. 10-02-2019 (48844065016).jpg',
}

def zapisz(im, name, widths=(720, 1280, 1920)):
    im = ImageOps.exif_transpose(im).convert('RGB')
    w0 = im.size[0]
    done = set()
    for w in widths:
        w = min(w, w0)
        if w in done: continue
        done.add(w)
        r = im.resize((w, round(im.size[1] * w / w0)), Image.LANCZOS) if w < w0 else im
        r.save(os.path.join(OUT, f'{name}-{w}.webp'), quality=80, method=6)

for name, (f, wm) in KLIENT.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, 'orig', f)))
    if wm:
        w, h = im.size
        im = im.crop((0, 0, w, int(h * (0.875 if w > h else 0.915))))
    zapisz(im, name)

meta = json.load(open(os.path.join(SRC, 'com', 'meta.json'), encoding='utf-8'))
zrodla = {}
for name, t in COMMONS.items():
    m = meta[t]
    p = os.path.join(SRC, 'com', name + '.jpg')
    if not os.path.exists(p):
        url = m['url']
        open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read())
    zapisz(Image.open(p), name)
    zrodla[name] = dict(title=t, lic=m['lic'], artist=m['artist'], page='https://commons.wikimedia.org/wiki/' + t.replace(' ', '_'))
json.dump(zrodla, open(os.path.join(SRC, 'zrodla.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(os.listdir(OUT)))
