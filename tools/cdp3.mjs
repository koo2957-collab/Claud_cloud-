// 크롬 헤드리스를 CDP로 조작해 새 업무 4단계·참고 자료 창·같은 이름 묻기를 확인
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const dir = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const file = process.argv[2];
const chrome = (process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome'));
import net from 'node:net';
// CDP_PORT=auto: 비어 있는 포트를 새로 고름 (여러 개 동시에·연달아 돌릴 때 앞 시험의 꺼지는 중인 크롬에 붙지 않게)
const freePort = () => new Promise(r => { const sv = net.createServer(); sv.listen(0, '127.0.0.1', () => { const p = sv.address().port; sv.close(() => r(p)); }); });
const PORT = process.env.CDP_PORT === 'auto' ? await freePort() : Number(process.env.CDP_PORT || 9338);
const prof = path.join(dir, process.env.CDP_PROF ? `${process.env.CDP_PROF}-${process.pid}` : 'chrome-prof4');  // 여러 개 동시에 돌릴 때는 실행마다 따로
const SC = process.env.SELFCHECK ? fs.readFileSync(path.join(dir, 'selfcheck.js'), 'utf8') : null;  // 단계마다 「서로 맞아야 하는 것」 검사
const STEPS = process.env.STEPS || 'steps3.json';
const W0 = Number(process.env.VW || 1440), H0 = Number(process.env.VH || 810);
let curLabel = '';
fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`, '--window-size=1460,900', '--allow-file-access-from-files', /* 헤드리스도 마우스 있는 화면으로 */ '--blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4', ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []), 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map(); const logs = [];
async function connect() {
  for (let i = 0; i < 160; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json`); const j = await r.json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {}
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
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } if (d.method === 'Runtime.exceptionThrown') logs.push('EXC [' + curLabel + '] ' + (d.params.exceptionDetails.exception?.description || '').split(String.fromCharCode(10))[0]); if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') logs.push('ERR [' + curLabel + '] ' + d.params.args.map(a => a.value || a.description).join(' ')); };
  await send('Runtime.enable'); await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: W0, height: H0, deviceScaleFactor: 4/3, mobile: false }); await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  await send('Page.navigate', { url: 'file:///' + file.replace(/\\/g, '/') });
  await sleep(1500);
  const ready = async () => { for (let k = 0; k < 60; k++) { if (await ev("typeof app!=='undefined'&&!!app&&!!app.allData&&app._dataLoaded===true&&document.readyState==='complete'") === true) return; await sleep(500); } };  // 프로그램이 다 켜질 때까지 (컴퓨터가 바쁘면 4초로 모자랐다)
  await ready(); await sleep(2500);  // 켜진 직후 하는 일(마감 알림·다시 그리기)이 끝나도록
  if (process.env.DARK) await ev("localStorage.setItem('darkMode','true');document.documentElement.classList.add('dark-mode')");  // 다크 모드로 시험
  const steps = JSON.parse(fs.readFileSync(path.join(dir, STEPS), 'utf8'));
  for (const s of steps) {
    if (s.label) curLabel = s.label;
    if (s.wait) await sleep(s.wait);
    if (s.reload) { await send('Page.reload', { ignoreCache: true }); await sleep(1500); await ready(); await sleep(2500); }  // 새로 고침(다시 켜기)
    if (s.dark) await ev("document.documentElement.classList.add('dark-mode')");
    if (s.viewport) { const [width, height, scale = 1] = s.viewport; await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: scale, mobile: false }); await sleep(600); }  // 작은 화면(노트북) 시험
    if (s.pt) { const v = await ev(s.js); try { globalThis.__pt = JSON.parse(v); } catch (e) { console.log('>', curLabel + ' (누를 곳 찾기)', '=>', JSON.stringify('ERR 누를 곳을 못 찾음: ' + String(v).slice(0, 150))); globalThis.__pt = [2, 2]; } continue; }
    if (s.clickpt) s.click = [...globalThis.__pt, s.clickpt];
    if (s.hoverpt) { const [x, y] = globalThis.__pt; await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await sleep(300); }
    if (s.rclickpt) { const [x, y] = globalThis.__pt; await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'right', clickCount: 1 }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'right', clickCount: 1 }); await sleep(400); }
    if (s.wheel) { const [x, y] = globalThis.__pt; await send('Input.dispatchMouseEvent', { type: 'mouseWheel', x, y, deltaX: 0, deltaY: s.wheel, modifiers: s.mods || 0 }); await sleep(250); }  // 마우스 휠 (mods: Ctrl=2)
    if (s.drag) { const [x, y] = globalThis.__pt, [dx, dy] = s.drag; await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); for (let k = 1; k <= 8; k++) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x + dx * k / 8, y: y + dy * k / 8, button: 'left', buttons: 1 }); await sleep(20); } await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: x + dx, y: y + dy, button: 'left', clickCount: 1 }); await sleep(300); }  // 끌기 [dx, dy]
    if (s.text) { await send('Input.insertText', { text: s.text }); await sleep(200); }
    if (s.js && s.save) { const v = await ev(s.js); fs.writeFileSync(path.resolve(dir, s.save), typeof v === 'string' ? v : JSON.stringify(v)); console.log('>', s.label || '', '=> 저장', s.save, (typeof v === 'string' ? v.length : 0) + '자'); continue; }  // 돌려받은 글을 파일로 (연습 업무 파일 만들기 등)
    if (s.js) console.log('>', s.label || '', '=>', JSON.stringify(await ev(s.js)));
    if (s.js && SC && !s.nocheck && !/^정리/.test(s.label || '')) { let r = await ev(SC); if (r && r.e && r.e.length === 1 && /준비되지 않음/.test(r.e[0])) { await ready(); await sleep(2500); r = await ev(SC); } /* 시험이 스스로 새로 고친 직후면 켜질 때까지 */ if (r && r.e && r.e.length) console.log('SELFCHECK', s.label || '', '=>', JSON.stringify(r.e)); else if (r && typeof r === 'string') console.log('SELFCHECK', s.label || '', '=>', JSON.stringify(r)); }
    if (s.click) { const [x, y, n = 1] = s.click; for (let k = 1; k <= n; k++) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: k }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: k }); await sleep(60); } await sleep(400); }
    if (s.key) { await send('Input.dispatchKeyEvent', { type: 'keyDown', key: s.key, code: s.key, windowsVirtualKeyCode: s.vk || 0, modifiers: s.mods || 0, ...(s.ktext ? { text: s.ktext, unmodifiedText: s.ktext } : {}) });  /* ktext: 실제 키처럼 글자도 넣기 (예: Enter → '
') */ await send('Input.dispatchKeyEvent', { type: 'keyUp', key: s.key, code: s.key, windowsVirtualKeyCode: s.vk || 0, modifiers: s.mods || 0 }); await sleep(300); }
    if (s.shot) await shot(s.shot);
  }
  console.log('LOGS:', logs.slice(0, 20).join('\n'));
} finally { try { ws?.close(); } catch (e) {} proc.kill(); if (process.env.CDP_PROF) { await sleep(1500); try { fs.rmSync(prof, { recursive: true, force: true }); } catch (e) {} } }
