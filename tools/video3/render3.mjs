// 헤드리스 크롬으로 페이지를 열고 window.__b64(만든 파일)를 받아 저장 — 배경음악 합성용
// 실행: node render3.mjs <페이지.html> <저장 파일>
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const [, , page, out] = process.argv;
const chrome = process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome');
const prof = path.resolve(path.dirname(out), 'chrome-prof-render');
fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn(chrome, ['--headless=new', '--remote-debugging-port=9338', `--user-data-dir=${prof}`, '--allow-file-access-from-files', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map();
const send = (method, params = {}) => new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async e => (await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result?.result?.value;
try {
  for (let i = 0; i < 60 && !ws; i++) { try { const j = await (await fetch('http://127.0.0.1:9338/json')).json(); const p = j.find(x => x.type === 'page'); if (p) { ws = new WebSocket(p.webSocketDebuggerUrl); break; } } catch (e) {} await sleep(250); }
  if (!ws) throw new Error('크롬 연결 안 됨');
  if (ws.readyState !== 1) await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  await send('Page.enable'); await send('Page.navigate', { url: 'file:///' + path.resolve(page).replace(/\\/g, '/') });
  for (let i = 0; i < 600; i++) { await sleep(500); if (await ev('!!window.__done')) break; }
  const err = await ev('window.__err||""'); if (err) throw new Error(err);
  const len = await ev('window.__b64.length'); const parts = [];
  for (let off = 0; off < len; off += 2000000) parts.push(await ev(`window.__b64.slice(${off},${off + 2000000})`));
  fs.writeFileSync(out, Buffer.from(parts.join(''), 'base64'));
  console.log('저장', out, (fs.statSync(out).size / 1e6).toFixed(1), 'MB');
} catch (e) { console.log('ERR', e.message); }
finally { try { ws.close(); } catch (e) {} proc.kill(); }
