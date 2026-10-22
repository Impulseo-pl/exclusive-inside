# -*- coding: utf-8 -*-
"""Generator dema Exclusive Inside (v2, styl jak demo ElMac). Uruchom: python _src/build.py"""
import os, re, json, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://impulseo-pl.github.io/exclusive-inside/'
IMG = os.path.join(ROOT, 'img')
TEL, TELH = '506 931 962', '+48506931962'
MAIL = 'viitovichroman@gmail.com'
FB = 'https://www.facebook.com/p/Exclusive-Inside-100093231471373/'
OFERTEO = 'https://www.oferteo.pl/classik-roman-viitovych/firma/4854063'
ZRODLA = json.load(open(os.path.join(ROOT, '_src', 'zrodla.json'), encoding='utf-8'))
LICZNIK = open(os.path.join(ROOT, '_src', 'licznik.js'), encoding='utf-8').read()
e = html.escape

# ---------- obrazy ----------
_V = {}
def variants(name):
    if name in _V: return _V[name]
    out = []
    for f in os.listdir(IMG):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.webp', f)
        if m:
            w, h = Image.open(os.path.join(IMG, f)).size
            out.append((int(m.group(1)), f, w, h))
    if not out: raise SystemExit('brak obrazu ' + name)
    _V[name] = sorted(out)
    return _V[name]

def img(p, name, alt, sizes='(max-width: 960px) 100vw, 50vw', lazy=True, style=''):
    v = variants(name); big = v[-1]
    srcset = ', '.join(f'{p}img/{f} {w}w' for _, f, w, h in v)
    a = f'<img src="{p}img/{big[1]}" srcset="{srcset}" sizes="{sizes}" width="{big[2]}" height="{big[3]}" alt="{e(alt)}"'
    a += ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    if style: a += f' style="{style}"'
    return a + '>'

def full(p, name): return p + 'img/' + variants(name)[-1][1]
def ratio(name): v = variants(name)[-1]; return f'{v[2]}/{v[3]}'

# ---------- ikony ----------
SV = lambda d, c='ico', w='1.6': f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" aria-hidden="true"><path d="{d}"/></svg>'
ARR = SV('M5 12h14M13 6l6 6-6 6', 'ico arr')
GO = SV('M7 17L17 7M9 7h8v8', 'ico', '1.8')
TELI = SV('M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2', 'ico', '1.8')
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.5 1.3 6.6L12 17.2l-5.9 3.3 1.3-6.6-4.9-4.5 6.6-.8z"/></svg>'
STARS = '<span class="stars" aria-label="5 na 5">' + STAR * 5 + '</span>'
SYG = ('<svg class="sygnet" viewBox="0 0 48 40" aria-hidden="true">'
       '<rect x="0" y="0" width="9" height="40"/><rect class="a1" x="11" y="0" width="22" height="11"/>'
       '<rect x="11" y="14.5" width="16" height="11"/><rect class="a2" x="11" y="29" width="22" height="11"/>'
       '<rect x="37" y="0" width="11" height="40"/></svg>')
INTRO = ('<div class="intro" aria-hidden="true"><div class="intro-in"><svg viewBox="0 0 48 40">'
         '<rect style="--i:0" x="0" y="0" width="9" height="40"/><rect class="a1" style="--i:1" x="11" y="0" width="22" height="11"/>'
         '<rect style="--i:2" x="11" y="14.5" width="16" height="11"/><rect class="a2" style="--i:3" x="11" y="29" width="22" height="11"/>'
         '<rect style="--i:4" x="37" y="0" width="11" height="40"/></svg>'
         '<div class="intro-name"><span>EXCLUSIVE INSIDE</span></div><div class="intro-meta">GLAZURNICTWO · ŚWIATŁOWODY</div></div></div>')

# ---------- klocki ----------
def H(text, cls='h2', tag='h2', d=0, rv=True):
    """Nagłówek łamany na linie znakiem |, *tekst* = kolor akcentu."""
    lines = []
    for k, ln in enumerate(text.split('|')):
        ln = re.sub(r'\*(.+?)\*', r'<em>\1</em>', ln)
        lines.append(f'<span class="ln"><span class="ln-i" style="--k:{k}">{ln}</span></span>')
    r = ' rv rv-h' if rv else ''
    st = f' style="--d:{d}"' if d else ''
    return f'<{tag} class="{cls}{r}"{st}>{"".join(lines)}</{tag}>'

def eyebrow(t, d=0): return f'<p class="eyebrow rv" style="--d:{d}">{t}</p>'

def fig(p, name, alt, tag=None, d=0, cls='', sizes='(max-width: 960px) 100vw, 40vw', natural=True):
    st = f'aspect-ratio:{ratio(name)};' if natural else ''
    t = f'<figcaption class="fig-tag">{e(tag)}</figcaption>' if tag else ''
    return f'<figure class="fig rv rv-img {cls}" style="{st}--d:{d}"><div class="cl">{img(p, name, alt, sizes)}</div>{t}</figure>'

def tile(p, href, name, alt, title, sub='', d=0, attrs='', sizes='(max-width: 960px) 100vw, 33vw', go=True):
    g = f'<span class="go">{GO}</span>' if go else ''
    s = f'<span>{e(sub)}</span>' if sub else ''
    return (f'<a class="tile rv rv-img" href="{href}" style="--d:{d}"{attrs}><div class="cl">{img(p, name, alt, sizes)}</div>{g}'
            f'<div class="tile-cap"><h3>{e(title)}</h3>{s}</div></a>')

def ticks(lista): return '<ul class="ticks">' + ''.join(f'<li>{e(x)}</li>' for x in lista) + '</ul>'

def secHead(ey, h, lead='', side=''):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="sec-head"><div>{eyebrow(ey)}{H(h)}</div><div class="side rv" style="--d:120">{l}{side}</div></div>'

# ---------- szkielet strony ----------
def head(p, title, desc, path, extra_ld=None):
    ld = {'@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness', 'name': 'Exclusive Inside',
          'founder': 'Roman Viitovych', 'telephone': TELH, 'email': MAIL, 'url': BASE,
          'image': BASE + 'img/' + variants('lazienka-drewno-geometria')[-1][1],
          'address': {'@type': 'PostalAddress', 'streetAddress': 'Błękitna 23', 'postalCode': '78-100', 'addressLocality': 'Kołobrzeg', 'addressCountry': 'PL'},
          'geo': {'@type': 'GeoCoordinates', 'latitude': 54.1629, 'longitude': 15.5379},
          'areaServed': ['województwo zachodniopomorskie', 'województwo lubuskie', 'województwo wielkopolskie'],
          'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '5.0', 'reviewCount': '3'},
          'sameAs': [FB, OFERTEO], 'vatID': 'PL6751463258'}
    lds = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    if extra_ld: lds += f'<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>'
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}img/{variants('lazienka-drewno-geometria')[1][1]}">
<meta property="og:locale" content="pl_PL">
<meta name="theme-color" content="#0E0D0C">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<script>(function(d){{d.classList.add('anim');try{{if(!sessionStorage.getItem('ei_intro'))d.classList.add('intro-on');else{{var k=sessionStorage.getItem('ei_k');if(k){{d.classList.add('przyjscie');d.style.setProperty('--kurtyna',k);sessionStorage.removeItem('ei_k')}}}}}}catch(e){{}}setTimeout(function(){{d.classList.remove('intro-on','przyjscie');d.classList.add('hero-go')}},7000)}})(document.documentElement)</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@400..700&family=Funnel+Sans:wght@400..600&display=swap">
<link rel="stylesheet" href="{p}assets/styles.css">
{lds}
<script>{LICZNIK}</script>
'''

def topbar(p, galaz, menu):
    links = ''.join(f'<a class="nl" href="{h}"{" aria-current=\"page\"" if a else ""}>{t}</a>' for h, t, a in menu)
    mlinks = ''.join(f'<a class="ml" href="{h}">{t}</a>' for h, t, a in menu)
    g_ta = ' class="ta"' if galaz == 'g' else ''
    s_ta = ' class="ta"' if galaz == 's' else ''
    przel = f'<nav class="przel" aria-label="Działy firmy"><a href="{p}glazurnictwo/"{g_ta}>Glazurnictwo</a><a href="{p}swiatlowody/"{s_ta}>Światłowody</a></nav>'
    sub = 'Glazurnictwo i wykończenia' if galaz == 'g' else 'Instalacje światłowodowe'
    return f'''<header class="head">
<div class="head-in">
<a class="brand" href="{p}" aria-label="Exclusive Inside – wybór działu">{SYG}<span><b>Exclusive Inside</b><small>{sub}</small></span></a>
{przel}
<nav class="nav-links" aria-label="Menu">{links}</nav>
<a class="btn btn-acc nav-cta" href="tel:{TELH}">{TELI}<span>{TEL}</span></a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
</div>
</header>
<div class="mnav"><div class="mnav-in">{przel}{mlinks}<div class="mnav-foot"><a class="btn btn-acc" href="tel:{TELH}">{TELI}Zadzwoń: {TEL}</a><span>ul. Błękitna 23, Kołobrzeg · {MAIL}</span></div></div></div>'''

def foot(p):
    return f'''<footer class="foot">
<div class="wrap">
<div class="foot-top">
<div><p class="foot-claim">Wnętrza wykończone dokładnie. Światłowód doprowadzony porządnie.</p><a class="btn btn-ghost" href="tel:{TELH}">{TELI}{TEL}</a></div>
<div><h4>Glazurnictwo</h4><ul><li><a href="{p}glazurnictwo/#specjalizacje">Specjalizacje</a></li><li><a href="{p}glazurnictwo/realizacje/">Realizacje</a></li><li><a href="{p}glazurnictwo/#jak-pracujemy">Jak pracujemy</a></li><li><a href="{p}glazurnictwo/#opinie">Opinie</a></li></ul></div>
<div><h4>Światłowody</h4><ul><li><a href="{p}swiatlowody/#zakres">Zakres prac</a></li><li><a href="{p}swiatlowody/#trasa">Jak powstaje przyłącze</a></li><li><a href="{p}swiatlowody/#dla-kogo">Dla kogo</a></li><li><a href="{p}swiatlowody/#pytania">Pytania</a></li></ul></div>
<div><h4>Kontakt</h4><ul><li><a href="tel:{TELH}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>ul. Błękitna 23, 78-100 Kołobrzeg</li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{OFERTEO}" target="_blank" rel="noopener">Oferteo</a></li></ul></div>
</div>
<div class="foot-mark" aria-hidden="true">Exclusive Inside</div>
<div class="foot-bottom"><span>© 2026 Exclusive Inside · Roman Viitovych · NIP 675-146-32-58</span><a href="{p}zrodla-zdjec/">Źródła zdjęć poglądowych</a></div>
</div>
</footer>'''

def kontakt(p, galaz):
    if galaz == 'g':
        tematy = ['Łazienka', 'Schody', 'Blat lub wyspa', 'Wykończenie mieszkania lub domu', 'Inne']
        ph = 'Np. łazienka ok. 6 m², płyty 120×60, mam już płytki / szukam projektu…'
        h, lead = 'Opowiedz, co|*chcesz zrobić.*', 'Oddzwonimy, umówimy oględziny i pomiar, a potem przygotujemy wycenę.'
    else:
        tematy = ['Przyłącze do domu', 'Budynek wielorodzinny', 'Wykop lub przewiert', 'Spawanie i pomiary', 'Podwykonawstwo dla operatora', 'Inne']
        ph = 'Np. dom jednorodzinny, operator już wybrany, trzeba doprowadzić kabel od skrzynki przy drodze…'
        h, lead = 'Gdzie mamy|*doprowadzić światłowód?*', 'Napisz, gdzie jest budynek i na jakim etapie jest przyłącze – oddzwonimy z odpowiedzią.'
    opts = ''.join(f'<option>{t}</option>' for t in tematy)
    return f'''<section class="dk cta-band" id="kontakt">
<div class="wrap cta-grid">
<div>
{eyebrow('Kontakt')}{H(h)}
<p class="lead rv">{lead}</p>
<div class="rv"><span class="lbl">Najszybciej telefonicznie</span>
<a class="cta-phone" href="tel:{TELH}">{TEL}</a>
<dl class="dane"><dt>Firma</dt><dd>Exclusive Inside · Roman Viitovych</dd><dt>Adres</dt><dd>ul. Błękitna 23, 78-100 Kołobrzeg</dd><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd><dt>Obszar</dt><dd>zachodniopomorskie, lubuskie, wielkopolskie</dd></dl>
<div class="mapa" id="mapa" role="img" aria-label="Mapa: ul. Błękitna 23, Kołobrzeg"></div></div>
</div>
<form class="form rv" style="--d:150" data-mail="{MAIL}">
<h3>Zapytanie o wycenę</h3>
<div class="dwa"><div><label for="f-imie">Imię</label><input id="f-imie" name="imie" autocomplete="given-name" required></div>
<div><label for="f-tel">Telefon</label><input id="f-tel" name="tel" type="tel" autocomplete="tel" required></div></div>
<div class="dwa"><div><label for="f-temat">Czego dotyczy</label><select id="f-temat" name="temat">{opts}</select></div>
<div><label for="f-m">Miejscowość</label><input id="f-m" name="miejsce"></div></div>
<label for="f-opis">Opis</label><textarea id="f-opis" name="opis" placeholder="{e(ph)}"></textarea>
<button class="btn btn-acc" type="submit">Wyślij zapytanie {ARR}</button>
<p class="info">Odpowiadamy telefonicznie lub mailowo. Dane służą tylko do odpowiedzi na zapytanie.</p>
</form>
</div>
</section>'''

def scripts(p, mapa=True):
    s = ''
    if mapa:
        s += ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">\n'
              '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" defer></script>\n')
    return s + f'<script src="{p}assets/lenis.min.js" defer></script>\n<script src="{p}assets/app.js" defer></script>\n'

def strona(p, galaz, title, desc, path, menu, tresc, mapa=True, ld=None):
    cls = 'glaz' if galaz == 'g' else 'swiatlo'
    return (head(p, title, desc, path, ld) + '</head>\n'
            f'<body class="{cls}">\n<a class="skip" href="#tresc">Przejdź do treści</a>\n{INTRO}<div class="kurtyna" aria-hidden="true"></div>\n'
            + topbar(p, galaz, menu) + f'\n<main id="tresc">\n{tresc}\n</main>\n' + foot(p)
            + f'\n<a class="btn btn-acc sticky-call" href="tel:{TELH}">{TELI}Zadzwoń: {TEL}</a>\n' + scripts(p, mapa) + '</body>\n</html>\n')

def zapisz(path, s):
    fp = os.path.join(ROOT, path, 'index.html') if path else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(s)

def hero(p, media, alt, pos, tag, h1, lead, ctas, foot_l, foot_m, src=''):
    s = f'<span class="hero-src">{src}</span>' if src else ''
    if isinstance(media, list):
        med = '<div class="hero-media tryp">' + ''.join(img(p, n, a, '(max-width: 620px) 34vw, 22vw', lazy=False) for n, a in media) + '</div>'
    else:
        med = f'<div class="hero-media">{img(p, media, alt, "100vw", lazy=False, style=f"--pos:{pos}")}</div>'
    return f'''<section class="hero">
{med}{s}
<div class="hero-in">
<div class="hero-tag up" style="--d:0"><span class="dot"></span>{tag[0]}<span class="sep"></span><span class="muted">{tag[1]}</span></div>
{H(h1, 'h1', 'h1', rv=False)}
<p class="hero-lead up" style="--d:380">{lead}</p>
<div class="hero-ctas up" style="--d:500">{ctas}</div>
<div class="hero-foot up" style="--d:650"><div class="rate">{foot_l}</div><span>{foot_m}</span><span class="cue"><span class="cue-line"><i></i></span>Przewiń</span></div>
</div>
</section>'''

def strip(items):
    return '<div class="strip"><div class="strip-in">' + ''.join(f'<div class="strip-it"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in items) + '</div></div>'

def svc_blocks(p, bloki):
    out = ''
    for i, (bid, t, opis, lista, fotki, cta) in enumerate(bloki):
        figs = ''.join(fig(p, n, a, tag, d=k * 140) for k, (n, a, tag) in enumerate(fotki))
        out += (f'<div class="svc-block{" flip" if i % 2 else ""}" id="{bid}"><div class="wrap svc-row">'
                f'<div class="svc-figs{" one" if len(fotki) == 1 else ""}">{figs}</div>'
                f'<div class="svc-txt"><span class="nr rv">{i + 1:02d} / {len(bloki):02d}</span>{H(t, "")}'
                f'<p class="rv">{opis}</p><div class="rv">{ticks(lista)}</div><div class="rv">{cta}</div></div></div></div>')
    return out

def faq(pyt):
    items = ''.join(f'<details class="faq-item rv" style="--d:{k * 60}"><summary>{q}<i></i><i></i></summary><div class="faq-a"><p>{a}</p></div></details>' for k, (q, a) in enumerate(pyt))
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pyt]}
    return items, ld

def stop(p, kier, media, alt, ey, h, lead, href, btn):
    return f'''<section class="stop do-{kier}">
<div class="stop-bg">{img(p, media, alt, '100vw')}</div>
<div class="stop-in">{eyebrow(ey)}{H(h)}<p class="lead rv">{lead}</p><div class="rv"><a class="btn btn-acc" href="{href}">{btn} {ARR}</a></div></div>
</section>'''

def about(p, h, txt, btn):
    return f'''<section class="sec">
<div class="wrap about">
{fig(p, 'bus-firmowy', 'Firmowy bus Exclusive Inside z numerem telefonu', 'Nasz bus – po nim poznasz nas na budowie')}
<div>{eyebrow('O firmie')}{H(h)}<p class="rv" style="margin-top:24px">{txt}</p>
<div class="stats rv">
<div class="stat"><b><span class="num" data-to="5,0">5,0</span></b><span>średnia ocen na Oferteo, 3 opinie</span></div>
<div class="stat"><b><span class="num" data-to="5">5</span><small>lat</small></b><span>na Oferteo, z potwierdzonymi zleceniami</span></div>
<div class="stat"><b><span class="num" data-to="3">3</span><small>woj.</small></b><span>zachodniopomorskie, lubuskie, wielkopolskie</span></div>
</div>
<div class="rv">{btn}</div></div>
</div>
</section>'''

# ---------- dane: realizacje i opinie ----------
KAT = [('lazienki', 'Łazienki'), ('schody', 'Schody'), ('blaty', 'Blaty i zabudowy'), ('sciany', 'Ściany i dekory'), ('budowa', 'W trakcie prac')]
FOTY = [
    ('lazienki', 'lazienka-drewno-geometria', 'Łazienka z ryflowaną ścianą w drewnie, wanna wolnostojąca, czarna armatura'),
    ('lazienki', 'lazienka-czarny-marmur-zloto', 'Czarny marmur ze złotym żyłkowaniem w strefie WC'),
    ('lazienki', 'prysznic-meander', 'Prysznic walk-in – czarno-biały wzór od podłogi po ścianę'),
    ('lazienki', 'lazienka-led-umywalka', 'Blat z umywalką i zabudowa pralki, podświetlenie LED'),
    ('lazienki', 'lazienka-czarny-marmur', 'Łazienka w czarnym i białym marmurze, kabina bez brodzika'),
    ('schody', 'schody-spiek-prety', 'Schody okładane płytą, balustrada z czarnych prętów'),
    ('lazienki', 'lazienka-zielona-oktagon', 'Butelkowa zieleń na ścianach, podłoga z oktagonów'),
    ('lazienki', 'lazienka-szara-prysznic', 'Szara płyta wielkoformatowa i drewno na podłodze'),
    ('blaty', 'wyspa-spiek-marmur', 'Wyspa obłożona płytą wielkoformatową w marmurze'),
    ('lazienki', 'zabudowa-wc-marmur', 'Zabudowa stelaża WC z płyty wielkoformatowej w marmurze'),
    ('schody', 'schody-zewnetrzne-szklo', 'Schody zewnętrzne z płyty w drewnie, balustrada szklana'),
    ('sciany', 'heksagony-3d', 'Heksagony 3D w bieli i kobalcie'),
    ('lazienki', 'lazienka-led-prysznic', 'Prysznic z wnęką i linią światła'),
    ('schody', 'schody-czarne-prety', 'Biegi schodów obłożone płytą, czarne pręty'),
    ('lazienki', 'lazienka-szara-umywalka', 'Umywalka nablatowa, ściany z szarej płyty'),
    ('sciany', 'korytarz-cegla', 'Korytarz z cegłą rozbiórkową i liniami światła'),
    ('lazienki', 'lazienka-czarny-marmur-2', 'Strefa prania i prysznic – czarny marmur'),
    ('schody', 'schody-spiek-prety-2', 'Schody w jasnej płycie – widok z dołu'),
    ('lazienki', 'lazienka-szara-kabina', 'Kabina z wnęką w płycie'),
    ('sciany', 'sciana-ramy-dekor', 'Ściana z ramami i wypełnieniem dekoracyjnym'),
    ('lazienki', 'prysznic-meander-2', 'Wnęka i dekor w strefie prysznica'),
    ('budowa', 'plyty-wielkoformatowe-podloga', 'Płyty wielkoformatowe na podłodze – układanie'),
    ('lazienki', 'lazienka-led-zabudowa', 'Zabudowa z płyty w połysku, podświetlenie sufitu'),
    ('schody', 'schody-zewnetrzne-klinkier', 'Schody wejściowe z płytek klinkierowych'),
    ('sciany', 'fototapeta-las', 'Fototapeta z mglistym lasem'),
    ('lazienki', 'lazienka-szara-wc', 'Stelaż WC obłożony płytą'),
    ('budowa', 'schody-krecone-budowa', 'Schody kręcone w trakcie okładania'),
    ('schody', 'schody-spiek-prety-3', 'Schody i ściana w płycie drewnopodobnej'),
    ('sciany', 'bateria-podtynkowa-beton', 'Bateria podtynkowa na płycie imitującej beton'),
    ('lazienki', 'lazienka-zielona-oktagon-2', 'Oktagony z czarną kostką – widok z góry'),
    ('budowa', 'wanna-narozna-odplyw', 'Wanna narożna i odpływ liniowy w trakcie prac'),
]
OPINIE = [
    ('A. S.', 'Szczerze polecam. Roman miał zrobić u mnie jedną łazienkę, zrobił cztery łazienki, położył płytki na schodach, zamontował trelki i pomalował cały korytarz. Wszystko ustala z inwestorem, nie podejmuje sam decyzji, nie marnuje płytek na bezsensowne cięcia i najważniejsze – sprząta po sobie!'),
    ('T. F.', 'Pan Roman robił u mnie łazienkę. Jestem mega zadowolona z wykonania. Oceniam robotę na 10 gwiazdek. Wyśmienity fachowiec (kocha to, co robi), bardzo uczciwy. Polecam w 100%.'),
    ('A. K.', 'Fachowość, staranność detali i dobra komunikacja, polecam tę firmę.'),
]

# =====================================================================
# 1. strona wyboru
# =====================================================================
def wybor():
    p = ''
    s = head(p, 'Exclusive Inside – glazurnictwo i instalacje światłowodowe, Kołobrzeg',
             'Exclusive Inside, Roman Viitovych: łazienki, schody i blaty z płyt wielkoformatowych oraz instalacje światłowodowe. Kołobrzeg, zachodniopomorskie, lubuskie, wielkopolskie. Tel. 506 931 962.', '')
    s += f'''</head>
<body class="glaz gate">
{INTRO}<div class="kurtyna" aria-hidden="true"></div>
<header class="head">
<div class="head-in">
<a class="brand" href="./" aria-label="Exclusive Inside">{SYG}<span><b>Exclusive Inside</b><small>Roman Viitovych · Kołobrzeg</small></span></a>
<nav class="przel" aria-label="Wybierz dział"><a class="g" href="glazurnictwo/">Glazurnictwo</a><a class="s" href="swiatlowody/">Światłowody</a></nav>
<a class="btn btn-ghost nav-cta" href="tel:{TELH}">{TELI}<span>{TEL}</span></a>
</div>
</header>
<main class="dzial">
<h1 class="sr">Exclusive Inside – glazurnictwo i instalacje światłowodowe</h1>
<a class="pol glaz" href="glazurnictwo/">
<div class="med">{img(p, 'lazienka-drewno-geometria', 'Łazienka wykonana przez Exclusive Inside', '(max-width: 960px) 100vw, 60vw', lazy=False)}</div>
<span class="szew"></span>
<div class="pol-in">
<span class="nr up" style="--d:100">Dział 01 · płytki wielkoformatowe i wykończenia</span>
{H('Glazurnictwo', 'pol-h', 'h2', rv=False)}
<p class="up" style="--d:350">Łazienki, schody, wyspy i blaty z dużych płyt. Projekt z wykonaniem – od wyrównania ścian po biały montaż.</p>
<span class="btn btn-acc up" style="--d:450">Wejdź {ARR}</span>
<div class="tagi up" style="--d:600"><span>Łazienki</span><span>Schody</span><span>Wyspy i blaty</span><span>Biały montaż</span></div>
</div>
</a>
<a class="pol swiatlo" href="swiatlowody/">
<div class="med">{img(p, 'spawanie-wlokien', 'Spawanie włókien światłowodowych (zdjęcie poglądowe)', '(max-width: 960px) 100vw, 60vw', lazy=False)}</div>
<div class="pol-in">
<span class="nr up" style="--d:200">Dział 02 · instalacje światłowodowe</span>
{H('Światłowody', 'pol-h', 'h2', rv=False)}
<p class="up" style="--d:450">Przyłącza do domów, wykopy i przewierty sterowane, spawanie włókien. Od skrzynki przy drodze do gniazdka w domu.</p>
<span class="btn btn-acc up" style="--d:550">Wejdź {ARR}</span>
<div class="tagi up" style="--d:700"><span>Przyłącza</span><span>Przewierty</span><span>Spawanie</span><span>Okablowanie budynków</span></div>
</div>
</a>
</main>
''' + scripts(p, mapa=False) + '</body>\n</html>\n'
    zapisz('', s)

# =====================================================================
# 2. glazurnictwo
# =====================================================================
def MENU_G(p, ta=''):
    return [(f'{p}glazurnictwo/#specjalizacje', 'Specjalizacje', False), (f'{p}glazurnictwo/realizacje/', 'Realizacje', ta == 'r'),
            (f'{p}glazurnictwo/#jak-pracujemy', 'Jak pracujemy', False), (f'{p}glazurnictwo/#opinie', 'Opinie', False),
            (f'{p}glazurnictwo/#kontakt', 'Kontakt', False)]

def glazurnictwo():
    p = '../'
    zadzwon = f'<a class="btn btn-acc" href="tel:{TELH}">{TELI}Zadzwoń: {TEL}</a>'
    h = hero(p, [('lazienka-czarny-marmur-zloto', 'Czarny marmur ze złotym żyłkowaniem'), ('lazienka-drewno-geometria', 'Łazienka z ryflowaną ścianą w drewnie'), ('prysznic-meander', 'Prysznic z czarno-białym wzorem')], '', '',
             ('Glazurnictwo', 'Kołobrzeg i okolice'), 'Łazienki|z dużych płyt.|*Pod klucz.*',
             'Exclusive Inside – Roman Viitovych. Łazienki, schody, wyspy i blaty z płyt wielkoformatowych. Zaprojektujemy łazienkę albo wykonamy Twój projekt – od wyrównania ścian po biały montaż.',
             zadzwon + f'<a class="btn btn-ghost" href="realizacje/">Zobacz realizacje {ARR}</a>',
             f'{STARS}<b>5,0</b><span>3 opinie na Oferteo, wszystkie na 5</span>', 'zachodniopomorskie · lubuskie · wielkopolskie')
    st = strip([('Łazienki', 'w dużych formatach'), ('Schody', 'wewnętrzne i zewnętrzne'), ('Wyspy i blaty', 'z płyt wielkoformatowych'),
                ('Wzory i dekory', 'oktagony, meandry, 3D'), ('Biały montaż', 'armatura, ceramika, kabiny')])
    kafle = ''.join(tile(p, f'#{a}', n, alt, t, s, d=i * 110, sizes='(max-width: 1180px) 50vw, 25vw') for i, (a, n, alt, t, s) in enumerate([
        ('lazienki', 'lazienka-czarny-marmur-zloto', 'Łazienka w czarnym marmurze', 'Łazienki', 'Płyty wielkoformatowe od podłogi po sufit'),
        ('schody', 'schody-spiek-prety', 'Schody okładane płytą', 'Schody', 'Okładziny z płyty, wewnątrz i na zewnątrz'),
        ('blaty', 'wyspa-spiek-marmur', 'Wyspa z płyty w marmurze', 'Wyspy i blaty', 'Ta sama płyta co na ścianach'),
        ('wzory', 'prysznic-meander', 'Prysznic z czarno-białym wzorem', 'Wzory i dekory', 'Rozkład ustalany przed pierwszym cięciem')]))
    bloki = [
        ('lazienki', 'Łazienki|*w dużych formatach.*',
         'Płyty 120×60, 120×120 i większe na ścianach i podłodze, mało fug, równe linie od progu po sufit. Ściany pod duży format wyrównujemy wcześniej, bo przy takiej płycie widać każdy milimetr.',
         ['Kabiny bez brodzika z odpływem liniowym', 'Zabudowy stelaży WC i wnęki z płyty', 'Podświetlenie LED w niszach i suficie', 'Biały montaż: armatura podtynkowa, ceramika, kabiny'],
         [('lazienka-czarny-marmur', 'Łazienka w czarnym marmurze, kabina bez brodzika', 'Czarny marmur, kabina bez brodzika'), ('zabudowa-wc-marmur', 'Zabudowa stelaża WC z płyty w marmurze', 'Zabudowa WC z jednej płyty')],
         f'<a class="btn btn-ghost" href="realizacje/">Łazienki w galerii {ARR}</a>'),
        ('schody', 'Schody|*okładane płytą.*',
         'Schody wewnętrzne i zewnętrzne: stopnice i podstopnie z płyty, docinane tak, żeby rysunek płyty szedł przez cały bieg. Robimy też schody kręcone i schody wejściowe z klinkieru.',
         ['Schody wewnętrzne z płyty drewnopodobnej i kamiennej', 'Schody zewnętrzne z klinkieru', 'Schody kręcone – docinki na łuku'],
         [('schody-spiek-prety-2', 'Schody okładane płytą z balustradą z prętów', 'Schody w jasnej płycie'), ('schody-zewnetrzne-szklo', 'Schody zewnętrzne z balustradą szklaną', 'Schody zewnętrzne')],
         f'<a class="btn btn-ghost" href="realizacje/">Schody w galerii {ARR}</a>'),
        ('blaty', 'Wyspy i blaty|*z jednej płyty.*',
         'Wyspa kuchenna, blat łazienkowy albo zabudowa pralki obłożona tą samą płytą co ściany. Narożniki łączone na kąt, żeby żyłkowanie przechodziło z blatu na bok.',
         ['Wyspy kuchenne', 'Blaty pod umywalki nablatowe', 'Zabudowy pralek i szafek'],
         [('wyspa-spiek-marmur', 'Wyspa obłożona płytą w marmurze', 'Wyspa w trakcie prac – narożniki na kąt')],
         f'<a class="btn btn-ghost" href="#kontakt">Zapytaj o blat {ARR}</a>'),
        ('wzory', 'Wzory i dekory|*rozplanowane z góry.*',
         'Oktagony z kostką, meandry, heksagony 3D – układy, przy których liczy się rozplanowanie przed pierwszym cięciem. Każdy wzór najpierw rozkładamy na sucho i uzgadniamy z inwestorem.',
         ['Oktagony i mozaiki podłogowe', 'Dekory ścienne i heksagony 3D', 'Fototapety, cegła, sztukateria'],
         [('lazienka-zielona-oktagon', 'Zielona łazienka z podłogą z oktagonów', 'Oktagony i butelkowa zieleń'), ('heksagony-3d', 'Heksagony 3D', 'Heksagony 3D')],
         f'<a class="btn btn-ghost" href="realizacje/">Wszystkie realizacje {ARR}</a>'),
    ]
    kroki = [
        ('Oględziny i pomiar', 'Przyjeżdżamy, mierzymy, sprawdzamy ściany i podłogę. Rozmawiamy o płytkach, układzie i armaturze.', None),
        ('Projekt łazienki', 'Gdy nie masz jeszcze projektu, przygotowujemy go razem z doborem płytek – potem wykonujemy dokładnie to, co jest na rysunku.', ('projekt-wizualizacja', 'Wydruk projektu łazienki')),
        ('Podłoże i hydroizolacja', 'Wyrównanie ścian pod duży format, zabudowy z płyt, hydroizolacja w strefach mokrych, przygotowanie pod odpływ liniowy.', ('wanna-narozna-odplyw', 'Odpływ liniowy przy wannie w trakcie prac')),
        ('Układanie', 'Rozkład płytek ustalamy z Tobą przed pierwszym cięciem. Nie podejmujemy decyzji za klienta i nie marnujemy płytek.', ('plyty-wielkoformatowe-podloga', 'Układanie płyt wielkoformatowych')),
        ('Biały montaż i sprzątanie', 'Montujemy ceramikę, armaturę i kabinę, a po pracy zostawiamy porządek – klienci sami piszą o tym w opiniach.', None),
    ]
    kr = ''.join(f'<li class="step" data-nazwa="{t}"><span class="no">{i + 1:02d} / {len(kroki):02d}</span><h3>{t}</h3><p>{o}</p>'
                 + (fig(p, f[0], f[1], natural=False) if f else '') + '</li>' for i, (t, o, f) in enumerate(kroki))
    gal = ''.join(tile(p, 'realizacje/', n, a, t, s, d=i * 120, sizes='(max-width: 960px) 100vw, 50vw') for i, (n, a, t, s) in enumerate([
        ('lazienka-szara-prysznic', 'Łazienka z szarej płyty i drewnianej podłogi', 'Szara płyta i drewno', 'Łazienka z kabiną i wnęką'),
        ('lazienka-led-umywalka', 'Łazienka z podświetleniem LED', 'Linie światła', 'Blat, zabudowa pralki, LED'),
        ('korytarz-cegla', 'Korytarz z cegłą rozbiórkową', 'Cegła i światło', 'Korytarz w domu jednorodzinnym')]))
    op_feat = OPINIE[0]
    op = (f'<figure class="op-card feat rv"><blockquote><p>„{e(op_feat[1])}”</p></blockquote>'
          f'<div class="op-foty">{img(p, "schody-spiek-prety-3", "Zdjęcie klienta do opinii – schody", "160px")}{img(p, "lazienka-szara-umywalka", "Zdjęcie klienta do opinii – łazienka", "160px")}{img(p, "lazienka-szara-kabina", "Zdjęcie klienta do opinii – kabina", "160px")}</div>'
          f'<figcaption><span class="av">AS</span><span><b>{op_feat[0]}</b>Oferteo · ze zdjęciami realizacji</span></figcaption></figure>')
    op += ''.join(f'<figure class="op-card rv" style="--d:{120 * (k + 1)}"><blockquote><p>„{e(t)}”</p></blockquote><figcaption><span class="av">{a.replace(". ", "").replace(".", "")}</span><span><b>{a}</b>Oferteo · {STARS}</span></figcaption></figure>' for k, (a, t) in enumerate(OPINIE[1:]))
    extra = [('Wykończenia pod klucz', 'Mieszkania i domy – od wyburzeń po malowanie.'), ('Gładzie i malowanie', 'Ściany i sufity, także w lokalach firmowych.'),
             ('Zabudowy z płyt G-K', 'Ścianki, sufity, zabudowy stelaży i wnęk.'), ('Tapety i fototapety', 'Tapetowanie i fototapety na całą ścianę.'),
             ('Drobna hydraulika', 'Podejścia pod armaturę, drobne naprawy.'), ('Wyburzenia', 'Rozbiórki wewnątrz budynków przed remontem.'),
             ('Instalacje elektryczne', 'Montaż instalacji przy remoncie.'), ('Cegła i dekory', 'Cegła rozbiórkowa, sztukateria, ramy.')]
    ex = ''.join(f'<div class="extra rv" style="--d:{(k % 4) * 80}"><i></i><h3>{a}</h3><p>{b}</p></div>' for k, (a, b) in enumerate(extra))
    fq, ld_faq = faq([
        ('Czy mogę sam kupić płytki?', 'Tak. Doradzimy format i ilość z zapasem na docinki, zanim pojedziesz do sklepu – przy płytach wielkoformatowych to ważne, bo każdą płytę trzeba rozplanować.'),
        ('Robicie projekt łazienki?', 'Tak – projekt z wykonaniem, razem z doborem płytek. Jeśli masz projekt od architekta, wykonamy go według rysunków.'),
        ('Jak wygląda wycena?', 'Po rozmowie przyjeżdżamy na oględziny i pomiar. Cena zależy od metrażu, formatu płyt i stanu ścian, dlatego wyceniamy po zobaczeniu pomieszczenia.'),
        ('Gdzie pracujecie?', 'Kołobrzeg i okolice oraz województwa zachodniopomorskie, lubuskie i wielkopolskie.'),
        ('Co z bałaganem po remoncie?', 'Sprzątamy po sobie – klienci zwracają na to uwagę w opiniach na Oferteo.')])
    tresc = f'''{h}
{st}
<section class="sec" id="specjalizacje">
<div class="wrap">
{secHead('Specjalizacje', 'W czym jesteśmy|*najlepsi.*', 'Wykańczamy całe wnętrza, ale najwięcej pracy i najwięcej poleceń mamy z łazienek, schodów i blatów z dużych płyt.', f'<a class="btn btn-ghost" href="realizacje/">Cała galeria {ARR}</a>')}
<div class="tiles-4">{kafle}</div>
</div>
</section>
<section class="pp2">{svc_blocks(p, bloki)}</section>
<section class="sec dk">
<div class="wrap">
{secHead('Projekt i wykonanie', 'Ta sama łazienka.|*Na papierze i na żywo.*', 'Po lewej wydruk projektu, który dostał inwestor. Po prawej ta sama łazienka po naszej pracy.')}
<div class="para">
<figure class="fig rv rv-img" style="aspect-ratio:{ratio('projekt-wizualizacja')}"><div class="cl">{img(p, 'projekt-wizualizacja', 'Wydruk projektu łazienki z ryflowaną ścianą', '(max-width: 960px) 100vw, 45vw')}</div><span class="etyk">Projekt</span></figure>
<figure class="fig rv rv-img" style="aspect-ratio:{ratio('lazienka-drewno-geometria')};--d:160"><div class="cl">{img(p, 'lazienka-drewno-geometria', 'Gotowa łazienka zgodna z projektem', '(max-width: 960px) 100vw, 45vw')}</div><span class="etyk">Wykonanie</span></figure>
</div>
<div class="para-opis"><p class="rv">Ściana z ryflowanej płyty drewnopodobnej, wnęka z podświetleniem, szara płyta na pozostałych ścianach, czarna armatura i wanna wolnostojąca.</p><p class="rv" style="--d:120">Masz projekt od architekta – wykonamy go. Nie masz – zaprojektujemy łazienkę razem z doborem płytek.</p></div>
</div>
</section>
{about(p, 'Roman Viitovych|*i ekipa Exclusive Inside.*', 'Zajmujemy się wykończeniami wnętrz i remontami. Najwięcej pracy mamy przy łazienkach, schodach i blatach z płyt wielkoformatowych – tam, gdzie liczy się rozplanowanie każdego cięcia i równe linie od podłogi po sufit.', zadzwon)}
<section class="sec dk" id="jak-pracujemy">
<div class="wrap proc-grid">
<div class="proc-side">{eyebrow('Jak pracujemy')}{H('Każda decyzja|*razem z Tobą.*')}<p class="lead rv" style="margin-top:24px">Od pomiaru po sprzątanie – wiesz, na jakim etapie jest Twoja łazienka.</p>
<div class="proc-count rv"><b>01</b><span>/ {len(kroki):02d}</span></div><div class="proc-now rv">{kroki[0][0]}</div></div>
<div class="proc-steps"><span class="wire"><i></i></span><ol class="proc-ol">{kr}</ol></div>
</div>
</section>
<section class="sec">
<div class="wrap">
{secHead('Realizacje', 'Tak wygląda|*skończona robota.*', 'Zdjęcia z naszych budów – bez retuszu i bez wizualizacji.', f'<a class="btn btn-ghost" href="realizacje/">Wszystkie realizacje ({len(FOTY)}) {ARR}</a>')}
<div class="gal-3">{gal}</div>
</div>
</section>
<section class="sec pp2" id="opinie">
<div class="wrap">
{secHead('Opinie', 'Co piszą|*klienci.*', '', f'<div class="op-meta"><span class="big">5,0</span><span>{STARS}<small>3 opinie na Oferteo, wszystkie na 5</small></span></div><a class="btn btn-ghost" href="{OFERTEO}" target="_blank" rel="noopener">Profil na Oferteo {ARR}</a>')}
<div class="opinie-grid">{op}</div>
</div>
</section>
<section class="sec dk2">
<div class="wrap">
{secHead('Przy okazji remontu', 'Robimy|*też resztę.*', 'Przy łazience często wychodzi coś więcej – nie musisz szukać drugiej ekipy.')}
<div class="extra-grid">{ex}</div>
</div>
</section>
<section class="sec" id="pytania">
<div class="wrap faq-wrap">
<div class="faq-side">{eyebrow('Pytania')}{H('Zanim|*zadzwonisz.*')}<p class="lead rv" style="margin-top:24px">Nie ma tu Twojego pytania? Zadzwoń – odpowiemy od razu.</p><div class="rv">{zadzwon}</div></div>
<div>{fq}</div>
</div>
</section>
{stop(p, 's', 'spawanie-wlokien', 'Spawanie włókien światłowodowych (zdjęcie poglądowe)', 'Drugi dział firmy', 'Remont i światłowód|*jedną ekipą.*', 'Zanim położymy płytki, możemy doprowadzić światłowód do domu i schować trasę kabla w ścianach – bez kucia drugi raz.', p + 'swiatlowody/', 'Instalacje światłowodowe')}
{kontakt(p, 'g')}'''
    zapisz('glazurnictwo', strona(p, 'g', 'Glazurnik Kołobrzeg – łazienki i schody z płyt wielkoformatowych | Exclusive Inside',
                                   'Glazurnik z Kołobrzegu: łazienki z płyt wielkoformatowych, schody, wyspy i blaty, projekt z wykonaniem, biały montaż. Opinie 5,0 na Oferteo. Tel. 506 931 962.',
                                   'glazurnictwo/', MENU_G(p), tresc, ld=ld_faq))

def realizacje():
    p = '../../'
    licz = {k: sum(1 for f in FOTY if f[0] == k) for k, _ in KAT}
    chips = f'<button class="chip ta" data-k="wszystkie">Wszystkie<sup>{len(FOTY)}</sup></button>' + ''.join(
        f'<button class="chip" data-k="{k}">{t}<sup>{licz[k]}</sup></button>' for k, t in KAT)
    mur = ''.join(f'<a class="tile rv rv-img" href="{full(p, n)}" data-lb data-k="{k}" data-opis="{e(a)}" style="--d:{(i % 3) * 90}"><div class="cl">{img(p, n, a, "(max-width: 620px) 50vw, 33vw")}</div><div class="tile-cap"><span>{e(a)}</span></div></a>' for i, (k, n, a) in enumerate(FOTY))
    tresc = f'''<section class="pagehead">
<div class="hero-media">{img(p, 'lazienka-czarny-marmur-zloto', 'Czarny marmur ze złotym żyłkowaniem', '100vw', lazy=False, style='--pos:50% 40%')}</div>
<div class="ph-in">
<div class="crumb up"><a href="../">Glazurnictwo</a><span class="sl"></span><span>Realizacje</span></div>
{H('Realizacje.|*Bez wizualizacji.*', 'h1', 'h1', rv=False)}
<p class="ph-lead up" style="--d:300">Łazienki, schody, blaty i ściany wykonane przez Exclusive Inside. Część zdjęć dodali sami klienci do swoich opinii.</p>
<div class="chips up" style="--d:420" role="toolbar" aria-label="Filtruj realizacje">{chips}</div>
</div>
</section>
<section class="sec" style="padding-top:clamp(50px, 6vw, 90px)"><div class="wrap"><div class="masonry">{mur}</div></div></section>
{stop(p, 's', 'mikrorurki', 'Mikrorurki pod kable światłowodowe (zdjęcie poglądowe)', 'Drugi dział firmy', 'Światłowód|*przy okazji remontu.*', 'Doprowadzamy światłowód do domu i chowamy trasę kabla, zanim powstanie wykończenie.', p + 'swiatlowody/', 'Instalacje światłowodowe')}
{kontakt(p, 'g')}'''
    zapisz('glazurnictwo/realizacje', strona(p, 'g', 'Realizacje – łazienki, schody, blaty | Exclusive Inside Kołobrzeg',
                                            'Galeria realizacji Exclusive Inside: łazienki z płyt wielkoformatowych, schody okładane płytą, wyspy i blaty, dekory ścienne.',
                                            'glazurnictwo/realizacje/', MENU_G(p, 'r'), tresc))

# =====================================================================
# 3. światłowody
# =====================================================================
def MENU_S(p):
    return [(f'{p}swiatlowody/#zakres', 'Zakres prac', False), (f'{p}swiatlowody/#trasa', 'Jak powstaje przyłącze', False),
            (f'{p}swiatlowody/#dla-kogo', 'Dla kogo', False), (f'{p}swiatlowody/#pytania', 'Pytania', False), (f'{p}swiatlowody/#kontakt', 'Kontakt', False)]

def swiatlowody():
    p = '../'
    zadzwon = f'<a class="btn btn-acc" href="tel:{TELH}">{TELI}Zadzwoń: {TEL}</a>'
    h = hero(p, 'spawanie-wlokien', 'Spawanie włókien światłowodowych', '62% 50%', ('Światłowody', 'Kołobrzeg i okolice'),
             'Światłowód|od drogi|*do gniazdka.*',
             'Przyłącza do domów, wykopy i przewierty sterowane, spawanie włókien i okablowanie budynków. Ta sama ekipa Exclusive Inside, która wykańcza wnętrza – z tym samym porządkiem na budowie.',
             zadzwon + f'<a class="btn btn-ghost" href="#trasa">Jak powstaje przyłącze {ARR}</a>',
             '<b>Przyłącza</b><span>· wykopy · przewierty · spawanie</span>', 'zachodniopomorskie · lubuskie · wielkopolskie', 'Zdjęcie poglądowe')
    st = strip([('Przyłącza', 'do domów jednorodzinnych'), ('Wykopy', 'pod instalacje'), ('Przewierty', 'sterowane pod nawierzchnią'),
                ('Spawanie', 'włókien i pomiary'), ('Okablowanie', 'budynków i lokali')])
    kafle = ''.join(tile(p, f'#{a}', n, alt, t, s, d=i * 110, sizes='(max-width: 1180px) 50vw, 25vw') for i, (a, n, alt, t, s) in enumerate([
        ('przylacza', 'puszka-abonencka', 'Puszka abonencka (zdjęcie poglądowe)', 'Przyłącza', 'Od skrzynki operatora do domu'),
        ('wykopy', 'wykop-mikrorurki', 'Mikrorurki w wykopie (zdjęcie poglądowe)', 'Wykopy i przewierty', 'Bez rozbierania podjazdu'),
        ('spawanie', 'spawarka-szafa', 'Spawarka przy przełącznicy (zdjęcie poglądowe)', 'Spawanie', 'Włókna, mufy, przełącznice'),
        ('budynki', 'mikrorurki', 'Wiązka mikrorurek (zdjęcie poglądowe)', 'Budynki', 'Piony, poziomy, kanalizacja')]))
    bloki = [
        ('przylacza', 'Przyłącza|*do domów.*',
         'Doprowadzamy kabel od punktu operatora przy drodze do budynku i montujemy zakończenie w domu – w miejscu, które ustalisz, a nie tam, gdzie było najprościej.',
         ['Trasa kabla uzgodniona z właścicielem', 'Przejście przez ścianę fundamentową lub elewację', 'Puszka abonencka i zakończenie włókna w domu'],
         [('puszka-abonencka', 'Puszka abonencka ze spawami', 'Puszka abonencka – zdjęcie poglądowe'), ('zlacze-sc-apc', 'Kabel ze złączem SC/APC', 'Złącze SC/APC – poglądowe')],
         f'<a class="btn btn-ghost" href="#trasa">Zobacz całą trasę {ARR}</a>'),
        ('wykopy', 'Wykopy|*i przewierty sterowane.*',
         'Kabel w ziemi prowadzimy wykopem albo przewiertem sterowanym – pod podjazdem, kostką czy trawnikiem przewiert pozwala przejść bez rozbierania nawierzchni.',
         ['Wykopy pod instalacje', 'Przewierty sterowane pod nawierzchnią', 'Rury osłonowe i mikrorurki', 'Odtworzenie terenu po pracach'],
         [('wykop-mikrorurki', 'Wykop z mikrorurkami', 'Wykop z mikrorurkami – poglądowe'), ('beben-kabla', 'Bębny kabli i rury osłonowe', 'Bębny kabli – poglądowe')],
         f'<a class="btn btn-ghost" href="#kontakt">Zapytaj o przewiert {ARR}</a>'),
        ('spawanie', 'Spawanie|*i montaż osprzętu.*',
         'Łączymy włókna spawarką, układamy spawy w kasetach i montujemy osprzęt: mufy, przełącznice, puszki. Po spawaniu połączenia są sprawdzane pomiarem.',
         ['Spawanie włókien', 'Montaż muf, przełącznic i puszek', 'Pomiary po wykonaniu'],
         [('spawarka-szafa', 'Spawarka i przełącznica w szafie', 'Spawarka i przełącznica – poglądowe'), ('kaseta-spawow', 'Kasety spawów', 'Kasety spawów – poglądowe')],
         f'<a class="btn btn-ghost" href="#dla-kogo">Dla operatorów {ARR}</a>'),
        ('budynki', 'Okablowanie|*w budynkach.*',
         'W budynkach wielorodzinnych i lokalach prowadzimy piony i poziomy do mieszkań. W nowych domach przygotowujemy trasę pod światłowód, zanim powstaną ściany i wykończenie.',
         ['Piony i poziomy w budynkach wielorodzinnych', 'Kanalizacja teletechniczna w nowym budynku', 'Trasy kabli schowane w ścianach przy remoncie'],
         [('mikrorurki', 'Wiązka mikrorurek', 'Mikrorurki – poglądowe')],
         f'<a class="btn btn-ghost" href="{p}glazurnictwo/">Remont z nami {ARR}</a>'),
    ]
    etapy = [
        ('Przy drodze', 'Punkt operatora', 'Sygnał zaczyna się w szafie lub studni operatora. Stąd planujemy trasę do budynku.', 'szafa-uliczna', 'Szafa dystrybucyjna sieci'),
        ('Pod ziemią', 'Wykop albo przewiert', 'Kładziemy rurę osłonową lub mikrorurkę. Gdzie nie da się kopać – przewiert sterowany pod nawierzchnią.', 'wykop-mikrorurki', 'Mikrorurki w wykopie'),
        ('W rurze', 'Kabel do budynku', 'Kabel wprowadzamy do rury i przez przepust do środka budynku – szczelnie, bez zawilgocenia ściany.', 'mikrorurki', 'Wiązka mikrorurek'),
        ('W domu', 'Spawanie i zakończenie', 'Włókna spawamy w puszce abonenckiej, a połączenie sprawdzamy pomiarem.', 'puszka-abonencka', 'Puszka abonencka ze spawami'),
        ('Gotowe', 'Złącze dla operatora', 'Zostaje złącze, do którego operator podłącza swoje urządzenie. Ty wybierasz, w którym pokoju.', 'zlacze-sc-apc', 'Złącze SC/APC'),
    ]
    tf = ''.join(f'<figure{" class=\"ta\"" if i == 0 else ""}>{img(p, n, a + " (zdjęcie poglądowe)", "50vw")}<figcaption>{e(a)} – poglądowe</figcaption></figure>' for i, (_, _, _, n, a) in enumerate(etapy))
    et = ''.join(f'<li{" class=\"ta\"" if i == 0 else ""}><span class="gdzie">{i + 1:02d} · {g}</span><h3>{t}</h3><p>{o}</p>{fig(p, n, a + " (zdjęcie poglądowe)", natural=False)}</li>' for i, (g, t, o, n, a) in enumerate(etapy))
    fq, ld_faq = faq([
        ('Czy do przyłącza trzeba kuć ściany w domu?', 'Zwykle nie. Kabel wchodzi do budynku przez przepust, a w środku prowadzimy go istniejącymi trasami albo w listwie. Jeśli i tak robisz remont, chowamy go w ścianie przed tynkiem lub płytkami.'),
        ('Czy rozkopiecie mi podjazd albo trawnik?', 'Pod nawierzchnią, której nie chcesz ruszać, robimy przewiert sterowany. Tam, gdzie kopiemy, teren jest odtwarzany po pracy.'),
        ('Pracujecie dla operatorów i firm wykonawczych?', 'Tak – możemy wejść jako podwykonawca na wykopy, przewierty, wciąganie kabli, spawanie i pomiary. Zakres ustalamy przy zleceniu.'),
        ('Jaki obszar obsługujecie?', 'Kołobrzeg i okolice oraz województwa zachodniopomorskie, lubuskie i wielkopolskie.'),
        ('Jak wygląda wycena?', 'Zadzwoń albo wyślij zapytanie z adresem budynku. Cena zależy od długości trasy, rodzaju terenu i prac w środku, dlatego wyceniamy po rozmowie lub oględzinach.')])
    tresc = f'''{h}
{st}
<section class="sec" id="zakres">
<div class="wrap">
{secHead('Zakres prac', 'Cała trasa|*albo jeden odcinek.*', 'Dla właścicieli domów, wspólnot i deweloperów – albo jako podwykonawca dla operatora.', f'<a class="btn btn-ghost" href="#kontakt">Zapytaj o wycenę {ARR}</a>')}
<div class="tiles-4">{kafle}</div>
<p class="uwaga rv">Zdjęcia w tym dziale są poglądowe (Wikimedia Commons) – w docelowej wersji zastąpimy je zdjęciami z Państwa realizacji.</p>
</div>
</section>
<section class="pp2">{svc_blocks(p, bloki)}</section>
<section class="sec dk" id="trasa">
<div class="wrap">
{secHead('Jak powstaje przyłącze', 'Pięć odcinków.|*Jedna ekipa.*', 'Przewijaj – zobaczysz, którędy światłowód idzie od skrzynki przy drodze do Twojego salonu.')}
<div class="trasa">
<div class="trasa-foto"><span class="licz">01</span>{tf}</div>
<ol class="etapy">{et}</ol>
</div>
</div>
</section>
<section class="sec" id="dla-kogo">
<div class="wrap">
{secHead('Dla kogo', 'Inny klient.|*Ten sam porządek.*', 'Robimy całą trasę albo tylko odcinek, który jest potrzebny.')}
<div class="trzy">
<div class="rv"><b>Dom jednorodzinny</b><h3>Właściciele domów</h3><p>Operator przyłącza Cię do sieci, ale trasę na działce i w domu trzeba zrobić porządnie. Uzgadniamy ją z Tobą i sprzątamy po sobie.</p></div>
<div class="rv" style="--d:110"><b>Inwestycje</b><h3>Deweloperzy i wspólnoty</h3><p>Kanalizacja teletechniczna w nowych budynkach, piony i poziomy w budynkach wielorodzinnych, przygotowanie lokali pod operatora.</p></div>
<div class="rv" style="--d:220"><b>Podwykonawstwo</b><h3>Operatorzy i wykonawcy</h3><p>Wykopy, przewierty, wciąganie i wdmuchiwanie kabli, spawanie, montaż osprzętu, pomiary.</p></div>
</div>
</div>
</section>
{about(p, 'Exclusive Inside.|*Dwa działy, jedna firma.*', 'Na co dzień wykańczamy wnętrza – łazienki, schody, blaty z płyt wielkoformatowych. Instalacje światłowodowe robimy z tą samą dokładnością: trasa uzgodniona z właścicielem, porządek po pracy.', f'<a class="btn btn-ink" href="{p}glazurnictwo/">Zobacz glazurnictwo {ARR}</a>')}
{stop(p, 'g', 'lazienka-drewno-geometria', 'Łazienka wykonana przez Exclusive Inside', 'Drugi dział firmy', 'Światłowód przy remoncie.|*Potem płytki.*', 'Robisz łazienkę albo wykończenie domu? Najpierw poprowadzimy trasę kabla w ścianach, potem położymy płytki – bez listew i bez kucia po fakcie.', p + 'glazurnictwo/', 'Glazurnictwo i wykończenia')}
<section class="sec" id="pytania">
<div class="wrap faq-wrap">
<div class="faq-side">{eyebrow('Pytania')}{H('Zanim|*zadzwonisz.*')}<p class="lead rv" style="margin-top:24px">To, o co klienci pytają najczęściej przed przyłączem.</p><div class="rv">{zadzwon}</div></div>
<div>{fq}</div>
</div>
</section>
{kontakt(p, 's')}'''
    zapisz('swiatlowody', strona(p, 's', 'Instalacje światłowodowe Kołobrzeg – przyłącza, przewierty, spawanie | Exclusive Inside',
                                 'Instalacje światłowodowe w Kołobrzegu i okolicy: przyłącza do domów, wykopy i przewierty sterowane, spawanie włókien, okablowanie budynków. Tel. 506 931 962.',
                                 'swiatlowody/', MENU_S(p), tresc, ld=ld_faq))

def zrodla():
    p = '../'
    rows = ''.join(f'<li><span>{e(k)}</span><small><a href="{v["page"]}" target="_blank" rel="noopener">{e(v["title"][5:])}</a> · {e(re.sub("<[^>]+>", "", v["artist"]).strip())} · {e(v["lic"])}</small></li>' for k, v in ZRODLA.items())
    tresc = f'''<section class="pagehead" style="min-height:52vh">
<div class="hero-media">{img(p, 'mikrorurki', 'Mikrorurki (zdjęcie poglądowe)', '100vw', lazy=False)}</div>
<div class="ph-in">{H('Źródła zdjęć|*poglądowych.*', 'h1', 'h1', rv=False)}<p class="ph-lead up" style="--d:300">Zdjęcia w dziale „Światłowody” pochodzą z Wikimedia Commons. Zdjęcia w dziale „Glazurnictwo” to realizacje firmy.</p></div>
</section>
<section class="sec"><div class="wrap"><ul class="zrodla">{rows}</ul></div></section>'''
    zapisz('zrodla-zdjec', strona(p, 's', 'Źródła zdjęć | Exclusive Inside', 'Licencje zdjęć poglądowych.', 'zrodla-zdjec/', MENU_S(p), tresc, mapa=False))

def extras():
    open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 60 60"><rect x="-6" y="-10" width="60" height="60" rx="10" fill="#0E0D0C"/>'
        '<rect x="0" y="0" width="9" height="40" fill="#fff"/><rect x="11" y="0" width="22" height="11" fill="#C9A46A"/>'
        '<rect x="11" y="14.5" width="16" height="11" fill="#fff"/><rect x="11" y="29" width="22" height="11" fill="#FFC928"/>'
        '<rect x="37" y="0" width="11" height="40" fill="#fff"/></svg>')
    urls = ['', 'glazurnictwo/', 'glazurnictwo/realizacje/', 'swiatlowody/']
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'<url><loc>{BASE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')

wybor(); glazurnictwo(); realizacje(); swiatlowody(); zrodla(); extras()
print('zbudowane')
