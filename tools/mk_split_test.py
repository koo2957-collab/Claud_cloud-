# 할 일 잘게 나누기 규칙 시험 대본 → steps3.json (가짜 AI)
# 확인: AI 편집·AI로 채우기 요청 글에 「따로 끝내고 따로 체크할 수 있는 일 하나」 규칙 · 끝낸 한 줄을 나누면 나뉜 줄도 모두 ✓
# 실행: (tools 폴더에서) python mk_split_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json, os
SPLIT = {"items": [
    {"text": "감사장 설치", "indent": 0, "from": ["o0"], "change": "유지", "note": "", "warn": [], "tip": "", "basis": []},
    {"text": "컴퓨터 대여", "indent": 1, "from": ["o1"], "change": "수정", "note": "두 가지 일을 나눔", "warn": [], "tip": "", "basis": []},
    {"text": "프린터 설치", "indent": 1, "from": ["o1"], "change": "수정", "note": "두 가지 일을 나눔", "warn": [], "tip": "", "basis": []},
    {"text": "테이블 설치", "indent": 1, "from": ["o2"], "change": "수정", "note": "두 가지 일을 나눔", "warn": [], "tip": "", "basis": []},
    {"text": "다과 배치", "indent": 1, "from": ["o2"], "change": "수정", "note": "두 가지 일을 나눔", "warn": [], "tip": "", "basis": []}],
    "removed": [], "branches": []}
FILL = {"items": [{"text": "감사장 설치", "indent": 0}, {"text": "컴퓨터 대여", "indent": 1}, {"text": "테이블 설치", "indent": 1}], "branches": []}
q = lambda o: json.dumps(o, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7995;const wf=()=>app.allData.workflows.find(w=>w.id===ID);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = [
    {"label": "A AI 편집: 요청 글 규칙 · 끝낸 줄을 나누면 둘 다 ✓", "js": P +
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
     "window.__p=[];app.callAIWithDocuments=app.callAI=async(p)=>{window.__p.push(p);await W(200);return /다시 정리해 주세요/.test(p)?'" + q(SPLIT) + "':'" + q(FILL) + "'};"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i,d)=>{const o={text:t,indent:i,completed:!!d};if(d)o.completedAt=new Date().toISOString();app.ensureChecklistItemId(o);return o};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'감사장 준비',checklist:[mk('감사장 설치',0),mk('컴퓨터·프린터 설치',1,true),mk('테이블 설치 및 다과 배치',1)],date:'2026. 10. 15.',createdAt:new Date().toISOString(),folderPath:''});"
     "app.focusWorkflow(ID);await W(1300);app.enterFocusEditMode();await W(500);await app.openAiRestructure(ID);await W(300);await app._aiRsStart();await W(500);"
     "const p=window.__p[0]||'';const notes=[...document.querySelectorAll('#aiRsModal .aip-row')].map(r=>r.title).filter(Boolean).join(',');await app._aiRsApply();await W(500);"
     "return '규칙='+/따로 끝내고 따로 체크할 수 있는 일 하나/.test(p)+' 나눌 때 규칙='+/두 가지 일을 나눔/.test(p)+' | 바꾼 까닭='+notes.slice(0,30)+' | 줄='+wf().checklist.map(x=>(x.indent?'└':'')+x.text+(x.completed?'✓':'')).join(' / ')" + E},
    {"label": "B AI로 채우기 요청 글에도 같은 규칙", "js": P +
     "app._discardFocusEdit?.();app.focusEditMode=false;app.exitFocusMode();await W(600);app.openModal('manualModal');await W(700);$('manualProjectName').value='감사장 준비';app._nwGo(2);await W(300);app._toggleManualAiSection();await W(200);$('manualContent').value='감사장 설치';await app.fillChecklistWithAI();await W(400);"
     "const p=window.__p[window.__p.length-1]||'';return '규칙='+/따로 끝내고 따로 체크할 수 있는 일 하나/.test(p)+' 다과 예='+/다과 배치/.test(p)+' 2~8개='+/2~8개/.test(p)" + E},
    {"label": "정리", "js": P + "app._aiFillPreviewClose?.();app._nwClosing=true;app.closeModal('manualModal');app._nwClosing=false;const id=app._nw&&app._nw.wfId;app._nw=null;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&w.id!==id&&!/감사장 준비/.test(w.title||''));app._allowMassDelete=true;app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'" + E}]
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
