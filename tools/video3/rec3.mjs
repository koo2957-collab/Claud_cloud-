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
const ST = k => { const x = SEG.find(s => s.id === curSeg)?.sents?.[k]; return x ? x.t : 0; };   // 지금 장면 k번째 문장이 시작하는 때(초)
const SD = k => { const x = SEG.find(s => s.id === curSeg)?.sents?.[k]; return x ? x.t + x.d : 0; };   // …끝나는 때
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
    await hl("document.querySelector('#aiPanelOfflineDashboard .proc-skip-pill')?.parentElement", 5); await snap('skip'); await sleep(2000); await hlOff();
    // 02 단계 남은 할 일 체크 → 03 단계(배제사유 확인 · 각서 받기)로 — 다음 장면이 서식부터 바로 보이게
    for (const t of ['1인 견적서 받기', '수의계약 근거서류 갖추기']) { await click(`row(${JSON.stringify(t)})?.querySelector('input.checkbox')`); await sleep(700); }
  },
  async forms() {     // 서식 이름 누르기 → 한글 서식 미리 보기 → [⬇ 내려받기] → 업무팁 작성례 → 다음 사진으로 넘기기
    const P = "document.querySelector('#aiPanelOfflineDashboard')";
    await click(`${P}.querySelector('.proc-fmt-open')`);
    await sleep(1500); await snap('form');
    const DL = "[...document.querySelectorAll('.pv-modal .pv-dl, .modal.show .pv-dl')].filter(b=>b.offsetParent).pop()";
    await until(ST(0) + 3.0); await hl(DL, 5);
    await until(ST(0) + 4.1); await click(DL, { scroll: false }); await hlOff();
    await ev(`__v.dl(${JSON.stringify('각서(수의계약 배제사유).hwpx')})`); await snap('dl');
    await until(Math.max(ST(1) - 0.3, ST(0) + 6.0));
    await js("document.querySelectorAll('.pv-modal').forEach(m=>m.querySelector('.close-preview-modal')?.click());app.restoreBodyScroll&&app.restoreBodyScroll();return 1");
    await sleep(400);
    await click(`${P}.querySelector('.proc-thumb')`);
    await sleep(1400); await snap('ex1');
    await until(ST(1) + 2.4);
    await ev("__v.ripple()"); await send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39 }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39 });
    await sleep(1200); await snap('ex2');
    await until(SD(1) + 0.8);
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
  async report() {    // 합쳐진 업무 → 진행상황 보고서 → 체크리스트(빠진 절차 점검표로)
    await js("app._prTab='report';app.openProgressReport(PW().id);return 1");
    await sleep(2400); await snap('rep');
    await until(ST(1) + 0.3);
    await click("document.querySelector('.pr-tabs [data-tab=checklist]')");
    await sleep(1600); await snap('cl');
    await until(SD(1) + 0.5);
    await js("app.closeProgressReport();app._prTab=null;return 1"); await sleep(400);
  },
  async collab() {    // 관리자: [업무 분담] → 04 납품·검사 김민수 · 05 대가 지급 이수진(회신 기한) → [요청 파일 만들기] → 회신 현황 → ⏳ 회신 대기 줄
    const D = n => new Date(Date.now() + n * 864e5).toLocaleDateString('sv-SE');   // 이 PC 시간대 기준 날짜
    await js("const c=app._collabEnsureOwner(PW());c.team=['김민수','이수진'];app.saveData();app._saveFileWithPicker=async()=>true;return 1");
    await click("[...document.querySelectorAll('.fap-btn')].find(b=>b.offsetParent&&b.textContent.trim()==='업무 분담')");
    await sleep(1300); await snap('open');
    const ROW = t => `[...document.querySelectorAll('#collabModal tr.cb-stagerow')].find(r=>r.querySelector('.cb-step-name')?.textContent.includes(${JSON.stringify(t)}))`;
    for (const [t, who, d] of [['납품·검사', '김민수', 14], ['대가 지급', '이수진', 20]]) {
      const [x, y] = await at(`${ROW(t)}?.querySelector('select')`);
      await move(x, y, 480); await ev('__v.ripple()'); await sleep(300);   // 고르는 목록은 화면에 안 찍히므로 값만 바꿈
      await js(`const s=${ROW(t)}.querySelector('select');s.value=${JSON.stringify(who)};s.dispatchEvent(new Event('change',{bubbles:true}));await W(250);app.collabSetStep(PW().id,PW().checklist[ix(${JSON.stringify(t)})].itemId,'deadline',${JSON.stringify(D(d))});return 1`);
      await sleep(600);
    }
    await hl(ROW('납품·검사'), 4); await snap('assigned');
    await until(Math.max(5.2, SD(1) - 2.6));
    const SEND = "[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('요청 파일 만들기'))";
    await hl(`${SEND}.closest('.cb-foot')||${SEND}`, 4);
    await until(Math.max(7.6, SD(1))); await hlOff();
    await click(SEND);
    await sleep(1600); await snap('status');
    await until(Math.max(12.0, SD(2) - 0.2));
    await js("app.closeCollabModal(true);app.restoreBodyScroll&&app.restoreBodyScroll();document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));return 1");
    await sleep(600);
    await at("document.querySelector('.cb-run')");   // 화면 밖이면 가운데로
    await hl("document.querySelector('.cb-run')", 5); await snap('waiting');
    await until(15.5); await hlOff();
  },
  async merge() {     // 관리자: 김민수의 회신 파일을 [회신 가져오기]로 열기 → 「바뀐 곳」 → [바뀐 곳 보기] → 04 납품·검사가 ✓
    // 담당자 PC에서 만든 것과 같은 형식(collab_reply)의 회신 파일을 만듦 — 합치는 것은 앱의 실제 기능(collabImportReplyFile)
    await js(`const w=PW(),c=w.collab,cl=w.checklist,sid=cl[ix('납품·검사')].itemId,st=c.steps[sid];
      const R={'납품 완료 통지 받기 (서면)':'○○상사 납품 완료 통지서 접수','납품 검사 (업체 참관)':'일회용 장갑 200상자·마스크 300상자 — 수량·규격 이상 없음 (업체 참관)','검사조서 작성':'검사조서 작성 — 검사자 김민수','검사 결과 서면 통지':'검사 합격 서면 통지 완료'};
      const now=new Date().toISOString();
      const items=app._collabStepIndices(cl,sid,c.steps).map(i=>({itemId:app.ensureChecklistItemId(cl[i]),stepId:sid,text:cl[i].text,completed:true,completedAt:now,completedViaSubItems:false,skipped:false,skipReason:'',skipManual:false,skipActionId:null,branchActionTaken:null,branchOnly:false,result:{text:R[cl[i].text]||'',summary:''}}));
      const cv=document.createElement('canvas');cv.width=900;cv.height=600;const g=cv.getContext('2d');g.fillStyle='#eef2f7';g.fillRect(0,0,900,600);g.fillStyle='#94a3b8';for(let k=0;k<5;k++){g.fillRect(90+k*150,250,110,190);g.fillRect(80+k*150,230,130,26);}
      g.fillStyle='#1e3a8a';g.font='bold 44px sans-serif';g.fillText('납품 검사 — 구급 소모품',90,120);g.fillStyle='#334155';g.font='28px sans-serif';g.fillText('장갑 200상자 · 마스크 300상자 · 업체 참관',90,180);g.fillText('검사자 김민수',90,520);
      const it=items.find(x=>x.text.startsWith('납품 검사'));const files={};
      if(it)files[it.itemId]=[{name:'납품검사_사진.jpg',type:'image/jpeg',size:60000,uploadDate:now,base64Data:cv.toDataURL('image/jpeg',0.85)}];
      window.__reply={type:'collab_reply',version:1,appVersion:APP_VERSION,uid:c.uid,sendId:st.sendId,from:'김민수',owner:c.owner,title:w.title,round:1,kind:'final',repliedAt:now,steps:[sid],items,files,comment:'검사 이상 없습니다. 검사 사진 첨부합니다.'};return 1`);
    const link = "document.querySelector('.fap-link-sub')";
    await hover(link, 600); await ev('__v.ripple()'); await sleep(250);   // 파일 고르는 창은 화면에 안 찍히므로 회신 파일을 바로 넣음
    await js("app.collabImportReplyFile(PW().id,new File([JSON.stringify(window.__reply)],'[회신] 소모품 구매_김민수.json',{type:'application/json'}));return 1");
    await sleep(1500);
    await hl("document.querySelector('#cbMergeDlg .modal-content')", 4); await snap('merged');
    await until(4.0); await hlOff();
    await click("document.querySelector('#cbMergeDlg [data-go]')");
    await sleep(1400);
    await hl("row('납품 검사 (업체 참관)')||row('납품·검사')", 5); await snap('reveal');
    await until(7.4); await hlOff();
  },
  async handover() {  // 진행 중인 월간 보고를 [내보내기] → 「후임자 PC」 → 그대로 가져오기 → 같은 자리에서 이어서
    const PM = "app.allData.workflows.find(w=>w.isPractice&&!w.isDeleted&&w.title.includes('월간'))";
    await js("document.getElementById('cbMergeDlg')?.remove();if(app.focusMode)app.exitFocusMode();await W(500);window.scrollTo(0,0);return 1");
    await sleep(500);
    await click(`document.getElementById('workflow-'+${PM}.id)`, { count: 2 });
    await sleep(1400);
    if (!(await js('return !!app.focusMode'))) { await js(`app.focusWorkflow(${PM}.id);return 1`); await sleep(1200); }
    await hl("document.querySelector('#procProg')||document.querySelector('#procHead')", 6);
    // 저장 창 대신 파일을 잡아 둠 · 내보내기 알림은 숨김
    await js("app._saveFileWithPicker=async(b,n)=>{window.__hb=b;return true};return 1");
    await until(3.0); await hlOff();
    await click("[...document.querySelectorAll('button,[onclick]')].filter(e=>e.offsetParent&&e.textContent.trim()==='내보내기').pop()");
    await sleep(900); await snap('export');
    await js("document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));return 1");
    await until(5.6);
    // 후임자 PC: 이 PC의 업무는 지우고(후임자에겐 없음) 받은 파일만 가져옴
    await ev("__v.label('후임자 PC · 받은 파일 그대로 가져오기')");
    await js(`const w=${PM};app.exitFocusMode&&app.exitFocusMode();w.isDeleted=true;w.deletedAt=new Date().toISOString();app.saveData();app.displayWorkflows();await W(500);window.scrollTo(0,0);app._showPackageImportChoice(JSON.parse(await window.__hb.text()));return 1`);
    await sleep(900);
    await hl("[...document.querySelectorAll('#packageImportChoiceModal label')].find(l=>l.textContent.includes('그대로 가져오기'))", 4); await snap('choice');
    await sleep(1400); await hlOff();
    await click("document.querySelector('#packageImportChoiceModal .btn-primary')");
    await sleep(1600);
    await js(`document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const w=app.allData.workflows.filter(x=>!x.isDeleted&&x.title.includes('월간 업무 실적')).sort((a,b)=>b.id-a.id)[0];app.focusWorkflow(w.id);return 1`);
    await sleep(1500);
    await hl("document.querySelector('#procProg')||document.querySelector('#procHead')", 6); await snap('continued');
    await sleep(1500);
    await hl("document.querySelector('#aiPanelOfflineDashboard .tip-sec')||document.querySelector('#aiPanelOfflineDashboard')", 5);
    await until(14.5); await hlOff();
  },
  async reference() { // 끝난 업무(5월 소모품 구매) → 레퍼런스로 등록 → 레퍼런스 탭
    await js("if(app.focusMode)app.exitFocusMode();await W(500);app.openWorkflowManager();await W(700);app.wfmSetTab('done');return 1");
    await sleep(900);
    // 예시 자료의 5월 처리완료본(소모품 구매 토너·복사용지)을 레퍼런스로
    const oldId = await js("return app.allData.workflows.find(w=>w.completedProcessed&&!w.isDeleted&&w.title.includes('토너'))?.id");
    const tr = `document.querySelector('#wfmTableBody tr[data-sel-key="${oldId}"]')`;
    const [x, y] = await at(tr);
    await clickXY(x - 120, y, { button: 'right' });
    await sleep(800);
    try { await click("[...document.querySelectorAll('#wfmCtxMenu *')].find(e=>e.children.length<3&&/레퍼런스/.test(e.textContent)&&e.offsetParent)"); } catch (e) {}
    await sleep(1100);
    await click("[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.textContent.trim()==='만들기')");
    await sleep(1200);
    await js("document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));app.wfmSetTab('reference');return 1");
    await sleep(900);
    await hl("document.querySelector('#wfmTableBody tr')", 4); await snap('ref');
    await sleep(2600); await hlOff();
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
#vDl{position:absolute;right:28px;top:76px;display:flex;align-items:center;gap:12px;background:#fff;color:#0f172a;border:1px solid #cbd5e1;border-radius:12px;padding:12px 18px;font-size:19px;font-weight:600;box-shadow:0 10px 30px rgba(0,0,0,.22);opacity:0;transform:translateY(-10px);transition:all .35s}#vDl.on{opacity:1;transform:none}#vDl b{display:inline-flex;width:30px;height:30px;border-radius:50%;background:#10b981;color:#fff;align-items:center;justify-content:center;font-size:18px}#vDl small{display:block;font-size:15px;color:#64748b;font-weight:500}
#vHl{position:absolute;border:3px solid #f59e0b;border-radius:10px;box-shadow:0 0 0 4px rgba(245,158,11,.25),0 0 30px rgba(245,158,11,.35);opacity:0;transition:all .4s cubic-bezier(.2,.8,.2,1)}#vHl.on{opacity:1}
` + '`' + String.raw`;document.head.appendChild(st);
const o=document.createElement('div');o.id='vOv';o.innerHTML='<div id="vCard"><div class="glow"></div><div id="vCardIn" style="display:flex;flex-direction:column;align-items:center;position:relative"></div></div><div id="vHl"></div><div id="vDl"></div><div id="vBot"><div id="vLab"></div><div id="vSub"></div></div><div id="vCardSub"></div><div id="vRip"></div><svg id="vCur" viewBox="0 0 24 24"><path d="M4 2l16 9.5-7 1.6 4.2 7.4-2.9 1.6-4.2-7.5L4 19z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
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
 dl(n){const e=$('vDl');e.innerHTML='<b>⬇</b><div>'+n+'<small>내 PC에 저장됨 — 한글에서 바로 작성</small></div>';e.classList.add('on');clearTimeout(this._dlT);this._dlT=setTimeout(()=>e.classList.remove('on'),3200);},
 t0:0,now(){return (performance.now()-this.t0)/1000;}
};})()`;

const LEAD = { card: 0.55, demo: 0.35 };
const PAD = { card: 0.75, demo: 0.45 };
try {
  ws = new WebSocket(await connect());
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: path.join(work, 'dl') });
  await send('Emulation.setFocusEmulationEnabled', { enabled: true });
  const url = 'file:///' + path.resolve(appFile).replace(/\\/g, '/');
  await send('Page.navigate', { url }); await sleep(3500);
  // 처음 안내 창들 끄기 → 예시 자료(설명서와 같은 업무들) → 연습 업무 넣기 → 다시 열기
  await ev(`(async()=>{localStorage.setItem('authorInfoSet','1');app._collabSetMe&&app._collabSetMe({dept:'사하소방서 청문감사담당관',rank:'소방위',name:'홍길동',phone:'4521'});return await ${SEED.trim()};})()`);
  // 예시 자료(설명서와 같음)는 연습 업무를 넣고 01 단계를 끝내 두므로, 영상에서는 처음 상태로 되돌려 직접 체크하며 보여 줌
  await js("window.confirm=()=>true;const w=PW();w.checklist.forEach(it=>{it.completed=false;delete it.completedAt;delete it.result;if(it.skipManual){it.skipped=false;delete it.skipManual;delete it.skipReason;}});app.saveData();await W(800);return 1");
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
