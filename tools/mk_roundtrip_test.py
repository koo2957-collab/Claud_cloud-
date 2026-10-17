# 왕복 시험 대본 → steps3.json  (「하고 → 되돌리면/다시 켜면/옮겼다 오면 똑같아야」)
# A 새로 고침: 처리결과·첨부·업무팁 예시·해당 없음·건너뛰기·마감일·업무 분담·레퍼런스·처리완료·폴더·법령 새 판까지 해 둔 뒤 다시 켜도 그대로
# B 되돌리기: 동작마다 「하기 전 사진」과 [되돌리기]·Ctrl+Z 뒤 사진이 같아야 (체크 해당 없음·건너뛰기·건너뛰기 취소·완료 처리·삭제·업무 관리 삭제·편집 삭제·법령 새 판·새 업무 초기화)
# C 내보내기 → 가져오기(그대로): 할 일·처리결과·업무팁·첨부 이름·예시 이름·서식 연결 수가 같아야 (+ 복사하여 시작은 체크만 비어야)
# D 전체 백업 → 바꾸기 → 복원: 백업한 때와 같아야, 복원한 뒤 다시 켜도 같아야
# 실행: python mk_roundtrip_test.py [ai] && SELFCHECK=1 node cdp3.mjs <앱>   (ai: AI 허용판에서 가짜 AI로 AI 편집 결과도 넣고 확인)
import json, os, sys
AI = len(sys.argv) > 1 and sys.argv[1] == 'ai'
here = os.path.dirname(os.path.abspath(__file__))
CANON = open(os.path.join(here, 'canon.js'), encoding='utf-8').read()
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));" + CANON.replace("'canon ok'", "") +
     ";const wf=id=>app.allData.workflows.find(w=>w.id===id);const ix=(w,t)=>w.checklist.findIndex(i=>i.text===t);"
     "const undoBtn=()=>document.querySelector('#toastMessage .toast-undo-btn, #toastMessage button');"
     "const choice=()=>[...document.querySelectorAll('.modal.show')].reverse().find(m=>m.querySelector('button[data-choice]'));"
     "const snap=async(o)=>JSON.stringify(await __canon(o||{}));"
     "const same=async(a,o)=>{const d=__diff(JSON.parse(a),await __canon(o||{}),8);return d.length?'다름 ✗ '+d.join(' | '):'같음 ✓'};"
     "const fileOf=async(t,txt)=>new File([txt||('%PDF-1.4 '+t)],t,{type:/pdf$/.test(t)?'application/pdf':'image/png'});"
     "const img=async(t)=>{const c=document.createElement('canvas');c.width=200;c.height=120;const g=c.getContext('2d');g.fillStyle='#fde';g.fillRect(0,0,200,120);g.fillStyle='#333';g.font='20px sans-serif';g.fillText(t,10,60);return new File([await new Promise(r=>c.toBlob(r,'image/png'))],t+'.png',{type:'image/png'})};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split(String.fromCharCode(10))[1]}})()"
S = []
def step(l, b, **k): S.append({"label": l, "js": P + b + E, **k})
STUB = ("app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
        "app.callAI=app.callAIWithDocuments=async()=>JSON.stringify({items:[{id:'o1',warn:['AI가 넣은 주의'],tip:'AI 팁',basis:['AI 근거 제1조']}],branches:[]});"
        "const __of=window.fetch.bind(window);window.fetch=async(u,...a)=>{if(/^(data|blob):/.test(String(u&&u.url||u)))return __of(u,...a);throw new Error('시험: 외부 통신 막음')};") if AI else ""
step("준비", "localStorage.setItem('welcomeShown','1');localStorage.setItem('deadlineNotifyMode','off');document.getElementById('welcomeModal')?.remove();app.checkBackupReminder=()=>{};window.confirm=()=>true;"
     "app._collabSetMe({name:'홍길동',dept:'시험과',rank:'소방위'});app._collabSetMyName('홍길동');localStorage.setItem('authorInfoSet','1');" + STUB +
     "await app.insertPracticeWorkflows();await W(2500);const ps=app.allData.workflows.filter(w=>w.isPractice);window.__pw=ps.find(w=>/소모품/.test(w.title)).id;window.__pm=ps.find(w=>/월간/.test(w.title)).id;localStorage.setItem('__rt_ids',JSON.stringify([window.__pw,window.__pm]));return '업무='+app.allData.workflows.length")
# ── 자료를 골고루 만들기
step("자료 만들기: 체크·처리결과·첨부·예시·해당 없음·건너뛰기·마감일", "const w=wf(window.__pw);app.focusWorkflow(w.id);await W(1200);"
     "for(const t of ['구매 요청 받기 — 품목·수량·규격 확인','추정가격 정하기','거래실례가격 조사 (2곳 이상)']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}"
     "app.markNotApplicable(w.id,[ix(w,'예정가격 작성')],'1인 견적');await W(1300);"
     "const i=ix(w,'추정가격 정하기');w.checklist[i].result={text:'추정가격 1,430만원',summary:''};app.saveData();"
     "await app.addResultFiles(w.id,i,{files:[await fileOf('가격 조사표.pdf'),await img('견적 화면')],value:''});await W(800);"
     "await app.addTipFiles(w.id,ix(w,'1인 견적서 받기'),{files:[await img('견적서 작성례')],value:''});await W(600);app.closeChecklistItemModal?.();"
     "const bi=ix(w,'금액 기준 확인 — 갈림길');app.handleBranchOption(w.id,bi,w.checklist[bi].branchOptions.findIndex(o=>o.label==='1인 견적'));await W(500);document.getElementById('branchPreviewConfirmBtn').click();await W(1300);"
     "app.saveChecklistItemDeadlineDirect(w.id,ix(w,'1인 견적서 받기'),'2026-11-03');await W(300);"
     "const c=app._collabEnsureOwner(w);c.steps=c.steps||{};c.steps[w.checklist[ix(w,'납품·검사')].itemId]={assignee:'김민수',status:'draft',deadline:'2026-11-20'};app.saveData();"
     "return '할 일 끝='+w.checklist.filter(x=>app.normalizeCompleted(x)).length")
step("자료 만들기: 월간 업무 끝내기·처리완료·레퍼런스·폴더", "const m=wf(window.__pm);app.focusWorkflow(m.id);await W(1000);for(let k=0;k<2;k++)for(let i=0;i<m.checklist.length;i++){if(!app.normalizeCompleted(m.checklist[i])&&(k||app._isSubEntry(m.checklist[i]))){app.toggleChecklistItem(m.id,i);await W(1200);}}"
     "app.markWorkflowDone(m.id);await W(900);app.registerAsReference(m.id);await W(600);document.querySelector('#refRegisterModal [data-act=ok]')?.click();await W(1500);"
     "app._wfmCreateFolderAt('','회계');app._wfmMoveItems([window.__pw],[],'회계');await W(300);if(app.focusMode)app.exitFocusMode();await W(500);"
     "return '레퍼런스='+app.allData.workflows.filter(w=>w.isReference).length+' 폴더='+wf(window.__pw).folderPath")
if AI:
    step("(AI) AI 편집 「그대로」로 업무팁 더하기", "app.focusWorkflow(window.__pw);await W(1000);await app.openAiRestructure(window.__pw);await W(900);const keep=[...document.querySelectorAll('#aiRsModal input[type=radio], #aiRsModal label, #aiRsModal button')].find(e=>/keep/.test(e.value||'')||/체크리스트는 그대로/.test(e.textContent||''));keep&&keep.click();await W(200);if(app._aiRs&&app._aiRs.mode!=='keep')app._aiRs.mode='keep';await W(300);await app._aiRsStart();await W(1500);await app._aiRsApply?.();await W(1000);if(app.focusEditMode)app.exitFocusEditMode();await W(800);const w=wf(window.__pw);return 'AI 주의 들어감='+w.checklist.some(i=>/AI가 넣은 주의/.test(i.tip?.content||''))")
# ── A 새로 고침
step("A1 저장 → 사진 찍기", "if(app.focusMode)app.exitFocusMode();await app.saveDataImmediate();await W(1500);localStorage.setItem('__rt_a',await snap());return 'ok'")
S.append({"reload": 5500, "label": "A2 새로 고침"})
step("A3 다시 켠 뒤 같은가", "await W(500);return await same(localStorage.getItem('__rt_a'))")
# ── B 되돌리기
step("B0 준비", "const [pw,pm]=JSON.parse(localStorage.getItem('__rt_ids'));window.__pw=pw;window.__pm=pm;localStorage.setItem('welcomeShown','1');document.getElementById('welcomeModal')?.remove();window.confirm=()=>true;app.checkBackupReminder=()=>{};app.focusWorkflow(pw);await W(1200);return 'ok'")
UNDO = [
    ("B1 체크 → 다시 누르기(체크는 되돌리기 대신 다시 누름)", "const w=wf(window.__pw);const i=ix(w,'1인 견적서 받기');app.toggleChecklistItem(w.id,i);await W(1300);app.toggleChecklistItem(w.id,i);await W(1300);", None),
    ("B2 해당 없음 → [되돌리기]", "const w=wf(window.__pw);app.markNotApplicable(w.id,[ix(w,'수의계약 근거서류 갖추기')],'시험');await W(1200);", "btn"),
    ("B3 건너뛰기 취소 → [되돌리기]", "const w=wf(window.__pw);app._cancelBranchFromItem(w.id,ix(w,'금액 기준 확인 — 갈림길'));await W(1200);", "btn"),
    ("B4 업무 삭제 → [실행 취소]", "await app.deleteWorkflow(window.__pw);await W(900);", "btn"),
    ("B5 업무 관리 삭제 → Ctrl+Z", "app._wfmDeleteItems([window.__pw],[]);await W(800);", "ctrlz"),
    ("B6 처리완료 → [되돌리기]", "const r=app.allData.workflows.find(w=>!w.isDeleted&&!w.isReference&&w.completedProcessed);if(r){app.undoMarkWorkflowDone(r.id);await W(800);}", "btn"),
    ("B7 법령 새 판 → [되돌리기]", "const fs=await app._getAllLibraryFiles();app._fbReplaceVersionWith('law',fs[0].id,await fileOf('새 판 시험.pdf','%PDF-1.4 new'));await W(800);choice()?.querySelector('button[data-choice=\"0\"]').click();await W(1500);", "btn"),
    ("B8 편집에서 줄 삭제 → Ctrl+Z → 저장", "app.focusWorkflow(window.__pw);await W(1000);app.enterFocusEditMode();await W(700);document.querySelector('#fci-2 .fci-title-text').click();await W(200);app._fciCmd('del');await W(500);document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'z',code:'KeyZ',ctrlKey:true,bubbles:true}));await W(600);app.exitFocusEditMode();await W(1000);", None),
    ("B9 서식 새 판 → Ctrl+Z", "const ds=await app._getAllRepoDocuments();app._fbReplaceVersionWith('repo',ds[0].id,await fileOf('새 서식 판.docx','new'));await W(800);choice()?.querySelector('button[data-choice=\"0\"]').click();await W(1500);", "ctrlz"),
]
for label, act, how in UNDO:
    undo = "" if how is None else ("const b=undoBtn();if(!b)return '되돌리기 단추 없음 ✗';b.click();await W(1500);" if how == "btn" else "document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'z',code:'KeyZ',ctrlKey:true,bubbles:true}));await W(1500);")
    step(label, "const before=await snap({times:false});" + act + undo + "const d=__diff(JSON.parse(before),await __canon({times:false}),8);return d.length?'다름 ✗ '+d.join(' | '):'같음 ✓'")
step("B10 새 업무 [초기화] → [되돌리기] (작성 중 내용)", "if(app.focusMode)app.exitFocusMode();await W(400);app.openModal('manualModal');await W(600);document.getElementById('manualProjectName').value='초기화 왕복';app._nwGo(2);await W(300);document.querySelector('#checklistItems .checklist-edit-item input').value='단계 하나';app.addChecklistItem('할 일 둘',1);app._nwGo(3);await W(500);const a=document.getElementById('manualProjectName').value+'|'+[...document.querySelectorAll('#checklistItems .checklist-edit-item input')].map(i=>i.value).join(',');document.querySelector('#manualModal .nw-reset').click();await W(500);undoBtn()?.click();await W(800);const b=document.getElementById('manualProjectName').value+'|'+[...document.querySelectorAll('#checklistItems .checklist-edit-item input')].map(i=>i.value).join(',');app.closeModal('manualModal');await W(400);choice()?.querySelector('button[data-choice=\"1\"]')?.click();await W(600);return a===b?'같음 ✓ '+a:'다름 ✗ '+a+' → '+b")
# ── C 내보내기 → 가져오기
step("C1 연습 업무 내보내기 → 그대로 가져오기", "let blob=null;app._saveFileWithPicker=async b=>{blob=b;return true};const before=await __canon({ids:false,times:false,live:true});await app.exportMultipleWorkflowPackages([window.__pw]);await W(800);app._restoreFromFile([new File([await blob.text()],'x.json')]);await W(900);document.querySelector('input[name=pkgImportMode][value=asIs]').click();await app._confirmPackageImport();await W(1500);"
     "const after=await __canon({ids:false,times:false,live:true});const k=Object.keys(before.wf).find(k=>/소모품/.test(k));const nw=app.allData.workflows.filter(w=>!w.isDeleted&&/소모품/.test(w.title)).sort((a,b)=>b.id-a.id)[0];window.__imp=nw.id;"
     "const strip=o=>{const x=JSON.parse(JSON.stringify(o));x.cl=x.cl.map(c=>({...c,at:undefined}));return x};const one=await __canon({ids:true,times:false});const d=__diff(strip(before.wf[k]),strip(one.wf[String(nw.id)]),10).filter(x=>!/^(title|folder|ref|done|del|collab|deadline)/.test(x));return '가져온 업무='+nw.title+' · '+(d.length?'다름 ✗ '+d.join(' | '):'할 일·처리결과·업무팁·첨부·예시·서식 같음 ✓')")
step("C2 같은 파일 「복사하여 시작」 → 체크·처리결과·첨부만 비어야", "let blob=null;app._saveFileWithPicker=async b=>{blob=b;return true};await app.exportMultipleWorkflowPackages([window.__pw]);await W(800);app._restoreFromFile([new File([await blob.text()],'x.json')]);await W(900);document.querySelector('input[name=pkgImportMode][value=new]').click();await app._confirmPackageImport();await W(1500);"
     "const nw=app.allData.workflows.filter(w=>!w.isDeleted&&/소모품/.test(w.title)).sort((a,b)=>b.id-a.id)[0];const o=wf(window.__pw);const c=(await __canon()).wf[String(nw.id)];"
     "const bad=[];if(c.cl.some(x=>x.c))bad.push('체크 남음');if(c.cl.some(x=>x.r))bad.push('처리결과 남음');if(c.cl.some(x=>x.rf.length))bad.push('처리결과 첨부 남음');if(c.cl.map(x=>x.t).join()!==o.checklist.map(x=>x.text).join())bad.push('할 일 다름');if(!c.cl.some(x=>x.tip))bad.push('업무팁 사라짐');if(!c.cl.some(x=>x.tf.length))bad.push('예시 사라짐');return bad.length?'✗ '+bad.join(', '):'체크만 비고 업무팁·예시·서식 그대로 ✓'")
# ── D 백업 → 바꾸기 → 복원
step("D1 전체 백업 → 사진", "window.__bk=await app._buildFullBackupObject();app._hideProgress?.();localStorage.setItem('__rt_d',await snap());window.__bkTxt=JSON.stringify(window.__bk);return '업무='+window.__bk.data.workflows.length")
step("D2 바꾸기(삭제·새 업무·체크)", "await app.deleteWorkflow(window.__imp);await W(600);app.allData.workflows.unshift({id:Date.now(),type:'manual',title:'백업 뒤 만든 업무',checklist:[{text:'a',completed:false}],date:'x'});const w=wf(window.__pw);app.toggleChecklistItem(w.id,ix(w,'1인 견적서 받기'));await W(1300);app.saveData();return 'ok'")
step("D3 백업 파일로 복원 → 백업한 때와 같은가", "window.confirm=()=>true;app._downloadJsonFile=()=>{};app._restoreFromFile([new File([window.__bkTxt],'b.json')]);await W(7000);return await same(localStorage.getItem('__rt_d'))")
step("D4 저장", "await app.saveDataImmediate();await W(1500);return 'ok'")
S.append({"reload": 5500, "label": "D5 새로 고침"})
step("D6 복원한 뒤 다시 켜도 같은가", "await W(500);return await same(localStorage.getItem('__rt_d'))")
out = os.path.join(here, 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
