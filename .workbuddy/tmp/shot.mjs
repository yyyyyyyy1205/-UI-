import puppeteer from 'puppeteer-core';
import fs from 'node:fs';

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const BASE = 'http://127.0.0.1:5173';
const OUT = 'E:\\新建文件夹\\exp2-vue\\.workbuddy\\tmp\\shots';
fs.mkdirSync(OUT, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: EDGE,
  headless: 'new',
  args: ['--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--disable-gpu']
});
const page = await browser.newPage();
await page.setViewport({ width: 1180, height: 900, deviceScaleFactor: 2 });

const shot = async (path, name) => {
  await page.goto(BASE + path, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 900));
  await page.screenshot({ path: `${OUT}\\${name}.png`, fullPage: true });
  console.log('shot', name, page.url());
};

// 先建立登录态（localStorage 同源共享）
await page.goto(BASE + '/login', { waitUntil: 'networkidle0' });
await page.evaluate(() => localStorage.setItem('isLogin', 'true'));

await shot('/home', '01-home');
await shot('/about', '02-about');
await shot('/project/list', '03-project-list');
await shot('/project/detail/1', '04-project-detail-1');
await shot('/login', '05-login');
await shot('/admin/profile', '06-admin-profile');
await shot('/admin', '07-admin-redirect');
await shot('/not-exist-page', '08-404');
await shot('/', '09-redirect-root');

// 退出登录后再访问后台，验证守卫拦截
await page.goto(BASE + '/login', { waitUntil: 'networkidle0' });
await page.evaluate(() => localStorage.removeItem('isLogin'));
await page.goto(BASE + '/admin/profile', { waitUntil: 'networkidle0' });
await new Promise(r => setTimeout(r, 800));
await page.screenshot({ path: `${OUT}\\10-guard-redirect.png`, fullPage: true });
console.log('shot 10-guard-redirect', page.url());

await browser.close();
console.log('done');
