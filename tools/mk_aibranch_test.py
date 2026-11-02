# AI 편집 「건너뛰기 버튼 추천」 → 고르기 → 넣기 → [저장] → 새로 고침까지 건너뛰기 버튼이 남는지 (가짜 AI) → steps3.json
#   K: 업무팁·근거만 보태기 · R: 체크리스트 다시 정리 · 후보 기본 체크 여부 · 일하는 화면 단추 · 실제로 누르면 건너뜀
# 실행: (tools 폴더에서) python mk_aibranch_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json
ID = 7988
def js(o): return json.dumps(o, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
KEEP = {"items": [{"id": "o1", "warn": ["금액 기준 확인"], "tip": "", "basis": []}], "branches": [{"at": "o1", "label": "2천만원 이하", "skip": ["o2"]}]}
RS = {"items": [{"text": "계약 준비", "indent": 0, "from": ["o0"], "change": "유지"}, {"text": "금액 기준 확인", "indent": 1, "from": ["o1"], "change": "유지"},
                {"text": "나라장터 공고", "indent": 1, "from": ["o2"], "change": "유지"}, {"text": "계약서 작성", "indent": 1, "from": ["o3"], "change": "유지"}],
      "removed": [], "branches": [{"at": 1, "label": "2천만원 이하", "skip": [2]}]}
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const tx=e=>e?e.textContent.replace(/\\s+/g,' ').trim():'(없음)';const wf=()=>app.allData.workflows.find(w=>w.id===ID);"
     "const br=()=>wf().checklist.map(x=>(x.branchOptions||[]).map(o=>x.text+'→['+o.label+':'+(o.targetItemIds||[]).map(id=>(wf().checklist.find(y=>y.itemId===id)||{}).text).join(',')+']').join(' ')).filter(Boolean).join(' / ')||'(없음)';"
     "const cand=()=>[...document.querySelectorAll('#aiRsModal .aip-row.br')].map(r=>(r.querySelector('input').checked?'☑':'☐')+tx(r).slice(0,70)).join(' / ');"
     "const btns=()=>[...document.querySelectorAll('#focus-checklist-scroll-'+ID+' .branch-option-btn, #focus-checklist-scroll-'+ID+' [onclick*=handleBranchOption]')].map(b=>tx(b)).join(',')||'(단추 없음)';")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
MK = ("const mk=(t,i)=>{const o={text:t,indent:i,completed:false};app.ensureChecklistItemId(o);return o};"
      "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);"
      "app.allData.workflows.unshift({id:ID,type:'manual',title:'건너뛰기 추천 시험',checklist:[mk('계약 준비',0),mk('금액 기준 확인',1),mk('나라장터 공고',1),mk('계약서 작성',1)],date:'2026. 11. 2.',createdAt:new Date().toISOString(),folderPath:''});await app.saveDataImmediate();")
ADD = {"adds": [{"id": "n1", "after": "o1", "text": "2인 견적서 받기", "why": "수의계약 견적"}], "branches": [{"at": "o1", "label": "2천만원 이하", "skip": ["n1", "o2", "o3"]}]}
STUB = ("app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
        "app.callAI=app.callAIWithDocuments=async p=>{window.__lastP=p;await W(200);return /빠진 할 일만/.test(p)?'" + js(ADD) + "':/바꾸지 말고/.test(p)?'" + js(KEEP) + "':'" + js(RS) + "'};")
OPEN = "app.focusWorkflow(ID);await W(1300);app.enterFocusEditMode();await W(500);await app.openAiRestructure(ID);await W(600);"
TOAST = "window.__toasts=[];if(!app.__tw){app.__tw=1;const o=app.showToast.bind(app);app.showToast=(...a)=>{window.__toasts.push(String(a[2]||''));return o(...a)};}"
PREP = lambda mode: ("document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};" + STUB + MK + OPEN +
    "app._aiRsMode('" + mode + "');app._aiRs.wantBranch=true;await W(200);await app._aiRsStart();for(let k=0;k<40&&app._aiRs.phase!=='review';k++)await W(200);" + TOAST)
for mode, lab in (('keep', 'K 업무팁·근거만 보태기'), ('restructure', 'R 다시 정리')):
    step(lab + ' — 준비·추천 받기(후보 처음부터 ☑)', PREP(mode) + "return '단계='+app._aiRs.phase+' | 후보='+cand()+' | 단추='+tx($('aiRsApplyBtn'))")
    step(lab + ' — 아무것도 안 누르고 넣기', "$('aiRsApplyBtn').click();await W(800);return '넣은 뒤 버튼='+br()+' | 알림='+window.__toasts.join(' / ')")
    step(lab + ' — [저장] → 일하는 화면', "app.exitFocusEditMode();await W(1200);return '버튼='+br()+' | 화면 단추='+btns()")
    S.append({"reload": 3000})
    step(lab + ' — 새로 고침 뒤', "await W(500);return '버튼='+br()")
step('U 후보를 풀고 넣기 → 알림에 넣지 않은 후보', PREP('keep') + "const c=document.querySelector('#aiRsModal .aip-row.br input');c.click();await W(200);const t=tx($('aiRsApplyBtn'));$('aiRsApplyBtn').click();await W(800);return '단추='+t+' | 버튼='+br()+' | 알림='+window.__toasts.join(' / ')")
step('P 다시 정리: 버튼 다는 줄의 단계를 풀면 후보도 풀림', PREP('restructure') + "const st=app._aiRs;const b0=cand();app._aiRsToggle(0,false);await W(200);const b1=cand();app._aiRsToggle(1,true);await W(200);return '처음='+b0+' | 단계 풂='+b1+' | 다시 고른 뒤='+cand()+' | 단추='+tx($('aiRsApplyBtn'))")
step('A 빠진 할 일 더하기: 계약서 작성(o3)은 끝냄 → 후보 처음부터 ☑ · 끝낸 줄은 건너뛸 대상에서 빠짐', PREP('add').replace("await app._aiRsStart()", "wf().checklist[3].completed=true;wf().checklist[3].completedAt=new Date().toISOString();app._aiRs.old[3].done=true;await app._aiRsStart()") + "return '요청 글 branches='+/branches/.test(window.__lastP)+' | 후보='+cand()+' | 단추='+tx($('aiRsApplyBtn'))")
step('A2 새 할 일을 풀면 후보는 남음(원래 줄 o2가 대상) → 넣기', "const r=document.querySelector('#aiRsModal .aip-row.add input');r.click();await W(200);const c1=cand()+' | 단추='+tx($('aiRsApplyBtn'));document.querySelector('#aiRsModal .aip-row.add input').click();await W(200);const c2=cand();$('aiRsApplyBtn').click();await W(800);return '새 할 일 풂='+c1+' | 다시 고름='+c2+' || 넣은 뒤 줄='+wf().checklist.map(x=>x.text).join('/')+' | 버튼='+br()+' | 알림='+window.__toasts.join(' / ')")
step('A3 [저장] → 새로 고침 뒤', "app.exitFocusEditMode();await W(1200);const a=btns();return '화면 단추='+a")
S.append({"reload": 3000})
step('A4 새로 고침 뒤', "await W(500);return '버튼='+br()")
step('정리', "app._aiRsClose?.();app.exitFocusEditMode?.();app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);await app.saveDataImmediate();return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
