import json
# 단계 공통(물려받기) 시험: 패널·길잡이·항목 창 안내·같은 글 지우기·서식 단계↔할 일 옮기기 → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7901);const ix=t=>wf().checklist.findIndex(x=>x.text===t);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
H = ("const panel=()=>{const d=document.querySelector('#aiPanelOfflineDashboard .proc-step-row.is-current .proc-step-detail');if(!d)return '패널 상세 없음';"
     "const src=[...d.querySelectorAll('.proc-tip-src, .proc-tip-fold')].map(x=>x.textContent.replace(/\\s+/g,' ').trim());const fm=[...d.querySelectorAll('.proc-fmt-name')].map(x=>x.textContent.trim());"
     "const fold=d.querySelector('.proc-tip-fold');return '업무팁 순서=['+src.join(' / ')+'] 공통 접힘='+(fold?fold.nextElementSibling.hidden:'-')+' | 권리 고지 글 수='+(d.textContent.match(/권리 고지/g)||[]).length+' | 서식=['+fm.join(', ')+']'};"
     "const guide=()=>{const m=[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();if(!m)return '길잡이 없음';const secs=[...m.querySelectorAll('.gd-sec')].map(s=>{const h=s.querySelector('.gd-sec-h').textContent.replace(/\\s+/g,' ').trim();const f=s.querySelector('.gd-common-fold');return h+(f?'('+f.textContent.trim()+', 접힘='+f.nextElementSibling.hidden+')':'')});return '묶음=['+secs.join(' / ')+']'};"
     "const closeG=()=>document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());"
     "const note=()=>[...document.querySelectorAll('.cim-inherit')].filter(x=>x.offsetParent).map(x=>x.textContent.replace(/\\s+/g,' ').trim()).join(' || ')||'(안내 없음)';")
S = []
def step(label, body): S.append({"label": label, "js": P + H + body + E})
def pt(body): S.append({"pt": True, "js": P + H + body + E})

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const mk=async n=>{const id=await app.dbManager.saveFile('repoDocuments',{name:n,size:20000,blob:new Blob(['x'.repeat(20000)]),type:'application/octet-stream',folderId:null,uploadedAt:new Date().toISOString(),updatedAt:new Date().toISOString(),tags:[]});return id};"
     "const dQ=await mk('피의자신문조서 양식.hwpx'),d1=await mk('1피의자 출석요구서.hwpx');await app._loadRepoDocMetaCache();"
     "const cl=[['범죄인지',0],['피의자 신문',0],['1피의자',1],['2피의자',1],['3피의자',1],['송치',0],['송치서 작성',1],['기록목록 작성',1]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7901,type:'manual',title:'단계 공통 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "const c=wf().checklist;const T='1. 신문 전 권리 고지(진술거부권·변호인 조력권)\\n2. 신문조서는 피의자가 읽고 서명';c[1].tip={type:'text',content:T,saved:true};c[1].linkedDocs=[dQ];"
     "c[2].tip={type:'text',content:T,saved:true};c[2].linkedDocs=[d1];c[3].tip={type:'text',content:'1. 2피의자는 통역 필요',saved:true};c[6].tip={type:'text',content:'1. 송치서 양식 확인',saved:true};"
     "c[0].completed=true;c[0].completedAt=new Date().toISOString();app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7901);await W(1800);return 'ok'")
step("P1 패널 · 지금 할 일=1피의자(단계와 같은 글)", "return panel()")
S.append({"shot": "cm_p1.png"})
step("P2 패널 · 지금 할 일=2피의자(자기 업무팁 있음)", "app.toggleChecklistItem(7901,ix('1피의자'));await W(1200);return panel()")
S.append({"shot": "cm_p2.png"})
step("P3 패널 · 지금 할 일=3피의자(아무것도 없음)", "app.toggleChecklistItem(7901,ix('2피의자'));await W(1200);const r=panel();app.toggleChecklistItem(7901,ix('2피의자'));await W(800);app.toggleChecklistItem(7901,ix('1피의자'));await W(1200);return r")
step("G1 길잡이 · 2피의자", "await app.showChecklistHelp(7901,ix('2피의자'));await W(1400);return guide()")
pt("const m=[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();const b=m.querySelector('.gd-common-fold');b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify([r.left+30,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("G1b 「펼쳐 보기」 실제로 누름", "await W(400);return guide()")
S.append({"shot": "cm_g1.png"})
step("G2 길잡이 · 3피의자(공통만, 펼친 채)", "closeG();await W(400);await app.showChecklistHelp(7901,ix('3피의자'));await W(1400);return guide()")
S.append({"shot": "cm_g2.png"})
step("G3 길잡이 · 1피의자(같은 글은 한 번만)", "closeG();await W(400);await app.showChecklistHelp(7901,ix('1피의자'));await W(1400);const m=[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();return guide()+' | 권리 고지 글 수='+(m.textContent.match(/권리 고지/g)||[]).length")
step("G4 길잡이 · 송치서 작성(단계는 제목뿐 → 공통 없음)", "closeG();await W(400);await app.showChecklistHelp(7901,ix('송치서 작성'));await W(1400);const r=guide();closeG();await W(400);return r")
step("M1 항목 창 · 1피의자 업무팁 탭", "await app.showChecklistItemModal(7901,ix('1피의자'),'tip');await W(800);return note()")
S.append({"shot": "cm_m1.png"})
pt("const b=[...document.querySelectorAll('.cim-inherit-btn')].find(x=>x.offsetParent&&/같은 내용 지우기/.test(x.textContent));const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("M1b 「여기 같은 내용 지우기」 실제로 누름", "await W(800);const t=[...document.querySelectorAll('.toast')].map(x=>x.textContent.replace(/\\s+/g,' ').trim()).pop()||'';return '1피의자 업무팁='+JSON.stringify(wf().checklist[ix('1피의자')].tip.content)+' | 안내='+note()+' | 알림='+t.slice(0,60)")
step("M1c [되돌리기]", "const b=[...document.querySelectorAll('.toast button, .toast [class*=action]')].find(x=>/되돌리기/.test(x.textContent));b&&b.click();await W(800);return '되돌림 후 업무팁 있음='+!!wf().checklist[ix('1피의자')].tip.content")
step("M2 항목 창 · 단계(피의자 신문) 업무팁 탭", "await app.showChecklistItemModal(7901,ix('피의자 신문'),'tip');await W(800);return note()")
step("M3 항목 창 · 1피의자 서식 탭", "await app.showChecklistItemModal(7901,ix('1피의자'),'formats');await W(800);return note()")
S.append({"shot": "cm_m3.png"})
pt("const row=[...document.querySelectorAll('#main-checklist-formats-list-7901-'+ix('1피의자')+' [oncontextmenu]')][0];const r=row.getBoundingClientRect();return JSON.stringify([r.left+80,r.top+r.height/2])")
S.append({"rclickpt": 1, "wait": 100})
step("M3b 서식 줄 오른쪽 클릭 메뉴", "await W(400);return [...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>x.textContent.trim()).join(' / ')")
S.append({"shot": "cm_m3b.png"})
step("M3c 「단계 공통으로 옮기기」", "[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].find(x=>/단계 공통으로/.test(x.textContent)).click();await W(800);const c=wf().checklist;return '1피의자 서식 수='+(c[ix('1피의자')].linkedDocs||[]).length+' | 단계 서식 수='+(c[ix('피의자 신문')].linkedDocs||[]).length+' | 안내='+note()")
step("M3d [되돌리기]", "const b=[...document.querySelectorAll('.toast button, .toast [class*=action]')].find(x=>/되돌리기/.test(x.textContent));b&&b.click();await W(800);const c=wf().checklist;return '1피의자 서식 수='+(c[ix('1피의자')].linkedDocs||[]).length+' | 단계 서식 수='+(c[ix('피의자 신문')].linkedDocs||[]).length")
step("M4 단계 서식 줄 오른쪽 클릭 → 할 일로 옮기기 메뉴", "await app.showChecklistItemModal(7901,ix('피의자 신문'),'formats');await W(800);const row=[...document.querySelectorAll('#main-checklist-formats-list-7901-'+ix('피의자 신문')+' [oncontextmenu]')][0];const b=row.getBoundingClientRect();row.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:b.left+80,clientY:b.top+10}));await W(400);const r=[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>x.textContent.trim()).filter(t=>/옮기기/.test(t)).join(' / ');document.body.click();app.closeChecklistItemModal();return r")
step("M5 다크 모드 안내 줄", "document.documentElement.classList.add('dark-mode');await app.showChecklistItemModal(7901,ix('2피의자'),'tip');await W(700);const r=note();return r")
S.append({"shot": "cm_m5.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app.closeChecklistItemModal();return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
