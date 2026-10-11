import json
# 단계가 끝나 접히는 동안 빠른 클릭 무시 시험 → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7701);"
E = "}catch(e){return 'ERR '+e.message}})()"
H = ("const card=t=>[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text, .fci-title-text')?.textContent.trim().replace(/[•·].*$/,'').trim()===t);"
     "const st=()=>wf().checklist.map(c=>(c.completed?'✓':'·')+c.text).join(' ')+' | 클릭 기록='+(window.__clk||[]).map(([t,b])=>((t-window.__clk[0][0])/1000).toFixed(2)+'초'+(b?'(막음)':'')).join(', ');"
     "const ptOf=t=>{const c=card(t);const b=[...c.querySelectorAll('input[type=checkbox], .cl-check-zone')].find(x=>x.getBoundingClientRect().width>8);const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])};")
S = []
def step(label, body): S.append({"label": label, "js": P + H + body + E})
def pt(t): S.append({"pt": True, "js": P + H + f"return ptOf('{t}')" + E})

step("seed", "localStorage.setItem('startupPromptShown','1');window.__clk=[];document.addEventListener('click',e=>{if(e.isTrusted)window.__clk.push([performance.now(),Date.now()<(app._clickBlockUntil||0)])},true);localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['가 단계',0],['가-1',1],['가-2',1],['나 단계',0],['나-1',1],['나-2',1],['다 단계',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7701,type:'manual',title:'빠른 클릭 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7701);await W(1500);app.toggleChecklistItem(7701,1);await W(1200);return st()")
pt("가-2")
S.append({"clickpt": 1})
S.append({"wait": 0, "clickpt": 1})
step("0.3초 뒤 같은 자리 다시 누름(접히기 전)", "return st()+' | 막는 중='+(Date.now()<app._clickBlockUntil)")
S.append({"clickpt": 1})
step("0.7초쯤 같은 자리 또 누름(접히는 중)", "return st()")
S.append({"wait": 1000})
step("접기 끝난 뒤 상태", "return st()+' | 막는 중='+(Date.now()<app._clickBlockUntil)")
pt("나-1")
S.append({"clickpt": 1})
step("1.5초 뒤 나-1 누름 → 정상 체크", "await W(500);return st()")
pt("나-1")
S.append({"clickpt": 1})
step("나-1 다시 눌러 체크 취소(평소 체크는 막지 않음)", "await W(500);return st()")
S.append({"shot": "hold_1.png"})
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
