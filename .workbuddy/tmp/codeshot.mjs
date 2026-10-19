import puppeteer from 'puppeteer-core';
import path from 'node:path';
import fs from 'node:fs';

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const HTML = 'file:///E:/%E6%96%B0%E5%BB%BA%E6%96%87%E4%BB%B6%E5%A4%B9/exp2-vue/.workbuddy/tmp/codepage.html';
const OUT = 'E:\\新建文件夹\\exp2-vue\\.workbuddy\\tmp\\codeshots';
fs.mkdirSync(OUT, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: EDGE, headless: 'new',
  args: ['--no-first-run', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2']
});
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 800, deviceScaleFactor: 2 });
await page.goto(HTML, { waitUntil: 'networkidle0' });
console.log('url:', page.url());
console.log('title:', await page.title());
console.log('cards-dom:', await page.evaluate(() => document.querySelectorAll('.card').length));
console.log('ready:', await page.evaluate(() => window.__ready));
page.on('console', m => console.log('[console]', m.type(), m.text()));
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.waitForFunction('window.__ready === true');
const n = await page.$$eval('.card', els => els.length);
console.log('cards:', n);
for (let i = 0; i < n; i++) {
  const el = await page.$(`#c${i}`);
  await el.screenshot({ path: path.join(OUT, `code-${String(i + 1).padStart(2, '0')}.png`) });
  console.log('saved code-' + String(i + 1).padStart(2, '0'));
}
await browser.close();
console.log('done');
