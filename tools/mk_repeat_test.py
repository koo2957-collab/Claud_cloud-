# 「↻ 여러 번 하는 일」 시험 대본 → steps_repeat.json  (배포판 index.html로 실행)
# 확인: 오른쪽 클릭 「여러 번 하는 일로」(할 일이 딸린 단계엔 없음) · 동그라미 실제 클릭 → 작은 창(체크 안 됨) → Enter 기록 = 첫 기록이면 체크
#       · 두 번째부터는 체크 그대로 · 날짜순 · 날짜 자리 「n회 · 날짜」 · Esc/바깥 누르기 = 창만 닫힘 · Ctrl+Z · 단계가 끝나 접혀도 맨 위 줄에서 기록
#       · 항목 창 처리결과 탭 기록 목록(고치기·× 지우기·[되돌리기]·[+ 이번 기록]이 창 위에·Esc는 작은 창만) · 업무 절차 패널 · 진행상황 출력 (n회)·날짜 줄
#       · 풀기·Ctrl+Z · 기록을 모두 지우면 체크도 풂 · 복사하여 시작은 기록만 비움 · 레퍼런스·완료 업무 · 편집 화면 ↻ · 새로 고침 뒤 그대로
# 실행: (tools 폴더에서) python mk_repeat_test.py && set STEPS=steps_repeat.json && set SELFCHECK=1 && node cdp3.mjs "<저장소>/index.html"
import json
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7951;"
     "const WF=()=>app.allData.workflows.find(w=>w.id===ID);const IT=()=>WF().checklist.find(c=>c.text==='수사보고서 작성');const IX=()=>WF().checklist.indexOf(IT());"
     "const row=t=>{const w=WF();const i=w.checklist.findIndex(c=>c.text===t);return document.querySelector('#checklist-items-'+ID+' .checklist-card[data-index=\"'+i+'\"] .checklist-card-header')};"
     "const pop=()=>$('repLogPop');const toast=()=>{const t=$('toast');return t&&t.classList.contains('show')?t.textContent.replace(/\\s+/g,' ').trim():'(알림 없음)'};"
     "const menuRow=T=>[...document.querySelectorAll('#checklistItemMenu button')].find(r=>r.textContent.trim()===T);"
     "const menuLabels=()=>[...document.querySelectorAll('#checklistItemMenu button')].map(x=>x.textContent.trim()).filter(Boolean).join(' / ');"
     "const st=()=>{const it=IT();return '기록 '+(it.logs||[]).length+'회 · 체크='+app.normalizeCompleted(it)+' · repeat='+(it.repeat===true)};"
     "const mid=el=>{if(!el)return 'ERR 누를 곳 없음';el.scrollIntoView({block:'nearest'});const r=el.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])};"
     "const ymd=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body, **kw): S.append({"label": label, "js": P + body + E, **kw})
def pt(body): S.append({"pt": True, "js": P + body + E})
def click(): S.append({"clickpt": 1, "wait": 150})
def rclick(): S.append({"rclickpt": 1})
def key(k, vk, **kw): S.append({"key": k, "vk": vk, "wait": 350, **kw})

step("준비: 단계 3개(01 할 일 2 · 02 할 일 2 · 03 할 일 없음) 업무를 열기",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};localStorage.setItem('deadlineNotifyMode','off');"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id<7950||w.id>7959);"
     "const mk=(t,i)=>{const x={text:t,indent:i,completed:false};app.ensureChecklistItemId(x);return x};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'반복 시험 사건',checklist:[mk('사건 접수',0),mk('접수 기록',1),mk('수사보고서 작성',1),mk('조사',0),mk('출석 요구',1),mk('조서 작성',1),mk('결과 보고',0)],date:'2026. 10. 1.',createdAt:new Date().toISOString()});"
     "await app.saveDataImmediate();app.focusWorkflow(ID);await W(1200);return '열림='+(app.focusedWorkflowId===ID)+' · 맨 위 줄='+!!document.querySelector('.rep-bar')")

# A. 오른쪽 클릭 → 「여러 번 하는 일로」
pt("return mid(row('수사보고서 작성'))"); rclick()
step("A1 할 일 오른쪽 클릭 메뉴", "return menuLabels()")
pt("return mid(menuRow('여러 번 하는 일로'))"); click()
step("A2 「여러 번 하는 일로」 누름", "await W(300);const r=row('수사보고서 작성');return st()+' · ↻ 표시='+!!r.querySelector('.cl-rep-mark')+' · 맨 위 줄='+(document.querySelector('.rep-bar')?.textContent.replace(/\\s+/g,' ').trim()||'없음')+' · 알림='+toast()")
pt("return mid(row('사건 접수'))"); rclick()
step("A3 할 일이 딸린 단계 메뉴엔 「여러 번 하는 일로」 없음", "const has=!!menuRow('여러 번 하는 일로');document.body.click();await W(200);return '있음='+has")
step("A4 할 일 없는 단계(03 결과 보고) 메뉴엔 있음", "const i=WF().checklist.findIndex(c=>c.text==='결과 보고');app.openChecklistItemMenu({type:'contextmenu',preventDefault(){},stopPropagation(){},clientX:500,clientY:300},ID,i);await W(200);const has=menuLabels();document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));await W(200);return '있음='+has")

# B. 동그라미 실제 클릭 → 작은 창 → 글 → Enter
pt("return mid($('main-checkbox-'+ID+'-'+IX()))"); click()
step("B1 동그라미를 누르면 체크 대신 작은 창", "await W(200);const c=$('main-checkbox-'+ID+'-'+IX());return '창='+!!pop()+' · '+(pop()?.querySelector('.rep-pop-n')?.textContent||'')+' · 체크칸 checked='+c.checked+' · '+st()+' · 초점='+(document.activeElement?.className||'')")
S.append({"shot": "rep_b1.png"})
S.append({"text": "참고인 김○○ 진술 확인"})
key("Enter", 13)
step("B2 Enter → 첫 기록 = 체크", "await W(400);const r=row('수사보고서 작성');return '창='+!!pop()+' · '+st()+' · 글='+IT().logs[0].text+' · 날짜 자리='+(r.querySelector('.cl-rep-badge')?.textContent.trim()||'없음')+' · 줄 취소선='+(getComputedStyle(r.querySelector('.item-title-text')).textDecorationLine)+' · 알림='+toast()")
S.append({"shot": "rep_b2.png"})

# C. 두 번째 기록: 날짜를 어제로, 글 없이
pt("return mid($('main-checkbox-'+ID+'-'+IX()))"); click()
step("C1 두 번째 — 날짜를 어제로", "await W(200);const d=new Date();d.setDate(d.getDate()-1);const dt=pop().querySelector('.rep-pop-date');dt.value=ymd(d);pop().querySelector('.rep-pop-text').focus();return (pop()?.querySelector('.rep-pop-n')?.textContent||'창 없음')")
key("Enter", 13)
step("C2 기록 2회 · 날짜순(어제가 앞) · 체크 그대로", "await W(400);const L=IT().logs;return st()+' · 순서='+L.map(l=>l.date.slice(5)+(l.text?'('+l.text.slice(0,6)+')':'')).join(' → ')+' · 날짜 자리='+(row('수사보고서 작성').querySelector('.cl-rep-badge')?.textContent.trim())")

# D. Esc · 바깥 누르기 = 작은 창만
step("D0 날짜 자리 「2회 · …」는 보기 전용(마우스를 올리면 버튼 줄이 덮음)", "const b=row('수사보고서 작성').querySelector('.cl-rep-badge');return (b?b.tagName+' '+b.textContent.trim():'없음')")
pt("return mid($('main-checkbox-'+ID+'-'+IX()))"); click()
step("D1 동그라미 → 작은 창", "await W(200);return '창='+!!pop()")
key("Escape", 27)
step("D2 Esc → 창만 닫힘(일하는 화면 그대로)", "await W(200);return '창='+!!pop()+' · 일하는 화면='+(app.focusMode&&app.focusedWorkflowId===ID)+' · '+st()")
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); click()
step("D3 맨 위 줄 단추 → 작은 창", "await W(200);return '창='+!!pop()")
pt("return mid(document.querySelector('.rep-bar-h'))"); click()
step("D4 바깥 누르기 → 창 닫힘, 기록 그대로", "await W(300);return '창='+!!pop()+' · '+st()")
step("D5 (정리) 펼친 줄 닫기", "app.clearChecklistPick?.();app._clPeek=null;app._rerenderChecklist(WF());await W(200);return 'ok'")

# E. 세 번째 기록 → Ctrl+Z
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); click()
key("Enter", 13)
step("E1 세 번째(글 없이)", "await W(300);return st()")
step("E1b 초점 빼기", "document.activeElement?.blur?.();await W(100);return 'ok'")
key("z", 90, mods=2)
step("E2 Ctrl+Z → 2회로, 체크 그대로", "await W(300);return st()+' · 알림='+toast()")

# F. 단계 01 끝내기 → 접혀도 맨 위 줄에서 기록
pt("return mid($('main-checkbox-'+ID+'-'+WF().checklist.findIndex(c=>c.text==='접수 기록')))"); click()
step("F1 남은 할 일 체크 → 단계 01 끝남·다음 단계로", "await W(1800);const w=WF();const s=app._stageInfo(w.checklist,w);return '01 끝남='+app.normalizeCompleted(w.checklist[0])+' · 진행중='+(w.checklist[s.currentIdx]?.text)+' · 수사보고서 줄 보임='+!!row('수사보고서 작성')+' · 맨 위 줄='+!!document.querySelector('.rep-bar')")
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); click()
S.append({"text": "추가 수사보고"})
key("Enter", 13)
step("F2 접힌 단계의 할 일도 맨 위 줄에서 기록", "await W(400);const w=WF();return st()+' · 01 그대로 끝남='+app.normalizeCompleted(w.checklist[0])+' · 진행중='+w.checklist[app._stageInfo(w.checklist,w).currentIdx]?.text+' · 맨 위 줄='+document.querySelector('.rep-bar .rep-chip .n')?.textContent")
S.append({"shot": "rep_f2.png"})

# G. 업무 절차 패널
step("G1 업무 절차 패널 맨 위 「↻ 여러 번 하는 일」", "app.refreshAIPanelDashboardIfNeeded?.();await W(500);const p=document.querySelector('.proc-rep');return p?p.textContent.replace(/\\s+/g,' ').trim():'없음'")
pt("return mid(document.querySelector('.proc-rep .proc-rep-row'))"); click()
step("G2 패널 줄 → 작은 창", "await W(200);const r=!!pop();return '창='+r")
key("Escape", 27)

# H. 항목 창 처리결과 탭
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); rclick()
step("H0 접힌 단계의 할 일 — 맨 위 줄 단추 오른쪽 클릭 메뉴", "return menuLabels()")
pt("return mid(menuRow('처리결과'))"); click()
step("H1 항목 창 처리결과 탭 맨 위 기록 목록", "await W(500);const L=document.querySelector('#cimOverlay .rep-logs');return L?L.querySelector('.rep-logs-h').textContent.replace(/\\s+/g,' ').trim()+' · 줄 '+L.querySelectorAll('.rep-log').length:'없음'")
S.append({"shot": "rep_h1.png"})
step("H2 첫 기록 글 고치기(칸 빠져나가면 저장)", "const i=document.querySelector('#cimOverlay .rep-log .rep-log-text');i.value='참고인 김○○ 진술 확인(고침)';i.dispatchEvent(new Event('change',{bubbles:true}));await W(200);return IT().logs[0].text")
pt("return mid(document.querySelectorAll('#cimOverlay .rep-log .rep-del')[1])"); click()
step("H3 × 실제 클릭 → 지움(묻지 않음)·[되돌리기]", "await W(300);return st()+' · 목록 줄='+document.querySelectorAll('#cimOverlay .rep-log').length+' · 알림='+toast()")
pt("return mid([...document.querySelectorAll('#toast button')].find(b=>b.textContent.includes('되돌리기')))"); click()
step("H4 [되돌리기] 실제 클릭", "await W(300);return st()+' · 목록 줄='+document.querySelectorAll('#cimOverlay .rep-log').length")
pt("return mid(document.querySelector('#cimOverlay .rep-add'))"); click()
step("H5 항목 창 [+ 이번 기록] → 작은 창이 항목 창 위에", "await W(200);const p=pop();if(!p)return '창 없음';const r=p.getBoundingClientRect();const top=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return '창 위에='+p.contains(top)+' · '+p.querySelector('.rep-pop-n').textContent")
key("Escape", 27)
step("H6 Esc → 작은 창만 닫히고 항목 창은 그대로", "await W(300);return '작은 창='+!!pop()+' · 항목 창='+!!document.getElementById('cimOverlay')")
key("Escape", 27)
step("H7 Esc 한 번 더 → 항목 창 닫힘", "await W(400);return '항목 창='+!!document.getElementById('cimOverlay')")

# I. 진행상황 출력
step("I1 진행상황 보고·체크리스트 표에 (n회)·날짜 줄", "const w=WF();const b=app._prReportBlocks(w,{subs:true,attach:false,skipped:false}).map(x=>x.text).filter(t=>/수사보고서|진술|추가 수사/.test(t));const P=app._checklistParts(w,{clResult:true});const row2=P.rows.map(r=>r.html).find(h=>h.includes('수사보고서'))||'';return '보고서: '+b.join(' | ')+' ‖ 표: '+row2.replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').trim().slice(0,120)")

# J. 풀기 → Ctrl+Z
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); rclick()
step("J0 메뉴", "return menuLabels()")
pt("return mid(menuRow('여러 번 하는 일 풀기'))"); click()
step("J1 「여러 번 하는 일 풀기」 → 맨 위 줄 없어짐·기록은 남음", "await W(300);return st()+' · 맨 위 줄='+!!document.querySelector('.rep-bar')+' · 알림='+toast()")
step("J1b 초점 빼기", "document.activeElement?.blur?.();await W(100);return 'ok'")
key("z", 90, mods=2)
step("J2 Ctrl+Z → 다시 여러 번 하는 일", "await W(300);return st()+' · 맨 위 줄='+!!document.querySelector('.rep-bar')")

# K. 편집 화면 ↻ · 복사하여 시작 · 레퍼런스 · 완료한 업무
step("K1 편집 화면 줄에도 ↻", "app.enterFocusEditMode();await W(700);const t=[...document.querySelectorAll('.fci-title-text')].find(x=>x.textContent.includes('수사보고서'));const r=app.focusEditMode+' 줄='+document.querySelectorAll('.fci-title-text').length+' '+(t?t.outerHTML.slice(0,160):'못 찾음');app.cancelFocusEditMode?app.cancelFocusEditMode():app.exitFocusEditMode?.();await W(600);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return '↻='+r+' · 편집 끝='+!app.focusEditMode")
step("K2 복사하여 시작 → 표시는 그대로, 기록·체크는 비움", "const nid=await app.executeDuplicateWorkflow(ID,{silent:true});await W(400);const n=app.allData.workflows.find(w=>w.id===nid);const it=n?.checklist.find(c=>c.text==='수사보고서 작성');const r='repeat='+(it?.repeat===true)+' · logs='+JSON.stringify(it?.logs)+' · 체크='+(it&&app.normalizeCompleted(it));if(n){app.allData.workflows=app.allData.workflows.filter(w=>w.id!==nid);await app.saveDataImmediate();}app.focusWorkflow(ID);await W(800);return r")
step("K3 레퍼런스는 맨 위 줄·기록 없음", "const ref={...JSON.parse(JSON.stringify(WF())),id:7952,isReference:true};return '맨 위 줄=\"'+app._repBarHtml(ref)+'\" · 패널=\"'+app._repPanelHtml(ref)+'\" · 항목 창 목록=\"'+app._repLogsHtml(ref,ref.checklist.findIndex(c=>c.text==='수사보고서 작성'),false)+'\"'")
step("K4 완료한 업무는 작은 창 대신 알림", "WF().completedProcessed=true;app.openRepeatLog(ID,IX(),null);await W(200);const r='창='+!!pop()+' · 알림='+toast();delete WF().completedProcessed;app._rerenderChecklist(WF());await W(300);return r")

# L. 새로 고침 뒤 그대로
step("L0 저장", "await app.saveDataImmediate();return st()")
S.append({"reload": 1})
step("L1 새로 고침 뒤", "app.checkBackupReminder=()=>{};document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.focusWorkflow(ID);await W(1000);return st()+' · 날짜 자리='+(row('수사보고서 작성')?.querySelector('.cl-rep-badge')?.textContent.trim()||'(접혀 안 보임)')+' · 맨 위 줄='+document.querySelector('.rep-bar .rep-chip .n')?.textContent")

# M. 기록을 모두 지우면 체크도 풂 → 단계 01 다시 진행 중 → 되돌리기
step("M1 기록을 모두 지우면 체크 풂", "const it=IT();const ids=it.logs.map(l=>l.id);for(const id of ids){app.deleteRepeatLog(ID,it.itemId,id);await W(150);}const w=WF();return st()+' · 01 끝남='+app.normalizeCompleted(w.checklist[0])+' · 진행중='+w.checklist[app._stageInfo(w.checklist,w).currentIdx]?.text+' · 알림='+toast()")
step("M2 마지막 지우기 되돌리기 → 다시 체크", "app._undoLast?.();await W(300);const w=WF();return st()+' · 01 끝남='+app.normalizeCompleted(w.checklist[0])")
# N. 체크 취소 (기록은 남김)
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); rclick()
step("N0 메뉴(체크된 여러 번 하는 일)", "return menuLabels()")
pt("return mid(menuRow('체크 취소 (기록은 남김)'))"); click()
step("N1 「체크 취소 (기록은 남김)」 → 체크만 풂·단계 다시 진행 중", "await W(400);const w=WF();return st()+' · 01 끝남='+app.normalizeCompleted(w.checklist[0])+' · 진행중='+w.checklist[app._stageInfo(w.checklist,w).currentIdx]?.text+' · 알림='+toast()")
pt("return mid(document.querySelector('.rep-bar .rep-chip'))"); rclick()
step("N2 체크 안 된 동안 메뉴엔 체크 취소 없음", "const r=menuLabels();document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));await W(200);return r")
step("N2b 초점 빼기", "document.querySelectorAll('#checklistItemMenu').forEach(m=>m.remove());document.activeElement?.blur?.();await W(100);return 'ok'")
key("z", 90, mods=2)
step("N3 Ctrl+Z → 다시 체크", "await W(400);const w=WF();return st()+' · 01 끝남='+app.normalizeCompleted(w.checklist[0])")
step("N4 다시 체크 취소 → 다음 기록이면 다시 체크", "app.uncheckRepeat(ID,IX());await W(300);const a=st();app.addRepeatLog(ID,IT().itemId,ymd(new Date()),'다시 기록');await W(400);return a+' → '+st()")
step("정리", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app._repClosePop();return 'ok'")

json.dump(S, open('steps_repeat.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
