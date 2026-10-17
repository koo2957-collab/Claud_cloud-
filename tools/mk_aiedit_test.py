# 체크리스트 편집 안의 「✨ AI 편집」 시험 대본 → steps3.json (예전 mk_rs_test·mk_rs2_test를 대신함)
# 확인: 왼쪽 [AI로 다시 정리] 없음 · [AI 기안] 기본 숨김 · 편집 명령 줄 「✨ AI 편집」 → 창(짧은 안내·무엇을 할까요·업무팁/근거/건너뛰기 따로·⤢)
#       · 다시 정리 → 사본 없이 편집 중 체크리스트에(진행 상태 그대로) → [되돌리기] / [편집 취소]로 버림 / [저장]으로 반영(합쳐진 항목 예시 사진 옮김)
#       · 체크리스트는 그대로 → 원래 업무팁 유지·없는 줄만 더함 · 목록 오른쪽 클릭 「✨ AI 편집」 → 업무 열고 편집 + 창
#       · 환경설정 「AI 기안 단추」 → 보임 · 처음 쓸 때 외부 AI 안내
# 실행: (tools 폴더에서) python mk_aiedit_test.py && node cdp3.mjs "<저장소>/ai_test .html"   (가짜 AI)
#       배포판: python mk_aiedit_test.py locked && node cdp3.mjs "<저장소>/index.html"   (AI 편집·AI 기안 없음)
import json, os, sys
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
RS = {"items": [
    {"text": "접수", "indent": 0, "from": ["o0"], "change": "수정", "note": "", "warn": [], "tip": "접수 대장에 적습니다", "basis": []},
    {"text": "출석요구서 발송 (회의 5일 전)", "indent": 1, "from": ["o1"], "change": "이동", "note": "", "warn": ["회의 5일 전까지 도달"], "tip": "", "basis": ["공무원 징계령 제10조"]},
    {"text": "진술 기회 부여", "indent": 1, "from": ["o2", "o4"], "change": "수정", "note": "합침", "warn": [], "tip": "", "basis": []},
    {"text": "징계 의결", "indent": 0, "from": ["o3"], "change": "유지", "note": "", "warn": [], "tip": "", "basis": []}],
    "removed": [], "branches": [{"at": 2, "label": "진술 포기", "skip": [1]}]}
KEEP = {"items": [{"id": "o0", "warn": ["접수일부터 30일 안에"], "tip": "접수 대장에 적기", "basis": ["징계 규정 제5조"]}], "branches": []}
q = lambda o: json.dumps(o, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7981;"
     "const wf=()=>app.allData.workflows.find(w=>w.id===ID);const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';const M=()=>$('aiRsModal');"
     "const fap=t=>[...document.querySelectorAll('.fap-btn')].some(b=>b.textContent.includes(t));"
     "const lines=()=>wf().checklist.map(x=>(x.indent?'└':'')+x.text+(x.completed?'✓':'')).join(' / ');"
     "const st=()=>'일하는 화면='+!!app.focusMode+' 편집='+!!app.focusEditMode+' 사본='+app.allData.workflows.filter(w=>/AI 정리본/.test(w.title||'')).length;")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(expr): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(120);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(14,b.width/2),b.top+b.height/2])" + E}); S.append({"clickpt": 1})
STUB = "window.__calls=[];app.callAIWithDocuments=app.callAI=async(p)=>{window.__calls.push(p);await W(300);return /바꾸지 말고/.test(p)?'" + q(KEEP) + "':'" + q(RS) + "'};"
SETUP = ("document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};localStorage.removeItem('showAiDraft');localStorage.removeItem('aiDraftWarned');"
         + ("" if LOCKED else "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB) +
         "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&!/AI 정리본/.test(w.title||''));"
         "const cl=[['사건 접수','접수 대장에 적기'],['출석요구서 발송',''],['진술서 받기',''],['징계위원회 개최',''],['중복 항목','']].map(([t,tip])=>({text:t,indent:0,completed:false,...(tip?{tip:{type:'text',content:tip,saved:true}}:{})}));"
         "cl[0].completed=true;cl[0].completedAt=new Date().toISOString();app.allData.workflows.unshift({id:ID,type:'manual',title:'AI 편집 시험',checklist:cl,date:'2026. 10. 15.',createdAt:new Date().toISOString(),folderPath:''});cl.forEach(it=>app.ensureChecklistItemId(it));window.__ids=cl.map(x=>x.itemId);"
         "app.checklistDetails[ID+'-t-'+cl[4].itemId]={attachments:[{id:'tf1',name:'예시.png',type:'image/png'}]};"
         + ("" if LOCKED else "for(const f of await app._getAllLibraryFiles()){if(/공무원 징계령|징계 시험 지침/.test(f.name))await app.dbManager.deleteFile('lawLibrary',f.id);}const lf=new File([\"제1조(목적) 이 영은 공무원 징계에 관하여 정한다.\\n제10조(출석 통지) 출석요구서는 징계위원회 회의 5일 전까지 혐의자에게 도달하여야 한다.\\n제12조(진술) 징계 혐의자에게 진술할 기회를 주어야 한다.\"],'공무원 징계령.txt',{type:'text/plain'});window.__lid=await app.dbManager.saveFile('lawLibrary',{name:lf.name,type:lf.type,size:lf.size,blob:lf,uploadDate:new Date().toISOString(),groupId:null});const lf2=new File(['제2조(감경) 표창이 있으면 징계를 감경할 수 있다. 진술 기회와 출석요구서 도달을 확인한다.'],'징계 시험 지침.txt',{type:'text/plain'});window.__lid2=await app.dbManager.saveFile('lawLibrary',{name:lf2.name,type:lf2.type,size:lf2.size,blob:lf2,uploadDate:new Date().toISOString(),groupId:null});await app._linkLibraryDocs(ID,[window.__lid]);") +
         "await app.saveDataImmediate();app.focusWorkflow(ID);await W(1300);")
step("준비 → 왼쪽 패널: [AI로 다시 정리] 없음 · [AI 기안] 기본 숨김", SETUP + "return st()+' | AI로 다시 정리='+fap('AI로 다시 정리')+' AI 기안='+fap('AI 기안')+' | 줄='+lines()")
click("[...document.querySelectorAll('.fap-btn')].find(b=>/체크리스트 편집/.test(b.textContent))")
step("A 체크리스트 편집 → 명령 줄 「✨ AI 편집」", "await W(700);const b=document.querySelector('.fci-bar .fci-ai');return st()+' | AI 편집 단추='+tx(b)")
if LOCKED:
    step("배포판: 환경설정 AI 탭에 AI 기안 칸 없음", "app.cancelFocusEditMode();await W(500);app.openPreferences('ai');await W(500);const r='칸='+[...document.querySelectorAll('.prefs-row')].some(x=>/AI 기안 단추/.test(x.textContent));app.closeModal('prefsModal');return r")
else:
    click("document.querySelector('.fci-bar .fci-ai')")
    step("A2 누름 → AI 편집 창", "await W(500);return '제목='+tx(M().querySelector('h3'))+' | 안내='+tx(M().querySelector('.rs-secure')).slice(0,30)+' | 고르기='+[...M().querySelectorAll('.rs-mode b')].map(b=>b.textContent).join('/')+' | 아래 안내='+tx(M().querySelector('.rs-note'))")
    click("M().querySelector('.rs-foot .btn-primary')")
    step("B 다시 정리 → 비교 화면: 끝난 단계 알림·근거 표시·보낸 조문", "await W(900);const p=window.__calls[window.__calls.length-1]||'';return '알림='+tx(M().querySelector('.rs-reopen')).slice(0,60)+' | 근거='+[...M().querySelectorAll('.aip-row .aip-b')].map(b=>b.textContent).filter(t=>/근거/.test(t)).join(',')+' | 보낸 조문='+/### 참고 자료: 공무원 징계령/.test(p)+' 원래 업무팁 유지 규칙='+/원래 업무팁에 없는 내용만/.test(p)+' | 넣기 단추='+tx($('aiRsApplyBtn'))+' | 아래 안내='+tx(M().querySelector('.rs-note')).slice(0,40)")
    click("M().querySelector('.aip-row.br input')")
    click("$('aiRsApplyBtn')")
    step("B2 넣기 → 사본 없이 편집 중 체크리스트에·진행 상태 그대로", "await W(700);return st()+' | 창='+!!M()+' | 줄='+lines()+' | 접수 업무팁='+JSON.stringify(wf().checklist[0].tip&&wf().checklist[0].tip.content)+' | 건너뛰기='+JSON.stringify((wf().checklist.find(x=>x.text==='진술 기회 부여')?.branchOptions||[]).map(o=>o.label))+' | 알림='+tx($('toastMessage')).slice(0,50)")
    step("B3 알림 [되돌리기] → AI 편집 전으로(편집은 계속)", "const b=[...document.querySelectorAll('#toast button')].find(x=>/되돌리기/.test(x.textContent));b.click();await W(500);return st()+' | 줄='+lines()")
    step("B4 [법령·매뉴얼에서 더하기] → 연결 안 된 자료도 고름", "await app.openAiRestructure(ID);await W(300);const n0=app._aiRs.files.length;await app._aiRsPickLibrary();await W(900);app._fbPick.sel.add(window.__lid2);app._fbPickDone('law');await W(800);const r='자료 '+n0+'→'+app._aiRs.files.length+' ('+app._aiRs.files.map(f=>f.name).join(', ')+') | 업무에 연결됨='+((app.checklistDetails['project-'+ID]||{}).linkedLibraryDocs||[]).length;app._aiRsClose();return r")
    step("C 다시 AI 편집 → 넣기 → [편집 취소] → 저장 안 함", "await app.openAiRestructure(ID);await W(300);await app._aiRsStart();await W(500);await app._aiRsApply();await W(500);const a=lines();app.cancelFocusEditMode();await W(400);const d=[...document.querySelectorAll('.modal.show')].pop();[...d.querySelectorAll('button')].find(b=>/저장 안 함/.test(b.textContent)).click();await W(600);return '넣은 뒤='+a+' || 취소 뒤: '+st()+' | 줄='+lines()")
    step("D 편집 → AI 편집 → 넣기 → [저장] → 반영·예시 사진이 합친 항목으로", "app.enterFocusEditMode();await W(500);await app.openAiRestructure(ID);await W(300);await app._aiRsStart();await W(500);await app._aiRsApply();await W(500);app.exitFocusEditMode();await W(700);const t=wf().checklist.find(x=>x.text==='진술 기회 부여');const d=app.checklistDetails[ID+'-t-'+t.itemId];return st()+' | 줄='+lines()+' | 합친 항목 예시='+JSON.stringify((d&&d.attachments||[]).map(a=>a.name))+' | 업무팁(출석요구서)='+JSON.stringify(wf().checklist[1].tip&&wf().checklist[1].tip.content)")
    step("E 그대로 모드: 편집 → AI 편집 → 그대로 → 넣기 → 저장", "app.enterFocusEditMode();await W(500);await app.openAiRestructure(ID);await W(300);app._aiRsMode('keep');await app._aiRsStart();await W(500);await app._aiRsApply();await W(500);const a=st();app.exitFocusEditMode();await W(600);return '넣은 뒤 '+a+' | 접수 업무팁='+JSON.stringify(wf().checklist[0].tip.content)")
    step("F 목록 오른쪽 클릭 「✨ AI 편집」", "app.exitFocusMode();await W(900);const el=document.querySelector('[data-sel-key=\"'+ID+'\"]');app._mainCtx({preventDefault(){},stopPropagation(){},clientX:300,clientY:300,currentTarget:el,target:el},ID);await W(200);const m=[...document.querySelectorAll('body > div')].reverse().find(d=>d.textContent.includes('폴더로 옮기기'));const it=m&&[...m.querySelectorAll('*')].find(x=>x.children.length===0&&/AI 편집/.test(x.textContent));return '메뉴='+(it?tx(it):'없음')+' 사본 글자='+!!(m&&/사본/.test(m.textContent))")
    step("F2 그 메뉴 → 업무 열고 편집 + 창", "document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));await app.openAiRestructure(ID);await W(400);const r=st()+' | 창='+!!M();app._aiRsClose();app.cancelFocusEditMode();await W(400);return r")
    step("G 환경설정 → AI 기안 단추 보임", "app.openPreferences('ai');await W(500);const row=[...document.querySelectorAll('.prefs-row')].find(x=>/AI 기안 단추/.test(x.textContent));[...row.querySelectorAll('.prefs-choice button')].find(b=>b.textContent==='보임').click();await W(400);app.closeModal('prefsModal');await W(300);return '칸='+!!row+' | 왼쪽 AI 기안='+fap('AI 기안')")
    click("[...document.querySelectorAll('.fap-btn')].find(b=>/AI 기안/.test(b.textContent))")
    step("G2 처음 누르면 외부 AI 안내", "await W(300);const d=[...document.querySelectorAll('.modal.show')].pop();const r='안내='+tx(d&&d.querySelector('h2'))+' / '+tx(d&&d.querySelector('p')).slice(0,40);d&&d.querySelector('[data-choice=cancel]').click();await W(200);localStorage.removeItem('showAiDraft');return r")
step("정리", "app._aiRsClose?.();if(app.focusEditMode)app._discardFocusEdit?.();app.focusEditMode=false;app.exitFocusMode?.();await W(600);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);for(const k of [window.__lid,window.__lid2])if(k)await app.dbManager.deleteFile('lawLibrary',k);app._allowMassDelete=true;app.allData.geminiApiKey='';localStorage.removeItem('showAiDraft');localStorage.removeItem('aiDraftWarned');await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
