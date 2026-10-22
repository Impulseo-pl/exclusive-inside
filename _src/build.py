# -*- coding: utf-8 -*-
"""Generator dema Exclusive Inside. Uruchom: python _src/build.py (z dowolnego katalogu)."""
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
e = html.escape

# ---------- obrazy ----------
def variants(name):
    out = []
    for f in os.listdir(IMG):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.webp', f)
        if m:
            w, h = Image.open(os.path.join(IMG, f)).size
            out.append((int(m.group(1)), f, w, h))
    if not out:
        raise SystemExit('brak obrazu ' + name)
    return sorted(out)

def pic(p, name, alt, sizes='(max-width: 900px) 100vw, 50vw', lazy=True, cls=''):
    v = variants(name)
    big = v[-1]
    srcset = ', '.join(f'{p}img/{f} {w}w' for _, f, w, h in v)
    a = (f'<img src="{p}img/{big[1]}" srcset="{srcset}" sizes="{sizes}" '
         f'width="{big[2]}" height="{big[3]}" alt="{e(alt)}"')
    a += ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    if cls: a += f' class="{cls}"'
    return a + '>'

def full(p, name):
    return p + 'img/' + variants(name)[-1][1]

def fig(p, name, alt, cap=None, sizes='(max-width: 900px) 100vw, 30vw'):
    c = f'<figcaption>{e(cap)}</figcaption>' if cap else ''
    return f'<figure>{pic(p, name, alt, sizes)}{c}</figure>'

# ---------- wspólne elementy ----------
LOGO = ('<svg viewBox="0 0 48 40" aria-hidden="true">'
        '<rect x="0" y="0" width="9" height="40" fill="currentColor"/>'
        '<rect class="a" x="11" y="0" width="22" height="11"/>'
        '<rect x="11" y="14.5" width="16" height="11" fill="currentColor"/>'
        '<rect class="a" x="11" y="29" width="22" height="11"/>'
        '<rect x="37" y="0" width="11" height="40" fill="currentColor"/></svg>')
LOADER = ('<div class="ladowanie" aria-hidden="true"><svg viewBox="0 0 48 40">'
          '<rect x="0" y="0" width="9" height="40" fill="#fff"/>'
          '<rect x="11" y="0" width="22" height="11" fill="#b8935a"/>'
          '<rect x="11" y="14.5" width="16" height="11" fill="#fff"/>'
          '<rect x="11" y="29" width="22" height="11" fill="#ffc928"/>'
          '<rect x="37" y="0" width="11" height="40" fill="#fff"/></svg>'
          '<div class="nazwa">EXCLUSIVE INSIDE</div></div>')
TEL_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true">'
           '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>')
LICZNIK = open(os.path.join(ROOT, '_src', 'licznik.js'), encoding='utf-8').read()

def head(p, title, desc, path, extra_ld=None):
    ld = {
        '@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness',
        'name': 'Exclusive Inside', 'founder': 'Roman Viitovych', 'telephone': TELH, 'email': MAIL,
        'url': BASE, 'image': BASE + 'img/' + variants('lazienka-drewno-geometria')[-1][1],
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Błękitna 23', 'postalCode': '78-100',
                    'addressLocality': 'Kołobrzeg', 'addressCountry': 'PL'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 54.1629, 'longitude': 15.5379},
        'areaServed': ['województwo zachodniopomorskie', 'województwo lubuskie', 'województwo wielkopolskie'],
        'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '5.0', 'reviewCount': '3'},
        'sameAs': [FB, OFERTEO], 'vatID': 'PL6751463258',
    }
    lds = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    if extra_ld:
        lds += f'<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>'
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
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<script>(function(d){{d.className+=' js';try{{if(!sessionStorage.getItem('ei_l'))d.className+=' pierwszy';var z=sessionStorage.getItem('ei_z');if(z)d.style.setProperty('--zaslona',z)}}catch(e){{}}}})(document.documentElement)</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="{p}assets/styles.css">
{lds}
<script>{LICZNIK}</script>
'''

def scripts(p, mapa=False):
    s = '<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js" defer></script>\n'
    if mapa:
        s = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">\n'
             '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" defer></script>\n') + s
    return s + f'<script src="{p}assets/app.js" defer></script>\n'

def topbar(p, galaz, menu):
    g_ta = ' class="ta"' if galaz == 'g' else ''
    s_ta = ' class="ta"' if galaz == 's' else ''
    links = ''.join(f'<a href="{h}"{" class=\"ta\"" if a else ""}>{t}</a>' for h, t, a in menu)
    return f'''<header class="top">
<div class="wrap">
<a class="logo" href="{p}" aria-label="Exclusive Inside – strona główna">{LOGO}<span>Exclusive Inside<small>{"Glazurnictwo i wykończenia" if galaz == "g" else "Instalacje światłowodowe"}</small></span></a>
<nav class="galezie" aria-label="Działy firmy"><a href="{p}glazurnictwo/"{g_ta}>Glazurnictwo</a><a href="{p}swiatlowody/"{s_ta}>Światłowody</a></nav>
<nav class="menu" aria-label="Menu">{links}<a class="tel-m" href="tel:{TELH}">Zadzwoń: {TEL}</a></nav>
<a class="tel" href="tel:{TELH}">{TEL_SVG}{TEL}</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div>
</header>'''

def kontakt(p, galaz):
    if galaz == 'g':
        tematy = ['Łazienka', 'Schody', 'Blat lub wyspa', 'Wykończenie mieszkania lub domu', 'Inne']
        opis_ph = 'Np. łazienka ok. 6 m², płyty 120×60, mam już płytki / szukam projektu…'
        lead = 'Opisz, co chcesz zrobić – oddzwonimy, umówimy oględziny i przygotujemy wycenę.'
    else:
        tematy = ['Przyłącze do domu', 'Budynek wielorodzinny', 'Wykop lub przewiert', 'Spawanie i pomiary', 'Podwykonawstwo dla operatora', 'Inne']
        opis_ph = 'Np. dom jednorodzinny, operator już wybrany, trzeba doprowadzić kabel od skrzynki przy drodze…'
        lead = 'Napisz, gdzie jest budynek i na jakim etapie jest przyłącze – oddzwonimy z odpowiedzią.'
    opts = ''.join(f'<option>{t}</option>' for t in tematy)
    return f'''<section class="sek" id="kontakt">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Kontakt</h2></div><p>{lead}</p></div>
<div class="kontakt">
<div class="dane">
Najszybciej telefonicznie:
<a class="duzy-tel" href="tel:{TELH}">{TEL}</a>
<dl>
<dt>Firma</dt><dd>Exclusive Inside<br>Roman Viitovych</dd>
<dt>Adres</dt><dd>ul. Błękitna 23<br>78-100 Kołobrzeg</dd>
<dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd>
<dt>Obszar</dt><dd>zachodniopomorskie, lubuskie, wielkopolskie</dd>
<dt>NIP</dt><dd>675-146-32-58</dd>
</dl>
<div class="mapa" id="mapa" role="img" aria-label="Mapa: ul. Błękitna 23, Kołobrzeg"></div>
</div>
<form class="formularz" data-mail="{MAIL}">
<h3>Zapytanie o wycenę</h3>
<div class="dwa"><div><label for="f-imie">Imię</label><input id="f-imie" name="imie" autocomplete="given-name" required></div>
<div><label for="f-tel">Telefon</label><input id="f-tel" name="tel" type="tel" autocomplete="tel" required></div></div>
<div class="dwa"><div><label for="f-temat">Czego dotyczy</label><select id="f-temat" name="temat">{opts}</select></div>
<div><label for="f-m">Miejscowość</label><input id="f-m" name="miejsce"></div></div>
<label for="f-opis">Opis</label><textarea id="f-opis" name="opis" placeholder="{e(opis_ph)}"></textarea>
<button class="btn btn-acc" type="submit">Wyślij zapytanie</button>
<p class="info">Odpowiadamy telefonicznie lub mailowo. Dane służą tylko do odpowiedzi na zapytanie.</p>
</form>
</div>
</div>
</section>'''

def stopka(p, galaz):
    return f'''<footer class="stopka">
<div class="wrap">
<div class="stopka-gora">
<div><a class="logo" href="{p}">{LOGO}<span>Exclusive Inside<small>Roman Viitovych</small></span></a>
<p>Wykończenia wnętrz, płytki wielkoformatowe i instalacje światłowodowe. Kołobrzeg i okolice, zachodniopomorskie, lubuskie, wielkopolskie.</p></div>
<div><h4>Glazurnictwo</h4><ul><li><a href="{p}glazurnictwo/#specjalizacje">Specjalizacje</a></li><li><a href="{p}glazurnictwo/realizacje/">Realizacje</a></li><li><a href="{p}glazurnictwo/#opinie">Opinie</a></li></ul></div>
<div><h4>Światłowody</h4><ul><li><a href="{p}swiatlowody/#zakres">Zakres prac</a></li><li><a href="{p}swiatlowody/#trasa">Jak powstaje przyłącze</a></li><li><a href="{p}swiatlowody/#faq">Pytania</a></li></ul></div>
<div><h4>Kontakt</h4><ul><li><a href="tel:{TELH}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li><li><a href="{OFERTEO}" target="_blank" rel="noopener">Opinie na Oferteo</a></li></ul></div>
</div>
<div class="stopka-dol"><span>© 2026 Exclusive Inside · ul. Błękitna 23, 78-100 Kołobrzeg · NIP 675-146-32-58</span><a href="{p}zrodla-zdjec/">Źródła zdjęć poglądowych</a></div>
</div>
</footer>'''

def strona(p, galaz, title, desc, path, menu, tresc, mapa=True, ld=None):
    cls = 'glaz' if galaz == 'g' else 'swiatlo'
    return (head(p, title, desc, path, ld) + '</head>\n'
            f'<body class="{cls}">\n<a class="skip" href="#tresc">Przejdź do treści</a>\n'
            f'{LOADER}<div class="zaslona start"></div>\n'
            + topbar(p, galaz, menu) + f'\n<main id="tresc">\n{tresc}\n</main>\n' + stopka(p, galaz)
            + '\n' + scripts(p, mapa) + '</body>\n</html>\n')

def zapisz(path, s):
    full_p = os.path.join(ROOT, path, 'index.html') if path else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(full_p), exist_ok=True)
    open(full_p, 'w', encoding='utf-8').write(s)

# ---------- realizacje ----------
KAT = [('lazienki', 'Łazienki'), ('schody', 'Schody'), ('blaty', 'Blaty i zabudowy'), ('sciany', 'Ściany i dekory'), ('budowa', 'W trakcie prac')]
FOTY = [
    ('lazienki', 'lazienka-drewno-geometria', 'Łazienka z ryflowaną ścianą w drewnie, wanna wolnostojąca, czarna armatura'),
    ('lazienki', 'lazienka-czarny-marmur-zloto', 'Czarny marmur ze złotym żyłkowaniem w strefie WC'),
    ('lazienki', 'prysznic-meander', 'Prysznic walk-in – czarno-biały wzór od podłogi po ścianę'),
    ('lazienki', 'lazienka-led-umywalka', 'Blat z umywalką i zabudowa pralki, podświetlenie LED'),
    ('lazienki', 'lazienka-czarny-marmur', 'Łazienka w czarnym i białym marmurze, kabina bez brodzika'),
    ('lazienki', 'lazienka-zielona-oktagon', 'Butelkowa zieleń na ścianach, podłoga z oktagonów'),
    ('lazienki', 'lazienka-szara-prysznic', 'Szara płyta wielkoformatowa i drewno na podłodze'),
    ('lazienki', 'zabudowa-wc-marmur', 'Zabudowa stelaża WC z płyty wielkoformatowej w marmurze'),
    ('lazienki', 'lazienka-led-prysznic', 'Prysznic z wnęką i linią światła'),
    ('lazienki', 'lazienka-szara-umywalka', 'Umywalka nablatowa, ściany z szarej płyty'),
    ('lazienki', 'lazienka-czarny-marmur-2', 'Strefa prania i prysznic – czarny marmur'),
    ('lazienki', 'lazienka-szara-kabina', 'Kabina z wnęką w płycie'),
    ('lazienki', 'prysznic-meander-2', 'Wnęka i dekor w strefie prysznica'),
    ('lazienki', 'lazienka-led-zabudowa', 'Zabudowa z płyty w połysku, podświetlenie sufitu'),
    ('lazienki', 'lazienka-szara-wc', 'Stelaż WC obłożony płytą, przycisk na tle płyty'),
    ('lazienki', 'lazienka-zielona-oktagon-2', 'Oktagony z czarną kostką – widok z góry'),
    ('schody', 'schody-spiek-prety', 'Schody okładane płytą, balustrada z czarnych prętów'),
    ('schody', 'schody-zewnetrzne-szklo', 'Schody zewnętrzne z płyty w drewnie, balustrada szklana'),
    ('schody', 'schody-czarne-prety', 'Biegi schodów obłożone płytą, czarne pręty'),
    ('schody', 'schody-spiek-prety-2', 'Schody w jasnej płycie – widok z dołu'),
    ('schody', 'schody-zewnetrzne-klinkier', 'Schody wejściowe z płytek klinkierowych'),
    ('schody', 'schody-spiek-prety-3', 'Schody i ściana w płycie drewnopodobnej'),
    ('blaty', 'wyspa-spiek-marmur', 'Wyspa obłożona płytą wielkoformatową w marmurze'),
    ('sciany', 'heksagony-3d', 'Heksagony 3D w bieli i kobalcie'),
    ('sciany', 'korytarz-cegla', 'Korytarz z cegłą rozbiórkową i liniami światła'),
    ('sciany', 'sciana-ramy-dekor', 'Ściana z ramami i wypełnieniem dekoracyjnym'),
    ('sciany', 'fototapeta-las', 'Fototapeta z mglistym lasem'),
    ('sciany', 'bateria-podtynkowa-beton', 'Bateria podtynkowa na płycie imitującej beton'),
    ('budowa', 'plyty-wielkoformatowe-podloga', 'Płyty wielkoformatowe na podłodze – układanie'),
    ('budowa', 'schody-krecone-budowa', 'Schody kręcone w trakcie okładania'),
    ('budowa', 'wanna-narozna-odplyw', 'Wanna narożna i odpływ liniowy w trakcie prac'),
]

def mur(p, foty):
    out = []
    for k, n, alt in foty:
        out.append(f'<a class="fot" href="{full(p, n)}" data-k="{k}" data-opis="{e(alt)}">'
                   f'{pic(p, n, alt, "(max-width: 560px) 50vw, (max-width: 900px) 50vw, 33vw")}<span>{e(alt)}</span></a>')
    return '<div class="mur">' + ''.join(out) + '</div>'

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
             'Exclusive Inside, Roman Viitovych: łazienki i schody z płyt wielkoformatowych oraz instalacje światłowodowe. Kołobrzeg, zachodniopomorskie, lubuskie, wielkopolskie. Tel. 506 931 962.', '')
    s += '</head>\n<body class="glaz wybor">\n' + LOADER + '<div class="zaslona start"></div>\n'
    s += f'''<header class="wybor-top">
<div class="wrap">
<a class="logo" href="./" aria-label="Exclusive Inside">{LOGO}<span>Exclusive Inside<small>Roman Viitovych · Kołobrzeg</small></span></a>
<nav class="galezie" aria-label="Wybierz dział"><a class="g" href="glazurnictwo/">Glazurnictwo</a><a class="s" href="swiatlowody/">Światłowody</a></nav>
<a class="tel" href="tel:{TELH}">{TEL_SVG}<span>{TEL}</span></a>
</div>
</header>
<main class="dzial">
<h1 class="skip">Exclusive Inside – glazurnictwo i instalacje światłowodowe</h1>
<a class="pol g" href="glazurnictwo/">
<div class="fot">{pic(p, 'lazienka-drewno-geometria', 'Łazienka wykonana przez Exclusive Inside', '(max-width: 900px) 100vw, 60vw', lazy=False)}</div>
<span class="linia"></span>
<div class="in">
<span class="rodzaj">Płytki wielkoformatowe · wykończenia wnętrz</span>
<h2>Glazurnictwo</h2>
<p>Łazienki, schody, wyspy i blaty z dużych płyt. Projekt z wykonaniem – od wyrównania ścian po biały montaż.</p>
<span class="wejdz">Wejdź <i></i></span>
</div>
</a>
<a class="pol s" href="swiatlowody/">
<div class="fot">{pic(p, 'spawanie-wlokien', 'Spawanie włókien światłowodowych (zdjęcie poglądowe)', '(max-width: 900px) 100vw, 60vw', lazy=False)}</div>
<span class="linia"></span>
<div class="in">
<span class="rodzaj">Instalacje światłowodowe</span>
<h2>Światłowody</h2>
<p>Przyłącza do domów, wykopy i przewierty sterowane, spawanie włókien. Od skrzynki przy drodze do gniazdka w domu.</p>
<span class="wejdz">Wejdź <i></i></span>
</div>
</a>
</main>
''' + scripts(p) + '</body>\n</html>\n'
    zapisz('', s)

# =====================================================================
# 2. glazurnictwo
# =====================================================================
MENU_G = lambda p, ta='': [(f'{p}glazurnictwo/#specjalizacje', 'Specjalizacje', False),
                           (f'{p}glazurnictwo/realizacje/', 'Realizacje', ta == 'r'),
                           (f'{p}glazurnictwo/#jak-pracujemy', 'Jak pracujemy', False),
                           (f'{p}glazurnictwo/#opinie', 'Opinie', False),
                           (f'{p}glazurnictwo/#kontakt', 'Kontakt', False)]

def glazurnictwo():
    p = '../'
    rzedy = [
        ('Łazienki w dużych formatach',
         'Płyty 120×60, 120×120 i większe na ścianach i podłodze, mało fug, równe linie od progu po sufit. Ściany pod płyty wielkoformatowe wyrównujemy wcześniej, bo przy takim formacie widać każdy milimetr.',
         ['Kabiny bez brodzika z odpływem liniowym', 'Zabudowy stelaży WC i wnęki z płyty', 'Podświetlenie LED w niszach i suficie', 'Biały montaż: armatura podtynkowa, ceramika, kabiny'],
         [('lazienka-czarny-marmur', 'Łazienka w czarnym marmurze, kabina bez brodzika'), ('zabudowa-wc-marmur', 'Zabudowa stelaża WC z płyty w marmurze')]),
        ('Schody okładane płytą',
         'Schody wewnętrzne i zewnętrzne: stopnice i podstopnie z płyty, docinane tak, żeby rysunek płyty szedł przez cały bieg. Robimy też schody kręcone i schody wejściowe z klinkieru.',
         ['Schody wewnętrzne z płyty drewnopodobnej i kamiennej', 'Schody zewnętrzne z klinkieru', 'Schody kręcone – docinki na łuku'],
         [('schody-spiek-prety', 'Schody okładane płytą z balustradą z prętów'), ('schody-zewnetrzne-szklo', 'Schody zewnętrzne z balustradą szklaną')]),
        ('Wyspy i blaty z płyt wielkoformatowych',
         'Wyspa kuchenna, blat łazienkowy albo zabudowa pralki obłożona tą samą płytą co ściany. Narożniki łączone na kąt, żeby żyłkowanie przechodziło z blatu na bok.',
         ['Wyspy kuchenne', 'Blaty pod umywalki nablatowe', 'Zabudowy pralek i szafek'],
         [('wyspa-spiek-marmur', 'Wyspa obłożona płytą w marmurze')]),
        ('Wzory, dekory, mozaiki',
         'Oktagony z kostką, meandry, heksagony 3D – układy, przy których liczy się rozplanowanie przed pierwszym cięciem. Każdy wzór najpierw rozkładamy na sucho i uzgadniamy z inwestorem.',
         ['Oktagony i mozaiki podłogowe', 'Dekory ścienne i heksagony 3D', 'Fototapety, cegła, sztukateria'],
         [('prysznic-meander', 'Prysznic z czarno-białym meandrem'), ('lazienka-zielona-oktagon', 'Zielona łazienka z podłogą z oktagonów')]),
    ]
    rz = ''
    for i, (t, opis, lista, fotki) in enumerate(rzedy):
        figs = ''.join(fig(p, n, a) for n, a in fotki)
        li = ''.join(f'<li>{e(x)}</li>' for x in lista)
        rz += (f'<div class="rzad{" odwr" if i % 2 else ""}"><div class="rzad-foto{" jedno" if len(fotki) == 1 else ""}">{figs}</div>'
               f'<div class="rzad-txt"><h3>{t}</h3><p>{opis}</p><ul>{li}</ul></div></div>')

    kroki = [
        ('Na początku', 'Oględziny i pomiar', 'Przyjeżdżamy, mierzymy, sprawdzamy ściany i podłogę. Rozmawiamy o płytkach, układzie i armaturze.'),
        ('Jeśli trzeba', 'Projekt łazienki', 'Gdy nie masz jeszcze projektu, przygotowujemy go razem z doborem płytek – potem wykonujemy dokładnie to, co jest na rysunku.'),
        ('Przed płytkami', 'Podłoże i hydroizolacja', 'Wyrównanie ścian pod duży format, zabudowy z płyt, hydroizolacja w strefach mokrych, przygotowanie pod odpływ liniowy.'),
        ('Układanie', 'Cięcia zaplanowane z góry', 'Rozkład płytek ustalamy z inwestorem przed pierwszym cięciem. Nie podejmujemy decyzji za klienta i nie marnujemy płytek.'),
        ('Na koniec', 'Biały montaż i sprzątanie', 'Montujemy ceramikę, armaturę i kabinę, a po pracy zostawiamy porządek.'),
    ]
    kr = ''.join(f'<li><span class="kiedy">{a}</span><div><h3>{b}</h3><p>{c}</p></div></li>' for a, b, c in kroki)

    op = ''.join(f'<figure class="opinia"><blockquote>{e(t)}</blockquote><figcaption><span class="gw">★★★★★</span>{a} · opinia na Oferteo</figcaption></figure>' for a, t in OPINIE)

    dodatkowe = [('Remonty i wykończenia pod klucz', 'mieszkania i domy'), ('Gładzie i malowanie', 'ściany i sufity'),
                 ('Zabudowy z płyt G-K', 'ścianki, sufity, zabudowy'), ('Tapetowanie i fototapety', ''),
                 ('Drobne prace hydrauliczne', ''), ('Wyburzenia wewnątrz budynków', 'przed remontem'),
                 ('Montaż instalacji elektrycznych', ''), ('Cegła rozbiórkowa i dekory ścienne', '')]
    dd = ''.join(f'<li>{a}<small>{b}</small></li>' for a, b in dodatkowe)

    mini = [f for f in FOTY if f[1] in ('lazienka-czarny-marmur-zloto', 'heksagony-3d', 'lazienka-led-umywalka', 'schody-czarne-prety', 'korytarz-cegla', 'lazienka-szara-prysznic')]

    tresc = f'''<section class="hero">
<div class="wrap">
<div class="hero-txt">
<h1 class="anim">Łazienki, schody i blaty z płyt wielkoformatowych</h1>
<p class="lead anim">Exclusive Inside – Roman Viitovych. Robimy projekt z wykonaniem albo układamy według Twojego projektu: od wyrównania ścian po biały montaż.</p>
<div class="ctas anim"><a class="btn btn-acc" href="tel:{TELH}">{TEL_SVG} Zadzwoń: {TEL}</a><a class="btn btn-line" href="realizacje/">Zobacz realizacje</a></div>
<div class="gdzie anim"><span><b>Kołobrzeg</b> i okolice</span><span>zachodniopomorskie · lubuskie · wielkopolskie</span></div>
</div>
<div class="hero-foto">{pic(p, 'lazienka-drewno-geometria', 'Łazienka z ryflowaną ścianą w drewnie i wanną wolnostojącą', '(max-width: 900px) 100vw, 46vw', lazy=False)}<span class="podpis">Realizacja: łazienka z wanną wolnostojącą</span></div>
</div>
</section>
<div class="pasek"><div class="wrap"><span><b>5,0</b> <span class="gw">★★★★★</span></span><span>3 opinie na <a href="{OFERTEO}" target="_blank" rel="noopener">Oferteo</a> – wszystkie na 5 gwiazdek</span><span>Specjalizacja: płytki wielkoformatowe</span><span>Projekt z wykonaniem</span></div></div>

<section class="sek" id="specjalizacje">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>W czym jesteśmy najlepsi</h2></div><p>Wykańczamy całe wnętrza, ale najwięcej pracy i najwięcej poleceń mamy z łazienek, schodów i blatów z dużych płyt.</p></div>
{rz}
</div>
</section>

<section class="sek ciemna">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Projekt i wykonanie tej samej łazienki</h2></div><p>Po lewej wydruk projektu, który dostał inwestor. Po prawej ta sama łazienka po naszej pracy.</p></div>
<div class="para">
<figure><span class="etyk">Projekt</span>{pic(p, 'projekt-wizualizacja', 'Wydruk projektu łazienki z ryflowaną ścianą', '(max-width: 900px) 100vw, 45vw')}</figure>
<figure><span class="etyk">Wykonanie</span>{pic(p, 'lazienka-drewno-geometria', 'Gotowa łazienka zgodna z projektem', '(max-width: 900px) 100vw, 45vw')}</figure>
</div>
<div class="para-opis"><p>Ściana z ryflowanej płyty drewnopodobnej, wnęka z podświetleniem, szara płyta na pozostałych ścianach, czarna armatura i wanna wolnostojąca.</p><p>Jeśli masz projekt od architekta – wykonamy go. Jeśli nie masz – zaprojektujemy łazienkę razem z doborem płytek.</p></div>
</div>
</section>

<section class="sek">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Realizacje</h2></div><p>Zdjęcia z naszych budów – bez retuszu i bez wizualizacji.</p></div>
{mur(p, mini)}
<div class="wiecej"><span>W galerii {len(FOTY)} zdjęć: łazienki, schody, blaty, ściany.</span><a class="btn btn-ink" href="realizacje/">Cała galeria realizacji</a></div>
</div>
</section>

<section class="sek soft" id="jak-pracujemy">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Jak pracujemy</h2></div><p>Każdą decyzję o rozkładzie płytek podejmujemy razem z inwestorem.</p></div>
<div class="proces">
<div class="proces-foto">{fig(p, 'plyty-wielkoformatowe-podloga', 'Układanie płyt wielkoformatowych na podłodze', 'Płyty wielkoformatowe w trakcie układania')}{fig(p, 'schody-krecone-budowa', 'Schody kręcone w trakcie okładania')}{fig(p, 'wanna-narozna-odplyw', 'Odpływ liniowy przy wannie narożnej')}</div>
<ol class="kroki">{kr}</ol>
</div>
</div>
</section>

<section class="sek" id="opinie">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Co piszą klienci</h2></div><p>Opinie przepisane z profilu firmy na Oferteo.</p></div>
<div class="opinie">
<div>{op}</div>
<aside class="ocena"><div class="duza">5,0</div><p>Średnia z 3 opinii na Oferteo.<br>Zdjęcia dodane przez klientów do opinii:</p>
<div class="fotki">{pic(p, 'schody-spiek-prety-2', 'Schody – zdjęcie klienta z opinii', '120px')}{pic(p, 'lazienka-szara-umywalka', 'Łazienka – zdjęcie klienta z opinii', '120px')}{pic(p, 'lazienka-czarny-marmur-zloto', 'Łazienka – zdjęcie klienta z opinii', '120px')}</div>
<p><a href="{OFERTEO}" target="_blank" rel="noopener">Profil na Oferteo</a></p></aside>
</div>
</div>
</section>

<section class="sek soft">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Robimy też</h2></div><p>Przy remoncie łazienki często wychodzi coś więcej – nie musisz szukać drugiej ekipy.</p></div>
<ul class="lista2">{dd}</ul>
</div>
</section>

<section class="most do-s">
<div class="m-foto">{pic(p, 'mikrorurki', 'Mikrorurki pod kable światłowodowe (zdjęcie poglądowe)', '(max-width: 900px) 100vw, 50vw')}</div>
<div class="m-txt"><h2>Remont i światłowód jedną ekipą</h2><p>Zanim położymy płytki, możemy doprowadzić światłowód do domu i przygotować trasę kabla w ścianach – bez kucia drugi raz.</p><a class="btn" href="{p}swiatlowody/">Instalacje światłowodowe</a></div>
</section>

{kontakt(p, 'g')}'''
    zapisz('glazurnictwo', strona(p, 'g', 'Glazurnik Kołobrzeg – łazienki i schody z płyt wielkoformatowych | Exclusive Inside',
                                   'Glazurnik z Kołobrzegu: łazienki z płyt wielkoformatowych, schody, wyspy i blaty, projekt z wykonaniem, biały montaż. Opinie 5,0 na Oferteo. Tel. 506 931 962.',
                                   'glazurnictwo/', MENU_G(p), tresc))

def realizacje():
    p = '../../'
    licz = {k: sum(1 for f in FOTY if f[0] == k) for k, _ in KAT}
    fb = f'<button class="ta" data-k="wszystkie">Wszystkie<sup>{len(FOTY)}</sup></button>' + ''.join(
        f'<button data-k="{k}">{t}<sup>{licz[k]}</sup></button>' for k, t in KAT)
    tresc = f'''<section class="podhero">
<div class="wrap">
<div class="okruchy"><a href="../">Glazurnictwo</a> / Realizacje</div>
<h1>Realizacje</h1>
<p>Łazienki, schody, blaty i ściany wykonane przez Exclusive Inside. Część zdjęć dodali sami klienci do swoich opinii.</p>
</div>
</section>
<section class="sek" style="padding-top:60px">
<div class="wrap">
<div class="filtry" role="toolbar" aria-label="Filtruj realizacje">{fb}</div>
{mur(p, FOTY)}
</div>
</section>
{kontakt(p, 'g')}'''
    zapisz('glazurnictwo/realizacje', strona(p, 'g', 'Realizacje – łazienki, schody, blaty | Exclusive Inside Kołobrzeg',
                                            'Galeria realizacji Exclusive Inside: łazienki z płyt wielkoformatowych, schody okładane płytą, wyspy i blaty, dekory ścienne.',
                                            'glazurnictwo/realizacje/', MENU_G(p, 'r'), tresc))

# =====================================================================
# 3. światłowody
# =====================================================================
MENU_S = lambda p: [(f'{p}swiatlowody/#zakres', 'Zakres prac', False), (f'{p}swiatlowody/#trasa', 'Jak powstaje przyłącze', False),
                    (f'{p}swiatlowody/#dla-kogo', 'Dla kogo', False), (f'{p}swiatlowody/#faq', 'Pytania', False),
                    (f'{p}swiatlowody/#kontakt', 'Kontakt', False)]

def swiatlowody():
    p = '../'
    rzedy = [
        ('Przyłącza światłowodowe do domów',
         'Doprowadzamy kabel od punktu operatora przy drodze do budynku i montujemy zakończenie w domu – w miejscu, które ustalisz, a nie tam, gdzie było najprościej.',
         ['Trasa kabla uzgodniona z właścicielem', 'Przejście przez ścianę fundamentową lub elewację', 'Puszka abonencka i zakończenie włókna w domu'],
         [('puszka-abonencka', 'Puszka abonencka ze spawami (zdjęcie poglądowe)'), ('zlacze-sc-apc', 'Kabel ze złączem SC/APC (zdjęcie poglądowe)')]),
        ('Wykopy pod instalacje i przewierty sterowane',
         'Kabel w ziemi prowadzimy wykopem albo przewiertem sterowanym – pod podjazdem, kostką czy trawnikiem przewiert pozwala przejść bez rozbierania nawierzchni.',
         ['Wykopy pod instalacje', 'Przewierty sterowane pod nawierzchnią', 'Ułożenie rur osłonowych i mikrorurek', 'Odtworzenie terenu po pracach'],
         [('wykop-mikrorurki', 'Wykop z mikrorurkami (zdjęcie poglądowe)'), ('beben-kabla', 'Bębny kabli i rury osłonowe na budowie (zdjęcie poglądowe)')]),
        ('Spawanie włókien i montaż osprzętu',
         'Łączymy włókna spawarką, układamy spawy w kasetach i montujemy osprzęt: mufy, przełącznice, puszki. Po spawaniu połączenia są sprawdzane pomiarem.',
         ['Spawanie włókien', 'Montaż muf, przełącznic i puszek', 'Pomiary po wykonaniu'],
         [('spawarka-szafa', 'Spawarka i przełącznica w szafie (zdjęcie poglądowe)'), ('kaseta-spawow', 'Kasety spawów (zdjęcie poglądowe)')]),
        ('Okablowanie w budynkach',
         'W budynkach wielorodzinnych i lokalach prowadzimy piony i poziomy do mieszkań. W nowych domach – przygotowujemy trasę pod światłowód, zanim powstaną ściany i wykończenie.',
         ['Piony i poziomy w budynkach wielorodzinnych', 'Kanalizacja teletechniczna w nowym budynku', 'Trasy kabli schowane w ścianach przy remoncie'],
         [('mikrorurki', 'Wiązka mikrorurek (zdjęcie poglądowe)')]),
    ]
    rz = ''
    for i, (t, opis, lista, fotki) in enumerate(rzedy):
        figs = ''.join(fig(p, n, a) for n, a in fotki)
        li = ''.join(f'<li>{e(x)}</li>' for x in lista)
        rz += (f'<div class="rzad{" odwr" if i % 2 else ""}"><div class="rzad-foto{" jedno" if len(fotki) == 1 else ""}">{figs}</div>'
               f'<div class="rzad-txt"><h3>{t}</h3><p>{opis}</p><ul>{li}</ul></div></div>')

    etapy = [
        ('Przy drodze', 'Punkt operatora', 'Sygnał zaczyna się w szafie lub studni operatora. Stąd planujemy trasę do budynku.', 'szafa-uliczna', 'Szafa dystrybucyjna sieci światłowodowej'),
        ('Pod ziemią', 'Wykop albo przewiert', 'Kładziemy rurę osłonową lub mikrorurkę. Gdzie nie da się kopać – przewiert sterowany pod nawierzchnią.', 'wykop-mikrorurki', 'Mikrorurki w wykopie'),
        ('W rurze', 'Kabel do budynku', 'Kabel wprowadzamy do rury i przez przepust do środka budynku – szczelnie, bez zawilgocenia ściany.', 'mikrorurki', 'Wiązka mikrorurek'),
        ('W domu', 'Spawanie i zakończenie', 'Włókna spawamy w puszce abonenckiej, a połączenie sprawdzamy pomiarem.', 'puszka-abonencka', 'Puszka abonencka ze spawami'),
        ('Gotowe', 'Złącze dla operatora', 'Zostaje złącze, do którego operator podłącza swoje urządzenie. Ty wybierasz, w którym pokoju.', 'zlacze-sc-apc', 'Złącze SC/APC'),
    ]
    tf = ''.join(f'<figure{" class=\"ta\"" if i == 0 else ""}>{pic(p, n, a + " (zdjęcie poglądowe)", "50vw")}<figcaption>{e(a)} – zdjęcie poglądowe</figcaption></figure>' for i, (_, _, _, n, a) in enumerate(etapy))
    et = ''.join(f'<li data-i="{i}"{" class=\"ta\"" if i == 0 else ""}><span class="gdzie">{g}</span><h3>{t}</h3><p>{o}</p>{pic(p, n, a + " (zdjęcie poglądowe)", "100vw")}</li>' for i, (g, t, o, n, a) in enumerate(etapy))

    faq = [
        ('Czy do przyłącza trzeba kuć ściany w domu?', 'Zwykle nie. Kabel wchodzi do budynku przez przepust, a w środku prowadzimy go istniejącymi trasami albo w listwie. Jeśli i tak robisz remont, chowamy go w ścianie przed tynkiem lub płytkami.'),
        ('Czy rozkopiecie mi podjazd albo trawnik?', 'Pod nawierzchnią, której nie chcesz ruszać, robimy przewiert sterowany. Tam, gdzie kopiemy, teren jest odtwarzany po pracy.'),
        ('Pracujecie dla operatorów i firm wykonawczych?', 'Tak – możemy wejść jako podwykonawca na wykopy, przewierty, wciąganie kabli, spawanie i pomiary. Zakres ustalamy przy zleceniu.'),
        ('Jaki obszar obsługujecie?', 'Kołobrzeg i okolice oraz województwa zachodniopomorskie, lubuskie i wielkopolskie.'),
        ('Jak wygląda wycena?', 'Zadzwoń albo wyślij zapytanie z adresem budynku. Cena zależy od długości trasy, rodzaju terenu i tego, co trzeba zrobić w środku, dlatego wyceniamy po rozmowie lub oględzinach.'),
    ]
    fq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}

    tresc = f'''<section class="hero">
<div class="wrap">
<div class="hero-txt">
<h1 class="anim">Instalacje światłowodowe od drogi do gniazdka</h1>
<p class="lead anim">Przyłącza do domów, wykopy, przewierty sterowane, spawanie włókien i okablowanie budynków. Ta sama ekipa Exclusive Inside, która wykańcza wnętrza – z tym samym porządkiem na budowie.</p>
<div class="ctas anim"><a class="btn btn-acc" href="tel:{TELH}">{TEL_SVG} Zadzwoń: {TEL}</a><a class="btn btn-line" href="#trasa">Jak powstaje przyłącze</a></div>
<div class="gdzie anim"><span><b>Kołobrzeg</b> i okolice</span><span>zachodniopomorskie · lubuskie · wielkopolskie</span></div>
</div>
<div class="hero-foto">{pic(p, 'spawanie-wlokien', 'Spawanie włókien światłowodowych', '(max-width: 900px) 100vw, 46vw', lazy=False)}<span class="podpis">Spawanie włókien – zdjęcie poglądowe</span></div>
</div>
</section>
<div class="pasek"><div class="wrap"><span><b>Przyłącza</b> do domów</span><span><b>Wykopy</b> i przewierty sterowane</span><span><b>Spawanie</b> i pomiary</span><span><b>Okablowanie</b> budynków</span></div></div>

<section class="sek" id="zakres">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Zakres prac</h2></div><p>Robimy całą trasę albo wybrany odcinek – dla właścicieli domów, wspólnot i jako podwykonawca dla operatorów.</p></div>
{rz}
<p class="uwaga">Zdjęcia w tej części strony są poglądowe (Wikimedia Commons) – w docelowej wersji zastąpimy je zdjęciami z Państwa realizacji.</p>
</div>
</section>

<section class="sek ciemna" id="trasa">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Jak powstaje przyłącze</h2></div><p>Pięć odcinków, przez które przechodzi światłowód, zanim w domu zacznie działać internet.</p></div>
<div class="trasa">
<div class="trasa-foto">{tf}<div class="pasek-postep"><i></i></div></div>
<ol class="etapy">{et}</ol>
</div>
</div>
</section>

<section class="sek" id="dla-kogo">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Dla kogo pracujemy</h2></div><p>Inny klient, inny zakres – ten sam sposób pracy.</p></div>
<div class="trzy">
<div><h3>Właściciele domów</h3><p>Operator przyłącza Cię do sieci, ale trasę na działce i w domu trzeba zrobić porządnie. Uzgadniamy ją z Tobą i sprzątamy po sobie.</p></div>
<div><h3>Deweloperzy i wspólnoty</h3><p>Kanalizacja teletechniczna w nowych budynkach, piony i poziomy w budynkach wielorodzinnych, przygotowanie lokali pod operatora.</p></div>
<div><h3>Operatorzy i wykonawcy</h3><p>Podwykonawstwo: wykopy, przewierty, wciąganie i wdmuchiwanie kabli, spawanie, montaż osprzętu, pomiary.</p></div>
</div>
</div>
</section>

<section class="most do-g">
<div class="m-txt"><h2>Światłowód przy remoncie</h2><p>Robisz łazienkę albo wykończenie domu? Najpierw poprowadzimy trasę kabla w ścianach, potem położymy płytki – bez listew i bez kucia po fakcie.</p><a class="btn" href="{p}glazurnictwo/">Glazurnictwo i wykończenia</a></div>
<div class="m-foto">{pic(p, 'korytarz-cegla', 'Korytarz wykończony przez Exclusive Inside', '(max-width: 900px) 100vw, 50vw')}</div>
</section>

<section class="sek soft" id="faq">
<div class="wrap">
<div class="naglowek"><div><span class="znak"></span><h2>Pytania</h2></div><p>To, o co klienci pytają najczęściej przed przyłączem.</p></div>
<div class="faq">{fq}</div>
</div>
</section>

{kontakt(p, 's')}'''
    zapisz('swiatlowody', strona(p, 's', 'Instalacje światłowodowe Kołobrzeg – przyłącza, przewierty, spawanie | Exclusive Inside',
                                 'Instalacje światłowodowe w Kołobrzegu i okolicy: przyłącza do domów, wykopy i przewierty sterowane, spawanie włókien, okablowanie budynków. Tel. 506 931 962.',
                                 'swiatlowody/', MENU_S(p), tresc, ld=ld_faq))

def zrodla():
    p = '../'
    rows = ''.join(f'<li>{e(k)}<small><a href="{v["page"]}" target="_blank" rel="noopener">{e(v["title"][5:])}</a> · {e(re.sub("<[^>]+>", "", v["artist"]).strip())} · {e(v["lic"])}</small></li>' for k, v in ZRODLA.items())
    tresc = f'''<section class="podhero"><div class="wrap"><h1>Źródła zdjęć poglądowych</h1><p>Zdjęcia w dziale „Światłowody” pochodzą z Wikimedia Commons. Zdjęcia w dziale „Glazurnictwo” to realizacje firmy.</p></div></section>
<section class="sek"><div class="wrap"><ul class="lista2" style="columns:1">{rows}</ul></div></section>'''
    zapisz('zrodla-zdjec', strona(p, 's', 'Źródła zdjęć | Exclusive Inside', 'Licencje zdjęć poglądowych.', 'zrodla-zdjec/', MENU_S(p), tresc, mapa=False))

def extras():
    open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 60 60"><rect x="-6" y="-10" width="60" height="60" rx="8" fill="#0f0e0d"/>'
        + LOGO.split('>', 1)[1].replace('currentColor', '#fff').replace('class="a"', 'fill="#b8935a"'))
    urls = ['', 'glazurnictwo/', 'glazurnictwo/realizacje/', 'swiatlowody/']
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'<url><loc>{BASE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')

wybor(); glazurnictwo(); realizacje(); swiatlowody(); zrodla(); extras()
print('zbudowane')
