import json, sys, glob, os
# 실제 업무 파일(내보내기 .json)을 가져와서 체크·체크 취소를 실제 클릭으로 반복 → 멈춤·화면 튐 확인 → steps3.json
# 쓰는 법: python mk_real_test.py "<업무 파일 경로>" [1366x768]
src = os.path.abspath(sys.argv[1]).replace('\\', '/')
url = 'file:///' + src
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===window.__wid);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
H = ("const cardAt=i=>document.querySelector(`.checklist-card[data-workflow-id=\"${window.__wid}\"][data-index=\"${i}\"]`);"
     "const sc=()=>document.getElementById('focus-checklist-scroll-'+window.__wid);"
     "const outer=()=>[...document.querySelectorAll('*')].filter(x=>x.scrollTop>0&&x!==sc()&&x.id!=='aiPanelOfflineDashboard'&&!x.closest('.modal')).map(x=>(x.id||x.className.toString().split(' ')[0]||x.tagName)+':'+Math.round(x.scrollTop));"
     "const vis=()=>{const s=sc();if(!s)return 0;const b=s.getBoundingClientRect();return [...s.querySelectorAll('.checklist-card')].filter(x=>{const r=x.getBoundingClientRect();return r.bottom>b.top&&r.top<b.bottom}).length};"
     "const lt=()=>{const a=window.__lt||[];window.__lt=[];return '긴 작업 '+a.length+'개 최대 '+Math.round(Math.max(0,...a))+'ms 합 '+Math.round(a.reduce((s,x)=>s+x,0))+'ms'};")
S = []
if len(sys.argv) > 2: S.append({'viewport': [int(v) for v in sys.argv[2].split('x')]})
def step(label, body): S.append({"label": label, "js": P + H + body + E})

step("가져오기", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(e.duration))).observe({entryTypes:['longtask']});"
     f"const t0=performance.now();const txt=await (await fetch({json.dumps(url)})).text();const before=new Set(app.allData.workflows.map(w=>w.id));"
     "await app.importTemplateFile([new File([txt],'업무.json',{type:'application/json'})]);await W(1500);"
     "const pick=[...document.querySelectorAll('.modal.show button')].find(b=>/이어서|그대로|가져오기|새로 시작/.test(b.textContent));const pl=pick?pick.textContent.trim():'-';pick&&pick.click();await W(2500);"
     "const nw=app.allData.workflows.find(w=>!before.has(w.id));if(!nw)return '가져온 업무 없음 | 버튼='+pl;window.__wid=nw.id;"
     "return '가져옴: '+nw.title+' | 줄 '+nw.checklist.length+' 끝난 줄 '+nw.checklist.filter(c=>c.completed).length+' | 고른 버튼='+pl+' | '+Math.round(performance.now()-t0)+'ms | '+lt()")
step("일하는 화면 열기", "const t0=performance.now();document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.displayWorkflows();await W(300);app.focusWorkflow(window.__wid);await W(2500);return '열기 '+Math.round(performance.now()-t0)+'ms | 보이는 줄='+vis()+' | 바깥 스크롤='+outer().join(',')+' | '+lt()")
S.append({"shot": "rl_0.png"})
if len(sys.argv) > 3 and sys.argv[3] == 'diag':
    # 진단: 끝난 단계 체크가 왜 안 풀리는지
    step("진단", "const cl=wf().checklist;const i=cl.findIndex(c=>c.text.startsWith('범죄인지서'));const c=cardAt(i);const s=sc();s.scrollTop+=c.getBoundingClientRect().top-s.getBoundingClientRect().top-200;await W(400);"
         "const inp=c.querySelector('input[type=checkbox]');const z=c.querySelector('.cl-check-zone');const r=inp.getBoundingClientRect();const at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);"
         "const info='input 크기 '+Math.round(r.width)+'x'+Math.round(r.height)+' disabled='+inp.disabled+' title='+(inp.title||z?.title||'')+' | 그 자리 요소='+(at?.tagName+'.'+(at?.className||'').toString().slice(0,30))+' | 협업='+JSON.stringify(wf().collab?{role:wf().collab.role,me:wf().collab.me}:null)+' 레퍼런스='+!!wf().isReference;"
         "const b=cl[i].completed;app.toggleChecklistItem(window.__wid,i);await W(800);const dlg=[...document.querySelectorAll('.modal.show h3,.modal.show h2,.toast')].map(x=>x.textContent.trim().slice(0,60)).join('|');return info+' | 직접 호출: '+b+'→'+cl[i].completed+' | 창/알림='+dlg")
    S.append({"shot": "rl_diag.png"})
    json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
    sys.exit(0)
# 계획: 끝난 줄 체크 취소 → 다시 체크 → 남은 줄 몇 개 체크 → 다시 취소
SEQ = len(sys.argv) > 3 and sys.argv[3] == 'seq'
if SEQ:
    step("계획 세우기(차례로)", "const cl=wf().checklist;window.__plan=cl.map((c,i)=>i).filter(i=>!cl[i].completed&&cl[i].skipped!==true&&!(!app._isSubEntry(cl[i])&&app.findSubItems(cl,i).some(x=>x.item.skipped!==true)));return '순서='+window.__plan.join(',')")
else:
  step("계획 세우기", "const cl=wf().checklist;const done=cl.map((c,i)=>[c,i]).filter(([c])=>c.completed&&c.skipped!==true).map(([,i])=>i);const todo=cl.map((c,i)=>[c,i]).filter(([c])=>!c.completed&&c.skipped!==true).map(([,i])=>i).slice(0,6);"
     "const d=done.slice(-6).reverse();window.__plan=[...d,...d.slice().reverse(),...todo,...todo.slice().reverse()];return '순서(줄 번호)='+window.__plan.join(',')")
N = 32 if SEQ else 24
for k in range(N):
    S.append({"pt": True, "js": P + H + "document.querySelectorAll('.modal.show').forEach(m=>{const b=[...m.querySelectorAll('button')].find(b=>/단계만|모두 풀기|함께 완료/.test(b.textContent));b&&b.click()});await W(300);"
              "const i=window.__plan.shift();window.__cur=i;if(i===undefined)return JSON.stringify([5,5]);let c=cardAt(i);"
              "if(!c){const cl=wf().checklist;const si=app._stageIndexOf(cl,i);const s=cardAt(si);const b=s&&[...s.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d+\\/\\d+$/.test(x.textContent.trim()));b&&b.click();await W(700);c=cardAt(i);}"
              "if(!c)return JSON.stringify([5,5]);const s=sc();s.scrollTop+=c.getBoundingClientRect().top-s.getBoundingClientRect().top-s.clientHeight/2;await W(400);"
              "window.__b={top:Math.round(c.getBoundingClientRect().top),st:Math.round(s.scrollTop),done:!!wf().checklist[i].completed};window.__lt=[];const cb=[...c.querySelectorAll('input[type=checkbox], .cl-check-zone')].find(x=>x.getBoundingClientRect().width>8);const r=cb.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])" + E})
    S.append({"clickpt": 1})
    step(f"클릭 {k+1}", "await W(1300);const i=window.__cur;if(i===undefined)return '(계획 끝)';const c=cardAt(i);const it=wf().checklist[i];const dlg=[...document.querySelectorAll('.modal.show h3, .modal.show h2')].map(x=>x.textContent.trim()).join('|');"
         "return '줄 '+i+' 「'+(it.text||'').slice(0,18)+'」 '+(window.__b.done?'끝남→':'안 끝남→')+(it.completed?'끝남':'안 끝남')+' | 줄 위치 '+window.__b.top+'→'+(c?Math.round(c.getBoundingClientRect().top):'안 보임')+' | 목록 스크롤 '+window.__b.st+'→'+Math.round(sc().scrollTop)+' | 보이는 줄='+vis()+' | 바깥 스크롤='+(outer().join(',')||'없음')+' | 목록 상자 위='+Math.round(sc().getBoundingClientRect().top)+' 화면에 보이는 높이='+Math.round(Math.min(innerHeight,sc().getBoundingClientRect().bottom)-Math.max(0,sc().getBoundingClientRect().top))+'/'+sc().clientHeight+' | '+lt()+(dlg?' | 창: '+dlg:'')")
    if k in (0, 5, 11, 17, 23): S.append({"shot": f"rl_{k+1}.png"})
# 맨 아래까지 내리기: 마우스 휠로 조금씩, 단계를 모두 펼친 상태에서
step("모든 단계 펼치기", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const cl=wf().checklist;cl.forEach((c,i)=>{const s=cardAt(i);if(!s)return;const b=[...s.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d+\\/\\d+$/.test(x.textContent.trim()));if(b&&app.findSubItems(cl,i).length&&!cardAt(app.findSubItems(cl,i)[0].index))b.click()});await W(1200);const s=sc();return '목록 높이 '+s.scrollHeight+' / 보이는 높이 '+s.clientHeight+' | 보이는 줄='+vis()")
S.append({"pt": True, "js": P + H + "const s=sc().getBoundingClientRect();return JSON.stringify([s.left+s.width/2,s.top+s.height/2])" + E})
for k in range(12):
    S.append({"wheel": 400})
    step(f"휠 {k+1}", "await W(500);const s=sc();const cards=[...s.querySelectorAll('.checklist-card')];const b=s.getBoundingClientRect();const last=cards[cards.length-1].getBoundingClientRect();return '목록 스크롤 '+Math.round(s.scrollTop)+'/'+(s.scrollHeight-s.clientHeight)+' | 보이는 줄='+vis()+' | 마지막 줄 아래 빈칸='+Math.round(b.bottom-last.bottom)+'px | 바깥 스크롤='+(outer().join(',')||'없음')+' | '+lt()")
    if k in (5, 11): S.append({"shot": f"rl_w{k+1}.png"})
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
