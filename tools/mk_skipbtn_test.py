# 건너뛰기 버튼을 누른 줄·건너뛴 줄의 제목 앞 ⤼ 표시(누르면 [건너뛰기 취소]만)·접힌 알약 까닭 표시·오른쪽 클릭 「건너뛰기 취소」 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_skipbtn_test.py [1366x768] && node cdp3.mjs <index.html 경로>
import json, os, sys
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7702);const SC=()=>document.getElementById('focus-checklist-scroll-7702');const row=i=>SC().querySelector('.checklist-card[data-index=\"'+i+'\"]');const menu=()=>document.getElementById('checklistItemMenu');const mtxt=()=>menu()?[...menu().children].map(e=>e.textContent.trim()).join(' / '):'메뉴 없음';const pills=()=>[...SC().querySelectorAll('.skip-run-pill')].map(b=>b.textContent.trim().replace(/\\s+/g,' ')+'('+b.className.replace('skip-run-pill','').trim()+')').join(' , ');const toast=()=>{const t=document.getElementById('toast');return t&&t.classList.contains('show')?document.getElementById('toastMessage').textContent.trim():'(알림 없음)'};"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr, dx="Math.min(30,b.width/2)"): S.append({"pt": True, "js": J("const el=" + expr + ";el.scrollIntoView({block:'nearest'});const b=el.getBoundingClientRect();return JSON.stringify([b.left+" + dx + ",b.top+b.height/2])")})

if len(sys.argv) > 1:
    w, h = map(int, sys.argv[1].split('x'))
    S.append({"viewport": [w, h]})

step("준비", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['구매 준비',0],['계약 방법 정하기',0],['견적서 2부 받기',0],['가격 비교표 작성',0],['계약 보증금 받기',0],['계약서 작성',0],['대가 지급',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7702,type:'manual',title:'건너뛰기 버튼 시험',checklist:cl,date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "const c=wf().checklist;c[1].branchOptions=[{label:'2인 견적',action:'',targetItemIds:[c[2].itemId,c[3].itemId]},{label:'견적 생략',action:'',targetItemIds:[c[2].itemId]}];"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7702);await W(900);app.toggleChecklistItem(7702,0);await W(1400);"
     "return '건너뛰기 버튼='+[...row(1).querySelectorAll('.branch-run-btn')].map(b=>b.textContent.trim()).join(',')")
# 실제 클릭: 「2인 견적」 → 확인 창 [실행]
pt("[...row(1).querySelectorAll('.branch-run-btn')].find(b=>b.textContent.includes('2인'))")
S.append({"clickpt": 1})
pt("document.getElementById('branchPreviewConfirmBtn')")
S.append({"clickpt": 1})
step("A 누른 뒤: 제목 아래 눌린 버튼 · 실행취소 없음 · 알림", "await W(500);const t=row(1).querySelector('.item-title-text > .cl-skip-mark');return '제목 앞 표시='+(t?'있음(글자:'+JSON.stringify(t.textContent.trim())+')':'없음')+' | 제목 아래 버튼='+row(1).querySelectorAll('.branch-run-btn').length+' | 「실행취소」 글자='+(SC().textContent.includes('실행취소'))+' | 「분기」 표시='+!!row(1).querySelector('.cl-right span[title^=\"분기\"]')+' | 알림='+toast()")
step("B 접힌 알약", "app.markNotApplicable(7702,[4]);await W(900);return pills()")
S.append({"shot": "skb_a.png"})
# 마우스를 올린 상태에서도 눌린 버튼이 보이고 눌리는지 (예전에는 버튼 줄이 덮음)
pt("row(1).querySelector('.item-title-text')")
S.append({"hoverpt": 1})
step("C 마우스 올림: 버튼 줄 보임 · 눌린 버튼 안 가려짐", "const h=row(1).querySelector('.cl-hbar');const t=row(1).querySelector('.cl-skip-mark');const b=t.getBoundingClientRect();const top=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2);const hb=h.getBoundingClientRect();const over=!(hb.right<b.left||hb.left>b.right||hb.bottom<b.top||hb.top>b.bottom);return '버튼줄 보임='+(getComputedStyle(h).visibility)+' | 눌린 버튼 맨 위='+!!(top&&top.closest('.cl-skip-mark'))+' | 겹침='+over")
S.append({"shot": "skb_hover.png"})
pt("row(1).querySelector('.cl-skip-mark')")
S.append({"clickpt": 1})
step("D 표시 누르면 메뉴(건너뛰기 취소만)", "await W(200);return mtxt()")
S.append({"shot": "skb_menu.png"})
S.append({"key": "Escape"})
step("E 알약 펼친 건너뛴 줄", "SC().querySelector('.skip-run-pill.br').click();await W(500);const r=row(3);const m=r&&r.querySelector('.item-title-text > .cl-skip-mark');return '줄 보임='+!!r+' | 보라 테두리='+(r&&r.classList.contains('skip-br'))+' | 제목 앞 표시='+!!m+' | 오른쪽 끝 버튼='+!!(r&&r.querySelector('.cl-right button:not(.cl-hb)'))")
S.append({"shot": "skb_open.png"})
# 건너뛴 줄에서 오른쪽 클릭 → 맨 위 「건너뛰기 취소」
pt("row(3).querySelector('.item-title-text')")
S.append({"rclickpt": 1})
step("F 건너뛴 줄 오른쪽 클릭", "return mtxt()")
S.append({"key": "Escape"})
pt("row(1).querySelector('.item-title-text')")
S.append({"rclickpt": 1})
step("G 버튼 누른 줄 오른쪽 클릭", "return mtxt()")
S.append({"key": "Escape"})
# 건너뛴 줄의 작은 눌린 버튼 → 같은 메뉴 → [건너뛰기 취소] (묻지 않음)
step("H0 확인 창 감시", "window.__cf=0;window.confirm=()=>{window.__cf++;return true};return 'ok'")
pt("row(3).querySelector('.cl-skip-mark')")
S.append({"clickpt": 1})
step("H1 작은 버튼 메뉴", "await W(200);return mtxt()")
pt("[...menu().querySelectorAll('button')].find(b=>b.textContent.includes('건너뛰기 취소'))")
S.append({"clickpt": 1})
step("H 건너뛰기 취소: 묻지 않음 · 풀림 · 알림", "await W(500);const c=wf().checklist;return '확인창='+window.__cf+' | 건너뜀='+c.filter(x=>x.skipped).map(x=>x.text).join(',')+' | 버튼줄 완료='+!!c[1].completed+' | 건너뛰기 버튼 다시 나옴='+[...row(1).querySelectorAll('.branch-run-btn')].map(b=>b.textContent.trim()).join(',')+' | 알림='+toast()")
S.append({"shot": "skb_cancel.png"})
pt("document.querySelector('#toastMessage .toast-undo-btn')")
S.append({"clickpt": 1})
step("I [되돌리기] → 다시 건너뜀", "await W(500);const c=wf().checklist;return '건너뜀='+c.filter(x=>x.skipped).map(x=>x.text).join(',')+' | 버튼줄 완료='+!!c[1].completed+' | 눌린버튼='+!!row(1).querySelector('.cl-skip-mark')+' | 알약='+pills()+' | 알림='+toast()")
step("J 오른쪽 클릭 메뉴의 건너뛰기 취소도 동작", "app._cancelBranchFromItem(7702,1);await W(500);const c=wf().checklist;return '건너뜀='+c.filter(x=>x.skipped).map(x=>x.text).join(',')+' | 확인창='+window.__cf")
step("K 다른 버튼(견적 생략)도 같은 모양", "app._executeBranchOption(7702,1,false,[{item:wf().checklist[2],id:wf().checklist[2].itemId,index:2}],wf().checklist[1].branchOptions[1]);await W(700);return '표시 말풍선='+row(1).querySelector('.cl-skip-mark').title+' | 알약='+pills()")
step("L 다크 모드", "document.documentElement.classList.add('dark-mode');SC().querySelector('.skip-run-pill.br').click();await W(500);return 'ok'")
S.append({"shot": "skb_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7702);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
