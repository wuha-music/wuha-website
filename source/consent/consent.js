/* WUHA cookie consent: nothing from third parties loads before consent.
   Google Tag Manager (GA4, Meta Pixel, TikTok Pixel) loads only after "Statistics" or "Marketing" is accepted. */
(function () {
  var GTM_ID = 'GTM-5JK6VLZG';
  var PRIVACY = 'https://www.wuha.world/privacy-policy/';
  var gtmLoaded = false;
  function gtag() { window.dataLayer.push(arguments); }
  function loadGTM() {
    if (gtmLoaded) return; gtmLoaded = true;
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    document.head.appendChild(s);
  }
  function apply() {
    var a = CookieConsent.acceptedCategory('analytics');
    var m = CookieConsent.acceptedCategory('marketing');
    var md = CookieConsent.acceptedCategory('media');
    gtag('consent', 'update', {
      analytics_storage: a ? 'granted' : 'denied',
      ad_storage: m ? 'granted' : 'denied',
      ad_user_data: m ? 'granted' : 'denied',
      ad_personalization: m ? 'granted' : 'denied'
    });
    window.dataLayer.push({ event: 'wuha_consent', consent_analytics: a, consent_marketing: m, consent_media: md });
    if (a || m) loadGTM();
    if (md && window.wuhaLoadPlayer) window.wuhaLoadPlayer();
  }
  CookieConsent.run({
    revision: 1,
    cookie: { name: 'wuha_consent', expiresAfterDays: 182 },
    guiOptions: {
      consentModal: { layout: 'box wide', position: 'bottom center', equalWeightButtons: true, flipButtons: false },
      preferencesModal: { layout: 'box', equalWeightButtons: true, flipButtons: false }
    },
    categories: {
      necessary: { enabled: true, readOnly: true },
      analytics: { autoClear: { cookies: [{ name: /^_ga/ }, { name: '_gid' }], reloadPage: true } },
      marketing: { autoClear: { cookies: [{ name: '_fbp' }, { name: /^_tt/ }, { name: '_ttp' }, { name: '_gcl_au' }], reloadPage: true } },
      media: {}
    },
    onConsent: apply,
    onChange: apply,
    language: {
      default: 'en',
      translations: {
        en: {
          consentModal: {
            title: 'Feel the Groove, your way',
            description: 'We use cookies to count visits and to measure our ads on Meta and TikTok. Nothing is loaded before you choose. You can change your choice any time under “Cookie settings”. <a href="' + PRIVACY + '">Privacy policy</a>',
            acceptAllBtn: 'Accept all',
            acceptNecessaryBtn: 'Only necessary',
            showPreferencesBtn: 'Choose'
          },
          preferencesModal: {
            title: 'Cookie settings',
            acceptAllBtn: 'Accept all',
            acceptNecessaryBtn: 'Only necessary',
            savePreferencesBtn: 'Save my choice',
            closeIconLabel: 'Close',
            sections: [
              { title: 'Your choice', description: 'Choose what WUHA may load. Fonts, images and music files come from our own server.' },
              { title: 'Necessary', description: 'Stores your cookie choice. Always on.', linkedCategory: 'necessary' },
              { title: 'Statistics', description: 'Google Analytics counts visits and which songs and pages people like. IP addresses are shortened.', linkedCategory: 'analytics' },
              { title: 'Marketing', description: 'Meta Pixel and TikTok Pixel measure our ads, for example clicks to Spotify and newsletter sign-ups.', linkedCategory: 'marketing' },
              { title: 'External media', description: 'Plays Spotify and YouTube directly on this site. Without it, the players load only when you click play.', linkedCategory: 'media' },
              { title: 'More information', description: 'Questions? Write to <a href="mailto:contact@wuha.world">contact@wuha.world</a>. <a href="' + PRIVACY + '">Privacy policy</a>' }
            ]
          }
        }
      }
    }
  });
})();
