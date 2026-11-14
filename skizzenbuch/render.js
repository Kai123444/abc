// Erzeugt die PDFs aus den HTML-Dateien (node render.js [--shots DIR])
const { chromium } = require('playwright');
const path = require('path');
async function one(browser, name, shots) {
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, name + '.html'));
  const over = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
    const foot = p.querySelector('.foot, .blankfoot');
    const limit = foot ? foot.getBoundingClientRect().top : p.getBoundingClientRect().bottom;
    let max = 0;
    p.querySelectorAll(':scope > *:not(.foot):not(.blankfoot)').forEach(c => { max = Math.max(max, c.getBoundingClientRect().bottom); });
    return max > limit + 1 ? `Seite ${i + 1}: ${Math.round(max - limit)}px zu lang` : null;
  }).filter(Boolean));
  if (over.length) console.log(name + ' ÜBERLAUF:\n' + over.join('\n')); else console.log(name + ': kein Überlauf');
  await page.pdf({ path: path.join(__dirname, name + '.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (shots) {
    const dir = shots;
    const n = await page.locator('.page').count();
    for (let k = 0; k < n; k++) await page.locator('.page').nth(k).screenshot({ path: `${dir}/p${String(k + 1).padStart(2, '0')}.png` });
  }
  await page.close();
}
(async () => {
  const browser = await chromium.launch();
  const i = process.argv.indexOf('--shots');
  await one(browser, 'skizzenbuch_beidseitig', i > 0 ? process.argv[i + 1] : null);
  await one(browser, 'skizzenbuch_einseitig', null);
  await browser.close();
})();
