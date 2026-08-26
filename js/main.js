/* GVI — navigatie, reveal-animaties, contactformulier, nieuwsbrief en downloads */
(function () {
  'use strict';

  /* Web3Forms verwerkt de formulieren via de aan de access key gekoppelde GVI-inbox. */
  var WEB3FORMS_KEY = '0106b5b5-0fe3-4816-ab7d-335848bfac1e';

  /* ---------- Mobiel menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.hoofdnav');
  if (toggle && nav) {
    var sluitMenu = function () {
      nav.classList.remove('open');
      document.body.classList.remove('menu-open');
      toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) sluitMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        sluitMenu();
        toggle.focus();
      }
    });

    /* Voorkom een vastgezette body na draaien van een telefoon of vergroten
       van het venster terwijl het mobiele menu open stond. */
    var desktopMenu = window.matchMedia('(min-width: 981px)');
    var herstelDesktop = function (e) { if (e.matches) sluitMenu(); };
    if (desktopMenu.addEventListener) desktopMenu.addEventListener('change', herstelDesktop);
    else desktopMenu.addListener(herstelDesktop);
  }

  /* ---------- Dropdown "Wat we doen" (klik + toetsenbord) ---------- */
  document.querySelectorAll('.heeft-sub').forEach(function (li) {
    var knop = li.querySelector('.navknop');
    if (!knop) return;
    knop.addEventListener('click', function (e) {
      e.stopPropagation();
      document.querySelectorAll('.heeft-sub.open').forEach(function (ander) {
        if (ander === li) return;
        ander.classList.remove('open');
        var andereKnop = ander.querySelector('.navknop');
        if (andereKnop) andereKnop.setAttribute('aria-expanded', 'false');
      });
      var open = li.classList.toggle('open');
      knop.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    li.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        li.classList.remove('open');
        knop.setAttribute('aria-expanded', 'false');
        knop.focus();
      }
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.heeft-sub.open').forEach(function (li) {
      li.classList.remove('open');
      var knop = li.querySelector('.navknop');
      if (knop) knop.setAttribute('aria-expanded', 'false');
    });
  });

  /* ---------- Reveal bij scroll (respecteert reduced motion) ---------- */
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealEls = document.querySelectorAll('.reveal');
  if (!reduceMotion && 'IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('zichtbaar');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('zichtbaar'); });
  }

  /* ---------- Gedeelde Web3Forms-verzending ---------- */
  function verstuur(velden, klaar) {
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(Object.assign({ access_key: WEB3FORMS_KEY }, velden))
    }).then(function (r) { return r.json(); }).then(function (res) {
      klaar(!!res.success);
    }).catch(function () { klaar(false); });
  }

  function geldigEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); }

  /* ---------- Contactformulier ---------- */
  var form = document.getElementById('contact-form');
  if (form) {
    /* onderwerp voorselecteren via ?onderwerp=... (bijv. vanaf de Regie Scan-pagina) */
    var gewenst = new URLSearchParams(window.location.search).get('onderwerp');
    if (gewenst && form.onderwerp) {
      Array.prototype.forEach.call(form.onderwerp.options, function (opt) {
        if (opt.value === gewenst || opt.text === gewenst) form.onderwerp.value = opt.value;
      });
    }
    var status = document.getElementById('form-status');

    var toonFout = function (veld, tonen) {
      var wrap = veld.closest('.veld');
      if (wrap) wrap.classList.toggle('fout', tonen);
      veld.setAttribute('aria-invalid', tonen ? 'true' : 'false');
    };

    var valideer = function () {
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (veld) {
        var leeg = veld.type === 'checkbox' ? !veld.checked : !veld.value.trim();
        var mailFout = veld.type === 'email' && veld.value.trim() && !geldigEmail(veld.value);
        toonFout(veld, leeg || mailFout);
        if (leeg || mailFout) ok = false;
      });
      return ok;
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      status.className = 'form-status';
      status.textContent = '';

      if (!valideer()) {
        status.className = 'form-status niet-ok';
        status.textContent = 'Controleer de rood gemarkeerde velden en probeer het opnieuw.';
        var eersteFout = form.querySelector('[aria-invalid="true"]');
        if (eersteFout) eersteFout.focus();
        return;
      }

      var knop = form.querySelector('button[type="submit"]');
      knop.disabled = true;
      verstuur({
        subject: 'GVI-website: ' + form.onderwerp.value + ' — ' + form.naam.value.trim(),
        from_name: form.naam.value.trim(),
        naam: form.naam.value.trim(),
        organisatie: form.organisatie.value.trim(),
        email: form.email.value.trim(),
        telefoon: form.telefoon.value.trim() || '—',
        onderwerp: form.onderwerp.value,
        bericht: form.bericht.value.trim(),
        privacy_akkoord: form.privacy.checked ? 'Ja' : 'Nee'
      }, function (gelukt) {
        knop.disabled = false;
        if (gelukt) {
          form.reset();
          status.className = 'form-status ok';
          status.textContent = 'Dank je wel! Je bericht is verstuurd. Ik reageer persoonlijk, meestal binnen een paar werkdagen.';
        } else {
          status.className = 'form-status niet-ok';
          status.textContent = 'Het versturen is niet gelukt. Probeer het later opnieuw of neem contact op via LinkedIn.';
        }
      });
    });

    form.addEventListener('input', function (e) {
      if (e.target.closest('.veld')) toonFout(e.target, false);
    });
  }

  /* ---------- Nieuwsbrief-formulieren (blok + footer) ---------- */
  document.querySelectorAll('form.nieuwsbrief').forEach(function (nb) {
    nb.addEventListener('input', function (e) {
      if (e.target.matches('input[type="email"]')) e.target.setAttribute('aria-invalid', 'false');
    });

    nb.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = nb.querySelector('input[type="email"]');
      var status = nb.querySelector('.form-status');
      var knop = nb.querySelector('button[type="submit"]');
      status.classList.remove('ok', 'niet-ok');
      if (!geldigEmail(input.value)) {
        input.setAttribute('aria-invalid', 'true');
        status.classList.add('niet-ok');
        status.textContent = 'Vul een geldig e-mailadres in.';
        return;
      }
      input.setAttribute('aria-invalid', 'false');
      knop.disabled = true;
      verstuur({
        subject: 'Nieuwsbrief-inschrijving via GVI-website',
        from_name: 'GVI-website',
        email: input.value.trim(),
        bericht: 'Nieuwe nieuwsbrief-inschrijving: ' + input.value.trim()
      }, function (gelukt) {
        knop.disabled = false;
        if (gelukt) {
          nb.reset();
          status.classList.add('ok');
          status.textContent = 'Dank je wel! Je inschrijving is ontvangen.';
        } else {
          status.classList.add('niet-ok');
          status.textContent = 'Inschrijven lukte niet. Probeer het later opnieuw.';
        }
      });
    });
  });

  /* ---------- Download-modal (lead magnets) ---------- */
  var modal = document.getElementById('download-modal');
  if (modal) {
    var dlTitel = modal.querySelector('#dl-titel');
    var dlForm = modal.querySelector('form');
    var dlStatus = modal.querySelector('.form-status');
    var huidigDoc = '';
    var huidigBestand = '';

    document.querySelectorAll('[data-download]').forEach(function (knop) {
      knop.addEventListener('click', function () {
        huidigDoc = knop.getAttribute('data-download');
        huidigBestand = knop.getAttribute('data-file') || '';
        dlTitel.textContent = huidigDoc;
        dlStatus.className = 'form-status';
        dlStatus.textContent = '';
        dlForm.reset();
        dlForm.querySelectorAll('[aria-invalid]').forEach(function (veld) { veld.removeAttribute('aria-invalid'); });
        dlForm.querySelectorAll('.veld.fout').forEach(function (wrap) { wrap.classList.remove('fout'); });
        modal.showModal();
      });
    });

    modal.querySelector('.modal-sluit').addEventListener('click', function () { modal.close(); });
    modal.addEventListener('click', function (e) { if (e.target === modal) modal.close(); });

    dlForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var naam = dlForm.querySelector('[name="naam"]');
      var email = dlForm.querySelector('[name="email"]');
      var org = dlForm.querySelector('[name="organisatie"]');
      var fouten = [[email, !geldigEmail(email.value)]];
      fouten.forEach(function (item) {
        item[0].setAttribute('aria-invalid', item[1] ? 'true' : 'false');
        var wrap = item[0].closest('.veld');
        if (wrap) wrap.classList.toggle('fout', item[1]);
      });
      if (fouten.some(function (item) { return item[1]; })) {
        dlStatus.className = 'form-status niet-ok';
        dlStatus.textContent = 'Vul een geldig e-mailadres in.';
        email.focus();
        return;
      }
      var knop = dlForm.querySelector('button[type="submit"]');
      knop.disabled = true;
      verstuur({
        subject: 'Download-aanvraag: ' + huidigDoc,
        from_name: naam.value.trim() || 'Websitebezoeker',
        naam: naam.value.trim() || '—',
        organisatie: org.value.trim() || '—',
        email: email.value.trim(),
        bericht: 'Download-aanvraag voor: ' + huidigDoc
      }, function (gelukt) {
        knop.disabled = false;
        if (gelukt) {
          dlStatus.className = 'form-status ok';
          if (huidigBestand) {
            dlStatus.textContent = 'Dank je wel! Je download start nu.';
            var a = document.createElement('a');
            a.href = huidigBestand;
            a.download = '';
            document.body.appendChild(a);
            a.click();
            a.remove();
          } else {
            dlStatus.textContent = 'Dank je wel! We mailen je de download-link.';
          }
        } else {
          dlStatus.className = 'form-status niet-ok';
          dlStatus.textContent = 'Aanvragen lukte niet. Probeer het later opnieuw.';
        }
      });
    });

    dlForm.addEventListener('input', function (e) {
      if (!e.target.matches('input')) return;
      e.target.setAttribute('aria-invalid', 'false');
      var wrap = e.target.closest('.veld');
      if (wrap) wrap.classList.remove('fout');
    });
  }
})();
