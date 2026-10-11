import json
def J(body): return "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.title==='징계처분 협업 시험');" + body + "}catch(e){return 'ERR '+e.message}})()"
D = "const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};"
# 체크리스트 상태 요약
SUM = ("const w=wf();if(!w)return 'no wf';const c=w.collab||{};"
       "return JSON.stringify({role:c.role||'-',me:c.me||c.owner||'',steps:Object.entries(c.steps||{}).map(([sid,s])=>{const it=w.checklist.find(x=>x.itemId===sid);return (it?it.text:sid)+'→'+s.assignee+'/'+s.status+(s.round?'/r'+s.round:'')}),"
       "items:w.checklist.map(x=>(app._isSubEntry(x)?'└':'')+x.text+(app.normalizeCompleted(x)?'✓':'')+(x.result&&x.result.text?'「'+x.result.text+'」':''))})")
dialog = "const dlg=()=>[...document.querySelectorAll('.modal.show')].map(m=>(m.querySelector('h2,h3,.modal-title,.cd-title')?.textContent||'').trim()+' :: '+[...m.querySelectorAll('button')].map(b=>b.textContent.trim()).filter(Boolean).join('/')).join(' || ');"
clickBtn = "const clickBtn=t=>{const b=[...document.querySelectorAll('.modal.show button, #collabPickModal button')].reverse().find(b=>b.textContent.trim().startsWith(t));if(!b)return false;b.click();return true;};"
S = []
PRE = dialog + clickBtn + "const sum=()=>{" + SUM + "};"
def A(label, body): S.append({"b": "A", "label": label, "js": J(PRE + body)})
def Bb(label, body): S.append({"b": "B", "label": label, "js": J(PRE + body)})

seed_people = "app._collabSavePeople([{name:'김민수',dept:'감사팀',rank:'소방장'},{name:'이수진',dept:'감사팀',rank:'소방교'}]);"
setup = ("window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));")
A("A1 관리자 PC 준비", setup + seed_people + "app._collabSetMe({dept:'감사팀',rank:'소방위',name:'홍길동'});app._collabSetMyName('홍길동');"
  "const cl=[['징계 의결 요구',0],['감찰 결과 보고서 접수',1],['징계의결요구서 작성',1],['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0],['징계 의결서 수령',1],['종결',0],['종결 보고',1]].map(([t,i])=>({text:t,indent:i,completed:false}));"
  "app.allData.workflows.unshift({id:7101,type:'manual',title:'징계처분 협업 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));app.saveData();app.displayWorkflows();await W(400);"
  "app.focusWorkflow(7101);await W(800);for(const i of [1,2])app.toggleChecklistItem(7101,i);await W(1500);return 'ok '+JSON.stringify(app._collabMe())")
B_setup = setup + seed_people
Bb("B1 담당자 PC 준비 (김민수)", B_setup + "return 'ok'")
A("A2 업무 분담 열기 → 2단계 김민수, 4단계 할 일 이수진", D +
  "app.openCollabModal(7101,'send');await W(700);[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('주소록에서 추가')).click();await W(600);"
  "for(const n of ['김민수','이수진']){[...document.querySelectorAll('#abModal .ab-person')].find(p=>p.querySelector('.ab-p-name').textContent===n).click();await W(250);}"
  "document.querySelector('#abModal .btn-primary').click();await W(700);const w=wf();const s2=w.checklist[3].itemId,s4=w.checklist[9].itemId;"
  "const sel=sid=>[...document.querySelectorAll('#collabModal select')].find(s=>(s.getAttribute('onchange')||'').includes(`'${sid}','assignee'`));"
  "const a=sel(s2);const opts=a?[...a.options].map(o=>o.value).join(','):'select 없음';if(!a)return opts;a.value='김민수';a.dispatchEvent(new Event('change',{bubbles:true}));await W(500);"
  "const b=sel(s4);b.value='이수진';b.dispatchEvent(new Event('change',{bubbles:true}));await W(500);"
  "const dl=sid=>[...document.querySelectorAll('#collabModal input[type=date]')].find(s=>(s.getAttribute('onchange')||'').includes(`'${sid}','deadline'`));const d2=dl(s2);if(d2){d2.value=D(3);d2.dispatchEvent(new Event('change',{bubbles:true}));}await W(400);"
  "const memo=document.getElementById('cbReqMemo');if(memo){memo.value='회의는 10.23.(금) 14:00입니다';memo.dispatchEvent(new Event('input',{bubbles:true}));}"
  "return 'options='+opts+' | '+sum()")
S.append({"b": "A", "shot": "c_A_send.png"})
A("A3 [요청 파일 만들기] 누름", "const btn=[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('요청 파일 만들기'));btn.click();await W(2500);return 'saved='+window.__saved.length+' '+(window.__saved[0]?window.__saved[0].name:'')+' | dlg='+dlg()+' | '+sum()")
S.append({"b": "A", "saveTo": "c_request.json"})
S.append({"b": "A", "shot": "c_A_status.png"})
# 관리자 PC에서 자기 요청 파일을 열면 → 안내
A("A4 관리자가 요청 파일을 자기 PC에서 열기 (준비)", "app.closeCollabModal&&app.closeCollabModal(true);document.getElementById('collabModal')?.remove();await W(300);return 'ok'")
S.append({"b": "A", "setFile": {"sel": "#templateFileInput", "file": "c_request.json"}})
A("A4 결과", "const t=dlg();clickBtn('확인');return t")
# 담당자 PC: 요청 파일 열기
S.append({"b": "B", "setFile": {"sel": "#templateFileInput", "file": "c_request.json"}})
Bb("B2 요청 받음 창", "const names=[...document.querySelectorAll('input[name=cbPickName]')].map(r=>r.value+(r.checked?'(선택)':''));return 'names='+names.join(',')+' | '+dlg()")
S.append({"b": "B", "shot": "c_B_pick.png"})
Bb("B3 김민수 고르고 [선택] → [네]", "const r=[...document.querySelectorAll('input[name=cbPickName]')].find(r=>r.value==='김민수');r.checked=true;clickBtn('선택');await W(500);const t=dlg();clickBtn('네, 김민수');await W(2500);return 'confirm='+t+' | '+sum()")
S.append({"b": "B", "shot": "c_B_received.png"})
Bb("B4 받은 화면 정리", "clickBtn('확인')||clickBtn('시작')||clickBtn('닫기');document.querySelectorAll('.modal.show').forEach(m=>{if(m.id!=='collabModal')m.classList.remove('show')});await W(400);return dlg()||'창 없음'")
# 담당자: 맡지 않은 단계는 잠김
Bb("B5 맡지 않은 3단계 할 일 체크 시도", "const w=wf();window.__t=[];const o=app.showToast.bind(app);app.showToast=(a,b,c,...r)=>{window.__t.push(c);return o(a,b,c,...r)};const before=app.normalizeCompleted(w.checklist[7]);app.toggleChecklistItem(w.id,7);await W(600);const t=dlg();clickBtn('확인');return 'before='+before+' after='+app.normalizeCompleted(w.checklist[7])+' | dlg='+t+' | toast='+window.__t.join(' / ')")
# 담당자: 맡은 단계 진행 (체크 + 처리결과 + 첨부)
Bb("B6 맡은 2단계 진행", "const w=wf();document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
   "await app.showChecklistItemModal(w.id,5,'result');await W(700);const rt=document.getElementById('main-checklist-result-text-'+w.id+'-5');if(rt){rt.value='10.16.(금) 등기 발송, 10.19.(월) 수령 확인';rt.dispatchEvent(new Event('input',{bubbles:true}));}"
   "const sh=document.getElementById('rf-shrink-'+w.id+'-5');if(sh)sh.checked=false;await app.addResultFiles(w.id,5,{files:[new File(['%PDF-1.4 '+'0'.repeat(20000)],'출석통지서_발송본.pdf',{type:'application/pdf'})],value:''});await W(1200);app.closeChecklistItemModal();await W(400);"
   "app.toggleChecklistItem(w.id,4);await W(500);app.toggleChecklistItem(w.id,5);await W(1500);return sum()")
S.append({"b": "B", "shot": "c_B_done.png"})
Bb("B7 [관리자에게 회신] 창", "app.openCollabReplyModal(wf().id);await W(800);const kinds=[...document.querySelectorAll('input[name=rpKind]')].map(r=>r.value+(r.checked?'(선택)':''));return 'kinds='+kinds.join(',')+' | '+dlg()")
S.append({"b": "B", "shot": "c_B_reply.png"})
Bb("B8 [회신 파일 만들기]", "const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='회신 파일 만들기');b.click();await W(2500);return 'saved='+window.__saved.length+' '+(window.__saved.at(-1)?.name||'')+' | '+dlg()")
S.append({"b": "B", "saveTo": "c_reply.json"})
# 담당자가 자기 회신 파일을 열면 → 안내
S.append({"b": "B", "setFile": {"sel": "#templateFileInput", "file": "c_reply.json"}})
Bb("B9 담당자가 자기 회신 파일 열기", "const t=dlg();clickBtn('확인');return t")
# 관리자: 회신 반영 전 상태 (2단계 회신 대기)
A("A5 회신 받기 전", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));" + "return sum()")
S.append({"b": "A", "setFile": {"sel": "#templateFileInput", "file": "c_reply.json"}})
A("A6 회신 반영 결과", "await W(1500);const t=dlg();const w=wf();const files=app._collabResultFiles(w.id,w.checklist[5].itemId).map(f=>f.name);return 'dlg='+t+' | files='+files.join(',')+' | '+sum()")
S.append({"b": "A", "shot": "c_A_merged.png"})
A("A7 같은 회신 다시 열기 (준비)", "clickBtn('확인')||clickBtn('닫기');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));await W(300);return 'ok'")
S.append({"b": "A", "setFile": {"sel": "#templateFileInput", "file": "c_reply.json"}})
A("A7 결과 (중복 반영 막힘?)", "await W(800);const t=dlg();clickBtn('확인');return t")
# 관리자가 아직 회신 안 온 이수진 단계를 직접 체크하면
A("A8 회신 대기(이수진) 할 일 체크 → 묻는 창 → [회신 기다리기]", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const w=wf();app.focusWorkflow(w.id);await W(800);const before=app.normalizeCompleted(w.checklist[9]);app.toggleChecklistItem(w.id,9);await W(600);const t=dlg();const msg=[...document.querySelectorAll('.modal.show')].pop()?.innerText.replace(/\s+/g,' ').slice(0,260);clickBtn('회신 기다리기');await W(400);return 'after='+app.normalizeCompleted(w.checklist[9])+' | dlg='+t+' | msg='+msg+' | '+sum()")
S.append({"b": "A", "shot": "c_A_locked.png"})
A("A9 메인 화면 사이드바 회신 대기", "app.exitFocusMode&&app.exitFocusMode();await W(800);const s=document.querySelector('.sidebar');return (s?s.innerText:'').replace(/\\s+/g,' ').slice(0,300)")
S.append({"b": "A", "shot": "c_A_sidebar.png"})

def C(label, body): S.append({"b": "C", "label": label, "js": J(PRE + body)})
C("C1 담당자 PC 준비 (이수진)", B_setup + "return 'ok'")
S.append({"b": "C", "setFile": {"sel": "#templateFileInput", "file": "c_request.json"}})
C("C2 이수진 고르기", "const r=[...document.querySelectorAll('input[name=cbPickName]')].find(r=>r.value==='이수진');r.checked=true;clickBtn('선택');await W(500);clickBtn('네, 이수진');await W(2500);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return sum()")
C("C3 중간 회신 (아직 진행 중)", "const w=wf();await app.showChecklistItemModal(w.id,9,'result');await W(600);const rt=document.getElementById('main-checklist-result-text-'+w.id+'-9');rt.value='보고서 초안 작성 중';rt.dispatchEvent(new Event('input',{bubbles:true}));await W(800);app.closeChecklistItemModal();await W(300);"
  "app.openCollabReplyModal(w.id);await W(700);document.querySelector('input[name=rpKind][value=interim]').click();await W(200);[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='회신 파일 만들기').click();await W(2500);return 'saved='+(window.__saved.at(-1)?.name||'없음')")
S.append({"b": "C", "saveTo": "c_reply_interim.json"})
S.append({"b": "A", "setFile": {"sel": "#templateFileInput", "file": "c_reply_interim.json"}})
A("A10 중간 회신 반영", "await W(1200);const t=dlg();clickBtn('닫기');const w=wf();const st=Object.values(w.collab.steps).find(s=>s.assignee==='이수진');return 'dlg='+t+' | status='+st.status+' interim='+JSON.stringify(st.interim||null)+' | '+sum()")
A("A11 ⏳ 줄 누름 → 메뉴 → 회수하고 직접 처리", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const w=wf();app.focusWorkflow(w.id);await W(800);const sid=Object.keys(w.collab.steps).find(k=>w.collab.steps[k].assignee==='이수진');const run=[...document.querySelectorAll('.cb-run')].find(r=>(r.getAttribute('onclick')||'').includes(sid));if(!run)return 'cb-run 없음';run.click();await W(400);const menu=[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>x.textContent.trim());[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].find(x=>x.textContent.includes('회수하고'))?.click();await W(500);const msg=[...document.querySelectorAll('.modal.show')].pop()?.innerText.replace(/\s+/g,' ').slice(0,300);clickBtn('회수하고 직접 처리');await W(1200);app.toggleStageCollapse&&0;const st4=[...document.querySelectorAll('.checklist-card')].find(c=>c.textContent.includes('종결 보고'));const tag=[...document.querySelectorAll('.cl-from-tag')].map(x=>x.textContent).concat(['data:'+(w.checklist[9].collabFrom||'없음'),'보임:'+!!st4]);return 'menu='+menu.join(',')+' | msg='+msg+' | tag='+tag.join(',')+' | '+sum()")
S.append({"b": "A", "shot": "c_A_recalled.png"})
A("A11b 종결 단계 펼쳐서 표시 확인", "const w=wf();const html=app.renderChecklistItem(w,w.checklist[9],9);const card=[...document.querySelectorAll('.checklist-card')].find(c=>c.querySelector('.item-title-text')?.textContent.trim().startsWith('종결')&&!app._isSubEntry(w.checklist[+c.dataset.index]));const h=card&&card.querySelector('.checklist-card-header');if(h&&h.querySelector('.cl-col-dots, [onclick*=toggleStage], .stage-toggle'))h.querySelector('.cl-col-dots, [onclick*=toggleStage], .stage-toggle').click();await W(600);const vis=[...document.querySelectorAll('.cl-from-tag')].map(x=>x.textContent);const panel=(document.querySelector('.proc-step-title')?.closest('div[id], section, aside')||document.body).innerText;return 'render에 표시='+html.includes('cl-from-tag')+' | 화면='+vis.join(',')+' | 오른쪽 패널에 회신 대기 남음='+/이수진 · 회신 대기/.test(document.body.innerText)")
S.append({"b": "A", "shot": "c_A_fromtag.png"})
C("C4 회수된 줄 모르고 최종 회신", "const w=wf();app.toggleChecklistItem(w.id,9);await W(1200);app.openCollabReplyModal(w.id);await W(700);document.querySelector('input[name=rpKind][value=final]').click();[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='회신 파일 만들기').click();await W(2500);return 'saved='+(window.__saved.at(-1)?.name||'없음')")
S.append({"b": "C", "saveTo": "c_reply_final.json"})
S.append({"b": "A", "setFile": {"sel": "#templateFileInput", "file": "c_reply_final.json"}})
A("A12 회수 뒤 늦게 온 회신 (거절되어야)", "await W(1000);const t=dlg();clickBtn('확인');return 'dlg='+t+' | '+sum()")
A("A13 회수한 할 일을 관리자가 직접 체크", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const w=wf();app.focusWorkflow(w.id);await W(800);app.toggleChecklistItem(w.id,7);await W(400);app.toggleChecklistItem(w.id,9);await W(1500);return sum()+' | 완료 처리 버튼='+!!document.querySelector('[onclick*=markWorkflowDone]')")
S.append({"b": "A", "shot": "c_A_final.png"})

A("D1 3단계를 김민수에게 임시 지정(보내기 전)", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const w=wf();for(const i of [7,9])if(app.normalizeCompleted(w.checklist[i]))app.toggleChecklistItem(w.id,i);await W(600);app.collabSetStep(w.id,w.checklist[6].itemId,'assignee','김민수');document.getElementById('collabModal')?.remove();await W(300);app.focusWorkflow(w.id);await W(800);return sum()")
A("D2 보내기 전 단계의 할 일을 체크 → 자동 취소 + 되돌리기", "window.__tm=[];const o=app.showToast.bind(app);app.showToast=(a,b,c,d,e)=>{window.__tm.push(c+(e&&e.actionLabel?' ['+e.actionLabel+']':''));return o(a,b,c,d,e)};const w=wf();app.toggleChecklistItem(w.id,7);await W(900);return 'toast='+window.__tm.join(' / ')+' | '+sum()")
S.append({"b": "A", "shot": "c_A_draftcancel.png"})
A("D3 [되돌리기] 누름", "const b=document.querySelector('#toast .toast-undo-btn');if(!b)return '되돌리기 버튼 없음';b.click();await W(900);return sum()")
A("D4 ⏳(보내기 전) 줄 메뉴 → 맡기기 취소 → 되돌리기", "const w=wf();app.focusWorkflow(w.id);await W(700);const sid=w.checklist[6].itemId;const run=[...document.querySelectorAll('.cb-run')].find(r=>(r.getAttribute('onclick')||'').includes(sid));if(!run)return 'cb-run 없음 | '+sum();run.click();await W(400);const menu=[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>x.textContent.trim());[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].find(x=>x.textContent.includes('맡기기 취소')).click();await W(700);const mid=sum();document.querySelector('#toast .toast-undo-btn')?.click();await W(700);return 'menu='+menu.join(',')+' | 취소 후='+mid+' | 되돌린 후='+sum()")

json.dump(S, open('steps_collab.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
