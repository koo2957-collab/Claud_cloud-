# 추천 1~4 시험 대본 → steps3.json
# 1 삭제 통일(묻지 않고 휴지통 + [실행 취소]·Ctrl+Z — 일하는 화면 [삭제]·업무 관리 Delete·오른쪽 클릭)
# 2 법령·서식 오른쪽 클릭 「새 판으로 바꾸기…」(이름이 달라도 같은 자료 자리에 · 쓰는 곳에 반영 · Esc 취소 · [되돌리기])
# 3 서식 같은 이름 교체 창: 「쓰는 할 일 n곳」 · 법령 창과 같은 단추 이름
# 4 새 업무 [초기화]: 묻지 않고 비우고 [되돌리기]로 되살림
# 실행: (tools 폴더에서) python mk_reco_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
     "const toast=()=>{const t=document.getElementById('toast');return t&&t.classList.contains('show')?document.getElementById('toastMessage').textContent.replace(/\\s+/g,' ').trim().slice(0,90):'-'};"
     "const undoBtn=()=>document.querySelector('#toastMessage .toast-undo-btn');"
     "const choice=()=>[...document.querySelectorAll('.modal.show')].reverse().find(m=>m.querySelector('button[data-choice]'));"
     "const ctxt=()=>{const c=choice();return c?c.textContent.replace(/\\s+/g,' ').trim().slice(0,160):'-'};"
     "const nWf=()=>app.allData.workflows.filter(w=>!w.isDeleted&&!w.isDraft).length;"
     "const btnT=(root,t)=>[...(root||document).querySelectorAll('button,.wfm-ctx-item')].find(b=>b.getClientRects().length&&b.textContent.replace(/\\s+/g,' ').includes(t));")
E = "}catch(e){return 'ERR '+e.message}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr): S.append({"pt": True, "js": J("let el=null;try{el=" + expr + ";}catch(e){}if(!el)return JSON.stringify([2,2]);el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(14,b.width/2),b.top+b.height/2])")})
def click(expr): pt(expr); S.append({"clickpt": 1})
def rclick(expr): pt(expr); S.append({"rclickpt": 1})
def key(k, vk, mods=0): S.append({"key": k, "vk": vk, "mods": mods})
def text(t): S.append({"text": t})

step("준비", "window.__c=0;window.confirm=m=>{window.__c++;window.__lc=String(m).slice(0,50);return true};localStorage.setItem('deadlineNotifyMode','off');localStorage.setItem('welcomeShown','1');app.checkBackupReminder=()=>{};document.getElementById('welcomeModal')?.remove();document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "await app.insertPracticeWorkflows();await W(2500);const ps=app.allData.workflows.filter(w=>w.isPractice);window.__pw=ps.find(w=>/소모품/.test(w.title)).id;window.__pm=ps.find(w=>/월간/.test(w.title)).id;return '업무='+nWf()")
# ── 1 삭제 통일
step("1-1 일하는 화면 [삭제] → 묻지 않음 · 목록으로 · [실행 취소]", "app.focusWorkflow(window.__pm);await W(1200);btnT(document.getElementById('focusActionPanel'),'삭제').click();for(let k=0;k<20&&!undoBtn();k++)await W(200);await W(700);return '확인창='+window.__c+' · 일하는 화면='+app.focusMode+' · 업무='+nWf()+' · 알림='+toast()")
click("undoBtn()")
step("1-2 [실행 취소] → 되살아남", "await W(700);return '업무='+nWf()+' · 지워짐='+!!app.allData.workflows.find(w=>w.id===window.__pm).isDeleted")
step("1-2b 지운 바로 뒤(화면이 사라지는 중) [실행 취소]도 되살아남", "app.focusWorkflow(window.__pm);await W(1200);btnT(document.getElementById('focusActionPanel'),'삭제').click();await W(30);const b=undoBtn();b&&b.click();await W(800);return '단추='+!!b+' · 지워짐='+!!app.allData.workflows.find(w=>w.id===window.__pm).isDeleted+' · 일하는 화면='+app.focusMode")
step("1-3 업무 관리에서 고르고 Delete", "app.openWorkflowManager();for(let k=0;k<30&&!document.querySelector('#workflowManagerModal tr[data-sel-key=\"'+window.__pm+'\"]');k++)await W(300);await W(300);const r=document.querySelector('#workflowManagerModal tr[data-sel-key=\"'+window.__pm+'\"]');r.click();await W(300);return '골라짐='+r.classList.contains('wfm-row-selected')")
key("Delete", 46)
step("1-4 Delete 결과", "for(let k=0;k<20&&!undoBtn();k++)await W(200);return '확인창='+window.__c+' · 업무='+nWf()+' · 알림='+toast()")
key("z", 90, 2)
step("1-5 Ctrl+Z → 되살아남", "await W(700);return '업무='+nWf()+' · 알림='+toast()")
rclick("document.querySelector('#workflowManagerModal tr[data-sel-key=\"'+window.__pm+'\"]')")
click("btnT(document.getElementById('wfmCtxMenu'),'삭제')")
step("1-6 오른쪽 클릭 「삭제」", "await W(700);return '확인창='+window.__c+' · 업무='+nWf()+' · 알림='+toast()")
click("undoBtn()")
step("1-7 [실행 취소]", "await W(700);app.closeModal('workflowManagerModal');await W(300);return '업무='+nWf()")
step("1-8 휴지통의 영구 삭제는 계속 묻는가", "const w={id:Date.now(),type:'manual',title:'영구 삭제 시험',checklist:[{text:'a'}],isDeleted:true,deletedAt:new Date().toISOString(),date:'x'};app.allData.workflows.push(w);app.saveData();const c0=window.__c;window.confirm=m=>{window.__c++;window.__lc=String(m).slice(0,50);return false};app.openTrashModal();await W(600);app.trashDeleteOne&&app.trashDeleteOne(w.id);await W(500);const ask=window.__c-c0;const cd=choice();const asked=ask>0||!!cd;cd&&[...cd.querySelectorAll('button')].pop().click();window.confirm=m=>{window.__c++;return true};await W(300);app.closeModal('trashModal');return '물음='+asked+' · 남음='+app.allData.workflows.some(x=>x.id===w.id)")
# ── 2 새 판으로 바꾸기 (법령)
step("2-0 법령·매뉴얼 열기", "await app.openLawLibrary();await W(900);const fs=await app._getAllLibraryFiles();window.__lf=fs.find(x=>/시행령/.test(x.name));return window.__lf.name+' · 쓰는 업무='+app._fbUsageOf('law',window.__lf.id).n")
rclick("document.querySelector('#lawLibraryModal [data-sel-key=\"'+window.__lf.id+'\"]')")
step("2-1 오른쪽 클릭 메뉴", "await W(300);const m=document.getElementById('fbCtxMenu');return m&&m.style.display!=='none'?m.textContent.replace(/\\s+/g,' ').trim():'없음'")
S.append({"shot": "reco_law_ctx.png"})
step("2-1b 메뉴 닫기", "document.getElementById('fbCtxMenu').style.display='none';return 'ok'")
step("2-2 다른 이름의 새 판 고름 → 묻는 창", "window.__nf=new File(['%PDF-1.4 새 판 '+'9'.repeat(900)],'지방계약법 시행령(2026.12.1. 시행).pdf',{type:'application/pdf'});app._fbReplaceVersionWith('law',window.__lf.id,window.__nf);await W(800);return ctxt()")
S.append({"shot": "reco_law_ask.png"})
key("Escape", 27)
step("2-3 Esc → 그대로", "await W(500);const f=await app._getLibraryFileById(window.__lf.id);return '이름='+f.name+' · 창='+!!choice()")
step("2-4 다시 → [새 판으로 바꾸기]", "app._fbReplaceVersionWith('law',window.__lf.id,window.__nf);await W(800);btnT(choice(),'새 판으로 바꾸기').click();await W(1500);const fs=await app._getAllLibraryFiles();const f=fs.find(x=>x.id===window.__lf.id);return '같은 번호 이름='+f.name+' · 크기='+f.size+' · 파일 수='+fs.length+' · 쓰는 업무='+app._fbUsageOf('law',window.__lf.id).n+' · 알림='+toast()")
step("2-5 업무 카드 참고 자료에 새 이름", "app.closeModal('lawLibraryModal');await W(300);app.focusWorkflow(window.__pw);await W(1500);const t=(document.querySelector('.ref-chip, .proj-ref-chips, [class*=ref-chip]')||{textContent:''}).closest?.('div')?.textContent||document.body.textContent;return '새 이름 보임='+document.body.textContent.includes('2026.12.1. 시행')")
S.append({"shot": "reco_law_card.png"})
click("undoBtn()")
step("2-6 알림 [되돌리기] → 예전 판", "await W(1500);const f=await app._getLibraryFileById(window.__lf.id);return '이름='+f.name+' · 크기='+f.size+' · 알림='+toast()")
step("2-7 다시 바꾸고 Ctrl+Z", "app.exitFocusMode();await W(400);await app.openLawLibrary();await W(700);app._fbReplaceVersionWith('law',window.__lf.id,window.__nf);await W(800);btnT(choice(),'새 판으로 바꾸기').click();await W(1500);const a=(await app._getLibraryFileById(window.__lf.id)).name;return a")
key("z", 90, 2)
step("2-8 Ctrl+Z 결과", "await W(1500);const f=await app._getLibraryFileById(window.__lf.id);app.closeModal('lawLibraryModal');return '이름='+f.name")
step("2-9 이미 있는 다른 자료 이름으로 바꾸려 하면 막힘", "const fs=await app._getAllLibraryFiles();const other=fs.find(x=>x.id!==window.__lf.id);app._fbReplaceVersionWith('law',window.__lf.id,new File(['x'],other.name,{type:'application/pdf'}));await W(800);return '창='+!!choice()+' · 알림='+toast()")
# ── 2' 서식 새 판
step("2-10 서식 「새 판으로 바꾸기」", "const ds=await app._getAllRepoDocuments();window.__rd=ds.find(x=>/각서/.test(x.name));await app.openDocumentRepo();await W(800);app._fbReplaceVersionWith('repo',window.__rd.id,new File(['새 서식 '+'3'.repeat(500)],'각서(수의계약 배제사유) 2027년판.docx',{type:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}));await W(900);return ctxt()")
step("2-11 [새 판으로 바꾸기]", "btnT(choice(),'새 판으로 바꾸기').click();await W(1500);const d=(await app._getAllRepoDocuments()).find(x=>x.id===window.__rd.id);const w=app.allData.workflows.find(x=>x.id===window.__pw);const it=w.checklist.find(i=>(i.linkedDocs||[]).includes(window.__rd.id));return '이름='+d.name+' · 연결 그대로='+!!it+' · 알림='+toast()")
click("undoBtn()")
step("2-12 [되돌리기]", "await W(1200);const d=(await app._getAllRepoDocuments()).find(x=>x.id===window.__rd.id);return '이름='+d.name")
# ── 3 서식 같은 이름 교체 창
step("3-1 같은 이름 새 판 올리기 → 창 문구·단추", "app._fbCfg('repo').upload([new File(['새 판 '+'4'.repeat(300)],window.__rd.name,{type:'application/octet-stream'})],null);await W(1500);const m=[...document.querySelectorAll('.modal.show')].pop();return m.textContent.replace(/\\s+/g,' ').trim().slice(0,220)")
S.append({"shot": "reco_repo_same.png"})
key("Escape", 27)
step("3-2 Esc → 건너뜀", "await W(600);const ds=(await app._getAllRepoDocuments()).filter(x=>x.name===window.__rd.name);app.closeModal('documentRepoModal');return '같은 이름 수='+ds.length+' · 크기='+ds.map(d=>d.size).join(',')")
# ── 4 [초기화]
step("4-1 새 업무 창에 적기", "app.exitFocusMode&&app.focusMode&&app.exitFocusMode();await W(300);app.openModal('manualModal');await W(600);document.getElementById('manualProjectName').value='초기화 시험 업무';app._nwGo(2);await W(400);const inp=document.querySelector('#checklistItems .checklist-edit-item input');inp.value='1단계';app.addChecklistItem('할 일 하나',1);await W(200);app._nwGo(3);await W(500);return '단계='+app._nwStep()")
click("document.querySelector('#manualModal .nw-reset')")
step("4-2 [초기화] → 묻지 않음 · 비움 · 알림", "await W(600);return '확인창='+window.__c+' · 묻는 창='+ctxt()+' · 단계='+app._nwStep()+' · 이름=['+document.getElementById('manualProjectName').value+'] · 알림='+toast()+' · 목록에 안 보임='+!app.allData.workflows.some(w=>!w.isDraft&&w.title==='초기화 시험 업무')")
S.append({"shot": "reco_reset.png"})
click("undoBtn()")
step("4-3 [되돌리기] → 이름·절차 되살아남", "await W(800);return '단계='+app._nwStep()+' · 이름='+document.getElementById('manualProjectName').value+' · 절차='+[...document.querySelectorAll('#checklistItems .checklist-edit-item input')].map(i=>i.value).join(',')+' · 묻는 창='+ctxt()")
step("4-4 다시 [초기화] → 창 닫기 → 되돌리기(창이 다시 열림)", "document.querySelector('#manualModal .nw-reset').click();await W(500);app.closeModal('manualModal');await W(500);const open0=document.getElementById('manualModal').classList.contains('show');undoBtn()&&undoBtn().click();await W(900);return '닫힘='+!open0+' · 다시 열림='+document.getElementById('manualModal').classList.contains('show')+' · 이름='+document.getElementById('manualProjectName').value+' · 묻는 창='+ctxt()")
step("4-5 [초기화] 뒤 15초 지나면 숨겨 둔 업무 지움", "document.querySelector('#manualModal .nw-reset').click();await W(400);const held=app.allData.workflows.filter(w=>w.nwDiscarded).map(w=>w.id);await W(15600);return '숨김='+held.length+' · 15초 뒤 남음='+app.allData.workflows.filter(w=>held.includes(w.id)).length")
step("4-6 빈 창 [초기화]는 알림 없음", "await W(200);document.querySelector('#manualModal .nw-reset').click();await W(400);const r='알림='+toast();app.closeModal('manualModal');return r")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
