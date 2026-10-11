// 브라우저 두 개(A = 관리자 PC, B = 담당자 PC)로 업무 분담 파일 주고받기를 실제로 시험
// · 파일 저장 창(showSaveFilePicker)만 가로채 내용을 받아 두고, 받는 쪽은 실제 파일 입력칸(DOM.setFileInputFiles)으로 연다
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const dir = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const [, , appFile, stepsFile] = process.argv;
const chrome = (process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome'));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const B = {};
async function launch(name, port) {
  const prof = path.join(dir, 'chrome-collab-' + name);
  fs.rmSync(prof, { recursive: true, force: true });
  const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--window-size=1460,900', '--allow-file-access-from-files', 'about:blank'], { stdio: 'ignore' });
  let url;
  for (let i = 0; i < 40 && !url; i++) { try { const j = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); url = j.find(x => x.type === 'page')?.webSocketDebuggerUrl; } catch (e) {} if (!url) await sleep(250); }
  const ws = new WebSocket(url); await new Promise(r => ws.onopen = r);
  const b = { name, proc, ws, id: 0, pend: new Map(), logs: [] };
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && b.pend.has(d.id)) { b.pend.get(d.id)(d); b.pend.delete(d.id); } if (d.method === 'Runtime.exceptionThrown') b.logs.push('EXC ' + d.params.exceptionDetails.exception?.description?.slice(0, 200)); if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') b.logs.push('ERR ' + d.params.args.map(a => a.value || a.description).join(' ').slice(0, 200)); };
  b.send = (method, params = {}) => new Promise(res => { const i = ++b.id; b.pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  b.ev = async expr => { const r = await b.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result?.exceptionDetails) return 'EXC: ' + (r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text); return r.result?.result?.value; };
  await b.send('Runtime.enable'); await b.send('Page.enable'); await b.send('DOM.enable');
  await b.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 810, deviceScaleFactor: 4 / 3, mobile: false });
  await b.send('Emulation.setFocusEmulationEnabled', { enabled: true });
  // 저장 창 가로채기 (실제 앱 코드는 그대로 실행)
  await b.send('Page.addScriptToEvaluateOnNewDocument', { source: `window.__saved=[];window.showSaveFilePicker=async(o)=>({createWritable:async()=>{const parts=[];return{write:async(x)=>{parts.push(x)},close:async()=>{const blob=new Blob(parts);window.__saved.push({name:o&&o.suggestedName,text:await blob.text()})}}}});` });
  await b.send('Page.navigate', { url: 'file:///' + appFile.replace(/\\\\/g, '/') });
  await sleep(4000);
  B[name] = b;
}
try {
  const steps = JSON.parse(fs.readFileSync(path.join(dir, stepsFile), 'utf8'));
  await launch('A', 9341); await launch('B', 9342); if (steps.some(s => s.b === 'C')) await launch('C', 9343);
  for (const s of steps) {
    const b = B[s.b];
    if (s.wait) await sleep(s.wait);
    if (s.js) console.log(`[${s.b}] ${s.label || ''} => ${await b.ev(s.js)}`);
    if (s.saveTo) {
      const v = await b.ev(`JSON.stringify(window.__saved[window.__saved.length-1]||null)`);
      const o = JSON.parse(v || 'null');
      if (!o) { console.log(`[${s.b}] 저장된 파일 없음`); continue; }
      fs.writeFileSync(path.join(dir, s.saveTo), o.text);
      console.log(`[${s.b}] 파일 저장됨: ${o.name} (${o.text.length}자) → ${s.saveTo}`);
    }
    if (s.setFile) {
      const doc = await b.send('DOM.getDocument', { depth: -1, pierce: true });
      const q = await b.send('DOM.querySelector', { nodeId: doc.result.root.nodeId, selector: s.setFile.sel });
      const r = await b.send('DOM.setFileInputFiles', { nodeId: q.result.nodeId, files: [path.join(dir, s.setFile.file)] });
      console.log(`[${s.b}] 파일 넣음: ${s.setFile.file} → ${s.setFile.sel} ${r.error ? 'ERR ' + r.error.message : 'ok'}`);
      await sleep(1500);
    }
    if (s.shot) { const r = await b.send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(dir, s.shot), Buffer.from(r.result.data, 'base64')); }
  }
  for (const k of Object.keys(B)) console.log(`LOGS ${k}:`, B[k].logs.slice(0, 10).join(' | '));
} finally { for (const k of Object.keys(B)) { try { B[k].ws.close(); } catch (e) {} B[k].proc.kill(); } }
