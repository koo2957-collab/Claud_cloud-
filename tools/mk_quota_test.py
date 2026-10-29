# 브라우저 저장 공간(localStorage)이 가득 찼을 때 AI 편집이 「AI 정리 실패: … exceeded the quota」로 끝나던 것 시험 → steps3.json
# 확인: 예전 자동 백업 기록(backup_history_v6)을 가득 채움 → 진짜 callAI(통신만 가짜)로 AI 편집이 끝까지 됨(사용량 기록 저장 실패를 삼킴)
#       · 새로 고침하면 예전 자동 백업 기록이 지워져 공간이 돌아옴 · 5분마다 다시 쌓지 않음
# 실행: (tools 폴더에서) python mk_quota_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json
RS = {"items": [{"text": "접수", "indent": 0, "from": ["o0"], "change": "유지", "note": "", "warn": [], "tip": "", "basis": []},
                {"text": "서류 확인", "indent": 1, "from": ["o1"], "change": "유지", "note": "", "warn": [], "tip": "", "basis": []}],
      "removed": [], "branches": []}
q = lambda o: json.dumps(o, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7983;"
     "const used=()=>{let n=0;for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);n+=k.length+(localStorage.getItem(k)||'').length;}return Math.round(n/1024)+'KB'};"
     "const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body, **kw): S.append({"label": label, "js": P + body + E, **kw})
# 통신만 가짜: 진짜 callAI → trackAPICall → saveAIStats 길을 그대로 탐
FETCH = ("if(!window.__of)window.__of=window.fetch;window.fetch=async(u,o)=>{u=String(u);if(/^(data|blob):/.test(u))return window.__of(u,o);"
         "await W(200);return new Response(JSON.stringify({candidates:[{content:{parts:[{text:'" + q(RS) + "'}]},finishReason:'STOP'}],usageMetadata:{totalTokenCount:120}}),{status:200,headers:{'Content-Type':'application/json'}})};")
FILL = ("const big='x'.repeat(256*1024);const h=[];try{for(let i=0;i<40;i++){h.push({id:i,data:big});localStorage.setItem('backup_history_v6',JSON.stringify(h));}}catch(e){}"
        "let pn=0;for(let s=64*1024;s>=1;s=s/2|0){for(;;){try{localStorage.setItem('__pad'+(pn++),'y'.repeat(s));}catch(e){break}}}window.__pn=pn;"
        "let full=false;try{localStorage.setItem('__probe','z'.repeat(2048));localStorage.removeItem('__probe');}catch(e){full=true}")
SETUP = ("document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
         "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();app._wfHasProgress=()=>false;" + FETCH +
         "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);"
         "const cl=[{text:'접수',indent:0,completed:false},{text:'서류 확인',indent:1,completed:false}];"
         "app.allData.workflows.unshift({id:ID,type:'manual',title:'저장 공간 시험',checklist:cl,date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});cl.forEach(it=>app.ensureChecklistItemId(it));"
         "await app.saveDataImmediate();")
step("A 저장 공간 가득 채움(예전 자동 백업 기록) → 사용량 기록 저장", SETUP + FILL + "let err='없음';try{app.trackAPICall(true,100,'gemini-3.6-flash')}catch(e){err=e.message}return '가득 참='+full+' 사용='+used()+' | trackAPICall 오류='+err")
step("B 가득 찬 채로 AI 편집 → 끝까지(검토 화면)", "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));app.focusWorkflow(ID);await W(1200);await app.openAiRestructure(ID);await W(300);await app._aiRsStart();await W(600);const r='단계='+(app._aiRs&&app._aiRs.phase)+' | 알림='+tx($('toastMessage')).slice(0,60);app._aiRsClose();app.exitFocusMode?.();await W(500);return r")
S.append({"reload": 4000})
step("C 새로 고침 뒤: 예전 자동 백업 기록 지워짐·공간 돌아옴·되풀이 없음", "Object.keys(localStorage).filter(k=>k.startsWith('__pad')).forEach(k=>localStorage.removeItem(k));let ok=true;try{localStorage.setItem('__probe','z'.repeat(512*1024));localStorage.removeItem('__probe');}catch(e){ok=false}return '기록 남음='+(localStorage.getItem('backup_history_v6')!=null)+' | 500KB 저장='+ok+' | 사용='+used()+' | 자동 백업 타이머='+!!app.autoBackupInterval")
step("정리", "for(let i=0;i<2000;i++)localStorage.removeItem('__pad'+i);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.allData.geminiApiKey='';await app.saveDataImmediate();if(window.__of)window.fetch=window.__of;return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(S), '단계')
