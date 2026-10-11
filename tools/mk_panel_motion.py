import json, sys
# 업무 절차 패널: 고정 머리(완료 개수 늘 보임)·단계 넘어갈 때 한 번만 움직임·가운데 목록과 같은 때·고른 항목 겹침 시험 → steps3.json
# 쓰는 법: python mk_panel_motion.py [1366x768]
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7801);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
H = ("const card=t=>[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text, .fci-title-text')?.textContent.trim().replace(/[•·].*$/,'').trim()===t);"
     "const ps=()=>{const box=document.getElementById('aiPanelOfflineDashboard');const b=box.getBoundingClientRect();const hd=document.getElementById('procHead');const hb=hd?hd.getBoundingClientRect().bottom:b.top;"
     "const prog=document.getElementById('procProg');const pk=document.getElementById('procPick');const cur=box.querySelector('.proc-step-row.is-current .proc-step-title');const t=performance.now()-(window.__t0||0);"
     "const vis=el=>{if(!el)return '-';const r=el.getBoundingClientRect();return r.top>=b.top-1&&r.bottom<=b.bottom+1?'보임':'안 보임'};"
     "return (t/1000).toFixed(2)+'초 | 머리 둘째 줄='+(pk?'고른 줄 「'+pk.textContent.replace(/\\s+/g,' ').trim()+'」':prog?'「'+prog.textContent.replace(/\\s+/g,' ').trim()+'」 '+vis(prog):'없음')+' | 패널 스크롤='+Math.round(box.scrollTop)+' | 진행중 제목(머리 아래 기준)='+(cur?Math.round(cur.getBoundingClientRect().top-hb)+'px 「'+cur.textContent.trim().slice(0,8)+'」':'-')+' | 배='+!!document.querySelector('.proc-sailboat')};")
S = []
if len(sys.argv) > 1: S.append({'viewport': [int(v) for v in sys.argv[1].split('x')]})
def step(label, body): S.append({"label": label, "js": P + H + body + E})
step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[];['접수','사실 확인','관계인 조사','내사 결과 보고','입건 여부 결정','피의자 신문','수사 결과 보고','송치'].forEach((s,k)=>{cl.push({text:s,indent:0,completed:false});for(let j=1;j<=3;j++)cl.push({text:s+' 할 일 '+j,indent:1,completed:false});});"
     "app.allData.workflows.unshift({id:7801,type:'manual',title:'패널 움직임 시험 — 구급활동 방해 내사(+수사) 사건 처리 절차',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>{app.ensureChecklistItemId(it);it.tip={type:'text',content:'1. '+it.text+' 업무팁\\n2. 확인할 것\\n3. 주의할 것\\n4. 근거 확인',saved:true};});"
     "const now=new Date().toISOString();for(let i=0;i<12;i++){wf().checklist[i].completed=true;wf().checklist[i].completedAt=now;}"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7801);await W(2000);app.toggleChecklistItem(7801,13);await W(1500);app.toggleChecklistItem(7801,14);await W(1500);return ps()")
S.append({"shot": "pm_0.png"})
step("패널을 아래로 내려도 완료 줄은 머리에", "const box=document.getElementById('aiPanelOfflineDashboard');box.scrollTop=400;await W(300);const r=ps();box.scrollTop=0;window.__t0=0;return r")
S.append({"pt": True, "js": P + H + "const c=card('내사 결과 보고 할 일 3');const b=[...c.querySelectorAll('input[type=checkbox], .cl-check-zone')].find(x=>x.getBoundingClientRect().width>8).getBoundingClientRect();window.__t0=performance.now();window.__log=[];const box=document.getElementById('aiPanelOfflineDashboard');let last='';const tick=()=>{const cur=box.querySelector('.proc-step-row.is-current .proc-step-title');const k=(cur?cur.textContent.trim().slice(0,6):'')+'@'+Math.round(box.scrollTop);if(k!==last){window.__log.push(((performance.now()-window.__t0)/1000).toFixed(2)+'초 '+k+(card('내사 결과 보고 할 일 1')?'':' (가운데 접힘)'));last=k}if(performance.now()-window.__t0<2500)requestAnimationFrame(tick)};requestAnimationFrame(tick);return JSON.stringify([b.left+b.width/2,b.top+b.height/2])" + E})
S.append({"clickpt": 1})
step("단계 마지막 할 일 실제 클릭 → 변화 기록(진행중 제목@패널 스크롤)", "await W(2600);return window.__log.join(' → ')")
step("넘어간 뒤", "return ps()")
S.append({"shot": "pm_1.png"})
step("완료 줄 눌러 끝난 단계 펼치기", "document.getElementById('procProg').click();await W(700);const box=document.getElementById('aiPanelOfflineDashboard');const f=document.getElementById('procFoldList');const r=f.getBoundingClientRect(),b=box.getBoundingClientRect(),hb=document.getElementById('procHead').getBoundingClientRect().bottom;return '펼침='+document.getElementById('procFold').classList.contains('open')+' | 끝난 단계 줄 수='+f.querySelectorAll('.proc-step-row').length+' | 목록 위치(머리 아래 기준)='+Math.round(r.top-hb)+'px | 화살표 돌아감='+document.getElementById('procProg').classList.contains('open')")
S.append({"shot": "pm_2.png"})
step("다시 접기", "document.getElementById('procProg').click();await W(500);return '펼침='+document.getElementById('procFold').classList.contains('open')")
step("아래 항목 고르기(송치 할 일 2) → 머리와 겹침 확인", "const s=card('송치');if(!card('송치 할 일 2')){[...s.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d\\/\\d$/.test(x.textContent.trim()))?.click();await W(600);}app.toggleChecklistPeek(7801,wf().checklist.findIndex(x=>x.text==='송치 할 일 2'));await W(900);"
     "const box=document.getElementById('aiPanelOfflineDashboard');const hb=document.getElementById('procHead').getBoundingClientRect().bottom;const t=box.querySelector('.proc-step-row.is-picked .proc-step-title').getBoundingClientRect();return ps()+' | 고른 단계 제목(머리 아래 기준)='+Math.round(t.top-hb)+'px | 겹침='+(t.top<hb)")
S.append({"shot": "pm_3.png"})
step("지금 할 일로", "document.querySelector('#procPick .proc-pick-close').click();await W(700);return ps()")
step("다크 모드 머리 배경", "document.documentElement.classList.add('dark-mode');await W(300);const r=getComputedStyle(document.getElementById('procHead')).backgroundColor;return r")
S.append({"shot": "pm_4.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
