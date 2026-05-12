const fs = require('fs');

const html = fs.readFileSync('website/index.html', 'utf8');
const i18n = fs.readFileSync('website/js/i18n.js', 'utf8');
const htmlKeys = [...new Set([...html.matchAll(/data-i18n="([^"]+)"/g)].map(match => match[1]))];
let ok = true;

for (const lang of ['vi', 'zh', 'en', 'th']) {
  const start = i18n.indexOf(`  ${lang}: {`, i18n.indexOf('const T = {'));
  const next = ['vi', 'zh', 'en', 'th']
    .map(item => i18n.indexOf(`  ${item}: {`, start + 1))
    .filter(index => index > start)
    .sort((a, b) => a - b)[0] ?? i18n.indexOf('\n};', start);
  const keys = new Set([...i18n.slice(start, next).matchAll(/^    ([a-zA-Z0-9_]+):/gm)].map(match => match[1]));
  const missing = htmlKeys.filter(key => !keys.has(key));
  console.log(`${lang}: ${missing.length ? `missing ${missing.join(', ')}` : 'all keys present'}`);
  if (missing.length) ok = false;
}

process.exit(ok ? 0 : 1);
