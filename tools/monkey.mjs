// 무작위 사용자 시험 실행기
// node monkey.mjs <앱 경로> [씨앗=1] [동작 수=500] [ai]
//   동작마다: 검사기(selfcheck.js) · 페이지 오류 · (되돌린 동작이면) 하기 전과 같은지
//   150동작마다: 새로 고침 → 저장된 자료가 그대로인지 (__canon 비교)
//   결과: monkey_<씨앗>[_ai].json · 실패 화면 monkey_fail_*.png · 끝에 요약 줄 「MONKEY 결과 …」
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const dir = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const file = process.argv[2];
const SEED = Number(process.argv[3] || 1), N = Number(process.argv[4] || 500), AI = process.argv[5] === 'ai';
const TAG = `${SEED}${AI ? '_ai' : ''}`;
const PORT = Number(process.env.CDP_PORT || (9380 + (SEED % 19)));
const chrome = (process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome'));
const prof = path.join(dir, `chrome-monkey-${TAG}`);
fs.rmSync(prof, { recursive: true, force: true });
const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`, '--window-size=1460,900', '--allow-file-access-from-files', '--blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map(); let pageErrs = [];
const SC = fs.readFileSync(path.join(dir, 'selfcheck.js'), 'utf8');
const CANON = fs.readFileSync(path.join(dir, 'canon.js'), 'utf8');
const MONKEY = fs.readFileSync(path.join(dir, 'monkey_page.js'), 'utf8');
async function connect() { for (let i = 0; i < 160; i++) { try { const j = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); const pg = j.find(x => x.type === 'page'); if (pg) return pg.webSocketDebuggerUrl; } catch (e) {} await sleep(250); } throw new Error('no chrome'); }
function send(method, params = {}) { return new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); }
async function ev(expr, ms = 60000) {
  const r = await Promise.race([send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }), sleep(ms).then(() => ({ timeout: true }))]);
  if (r.timeout) return { __timeout: true };
  if (r.result?.exceptionDetails) return { __exc: (r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text || '').split('\n')[0] };
  return r.result?.result?.value;
}
async function shot(name) { const r = await send('Page.captureScreenshot', { format: 'png' }); if (r.result) fs.writeFileSync(path.join(dir, name), Buffer.from(r.result.data, 'base64')); }
const STUB = AI ? ("app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
  + "const mk=t=>/items/.test(t)?JSON.stringify({items:[{text:'준비',indent:0,from:['o0'],change:'유지',warn:[],tip:'',basis:[]},{text:'확인',indent:1,from:['o1'],change:'수정',warn:['기한 확인'],tip:'팁',basis:['시행령 제1조']}],removed:[],branches:[]}):'답: 이 할 일은 근거 [1] \u201c제1조\u201d에 따릅니다. 확인할 점: 기한.';"
  + "app.callAI=app.callAIWithDocuments=async(p)=>{await new Promise(r=>setTimeout(r,200));return mk(String(p))};"
  + "app.callAIWithHistory=async(m)=>{await new Promise(r=>setTimeout(r,200));return mk(String(m.at(-1)?.content||''))};"
  + "app._tryGeminiChainStream=async(p,k,c,contents,on)=>{const a=mk(String(contents.at(-1)?.parts?.[0]?.text||''));on(a,a);return a};"
  + "const __of=window.fetch.bind(window);window.fetch=async(u,...a)=>{if(/^(data|blob):/.test(String(u&&u.url||u)))return __of(u,...a);throw new Error('시험: 외부 통신 막음')};") : '';
const SETUP = "(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));localStorage.setItem('welcomeShown','1');localStorage.setItem('deadlineNotifyMode','off');['tipNwTab','tipSkipTargetSeen','startupPromptShown','authorInfoSet'].forEach(k=>localStorage.setItem(k,'1'));document.getElementById('welcomeModal')?.remove();app.checkBackupReminder=()=>{};app._collabSetMe({name:'홍길동',dept:'시험과',rank:'소방위'});app._collabSetMyName('홍길동');"
  + "window.confirm=()=>true;window.alert=()=>{};app._saveFileWithPicker=async()=>true;app._downloadJsonFile=()=>{};HTMLAnchorElement.prototype.click=function(){};window.open=()=>null;" + STUB + "return 'ok'})()";
const out = { seed: SEED, ai: AI, steps: 0, problems: [], skipped: 0, actions: {} };
const recent = [];
async function inject() { await ev(SETUP); await ev(CANON); await ev(MONKEY); await ev(`__monkey.init(${SEED * 7919 + out.steps},${AI})`); }
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); }
    if (d.method === 'Runtime.exceptionThrown') pageErrs.push('EXC ' + (d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text || '').split('\n').slice(0, 4).map(x => x.replace(/file:\/\/\/[^)]*index\.html:/, 'index:').replace(/file:\/\/\/[^)]*ai_test%20\.html:/, 'ai:')).join(' | '));
    if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') pageErrs.push('ERR ' + d.params.args.map(a => a.value || a.description || '').join(' ').split('\n')[0].slice(0, 200)); };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 810, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'file:///' + file.replace(/\\/g, '/') });
  for (let k = 0; k < 60; k++) { if (await ev("typeof app!=='undefined'&&!!app&&!!app.allData&&app._dataLoaded===true") === true) break; await sleep(500); }
  await sleep(800);
  await inject();
  await ev("(async()=>{await app.insertPracticeWorkflows();await new Promise(r=>setTimeout(r,2500));return 'ok'})()");
  pageErrs = [];
  let fails = 0;
  for (let i = 1; i <= N; i++) {
    out.steps = i;
    const r = await ev('__monkey.step()', 45000);
    const name = r && r.name || (r && r.__timeout ? '(멈춤)' : r && r.__exc ? '(실행 오류)' : '?');
    recent.push(`${i}:${name}${r && r.t ? '(' + r.t + ')' : ''}`); if (recent.length > 14) recent.shift();
    out.actions[name] = (out.actions[name] || 0) + 1;
    if (r && r.t === 'x') out.skipped++;
    const probs = [];
    if (r && r.__timeout) { probs.push('동작이 45초 안에 끝나지 않음(멈춤·끝나지 않는 대기)'); await ev("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))"); }
    if (r && r.__exc) probs.push('실행 오류 ' + r.__exc);
    if (r && r.err) probs.push(r.err);
    if (r && r.undoDiff) probs.push('되돌리기 뒤 하기 전과 다름: ' + r.undoDiff.join(' | '));
    const sc = await ev(SC, 30000);
    if (sc && sc.e && sc.e.length) probs.push(...sc.e.map(x => '검사기: ' + x));
    if (pageErrs.length) { probs.push(...pageErrs.slice(0, 4)); pageErrs = []; }
    // 150동작마다: 새로 고침 뒤 자료가 그대로인지
    if (i % 150 === 0 || i === N) {
      await ev("(async()=>{app.closeAllDropdowns?.();if(app.focusEditMode){app.exitFocusEditMode();}await app.saveDataImmediate();return 'ok'})()");
      await sleep(2000);
      const before = await ev(CANON + ";__canon({times:true})");
      await send('Page.reload', { ignoreCache: true }); await sleep(1500); for (let k = 0; k < 60; k++) { if (await ev("typeof app!=='undefined'&&!!app&&!!app.allData&&app._dataLoaded===true") === true) break; await sleep(500); } await sleep(1500);
      await inject();
      const after = await ev(CANON + ";__canon({times:true})");
      const d = await ev(`__diff(${JSON.stringify(before)},${JSON.stringify(after)},8)`);
      recent.push(`${i}:새로 고침`);
      if (Array.isArray(d) && d.length) { const ids = [...new Set(d.map(x => (x.match(/^wf\.(\d+)/) || [])[1]).filter(Boolean))]; const who = ids.map(id => { const w = (before.wf || {})[id] || {}; return `${id}=${(w.title || '').slice(0, 14)}${w.del ? '(지움)' : ''}${w.done ? '(완료)' : ''}${w.ref ? '(레퍼런스)' : ''}`; }).join(', '); probs.push('새로 고침 뒤 자료가 다름 [' + who + ']: ' + d.join(' | ')); }
      pageErrs = pageErrs.filter(x => !/favicon/.test(x));
      if (pageErrs.length) { probs.push(...pageErrs.slice(0, 4).map(x => '새로 고침 중 ' + x)); pageErrs = []; }
    }
    if (probs.length) {
      fails++;
      const state = await ev("(()=>{const w=app.focusMode?app.allData.workflows.find(x=>x.id===app.focusedWorkflowId):null;if(!w)return '(목록 화면)';return w.title.slice(0,14)+' 계산='+app.calculateProgress(w)+'% 패널='+((document.getElementById('procProg')||{textContent:''}).textContent.match(/\d+%/)||[''])[0]+' 편집='+app.focusEditMode+' 줄='+w.checklist.map(i=>(i.indent?'-':'')+i.text.slice(0,5)+(app.normalizeCompleted(i)?'✓':'')+(i.skipped?'⤼':'')).join(',')})()");
      const p = { step: i, action: name, problems: [...new Set(probs)], recent: [...recent], state };
      out.problems.push(p);
      console.log(`문제 #${fails} @${i} ${name}: ${p.problems.join(' ¦ ').slice(0, 400)}`);
      if (fails <= 6) await shot(`monkey_fail_${TAG}_${i}.png`);
    }
    if (i % 50 === 0) console.log(`… ${i}/${N} 동작 · 문제 ${fails}`);
    if (fails >= 40) { console.log('문제가 40개를 넘어 멈춤'); break; }
  }
  fs.writeFileSync(path.join(dir, `monkey_${TAG}.json`), JSON.stringify(out, null, 1));
  console.log(`MONKEY 결과 씨앗=${SEED}${AI ? ' AI' : ''} 동작=${out.steps} 건너뜀=${out.skipped} 문제=${out.problems.length}`);
} catch (e) { console.log('MONKEY 실행기 오류', e.message); } finally { try { ws?.close(); } catch (e) {} proc.kill(); }
