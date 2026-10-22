/* Exclusive Inside – ruch strony. Każdy blok w try/catch: awaria jednego nie zatrzymuje reszty. */
(function () {
  var d = document.documentElement;
  var RM = false;
  try { RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { }

  /* 1. Płynne przewijanie – tylko mysz/gładzik */
  var lenis = null;
  try {
    if (!RM && window.Lenis && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      lenis = new window.Lenis({ lerp: 0.085, wheelMultiplier: 0.95, smoothWheel: true, anchors: { offset: -70 } });
      var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      if (d.classList.contains('intro-on')) lenis.stop();
    }
  } catch (e) { lenis = null; }

  var scrollY = function () { return window.pageYOffset || d.scrollTop || 0; };
  var naScroll = [], tik = false;
  var przelicz = function () { tik = false; for (var i = 0; i < naScroll.length; i++) { try { naScroll[i](); } catch (e) { } } };
  var zglos = function () { if (!tik) { tik = true; requestAnimationFrame(przelicz); } };
  window.addEventListener('scroll', zglos, { passive: true });
  window.addEventListener('resize', zglos, { passive: true });

  /* 2. Ekran wejścia (raz na sesję) i start nagłówka */
  var heroGo = function () { requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('hero-go'); }); }); };
  try {
    if (d.classList.contains('intro-on')) {
      requestAnimationFrame(function () { d.classList.add('intro-gra'); });
      var koniec = function () {
        d.classList.add('intro-out');
        setTimeout(heroGo, 260);
        setTimeout(function () {
          d.classList.remove('intro-on', 'intro-gra', 'intro-out');
          if (lenis) lenis.start();
        }, 900);
        try { sessionStorage.setItem('ei_intro', '1'); } catch (e) { }
      };
      var t0 = Date.now();
      var gotowe = function () { setTimeout(koniec, Math.max(0, 2100 - (Date.now() - t0))); };
      if (document.readyState === 'complete') gotowe(); else window.addEventListener('load', gotowe);
      setTimeout(function () { if (d.classList.contains('intro-on')) koniec(); }, 5200);
    } else if (d.classList.contains('przyjscie')) {
      requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('odslon'); }); });
      setTimeout(heroGo, 180);
    } else {
      heroGo();
    }
    setTimeout(function () { d.classList.add('hero-go'); }, 5600);
  } catch (e) { d.classList.add('hero-go'); }

  /* 3. Kurtyna w kolorze działu, do którego się przechodzi */
  try {
    var kurtyna = document.querySelector('.kurtyna');
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      if (a.target || a.hasAttribute('download') || a.hasAttribute('data-lb')) return;
      var u = new URL(a.href, location.href);
      if (u.origin !== location.origin || !/^https?:/.test(u.protocol)) return;
      if (u.pathname === location.pathname && u.hash) return;
      e.preventDefault();
      var kolor = /\/swiatlowody\//.test(u.pathname) ? '#1D44C8' : '#0E0D0C';
      if (kurtyna) kurtyna.style.setProperty('--kurtyna', kolor);
      d.classList.remove('przyjscie', 'odslon');
      d.classList.add('wyjscie');
      try { sessionStorage.setItem('ei_k', kolor); } catch (er) { }
      setTimeout(function () { location.href = u.href; }, 520);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) { d.classList.remove('wyjscie'); d.classList.add('hero-go'); } });
  } catch (e) { }

  /* 4. Pasek: tło po zjechaniu, chowanie w dół, telefon na komórce */
  try {
    var head = document.querySelector('.head');
    var sc = document.querySelector('.sticky-call');
    var hero = document.querySelector('.hero, .pagehead');
    var ostatni = 0;
    naScroll.push(function () {
      var y = scrollY();
      if (head) {
        head.classList.toggle('scr', y > 24);
        if (!d.classList.contains('menu-open')) {
          if (y > ostatni + 4 && y > 520) head.classList.add('hid');
          else if (y < ostatni - 4 || y < 520) head.classList.remove('hid');
        }
      }
      if (sc) sc.classList.toggle('is-on', y > (hero ? hero.offsetHeight * 0.6 : 300));
      ostatni = y;
    });
    przelicz();
  } catch (e) { }

  /* 5. Menu na telefonie */
  try {
    var burger = document.querySelector('.burger');
    if (burger) {
      var zamknijMenu = function () { d.classList.remove('menu-open'); burger.setAttribute('aria-expanded', 'false'); if (lenis) lenis.start(); };
      burger.addEventListener('click', function () {
        var o = d.classList.toggle('menu-open');
        burger.setAttribute('aria-expanded', o ? 'true' : 'false');
        if (lenis) { if (o) lenis.stop(); else lenis.start(); }
      });
      document.querySelectorAll('.mnav a').forEach(function (a) { a.addEventListener('click', zamknijMenu); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') zamknijMenu(); });
    }
  } catch (e) { }

  /* 6. Odsłanianie: obserwator + zapas + bezpiecznik */
  try {
    var rv = [].slice.call(document.querySelectorAll('.rv'));
    var odslon = function (el) {
      if (el.classList.contains('is-in')) return;
      el.classList.add('is-in');
      var dl = parseInt(el.style.getPropertyValue('--d'), 10) || 0;
      setTimeout(function () { el.classList.add('rv-done'); }, 1400 + dl);
    };
    if (!d.classList.contains('anim')) rv.forEach(odslon);
    else {
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (w) {
          w.forEach(function (x) { if (x.isIntersecting) { odslon(x.target); io.unobserve(x.target); } });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
        rv.forEach(function (el) { io.observe(el); });
      }
      var zapas = function () {
        var h = window.innerHeight;
        for (var i = 0; i < rv.length; i++) if (!rv[i].classList.contains('is-in') && rv[i].offsetParent !== null && rv[i].getBoundingClientRect().top < h * 0.94) odslon(rv[i]);
      };
      naScroll.push(zapas);
      setTimeout(zapas, 400); setTimeout(zapas, 3200);
    }
  } catch (e) { document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('is-in'); }); }

  /* 7. Parallaksa zdjęcia w nagłówku */
  try {
    var hm = document.querySelector('.hero-media');
    if (hm && !RM) naScroll.push(function () {
      var y = scrollY();
      if (y < window.innerHeight * 1.2) hm.style.transform = 'translate3d(0,' + (y * 0.22).toFixed(1) + 'px,0)';
    });
  } catch (e) { }

  /* 8. Liczniki */
  try {
    var liczby = [].slice.call(document.querySelectorAll('.num[data-to]'));
    var licz = function (el) {
      if (el.__l) return; el.__l = true;
      var cel = parseFloat(el.getAttribute('data-to').replace(',', '.'));
      var m = (el.getAttribute('data-to').split(',')[1] || '').length;
      var t0 = null, DUR = 1700;
      var krok = function (t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / DUR), e = 1 - Math.pow(2, -10 * p);
        el.textContent = (cel * (p === 1 ? 1 : e)).toFixed(m).replace('.', ',');
        if (p < 1) requestAnimationFrame(krok);
      };
      requestAnimationFrame(krok);
    };
    if ('IntersectionObserver' in window && !RM) {
      var io2 = new IntersectionObserver(function (w) {
        w.forEach(function (x) { if (x.isIntersecting) { licz(x.target); io2.unobserve(x.target); } });
      }, { threshold: 0.6 });
      liczby.forEach(function (el) { io2.observe(el); });
    }
  } catch (e) { }

  /* 9. Proces: linia zapala kolejne etapy */
  try {
    var kroki = document.querySelector('.proc-steps');
    if (kroki) {
      var wire = kroki.querySelector('.wire');
      var steps = [].slice.call(kroki.querySelectorAll('.step'));
      var licznik = document.querySelector('.proc-count b');
      var teraz = document.querySelector('.proc-now');
      naScroll.push(function () {
        var r = kroki.getBoundingClientRect(), linia = window.innerHeight * 0.58;
        var p = Math.max(0, Math.min(1, (linia - r.top - 16) / (r.height - 72)));
        if (wire) wire.style.setProperty('--p', p.toFixed(4));
        var akt = 0;
        steps.forEach(function (s, i) {
          var on = s.getBoundingClientRect().top + 14 < linia;
          s.classList.toggle('is-live', on);
          if (on) akt = i;
        });
        if (licznik) licznik.textContent = ('0' + (akt + 1)).slice(-2);
        if (teraz && steps[akt]) teraz.textContent = steps[akt].getAttribute('data-nazwa') || '';
      });
      przelicz();
    }
  } catch (e) { }

  /* 10. Trasa światłowodu: zdjęcie zmienia się z etapem */
  try {
    var etapy = [].slice.call(document.querySelectorAll('.etapy li'));
    var zdj = [].slice.call(document.querySelectorAll('.trasa-foto figure'));
    var lz = document.querySelector('.trasa-foto .licz');
    if (etapy.length) naScroll.push(function () {
      var linia = window.innerHeight * 0.5, akt = 0;
      etapy.forEach(function (e, i) { if (e.getBoundingClientRect().top < linia) akt = i; });
      etapy.forEach(function (e, i) { e.classList.toggle('ta', i === akt); });
      zdj.forEach(function (f, i) { f.classList.toggle('ta', i === akt); });
      if (lz) lz.textContent = ('0' + (akt + 1)).slice(-2);
    });
    przelicz();
  } catch (e) { }

  /* 11. Filtr realizacji */
  var fots = [].slice.call(document.querySelectorAll('[data-lb]'));
  try {
    var chips = [].slice.call(document.querySelectorAll('.chip[data-k]'));
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        chips.forEach(function (x) { x.classList.toggle('ta', x === b); });
        var k = b.getAttribute('data-k');
        fots.forEach(function (f) {
          var ukryj = k !== 'wszystkie' && f.getAttribute('data-k') !== k;
          f.classList.toggle('ukryte', ukryj);
          if (!ukryj) { f.classList.add('is-in', 'rv-done'); }
        });
        if (lenis) lenis.resize();
      });
    });
  } catch (e) { }

  /* 12. Podgląd zdjęć */
  try {
    if (fots.length) {
      var SV = function (p) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="' + p + '"/></svg>'; };
      var lb = document.createElement('div');
      lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Podgląd zdjęcia');
      lb.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
        '<button class="lb-btn lb-x" aria-label="Zamknij">' + SV('M6 6l12 12M18 6L6 18') + '</button>' +
        '<button class="lb-btn lb-prev" aria-label="Poprzednie">' + SV('M15 5l-7 7 7 7') + '</button>' +
        '<button class="lb-btn lb-next" aria-label="Następne">' + SV('M9 5l7 7-7 7') + '</button>';
      document.body.appendChild(lb);
      var li = lb.querySelector('img'), lc = lb.querySelector('figcaption'), biez = 0, lista = [];
      var pokaz = function (i) { biez = (i + lista.length) % lista.length; var f = lista[biez]; li.src = f.getAttribute('href'); lc.textContent = f.getAttribute('data-opis') || ''; };
      var zamknij = function () { lb.classList.remove('is-open'); if (lenis) lenis.start(); };
      fots.forEach(function (f) {
        f.addEventListener('click', function (e) {
          e.preventDefault();
          lista = fots.filter(function (x) { return !x.classList.contains('ukryte'); });
          pokaz(lista.indexOf(f)); lb.classList.add('is-open'); if (lenis) lenis.stop();
        });
      });
      lb.querySelector('.lb-x').onclick = zamknij;
      lb.querySelector('.lb-prev').onclick = function () { pokaz(biez - 1); };
      lb.querySelector('.lb-next').onclick = function () { pokaz(biez + 1); };
      lb.addEventListener('click', function (e) { if (e.target === lb) zamknij(); });
      document.addEventListener('keydown', function (e) {
        if (!lb.classList.contains('is-open')) return;
        if (e.key === 'Escape') zamknij(); if (e.key === 'ArrowLeft') pokaz(biez - 1); if (e.key === 'ArrowRight') pokaz(biez + 1);
      });
    }
  } catch (e) { }

  /* 13. Formularz: wiadomość składana w programie pocztowym */
  try {
    var form = document.querySelector('.form');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var t = 'Imię: ' + (f.get('imie') || '') + '\nTelefon: ' + (f.get('tel') || '') + '\nMiejscowość: ' + (f.get('miejsce') || '') + '\n\n' + (f.get('opis') || '');
      location.href = 'mailto:' + form.getAttribute('data-mail') + '?subject=' + encodeURIComponent('Zapytanie: ' + (f.get('temat') || '')) + '&body=' + encodeURIComponent(t);
    });
  } catch (e) { }

  /* 14. Mapa */
  try {
    var m = document.getElementById('mapa');
    if (m && window.L) {
      var map = L.map(m, { scrollWheelZoom: false }).setView([54.1629, 15.5379], 11);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap' }).addTo(map);
      L.circleMarker([54.1629, 15.5379], { radius: 9, color: '#fff', weight: 2, fillColor: getComputedStyle(document.body).getPropertyValue('--accent').trim() || '#C9A46A', fillOpacity: 1 }).addTo(map);
    }
  } catch (e) { }
})();
