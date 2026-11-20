# wuha.world

Statische Website von WUHA.

- `source/design/` – Seiten aus dem Design-Entwurf (`.dc.html`)
- `source/img/`, `source/fonts/` – Bilder und Schriften (lokal, keine Google Fonts)
- `source/build.py` – baut die fertige Seite nach `site/`
- `.github/workflows/deploy.yml` – baut bei jeder Änderung auf `main` und lädt per FTPS nach `2027/` bei world4you (www.wuha.world/2027/)

Das FTP-Passwort liegt nur als GitHub-Secret `FTP_PASSWORD`.

Lokal bauen: `pip install pillow && python source/build.py`

## Newsletter

`wordpress-plugin/wuha-subscribe.php` wird nach `wp-content/plugins/wuha-subscribe/` im WordPress hochgeladen und dort unter **Plugins** aktiviert.
Das Formular schickt die Anmeldung an `https://www.wuha.world/wp-admin/admin-ajax.php` (Aktion `wuha_subscribe`).
Das Plugin sucht die MailPoet-Listen über ihren Namen ("English" / "Deutsch"), trägt die Adresse ein und MailPoet schickt die Bestätigungsmail (Doppel-Opt-in).
Schutz: nur von wuha.world, unsichtbares Bot-Feld, max. 5 Anmeldungen pro IP und Stunde.

## Messung (für Meta, TikTok, Google über den Tag Manager)

Die Seite schreibt Ereignisse in `dataLayer`: `spotify_click`, `newsletter_button`, `newsletter_signup`, `listen_button`, `press_download`. Seitenaufrufe zählt der Tag Manager selbst. Geladen wird er erst nach Zustimmung im Cookie-Banner (noch offen).
