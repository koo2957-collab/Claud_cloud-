import json, sys
# 업무 절차 패널: 다른 항목을 고르면 맨 위 한 줄 + 제자리 펼침 (상자는 하나) 시험 → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7601);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
H = ("const card=t=>[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text, .fci-title-text')?.textContent.trim().replace(/[•·].*$/,'').trim()===t);"
     "const st=()=>{const box=document.getElementById('aiPanelOfflineDashboard');const pk=document.getElementById('procPick');const det=[...box.querySelectorAll('.proc-step-detail')].filter(x=>x.offsetParent);"
     "const picked=box.querySelector('.proc-step-row.is-picked');const cur=box.querySelector('.proc-step-row.is-current');const pr=picked?.querySelector('.proc-step-title').getBoundingClientRect(),br=box.getBoundingClientRect();"
     "return '한 줄='+(pk?pk.textContent.replace(/\\s+/g,' ').trim()+' (높이 '+pk.offsetHeight+')':'없음')+' | 상자 수='+det.length+' | 고른 단계='+(picked?picked.querySelector('.proc-step-title').textContent.trim():'-')+' 펼침='+!!picked?.querySelector('.proc-step-detail')"
     "+' 패널에 보임='+(pr?pr.top>=br.top&&pr.bottom<=br.bottom:'-')+' | 지금 할 일 상자='+!!cur?.querySelector('.proc-step-detail')+' | 안내문구='+!!box.querySelector('.proc-pick-empty')};")
S = []
if len(sys.argv) > 1: S.append({'viewport': [int(v) for v in sys.argv[1].split('x')]})
def step(label, body): S.append({"label": label, "js": P + H + body + E})
def click_title(t):
    unfold = r"if(!card('T')){const names=['접수','검토','결재','종결'];for(const n of names){const sc=card(n);const b=sc&&[...sc.querySelectorAll('*')].find(x=>x.children.length===0&&/^\d\/\d$/.test(x.textContent.trim()));if(b&&!card('T')){b.click();await W(500);if(!card('T')){b.click();await W(400);}}}}".replace('T', t)
    S.append({"pt": True, "js": P + H + unfold + f"const c=card('{t}');const sc=c.closest('[id^=focus-checklist-scroll]');sc.scrollTop+=c.getBoundingClientRect().top-sc.getBoundingClientRect().top-120;await W(400);const r=c.querySelector('.item-title-text, .fci-title-text').getBoundingClientRect();return JSON.stringify([r.left+15,r.top+r.height/2])" + E})
    S.append({"clickpt": 1, "wait": 450})

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['접수',0],['서류 확인',1],['보완 요청',1],['검토',0],['현장 확인',1],['의견서 작성',1],['결재',0],['기안',1],['통보',1],['종결',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7601,type:'manual',title:'미리 보기 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "wf().checklist.forEach((it,i)=>{if(i!==8)it.tip={type:'text',content:'1. '+it.text+' 업무팁 첫째 줄\\n2. 둘째 줄',saved:true};});"
     "const now=new Date().toISOString();[0,1,2].forEach(i=>{wf().checklist[i].completed=true;wf().checklist[i].completedAt=now});"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7601);await W(1800);return st()")
S.append({"shot": "pk_0.png"})
click_title("기안")
step("1 뒤쪽 할 일(기안)을 누름", "return st()")
S.append({"shot": "pk_1.png"})
S.append({"pt": True, "js": P + "const b=document.querySelector('#procPick .proc-pick-close');const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])" + E})
S.append({"clickpt": 1, "wait": 600})
step("2 「지금 할 일로」 누름", "return st()")
click_title("통보")
step("3 업무팁 없는 할 일(통보)", "return st()")
S.append({"shot": "pk_3.png"})
step("3b 준비: 고른 것 풀기", "app.clearChecklistPick(7601);await W(500);const s1=card('접수');[...s1.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d\\/2$/.test(x.textContent.trim()))?.click();await W(700);return st()")
click_title("서류 확인")
step("4 끝난 단계의 할 일(서류 확인) — 접힌 「완료」에서 펼쳐짐", "return st()")
S.append({"shot": "pk_4.png"})
click_title("종결")
step("5 다른 단계(종결)로 바로 바꿈", "return st()")
step("6 다크 모드", "document.documentElement.classList.add('dark-mode');await W(300);const pk=document.getElementById('procPick');const r=st()+' | 한 줄 배경='+getComputedStyle(pk).backgroundColor;return r")
S.append({"shot": "pk_6.png"})
step("7 Esc·정리", "document.documentElement.classList.remove('dark-mode');app.clearChecklistPick(7601);await W(400);return st()")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
