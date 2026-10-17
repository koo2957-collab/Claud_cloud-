import json
# 사용 설명서 촬영 대본 (v3 · 2026-10-17) — 모든 장면을 프로그램 안 「연습 업무」로 찍는다
#   window.__pw = [연습] 소모품 구매 — 계약부터 대가 지급까지 (일하는 화면·편집·분담·출력)
#   window.__pm = [연습] 월간 업무 실적 보고 (매달 5일) (완료·레퍼런스)
#   window.__wid = 1장에서 새로 만드는 「사무용 의자 구매」
S = []
def W(ms=600): return f"await new Promise(r=>setTimeout(r,{ms}));"
NL = "String.fromCharCode(10)"
HL = ("const R=(sel)=>{const el=typeof sel==='string'?document.querySelector(sel):sel;if(!el)return null;let r=el.getBoundingClientRect();let L=r.left,T=r.top,Rr=r.right,Bb=r.bottom;for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){const cs=getComputedStyle(p);if(/(auto|scroll|hidden|clip)/.test(cs.overflowY+cs.overflowX)){const q=p.getBoundingClientRect();L=Math.max(L,q.left);T=Math.max(T,q.top);Rr=Math.min(Rr,q.right);Bb=Math.min(Bb,q.bottom);}}L=Math.max(L,0);T=Math.max(T,0);Rr=Math.min(Rr,innerWidth);Bb=Math.min(Bb,innerHeight);return {x:Math.round(L),y:Math.round(T),w:Math.round(Math.max(0,Rr-L)),h:Math.round(Math.max(0,Bb-T))}};"
      "const toastOff=()=>document.querySelectorAll('.toast, .toast-container > *').forEach(t=>{if(t.id==='toast')t.classList.remove('show');else t.remove();});"
      "const wf=()=>app.allData.workflows.find(w=>w.id===window.__wid);"
      "const pw=()=>app.allData.workflows.find(w=>w.id===window.__pw);"
      "const row=(txt)=>[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text, .fci-title-text')?.textContent.trim().startsWith(txt));"
      "const idxOf=(t)=>wf().checklist.findIndex(x=>x.text===t);"
      "const px=(t)=>pw().checklist.findIndex(x=>x.text===t);"
      "const closeGuides=()=>{[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_[0-9]+$/.test(x.id)).forEach(m=>m.remove());document.body.style.overflow='';document.body.style.position='';document.body.style.top='';};"
      "const img=async(t,lines,c)=>{const cv=document.createElement('canvas');cv.width=900;cv.height=600;const g=cv.getContext('2d');g.fillStyle='#fdfaf2';g.fillRect(0,0,900,600);g.fillStyle=c||'#1e3a8a';g.font='bold 50px sans-serif';g.fillText(t,120,120);g.fillStyle='#333';g.font='30px sans-serif';lines.forEach((x,k)=>g.fillText(x,140,230+k*72));g.strokeStyle='#cbd5e1';g.lineWidth=3;g.strokeRect(60,60,780,480);return await new Promise(r=>cv.toBlob(r,'image/jpeg',0.9));};"
      "const D=(n)=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};")
def scene(name, code, hl=None, keepToast=False, hover=None):
    ret = f"return JSON.stringify({{hl: R({hl})}})" if hl else "return JSON.stringify({hl:null})"
    S.append({"label": name, "js": "(async()=>{try{" + HL + code + ("" if keepToast else "toastOff();") + W(300) + ret + "}catch(e){return JSON.stringify({err:e.message})}})()"})
    if hover: S.append({"hover": "(()=>{" + HL + hover + "})()"})
    S.append({"wait": 300, "shot": "man2/" + name + ".png", **({"hovered": True} if hover else {})})

T_REQ = "구매 요청 받기 — 품목·수량·규격 확인"
# ── 처음 켤 때: 환영 창 (새 프로필이라 저절로 뜸)
scene("00a_welcome", "localStorage.setItem('deadlineNotifyMode','off');app.checkBackupReminder=()=>{};if(!document.getElementById('welcomeModal')){localStorage.removeItem('welcomeShown');app.checkWelcome();}" + W(500), "'#welcomeModal .modal-content'")
# ── 준비: 내 정보 · 연습 업무 · 주소록 · 지난번 업무
scene("00_seed",
 "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown','welcomeShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.removeItem('lastDeadlineNotifyDate');localStorage.setItem('deadlineNotifyMode','daily');"
 "document.getElementById('welcomeModal')?.remove();document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
 "app._collabSetMe({dept:'○○소방서 행정과',rank:'소방위',name:'홍길동',phone:'4521'});app._collabSetMyName('홍길동');localStorage.setItem('authorInfoSet','1');app.renderMeAvatar&&app.renderMeAvatar();"
 "app._collabSavePeople([{name:'김민수',dept:'○○소방서 행정과',rank:'소방장'},{name:'이수진',dept:'○○소방서 행정과',rank:'소방교'},{name:'박정훈',dept:'○○소방서 장비담당',rank:'소방장'},{name:'최예린',dept:'○○소방서 회계담당',rank:'소방교'}]);"
 "await app.insertPracticeWorkflows();" + W(2500) +
 "const ps=app.allData.workflows.filter(w=>w.isPractice&&!w.isDeleted);window.__pw=ps.find(w=>/소모품/.test(w.title)).id;window.__pm=ps.find(w=>/월간/.test(w.title)).id;"
 # 지난번(5월)에 끝낸 같은 업무 — 「지난번엔 이렇게」·처리완료 탭·보관함 장면용
 "const src=pw();const old=JSON.parse(JSON.stringify(src));old.id=Date.now()+7;old.title='소모품 구매 (2026. 5. 토너·복사용지)';delete old.isPractice;old.createdAt='2026-05-04T09:00:00Z';old.date='2026. 5. 4.';old.completedProcessed=true;old.completedAt='2026-05-28T17:00:00Z';old.deadline='2026-05-29';"
 "old.checklist.forEach((it,k)=>{it.completed=!it.skipped;it.completedAt='2026-05-'+String(4+Math.floor(k/2)).padStart(2,'0')+'T10:00:00';});"
 "const res={'추정가격 정하기':'토너 12개·복사용지 40박스 — 추정가격 4,820,000원 (부가세 별도)','거래실례가격 조사 (2곳 이상)':'조달청 가격정보·△△오피스 견적 비교 — 최저 4,610,000원','1인 견적서 받기':'□□상사 견적 4,580,000원 (5.12.)','대가 지급 (청구일부터 5일 안)':'5.27.(수) 청구 → 5.28.(목) 지급 완료'};"
 "old.checklist.forEach(it=>{if(res[it.text])it.result={text:res[it.text],summary:''};});window.__old=old.id;app.allData.workflows.push(old);"
 # 연습 업무를 「일하는 중」으로: 01 구매 준비를 끝내고 처리결과 몇 줄
 "const w=pw();{const na=w.checklist[px('예정가격 작성')];na.skipped=true;na.skipManual=true;na.skipReason='1인 견적 소액 수의계약 — 예정가격 작성 생략';}const done=['" + T_REQ + "','추정가격 정하기','거래실례가격 조사 (2곳 이상)'];done.forEach(t=>{const it=w.checklist[px(t)];it.completed=true;it.completedAt=new Date(Date.now()-864e5*(4-done.indexOf(t))).toISOString();});w.checklist[0].completed=true;w.checklist[0].completedAt=new Date(Date.now()-864e5).toISOString();"
 "w.checklist[px('추정가격 정하기')].result={text:'의자 20개·책상 10개 — 추정가격 14,300,000원 (부가세 별도)',summary:''};w.checklist[px('거래실례가격 조사 (2곳 이상)')].result={text:'조달청 가격정보 · ○○가구 · △△오피스 3곳 비교 — 최저 13,980,000원',summary:''};"
 "w.lastProgressAt=new Date().toISOString();w.deadline=D(26);"
 "app.saveData();app.displayWorkflows();" + W(900))
# ── 0. 하루의 시작
scene("01_main", "", "'.sidebar, #sidebarUrgent, .urgent-section'")
scene("02_banner", "app.checkDeadlineNotifications({startup:true});" + W(900), "'#deadlineBanner'", keepToast=True)
scene("03_notify", "app.hideDeadlineBanner();const b=document.getElementById('deadlineBanner');if(b){b.classList.remove('show');b.style.display='none';}app.toggleNotifyCenter();" + W(700), "'#notifyCenterMenu'")
scene("04_newmenu", "if(document.getElementById('notifyCenterMenu')?.classList.contains('show'))app.toggleNotifyCenter();document.body.click();" + W(300) + "document.querySelector('[onclick*=\"newWorkMenu\"]').click();" + W(400), "'#newWorkMenu'")
# ── 1. 새 업무 만들기 (사무용 의자 구매)
NEWROWS = "[['구매 준비',0],['구매 요청 받기 — 품목·수량·규격 확인',1],['추정가격 정하기',1],['계약',0],['1인 견적서 받기',1],['계약서 작성',1],['납품·검사',0],['납품 검사 (업체 참관)',1],['검사조서 작성',1],['대가 지급',0],['대가 지급 (청구일부터 5일 안)',1]]"
scene("05_step1", "app.closeAllDropdowns();app.openModal('manualModal');" + W(600) + "document.getElementById('manualProjectName').value='사무용 의자 구매 (2026. 11.)';", "'#manualProjectName'")
scene("06_step2", "app._nwGo(2);" + W(500) + "const box=document.getElementById('checklistItems');const first=box.querySelector('.checklist-edit-item input');const rows=" + NEWROWS + ";"
 "if(first)first.value=rows[0][0];rows.slice(first?1:0).forEach(([t,i])=>app.addChecklistItem(t,i));" + W(300) + "const sc=box.closest('.nw-body')||box.parentElement;sc.scrollTop=0;document.getElementById('nwTabTip')?.remove();", "'#checklistItems'")
scene("07_step3", "app._nwGo(3);" + W(600) + "window.__wid=app._nw.wfId;", "'#nwMaterials'")
# 업무팁 세 칸 — 놓치기 쉬운 것 · 업무 팁 · 근거
scene("08_tip", "app._nwOpenItem(idxOf('1인 견적서 받기'),'tip');" + W(800) + "const i=idxOf('1인 견적서 받기'),w=window.__wid;const set=(k,v)=>{const t=document.getElementById('tip3-'+k+'-'+w+'-'+i);if(t){t.value=v;app._tip3Input(w,i,t);t.dispatchEvent(new Event('input',{bubbles:true}));}};"
 "set('warn',['추정가격 2천만원 초과면 1인 견적 불가 — 2인 이상 견적(나라장터 안내공고)','견적서 날짜가 계약일보다 늦으면 안 됩니다'].join(" + NL + "));"
 "set('body',['1. 업체 1곳에서 견적서를 받습니다 (사업자등록증 사본 함께)','2. 거래실례가격·예정가격과 비교해 계약금액을 정합니다'].join(" + NL + "));"
 "set('basis',['시행령 제30조제1항제2호','집행기준 제5장 제3절'].join(" + NL + "));" + W(600), "'#cimOverlay > div'")
scene("08b_tipfiles", "const i=idxOf('1인 견적서 받기');await app.addTipFiles(window.__wid,i,{files:[new File([await img('견적서 작성례',['품명  사무용 의자 (메시형)','수량  20개   단가  178,000원','합계  3,560,000원 (부가세 포함)','견적일  2026. 11. 3.'],'#b91c1c')],'견적서 작성례.jpg',{type:'image/jpeg'}),new File(['%PDF-1.4 '+'0'.repeat(90000)],'수의계약 체결 결재 예시.pdf',{type:'application/pdf'})],value:''});" + W(1000), "'#tf-'+window.__wid+'-'+idxOf('1인 견적서 받기')")
scene("09_fmpick", "app.closeChecklistItemModal();" + W(400) + "await app.openDocumentPicker(window.__wid,idxOf('계약서 작성'));" + W(900) + "const ds=await app._getAllRepoDocuments();window.__rdoc=ds.find(d=>/각서/.test(d.name));const r=document.querySelector('#documentRepoModal .fb-tbody tr[data-sel-key=\"'+window.__rdoc.id+'\"]');r&&r.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));" + W(400), "'#documentRepoModal .fb-pick-banner'")
scene("10_step3done", "document.querySelector('#documentRepoModal .fb-pick-foot .wfm-btn-primary').click();" + W(900) +
 "const w=wf();w.checklist[idxOf('대가 지급 (청구일부터 5일 안)')].tip={type:'text',content:['⚠ 청구서를 받은 날부터 5일 안에 지급해야 합니다','1. 검사조서·청구서·세금계산서를 붙여 지출 결의','근거: 시행령 제67조'].join(" + NL + "),saved:true};app.saveData();app._nwRenderMaterials();", "'#nwMaterials'")
scene("11_refpick", "app._nwGo(4);" + W(500) + "document.querySelector('#nwWhole .mat-btn.lib').click();" + W(1000) + "const fs=await app._getAllLibraryFiles();for(const f of fs.filter(x=>/시행령/.test(x.name))){const r=document.querySelector('#lawLibraryModal .fb-tbody tr[data-sel-key=\"'+f.id+'\"]');r&&r.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));" + W(250) + "}", "'#lawLibraryModal .fb-pick-foot'")
scene("12_step4", "document.querySelector('#lawLibraryModal .fb-pick-foot .wfm-btn-primary').click();" + W(1200), "'#nwWhole'")
# 만든 업무는 목록에 남겨 두고, 2장부터는 연습 업무(소모품 구매)로 일한다
scene("13_focus", "await app._nwFinish();" + W(1500) + "app.focusWorkflow(window.__pw);" + W(1200), "'#checklist-items-'+window.__pw")
# ── 2. 일하는 화면 (연습 업무)
scene("17_work", "const r=row('금액 기준 확인');r&&r.querySelector('.checklist-card-header').click();" + W(700) + "const ta=document.querySelector('.cl-peek .cl-result-input');if(ta){ta.value='추정가격 1,430만원 — 2천만원 이하라 1인 견적 가능';ta.dispatchEvent(new Event('input',{bubbles:true}));}" + W(300), "'.cl-peek'",
 hover="const t=row('1인 견적서 받기').querySelector('.item-title-text').getBoundingClientRect();return JSON.stringify([t.left+30,t.top+t.height/2])")
scene("18_result", "const ta=document.querySelector('.cl-peek .cl-result-input');const i0=px('금액 기준 확인 — 갈림길');ta&&await app.saveMainChecklistResultOnBlur(window.__pw,i0,ta);app.clearChecklistPick&&app.clearChecklistPick(window.__pw);" + W(300) +
 "const i=px('거래실례가격 조사 (2곳 이상)');await app.showChecklistItemModal(window.__pw,i,'result');" + W(700) +
 "const sh=document.getElementById('rf-shrink-'+window.__pw+'-'+i);if(sh)sh.checked=false;await app.addResultFiles(window.__pw,i,{files:[new File(['%PDF-1.4 '+'0'.repeat(150000)],'가격 조사표 (3곳 비교).pdf',{type:'application/pdf'}),new File([await img('조달청 가격정보',['사무용 의자 (메시형)','단가  172,000원 ~ 189,000원','조회일  2026. 10. 13.'],'#1e3a8a')],'조달청 가격정보 화면.jpg',{type:'image/jpeg'})],value:''});" + W(1300), "'#cimOverlay > div'")
scene("19_formats", "app.closeChecklistItemModal();" + W(300) + "const i=px('배제사유 확인 · 각서 받기');await app.showChecklistItemModal(window.__pw,i,'formats');" + W(700), "'#cimOverlay .mat-head'")
# 지금 할 일(1인 견적서 받기)에 예시를 넣어 업무 절차 패널 썸네일
scene("17b_thumbs", "app.closeChecklistItemModal();" + W(300) + "await app.addTipFiles(window.__pw,px('금액 기준 확인 — 갈림길'),{files:[new File([await img('수의계약 금액 기준',['2천만원 이하  1인 견적 가능','2천만원 초과  2인 이상 견적','200만원 미만  견적 생략 가능'],'#7c3aed')],'금액 기준 요약표.jpg',{type:'image/jpeg'}),new File(['%PDF-1.4 '+'0'.repeat(60000)],'추정가격 산정 예시.pdf',{type:'application/pdf'})],value:''});" + W(400) + "app.closeChecklistItemModal();const i=px('1인 견적서 받기');await app.addTipFiles(window.__pw,i,{files:[new File([await img('견적서 작성례',['품명  사무용 의자 (메시형)','수량  20개   단가  178,000원','견적일  2026. 11. 3.'],'#b91c1c')],'견적서 작성례.jpg',{type:'image/jpeg'}),new File([await img('견적 요청 메일',['받는 곳  ○○가구','제목  사무용 의자 견적 요청','회신  10. 24.까지'],'#065f46')],'견적 요청 메일 예시.jpg',{type:'image/jpeg'})],value:''});" + W(500) + "app.closeChecklistItemModal();app.refreshAIPanelDashboardIfNeeded();" + W(900), "'.proc-thumbs'")
scene("17c_pick", "app.toggleStageOpen(window.__pw,px('계약'));" + W(500) + "app.toggleChecklistPeek(window.__pw,px('배제사유 확인 · 각서 받기'));" + W(900), "'.proc-step-row.is-picked'")
# 넓게 보기 · 읽는 글 크기 (v1.5.7)
scene("17d_wide", "app.clearChecklistPick&&app.clearChecklistPick(window.__pw);app.toggleStageOpen(window.__pw,px('계약'));" + W(400) + "app.toggleProcWide(true);" + W(900), "'#aiPanel'")
scene("17e_font", "app.toggleProcWide(false);" + W(600) + "const b=document.getElementById('aiPanelFontBtn');const r=b.getBoundingClientRect();app.openReadScaleMenu({clientX:r.left,clientY:r.bottom+4,preventDefault(){},stopPropagation(){}});" + W(400), "'#fbCtxMenu'")
scene("20_refpop", "document.getElementById('fbCtxMenu').style.display='none';" + W(200) + "const m=document.querySelector('.ref-chip-more');m&&m.click();" + W(500), "'#refPop'")
scene("21_preview", "app._refPopClose();" + W(200) + "const fs=await app._getAllLibraryFiles();await app.previewLibraryFile(fs.find(x=>/시행령/.test(x.name)).id);" + W(2500), "'.pv-modal .modal-content'")
scene("21b_zoom", "document.querySelectorAll('.pv-modal').forEach(m=>m.remove());app.restoreBodyScroll&&app.restoreBodyScroll();" + W(300) + "app.previewTipFile(window.__pw,px('1인 견적서 받기'),0);" + W(1500) +
 "const pc=[...document.querySelectorAll('.pv-win #previewContent')].pop();const im=pc&&pc.querySelector('img');if(im){const r=im.getBoundingClientRect();app._pvZoomSet(pc,Math.max(1.4,app._pvZoomFit(pc,im)*2),r.left+r.width*0.42,r.top+r.height*0.5);}" + W(500), "[...document.querySelectorAll('.pv-zbar')].pop()")
# 오른쪽 클릭 메뉴 — 맨 위 체크 · 그 줄의 건너뛰기 버튼
scene("22_menu", "document.querySelectorAll('.pv-modal').forEach(m=>m.remove());app.restoreBodyScroll&&app.restoreBodyScroll();" + W(300) +
 "const r=row('금액 기준 확인');const h=r.querySelector('.checklist-card-header');const b=h.getBoundingClientRect();h.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:b.left+260,clientY:b.top+16}));" + W(400), "'#checklistItemMenu'")
scene("22a_panelmenu", "app._closeChecklistItemMenu();" + W(300) + "const D0=document.getElementById('aiPanelOfflineDashboard');const el=[...D0.querySelectorAll('.proc-sub-row:not(.proc-skip-sub)')].find(x=>x.offsetParent&&/1인 견적서/.test(x.textContent));if(el){const b=el.getBoundingClientRect();el.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:b.left+60,clientY:b.top+b.height/2}));}" + W(400), "'#checklistItemMenu'")
scene("22b_guide", "app._closeChecklistItemMenu&&app._closeChecklistItemMenu();await app.showChecklistHelp(window.__pw,px('1인 견적서 받기'));" + W(1200), "[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/_content$/.test(x.id)).pop()")
# 건너뛰기 실행 → 패널 제자리 표시 → ⤼ 표시 누르기
scene("40_practice_skip", "closeGuides();" + W(300) + "const bi=px('금액 기준 확인 — 갈림길');app.handleBranchOption(window.__pw,bi,pw().checklist[bi].branchOptions.findIndex(o=>o.label==='1인 견적'));" + W(700), "'#branchPreviewConfirmBtn'")
scene("22e_skip", "document.getElementById('branchPreviewConfirmBtn').click();" + W(1500) +
 "const sc=document.getElementById('aiPanelOfflineDashboard');const r0=sc&&sc.querySelector('.proc-skip-row, .proc-skip-sub');if(r0){sc.scrollTop+=r0.getBoundingClientRect().top-sc.getBoundingClientRect().top-200;}" + W(500), "document.querySelector('#aiPanelOfflineDashboard .proc-skip-row, #aiPanelOfflineDashboard .proc-skip-sub')")
scene("40b_skip_taken", "const bi=px('금액 기준 확인 — 갈림길');const b=document.querySelector('#focus-checklist-scroll-'+window.__pw+' .checklist-card[data-index=\"'+bi+'\"] .cl-skip-mark');b.scrollIntoView({block:'nearest'});" + W(400) + "b.click();" + W(500), "'#checklistItemMenu'")
scene("22d_checklist", "app._closeChecklistItemMenu();" + W(300) + "localStorage.setItem('progressReportOpts',JSON.stringify({...JSON.parse(localStorage.getItem('progressReportOpts')||'{}'),clResult:true,clSkipped:true}));app._prTab='checklist';app.openProgressReport(window.__pw);" + W(1300), "'#prPage'")
scene("41_practice_print", "const tr=[...document.querySelectorAll('#prPage tr')].find(r=>r.textContent.includes('나라장터'));if(tr)tr.scrollIntoView({block:'center'});" + W(500), "[...document.querySelectorAll('#prPage tr')].find(r=>r.textContent.includes('나라장터'))")
scene("22c_report", "document.querySelector('.pr-tabs [data-tab=report]').click();" + W(800), "'#progressReportModal .pr-win'")
# ── 3. 체크리스트 편집
scene("14_edit", "app.closeProgressReport&&app.closeProgressReport();" + W(400) + "app.enterFocusEditMode();" + W(800) + "const c=row('계약서 작성');c&&c.querySelector('.fci-card-header').dispatchEvent(new MouseEvent('click',{bubbles:true}));" + W(300), "'.fci-bar'")
scene("15_branch", "app._clClearSel&&app._clClearSel();const i=px('계약금액 확인 — 갈림길');app.startBranchPick(window.__pw,i,0);" + W(800) + "const L=document.getElementById('bpLabel');const sc=document.getElementById('focus-checklist-scroll-'+window.__pw);const r=row('계약금액 확인');if(r&&sc)sc.scrollTop+=r.getBoundingClientRect().top-sc.getBoundingClientRect().top-80;" + W(300), "'.bp-bar'")
scene("16_edit_tags", "app.cancelBranchPick();" + W(400) + "app.refreshFocusChecklist(pw());" + W(400) + "const sc=document.getElementById('focus-checklist-scroll-'+window.__pw);const r=row('계약금액 확인');if(r&&sc)sc.scrollTop+=r.getBoundingClientRect().top-sc.getBoundingClientRect().top-80;" + W(300) + "const t=document.querySelector('.fci-cond');t&&t.dispatchEvent(new MouseEvent('mouseenter'));" + W(300), "'.fci-mark-branch'")
# ── 4. 일정
scene("23_schedule", "document.querySelectorAll('.fci-cond').forEach(t=>t.dispatchEvent(new MouseEvent('mouseleave')));app.exitFocusEditMode();" + W(900) + "app.saveChecklistItemDeadlineDirect(window.__pw,px('1인 견적서 받기'),D(3));app.saveChecklistItemDeadlineDirect(window.__pw,px('납품 검사 (업체 참관)'),D(12));app.saveChecklistItemDeadlineDirect(window.__pw,px('대가 지급 (청구일부터 5일 안)'),D(19));" + W(500) + "app.openSchedule(null);" + W(900), "'#schedView'")
# ── 5. 업무 분담 (04 납품·검사 → 김민수, 05 대가 지급 → 이수진)
scene("24_collab", "app.closeSchedule();" + W(300) + "const w=pw();const c=app._collabEnsureOwner(w);c.steps=c.steps||{};c.steps[app.ensureChecklistItemId(w.checklist[px('납품·검사')])]={assignee:'김민수',status:'draft',deadline:D(14)};c.steps[app.ensureChecklistItemId(w.checklist[px('대가 지급')])]={assignee:'이수진',status:'draft',deadline:D(20)};c.team=['김민수','이수진'];app.saveData();"
 "app.openCollabModal(window.__pw,'send');" + W(1000), "'#collabModal .modal-content'")
scene("25_waiting", "document.getElementById('collabModal')?.remove();app.restoreBodyScroll&&app.restoreBodyScroll();const w=pw();Object.values(w.collab.steps).forEach(st=>{st.status='sent';st.sentAt=new Date().toISOString();});app.saveData();app.refreshFocusChecklist(w);" + W(700) + "const r=document.querySelector('.cb-run');r&&r.scrollIntoView({block:'center'});" + W(300), "'.cb-run'")
scene("25b_runmenu", "const r=document.querySelector('.cb-run .cb-run-pill');const b=r.getBoundingClientRect();r.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,clientX:b.left+b.width*0.62,clientY:b.bottom-6}));" + W(500), "'#fbCtxMenu'")
scene("25c_recall", "document.getElementById('fbCtxMenu').style.display='none';const w=pw();const sid=Object.keys(w.collab.steps).find(k=>w.collab.steps[k].status==='sent');app._collabAskRecall(w,sid);" + W(700), "[...document.querySelectorAll('.modal.show .modal-content')].pop()")
scene("26_sidebar", "[...document.querySelectorAll('.modal.show button')].find(b=>b.textContent.includes('회신 기다리기'))?.click();" + W(300) + "app.exitFocusMode();" + W(800) + "const t=document.querySelector('.filter-tab[data-mode=\"inProgress\"]');t&&t.click();" + W(600), "'.sidebar'")
scene("27_addressbook", "app.openAddressBook();" + W(800), "'#abModal .modal-content'")
# ── 6. 공유
scene("28_share", "app.closeAddressBook();" + W(300) + "app.showShareModal(window.__pw);" + W(900), "'#shareGoBtn'")
scene("28b_tipexclude", "app._shareClose();" + W(300) + "app._saveFileWithPicker=async()=>true;await app.exportMultipleWorkflowPackages([window.__pw]);" + W(900), "[...document.querySelectorAll('.toast')].pop()", keepToast=True)
# ── 7. 마무리 (월간 업무 실적 보고)
scene("29_done", "app._shareClose();" + W(300) + "app.focusWorkflow(window.__pm);" + W(1000) + "const w=app.allData.workflows.find(x=>x.id===window.__pm);"
 "w.checklist.forEach((it,i)=>{if(!app.normalizeCompleted(it)&&app._isSubEntry(it))app.toggleChecklistItem(w.id,i);});" + W(1600) +
 "w.checklist.forEach((it,i)=>{if(!app.normalizeCompleted(it))app.toggleChecklistItem(w.id,i);});" + W(1400), "'[onclick*=markWorkflowDone]'")
scene("30_main_done", "app.markWorkflowDone(window.__pm);" + W(900) + "if(app.focusMode)app.exitFocusMode();" + W(600) + "const t=document.querySelector('.filter-tab[data-mode=\"done\"]');t&&t.click();" + W(600), "'#workflowList'")
scene("31_reference", "app.openWorkflowManager();" + W(700) + "app.wfmSetTab('done');" + W(400) + "const tr=document.querySelector('#wfmTableBody tr[data-sel-key=\"'+window.__pm+'\"]');tr&&tr.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:600,clientY:320}));" + W(500), "'#wfmCtxMenu'")
scene("32_reftab", "document.getElementById('wfmCtxMenu').style.display='none';app.setReference(window.__pm,true);" + W(700) + "const mk=document.querySelector('#refRegisterModal [data-act=ok]');mk&&mk.click();" + W(1200) + "app.wfmSetTab('reference');" + W(700), "'#workflowManagerModal .wfm-tabs'")
scene("33_archive", "app.wfmSetTab('done');" + W(400) + "app.archiveTemplate(window.__old);" + W(900) + "app.wfmSetTab('archived');" + W(700), "'#wfmTableBody'")
scene("34_folders", "app.wfmSetTab('all');" + W(300) + "app._wfmCreateFolderAt('','회계·계약');app._wfmCreateFolderAt('','정기 보고');app._wfmCreateFolderAt('회계·계약','2026년');app.saveData();app._wfmMoveItems([window.__pw,window.__wid],[],'회계·계약/2026년');app._wfmMoveItems([window.__pm],[],'정기 보고');app.wfmSelectFolder('회계·계약/2026년');" + W(700), "'#wfmSidebar'")
# ── 8. 조직 자료
scene("35_law", "app.closeModal('workflowManagerModal');" + W(300) + "await app.openLawLibrary();" + W(900), "'#lawLibraryModal .modal-content'")
scene("35b_lawreplace", "const fs=await app._getAllLibraryFiles();const f0=fs.find(x=>/시행규칙/.test(x.name));app._fbCfg('law').upload([new File(['%PDF-1.4 new '+'1'.repeat(400)],f0.name,{type:'application/pdf',lastModified:Date.now()})],f0.groupId??null);" + W(1500), "[...document.querySelectorAll('.modal.show .modal-content')].pop()")
scene("36_repo", "const m=[...document.querySelectorAll('.modal.show')].pop();const c=m&&[...m.querySelectorAll('button')].find(b=>/취소|그대로|건너/.test(b.textContent));c?c.click():document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));" + W(600) + "app.closeModal('lawLibraryModal');" + W(300) + "await app.openDocumentRepo();" + W(900), "'#documentRepoModal .modal-content'")
scene("36b_repo_replace", "const ds=await app._getAllRepoDocuments();const d=ds.find(x=>/공개내역서/.test(x.name));app._fbCfg('repo').upload([new File(['새 판 '+'2'.repeat(400)],d.name,{type:d.type||'application/octet-stream'})],d.folderId??null);" + W(1500), "[...document.querySelectorAll('.modal.show .modal-content')].pop()")
# ── 9. 안전 · 설정
scene("37_trash", "document.getElementById('owCancelBtn')?.click();" + W(500) + "app.closeModal('documentRepoModal');" + W(300) + "app.allData.workflows.unshift({id:9990,type:'manual',title:'시험 삼아 만든 업무 (지운 것)',checklist:[{text:'연습',completed:false}],date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();app._wfmDeleteItems([9990],[]);" + W(600) + "app.openTrashModal();" + W(800) + "const it=document.querySelector('#trash-item-9990');it&&it.click();" + W(300), "'#trashModal .modal-content'")
scene("38_backup", "app.closeModal('trashModal');" + W(300) + "app.openPreferences('backup');" + W(900), "'#prefsModal .modal-content'")
scene("38b_prefs", "app.openMyInfo();" + W(900), "'#prefsModal .modal-content'")
# ── 10. 연습 업무 넣기 (메뉴)
scene("39_practice", "app.closeModal('prefsModal');" + W(300) + "if(app.focusMode)app.exitFocusMode();" + W(300) + "const t=document.querySelector('.filter-tab[data-mode=\"inProgress\"]');t&&t.click();" + W(300) + "document.querySelector('[onclick*=\"newWorkMenu\"]').click();" + W(500), "[...document.querySelectorAll('#newWorkMenu .mi')].pop()")
json.dump(S, open('steps.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
