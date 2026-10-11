# 업무 절차 패널: ① 필요 서식 바로 열기 ② 체크리스트에서 고른 줄 따라가기 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_pick_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7501);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
ROW = "const row=t=>[...document.querySelectorAll('[id^=\"focus-checklist-scroll-\"] .checklist-card')].find(c=>c.querySelector('.item-title-text')?.textContent.trim().startsWith(t));"
S = []
def step(label, body): S.append({"label": label, "js": J(ROW + body)})
def pt(expr): S.append({"pt": True, "js": J(ROW + "const el=" + expr + ";const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(30,b.width/2),b.top+b.height/2])")})
step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const mk=async n=>app.dbManager.saveFile('repoDocuments',{name:n,size:3000,blob:new Blob(['(시험용 서식) '+n],{type:'text/plain'}),type:'text/plain',folderId:null,uploadedAt:new Date().toISOString(),updatedAt:new Date().toISOString(),tags:[]});"
     "const d1=await mk('출석통지서.txt'),d2=await mk('징계의결서 수령 확인서.txt');await app._loadRepoDocMetaCache();"
     "const cl=[['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0],['징계위원회 출석·진술',1],['징계 의결서 수령',1],['종결',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7501,type:'manual',title:'고른 줄 따라가기 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "wf().checklist[2].tip={type:'text',content:'출석통지서는 회의 3일 전까지 도달',saved:true};wf().checklist[2].linkedDocs=[d1];"
     "wf().checklist[5].tip={type:'text',content:'의결서를 받으면 15일 안에 처분하고 처분사유설명서를 교부',saved:true};wf().checklist[5].linkedDocs=[d2];"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7501);await W(900);app.toggleChecklistItem(7501,1);await W(1500);return 'ok'")
step("A 패널의 필요 서식이 누를 수 있는 단추", "const r=[...document.querySelectorAll('#aiPanelOfflineDashboard .proc-fmt-row')];return '서식 줄='+r.length+' 이름='+r.map(x=>x.textContent.trim()).join(',')+' 열기단추='+r.filter(x=>x.querySelector('.proc-fmt-open')).length+' 내려받기단추='+r.filter(x=>x.querySelector('.proc-fmt-down')).length")
pt("document.querySelector('#aiPanelOfflineDashboard .proc-fmt-open')")
S.append({"clickpt": 1})
step("B 서식 이름을 누르면 미리보기", "await W(900);const m=[...document.querySelectorAll('.modal.show')].pop();const r='열린 창='+(m?(m.querySelector('h2,h3,.modal-title')?.textContent.trim()||m.id):'없음');document.querySelectorAll('.pv-modal').forEach(x=>x.remove());app.restoreBodyScroll&&app.restoreBodyScroll();await W(300);return r")
S.append({"shot": "pick_a.png"})
pt("row('심의·의결').querySelector('.stage-num')")
S.append({"clickpt": 1, "wait": 100})
pt("row('징계 의결서 수령').querySelector('.item-title-text')")
S.append({"clickpt": 1})
step("C 다음 단계의 할 일을 한 번 누르면 패널 맨 위에 그 업무팁·서식", "await W(800);const p=document.getElementById('procPick');if(!p)return '미리 보기 없음';return '태그='+p.querySelector('.proc-pick-tag').textContent+' 제목='+p.querySelector('.proc-pick-title').textContent.trim()+' | 팁='+(p.textContent.includes('15일 안에'))+' 서식='+[...p.querySelectorAll('.proc-fmt-row')].map(x=>x.textContent.trim()).join(',')+' | 패널 스크롤='+document.getElementById('aiPanelOfflineDashboard').scrollTop+' | 줄 펼침='+!!row('징계 의결서 수령').querySelector('.cl-peek')")
S.append({"shot": "pick_c.png"})
pt("row('종결').querySelector('.item-title-text')")
S.append({"clickpt": 1})
step("D 업무팁·서식이 없는 항목", "await W(800);const p=document.getElementById('procPick');return p?('제목='+p.querySelector('.proc-pick-title').textContent.trim()+' 안내='+(p.querySelector('.proc-pick-empty')?.textContent.trim()||'없음')):'미리 보기 없음'")
pt("document.querySelector('#procPick .proc-pick-close')")
S.append({"clickpt": 1})
step("E 「지금 할 일로」 누르면 원래대로", "await W(700);return '미리 보기='+!!document.getElementById('procPick')+' 줄 펼침='+!!document.querySelector('.cl-peek')")
pt("row('출석통지서').querySelector('.item-title-text')")
S.append({"clickpt": 1})
step("F 지금 할 일을 누르면 중복으로 안 나옴", "await W(700);return '미리 보기='+!!document.getElementById('procPick')+' 줄 펼침='+!!row('출석통지서').querySelector('.cl-peek')")
step("G 끝난 항목", "app._clPeek=null;app._rerenderChecklist(wf());await W(500);app.toggleChecklistItemPeekById=null;" "const it=wf().checklist[1];app._clPeek={wfId:7501,itemId:it.itemId};app._rerenderChecklist(wf());await W(700);const p=document.getElementById('procPick');return p?('태그='+p.querySelector('.proc-pick-tag').textContent+' 안내='+(p.querySelector('.proc-pick-empty')?'있음':'없음')):'미리 보기 없음'")
step("H 같은 줄을 다시 누르면 닫힘(풀림)", "app.toggleChecklistPeek(7501,1);await W(600);return '미리 보기='+!!document.getElementById('procPick')")
step("H2 고른 할 일이 든 단계를 접으면 미리 보기도 닫힘", "app._clPeek={wfId:7501,itemId:wf().checklist[5].itemId};app._rerenderChecklist(wf());await W(600);const before=!!document.getElementById('procPick');const st=app._isStageOpen(wf(),3,app._stageInfo(wf().checklist,wf()).currentIdx);if(!st)app.toggleStageOpen(7501,3);await W(400);app.toggleStageOpen(7501,3);await W(700);return '접기 전='+before+' 접은 뒤='+!!document.getElementById('procPick')+' 고른것='+JSON.stringify(app._clPeek)")
step("I 다크 모드", "document.documentElement.classList.add('dark-mode');app._clPeek={wfId:7501,itemId:wf().checklist[5].itemId};app._rerenderChecklist(wf());await W(800);return 'ok'")
S.append({"shot": "pick_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app._clPeek=null;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7501);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
