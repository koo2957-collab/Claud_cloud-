# 완료 처리·완료 취소: 묻지 않고 바로 옮긴 뒤 알림의 [되돌리기]로 되돌림 — 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_done_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===8981);window.__cf=0;window.confirm=()=>{window.__cf++;return true;};"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
TOAST = "const toast=()=>{const t=[...document.querySelectorAll('.toast')].pop();return t?t.textContent.replace(/\\s+/g,' ').trim():'없음'};const undoBtn=()=>[...document.querySelectorAll('.toast button')].find(b=>b.textContent.includes('되돌리기'));"

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const now=new Date().toISOString();const cl=[['접수',0],['종결',0]].map(([t,i])=>({text:t,indent:i,completed:true,completedAt:now}));"
     "app.allData.workflows.unshift({id:8981,type:'manual',title:'완료 처리 시험',checklist:cl,date:'2026. 10. 11.',createdAt:now,folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(8981);await W(1200);return 'ok'")
pt("const b=[...document.querySelectorAll('button')].find(x=>x.textContent.includes('완료 처리')&&x.offsetParent);const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("A [✅ 완료 처리] → 묻지 않고 처리완료로 · 알림에 [되돌리기]", TOAST + "await W(600);return '물어본 횟수='+window.__cf+' | 처리완료='+!!wf().completedProcessed+' | 알림='+toast()+' | 되돌리기 단추='+!!undoBtn()")
pt(TOAST + "const r=undoBtn().getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("B 알림 [되돌리기] → 진행중으로", TOAST + "await W(600);return '처리완료='+!!wf().completedProcessed+' | 물어본 횟수='+window.__cf+' | 알림='+toast()")
step("C [↩ 완료 취소]도 묻지 않음 · [되돌리기]로 다시 완료", TOAST + "app.markWorkflowDone(8981);await W(500);app.undoMarkWorkflowDone(8981);await W(500);const a='취소 뒤 처리완료='+!!wf().completedProcessed+' 물어본 횟수='+window.__cf;undoBtn().click();await W(500);return a+' | 되돌리기 뒤 처리완료='+!!wf().completedProcessed")
step("정리", "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==8981);app.saveData();app.displayWorkflows();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
