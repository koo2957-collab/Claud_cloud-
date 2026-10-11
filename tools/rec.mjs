// 크롬(헤드리스)으로 video.html을 실제 시간대로 재생하며 캔버스를 녹화 → WebM 파일로 저장
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const dir = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, '$1'));
const [, , pageFile, outFile] = process.argv;
const chrome = (process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome'));
const prof = path.join(dir, 'chrome-prof-rec');
fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn(chrome, ['--headless=new', '--remote-debugging-port=9334', `--user-data-dir=${prof}`, '--window-size=1400,900',
  '--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling', '--disable-renderer-backgrounding', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map();
async function connect() {
  for (let i = 0; i < 40; i++) {
    try { const r = await fetch('http://127.0.0.1:9334/json'); const j = await r.json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {}
    await sleep(250);
  }
  throw new Error('no chrome');
}
function send(method, params = {}) { return new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); }
async function ev(expr) { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); return r.result?.result?.value; }
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  await send('Page.navigate', { url: 'file:///' + pageFile.replace(/\\/g, '/') });
  const total = 600;
  for (let s = 0; s < total; s += 5) {
    await sleep(5000);
    const st = await ev('JSON.stringify({d:!!window.__done,p:window.__prog,e:window.__err||""})');
    const o = JSON.parse(st || '{}');
    process.stdout.write(`${o.p ?? '?'}% `);
    if (o.d) { if (o.e) throw new Error(o.e); break; }
  }
  const len = await ev('window.__b64 ? window.__b64.length : 0');
  if (!len) throw new Error('no video data');
  const parts = [];
  for (let off = 0; off < len; off += 1500000) parts.push(await ev(`window.__b64.slice(${off}, ${off + 1500000})`));
  fs.writeFileSync(outFile, Buffer.from(parts.join(''), 'base64'));
  console.log('\nsaved', outFile, fs.statSync(outFile).size, 'bytes');
} catch (e) { console.log('\nERR', e.message); }
finally { try { ws.close(); } catch (e) {} proc.kill(); }
