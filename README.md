# wuha.world

Statische Website von WUHA.

- `source/design/` – Seiten aus dem Design-Entwurf (`.dc.html`)
- `source/img/`, `source/fonts/` – Bilder und Schriften (lokal, keine Google Fonts)
- `source/build.py` – baut die fertige Seite nach `site/`
- `.github/workflows/deploy.yml` – baut bei jeder Änderung auf `main` und lädt per FTPS ins Startverzeichnis des FTP-Benutzers (bei world4you `/2027/`, also www.wuha.world/2027/)

Das FTP-Passwort liegt nur als GitHub-Secret `FTP_PASSWORD`.

Lokal bauen: `pip install pillow && python source/build.py`
