// 크롬 헤드리스를 CDP로 조작해 새 업무 4단계·참고 자료 창·같은 이름 묻기를 확인
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const dir = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const file = process.argv[2];
const chrome = (process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome'));
const prof = path.join(dir, 'chrome-prof2');
fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn(chrome, ['--headless=new', '--remote-debugging-port=9335', `--user-data-dir=${prof}`, '--window-size=1460,900', '--allow-file-access-from-files', /* 헤드리스도 마우스 있는 화면으로 */ '--blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4', ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []), 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map(); const logs = [];
async function connect() {
  for (let i = 0; i < 40; i++) {
    try { const r = await fetch('http://127.0.0.1:9335/json'); const j = await r.json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {}
    await sleep(250);
  }
  throw new Error('no chrome');
}
function send(method, params = {}) { return new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); }
async function ev(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) return 'EXC: ' + (r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text);
  return r.result?.result?.value;
}
async function shot(name) { const r = await send('Page.captureScreenshot', { format: 'png' }); const f = path.join(dir, name); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, Buffer.from(r.result.data, 'base64')); }
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } if (d.method === 'Runtime.exceptionThrown') logs.push('EXC ' + d.params.exceptionDetails.exception?.description); if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') logs.push('ERR ' + d.params.args.map(a => a.value || a.description).join(' ')); };
  await send('Runtime.enable'); await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 810, deviceScaleFactor: 4/3, mobile: false }); await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  await send('Page.navigate', { url: 'file:///' + file.replace(/\\/g, '/') });
  await sleep(4000);
  const steps = JSON.parse(fs.readFileSync(path.join(dir, 'steps.json'), 'utf8'));
  for (const s of steps) {
    if (s.wait) await sleep(s.wait);
    if (s.js) console.log('>', s.label || '', '=>', JSON.stringify(await ev(s.js)));
    // hover: [x,y]를 돌려주는 식 — 그 자리에 마우스를 올린 채 찍고, 찍은 뒤에는 마우스를 구석으로 치움
    if (s.hover) { const p = JSON.parse(await ev(s.hover)); await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: p[0], y: p[1] }); await sleep(300); }
    if (s.shot) await shot(s.shot);
    if (s.shot && s.hovered) await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 2, y: 2 });
  }
  console.log('LOGS:', logs.slice(0, 20).join('\n'));
} finally { try { ws?.close(); } catch (e) {} proc.kill(); }
