import json
S = []
def W(ms=600): return f"await new Promise(r=>setTimeout(r,{ms}));"
NL = "String.fromCharCode(10)"
HL = ("const R=(sel)=>{const el=typeof sel==='string'?document.querySelector(sel):sel;if(!el)return null;const r=el.getBoundingClientRect();return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)}};"
      "const toastOff=()=>document.querySelectorAll('.toast, .toast-container > *').forEach(t=>t.remove());"
      "const wf=()=>app.allData.workflows.find(w=>w.id===window.__wid);"
      "const row=(txt)=>[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text, .fci-title-text')?.textContent.trim().startsWith(txt));"
      "const idxOf=(t)=>wf().checklist.findIndex(x=>x.text===t);"
      "const D=(n)=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};")
def scene(name, code, hl=None, keepToast=False):
    ret = f"return JSON.stringify({{hl: R({hl})}})" if hl else "return JSON.stringify({hl:null})"
    S.append({"label": name, "js": "(async()=>{try{" + HL + code + ("" if keepToast else "toastOff();") + W(300) + ret + "}catch(e){return JSON.stringify({err:e.message})}})()"})
    S.append({"wait": 300, "shot": "man2/" + name + ".png"})

# 예시 체크리스트 만들기 (단계·할 일)
def cl(rows, day0):
    out = []
    for k, (t, i, c) in enumerate(rows):
        ca = (",completedAt:'2026-10-%02dT%02d:20:00'" % (min(10, day0 + k // 2), 9 + k % 8)) if c else ""
        out.append("{text:" + json.dumps(t, ensure_ascii=False) + ",indent:" + str(i) + ",completed:" + ("true" if c else "false") + ca + "}")
    return "[" + ",".join(out) + "]"
contract = cl([("구매 요구",0,True),("물품 구매 요구서 접수",1,True),("예산 배정 확인",1,True),
    ("계약 방법 결정",0,True),("추정가격 산정",1,True),("견적서 받기 (2천만 원 이하 수의계약)",1,True),
    ("계약 체결",0,True),("계약서 작성·날인",1,True),
    ("납품·검사",0,False),("납품 확인",1,True),("검사·검수 조서 작성",1,False),
    ("대가 지급",0,False),("대가 지급 청구서 접수",1,False),("지출 결의·지급 (청구 후 5일 이내)",1,False)], 2)
audit = cl([("사건 접수",0,True),("기관 통보 공문 접수",1,True),("사건 배당",1,True),
    ("조사 계획 수립",0,True),("조사 계획서 작성·결재",1,True),
    ("출석 요구",0,False),("출석요구서 발송 (조사 기일 3일 전)",1,True),("진술거부권 등 권리 사전 고지",1,False),
    ("문답 조사",0,False),("문답서 작성",1,False),("확인서·증거자료 받기",1,False),
    ("결과 보고",0,False),("감찰 결과 보고서 작성",1,False),("징계 의결 요구 여부 판단",1,False)], 1)

# ── 준비: 조직 자료 · 진행 중인 업무 · 주소록
scene("00_seed",
 "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.removeItem('lastDeadlineNotifyDate');localStorage.setItem('deadlineNotifyMode','daily');"
 "localStorage.setItem('collabMyName','홍길동');"
 "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
 "app.allData.libraryGroups=[{id:501,name:'징계·감찰',parentId:null},{id:502,name:'회계·계약',parentId:null}];"
 "const mk=(id,name,g,txt)=>app.dbManager.saveFile('lawLibrary',{id,name,size:new Blob([txt]).size*40,uploadedAt:'2026-09-01T09:00:00Z',groupId:g,blob:new Blob([txt],{type:'text/plain'}),type:'text/plain'});"
 "await mk(7401,'소방공무원 징계령.txt',501,'소방공무원 징계령 (시연용 요약)'+" + NL + "+" + NL + "+'· 징계위원회 출석통지: 회의 3일 전까지 도달'+" + NL + "+'· 징계처분: 의결 통보를 받으면 처분사유설명서를 교부'+" + NL + "+'※ 실제 업무에서는 국가법령정보센터의 현행 조문을 확인하세요.');"
 "await mk(7402,'공무원 징계령.txt',501,'공무원 징계령 (시연용 요약)'+" + NL + "+'· 제10조 출석: 출석통지서는 회의 3일 전까지 도달하도록');"
 "await mk(7403,'소방감찰규정.txt',501,'소방감찰규정 (시연용 요약)'+" + NL + "+'· 출석요구: 조사 기일 3일 전까지 통지'+" + NL + "+'· 진술거부권 등 권리를 사전에 고지');"
 "await mk(7404,'지방계약법 시행령.txt',502,'지방자치단체를 당사자로 하는 계약에 관한 법률 시행령 (시연용 요약)'+" + NL + "+'· 제25조: 추정가격 2천만 원 이하 물품·용역은 수의계약 가능'+" + NL + "+'· 제67조: 검사 후 청구받은 날부터 5일 이내 대가 지급');"
 "const rd=(name)=>app.dbManager.saveFile('repoDocuments',{name,size:38000,blob:new Blob(['(시연용 서식) '+name],{type:'text/plain'}),type:'text/plain',folderId:null,uploadedAt:'2026-09-01T09:00:00Z',updatedAt:'2026-09-01T09:00:00Z',tags:[]});"
 "window.__rd={};for(const n of ['징계의결요구서.txt','출석통지서.txt','처분사유설명서.txt','출석요구서(감찰).txt','문답서.txt','물품 구매 요구서.txt','검사·검수 조서.txt','지출결의서.txt'])window.__rd[n]=await rd(n);await app._loadRepoDocMetaCache();"
 "app._collabSavePeople([{name:'김민수',dept:'감사팀'},{name:'이수진',dept:'감사팀'},{name:'박정훈',dept:'회계팀'},{name:'최예린',dept:'인사팀'}]);"
 "const now=new Date().toISOString();"
 "const B={id:8101,type:'manual',title:'개인보호장비 구매 계약 및 대가 지급',checklist:" + contract + ",deadline:D(1),date:'2026. 9. 28.',createdAt:'2026-09-28T09:00:00Z',folderPath:''};"
 "const C={id:8102,type:'manual',title:'공무원 범죄 기관통보 사건 감찰조사',checklist:" + audit + ",deadline:D(-2),date:'2026. 9. 20.',createdAt:'2026-09-20T09:00:00Z',folderPath:''};"
 "app.allData.workflows.unshift(B,C);[B,C].forEach(w=>w.checklist.forEach(it=>app.ensureChecklistItemId(it)));"
 "const cc=app._collabEnsureOwner(C);cc.team=['이수진'];cc.steps={};const si=C.checklist.findIndex(x=>x.text==='문답 조사');cc.steps[C.checklist[si].itemId]={assignee:'이수진',status:'sent',deadline:D(2),sentAt:now};"
 "app.saveData();app.displayWorkflows();" + W(900))
# ── 0. 하루의 시작: 마감 임박 알림 · 사이드바
scene("01_main", "", "'.sidebar, #sidebarUrgent, .urgent-section'")
scene("02_banner", "app.checkDeadlineNotifications();" + W(900), "'#deadlineBanner'", keepToast=True)
scene("03_notify", "document.getElementById('deadlineBanner')?.classList.remove('show');const b=document.getElementById('deadlineBanner');if(b)b.style.display='none';app.toggleNotifyCenter();" + W(700), "'#notifyCenterMenu'")
# ── 1. 새 업무 만들기 (징계처분)
scene("04_newmenu", "if(document.getElementById('notifyCenterMenu')?.classList.contains('show'))app.toggleNotifyCenter();document.body.click();" + W(300) + "document.querySelector('[onclick*=\"newWorkMenu\"]').click();" + W(400), "'#newWorkMenu'")
scene("05_step1", "app.closeAllDropdowns();app.openModal('manualModal');" + W(500) + "document.getElementById('manualProjectName').value='소방장 품위유지의무 위반 징계처분';", "'#manualProjectName'")
scene("06_step2", "app._nwGo(2);" + W(500) + "const box=document.getElementById('checklistItems');const first=box.querySelector('.checklist-edit-item input');"
 "const rows=[['징계 의결 요구',0],['감찰 결과 보고서 접수',1],['징계의결요구서 작성·제출',1],['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송 (회의 3일 전 도달)',1],['심의·의결',0],['징계위원회 출석·진술',1],['징계 의결서 수령',1],['징계 처분',0],['처분사유설명서 작성',1],['처분사유설명서 교부',1],['인사기록 등재',1],['종결',0],['소청심사 청구 안내',1],['종결 보고',1]];"
 "if(first)first.value=rows[0][0];rows.slice(first?1:0).forEach(([t,i])=>app.addChecklistItem(t,i));" + W(300) + "const sc=box.closest('.nw-body')||box.parentElement;sc.scrollTop=0;", "'#checklistItems'")
scene("07_step3", "app._nwGo(3);" + W(600) + "window.__wid=app._nw.wfId;", "'#nwMaterials'")
scene("08_tip", "app._nwOpenItem(idxOf('출석통지서 발송 (회의 3일 전 도달)'),'tip');" + W(800) + "const i=idxOf('출석통지서 발송 (회의 3일 전 도달)');const ta=document.querySelector('#cimOverlay .checklist-tip-textarea');app.switchTipToEditMode(window.__wid,i);"
 "ta.value=['1. 출석통지서는 회의 3일 전까지 도달해야 합니다 (발송일이 아니라 도달일 기준)','2. 직접 교부가 어려우면 등기우편 + 문자로 함께 알리고 수령 증빙을 남깁니다','3. 진술권 포기 시 진술권 포기서를 받아 둡니다'].join(" + NL + ");ta.dispatchEvent(new Event('input',{bubbles:true}));ta.dispatchEvent(new Event('blur'));" + W(900), "'#cimOverlay > div'")
scene("08b_tipfiles", "const i=idxOf('출석통지서 발송 (회의 3일 전 도달)');const mk=async(t,c)=>{const cv=document.createElement('canvas');cv.width=900;cv.height=600;const g=cv.getContext('2d');g.fillStyle='#fdfaf2';g.fillRect(0,0,900,600);g.fillStyle=c;g.font='bold 54px sans-serif';g.fillText(t,160,130);g.fillStyle='#333';g.font='30px sans-serif';['등기번호 1234-5678-9012','수령인  김○○ (본인)','수령일  2026. 10. 19.'].forEach((x,k)=>g.fillText(x,180,250+k*80));return await new Promise(r=>cv.toBlob(r,'image/jpeg',0.9));};await app.addTipFiles(window.__wid,i,{files:[new File([await mk('등기우편물 수령증','#b91c1c')],'등기 수령증 예시.jpg',{type:'image/jpeg'}),new File(['%PDF-1.4 '+'0'.repeat(120000)],'출석통지서 작성례.pdf',{type:'application/pdf'})],value:''});" + W(1000), "'#tf-'+window.__wid+'-'+idxOf('출석통지서 발송 (회의 3일 전 도달)')")
scene("09_fmpick", "app.closeChecklistItemModal();" + W(300) + "await app.openDocumentPicker(window.__wid,idxOf('출석통지서 발송 (회의 3일 전 도달)'));" + W(900) + "const r=document.querySelector('#documentRepoModal .fb-tbody tr[data-sel-key=\"'+window.__rd['출석통지서.txt']+'\"]');r&&r.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));" + W(400), "'#documentRepoModal .fb-pick-banner'")
scene("10_step3done", "document.querySelector('#documentRepoModal .fb-pick-foot .wfm-btn-primary').click();" + W(900) +
 "const w=wf();const put=(t,n)=>{const it=w.checklist[idxOf(t)];it.linkedDocs=[...(it.linkedDocs||[]),window.__rd[n]];};put('징계의결요구서 작성·제출','징계의결요구서.txt');put('처분사유설명서 작성','처분사유설명서.txt');"
 "w.checklist[idxOf('처분사유설명서 교부')].tip={type:'text',content:'1. 의결 통보를 받은 뒤 처분사유설명서에 의결서 사본을 붙여 교부'+" + NL + "+'2. 교부 일자를 기록 — 소청 기간 계산의 기준',saved:true};app.saveData();app._nwRenderMaterials();", "'#nwMaterials'")
scene("11_refpick", "app._nwGo(4);" + W(500) + "document.querySelector('#nwWhole .mat-btn.lib').click();" + W(1000) + "for(const id of [7401,7402]){const r=document.querySelector('#lawLibraryModal .fb-tbody tr[data-sel-key=\"'+id+'\"]');r&&r.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));" + W(250) + "}", "'#lawLibraryModal .fb-pick-foot'")
scene("12_step4", "document.querySelector('#lawLibraryModal .fb-pick-foot .wfm-btn-primary').click();" + W(1200), "'#nwWhole'")
# ── 2. 일하는 화면
scene("13_focus", "await app._nwFinish();" + W(1500) + "if(!app.focusMode)app.focusWorkflow(window.__wid);" + W(900), "'#checklist-items-'+window.__wid")
# ── 3. 체크리스트 편집 · 건너뛰기
scene("14_edit", "app.enterFocusEditMode();" + W(700) + "const c=row('징계 의결서 수령');c&&c.querySelector('.fci-card-header').dispatchEvent(new MouseEvent('click',{bubbles:true}));" + W(300), "'.fci-bar'")
scene("15_branch", "const w=wf();const cl=w.checklist;const i=idxOf('징계 의결서 수령');const a=idxOf('징계 처분'),b=idxOf('종결');const tg=cl.slice(a,b);"
 "app.startBranchPick(window.__wid,i,null);" + W(500) + "const L=document.getElementById('bpLabel');L.value='불문·경고 의결';app._branchPick.label=L.value;app.toggleBranchPickItem(window.__wid,a);app.refreshFocusChecklist(w);" + W(600) + "document.getElementById('focus-checklist-scroll-'+window.__wid).scrollTop=380;" + W(300), "'.bp-bar'")
scene("16_edit_tags", "app.saveBranchPick();" + W(400) + "app.refreshFocusChecklist(wf());" + W(400) + "document.getElementById('focus-checklist-scroll-'+window.__wid).scrollTop=260;" + W(300) + "const t=document.querySelector('.fci-cond');t&&t.dispatchEvent(new MouseEvent('mouseenter'));" + W(300), "'.fci-mark-branch'")
scene("17_work", "document.querySelectorAll('.fci-cond').forEach(t=>t.dispatchEvent(new MouseEvent('mouseleave')));app.exitFocusEditMode();" + W(900) +
 "['감찰 결과 보고서 접수','징계의결요구서 작성·제출'].forEach(t=>app.toggleChecklistItem(window.__wid,idxOf(t)));" + W(1500) +
 "const r=row('위원 구성·회의 일정 확정');r&&r.querySelector('.checklist-card-header').click();" + W(600) + "const ta=document.querySelector('.cl-peek .cl-result-input');if(ta){ta.value='위원 5명 구성, 10.23.(금) 14:00 소회의실';ta.dispatchEvent(new Event('input',{bubbles:true}));}" + W(300), "'.cl-peek'")
scene("18_result", "const ta=document.querySelector('.cl-peek .cl-result-input');const i0=idxOf('위원 구성·회의 일정 확정');ta&&await app.saveMainChecklistResultOnBlur(window.__wid,i0,ta);app.toggleChecklistItem(window.__wid,i0);" + W(600) +
 "const i=idxOf('출석통지서 발송 (회의 3일 전 도달)');await app.showChecklistItemModal(window.__wid,i,'result');" + W(700) +
 "const rt=document.getElementById('main-checklist-result-text-'+window.__wid+'-'+i);if(rt){rt.value='10.16.(금) 등기우편 발송, 10.19.(월) 수령 확인 (회의 4일 전 도달)';rt.dispatchEvent(new Event('input',{bubbles:true}));}"
 "const sh=document.getElementById('rf-shrink-'+window.__wid+'-'+i);if(sh)sh.checked=false;await app.addResultFiles(window.__wid,i,{files:[new File(['%PDF-1.4 '+'0'.repeat(186000)],'출석통지서_발송본.pdf',{type:'application/pdf'}),await (async()=>{const cv=document.createElement('canvas');cv.width=900;cv.height=600;const g=cv.getContext('2d');g.fillStyle='#fdfaf2';g.fillRect(0,0,900,600);g.fillStyle='#b91c1c';g.font='bold 54px sans-serif';g.fillText('등기우편물 수령증',220,120);g.fillStyle='#333';g.font='30px sans-serif';['등기번호 1234-5678-9012','수령인  김○○ (본인)','수령일  2026. 10. 19.'].forEach((t,k)=>g.fillText(t,200,240+k*80));g.strokeStyle='#b91c1c';g.lineWidth=6;g.beginPath();g.arc(720,470,70,0,7);g.stroke();const b=await new Promise(r=>cv.toBlob(r,'image/jpeg',0.9));return new File([b],'등기 수령증.jpg',{type:'image/jpeg'});})()],value:''});" + W(1300), "'#cimOverlay > div'")
scene("19_formats", "const i=idxOf('출석통지서 발송 (회의 3일 전 도달)');app.switchChecklistItemTab(window.__wid,i,'formats');" + W(500), "'#cimOverlay .mat-head'")
scene("17b_thumbs", "app.closeChecklistItemModal();" + W(400) + "app.refreshAIPanelDashboardIfNeeded();" + W(900), "'.proc-thumbs'")
scene("20_refpop", "app.closeChecklistItemModal();" + W(400) + "const m=document.querySelector('.ref-chip-more');m&&m.click();" + W(500), "'#refPop'")
scene("21_preview", "app._refPopClose();" + W(200) + "await app.previewLibraryFile(7401);" + W(900), "'.pv-modal .modal-content'")
scene("22_menu", "document.querySelectorAll('.pv-modal').forEach(m=>m.remove());app.restoreBodyScroll&&app.restoreBodyScroll();" + W(300) +
 "const r=row('출석통지서 발송');const h=r.querySelector('.checklist-card-header');const b=h.getBoundingClientRect();h.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:b.left+240,clientY:b.top+16}));" + W(400), "'#checklistItemMenu'")
scene("22b_guide", "app._closeChecklistItemMenu&&app._closeChecklistItemMenu();await app.showChecklistHelp(window.__wid,idxOf('출석통지서 발송 (회의 3일 전 도달)'));" + W(1200), "[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/_content$/.test(x.id)).pop()")
scene("23_schedule", "[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>!/_(content|closeBtn|footerCloseBtn)$/.test(x.id)).forEach(m=>m.remove());document.body.style.overflow='';document.body.style.position='';document.body.style.top='';app._closeChecklistItemMenu&&app._closeChecklistItemMenu();app.saveFocusDeadline(window.__wid,D(18));app.saveChecklistItemDeadlineDirect(window.__wid,idxOf('출석통지서 발송 (회의 3일 전 도달)'),D(6));app.saveChecklistItemDeadlineDirect(window.__wid,idxOf('처분사유설명서 교부'),D(16));" + W(500) + "app.openSchedule(null);" + W(900), "'#schedView'")
# ── 4. 업무 분담
scene("24_collab", "document.getElementById('schedView')?.remove();document.querySelectorAll('.sched-overlay').forEach(e=>e.remove());" + W(200) +
 "const w=wf();const c=app._collabEnsureOwner(w);const si=idxOf('징계위원회 개최 준비');c.steps=c.steps||{};c.steps[app.ensureChecklistItemId(w.checklist[si])]={assignee:'김민수',status:'draft',deadline:D(3)};c.team=['김민수'];app.saveData();"
 "app.openCollabModal(window.__wid,'send');" + W(700) + "const d=document.getElementById('cbSetupDept');if(d){d.value='감사팀';document.getElementById('cbSetupRank').value='소방위';document.getElementById('cbSetupName').value='홍길동';app.saveCollabMe('cbSetup');}" + W(900), "'#collabModal .modal-content'")
scene("25_waiting", "document.getElementById('collabModal')?.remove();const w=wf();const c=w.collab;Object.values(c.steps).forEach(st=>{st.status='sent';st.sentAt=new Date().toISOString();});app.saveData();app.refreshFocusChecklist(w);" + W(700), "'.cb-run'")
scene("25b_runmenu", "const r=document.querySelector('.cb-run .cb-run-pill');const b=r.getBoundingClientRect();r.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,clientX:b.left+b.width*0.62,clientY:b.bottom-6}));" + W(500), "'#fbCtxMenu'")
scene("25c_recall", "document.getElementById('fbCtxMenu').style.display='none';const w=wf();const sid=Object.keys(w.collab.steps).find(k=>w.collab.steps[k].status==='sent');app._collabAskRecall(w,sid);" + W(700), "[...document.querySelectorAll('.modal.show .modal-content')].pop()")
scene("26_sidebar", "[...document.querySelectorAll('.modal.show button')].find(b=>b.textContent.includes('회신 기다리기'))?.click();" + W(300) + "app.exitFocusMode();" + W(800) + "const t=document.querySelector('.filter-tab[data-mode=\"inProgress\"]');t&&t.click();" + W(600), "'.sidebar'")
scene("27_addressbook", "app.openAddressBook();" + W(800), "'#abModal .modal-content'")
# ── 5. 공유
scene("28_share", "app.closeAddressBook();" + W(300) + "app.showShareModal(8101);" + W(900), "'#shareGoBtn'")
# ── 6. 회신 받고 마무리 → 완료 · 레퍼런스 · 보관
scene("29_done", "app._shareClose();" + W(300) + "app.focusWorkflow(window.__wid);" + W(900) + "const w=wf();Object.values(w.collab.steps).forEach(st=>{st.status='replied';st.repliedAt=new Date().toISOString();});"
 "w.checklist.forEach((it,i)=>{if(!app.normalizeCompleted(it)&&it.skipped!==true&&app._isSubEntry(it))app.toggleChecklistItem(window.__wid,i);});" + W(1600) +
 "w.checklist.forEach((it,i)=>{if(!app.normalizeCompleted(it)&&it.skipped!==true)app.toggleChecklistItem(window.__wid,i);});" + W(1400), "'[onclick*=markWorkflowDone]'")
scene("30_main_done", "app.markWorkflowDone(window.__wid);" + W(900) + "if(app.focusMode)app.exitFocusMode();" + W(600) + "const t=document.querySelector('.filter-tab[data-mode=\"done\"]');t&&t.click();" + W(600), "'#workflowList'")
scene("31_reference", "app.openWorkflowManager();" + W(700) + "app.wfmSetTab('done');" + W(400) + "const tr=document.querySelector('#wfmTableBody tr[data-sel-key=\"'+window.__wid+'\"]');tr&&tr.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:600,clientY:320}));" + W(500), "'#wfmCtxMenu'")
scene("32_reftab", "document.getElementById('wfmCtxMenu').style.display='none';app.setReference(window.__wid,true);" + W(700) + "const mk=[...[...document.querySelectorAll('.modal.show')].pop().querySelectorAll('button')].find(b=>b.textContent.trim()==='만들기');mk&&mk.click();" + W(1200) + "app.wfmSetTab('reference');" + W(700), "'#workflowManagerModal .wfm-tabs'")
scene("33_archive", "app.wfmSetTab('done');" + W(400) + "app.archiveTemplate(window.__wid);" + W(900) + "app.wfmSetTab('archived');" + W(700), "'#wfmTableBody'")
scene("34_folders", "app.wfmSetTab('all');" + W(300) + "app._wfmCreateFolderAt('','징계·감찰');app._wfmCreateFolderAt('','회계·계약');app._wfmCreateFolderAt('징계·감찰','2026년');app.saveData();app._wfmMoveItems([window.__wid,8102],[],'징계·감찰/2026년');app._wfmMoveItems([8101],[],'회계·계약');app.wfmSelectFolder('징계·감찰/2026년');" + W(700), "'#wfmSidebar'")
# ── 7. 조직 자료 · 안전
scene("35_law", "app.closeModal('workflowManagerModal');" + W(300) + "await app.openLawLibrary();" + W(900), "'#lawLibraryModal .modal-content'")
scene("36_repo", "app.closeModal('lawLibraryModal');" + W(300) + "await app.openDocumentRepo();" + W(900), "'#documentRepoModal .modal-content'")
scene("37_trash", "app.closeModal('documentRepoModal');" + W(300) + "app.allData.workflows.unshift({id:9990,type:'manual',title:'연습용 업무 (지운 것)',checklist:[{text:'연습',completed:false}],date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();app._wfmDeleteItems([9990],[]);" + W(600) + "app.openTrashModal();" + W(800) + "const it=document.querySelector('#trash-item-9990');it&&it.click();" + W(300), "'#trashModal .modal-content'")
scene("38_backup", "app.closeModal('trashModal');" + W(300) + "app.openPreferences('backup');" + W(900), "'#prefsModal .modal-content'")
json.dump(S, open('steps.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
