import json
# 단계·자료가 많은 업무에서 체크·체크 취소할 때 멈춤·화면 튐 시험 → steps3.json
# 12단계 × 할 일 5개(72줄), 항목마다 긴 업무팁·서식 2개·조치결과, 사진 예시 여러 장
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7401);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(body): return P + body + E
S = []
import sys
if len(sys.argv) > 1: S.append({'viewport': [int(v) for v in sys.argv[1].split('x')]})
def step(label, body): S.append({"label": label, "js": J(H + body)})
def pt(body): S.append({"pt": True, "js": J(H + body)})
# 도우미: 줄 찾기 · 스크롤 상자 · 화면 상태 재기
H = ("Element.prototype.__center=function(){const sc=scroller(this);if(sc&&sc!==document.scrollingElement){sc.scrollTop+=(this.getBoundingClientRect().top-sc.getBoundingClientRect().top)-sc.clientHeight/2;}};const card=t=>[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text, .fci-title-text')?.textContent.trim().replace(/[•·].*$/,'').trim()===t);"
     "const scroller=el=>{while(el&&el!==document.body){if(/^workflow-/.test(el.id)){el=el.parentElement;continue}const cs=getComputedStyle(el);if(el.scrollHeight>el.clientHeight+2&&/(auto|scroll)/.test(cs.overflowY))return el;el=el.parentElement}return document.scrollingElement};"
     "const state=t=>{const c=card(t);const sc=c?scroller(c):null;const r=c?.getBoundingClientRect();const sr=sc?.getBoundingClientRect();"
     "const vis=sc?[...sc.querySelectorAll('.checklist-card')].filter(x=>{const b=x.getBoundingClientRect();return b.bottom>sr.top&&b.top<sr.bottom}).length:0;"
     "const pn=document.getElementById('aiPanelOfflineDashboard');"
     "const other=[...document.querySelectorAll('*')].filter(x=>x.scrollTop>0&&x!==sc&&x!==pn).map(x=>(x.id||x.className.toString().split(' ')[0]||x.tagName)+':'+Math.round(x.scrollTop));return (other.length?'[다른 곳 스크롤 '+other.join(',')+'] ':'')+'줄 위치='+(r&&sr?Math.round(r.top-sr.top):'없음')+' 목록 스크롤='+(sc?Math.round(sc.scrollTop):'-')+'/'+(sc?sc.scrollHeight-sc.clientHeight:'-')+' 보이는 줄='+vis+' 페이지 스크롤='+Math.round(document.scrollingElement.scrollTop)+' 패널 스크롤='+(pn?Math.round(pn.scrollTop):'-')};"
     "const lt=()=>{const a=window.__lt||[];window.__lt=[];return '긴 작업 '+a.length+'개 합 '+Math.round(a.reduce((s,x)=>s+x,0))+'ms 최대 '+Math.round(Math.max(0,...a))+'ms'};")

step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(e.duration))).observe({entryTypes:['longtask']});"
     "const cl=[];for(let s=1;s<=12;s++){cl.push({text:'단계 '+s+' 업무 처리',indent:0,completed:false});for(let k=1;k<=5;k++)cl.push({text:'할 일 '+s+'-'+k,indent:1,completed:false});}"
     "app.allData.workflows.unshift({id:7401,type:'manual',title:'큰 업무 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "const docs=[];for(let d=0;d<10;d++){docs.push(await app.dbManager.saveFile('repoDocuments',{name:'서식 '+d+'.hwpx',size:50000,blob:new Blob(['x'.repeat(50000)]),type:'application/octet-stream',folderId:null,uploadedAt:new Date().toISOString(),updatedAt:new Date().toISOString(),tags:[]}));}await app._loadRepoDocMetaCache();"
     "wf().checklist.forEach((it,i)=>{it.tip={type:'text',content:Array.from({length:12},(_,k)=>(k+1)+'. 업무팁 '+i+'번 줄 '+k+' — 처리 기준과 주의할 점을 길게 적어 둔 문장입니다').join('\\n'),saved:true};it.linkedDocs=[docs[i%10],docs[(i+3)%10]];it.result={text:'조치결과 '+i+' — 처리함'};});"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7401);await W(1500);"
     "const cv=document.createElement('canvas');cv.width=1600;cv.height=1000;const g=cv.getContext('2d');for(let i=0;i<20;i++){g.fillStyle='hsl('+i*18+',60%,50%)';g.fillRect(0,0,1600,1000);for(let k=0;k<400;k++){g.fillStyle='hsl('+(k*7)+',70%,'+(30+k%40)+'%)';g.fillRect(Math.random()*1600,Math.random()*1000,60,40);}const b=await new Promise(r=>cv.toBlob(r,'image/png'));await app.addTipFiles(7401,1+(i%12)*6,{files:[new File([b],'사진'+i+'.png',{type:'image/png'})],value:''});}"
     "await W(1500);window.__lt=[];return 'ok 줄='+wf().checklist.length+' 저장 크기='+Math.round(JSON.stringify(app.allData).length/1024)+'KB'")
S.append({"shot": "pf_0.png"})

def act(label, title, js_before=""):
    pt(js_before + f"const c=card('{title}');c.__center();await W(500);window.__before=state('{title}');window.__lt=[];const cb=c.querySelector('input[type=checkbox]')||c.querySelector('.cl-check-zone');const r=cb.getBoundingClientRect();window.__t0=performance.now();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
    S.append({"clickpt": 1})
    step(label, f"await W(1500);const dlg=[...document.querySelectorAll('.modal.show, .choice-dialog, [class*=dialog]')].filter(x=>x.offsetParent).map(x=>x.textContent.trim().slice(0,30)).join('|');return '전: '+window.__before+' → 후: '+state('{title}')+' | '+lt()+(dlg?' | 창: '+dlg:'')")

act("1 할 일 체크(중간 단계)", "할 일 1-1")
act("2 같은 줄 체크 취소", "할 일 1-1")
S.append({"shot": "pf_2.png"})
act("3 아래쪽 할 일 체크(접힌 9단계 펼쳐서)", "할 일 9-3", "const s9=card('단계 9 업무 처리');[...s9.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d\\/5$/.test(x.textContent.trim()))?.click();await W(800);")
act("4 아래쪽 할 일 체크 취소", "할 일 9-3")
S.append({"shot": "pf_4.png"})
# 1단계 할 일을 모두 끝내 단계를 넘김
step("5 준비: 1단계 할 일 4개 체크", "for(let k=2;k<=5;k++){app.toggleChecklistItem(7401,k);await W(700);}await W(800);window.__lt=[];return state('할 일 1-1')")
act("6 1단계 마지막 할 일 체크 → 단계 넘어감", "할 일 1-1")
S.append({"shot": "pf_6.png"})
act("7 끝난 1단계를 펼쳐 할 일 체크 취소", "할 일 1-1", "const s1=card('단계 1 업무 처리');[...s1.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d\\/5$/.test(x.textContent.trim()))?.click();await W(800);")
S.append({"shot": "pf_7.png"})
act("8 끝난 단계(단계 줄) 체크 취소 → 묻는 창", "단계 2 업무 처리", "app.toggleChecklistItem(7401,6,{confirmed:true});await W(900);for(let k=7;k<=11;k++){app.toggleChecklistItem(7401,k);await W(500);}await W(900);")
S.append({"shot": "pf_8.png"})
# 화면 아래쪽까지 내린 상태에서 위쪽 단계 체크 취소 (단계가 다시 펼쳐지며 목록 길이가 바뀜)
# 항목 창 위쪽 체크박스로 체크·취소
def actm(label):
    pt("const cb=document.querySelector('#cimOverlay input[type=checkbox], .cim-header input[type=checkbox]')||[...document.querySelectorAll('input[type=checkbox]')].filter(x=>x.offsetParent&&x.closest('[id*=cim], [class*=cim]')).pop();window.__before=state('할 일 4-2');window.__lt=[];const r=cb.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
    S.append({"clickpt": 1})
    step(label, "await W(1500);const ov=[...document.querySelectorAll('[id*=cim], [class*=cim-modal]')].filter(x=>x.offsetParent).length;return '전: '+window.__before+' → 후: '+state('할 일 4-2')+' | '+lt()+' | 항목 창 보임='+ov")
step("M0 항목 창 열기(4단계 할 일)", "document.querySelectorAll('.modal.show').forEach(m=>{const b=[...m.querySelectorAll('button')].find(b=>/취소/.test(b.textContent));b&&b.click()});await W(500);const s4=card('단계 4 업무 처리');[...s4.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d\\/5$/.test(x.textContent.trim()))?.click();await W(800);card('할 일 4-2').__center();await W(400);await app.showChecklistItemModal(7401,wf().checklist.findIndex(x=>x.text==='할 일 4-2'),'result');await W(900);window.__lt=[];return state('할 일 4-2')")
actm("M1 항목 창에서 체크")
S.append({"shot": "pf_m1.png"})
actm("M2 항목 창에서 체크 취소")
S.append({"shot": "pf_m2.png"})
step("M3 닫기", "app.closeChecklistItemModal();await W(600);return state('할 일 4-2')")
# 줄을 눌러 조치결과 칸을 펼친 상태에서 체크·취소
pt("const c=card('할 일 4-3');c.__center();await W(400);const t=c.querySelector('.item-title-text, .fci-title-text');const r=t.getBoundingClientRect();return JSON.stringify([r.left+20,r.top+r.height/2])")
S.append({"clickpt": 1})
act("P1 펼친 줄에서 체크", "할 일 4-3")
act("P2 펼친 줄에서 체크 취소", "할 일 4-3")
S.append({"shot": "pf_p2.png"})
step("9 묻는 창 닫기", "document.querySelectorAll('.modal.show').forEach(m=>{const b=[...m.querySelectorAll('button')].find(b=>/취소/.test(b.textContent));b&&b.click()});await W(600);return state('단계 3 업무 처리')")
step("9b 맨 아래로 내림 후 상태", "const sc=scroller(card('단계 12 업무 처리'));sc.scrollTop=1e6;await W(600);return state('단계 12 업무 처리')")
# 진행률 100% → 체크 취소
step("10 준비: 전부 끝냄(100%)", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const cl=wf().checklist;const now=new Date().toISOString();cl.forEach(it=>{it.completed=true;it.completedAt=now});cl[cl.length-1].completed=false;app.saveData();app.displayWorkflows();await W(500);app.focusWorkflow(7401);await W(1200);app.toggleChecklistItem(7401,cl.length-1);await W(1500);window.__lt=[];return '진행률='+app.calculateProgress(wf())+' | '+state('단계 12 업무 처리')")
S.append({"shot": "pf_10.png"})
act("11 100%에서 마지막 할 일 체크 취소", "할 일 12-5", "const s12=card('단계 12 업무 처리');[...s12.querySelectorAll('*')].find(x=>x.children.length===0&&/^\\d\\/5$/.test(x.textContent.trim()))?.click();await W(800);")
S.append({"shot": "pf_11.png"})
act("12 다시 체크해서 100%", "할 일 12-5")
S.append({"shot": "pf_12.png"})
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
