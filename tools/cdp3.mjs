// 크롬 헤드리스를 CDP로 조작해 새 업무 4단계·참고 자료 창·같은 이름 묻기를 확인
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const dir = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const file = process.argv[2];
const chrome = (process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome'));
const prof = path.join(dir, 'chrome-prof4');
fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn(chrome, ['--headless=new', '--remote-debugging-port=9338', `--user-data-dir=${prof}`, '--window-size=1460,900', '--allow-file-access-from-files', /* 헤드리스도 마우스 있는 화면으로 */ '--blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4', ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []), 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map(); const logs = [];
async function connect() {
  for (let i = 0; i < 40; i++) {
    try { const r = await fetch('http://127.0.0.1:9338/json'); const j = await r.json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {}
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
async function shot(name) { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(dir, name), Buffer.from(r.result.data, 'base64')); }
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } if (d.method === 'Runtime.exceptionThrown') logs.push('EXC ' + d.params.exceptionDetails.exception?.description); if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') logs.push('ERR ' + d.params.args.map(a => a.value || a.description).join(' ')); };
  await send('Runtime.enable'); await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 810, deviceScaleFactor: 4/3, mobile: false }); await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  await send('Page.navigate', { url: 'file:///' + file.replace(/\\/g, '/') });
  await sleep(4000);
  const steps = JSON.parse(fs.readFileSync(path.join(dir, 'steps3.json'), 'utf8'));
  for (const s of steps) {
    if (s.wait) await sleep(s.wait);
    if (s.viewport) { const [width, height, scale = 1] = s.viewport; await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: scale, mobile: false }); await sleep(600); }  // 작은 화면(노트북) 시험
    if (s.pt) { globalThis.__pt = JSON.parse(await ev(s.js)); continue; }
    if (s.clickpt) s.click = [...globalThis.__pt, s.clickpt];
    if (s.hoverpt) { const [x, y] = globalThis.__pt; await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await sleep(300); }
    if (s.rclickpt) { const [x, y] = globalThis.__pt; await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'right', clickCount: 1 }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'right', clickCount: 1 }); await sleep(400); }
    if (s.wheel) { const [x, y] = globalThis.__pt; await send('Input.dispatchMouseEvent', { type: 'mouseWheel', x, y, deltaX: 0, deltaY: s.wheel }); await sleep(250); }  // 마우스 휠
    if (s.text) { await send('Input.insertText', { text: s.text }); await sleep(200); }
    if (s.js) console.log('>', s.label || '', '=>', JSON.stringify(await ev(s.js)));
    if (s.click) { const [x, y, n = 1] = s.click; for (let k = 1; k <= n; k++) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: k }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: k }); await sleep(60); } await sleep(400); }
    if (s.key) { await send('Input.dispatchKeyEvent', { type: 'keyDown', key: s.key, code: s.key, windowsVirtualKeyCode: s.vk || 0, modifiers: s.mods || 0 }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: s.key, code: s.key, windowsVirtualKeyCode: s.vk || 0, modifiers: s.mods || 0 }); await sleep(300); }
    if (s.shot) await shot(s.shot);
  }
  console.log('LOGS:', logs.slice(0, 20).join('\n'));
} finally { try { ws?.close(); } catch (e) {} proc.kill(); }
