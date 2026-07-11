/**
 * GVI — automatische ontvangstbevestiging
 * ----------------------------------------
 * Draait als Google Apps Script (script.google.com) op het Gmail-account
 * van Iris. Kijkt elke paar minuten of er nieuwe formulier-mails van de
 * GVI-website (via Web3Forms) zijn binnengekomen en stuurt de inzender
 * direct een warme ontvangstbevestiging — vanaf Iris' eigen adres.
 *
 * Alleen een ONTVANGSTbevestiging; nooit een inhoudelijk antwoord.
 *
 * Installatie (eenmalig):
 *   1. Ga naar https://script.google.com → Nieuw project
 *   2. Plak dit hele bestand in de editor, sla op (naam: "GVI autobevestiging")
 *   3. Voer één keer de functie verstuurBevestigingen uit en geef toestemming
 *   4. Voeg een trigger toe: verstuurBevestigingen — tijdgestuurd — elke 5 minuten
 */

var AFZENDER_NAAM = 'Iris Ficker-Younge — GVI';
var ANTWOORD_ADRES = 'irisfickeryounge+gvi@gmail.com';
var WEBSITE = 'globalvoiceintelligence.com';
var LABEL_NAAM = 'GVI-bevestigd';
var MAX_LEEFTIJD = 'newer_than:2d'; // oudere mails nooit alsnog beantwoorden

/* Onderwerpen zoals js/main.js ze meegeeft aan Web3Forms */
var ZOEKOPDRACHT = '(subject:"GVI-website:" OR subject:"Nieuwsbrief-inschrijving via GVI-website" OR subject:"Download-aanvraag:") ' + MAX_LEEFTIJD + ' -label:' + LABEL_NAAM;

function verstuurBevestigingen() {
  var props = PropertiesService.getScriptProperties();
  var verwerkt = JSON.parse(props.getProperty('verwerkteIds') || '[]');
  var label = GmailApp.getUserLabelByName(LABEL_NAAM) || GmailApp.createLabel(LABEL_NAAM);

  GmailApp.search(ZOEKOPDRACHT, 0, 20).forEach(function (thread) {
    thread.getMessages().forEach(function (bericht) {
      var id = bericht.getId();
      if (verwerkt.indexOf(id) !== -1) return;
      verwerkt.push(id);

      var onderwerp = bericht.getSubject() || '';
      var tekst = bericht.getPlainBody() || '';
      var naar = vindInzender(bericht, tekst);
      if (!naar) return; // geen e-mailadres gevonden — stil overslaan

      var mail = steldMailSamen(onderwerp, tekst);
      GmailApp.sendEmail(naar, mail.onderwerp, mail.tekst, {
        name: AFZENDER_NAAM,
        replyTo: ANTWOORD_ADRES
      });
    });
    thread.addLabel(label);
  });

  /* alleen de laatste 300 ids bewaren */
  props.setProperty('verwerkteIds', JSON.stringify(verwerkt.slice(-300)));
}

/* E-mailadres van de inzender: eerst Reply-To, anders het email-veld in de mailtekst */
function vindInzender(bericht, tekst) {
  var patroon = /[\w.+-]+@[\w-]+\.[\w.-]+/;
  var replyTo = (bericht.getReplyTo() || '').match(patroon);
  if (replyTo && replyTo[0].indexOf('web3forms') === -1) return replyTo[0];
  var veld = tekst.match(/email[^\S\r\n]*[:\s]+\s*([\w.+-]+@[\w-]+\.[\w.-]+)/i);
  return veld ? veld[1] : null;
}

/* Voornaam uit het naam-veld, voor een persoonlijke aanhef */
function vindVoornaam(tekst) {
  var m = tekst.match(/\bnaam[^\S\r\n]*[:\s]+[^\S\r\n]*([^\r\n]+)/i);
  if (!m) return '';
  var naam = m[1].trim().split(/\s+/)[0];
  return /^[A-Za-zÀ-ÿ'-]{2,}$/.test(naam) ? naam : '';
}

function steldMailSamen(onderwerp, tekst) {
  var voornaam = vindVoornaam(tekst);
  var aanhef = voornaam ? 'Hallo ' + voornaam + ',' : 'Hallo,';
  var groet = '\n\nHartelijke groet,\nIris Ficker-Younge\nGVI — Global Voice Intelligence\n' + WEBSITE;

  if (onderwerp.indexOf('Nieuwsbrief-inschrijving') !== -1) {
    return {
      onderwerp: 'Je staat op de lijst — GVI',
      tekst: aanhef + '\n\nDank je wel voor je inschrijving — het is gelukt, je staat op de lijst.\n\n' +
        'Je hoort van me zodra er iets te lezen valt. Geen wekelijkse stroom, wel af en toe iets dat de moeite waard is.' + groet
    };
  }

  if (onderwerp.indexOf('Download-aanvraag:') === 0) {
    var doc = onderwerp.replace('Download-aanvraag:', '').trim();
    return {
      onderwerp: 'Gelukt — je download van GVI',
      tekst: aanhef + '\n\nDank je wel voor je interesse in ' + (doc || 'de whitepaper') + ' — je aanvraag is goed aangekomen.\n\n' +
        'Als de download niet vanzelf startte, stuur dan even een reactie op deze mail; dan stuur ik hem persoonlijk toe.\n\n' +
        'Heb je na het lezen vragen? Reageer gerust — ik lees alles zelf, en antwoord meestal binnen een paar werkdagen.' + groet
    };
  }

  /* contactformulier (onderwerp: "GVI-website: ...") */
  return {
    onderwerp: 'Goed aangekomen — je bericht aan GVI',
    tekst: aanhef + '\n\nJe bericht is goed aangekomen — dank je wel dat je de moeite nam.\n\n' +
      'Dit is alleen een bevestiging, zodat je weet dat het versturen gelukt is. Het echte antwoord komt van mij persoonlijk — van een mens, niet van een bot. Meestal binnen een paar werkdagen.' + groet
  };
}
