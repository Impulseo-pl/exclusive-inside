(function(){
  var d=document.documentElement,pierwszy=d.classList.contains('pierwszy'),
      malo=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ekran ładowania przy pierwszym wejściu, potem tylko zasłona */
  var start=Date.now(),MIN=pierwszy&&!malo?2000:0;
  function gotowe(){
    if(d.classList.contains('gotowe'))return;
    setTimeout(function(){
      d.classList.add('gotowe');
      try{sessionStorage.setItem('ei_l','1')}catch(e){}
    },Math.max(0,MIN-(Date.now()-start)));
  }
  if(document.readyState==='complete')gotowe();else window.addEventListener('load',gotowe);
  setTimeout(gotowe,MIN+2500);

  /* zasłona w kolorze gałęzi, do której się przechodzi */
  var zaslona=document.querySelector('.zaslona');
  document.addEventListener('click',function(e){
    var a=e.target.closest('a');
    if(!a||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;
    if(a.target||a.hasAttribute('download')||a.classList.contains('fot'))return;
    var u=new URL(a.href,location.href);
    if(u.origin!==location.origin||!/^https?:/.test(u.protocol))return;
    if(u.pathname===location.pathname&&u.hash)return;
    e.preventDefault();
    var kolor=/\/swiatlowody\//.test(u.pathname)?'#1d44c8':(/\/glazurnictwo\//.test(u.pathname)?'#0f0e0d':'#0f0e0d');
    if(zaslona){zaslona.classList.remove('start');zaslona.style.setProperty('--zaslona',kolor);}
    d.classList.add('wyjscie');
    try{sessionStorage.setItem('ei_z',kolor)}catch(e){}
    setTimeout(function(){location.href=u.href},480);
  });
  window.addEventListener('pageshow',function(e){if(e.persisted){d.classList.remove('wyjscie');d.classList.add('gotowe')}});

  /* płynne przewijanie */
  var lenis=null;
  if(window.Lenis&&!malo){
    lenis=new Lenis({duration:1.2,easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t))},anchors:{offset:-90},smoothWheel:true});
    (function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(performance.now());
  }

  /* nagłówek: tło po zjechaniu z hero, chowanie przy przewijaniu w dół */
  var top=document.querySelector('.top'),ostatni=0,heroFoto=document.querySelector('.hero-foto img');
  function naScroll(){
    var y=window.scrollY;
    if(top){
      var otw=top.classList.contains('otw');
      top.classList.toggle('tlo',y>60);
      top.classList.toggle('schowany',!otw&&y>ostatni&&y>400);
    }
    ostatni=y;
    if(heroFoto&&!malo&&y<1100)heroFoto.style.transform='translate3d(0,'+(y*0.12)+'px,0) scale(1.06)';
  }
  window.addEventListener('scroll',naScroll,{passive:true});naScroll();

  /* menu mobilne */
  var burger=document.querySelector('.burger');
  if(burger)burger.addEventListener('click',function(){
    var o=top.classList.toggle('otw');burger.setAttribute('aria-expanded',o);
    if(lenis){o?lenis.stop():lenis.start()}
    document.body.style.overflow=o?'hidden':'';
  });
  document.querySelectorAll('.menu a').forEach(function(a){a.addEventListener('click',function(){
    if(top.classList.contains('otw')){top.classList.remove('otw');document.body.style.overflow='';if(lenis)lenis.start()}
  })});

  /* odsłanianie przy przewijaniu */
  var GRUPY=[['.naglowek>*','g'],['.rzad-txt',''],['.kroki li',''],['.opinia',''],['.trzy>div','g'],['.faq details','g'],
    ['.lista2 li',''],['.dane',''],['.formularz',''],['.para-opis>*','g'],['.m-txt>*','g'],['.stopka-gora>div','g'],['.filtry',''],['.ocena','']];
  var FOTO=['.rzad-foto figure','.para figure','.proces-foto figure','.mur .fot','.m-foto'];
  var el=[];
  GRUPY.forEach(function(g){document.querySelectorAll(g[0]).forEach(function(x){
    x.classList.add('rv');
    if(g[1]){var i=Array.prototype.indexOf.call(x.parentNode.children,x);x.style.setProperty('--d',(Math.min(i,6)*0.09)+'s')}
    el.push(x);
  })});
  FOTO.forEach(function(s){document.querySelectorAll(s).forEach(function(x){
    x.classList.add('rv-foto');
    var i=Array.prototype.indexOf.call(x.parentNode.children,x);
    if(x.matches('.mur .fot'))i=i%3;
    x.style.setProperty('--d',(Math.min(i,6)*0.1)+'s');el.push(x);
  })});
  if('IntersectionObserver' in window&&!malo){
    var io=new IntersectionObserver(function(en){en.forEach(function(x){
      if(x.isIntersecting){x.target.classList.add('widac');io.unobserve(x.target)}
    })},{rootMargin:'0px 0px -8% 0px',threshold:0.06});
    el.forEach(function(x){io.observe(x)});
  }else el.forEach(function(x){x.classList.add('widac')});

  /* trasa światłowodu: zdjęcie po lewej zmienia się z etapem */
  var etapy=document.querySelectorAll('.etapy li'),zdj=document.querySelectorAll('.trasa-foto figure'),pas=document.querySelector('.pasek-postep i');
  if(etapy.length&&'IntersectionObserver' in window){
    var io2=new IntersectionObserver(function(en){en.forEach(function(x){
      if(!x.isIntersecting)return;
      var i=+x.target.dataset.i;
      etapy.forEach(function(e,k){e.classList.toggle('ta',k===i)});
      zdj.forEach(function(f,k){f.classList.toggle('ta',k===i)});
      if(pas)pas.style.height=((i+1)/etapy.length*100)+'%';
    })},{rootMargin:'-45% 0px -45% 0px'});
    etapy.forEach(function(e){io2.observe(e)});
  }

  /* filtr realizacji */
  var fb=document.querySelectorAll('.filtry button'),fots=document.querySelectorAll('.mur .fot');
  fb.forEach(function(b){b.addEventListener('click',function(){
    fb.forEach(function(x){x.classList.toggle('ta',x===b)});
    var k=b.dataset.k;
    fots.forEach(function(f){f.classList.toggle('ukryte',k!=='wszystkie'&&f.dataset.k!==k)});
    if(lenis)lenis.resize();
  })});

  /* podgląd zdjęć */
  if(fots.length){
    var lb=document.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');
    lb.innerHTML='<button class="x" aria-label="Zamknij">&times;</button><button class="pop" aria-label="Poprzednie">&#8249;</button><img alt=""><button class="nast" aria-label="Następne">&#8250;</button><p></p>';
    document.body.appendChild(lb);
    var lbi=lb.querySelector('img'),lbp=lb.querySelector('p'),biez=0,lista=[];
    function pokaz(i){biez=(i+lista.length)%lista.length;var f=lista[biez];lbi.src=f.href;lbp.textContent=f.dataset.opis||'';}
    function zamknij(){lb.classList.remove('otw');if(lenis)lenis.start();document.body.style.overflow=''}
    fots.forEach(function(f){f.addEventListener('click',function(e){
      e.preventDefault();lista=Array.prototype.filter.call(fots,function(x){return !x.classList.contains('ukryte')});
      pokaz(lista.indexOf(f));lb.classList.add('otw');if(lenis)lenis.stop();document.body.style.overflow='hidden';
    })});
    lb.querySelector('.x').onclick=zamknij;
    lb.querySelector('.pop').onclick=function(){pokaz(biez-1)};
    lb.querySelector('.nast').onclick=function(){pokaz(biez+1)};
    lb.addEventListener('click',function(e){if(e.target===lb)zamknij()});
    document.addEventListener('keydown',function(e){
      if(!lb.classList.contains('otw'))return;
      if(e.key==='Escape')zamknij();if(e.key==='ArrowLeft')pokaz(biez-1);if(e.key==='ArrowRight')pokaz(biez+1);
    });
  }

  /* formularz: wiadomość składana w programie pocztowym */
  var form=document.querySelector('.formularz');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    var f=new FormData(form),t='Imię: '+(f.get('imie')||'')+'\nTelefon: '+(f.get('tel')||'')+'\nMiejscowość: '+(f.get('miejsce')||'')+'\n\n'+(f.get('opis')||'');
    location.href='mailto:'+form.dataset.mail+'?subject='+encodeURIComponent('Zapytanie: '+(f.get('temat')||''))+'&body='+encodeURIComponent(t);
  });

  /* mapa */
  var m=document.getElementById('mapa');
  if(m&&window.L){
    var map=L.map(m,{scrollWheelZoom:false,attributionControl:true}).setView([54.1629,15.5379],12);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; OpenStreetMap'}).addTo(map);
    L.marker([54.1629,15.5379]).addTo(map);
  }
})();
