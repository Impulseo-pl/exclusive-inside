import sys
from playwright.sync_api import sync_playwright
from PIL import Image
w=int(sys.argv[1]); path=sys.argv[2]; step=int(sys.argv[3]) if len(sys.argv)>3 else 900; mobile=w<700
H=900 if not mobile else 844
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':H},is_mobile=mobile,has_touch=mobile)
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://127.0.0.1:8124/exclusive-inside/'+path+'?team=1',wait_until='networkidle'); pg.wait_for_timeout(4200)
    h=pg.evaluate('document.documentElement.scrollHeight'); shots=[]
    y=0
    while y < h:
        pg.evaluate(f'window.__lenis?window.__lenis.scrollTo({y},{{immediate:true}}):window.scrollTo(0,{y})')
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(1500)
        f=f'tour_{len(shots)}.png'; pg.screenshot(path=f); shots.append(f); y+=step
        h=pg.evaluate('document.documentElement.scrollHeight')
    print('errors',errs,'h',h,'sw',pg.evaluate('document.documentElement.scrollWidth'),'n',len(shots))
    b.close()
tw=480 if not mobile else 260; th=int(H*tw/w); cols=4 if not mobile else 6
ims=[Image.open(f).resize((tw,th)) for f in shots]
name=(path.strip('/') or 'home').replace('/','_')+f'_{w}'
for part in range(0,len(ims),cols*3):
    sub=ims[part:part+cols*3]; rows=(len(sub)+cols-1)//cols
    s=Image.new('RGB',(cols*(tw+6),rows*(th+6)),'red')
    for i,im in enumerate(sub): s.paste(im,((i%cols)*(tw+6),(i//cols)*(th+6)))
    s.save(f'tour_{name}_{part//(cols*3)}.png')
    print(f'tour_{name}_{part//(cols*3)}.png')
