import json
# 업무 관리 오른쪽 클릭 [보관함으로 이동]·[완료 취소](여러 개 · 하나) · 보관된 업무 [삭제] · 일하는 화면 [보관]:
# 묻지 않고 [실행 취소]·Ctrl+Z (실제 클릭) → steps_wfmundo.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
H = ("const A=()=>app.allData.workflows.find(x=>x.id===window.__a),B=()=>app.allData.workflows.find(x=>x.id===window.__b);"
     "const s1=w=>(w.isArchived?'보관':'')+(w.completedProcessed?'완료':'')+(w.isDeleted?'지움':'')||'진행';"
     "const st=()=>'소모품='+s1(A())+' 월간='+s1(B());"
     "const toast=()=>[...document.querySelectorAll('.toast')].map(x=>x.textContent.replace(/\\s+/g,' ').trim()).pop()||'';"
     "const rowPt=(w,dx)=>{const r0=[...document.querySelectorAll('#workflowManagerModal tbody tr')].find(x=>x.offsetParent&&x.textContent.includes(w.title));if(!r0)return 'ERR 줄 없음 '+w.title;r0.scrollIntoView({block:'center'});const r=r0.getBoundingClientRect();return JSON.stringify([r.left+(dx||160),r.top+r.height/2])};"
     "const menuPt=re=>{const it=[...document.querySelectorAll('.mini-menu *, #wfmCtxMenu .wfm-ctx-item, [class*=ctx] [onclick]')].filter(x=>x.getClientRects().length&&re.test(x.textContent)&&x.textContent.trim().length<60).pop();if(!it)return 'ERR 메뉴 없음';const r=it.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])};"
     "const undoPt=()=>{const b=[...document.querySelectorAll('.toast button, .toast [class*=action]')].reverse().find(x=>/실행 취소/.test(x.textContent));if(!b)return 'ERR 실행 취소 없음';const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])};"
     "const ask=()=>' | 물음='+window.__asked;")
S = []
def step(label, body): S.append({"label": label, "js": P + H + body + E})
def pt(body): S.append({"pt": True, "js": P + H + body + E})
def click(mods=0): S.append({"clickpt": 1, "wait": 100, **({"mods": mods} if mods else {})})
def rclick(): S.append({"rclickpt": 1, "wait": 100})
def ctrlz(): S.append({"key": "z", "vk": 90, "mods": 2, "wait": 100})
def pick_two():
    pt("return rowPt(A())"); click()
    pt("return rowPt(B())"); click(2)
    pt("return rowPt(B())"); rclick()

step("준비", "localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));window.__asked=0;window.confirm=m=>{window.__asked++;return true};app.insertPracticeWorkflows();await W(2500);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const ws=app.allData.workflows.filter(w=>/^\\[연습\\]/.test(w.title)&&!w.isReference);window.__a=ws.find(w=>/소모품/.test(w.title)).id;window.__b=ws.find(w=>/월간/.test(w.title)).id;app.openWorkflowManager();await W(900);return st()")
# A 여러 개 보관 → [실행 취소] 클릭
pick_two()
pt("return menuPt(/보관함으로 이동/)"); click()
step("A1 두 개 오른쪽 클릭 [보관함으로 이동]", "await W(600);return st()+ask()+' | 알림='+toast().slice(0,40)")
pt("return undoPt()"); click()
step("A2 [실행 취소] 클릭 → 둘 다 원래대로", "await W(700);return st()")
# A' 다시 보관 → Ctrl+Z
pick_two()
pt("return menuPt(/보관함으로 이동/)"); click()
step("A3 다시 보관", "await W(600);document.activeElement?.blur?.();return st()")
ctrlz()
step("A4 Ctrl+Z → 원래대로", "await W(700);return st()+ask()")
# B 여러 개 완료 취소
step("B0 둘 다 완료 처리해 두고 처리완료 탭", "[A(),B()].forEach(w=>{w.completedProcessed=true;w.completedAt=new Date().toISOString()});app.saveData();app.openWorkflowManager({tab:'done'});await W(800);return st()")
pick_two()
pt("return menuPt(/완료 취소/)"); click()
step("B1 [완료 취소] — 묻지 않음", "await W(600);return st()+ask()+' | 알림='+toast().slice(0,40)")
pt("return undoPt()"); click()
step("B2 [실행 취소] → 다시 완료", "await W(700);const r=st();[A(),B()].forEach(w=>{delete w.completedProcessed;delete w.completedAt});app.saveData();app.openWorkflowManager();await W(800);return r")
# C 하나 오른쪽 클릭 [보관함으로 이동] (archiveTemplate)
pt("return rowPt(A())"); click()
pt("return rowPt(A())"); rclick()
pt("return menuPt(/보관/)"); click()
step("C1 하나 오른쪽 클릭 보관 — 묻지 않음", "await W(600);return st()+ask()+' | 알림='+toast().slice(0,40)")
pt("return undoPt()"); click()
step("C2 [실행 취소] → 원래대로", "await W(700);return st()")
# D 보관된 업무 오른쪽 클릭 [삭제]
step("D0 보관해 두고 보관함 탭", "A().isArchived=true;app.saveData();app.openWorkflowManager({tab:'archived'});await W(900);return st()")
pt("return rowPt(A())"); click()
pt("return rowPt(A())"); rclick()
pt("return menuPt(/삭제/)"); click()
step("D1 보관된 업무 [삭제] — 묻지 않음", "await W(600);return st()+ask()+' | 알림='+toast().slice(0,40)")
ctrlz()
step("D2 Ctrl+Z → 보관 상태로", "await W(700);const r=st();A().isArchived=false;app.saveData();app.closeModal('workflowManagerModal');await W(400);return r")
# E 일하는 화면 [보관] (레퍼런스는 아래 줄에 [보관] — 여기선 함수로)
step("E1 일하는 화면에서 연 업무 보관", "app.focusWorkflow(window.__a);await W(1500);app.archiveTemplate(window.__a);await W(800);return st()+' | 일하는 화면='+app.focusMode+ask()+' | 알림='+toast().slice(0,40)")
pt("return undoPt()"); click()
step("E2 [실행 취소] → 홈 목록에 보임", "await W(800);return st()+' | 홈 목록='+document.body.innerText.includes(A().title)")
step("정리", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return 'ok'")
json.dump(S, open('steps_wfmundo.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
