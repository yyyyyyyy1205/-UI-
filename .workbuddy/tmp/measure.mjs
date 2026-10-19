import fs from 'node:fs';
const h = fs.readFileSync('E:/新建文件夹/exp2-vue/.workbuddy/tmp/codepage.html', 'utf8');
const start = h.indexOf('const snippets = [');
const end = h.indexOf('\n];', start);
const block = h.slice(start, end);
const re = /code:\n`([\s\S]*?)`\s*\}/g;
const w = l => [...l].reduce((a, c) => a + (c.charCodeAt(0) > 255 ? 1.9 : 1), 0);
let m, i = 0;
while ((m = re.exec(block))) {
  i++;
  const lines = m[1].split('\n');
  let mx = 0, ml = '';
  for (const l of lines) { const v = w(l); if (v > mx) { mx = v; ml = l; } }
  console.log(`snippet ${i}  maxW=${mx.toFixed(1)}  lines=${lines.length}`);
  console.log('   ', ml);
}
