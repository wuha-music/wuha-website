# Builds the press kit PDFs (EN + DE, full kit and one sheet per song) into source/press/pdf/.
# Text comes from source/presskit/{en,de}/*.md (exported from the WUHA press kit docs).
# Run locally: python3 tools/make-presskit.py   (needs `pip install markdown`, Node + Playwright)
import os, re, json, subprocess, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'source')
KIT = os.path.join(SRC, 'presskit')
OUT = os.path.join(SRC, 'press', 'pdf')
TMP = os.path.join(ROOT, 'tools', '.presskit-tmp')
STAMP = '2026-11'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
U = lambda p: 'file://' + os.path.join(SRC, p)

SONGS = [('s1', 'losing-my-shape', 'Losing-My-Shape'), ('s2', 'nothing-is-forever', 'Nothing-Is-Forever'),
         ('s3', 'rainbow-eyes', 'Rainbow-Eyes'), ('s4', 'caroline', 'Caroline')]

L = {
    'en': dict(kit='Press Kit', file='WUHA_PressKit_EN', sheet='WUHA_SongSheet_EN', sub='Synthpop from Vienna · Feel the Groove',
               asof='As of November 2026', parts=['Overview', 'Radio', 'TV', 'Print & Online', 'Songs'], songsheet='Song sheet',
               dl='Photos, logo and covers: www.wuha.world/press/ · Free to use with the credit “WUHA”. Audio (WAV + MP3) on request at contact@wuha.world'),
    'de': dict(kit='Pressekit', file='WUHA_Pressekit_DE', sheet='WUHA_Songblatt_DE', sub='Synthpop aus Wien · Feel the Groove',
               asof='Stand: November 2026', parts=['Übersicht', 'Radio', 'TV', 'Print & Online', 'Songs'], songsheet='Songblatt',
               dl='Fotos, Logo und Cover: www.wuha.world/press/ · Abdruck honorarfrei mit Credit „WUHA“. Audio (WAV + MP3) auf Anfrage an contact@wuha.world'),
}

DROP = ['Still to fill in', 'Vor dem Versand ausfüllen', 'Quotes (drafts', 'Zitate (Vorschläge']


def clean(md, lang):
    # drop internal sections (drafts, to-do lists)
    parts = re.split(r'(?m)^(?=## )', md)
    parts = [p for p in parts if not any(p.startswith('## ' + d) for d in DROP)]
    md = ''.join(parts)
    md = re.sub(r'(?m)^Note: these quotes.*\n|^Hinweis: Diese Zitate.*\n', '', md)
    # table rows with open placeholders like [LENGTH] / [BPM] / [please confirm]
    out = []
    for line in md.split('\n'):
        if line.startswith('|') and re.search(r'\\\[', line):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(re.fullmatch(r'\\\[.*\\\]', c) for c in cells[1:]):
                continue
            line = '| ' + ' | '.join('–' if re.fullmatch(r'\\\[.*\\\]', c) else c for c in cells) + ' |'
        out.append(line)
    md = '\n'.join(out)
    rep = [
        (r'Vienna, \\\[DATE\\\] – ', 'Vienna – '), (r'Wien, \\\[DATUM\\\] – ', 'Wien – '),
        (r': \\\[LIVE / PLAYBACK / ACOUSTIC – to be confirmed\\\]', ''), (r': \\\[LIVE / PLAYBACK / AKUSTIK – bitte klären\\\]', ''),
        (r' \\\[please confirm\\\]', ''), (r' \\\[bitte bestätigen\\\]', ''),
        (r'\\\[SONG TITLE\\\]', 'song title'), (r'\\\[SONGTITEL\\\]', 'Songtitel'),
        (r' Alles in \\\[eckigen Klammern\\\] vor dem Versand ausfüllen\.', ''),
        (r'\(here\)', ''), (r'\(hier\)', ''),
        ('in the song tabs under “Songs”', 'on the song sheets'), ('in the song tabs', 'on the song sheets'),
        ('in den Song-Tabs unter „Songs“', 'auf den Songblättern'), ('in den Song-Tabs', 'auf den Songblättern'),
        (r'Black-and-white press photos on request at contact@wuha\.world', 'Press photos: www.wuha.world/press/'),
        (r'Pressefotos in Schwarz-Weiß auf Anfrage an contact@wuha\.world', 'Pressefotos: www.wuha.world/press/'),
        (r'As of Nov 20, 2026', L['en']['asof']), (r'Stand: Nov 20, 2026', L['de']['asof']),
        (r'WUHA · Wien, Österreich E-Mail: (\S+) Web: (\S+) Ansprechpartner Presse/Radio/TV: ', r'WUHA · Wien, Österreich · \1 · \2\n\nPresse, Radio und TV: '),
        (r'WUHA – Synthpop aus Wien Wolfgang Laab – Gesang, Gitarre Andreas', 'WUHA – Synthpop aus Wien\n\nWolfgang Laab – Gesang, Gitarre\n\nAndreas'),
    ]
    for a, b in rep:
        md = re.sub(a, b, md)
    # "press material on request" list → download link
    md = re.sub(r'(## Press material\n\n)On request at contact@wuha\.world:\n\n(?:- .*\n)+', r'\1' + L['en']['dl'] + '\n', md)
    md = re.sub(r'(## Pressematerial\n\n)Auf Anfrage an contact@wuha\.world:\n\n(?:- .*\n)+', r'\1' + L['de']['dl'] + '\n', md)
    md = md.replace('\\_', '_')
    return md


def html(md):
    h = markdown.markdown(md, extensions=['tables'])
    h = re.sub(r'(https?://[^\s<·]+)', r'<a href="\1">\1</a>', h)
    h = re.sub(r'(?<![/\w.])(www\.wuha\.world[^\s<·,)]*)', r'<a href="https://\1">\1</a>', h)
    h = re.sub(r'(?<![\w.])(contact@wuha\.world)', r'<a href="mailto:\1">\1</a>', h)
    return h


CSS = f'''
@font-face{{font-family:Anton;src:url({U('fonts/anton-latin-400-normal.woff2')})}}
@font-face{{font-family:Inter;font-weight:400;src:url({U('fonts/inter-latin-400-normal.woff2')})}}
@font-face{{font-family:Inter;font-weight:600;src:url({U('fonts/inter-latin-600-normal.woff2')})}}
@font-face{{font-family:Inter;font-weight:700;src:url({U('fonts/inter-latin-700-normal.woff2')})}}
@page{{size:A4;margin:16mm 16mm 16mm}}
@page cover{{margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Inter,sans-serif;font-size:9.4pt;line-height:1.48;color:#1A1A1A}}
a{{color:#C4146A;text-decoration:none}}
h1{{font-family:Anton,Impact,sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.02em;font-size:30pt;line-height:1;margin:0 0 4mm}}
h1::after{{content:"";display:block;width:22mm;height:1.2mm;background:#FF2E88;margin-top:4mm}}
h2{{font-family:Inter;font-weight:700;font-size:8pt;letter-spacing:.32em;text-transform:uppercase;color:#C4146A;margin:6mm 0 2mm;break-after:avoid}}
p{{margin:0 0 3mm}} ul,ol{{margin:0 0 3mm;padding-left:5mm}} li{{margin-bottom:1.5mm}}
strong{{font-weight:700}}
table{{width:100%;border-collapse:collapse;margin:0 0 3mm;font-size:9.5pt;break-inside:avoid}}
th,td{{text-align:left;vertical-align:top;padding:1.8mm 3mm 1.8mm 0;border-bottom:.3mm solid #E2E2E2}}
td:first-child{{color:#6A6A6A;width:32%}} thead th{{font-size:8pt;color:#6A6A6A;font-weight:600}}
thead tr:first-child th:empty{{border:0}}
.sec{{break-before:page}}
.cover{{page:cover;position:relative;width:210mm;height:297mm;background:#0A0A0A;color:#F5F5F5;overflow:hidden}}
.cover .bg{{position:absolute;left:0;top:0;width:100%;height:64%;object-fit:cover;object-position:center 30%;filter:grayscale(1) contrast(1.15) brightness(.85)}}
.cover .v{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,0) 35%,#0A0A0A 64%)}}
.cover .c{{position:absolute;left:18mm;right:18mm;bottom:24mm}}
.cover .lg{{width:95mm;display:block;margin-bottom:9mm}}
.cover .k{{font-weight:700;font-size:9pt;letter-spacing:.45em;text-transform:uppercase;color:#FF2E88;margin-bottom:3mm}}
.cover .t{{font-family:Anton;font-size:46pt;line-height:.95;text-transform:uppercase;letter-spacing:.02em}}
.cover .r{{width:26mm;height:1.4mm;background:#FF2E88;box-shadow:0 0 4mm rgba(255,46,136,.9);margin:7mm 0}}
.cover .s{{font-size:11pt;color:#D0D0D0}} .cover .m{{font-size:9pt;color:#9A9A9A;margin-top:12mm;letter-spacing:.08em}}
.cover .toc{{font-size:9pt;color:#BDBDBD;margin-top:3mm;letter-spacing:.06em}}
.song{{display:flex;gap:6mm;align-items:flex-end;margin-bottom:3mm}} .sheet{{font-size:9pt;line-height:1.42}} .sheet td,.sheet th{{padding:1.2mm 3mm 1.2mm 0}} .sheet h2{{margin:4.5mm 0 1.5mm}}
.song img{{width:34mm;height:34mm;object-fit:cover;display:block}}
.song .k{{font-weight:700;font-size:8pt;letter-spacing:.32em;text-transform:uppercase;color:#C4146A;margin-bottom:2mm}}
.song h1{{font-size:26pt}}
'''


def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


def strip_h1(h):
    return re.sub(r'^<h1>.*?</h1>\s*', '', h, count=1, flags=re.S)


jobs = []
for lang, c in L.items():
    d = os.path.join(KIT, lang)
    rd = lambda n: clean(open(os.path.join(d, n + '.md'), encoding='utf-8').read(), lang)
    cover = (f'<section class="cover"><img class="bg" src="{U('press/photos/wuha-band-bw.jpg')}" alt=""><div class="v"></div><div class="c">'
             f'<img class="lg" src="{U("press/logo/wuha-logo-scanline.svg")}" alt="WUHA">'
             f'<div class="k">{c["sub"].split(" · ")[0]}</div><div class="t">{c["kit"]}</div><div class="r"></div>'
             f'<div class="s">Feel the Groove</div><div class="toc">{" · ".join(c["parts"])}</div>'
             f'<div class="m">{c["asof"]} · www.wuha.world · contact@wuha.world</div></div></section>')
    secs = []
    first = html(rd('1'))
    secs.append('<section class="sec">' + first + '</section>')
    for n in ['2', '3', '4']:
        secs.append('<section class="sec">' + html(rd(n)) + '</section>')
    sheets = []
    for key, slug, nice in SONGS:
        h = html(rd(key))
        title = re.search(r'<h1>(.*?)</h1>', h, re.S).group(1)
        title = re.sub(r'^WUHA – ', '', title)
        head = (f'<div class="song"><img src="{U("press/covers/wuha-cover-" + slug + ".jpg")}" alt="">'
                f'<div><div class="k">WUHA · {c["songsheet"]}</div><h1>{title}</h1></div></div>')
        body = head + strip_h1(h)
        sheets.append('<section class="sec sheet">' + body + '</section>')
        jobs.append([f'{c["sheet"]}_{nice}_{STAMP}.pdf', page('<div class="sheet">' + body + '</div>')])
    jobs.append([f'{c["file"]}_{STAMP}.pdf', page(cover + ''.join(secs) + ''.join(sheets))])

for i, (name, doc) in enumerate(jobs):
    f = os.path.join(TMP, f'{i}.html')
    open(f, 'w', encoding='utf-8').write(doc)
    jobs[i] = [f, os.path.join(OUT, name)]

for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))
subprocess.run(['node', os.path.join(ROOT, 'tools', 'print-pdf.js'), json.dumps(jobs)], check=True)
for f, _ in jobs:
    os.remove(f)
os.rmdir(TMP)
