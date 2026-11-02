# AI 업무팁 중복 줄이기 시험 (가짜 AI) → steps3.json
#   K: AI 편집 「업무팁·근거만」 · R: 「다시 정리」 · A: 「빠진 할 일 더하기」 · F: 새 업무 「AI로 채우기」
#   단계 업무팁(단계 공통)에 있는 줄은 뺌 · 같은 단계 여러 할 일에 같은 줄은 단계에 한 번 · 숫자(기한·조문)가 다르면 다른 줄
#   · 요청 글에 「단계 공통 업무팁」·중복 규칙 · 검토 화면 「같은 내용 n줄 뺌」 · 실제 클릭으로 넣기
# 실행: (tools 폴더에서) python mk_dedup_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json
ID = 7989
def js(o): return json.dumps(o, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
KEEP = {"items": [
    {"id": "o1", "warn": ["예산 확인", "금액 2천만원 기준 확인", "계약 기간 10일 확인"], "tip": "", "basis": ["지방계약법 시행령 제25조"]},
    {"id": "o2", "warn": ["금액 2천만원 기준 확인"], "tip": "", "basis": ["지방계약법 시행령 제25조 (3쪽)"]},
    {"id": "o3", "warn": ["계약 기간 7일 확인"], "tip": "계약 기간 7일 확인\n도장 받기", "basis": ["지방계약법 시행령 제26조"]}], "branches": []}
RS = {"items": [
    {"text": "계약 준비", "indent": 0, "from": ["o0"], "change": "유지", "warn": [], "tip": "", "basis": []},
    {"text": "금액 기준 확인", "indent": 1, "from": ["o1"], "change": "유지", "warn": ["예산 확인", "검수 조서는 3일 안에"], "tip": "", "basis": []},
    {"text": "견적서 받기", "indent": 1, "from": ["o2"], "change": "유지", "warn": ["검수 조서는 3일 안에"], "tip": "", "basis": []},
    {"text": "계약서 작성", "indent": 1, "from": ["o3"], "change": "유지", "warn": [], "tip": "", "basis": []}], "removed": [], "branches": []}
ADD = {"adds": [
    {"after": "o1", "text": "예산 부서 협의하기", "why": "예산", "warn": ["예산 확인", "협의 기록 남기기"], "tip": "", "basis": []},
    {"after": "o2", "text": "견적 비교표 만들기", "why": "견적", "warn": ["협의 기록 남기기"], "tip": "", "basis": []}]}
FILL = {"items": [
    {"text": "구매 준비", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "금액 기준 확인", "indent": 1, "warn": ["추정가격은 부가세를 뺀 금액"], "tip": "예산서와 맞춰 봅니다", "basis": ["지방계약법 시행령 제30조"]},
    {"text": "견적서 받기", "indent": 1, "warn": ["추정가격은 부가세를 뺀 금액"], "tip": "2곳 이상에서 받습니다", "basis": ["지방계약법 시행령 제30조"]},
    {"text": "구매 요청서 쓰기", "indent": 1, "warn": [], "tip": "", "basis": ["지방계약법 시행령 제31조"]},
    {"text": "계약", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "계약서 작성", "indent": 1, "warn": ["추정가격은 부가세를 뺀 금액"], "tip": "", "basis": []}], "branches": []}
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const tx=e=>e?e.textContent.replace(/\\s+/g,' ').trim():'(없음)';const wf=()=>app.allData.workflows.find(w=>w.id===ID);"
     "const tips=()=>wf().checklist.map(x=>x.text+'='+((x.tip&&x.tip.content)||'').replace(/\\n/g,' / ')).join(' ‖ ');"
     "const note=()=>tx(document.querySelector('#aiRsModal .rs-dedup'));")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(expr): S.append({"pt": True, "js": P + "const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(12,b.width/2),b.top+b.height/2])" + E})
def click(expr): pt(expr); S.append({"clickpt": 1})
MK = ("const mk=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
      "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);"
      "app.allData.workflows.unshift({id:ID,type:'manual',title:'업무팁 중복 시험',checklist:[mk('계약 준비',0,'⚠ 예산 확인'),mk('금액 기준 확인',1),mk('견적서 받기',1,'근거: 지방계약법 시행령 제30조'),mk('계약서 작성',1)],date:'2026. 11. 2.',createdAt:new Date().toISOString(),folderPath:''});await app.saveDataImmediate();")
STUB = ("app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
        "app.callAI=app.callAIWithDocuments=async p=>{window.__lastP=p;await W(200);return /빠진 할 일만/.test(p)?'" + js(ADD) + "':/바꾸지 말고/.test(p)?'" + js(KEEP) + "':'" + js(RS) + "'};")
OPEN = "app.focusWorkflow(ID);await W(1300);app.enterFocusEditMode();await W(500);await app.openAiRestructure(ID);await W(600);"
PREP = lambda mode: ("document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};app._wfHasProgress=()=>false;" + STUB + MK + OPEN +
    "app._aiRsMode('" + mode + "');app._aiRs.wantTips=true;app._aiRs.wantBasis=true;await W(200);await app._aiRsStart();for(let k=0;k<40&&app._aiRs.phase!=='review';k++)await W(200);")
RULE = "'요청 글: 단계 공통 업무팁='+/단계 공통 업무팁: (\\[1\\] )?⚠ 예산 확인/.test(window.__lastP)+' · 중복 규칙='+/단계에 한 번만 쓰고|단계 공통 업무팁」\\(그 단계 할 일 모두에 보임\\)/.test(window.__lastP)+' · 줄 수='+/warn은 2줄, tip은 3줄까지/.test(window.__lastP)"

# K 업무팁·근거만
step('K 업무팁·근거만 — 추천 받기 · 검토 화면', PREP('keep') + "const rows=[...document.querySelectorAll('#aiRsModal .aip-row.rs-keep')].map(r=>tx(r)).join(' ‖ ');return " + RULE + "+' | 알림 글='+note()+' | 줄='+rows")
click("$('aiRsApplyBtn')")
step('K 넣은 뒤 업무팁', "await W(800);return tips()")
# R 다시 정리
step('R 다시 정리 — 추천 받기', PREP('restructure') + "return " + RULE + "+' | 알림 글='+note()")
click("$('aiRsApplyBtn')")
step('R 넣은 뒤 업무팁', "await W(800);return tips()")
# A 빠진 할 일 더하기 (원래 줄은 손대지 않음 → 단계에 모으지 않고 처음 한 번만)
step('A 빠진 할 일 더하기 — 찾기', PREP('add') + "return " + RULE + "+' | 알림 글='+note()")
click("$('aiRsApplyBtn')")
step('A 넣은 뒤 업무팁(원래 줄 그대로)', "await W(800);return tips()")
step('A 정리', "app._aiRsClose?.();app.exitFocusEditMode?.();await W(800);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);await app.saveDataImmediate();app.goHome?.();await W(500);return 'ok'")
# F AI로 채우기
step('F 새 업무 ② AI로 채우기 — 미리 보기', "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "app.callAI=app.callAIWithDocuments=async p=>{window.__lastP=p;await W(200);return '" + js(FILL) + "'};"
     "app.openModal('manualModal');await W(800);app.updateManualAiFillButtonState();$('manualProjectName').value='업무팁 중복 시험(채우기)';app._nwGo(2);await W(500);app._toggleManualAiSection();await W(300);$('manualContent').value='물품 구매';"
     "await app.fillChecklistWithAI();await W(500);const b=$('aiFillPreview');"
     "return '중복 규칙='+/단계에 한 번만 쓰고/.test(window.__lastP)+' | 알림 글='+tx(b.querySelector('.rs-dedup'))+' | 줄='+app._aiFillState.items.map(x=>x.text+'='+(x.tipText||'').replace(/\\n/g,' / ')).join(' ‖ ')")
click("$('aiFillInsertBtn')")
step('F 넣은 뒤 줄 업무팁', "await W(1200);return [...document.querySelectorAll('#checklistItems .checklist-edit-item')].map(r=>r.querySelector('input').value+'='+(r.dataset.tip||'').replace(/\\n/g,' / ')).join(' ‖ ')")
step('정리', "const w=app.allData.workflows.find(x=>x.id===app._nw?.wfId);app.closeModal?.('manualModal');await W(500);if(w){app.allData.workflows=app.allData.workflows.filter(x=>x!==w);await app.saveDataImmediate();}return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
