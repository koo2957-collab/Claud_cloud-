import { spawn } from 'node:child_process'; import fs from 'node:fs'; import path from 'node:path';
const [, , file, outPrefix, timesArg] = process.argv;
const dir = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, '$1'));
const prof = path.join(dir, 'chrome-prof-vc'); fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn((process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome')), ['--headless=new', '--remote-debugging-port=9337', `--user-data-dir=${prof}`, '--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms)); let ws, id = 0; const pend = new Map();
async function connect() { for (let i = 0; i < 40; i++) { try { const j = await (await fetch('http://127.0.0.1:9337/json')).json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {} await sleep(250); } }
function send(m, p = {}) { return new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method: m, params: p })); }); }
async function ev(x) { const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true }); return r.result?.result?.value ?? JSON.stringify(r.result?.exceptionDetails); }
try {
  ws = new WebSocket(await connect()); await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  await send('Page.navigate', { url: 'file:///' + path.dirname(file) + '/' }); await sleep(800);
  const url = 'file:///' + file;
  console.log(await ev(`(async()=>{const v=document.createElement('video');v.src=${JSON.stringify(url)};document.body.appendChild(v);await new Promise((r,j)=>{v.onloadedmetadata=r;v.onerror=()=>j(v.error&&v.error.message)});
   const ab=await (await fetch(${JSON.stringify(url)})).arrayBuffer();const ac=new OfflineAudioContext(2,48000,48000);let info='';try{const b=await ac.decodeAudioData(ab);const d=b.getChannelData(0);const sec=[];for(let s=0;s<Math.floor(b.duration);s++){let q=0;for(let i=s*b.sampleRate;i<(s+1)*b.sampleRate;i++)q+=d[i]*d[i];sec.push(Math.round(10*Math.log10(q/b.sampleRate+1e-12)))}info='audio '+b.duration.toFixed(1)+'s ch'+b.numberOfChannels+' dB/s '+sec.join(',')}catch(e){info='audio decode fail '+e}
   return 'dur '+v.duration+' size '+v.videoWidth+'x'+v.videoHeight+' | '+info})()`));
  for (const t of (timesArg || '').split(',').filter(Boolean)) {
    const d = await ev(`(async()=>{const v=document.querySelector('video');v.currentTime=${t};await new Promise(r=>v.onseeked=r);const c=document.createElement('canvas');c.width=960;c.height=540;c.getContext('2d').drawImage(v,0,0,960,540);return c.toDataURL('image/jpeg',0.8).split(',')[1]})()`);
    fs.writeFileSync(`${outPrefix}_${t}.jpg`, Buffer.from(d, 'base64'));
  }
} finally { try { ws.close(); } catch (e) {} proc.kill(); }
