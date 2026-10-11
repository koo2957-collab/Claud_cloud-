# 업무 절차 패널: 건너뛴 단계·할 일을 제자리에 흐리게 + 알약, 연달아 건너뛴 단계 묶음, 진행 줄 「건너뜀 n」 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_skippanel_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7701);const D=()=>document.getElementById('aiPanelOfflineDashboard');"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr): S.append({"pt": True, "js": J("const el=" + expr + ";const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(30,b.width/2),b.top+b.height/2])")})

ROWS = "const rows=()=>[...D().querySelectorAll('#procStepsTrack > .proc-step-row, #procStepsTrack > .proc-fold .proc-step-row')].map(r=>r.classList.contains('proc-skip-run')?'['+r.textContent.trim().replace(/\\s+/g,' ')+']':r.classList.contains('proc-skip-row')?'~'+r.querySelector('s').textContent+'('+r.querySelector('.proc-skip-pill').textContent.trim()+')':r.querySelector('.proc-step-title').childNodes[0].textContent.trim());"

step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['사건 접수',0],['기관 통보 공문 접수',1],['조사',0],['출석 요구',1],['진술 영상 녹화',1],['문답서 작성',1],['징계 처분',0],['처분사유설명서 교부',1],['인사기록 등재',0],['종결',0],['종결 보고',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7701,type:'manual',title:'건너뛴 항목 표시 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     # 건너뛰기 버튼으로 건너뛴 단계 2개(이어짐) — 실제 저장 모양 그대로
     "for(const i of [6,7,8]){const it=wf().checklist[i];it.skipped=true;it.skipReason='불문·경고 의결 (징계 의결서 수령)';it.skipActionId='a1';}"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7701);await W(900);"
     "app.toggleChecklistItem(7701,1);await W(1300);app.toggleChecklistItem(7701,3);await W(1300);"
     # 해당 없음(실제 기능으로): 할 일 「진술 영상 녹화」, 단계 「종결 보고」
     "app.markNotApplicable(7701,[4],'피조사자 녹화 거부');await W(700);app.markNotApplicable(7701,[10]);await W(900);return 'ok'")
step("A 패널 차례", ROWS + "return rows().join(' | ')")
step("B 진행 줄", "return D().querySelector('#procProg .proc-prog-text').textContent")
step("C 지금 단계 안의 건너뛴 할 일", "const s=D().querySelector('.proc-skip-sub');return s?('글='+s.querySelector('s').textContent+' 알약='+s.querySelector('.proc-skip-pill').textContent+' 사유말풍선='+s.title+' 빈동그라미 아님='+!!s.querySelector('.proc-skip-dot')):'없음'")
step("D 마지막이 건너뛴 단계여도 목적지 표시", "const r=[...D().querySelectorAll('.proc-skip-row')].pop();return '마지막 줄='+r.querySelector('s').textContent+' 목적지핀='+!!r.querySelector('svg path[d^=\"M21 10\"]')")
S.append({"shot": "skp_a.png"})
pt("D().querySelector('.proc-skip-run-btn')")
S.append({"clickpt": 1})
step("E 「n개 건너뜀」 누르면 펼침", ROWS + "await W(400);return rows().join(' | ')+' | 알약 말풍선='+D().querySelector('.proc-skip-row.in-run .proc-skip-pill').title")
S.append({"shot": "skp_e.png"})
pt("D().querySelector('.proc-skip-run-btn')")
S.append({"clickpt": 1})
step("E2 다시 누르면 접힘", ROWS + "await W(400);return rows().join(' | ')")
step("F 건너뛴 줄을 누르면 체크리스트의 그 줄로", "const r=[...D().querySelectorAll('.proc-skip-row')].pop();r.click();await W(800);return '오류 없음'")
step("G 되살리면 패널에서도 원래대로", ROWS + "app.restoreNotApplicable(7701,10);await W(900);return rows().join(' | ')+' | 진행줄='+D().querySelector('#procProg .proc-prog-text').textContent")
step("H 앞쪽 단계까지 끝내면 건너뛴 단계는 접힌 쪽으로", ROWS + "app.toggleChecklistItem(7701,5);await W(1500);const fold=[...D().querySelectorAll('#procFoldList .proc-step-row')].map(r=>r.classList.contains('proc-skip-run')?'[묶음]':r.querySelector('.proc-step-title').textContent.trim().slice(0,8));return '접힌 쪽='+fold.join(',')+' | 보이는 쪽='+rows().filter(x=>!fold.some(f=>x.startsWith(f.slice(0,3)))).join(' | ')")
step("I 다크 모드", "document.documentElement.classList.add('dark-mode');app.toggleChecklistItem(7701,5);await W(1200);app.toggleProcSkipRun(7701,6);await W(400);return 'ok'")
S.append({"shot": "skp_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7701);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
