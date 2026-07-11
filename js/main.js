/* GVI — navigatie, reveal-animaties, contactformulier, nieuwsbrief en downloads */
(function () {
  'use strict';

  /* Web3Forms: verzendt formulieren naar irisfickeryounge@gmail.com (zie README) */
  var WEB3FORMS_KEY = '0106b5b5-0fe3-4816-ab7d-335848bfac1e';
  var ONTVANGER = 'irisfickeryounge@gmail.com';

  /* ---------- Mobiel menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.hoofdnav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---------- Dropdown "Wat we doen" (klik + toetsenbord) ---------- */
  document.querySelectorAll('.heeft-sub').forEach(function (li) {
    var knop = li.querySelector('.navknop');
    if (!knop) return;
    knop.addEventListener('click', function (e) {
      e.stopPropagation();
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
        bericht: form.bericht.value.trim()
      }, function (gelukt) {
        knop.disabled = false;
        if (gelukt) {
          form.reset();
          status.className = 'form-status ok';
          status.textContent = 'Dank je wel! Je bericht is verstuurd — je krijgt zo een bevestiging per mail. Ik reageer persoonlijk, meestal binnen een paar werkdagen.';
        } else {
          status.className = 'form-status niet-ok';
          status.textContent = 'Het versturen is niet gelukt. Mail ons direct via ' + ONTVANGER + ' — dan komt je bericht zeker aan.';
        }
      });
    });

    form.addEventListener('input', function (e) {
      if (e.target.closest('.veld')) toonFout(e.target, false);
    });
  }

  /* ---------- Nieuwsbrief-formulieren (blok + footer) ---------- */
  document.querySelectorAll('form.nieuwsbrief').forEach(function (nb) {
    nb.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = nb.querySelector('input[type="email"]');
      var status = nb.querySelector('.form-status');
      var knop = nb.querySelector('button[type="submit"]');
      status.classList.remove('ok', 'niet-ok');
      if (!geldigEmail(input.value)) {
        status.classList.add('niet-ok');
        status.textContent = 'Vul een geldig e-mailadres in.';
        return;
      }
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
          status.textContent = 'Dank je wel! Je staat op de lijst — je krijgt zo een bevestiging per mail.';
        } else {
          status.classList.add('niet-ok');
          status.textContent = 'Inschrijven lukte niet — mail ons via ' + ONTVANGER + '.';
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
      if (!naam.value.trim() || !org.value.trim() || !geldigEmail(email.value)) {
        dlStatus.className = 'form-status niet-ok';
        dlStatus.textContent = 'Vul naam, organisatie en een geldig e-mailadres in.';
        return;
      }
      var knop = dlForm.querySelector('button[type="submit"]');
      knop.disabled = true;
      verstuur({
        subject: 'Download-aanvraag: ' + huidigDoc,
        from_name: naam.value.trim(),
        naam: naam.value.trim(),
        organisatie: org.value.trim(),
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
          dlStatus.textContent = 'Aanvragen lukte niet — mail ons via ' + ONTVANGER + '.';
        }
      });
    });
  }
})();
