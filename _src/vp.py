import sys
from playwright.sync_api import sync_playwright
w=int(sys.argv[1]); path=sys.argv[2]; ys=[int(x) for x in sys.argv[3].split(',')]; mobile=w<700
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':900 if not mobile else 844},is_mobile=mobile,has_touch=mobile)
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://127.0.0.1:8124/exclusive-inside/'+path+'?team=1',wait_until='networkidle'); pg.wait_for_timeout(2800)
    for y in ys:
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(1600)
        pg.screenshot(path=f'vp_{(path.strip("/") or "home").replace("/","_")}_{w}_{y}.png')
    print('errors',errs, 'sw', pg.evaluate('document.documentElement.scrollWidth'))
    b.close()
