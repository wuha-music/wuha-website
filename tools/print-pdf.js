// Prints local HTML files to A4 PDFs with a small WUHA footer. Used by tools/make-presskit.py.
const { chromium } = require('playwright');
const jobs = JSON.parse(process.argv[2]);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [src, out] of jobs) {
    await p.goto('file://' + src);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.pdf({
      path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: '<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7px;letter-spacing:.2em;color:#9A9A9A;padding:0 18mm;display:flex;justify-content:space-between"><span>WUHA · WWW.WUHA.WORLD · CONTACT@WUHA.WORLD</span><span class="pageNumber"></span></div>',
    });
    console.log(out.split('/').pop());
  }
  await b.close();
})();
