// Builds the social preview images (Open Graph, 1200x630) into source/og/.
// Run locally: node tools/make-og.js   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'source');
const OUT = path.join(SRC, 'og');
fs.mkdirSync(OUT, { recursive: true });

const url = (p) => 'file://' + path.join(SRC, p);
const songs = JSON.parse(fs.readFileSync(path.join(SRC, 'songs.json'), 'utf8'));

const base = `
@font-face{font-family:Anton;src:url(${url('fonts/anton-latin-400-normal.woff2')})}
@font-face{font-family:Inter;font-weight:500;src:url(${url('fonts/inter-latin-500-normal.woff2')})}
@font-face{font-family:Inter;font-weight:700;src:url(${url('fonts/inter-latin-700-normal.woff2')})}
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden;background:#0A0A0A;color:#F5F5F5;font-family:Inter,sans-serif}
.bg{position:absolute;inset:0;background:url(${url('img/wuha-hero-source.webp')}) center/cover}
.scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 2px,transparent 2px 4px);pointer-events:none}
.kick{font-weight:500;font-size:20px;letter-spacing:.45em;text-transform:uppercase;color:#9A9A9A}
.rule{width:120px;height:4px;background:#FF2E88;box-shadow:0 0 14px rgba(255,46,136,.9)}
.groove{font-weight:700;font-size:22px;letter-spacing:.5em;text-transform:uppercase}
.url{position:absolute;bottom:34px;font-weight:700;font-size:20px;letter-spacing:.3em;text-transform:uppercase;color:#FF2E88}
`;

function hero(kicker, sub) {
  return `<style>${base}
.v{position:absolute;inset:0;background:radial-gradient(ellipse 44% 70% at 50% 50%,rgba(10,10,10,.75),transparent 75%),linear-gradient(180deg,rgba(10,10,10,.2),rgba(10,10,10,.65))}
.c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px;text-align:center}
.c img{width:520px;filter:drop-shadow(0 0 30px rgba(0,0,0,.8))}
.sub{font-weight:500;font-size:22px;color:#D0D0D0;letter-spacing:.04em}
.url{left:0;right:0;text-align:center}
</style>
<div class="bg"></div><div class="v"></div><div class="scan"></div>
<div class="c"><div class="kick">${kicker}</div><img src="${url('press/logo/wuha-logo-scanline.svg')}"><div class="rule"></div><div class="groove">${sub}</div></div>
<div class="url">wuha.world</div>`;
}

function song(s) {
  return `<style>${base}
.bg{filter:blur(3px) brightness(.55);transform:scale(1.05)}
.v{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,10,10,.92) 0%,rgba(10,10,10,.75) 50%,rgba(10,10,10,.35) 100%)}
.l{position:absolute;left:70px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center;gap:22px}
.l img{width:220px}
h1{font-family:Anton,Impact,sans-serif;font-weight:400;text-transform:uppercase;font-size:${s.title.length > 18 ? 70 : 92}px;line-height:.95;letter-spacing:.01em}
.k{color:#FF2E88}
.cv{position:absolute;right:70px;top:65px;width:500px;height:500px;box-shadow:0 0 0 1px rgba(255,255,255,.08),0 30px 80px rgba(0,0,0,.7),0 0 60px rgba(255,46,136,.35)}
.url{left:70px}
</style>
<div class="bg"></div><div class="v"></div><div class="scan"></div>
<div class="l"><img src="${url('press/logo/wuha-logo-scanline.svg')}"><div class="kick k">${s.kicker}</div><h1>${s.title}</h1><div class="rule"></div><div class="groove" style="font-size:18px">Listen now</div></div>
<img class="cv" src="${url('press/covers/wuha-cover-' + s.slug + '.jpg')}">
<div class="url">wuha.world/${s.slug}</div>`;
}

const jobs = [
  ['og-home', hero('International Synthpop Act · Vienna', 'Feel the Groove')],
  ['og-press', hero('Press &amp; radio kit', 'Bio · Photos · Logo · Covers')],
  ['og-listen', hero('Listen now', 'Spotify · Apple Music · YouTube')],
  ['og-newsletter', hero('Newsletter', 'Feel the Groove')],
  ...songs.map((s) => ['og-' + s.slug, song(s)]),
];

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const [name, html] of jobs) {
    const f = path.join(OUT, name + '.html');
    fs.writeFileSync(f, '<!doctype html><meta charset="utf-8">' + html);
    await p.goto('file://' + f);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(OUT, name + '.jpg'), type: 'jpeg', quality: 86 });
    fs.unlinkSync(f);
    console.log(name);
  }
  await b.close();
})();
