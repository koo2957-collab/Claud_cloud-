# 길잡이 「법령·매뉴얼 점검」 찾은 곳 사실대로 · [＋ 연결] · 연결 안 된 자료는 더 엄격하게 / 할 일 마감 알림(이름·외 n개·눌러서 그 할 일로·접힌 단계 줄 「할 일 D-n」) → steps3.json
#   G: (AI 허용판·가짜 AI) 연결한 자료 없음 → 「연결한 자료 없음 · 법령·매뉴얼 전체에서 찾음」·점선 근거·[＋ 연결] 실제 클릭 → ✓ 연결함·실행 취소 알림
#      · 다시 열면 「업무에 연결한 자료 1개에서」·연결 줄 없음 · 찾는 중 문구 · 낱말 하나만 걸린 엉뚱한 자료는 안 보임
#   D: (배포판도) 켤 때 알림·왼쪽 마감 임박에 「할 일 · 이름 외 n개」 · 업무 마감과 같은 날이면 「업무 전체 마감 · 할 일 …」
#      · 알림 줄 실제 클릭 → 그 할 일 줄이 보이고 밝혀짐 · 접힌 단계 줄에 「할 일 D-1」 · 일정에서 할 일 누르기(같은 함수) 그대로
# 실행: (tools 폴더에서) python mk_due_test.py && node cdp3.mjs "<저장소>/ai_test .html"   (index.html이면 G는 건너뜀)
import json
ID = 7987
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const tx=e=>e?e.textContent.replace(/\\s+/g,' ').trim():'(없음)';const wf=()=>app.allData.workflows.find(w=>w.id===ID);"
     "const ymd=n=>{const d=new Date();d.setDate(d.getDate()+n);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};"
     "const gm=()=>[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();"
     "const gclose=async()=>{document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(500)};"
     "const gbody=async()=>{for(let k=0;k<40;k++){const b=gm()?.querySelector('.gd-ai-body');if(b&&!b.querySelector('.chat-status'))return b;await W(200)}return gm()?.querySelector('.gd-ai-body')};"
     "const ti=()=>wf().checklist.findIndex(x=>x.text==='견적서 받기 및 예정가격 결정');"
     "const ban=async()=>{app.hideDeadlineBanner();localStorage.setItem('deadlineNotifyMode','always');app.checkDeadlineNotifications({startup:true});await W(500);const b=$('deadlineBanner');return {rows:[...b.querySelectorAll('.cs-row')],t:tx($('dbTitle')),log:(app.loadNotifyLog()[0]||{}).body||''}};"
     "const side=()=>{app.displayUrgentWorks();return [...document.querySelectorAll('#urgentWorksList .cs-row')]};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(expr): S.append({"pt": True, "js": P + "const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([Math.round(b.left+Math.min(b.width/2,40)),Math.round(b.top+b.height/2)])" + E})
def click(expr): pt(expr); S.append({"clickpt": 1})

MK = ("const mk=(t,i)=>{const o={text:t,indent:i,completed:false};app.ensureChecklistItemId(o);return o};"
      "const cl=[mk('구매 준비',0),mk('구매 요청서 확인',1),mk('예산 확인',1),mk('계약 준비',0),mk('견적서 받기 및 예정가격 결정',1),mk('계약 방법 정하기',1),mk('계약서 작성',1),mk('검사',0),mk('검사조서 받기',1)];")
step("준비: 시험 업무 · 법령·매뉴얼 자료 두 개(맞는 것·낱말 하나만 같은 것)",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};localStorage.setItem('deadlineNotifyMode','off');"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);" + MK +
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'마감 시험 물품 구매',checklist:cl,date:'2026. 11. 2.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();"
     "app.allData.geminiApiKey='TEST-KEY';app.allData.provider='gemini';app._syncAiOff?.();window.__ai=app.isAIAvailable();if(window.__ai){"
     "app.callAI=async p=>{window.__p=p;await W(200);return JSON.stringify({must:[{text:'견적서는 두 곳 이상에서 받습니다',ref:1,quote:'견적서를 받아 예정가격을 결정'}],diff:[],missing:[]})};app._lawEmbedBoost=async()=>new Map();"
     "app._generateAndStoreLibraryEmbeddings=async()=>({success:true,successCount:0,totalCount:0});"
     "const f1=new File(['제5조(견적서 받기) 계약담당자는 견적서를 받아 예정가격을 결정한다. 견적서 받기는 두 곳 이상에서 하며 예정가격 결정 전에 마친다.\\n제6조(계약 방법) 계약 방법을 정한다.'],'시험_계약사무규칙.txt',{type:'text/plain'});"
     "const f2=new File(['제1조(회의) 회의에서 소화기 점검 일정을 정했다. 견적서 이야기도 잠깐 했다.'],'시험_회의록.txt',{type:'text/plain'});"
     "await app.addLawLibraryFiles({type:'drop',dataTransfer:{files:[f1,f2]}});app.closeModal?.('lawLibraryModal');}"
     "return 'AI='+window.__ai+' · 할 일='+wf().checklist[ti()].text")
# ── G: 길잡이 법령 점검 (AI 허용판만) ──
step("G1 연결한 자료 없음 → 찾는 중 문구 · 「연결한 자료 없음 · 전체에서 찾음」 · 점선 근거 · [＋ 연결]",
     "if(!window.__ai)return '— 배포판: 건너뜀';app.focusWorkflow(ID);await W(1500);const i=ti();await app.showChecklistHelp(ID,i);await gbody();const m=gm();app._guideAiCheck(m.id,ID,i,{force:true});const s0=tx(m.querySelector('.gd-ai-body'));const b=await gbody();"
     "const h=tx(b.querySelector('.ai-src-h small'));const chips=[...b.querySelectorAll('.ai-chip')];const un=chips.filter(c=>c.classList.contains('unlinked')).length;const btns=[...b.querySelectorAll('.ai-src-link button')].map(x=>tx(x));const odd=chips.some(c=>/회의록/.test(c.title));"
     "const ok=/연결한 자료가 없어 법령·매뉴얼 전체에서/.test(s0)&&h==='연결한 자료 없음 · 법령·매뉴얼 전체에서 찾음'&&un===chips.length&&chips.length>0&&btns.length===1&&/계약사무규칙/.test(btns[0])&&!odd;"
     "window.__toasts=[];const _o=app.showToast.bind(app);app.showToast=(...a)=>{window.__toasts.push({m:String(a[2]||''),acts:(a[4]&&a[4].actions)||[]});return _o(...a)};return (ok?'✓':'✗')+' 찾는 중='+s0.slice(0,40)+' · 머리='+h+' · 근거 '+chips.length+'(점선 '+un+') · 단추='+btns.join('/')+' · 회의록 섞임='+odd")
click("(window.__ai?gm().querySelector('.ai-src-link button'):document.querySelector('.header')||document.body)")
step("G2 [＋ 연결] 실제 클릭 → ✓ 연결함 · 업무에 연결됨 · 실행 취소 알림",
     "if(!window.__ai)return '— 건너뜀';await W(600);const b=gm().querySelector('.ai-src-link button');const ids=app.checklistDetails['project-'+ID]?.linkedLibraryDocs||[];"
     "const T=window.__toasts.filter(x=>/연결했습니다/.test(x.m)).pop();const u=T&&T.acts.find(a=>a.label==='실행 취소');const n1=ids.length;if(u){await u.onAction();await W(300)}const n2=(app.checklistDetails['project-'+ID]?.linkedLibraryDocs||[]).length;"
     "const lid=(await app._getLibraryFileByName('시험_계약사무규칙.txt')).id;await app._lawLinkToWf(ID,lid,null);await W(300);"
     "const ok=b.disabled&&/연결함/.test(tx(b))&&n1===1&&!!u&&n2===0;return (ok?'✓':'✗')+' 단추='+tx(b)+' · 연결 수='+n1+' · 알림='+(T?T.m:'(없음)')+' · [실행 취소] 뒤 연결 수='+n2+' (다시 연결함)'")
step("G3 다시 열면 「업무에 연결한 자료 1개에서」 · 연결 줄 없음 · 찾는 중 문구",
     "if(!window.__ai)return '— 건너뜀';await gclose();const i=ti();await app.showChecklistHelp(ID,i);await gbody();app._guideAiCheck(gm().id,ID,i,{force:true});const s0=tx(gm().querySelector('.gd-ai-body'));const b=await gbody();const h=tx(b.querySelector('.ai-src-h small'));const row=!!b.querySelector('.ai-src-link');const un=b.querySelectorAll('.ai-chip.unlinked').length;"
     "const ok=/업무에 연결한 법령·매뉴얼에서/.test(s0)&&h==='업무에 연결한 자료 1개에서'&&!row&&un===0;await gclose();return (ok?'✓':'✗')+' 찾는 중='+s0.slice(0,30)+' · 머리='+h+' · 연결 줄='+row+' · 점선='+un")
step("G4 연결 자료에서 못 찾으면 「연결 자료 1개 + 전체에서」 (할 일이 다른 자료에만 맞을 때)",
     "if(!window.__ai)return '— 건너뜀';const f3=new File(['제9조(검사조서) 검사조서 받기는 검사를 마친 뒤 검사조서를 받아 보관한다. 검사조서 받기 기한은 7일.'],'시험_검사지침.txt',{type:'text/plain'});await app.addLawLibraryFiles({type:'drop',dataTransfer:{files:[f3]}});"
     "const i=wf().checklist.findIndex(x=>x.text==='검사조서 받기');await app.showChecklistHelp(ID,i);const b=await gbody();const h=tx(b.querySelector('.ai-src-h small'));const btn=tx(b.querySelector('.ai-src-link button'));await gclose();"
     "const ok=h==='연결 자료 1개 + 법령·매뉴얼 전체에서 찾음'&&/검사지침/.test(btn);return (ok?'✓':'✗')+' 머리='+h+' · 단추='+btn")
# ── D: 마감 알림 ──
step("D1 업무 마감 없음 · 뒤 단계(접힘) 할 일 D-1 → 켤 때 알림·왼쪽에 「할 일 · 이름」 · 알림 문장",
     "app.exitFocusMode?.();await W(600);const w=wf();w.deadline=null;w.checklist.forEach(x=>x.deadline=null);w.checklist[ti()].deadline=ymd(1);app.saveData();const r=await ban();const row=r.rows.find(x=>/마감 시험/.test(tx(x)));const sd=side().find(x=>/마감 시험/.test(tx(x)));"
     "const sub=tx(row&&row.querySelector('.cs-sub')),ss=tx(sd&&sd.querySelector('.cs-sub'));const ok=sub==='할 일 · 견적서 받기 및 예정가격 결정'&&/^할 일 · 견적서 받기 및 예정가격 결정/.test(ss)&&/할 일 「견적서 받기 및 예정가격 결정」의 마감/.test(r.log);"
     "return (ok?'✓':'✗')+' 알림 줄 아래='+sub+' · 왼쪽='+ss+' · 알림 문장='+r.log.slice(0,70)")
S.append({"shot": "due_banner.png"})
click("[...$('deadlineBanner').querySelectorAll('.cs-row')].find(x=>/마감 시험/.test(x.textContent))")
step("D2 알림 줄 실제 클릭 → 업무가 열리고 그 할 일 줄이 화면에 보이고 밝혀짐",
     "await W(1400);const i=ti();const sc=$('focus-checklist-scroll-'+ID);const el=sc&&sc.querySelector('.checklist-card[data-index=\"'+i+'\"]');const vis=!!el&&el.offsetParent!==null&&(()=>{const a=el.getBoundingClientRect(),b=sc.getBoundingClientRect();return a.top>=b.top-2&&a.bottom<=b.bottom+2})();"
     "const ok=app.focusedWorkflowId===ID&&vis&&!$('deadlineBanner').classList.contains('show');return (ok?'✓':'✗')+' 열린 업무='+(app.focusedWorkflowId===ID)+' · 할 일 줄 보임='+vis+' · 알림 닫힘='+!$('deadlineBanner').classList.contains('show')")
step("D3 접힌 단계 줄에 「할 일 D-1」 (단계를 접은 뒤)",
     "app.exitFocusMode?.();await W(500);app._stageOpen={};app.focusWorkflow(ID);await W(1500);const w=wf();const si=w.checklist.findIndex(x=>x.text==='계약 준비');const sc=$('focus-checklist-scroll-'+ID);const row=sc.querySelector('.checklist-card[data-index=\"'+si+'\"]');const kid=row&&row.querySelector('.cl-kid-due');const taskRow=sc.querySelector('.checklist-card[data-index=\"'+ti()+'\"]');"
     "const ok=!!kid&&tx(kid)==='할 일 D-1'&&/견적서 받기/.test(kid.title);return (ok?'✓':'✗')+' 단계 줄 표시='+tx(kid)+' · 설명='+(kid&&kid.title)+' · 할 일 줄 보임='+!!(taskRow&&taskRow.offsetParent)")
S.append({"shot": "due_stage.png"})
step("D4 업무 마감 D-1 · 할 일 D-1(같은 날) → 「업무 전체 마감 · 할 일 …」",
     "app.exitFocusMode?.();await W(500);const w=wf();w.deadline=ymd(1);app.saveData();const r=await ban();const row=r.rows.find(x=>/마감 시험/.test(tx(x)));const sub=tx(row&&row.querySelector('.cs-sub'));const ss=tx(side().find(x=>/마감 시험/.test(tx(x)))?.querySelector('.cs-sub'));app.hideDeadlineBanner();"
     "const ok=sub==='업무 전체 마감 · 할 일 견적서 받기 및 예정가격 결정'&&/^업무 전체 마감 · 할 일 견적서/.test(ss);return (ok?'✓':'✗')+' 알림='+sub+' · 왼쪽='+ss")
step("D5 할 일 셋(D-1·D-2·하루 지남) → 가장 급한 것 + 「외 2개」 · 마우스 올리면 셋 다",
     "const w=wf();w.deadline=null;w.checklist[ti()].deadline=ymd(1);w.checklist.find(x=>x.text==='계약 방법 정하기').deadline=ymd(2);w.checklist.find(x=>x.text==='예산 확인').deadline=ymd(-1);app.saveData();const r=await ban();const row=r.rows.find(x=>/마감 시험/.test(tx(x)));const sub=tx(row&&row.querySelector('.cs-sub'));const t=row?row.title:'';app.hideDeadlineBanner();"
     "const ok=sub==='할 일 · 예산 확인 외 2개'&&/예산 확인 \\(D\\+1\\)/.test(t)&&/견적서 받기 및 예정가격 결정 \\(D-1\\)/.test(t)&&/계약 방법 정하기 \\(D-2\\)/.test(t);return (ok?'✓':'✗')+' 줄 아래='+sub+' · 마우스='+t.replace(/\\n/g,' / ')")
click("side().find(x=>/마감 시험/.test(x.textContent))")
step("D6 왼쪽 마감 임박 실제 클릭 → 가장 급한 할 일(예산 확인) 줄이 보임",
     "await W(1400);const i=wf().checklist.findIndex(x=>x.text==='예산 확인');const sc=$('focus-checklist-scroll-'+ID);const el=sc&&sc.querySelector('.checklist-card[data-index=\"'+i+'\"]');const vis=!!el&&el.offsetParent!==null;return (app.focusedWorkflowId===ID&&vis?'✓':'✗')+' 열림='+(app.focusedWorkflowId===ID)+' · 예산 확인 줄 보임='+vis")
step("D7 일정 화면에서 할 일 누르기(같은 함수로 바꿈) 그대로",
     "app.exitFocusMode?.();await W(500);app.openSchedule(ID);await W(600);const e=app._schedEntries().find(x=>x.kind==='item'&&x.index===ti());app._schedGo(e.key);await W(1600);const sc=$('focus-checklist-scroll-'+ID);const el=sc&&sc.querySelector('.checklist-card[data-index=\"'+ti()+'\"]');const vis=!!el&&el.offsetParent!==null;"
     "return (!$('schedView')&&app.focusedWorkflowId===ID&&vis?'✓':'✗')+' 일정 닫힘='+!$('schedView')+' · 할 일 줄 보임='+vis")
step("정리", "app.exitFocusMode?.();await W(400);app.hideDeadlineBanner();localStorage.setItem('deadlineNotifyMode','off');app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.saveData();return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
