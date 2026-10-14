# 오른쪽 클릭 메뉴 시험 대본 → steps3.json
# ① 진행 중 업무: 맨 위 체크/체크 취소 · 그 줄의 건너뛰기 버튼 · ⋯ 버튼도 같은 메뉴
# ② 완료한 업무 · 레퍼런스: 메뉴가 나오고 보는 명령은 그대로, 고치는 명령은 회색 + 안내
# ③ 업무 절차 패널 줄도 같은 메뉴  ④ 접힌 알약: 펼치기 · 모두 되살리기 / 건너뛰기 취소 + [되돌리기]
# 실행: (tools 폴더에서) python mk_ctxmenu_test.py [1366x768] && node cdp3.mjs <index.html 경로>
import json, os, sys
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===window.__w);"
     "const ix=t=>wf().checklist.findIndex(i=>i.text===t);const SC=()=>document.getElementById('focus-checklist-scroll-'+window.__w);"
     "const row=i=>document.querySelector('.checklist-card[data-workflow-id=\"'+window.__w+'\"][data-index=\"'+i+'\"]');const menu=()=>document.getElementById('checklistItemMenu');"
     "const mtxt=()=>menu()?[...menu().children].map(e=>e.classList.contains('ci-menu-sep')?'│':(e.textContent.trim()+(e.classList.contains('ci-dis')?'(회색)':''))).join(' / '):'메뉴 없음';"
     "const toast=()=>{const t=document.getElementById('toast');return t&&t.classList.contains('show')?document.getElementById('toastMessage').textContent.trim():'(알림 없음)'};"
     "const D=()=>document.getElementById('aiPanelOfflineDashboard');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr, dx="Math.min(14,b.width/2)"): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음: " + expr.replace("'", "").replace('"', '')[:40] + "');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+" + dx + ",b.top+b.height/2])")})
def rclick(expr): pt(expr); S.append({"rclickpt": 1})
def click(expr): pt(expr); S.append({"clickpt": 1})
def menu_click(text): click("[...menu().querySelectorAll('button')].find(b=>b.textContent.includes('" + text + "'))")

if len(sys.argv) > 1:
    w, h = map(int, sys.argv[1].split('x'))
    S.append({"viewport": [w, h]})

step("준비", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "await app.insertPracticeWorkflows();await W(1500);const w=app.allData.workflows.find(x=>/소모품/.test(x.title));window.__w=w.id;app.focusWorkflow(w.id);await W(1500);return '연습 업무 '+w.checklist.length+'줄'")
T1 = "구매 요청 받기 — 품목·수량·규격 확인"
# ① 체크 / 체크 취소
rclick("row(ix('" + T1 + "')).querySelector('.item-title-text')")
step("A1 안 끝난 할 일 오른쪽 클릭", "return mtxt()")
S.append({"shot": "ctx_a.png"})
menu_click("체크 (완료)")
step("A2 메뉴 「체크 (완료)」 → 체크됨", "await W(800);return '체크='+app.normalizeCompleted(wf().checklist[ix('" + T1 + "')])")
rclick("row(ix('" + T1 + "')).querySelector('.item-title-text')")
step("A3 끝낸 할 일 오른쪽 클릭", "return mtxt()")
menu_click("체크 취소")
step("A4 「체크 취소」 → 풀림", "await W(800);return '체크='+app.normalizeCompleted(wf().checklist[ix('" + T1 + "')])")
# 건너뛰기 버튼이 있는 줄
step("B0 갈림길 앞까지 끝내기", "for(const t of ['" + T1 + "','추정가격 정하기','거래실례가격 조사 (2곳 이상)']){app.toggleChecklistItem(window.__w,ix(t));await W(1300);}app.markNotApplicable(window.__w,[ix('예정가격 작성')]);await W(1500);return 'ok'")
rclick("row(ix('금액 기준 확인 — 갈림길')).querySelector('.item-title-text')")
step("B1 건너뛰기 버튼 있는 줄 오른쪽 클릭", "return mtxt()")
S.append({"shot": "ctx_b.png"})
menu_click("1인 견적")
step("B2 메뉴의 「1인 견적」 → 미리 보기 확인 창", "await W(400);const o=document.getElementById('branchPreviewOverlay');return '확인 창='+!!o+' | '+(o?o.textContent.replace(/\\s+/g,' ').trim().slice(0,60):'')")
click("document.getElementById('branchPreviewConfirmBtn')")
step("B3 실행 뒤 같은 줄 메뉴", "await W(900);return '건너뛴 줄='+wf().checklist.filter(x=>x.skipped&&!x.skipManual).map(x=>x.text).join(',')")
rclick("row(ix('금액 기준 확인 — 갈림길')).querySelector('.item-title-text')")
step("B4 버튼 누른 줄 오른쪽 클릭 (체크 대신 건너뛰기 취소)", "const r=mtxt();app._closeChecklistItemMenu();return r")
# ⋯ 버튼
pt("row(ix('계약 방법 정하기') >= 0 ? ix('계약 방법 정하기') : 0).querySelector('.item-title-text')")
step("C0 지금 할 일 줄 찾기", "const r=[...SC().querySelectorAll('.checklist-card:not(.skipped)')].find(c=>!c.querySelector('input.checkbox:checked'));window.__ci=+r.dataset.index;return wf().checklist[window.__ci].text")
pt("row(window.__ci).querySelector('.item-title-text')")
S.append({"hoverpt": 1})
click("row(window.__ci).querySelector('.cl-hb-more')")
step("C1 ⋯ 버튼 → 같은 메뉴(버튼 아래)", "const m=menu();const b=row(window.__ci).querySelector('.cl-hb-more').getBoundingClientRect();const mr=m?m.getBoundingClientRect():null;return mtxt()+' | 버튼 아래='+(mr&&mr.top>=b.bottom-1&&Math.abs(mr.right-b.right)<3)")
step("C2 메뉴 닫기", "app._closeChecklistItemMenu();return 'ok'")
# ③ 업무 절차 패널 줄
pt("(()=>{const vis=q=>[...D().querySelectorAll(q)].find(x=>x.offsetParent&&x.getBoundingClientRect().height>0);return vis('.proc-sub-row:not(.proc-skip-sub)')})()"); S.append({"rclickpt": 1})
step("D1 업무 절차 패널 할 일 줄 오른쪽 클릭", "return mtxt()")
S.append({"shot": "ctx_panel.png"})
step("D1b 메뉴 닫기", "app._closeChecklistItemMenu();return 'ok'")
pt("(()=>{const vis=q=>[...D().querySelectorAll(q)].find(x=>x.offsetParent&&x.getBoundingClientRect().height>0);return vis('.proc-step-row.is-current .proc-step-title')})()"); S.append({"rclickpt": 1})
step("D2 패널 단계 줄 오른쪽 클릭", "const r=mtxt();app._closeChecklistItemMenu();return r")
# ④ 접힌 알약
rclick("SC().querySelector('.skip-run-pill.na')")
step("E1 해당 없음 알약 오른쪽 클릭", "return mtxt()")
menu_click("모두 되살리기")
step("E2 모두 되살리기", "await W(700);return '해당 없음 남음='+wf().checklist.filter(x=>x.skipManual).length+' | 알림='+toast()")
click("document.querySelector('#toastMessage .toast-undo-btn')")
step("E3 [되돌리기] → 다시 해당 없음", "await W(700);return '해당 없음='+wf().checklist.filter(x=>x.skipManual).map(x=>x.text).join(',')")
rclick("SC().querySelector('.skip-run-pill.br')")
step("E4 건너뛰기 알약 오른쪽 클릭", "return mtxt()")
menu_click("펼치기")
step("E5 펼치기", "await W(500);return '펼친 줄='+SC().querySelectorAll('.skip-run-items .checklist-card').length")
rclick("SC().querySelector('.skip-run-pill.br')")
menu_click("건너뛰기 취소")
step("E6 알약 메뉴의 건너뛰기 취소", "await W(800);return '건너뛴 줄='+wf().checklist.filter(x=>x.skipped&&!x.skipManual).length+' | 알림='+toast()")
# ② 완료한 업무
step("F0 완료 처리", "wf().completedProcessed=true;app.saveData();app.focusWorkflow(window.__w);await W(1500);return '완료='+wf().completedProcessed")
rclick("row(ix('금액 기준 확인 — 갈림길')).querySelector('.item-title-text')")
step("F1 완료한 업무 오른쪽 클릭", "return mtxt()")
S.append({"shot": "ctx_done.png"})
click("[...menu().querySelectorAll('button')].find(b=>b.textContent.includes('체크'))")
step("F2 회색 명령 누름 → 메뉴 그대로 · 바뀐 것 없음", "return '메뉴 열림='+!!menu()+' | 체크='+app.normalizeCompleted(wf().checklist[ix('금액 기준 확인 — 갈림길')])")
menu_click("처리결과")
step("F3 보는 명령(처리결과) → 항목 창 열림", "await W(600);const o=document.getElementById('cimOverlay');const r='항목 창='+!!o;app.closeChecklistItemModal&&app.closeChecklistItemModal();await W(300);return r")
# 레퍼런스
step("G0 레퍼런스로", "wf().completedProcessed=false;wf().isReference=true;app.saveData();app.focusWorkflow(window.__w);await W(1500);return 'ok'")
rclick("document.querySelector('.checklist-card[data-workflow-id=\"'+window.__w+'\"] .item-title-text')")
step("G1 레퍼런스 오른쪽 클릭", "const r=mtxt();app._closeChecklistItemMenu();return r")
step("H 다크 모드", "wf().isReference=false;app.saveData();app.focusWorkflow(window.__w);await W(1200);document.documentElement.classList.add('dark-mode');return 'ok'")
rclick("row(ix('금액 기준 확인 — 갈림길')).querySelector('.item-title-text')")
S.append({"shot": "ctx_dark.png"})
step("정리", "app._closeChecklistItemMenu();document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
