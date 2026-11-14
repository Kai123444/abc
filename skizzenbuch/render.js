// Erzeugt skizzenbuch.pdf aus skizzenbuch.html (node render.js [--shots DIR])
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'skizzenbuch.html'));
  const over = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
    const foot = p.querySelector('.foot, .blankfoot');
    const limit = foot ? foot.getBoundingClientRect().top : p.getBoundingClientRect().bottom;
    let max = 0;
    p.querySelectorAll(':scope > *:not(.foot):not(.blankfoot)').forEach(c => { max = Math.max(max, c.getBoundingClientRect().bottom); });
    return max > limit + 1 ? `Seite ${i + 1}: ${Math.round(max - limit)}px zu lang` : null;
  }).filter(Boolean));
  if (over.length) console.log('ÜBERLAUF:\n' + over.join('\n')); else console.log('kein Überlauf');
  await page.pdf({ path: path.join(__dirname, 'skizzenbuch.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  const i = process.argv.indexOf('--shots');
  if (i > 0) {
    const dir = process.argv[i + 1];
    const n = await page.locator('.page').count();
    for (let k = 0; k < n; k++) await page.locator('.page').nth(k).screenshot({ path: `${dir}/p${String(k + 1).padStart(2, '0')}.png` });
  }
  await browser.close();
})();
