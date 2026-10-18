// 사용 설명서 PDF 만들기 + 쪽 넘침 검사
//   node mk_manual_pdf.mjs [설명서 html] [--shots 폴더]
//   → 같은 폴더에 업무내비게이터_사용설명서.pdf, 넘친 쪽은 「넘침」 줄로 알림(종료 코드 1)
//   --shots: 쪽마다 PNG로도 찍음(눈으로 확인용)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';
const dir = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const args = process.argv.slice(2);
const si = args.indexOf('--shots');
const shotsDir = si >= 0 ? path.resolve(args[si + 1]) : null;
const file = path.resolve(args.find((a, i) => !a.startsWith('--') && (si < 0 || i !== si + 1)) || path.join(dir, '..', '사용설명서', '업무내비게이터_사용설명서.html'));
const chrome = process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome');
const port = await new Promise(r => { const s = net.createServer(); s.listen(0, () => { const p = s.address().port; s.close(() => r(p)); }); });
const prof = path.join(dir, 'chrome-prof-pdf-' + process.pid);
const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--allow-file-access-from-files', ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []), 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map();
async function connect() {
  for (let i = 0; i < 60; i++) {
    try { const j = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {}
    await sleep(250);
  }
  throw new Error('크롬에 붙지 못함');
}
const send = (method, params = {}) => new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async expr => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
let bad = 0;
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setEmulatedMedia', { media: 'print' });
  await send('Page.navigate', { url: 'file:///' + file.replace(/\\/g, '/') });
  await sleep(1500);
  // 사진을 모두 읽을 때까지
  await ev(`Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))`);
  const info = JSON.parse(await ev(`JSON.stringify([...document.querySelectorAll('.pg')].map((p, i) => { const b = p.querySelector('.pb'); const last = [...b.querySelectorAll('*')].reduce((m, e) => Math.max(m, e.getBoundingClientRect().bottom), 0); const br = b.getBoundingClientRect(); return { n: i + 1, id: p.id, over: Math.round(last - br.bottom), free: Math.round(br.bottom - last) }; }))`));
  const broken = await ev(`[...document.images].filter(i => !i.naturalWidth).map(i => i.src).join(' ')`);
  if (broken) { console.log('사진 없음', broken); bad++; }
  for (const p of info) if (p.over > 0) { console.log(`넘침 ${p.n}쪽 ${p.id} ${p.over}px`); bad++; }
  console.log('쪽', info.length, '· 남은 높이(px) 가장 적은 5쪽:', info.filter(p => p.over <= 0).sort((a, b) => a.free - b.free).slice(0, 5).map(p => `${p.n}쪽 ${p.free}`).join(', '));
  // 결과가 커서(사진 수십 장) 한 번에 받지 않고 나눠 받음
  const r = await send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false, transferMode: 'ReturnAsStream' });
  if (!r.result?.stream) throw new Error('PDF 만들기 실패 ' + JSON.stringify(r.error || r));
  const out = file.replace(/\.html$/i, '.pdf');
  const chunks = [];
  for (;;) {
    const c = (await send('IO.read', { handle: r.result.stream, size: 512 << 10 })).result;
    chunks.push(Buffer.from(c.data, c.base64Encoded ? 'base64' : 'binary'));
    if (c.eof) break;
  }
  await send('IO.close', { handle: r.result.stream });
  fs.writeFileSync(out, Buffer.concat(chunks));
  console.log('PDF', out, Math.round(fs.statSync(out).size / 1024) + 'KB');
  if (shotsDir) {
    fs.mkdirSync(shotsDir, { recursive: true });
    await send('Emulation.setDeviceMetricsOverride', { width: 900, height: 1200, deviceScaleFactor: 1, mobile: false });
    const rects = JSON.parse(await ev(`JSON.stringify([...document.querySelectorAll('.pg')].map(p => { const r = p.getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height]; }))`));
    for (let i = 0; i < rects.length; i++) {
      const [x, y, w, h] = rects[i];
      const s = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x, y, width: w, height: h, scale: 1 } });
      fs.writeFileSync(path.join(shotsDir, `p${String(i + 1).padStart(2, '0')}.png`), Buffer.from(s.result.data, 'base64'));
    }
    console.log('쪽 사진', rects.length, shotsDir);
  }
} finally { try { ws?.close(); } catch (e) {} proc.kill(); await sleep(500); try { fs.rmSync(prof, { recursive: true, force: true }); } catch (e) {} }
process.exit(bad ? 1 : 0);
