// 시연·홍보 영상 녹화: 실제 업무 내비게이터를 헤드리스 크롬에서 조작하며 탭 화면을 그대로 녹화(MediaRecorder)
// 화면 위에 덧씌우는 것: 큰 글씨 장면(card)·아래 자막·장면 이름표·마우스 화살표·강조 상자 — 모두 녹화에 함께 찍힘
// 소리(내레이션·배경음악)는 나중에 mix3.py가 장면 시각(marks.json)에 맞춰 붙임
// 실행: node tools/video3/rec3.mjs <index.html 경로> [dry]   (dry = 녹화 없이 장면마다 사진만 → 영상작업/dry/)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const here = path.dirname(decodeURIComponent(new URL(import.meta.url).pathname).replace(/^\/(\w:)/, '$1'));
const work = path.join(here, '..', '..', '영상작업');
const [, , appFile, mode] = process.argv;
const DRY = mode === 'dry';
const SEG = JSON.parse(fs.readFileSync(path.join(work, 'seg.json'), 'utf-8'));     // build3.py가 만든 장면 목록(+ 음성 길이·문장 시각)
const SEED = fs.readFileSync(path.join(work, 'seed.js'), 'utf-8');
const chrome = process.env.CHROME_PATH || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : 'google-chrome');
const prof = path.join(work, 'chrome-prof');
fs.rmSync(prof, { recursive: true, force: true });
const VW = 1440, VH = 810, DPR = 4 / 3;   // 화면 1440×810(CSS) × 4/3 = 1920×1080
const proc = spawn(chrome, ['--headless=new', '--remote-debugging-port=9336', `--user-data-dir=${prof}`, `--window-size=${VW},${VH}`, `--force-device-scale-factor=${DPR}`,
  '--auto-accept-this-tab-capture', '--autoplay-policy=no-user-gesture-required', '--allow-file-access-from-files', '--hide-scrollbars',
  '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map();
async function connect() {
  for (let i = 0; i < 60; i++) {
    try { const j = await (await fetch('http://127.0.0.1:9336/json')).json(); const p = j.find(x => x.type === 'page'); if (p) return p.webSocketDebuggerUrl; } catch (e) {}
    await sleep(250);
  }
  throw new Error('크롬 연결 안 됨');
}
function send(method, params = {}) { return new Promise(res => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); }
async function ev(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true, userGesture: true });
  if (r.result?.exceptionDetails) throw new Error('JS: ' + (r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text).slice(0, 300));
  return r.result?.result?.value;
}
// 앱 안에서 실행(편의 함수 포함)
const PRE = "const W=ms=>new Promise(r=>setTimeout(r,ms));const PW=()=>app.allData.workflows.find(w=>w.isPractice&&!w.isDeleted&&w.title.includes('소모품'));const ix=t=>PW().checklist.findIndex(i=>i.text===t);"
  + "const row=t=>document.querySelector('.checklist-card[data-workflow-id=\"'+PW().id+'\"][data-index=\"'+ix(t)+'\"]');";
const js = body => ev(`(async()=>{${PRE}${body}})()`);
// 요소 가운데 좌표 (화면 밖이면 가운데로 스크롤)
async function at(selJs, scroll = true) {
  const r = await js(`const el=(${selJs});if(!el)return null;${scroll ? "const b0=el.getBoundingClientRect();if(b0.top<60||b0.bottom>innerHeight-90){el.scrollIntoView({block:'center',behavior:'smooth'});await W(450);}" : ''}const b=el.getBoundingClientRect();return [b.left+b.width/2,b.top+b.height/2,b.left,b.top,b.width,b.height];`);
  if (!r) throw new Error('요소 없음: ' + selJs.slice(0, 120));
  return r;
}
let cx = VW * 0.55, cy = VH * 0.6;
async function move(x, y, ms = 520) {   // 화살표를 부드럽게 옮기고(화면), 실제 마우스도 같은 길로(hover 효과)
  await ev(`__v.cur(${x},${y},${ms})`);
  const n = Math.max(6, Math.round(ms / 40));
  for (let k = 1; k <= n; k++) {
    const t = k / n, e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx + (x - cx) * e, y: cy + (y - cy) * e });
    await sleep(ms / n);
  }
  cx = x; cy = y;
}
async function clickXY(x, y, { count = 1, button = 'left', ms } = {}) {
  await move(x, y, ms);
  await sleep(120);
  await ev(`__v.ripple()`);
  for (let c = 1; c <= count; c++) {
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button, clickCount: c });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button, clickCount: c });
    if (c < count) await sleep(70);
  }
}
async function click(selJs, o = {}) { const [x, y] = await at(selJs, o.scroll !== false); await clickXY(x + (o.dx || 0), y + (o.dy || 0), o); }
async function hover(selJs, ms) { const [x, y] = await at(selJs); await move(x, y, ms); }
async function hl(selJs, pad = 6) { const r = await at(selJs, false); await ev(`__v.hl(${r[2] - pad},${r[3] - pad},${r[4] + pad * 2},${r[5] + pad * 2})`); }
const hlOff = () => ev('__v.hl(null)');
let snapN = 0, curSeg = '';
async function snap(tag) { if (!DRY) return; await sleep(250); const sh = await send('Page.captureScreenshot', { format: 'png' }); fs.mkdirSync(path.join(work, 'dry'), { recursive: true }); fs.writeFileSync(path.join(work, 'dry', `m${String(++snapN).padStart(2, '0')}_${curSeg}_${tag}.png`), Buffer.from(sh.result.data, 'base64')); }
let actT0 = 0; const until = async t => { const w = actT0 + t * 1000 - Date.now(); if (w > 0) await sleep(w); };
async function typeText(t, cps = 22) { for (const ch of t) { await send('Input.insertText', { text: ch }); await sleep(1000 / cps); } }

// 장면별 실제 조작
const ACT = {
  async prep() {},
  async morning() {   // 켤 때 마감 알림 → 닫기 → 연습 업무 카드 가리키기
    await sleep(600);
    await js("localStorage.removeItem('lastDeadlineNotifyDate');app.checkDeadlineNotifications({startup:true});await W(300);return 1");
    await sleep(1200); await snap('alert'); await sleep(2200);
    const closeSel = "[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&/^(닫기|확인)$/.test(b.textContent.trim())).pop()";
    try { await click(closeSel); } catch (e) { await js("app.hideDeadlineBanner&&app.hideDeadlineBanner();return 1"); }
    await sleep(700);
    await hover("document.getElementById('workflow-'+PW().id)", 700);
    await hl("document.getElementById('workflow-'+PW().id)", 4);
    await sleep(1600); await hlOff();
  },
  async open() {      // 두 번 눌러 열기 → 일하는 화면
    await click("document.getElementById('workflow-'+PW().id)", { count: 2 });
    await sleep(1600);
    if (!(await js('return !!app.focusMode'))) { await js('app.focusWorkflow(PW().id);return 1'); await sleep(1500); }
    await hl("document.querySelector('#procProg')||document.querySelector('#procHead')", 6); await sleep(1800);
    await hl("document.getElementById('checklist-items-'+PW().id)||document.querySelector('.focus-checklist')", 4); await sleep(1800); await hlOff();
  },
  async tip() {       // 업무 절차 패널의 업무팁 세 칸 → 단계 공통 업무팁(쪼개기 금지)
    const P = "document.querySelector('#aiPanelOfflineDashboard')";
    await hover(`${P}.querySelector('.tip-sec')||${P}`, 700);
    await until(3.7); await hl(`${P}.querySelector('.tip-warn')`, 5); await snap('warn');
    await until(6.3); await hl(`${P}.querySelector('.tip-basis')`, 5);
    await until(8.4); await hlOff();
    await click(`${P}.querySelector('.proc-tip-fold')`);
    await sleep(700);
    await hl(`${P}.querySelector('.proc-tip-foldbody .tip-warn')`, 5); await snap('split');
    await until(14.6); await hlOff();
  },
  async check() {     // 01 단계 할 일 네 개 체크 → 단계가 접히고 다음 단계로
    for (const t of ['구매 요청 받기 — 품목·수량·규격 확인', '추정가격 정하기', '거래실례가격 조사 (2곳 이상)', '예정가격 작성']) {
      await click(`row(${JSON.stringify(t)})?.querySelector('input.checkbox')`);
      await sleep(t === '예정가격 작성' ? 1800 : 900);
    }
  },
  async branch() {    // 갈림길 [1인 견적] → 미리 보기 → 실행 → 건너뛴 줄 보기
    await hover("row('금액 기준 확인 — 갈림길')", 600); await sleep(500);
    await click("[...document.querySelectorAll('.branch-run-btn')].find(b=>b.textContent.trim().endsWith('1인 견적'))");
    await sleep(1500);
    await click("document.getElementById('branchPreviewConfirmBtn')");
    await sleep(1500);
    await hl("document.querySelector('#aiPanelOfflineDashboard .proc-skip-pill')?.parentElement", 5); await snap('skip'); await sleep(2200); await hlOff();
  },
  async forms() {     // 남은 할 일 체크 → 03 단계 첫 할 일의 서식 바로 열기 → 예시 그림
    for (const t of ['1인 견적서 받기', '수의계약 근거서류 갖추기']) { await click(`row(${JSON.stringify(t)})?.querySelector('input.checkbox')`); await sleep(800); }
    await sleep(900);
    await click("document.querySelector('#aiPanelOfflineDashboard .proc-fmt-open')");
    await sleep(1800); await snap('form'); await sleep(800);
    await js("document.querySelectorAll('.pv-modal').forEach(m=>m.querySelector('.close-preview-modal')?.click());await W(200);app.previewTipFile(PW().id,ix('지출 처리 (e호조)'),0);return 1");
    await sleep(1800); await snap('ex'); await sleep(800);
    await js("document.querySelectorAll('.pv-modal').forEach(m=>m.querySelector('.close-preview-modal')?.click());app.restoreBodyScroll&&app.restoreBodyScroll();return 1");
  },
  async result() {    // 줄을 눌러 처리결과 칸 → 적기 → 체크 → 마감일 D-n
    const t = JSON.stringify('배제사유 확인 · 각서 받기');
    await click(`row(${t}).querySelector('.checklist-card-header .item-title-text, .checklist-card-header')`);
    await sleep(700);
    await click("document.querySelector('.cl-peek .cl-result-input')");
    await sleep(250);
    await typeText('○○상사 배제사유 없음 확인, 각서 받음');
    await snap('typed'); await sleep(300);
    await click(`row(${t}).querySelector('input.checkbox')`);
    await sleep(1100);
    await hl(`[...row('수의계약 체결 제한 대상인지 확인').querySelectorAll('*')].find(e=>e.children.length===0&&/^D-\\d+$/.test(e.textContent.trim()))`, 5);
    await snap('due'); await sleep(1800); await hlOff();
  },
  async report() {    // 진행상황 출력: 체크리스트 → 진행상황 보고
    await js("app._prTab=null;app.openProgressReport(PW().id);return 1");
    await sleep(2600);
    await snap('cl');
    await click("document.querySelector('.pr-tabs [data-tab=report]')");
    await sleep(1500); await snap('rep'); await sleep(1700);
    await click("document.querySelector('.pr-tabs [data-tab=checklist]')");
    await sleep(2200);
    await js("app.closeProgressReport();return 1"); await sleep(400);
  },
  async handover() {  // 끝낸 업무 → 레퍼런스로 등록 → 내보내기(파일 하나)
    await js("if(app.focusMode)app.exitFocusMode();await W(500);app.openWorkflowManager();await W(700);app.wfmSetTab('done');return 1");
    await sleep(1000);
    const tr = "document.querySelector('#wfmTableBody tr[data-sel-key=\"8100\"]')";
    const [x, y] = await at(tr);
    await clickXY(x - 120, y, { button: 'right' });
    await sleep(900);
    try { await click("[...document.querySelectorAll('#wfmCtxMenu *')].find(e=>e.children.length<3&&/레퍼런스/.test(e.textContent)&&e.offsetParent)"); } catch (e) {}
    await sleep(1300);
    await click("[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()==='만들기')");
    await sleep(1500); await snap('ref');
    await js("app._saveFileWithPicker=async()=>true;return 1");
    await click("document.querySelector('#wfmModal .modal-close, #wfmModal [onclick*=closeWorkflowManager]')||[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.textContent.trim()==='×').pop()").catch(() => {});
    await js("if(document.querySelector('#wfmModal.show')||document.querySelector('.wfm-modal.show'))app.closeWorkflowManager&&app.closeWorkflowManager();app.focusWorkflow(PW().id);return 1");
    await sleep(1300);
    await click("[...document.querySelectorAll('button,[onclick]')].filter(e=>e.offsetParent&&e.textContent.trim()==='내보내기').pop()");
    await sleep(1300);
    if (DRY) console.log('  알림:', await js("return [...document.querySelectorAll('.toast')].map(t=>t.textContent.replace(/\s+/g,' ').trim()).join(' / ')"));
    await snap('export'); await sleep(1500);
  },
};

// 화면 위 덧씌우개(녹화에 함께 찍힘)
const OVERLAY = String.raw`(()=>{if(window.__v)return;const st=document.createElement('style');st.textContent=` + '`' + String.raw`
#vOv{position:fixed;inset:0;z-index:2147483000;pointer-events:none;font-family:'Pretendard','Malgun Gothic',sans-serif;}
#vCard{position:absolute;inset:0;background:radial-gradient(1200px 700px at 50% 45%,#13213b 0%,#070d1a 60%,#03060d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;transition:opacity .45s ease;}
#vCard.on{opacity:1}#vCard .ln{color:#e2e8f0;font-size:46px;font-weight:700;letter-spacing:-.02em;line-height:1.35;opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .7s cubic-bezier(.2,.8,.2,1);text-align:center;}
#vCard .ln.on{opacity:1;transform:none}#vCard .ln.big{font-size:118px;font-weight:800;letter-spacing:-.03em;background:linear-gradient(90deg,#fb923c,#f43f5e);-webkit-background-clip:text;color:transparent;}
#vCard.cl .ln.big{background:linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);-webkit-background-clip:text;color:transparent;font-size:104px}
#vCard.tt .ln:first-child{font-size:92px;font-weight:800;background:linear-gradient(90deg,#60a5fa,#a78bfa);-webkit-background-clip:text;color:transparent;}
#vCard.tt .ln:nth-child(2){font-size:34px;color:#cbd5e1;font-weight:600;margin-top:14px}
#vCard .sb{margin-top:26px;font-size:21px;color:#8391a7;opacity:0;transition:opacity .8s ease .9s}#vCard .sb.on{opacity:1}
#vCard .glow{position:absolute;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(96,165,250,.22),transparent 65%);filter:blur(10px);opacity:0;transition:opacity 1.2s}#vCard.cl .glow,#vCard.tt .glow{opacity:1}
#vBot{position:absolute;left:0;right:0;bottom:22px;display:flex;flex-direction:column;align-items:center;gap:8px}
#vLab{font-size:17px;font-weight:800;color:#fff;background:#f59e0b;padding:5px 14px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.25);opacity:0;transform:translateY(8px);transition:all .35s}
#vLab.on{opacity:1;transform:none}
#vSub{max-width:1180px;font-size:27px;line-height:1.42;font-weight:600;color:#fff;background:rgba(3,7,18,.80);padding:9px 24px 10px;border-radius:12px;text-align:center;opacity:0;transition:opacity .22s;word-break:keep-all}
#vSub.on{opacity:1}#vCardSub{position:absolute;left:0;right:0;bottom:40px;text-align:center;font-size:27px;font-weight:500;color:#cbd5e1;opacity:0;transition:opacity .3s}#vCardSub.on{opacity:1}
#vCur{position:absolute;left:0;top:0;width:26px;height:26px;transform:translate(800px,500px);transition-property:transform;transition-timing-function:cubic-bezier(.45,.05,.25,1);filter:drop-shadow(0 2px 3px rgba(0,0,0,.35));opacity:0}
#vCur.on{opacity:1}#vRip{position:absolute;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;border:3px solid #f59e0b;opacity:0}
#vRip.go{animation:vrip .5s ease-out}@keyframes vrip{0%{opacity:.95;transform:scale(.3)}100%{opacity:0;transform:scale(1.4)}}
#vHl{position:absolute;border:3px solid #f59e0b;border-radius:10px;box-shadow:0 0 0 4px rgba(245,158,11,.25),0 0 30px rgba(245,158,11,.35);opacity:0;transition:all .4s cubic-bezier(.2,.8,.2,1)}#vHl.on{opacity:1}
` + '`' + String.raw`;document.head.appendChild(st);
const o=document.createElement('div');o.id='vOv';o.innerHTML='<div id="vCard"><div class="glow"></div><div id="vCardIn" style="display:flex;flex-direction:column;align-items:center;position:relative"></div></div><div id="vHl"></div><div id="vBot"><div id="vLab"></div><div id="vSub"></div></div><div id="vCardSub"></div><div id="vRip"></div><svg id="vCur" viewBox="0 0 24 24"><path d="M4 2l16 9.5-7 1.6 4.2 7.4-2.9 1.6-4.2-7.5L4 19z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
document.body.appendChild(o);const $=i=>document.getElementById(i);let subT=[],curX=800,curY=500;
window.__v={
 card(c){const k=$('vCard');k.className='on'+(c.climax?' cl':'')+(c.title?' tt':'');const ci=$('vCardIn');ci.innerHTML=c.lines.map(l=>{const b=/^\*\*(.*)\*\*$/.exec(l);return '<div class="ln'+(b?' big':'')+'">'+(b?b[1]:l)+'</div>'}).join('')+(c.sub?'<div class="sb">'+c.sub+'</div>':'');
  [...ci.querySelectorAll('.ln')].forEach((e,i)=>setTimeout(()=>e.classList.add('on'),120+i*(c.climax?220:380)));setTimeout(()=>ci.querySelector('.sb')?.classList.add('on'),60);$('vLab').classList.remove('on');$('vCur').classList.remove('on');},
 cardOff(){$('vCard').classList.remove('on');},
 label(t){const l=$('vLab');if(!t){l.classList.remove('on');return}l.textContent=t;l.classList.add('on');$('vCur').classList.add('on');},
 subs(list,isCard){subT.forEach(clearTimeout);subT=[];const s=isCard?$('vCardSub'):$('vSub');$('vSub').classList.remove('on');$('vCardSub').classList.remove('on');
  list.forEach(x=>{subT.push(setTimeout(()=>{s.textContent=x.text;s.classList.add('on')},x.t*1000));subT.push(setTimeout(()=>{if(s.textContent===x.text)s.classList.remove('on')},(x.t+x.d)*1000+250));});},
 cur(x,y,ms){const c=$('vCur');c.classList.add('on');c.style.transitionDuration=ms+'ms';c.style.transform='translate('+(x-4)+'px,'+(y-2)+'px)';curX=x;curY=y;},
 ripple(){const r=$('vRip');r.style.left=curX+'px';r.style.top=curY+'px';r.classList.remove('go');void r.offsetWidth;r.classList.add('go');},
 hl(x,y,w,h){const e=$('vHl');if(x===null||x===undefined){e.classList.remove('on');return}Object.assign(e.style,{left:x+'px',top:y+'px',width:w+'px',height:h+'px'});e.classList.add('on');},
 t0:0,now(){return (performance.now()-this.t0)/1000;}
};})()`;

const LEAD = { card: 0.55, demo: 0.35 };
const PAD = { card: 0.75, demo: 0.45 };
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  const url = 'file:///' + path.resolve(appFile).replace(/\\/g, '/');
  await send('Page.navigate', { url }); await sleep(3500);
  // 처음 안내 창들 끄기 → 예시 자료(설명서와 같은 업무들) → 연습 업무 넣기 → 다시 열기
  await ev(`(async()=>{localStorage.setItem('authorInfoSet','1');app._collabSetMe&&app._collabSetMe({dept:'사하소방서 청문감사담당관',rank:'소방위',name:'홍길동',phone:'4521'});return await ${SEED.trim()};})()`);
  await js("window.confirm=()=>true;await app.insertPracticeWorkflows();await W(3000);app.allData.workflows.filter(w=>w.id===8101||w.id===8102).forEach(w=>{});app.saveData();return 1");
  await sleep(1500);
  await send('Page.reload'); await sleep(4000);
  await js("window.confirm=()=>true;document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const t=document.querySelector('.filter-tab[data-mode=\"inProgress\"]');t&&t.click();window.scrollTo(0,0);return 1");
  await sleep(800);
  { const [iw, ih] = JSON.parse(await ev('JSON.stringify([innerWidth,innerHeight])')); const wt = await send('Browser.getWindowForTarget');
    await send('Browser.setWindowBounds', { windowId: wt.result.windowId, bounds: { width: VW + (VW - iw), height: VH + (VH - ih) } }); await sleep(800); }
  await ev(OVERLAY);
  await ev(`__v.card(${JSON.stringify(SEG[0])})`);
  await sleep(900);
  const dim = await ev('JSON.stringify([innerWidth,innerHeight,devicePixelRatio])'); console.log('화면', dim);
  if (!DRY) {
    // 탭 공유를 먼저 시작 → 크롬이 「탭 공유 중」 줄을 넣어 화면이 줄어들므로 창을 다시 키워 1440×810으로 맞춘 뒤 녹화 시작
    const g = await ev(`(async()=>{try{window.__s=await navigator.mediaDevices.getDisplayMedia({video:{frameRate:30,width:{ideal:1920},height:{ideal:1080}},audio:false,preferCurrentTab:true});return 'ok'}catch(e){return 'ERR '+e.message}})()`);
    if (g !== 'ok') throw new Error('탭 공유 ' + g);
    await sleep(800);
    for (let k = 0; k < 3; k++) {
      const [iw, ih] = JSON.parse(await ev('JSON.stringify([innerWidth,innerHeight])')); if (iw === VW && ih === VH) break;
      const wt = await send('Browser.getWindowForTarget'); const b = (await send('Browser.getWindowBounds', { windowId: wt.result.windowId })).result.bounds;
      await send('Browser.setWindowBounds', { windowId: wt.result.windowId, bounds: { width: b.width + (VW - iw), height: b.height + (VH - ih) } }); await sleep(900);
    }
    console.log('녹화 화면', await ev('JSON.stringify([innerWidth,innerHeight,window.__s.getVideoTracks()[0].getSettings().width,window.__s.getVideoTracks()[0].getSettings().height])'));
    const r = await ev(`(async()=>{try{const s=window.__s;
      const mime=['video/mp4;codecs=avc1.640028','video/mp4;codecs=avc1','video/webm;codecs=vp9'].find(m=>MediaRecorder.isTypeSupported(m));
      const rec=new MediaRecorder(s,{mimeType:mime,videoBitsPerSecond:12000000});window.__ch=[];rec.ondataavailable=e=>window.__ch.push(e.data);window.__rec=rec;window.__mime=mime;
      rec.start(1000);__v.t0=performance.now();const st=s.getVideoTracks()[0].getSettings();return mime+' '+st.width+'x'+st.height;}catch(e){return 'ERR '+e.message}})()`);
    console.log('녹화 시작', r); if (String(r).startsWith('ERR')) throw new Error(r);
  } else await ev('__v.t0=performance.now()');
  const marks = [];
  for (let i = 0; i < SEG.length; i++) {
    const s = SEG[i];
    const t0 = await ev('__v.now()');
    if (s.kind === 'card') { if (i > 0) await ev(`__v.card(${JSON.stringify(s)})`); }
    else { await ev('__v.cardOff()'); await ev(`__v.label(${JSON.stringify(s.label)})`); }
    await ev(`__v.subs(${JSON.stringify(s.sents.map(x => ({ t: x.t + LEAD[s.kind], d: x.d, text: x.text })))},${s.kind === 'card'})`);
    const voiceAt = t0 + LEAD[s.kind];
    curSeg = s.id; actT0 = Date.now() + LEAD[s.kind] * 1000;
    const actP = (async () => { try { if (s.act && ACT[s.act]) await ACT[s.act](); } catch (e) { console.log(`  [${s.id}] 조작 오류:`, e.message); } })();
    const minEnd = sleep((LEAD[s.kind] + s.dur + (s.end ? 2.6 : PAD[s.kind])) * 1000);
    await Promise.all([actP, minEnd]);
    if (s.kind === 'demo') await sleep(250);
    const t1 = await ev('__v.now()');
    marks.push({ id: s.id, kind: s.kind, t0, voiceAt, t1, climax: !!s.climax, title: !!s.title, end: !!s.end });
    console.log(`${s.id}  ${t0.toFixed(2)} → ${t1.toFixed(2)}  (음성 ${s.dur}s)`);
    if (DRY) { const sh = await send('Page.captureScreenshot', { format: 'png' }); fs.mkdirSync(path.join(work, 'dry'), { recursive: true }); fs.writeFileSync(path.join(work, 'dry', `${String(i).padStart(2, '0')}_${s.id}.png`), Buffer.from(sh.result.data, 'base64')); }
  }
  fs.writeFileSync(path.join(work, DRY ? 'marks_dry.json' : 'marks.json'), JSON.stringify({ total: marks[marks.length - 1].t1, marks }, null, 1));
  if (!DRY) {
    await ev('(async()=>{window.__rec.stop();await new Promise(r=>window.__rec.onstop=r);const b=new Blob(window.__ch,{type:window.__mime});const u8=new Uint8Array(await b.arrayBuffer());let s="";for(let i=0;i<u8.length;i+=32768)s+=String.fromCharCode.apply(null,u8.subarray(i,i+32768));window.__b64=btoa(s);return 1})()');
    const len = await ev('window.__b64.length'); const parts = [];
    for (let off = 0; off < len; off += 2000000) parts.push(await ev(`window.__b64.slice(${off},${off + 2000000})`));
    const ext = (await ev('window.__mime')).includes('mp4') ? 'mp4' : 'webm';
    const out = path.join(work, 'raw.' + ext); fs.writeFileSync(out, Buffer.from(parts.join(''), 'base64'));
    console.log('저장', out, (fs.statSync(out).size / 1e6).toFixed(1), 'MB');
  }
} catch (e) { console.log('ERR', e.message); }
finally { try { ws.close(); } catch (e) {} proc.kill(); }
