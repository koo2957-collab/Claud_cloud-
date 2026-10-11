# 실제로 쓰는 흐름 전체 시험 (브라우저 3개: A=관리자 홍길동, B=담당자 김민수, C=담당자 이수진) → steps_flow.json
# 흐름 1: 연습 업무 넣기 → 진행·건너뛰기 → 업무 분담(주소록에 새 사람 추가·단계 나누기·전달사항) → 요청 파일
#         → 담당자 둘이 받아 처리(체크·처리결과·첨부) → 중간·최종 회신 → 관리자가 [파일 고르기]·끌어다 놓기·[업무 가져오기]로 합침
#         → 남은 단계 끝 → 진행상황 출력(체크리스트) → 완료 처리 → 레퍼런스 등록 → 복사하여 시작
# 흐름 2: 관리자의 업무를 [내보내기] → 담당자 B가 [업무 가져오기](그대로) → B가 관리자가 되어 C에게 나눔 → 회신 합치기 → 출력
# 흐름 3: [공유] 창에서 업무 2개 골라 [업무 파일 만들기] → C가 [업무 가져오기]
# 실행: (tools 폴더에서) python mk_flow_test.py && node collab2.mjs <index.html 경로> steps_flow.json
import json, os

def J(body): return ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
                     "const byT=t=>app.allData.workflows.filter(w=>!w.isDeleted&&w.title.includes(t)).sort((a,b)=>String(b.createdAt).localeCompare(String(a.createdAt)))[0];"
                     "const ix=(w,t)=>w.checklist.findIndex(i=>i.text===t);"
                     "const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};"
                     "const dlg=()=>[...document.querySelectorAll('.modal.show')].map(m=>(m.querySelector('h2,h3,.modal-title,.cd-title')?.textContent||'').trim()+' :: '+[...m.querySelectorAll('button')].map(b=>b.textContent.trim()).filter(Boolean).join('/')).join(' || ');"
                     "const clickBtn=t=>{const b=[...document.querySelectorAll('.modal.show button, #collabPickModal button')].reverse().find(b=>b.textContent.trim().startsWith(t));if(!b)return false;b.click();return true;};"
                     "const closeAll=()=>document.querySelectorAll('.modal.show').forEach(m=>{m.classList.remove('show');});"
                     "const steps=w=>Object.entries((w.collab||{}).steps||{}).map(([sid,s])=>{const it=w.checklist.find(x=>x.itemId===sid);return (it?it.text:sid)+'→'+s.assignee+'/'+s.status}).join(', ');"
                     "const done=w=>w.checklist.filter(i=>app.normalizeCompleted(i)).length+'/'+w.checklist.length+' (건너뜀 '+w.checklist.filter(i=>i.skipped).length+')';"
                     "const toast=()=>[...document.querySelectorAll('.toast')].map(t=>t.textContent.replace(/\\s+/g,' ').trim()).pop()||'';"
                     + body + "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()")
S = []
def A(label, body): S.append({"b": "A", "label": label, "js": J(body)})
def B(label, body): S.append({"b": "B", "label": label, "js": J(body)})
def C(label, body): S.append({"b": "C", "label": label, "js": J(body)})
setup = ("window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');closeAll();")
BUY = "byT('[연습] 소모품 구매')"
# 담당자가 맡은 할 일을 체크하고 처리결과·첨부를 남기는 도우미
WORK = ("const work=async(w,t,txt,file)=>{const i=ix(w,t);if(txt||file){await app.showChecklistItemModal(w.id,i,'result');await W(600);const rt=document.getElementById('main-checklist-result-text-'+w.id+'-'+i);"
        "if(rt&&txt){rt.value=txt;rt.dispatchEvent(new Event('input',{bubbles:true}));await W(900);}if(file){const sh=document.getElementById('rf-shrink-'+w.id+'-'+i);if(sh)sh.checked=false;await app.addResultFiles(w.id,i,{files:[new File(['%PDF-1.4 '+'0'.repeat(9000)],file,{type:'application/pdf'})],value:''});await W(900);}"
        "app.closeChecklistItemModal();await W(400);}if(!app.normalizeCompleted(w.checklist[i])){app.toggleChecklistItem(w.id,i);await W(1300);}};")
REPLY = ("const reply=async(w,kind)=>{app.openCollabReplyModal(w.id);await W(700);document.querySelector('input[name=rpKind][value='+kind+']').click();await W(200);"
         "[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='회신 파일 만들기').click();await W(2500);return window.__saved.at(-1)?.name||'없음';};")
PICK = ("const pick=async n=>{const r=[...document.querySelectorAll('input[name=cbPickName]')].find(r=>r.value===n);if(!r)return '이름 없음: '+dlg();r.checked=true;clickBtn('선택');await W(500);clickBtn('네, '+n);await W(2500);"
        "clickBtn('확인')||clickBtn('시작')||clickBtn('닫기');closeAll();await W(300);return 'ok';};")

# ───────── 흐름 1 ─────────
A("1-1 관리자 준비 · 연습 업무 넣기", setup + "app._collabSavePeople([{name:'김민수',dept:'사하소방서 행정과',rank:'소방장'}]);app._collabSetMe({dept:'사하소방서 행정과',rank:'소방위',name:'홍길동',phone:'4521'});app._collabSetMyName('홍길동');"
  "await app.insertPracticeWorkflows();await W(2500);const w=" + BUY + ";app.focusWorkflow(w.id);await W(1200);return '업무='+w.title+' | '+done(w)")
A("1-2 01 단계 진행 + 해당 없음 + 건너뛰기 [1인 견적]", "const w=" + BUY + ";for(const t of ['구매 요청 받기 — 품목·수량·규격 확인','추정가격 정하기','거래실례가격 조사 (2곳 이상)']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}"
  "app.markNotApplicable(w.id,[ix(w,'예정가격 작성')],'1인 견적 소액 수의계약');await W(1500);const bi=ix(w,'금액 기준 확인 — 갈림길');const oi=w.checklist[bi].branchOptions.findIndex(o=>o.label==='1인 견적');"
  "app.handleBranchOption(w.id,bi,oi);await W(500);document.getElementById('branchPreviewConfirmBtn').click();await W(1500);return done(w)+' | 2인 견적 건너뜀='+!!w.checklist[ix(w,'나라장터 수의계약 안내공고 (2인 이상 견적)')].skipped")
A("1-3 업무 분담 열기 → 주소록에서 추가 → 새 사람(이수진) 넣기", "const w=" + BUY + ";app.openCollabModal(w.id,'send');await W(800);[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('주소록에서 추가')).click();await W(700);"
  "app._abEditPerson(null);await W(400);const f=(id,v)=>{const e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));};f('abFName','이수진');f('abFDept','사하소방서 행정과');f('abFRank','소방교');app._abSavePerson();await W(600);"
  "const auto=app._ab.picked.includes('이수진');for(const n of ['김민수','이수진']){if(app._ab.picked.includes(n))continue;const p=[...document.querySelectorAll('#abModal .ab-person')].find(p=>p.querySelector('.ab-p-name').textContent===n);if(!p)return '주소록에 '+n+' 없음';p.click();await W(250);}app._abConfirm();await W(800);"
  "return '새로 넣은 사람 저절로 골라짐='+auto+' | 이 업무에 함께 일할 사람='+app._collabTeam(byT('[연습] 소모품 구매')).join(', ')")
A("1-4 단계 나누기(04 납품·검사→김민수, 05 대가 지급→이수진) · 회신 기한 · 전달사항", "const w=" + BUY + ";const sid=t=>w.checklist[ix(w,t)].itemId;"
  "const sel=s=>[...document.querySelectorAll('#collabModal select')].find(x=>(x.getAttribute('onchange')||'').includes(`'${s}','assignee'`));"
  "for(const [t,n] of [['납품·검사','김민수'],['대가 지급','이수진']]){const e=sel(sid(t));if(!e)return '고르는 칸 없음: '+t;e.value=n;e.dispatchEvent(new Event('change',{bubbles:true}));await W(500);}"
  "const dl=[...document.querySelectorAll('#collabModal input[type=date]')].find(x=>(x.getAttribute('onchange')||'').includes(`'${sid('납품·검사')}','deadline'`));if(dl){dl.value=D(5);dl.dispatchEvent(new Event('change',{bubbles:true}));}await W(300);"
  "const m=document.getElementById('cbReqMemo');if(m){m.value='○○상사 납품 예정 10.20.(화) — 업체 참관 아래 검사해 주세요';m.dispatchEvent(new Event('input',{bubbles:true}));}await W(300);return steps(w)")
S.append({"b": "A", "shot": "fl_1_assign.png"})
A("1-5 [요청 파일 만들기]", "const w=" + BUY + ";[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('요청 파일 만들기')).click();await W(2800);return '파일='+(window.__saved.at(-1)?.name||'없음')+' | '+steps(w)")
S.append({"b": "A", "saveTo": "fl_request.json"})
A("1-5b 업무 분담 창 닫기", "app.closeCollabModal&&app.closeCollabModal(true);document.getElementById('collabModal')?.remove();closeAll();await W(300);return 'ok'")

B("1-6 김민수 PC: 요청 파일 열기 → 김민수", setup + PICK + "return 'pick'")
S.append({"b": "B", "setFile": {"sel": "#templateFileInput", "file": "fl_request.json"}})
B("1-6b 이름 고르기", PICK + "const r=await pick('김민수');const w=" + BUY + ";return r+' | 업무='+(w?w.title:'없음')+' | 전달사항='+(w&&JSON.stringify(Object.values(w.collab.steps).map(s=>s.memo)))")
B("1-7 맡지 않은 단계는 잠김", "const w=" + BUY + ";window.__t=[];const o=app.showToast.bind(app);app.showToast=(a,b,c,...r)=>{window.__t.push(c);return o(a,b,c,...r)};const i=ix(w,'대금청구서 · 세금계산서 받기');app.toggleChecklistItem(w.id,i);await W(600);clickBtn('확인');app.showToast=o;return '체크됨='+app.normalizeCompleted(w.checklist[i])+' | 알림='+window.__t.join(' / ').slice(0,90)")
B("1-8 맡은 04 단계 처리(체크·처리결과·첨부) → 최종 회신", WORK + REPLY + "const w=" + BUY + ";app.focusWorkflow(w.id);await W(900);"
  "await work(w,'납품 완료 통지 받기 (서면)','10.20.(화) ○○상사 납품 완료 통지서 접수');await work(w,'납품 검사 (업체 참관)','10.21.(수) 수량 2,000개·포장 이상 없음 (업체 참관)','납품검사 사진.pdf');"
  "app.markNotApplicable(w.id,[ix(w,'검사조서 작성')],'계약금액 3천만원 이하');await W(1200);await work(w,'검사 결과 서면 통지','10.21.(수) 검사 결과 통지');"
  "const f=await reply(w,'final');return '04 끝남='+w.checklist[ix(w,'납품·검사')].completed+' | 회신 파일='+f")
S.append({"b": "B", "saveTo": "fl_reply_B.json"})

C("1-9 이수진 PC: 요청 파일 열기 → 이수진", setup + "return 'ok'")
S.append({"b": "C", "setFile": {"sel": "#templateFileInput", "file": "fl_request.json"}})
C("1-9b 이름 고르기 · 일부 처리 → 중간 회신", PICK + WORK + REPLY + "await pick('이수진');const w=" + BUY + ";app.focusWorkflow(w.id);await W(900);"
  "await work(w,'대금청구서 · 세금계산서 받기','10.22.(목) 청구서·세금계산서 접수','세금계산서.pdf');const f=await reply(w,'interim');return '중간 회신='+f+' | '+done(w)")
S.append({"b": "C", "saveTo": "fl_reply_C1.json"})

A("1-10 [회신 현황] → [파일 고르기]로 김민수 회신", "const w=" + BUY + ";app.focusWorkflow(w.id);await W(800);app.openCollabModal(w.id,'status');await W(900);return '놓는 칸='+!!document.getElementById('cbDropZone')")
S.append({"b": "A", "choose": "fl_reply_B.json", "label": "1-10b 파일 고르기 누름", "js": J("document.getElementById('cbDropZone').click();return 'clicked'")})
A("1-10c 반영 결과", "await W(1500);const t=dlg();clickBtn('닫기')||clickBtn('확인');const w=" + BUY + ";const files=app._collabResultFiles(w.id,w.checklist[ix(w,'납품 검사 (업체 참관)')].itemId).map(f=>f.name);return '창='+t.slice(0,120)+' | 04 끝남='+w.checklist[ix(w,'납품·검사')].completed+' | 첨부='+files.join(',')+' | '+steps(w)")
S.append({"b": "A", "shot": "fl_1_merged_B.png"})
A("1-11 이수진 중간 회신을 [회신 현황]에 끌어다 놓기", "closeAll();const w=" + BUY + ";app.openCollabModal(w.id,'status');await W(900);const txt=await (await fetch('./tools/fl_reply_C1.json')).text();const dt=new DataTransfer();dt.items.add(new File([txt],'[회신] 소모품 구매_이수진.json',{type:'application/json'}));"
  "const body=document.getElementById('collabModalBody');body.dispatchEvent(new DragEvent('dragover',{bubbles:true,cancelable:true,dataTransfer:dt}));await W(200);const over=body.classList.contains('cb-drop');body.dispatchEvent(new DragEvent('drop',{bubbles:true,cancelable:true,dataTransfer:dt}));await W(1800);"
  "const t=dlg();clickBtn('닫기')||clickBtn('확인');const st=Object.values(w.collab.steps).find(s=>s.assignee==='이수진');return '끌 때 표시='+over+' | 창='+t.slice(0,100)+' | 이수진='+st.status+' 중간='+!!st.interim+' | 청구서 줄 체크='+app.normalizeCompleted(w.checklist[ix(w,'대금청구서 · 세금계산서 받기')])")

C("1-12 이수진 나머지 처리 → 최종 회신", WORK + REPLY + "const w=" + BUY + ";await work(w,'지출 처리 (e호조)','10.23.(금) 지출결의·결재 완료');await work(w,'대가 지급 (청구일부터 5일 안)','10.26.(월) 지급 완료 (청구일부터 2일)');const f=await reply(w,'final');return '최종 회신='+f+' | '+done(w)")
S.append({"b": "C", "saveTo": "fl_reply_C2.json"})
A("1-13 최종 회신은 [업무 가져오기]로", "app.closeCollabModal&&app.closeCollabModal(true);document.getElementById('collabModal')?.remove();closeAll();await W(300);return 'ok'")
S.append({"b": "A", "setFile": {"sel": "#templateFileInput", "file": "fl_reply_C2.json"}})
A("1-13b 반영 결과", "await W(1500);const t=dlg();clickBtn('닫기')||clickBtn('확인');const w=" + BUY + ";return '창='+t.slice(0,100)+' | 05 끝남='+w.checklist[ix(w,'대가 지급')].completed+' | '+steps(w)+' | '+done(w)")
A("1-14 남은 02·03·06 끝내기 (03은 [5천만원 이하])", "closeAll();const w=" + BUY + ";app.focusWorkflow(w.id);await W(900);for(const t of ['1인 견적서 받기','수의계약 근거서류 갖추기','배제사유 확인 · 각서 받기','수의계약 체결 제한 대상인지 확인','청렴서약서 받기']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}"
  "const bi=ix(w,'계약금액 확인 — 갈림길');app.handleBranchOption(w.id,bi,w.checklist[bi].branchOptions.findIndex(o=>o.label==='5천만원 이하'));await W(500);document.getElementById('branchPreviewConfirmBtn').click();await W(1500);"
  "for(const t of ['청구서·각서 등 증거서류 받기 (계약서 생략 시)','수의계약 내역 공개','진행상황 출력 — 체크리스트 보관','레퍼런스로 등록']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}return done(w)+' | 모든 단계 끝='+w.checklist.filter(i=>!i.indent).every(i=>i.completed||i.skipped)")
S.append({"b": "A", "shot": "fl_1_alldone.png"})
A("1-15 진행상황 출력 → 체크리스트 표", "const w=" + BUY + ";app.openProgressReport(w.id);await W(1200);const M=document.getElementById('progressReportModal');const tab=M.querySelector('.pr-tabs .on')?.textContent;const rows=[...document.querySelectorAll('#prPage tr')].length;const txt=document.getElementById('prPage').innerText;"
  "return '탭='+tab+' | 표 줄='+rows+' | 처리결과 보임='+txt.includes('수량 2,000개')+' | 회신자 결과(이수진) 보임='+txt.includes('지급 완료')+' | 해당 없음 표시='+/해당 없음/.test(txt)+' | 쪽='+document.querySelectorAll('#prPage .pr-pg').length")
S.append({"b": "A", "shot": "fl_1_report.png"})
A("1-16 완료 처리 → 레퍼런스 등록 → 복사하여 시작", "app.closeProgressReport();await W(300);const w=" + BUY + ";app.markWorkflowDone(w.id);await W(900);const t1=toast();app.setReference(w.id,true);await W(700);const rm=document.getElementById('refRegisterModal');const refName=rm?.querySelector('#refRegisterTitle').value;rm?.querySelector('[data-act=ok]').click();await W(1800);closeAll();"
  "const refs=app.allData.workflows.filter(x=>!x.isDeleted&&x.isReference&&x.title.includes('[연습] 소모품 구매'));const ref=refs[0];const refClean=ref&&ref.checklist.every(i=>!app.normalizeCompleted(i));"
  "const before=app.allData.workflows.length;if(ref){app.duplicateWorkflowFromManager(ref.id);await W(800);const dl=document.getElementById('duplicateDeadlineInput');if(dl)dl.value=D(30);app.executeDuplicateWorkflow(ref.id);await W(2000);}closeAll();const nw=app.allData.workflows.length>before?app.allData.workflows.find(x=>!x.isReference&&!x.completedProcessed&&x.title.includes('[연습] 소모품 구매')&&x.id!==w.id):null;"
  "return '레퍼런스 이름='+refName+' | 완료 알림='+t1.slice(0,40)+' | 원래 업무 처리완료='+!!w.completedProcessed+' 기록 남음='+w.checklist.some(i=>i.result&&i.result.text)+' | 레퍼런스='+refs.length+' 체크 비움='+refClean+' | 복사하여 시작='+(nw?nw.title+' 체크0='+nw.checklist.every(i=>!app.normalizeCompleted(i))+' 업무팁='+nw.checklist.filter(i=>i.tip).length:'없음')")

# ───────── 흐름 2: 내보내기 → 다른 PC에서 가져와 나누기 ─────────
A("2-1 월간 보고 업무 [내보내기]", "closeAll();const w=byT('[연습] 월간 업무 실적 보고');app.focusWorkflow(w.id);await W(900);const b=[...document.querySelectorAll('button, .fap-btn')].find(x=>x.textContent.trim()==='내보내기'&&x.offsetParent);b.click();await W(2500);return '파일='+(window.__saved.at(-1)?.name||'없음')")
S.append({"b": "A", "saveTo": "fl_export.json"})
B("2-2 김민수 PC: [업무 가져오기] → 그대로 가져오기", "closeAll();return 'ok'")
S.append({"b": "B", "setFile": {"sel": "#templateFileInput", "file": "fl_export.json"}})
B("2-2b 가져오는 방식", "await W(800);const t=dlg();document.querySelector('input[name=pkgImportMode][value=asIs]').click();await W(100);app._confirmPackageImport();await W(2500);const w=byT('[연습] 월간 업무 실적 보고');return '창='+t.slice(0,60)+' | 가져옴='+(w?w.title:'없음')+' | '+(w?done(w):'')")
B("2-3 김민수가 관리자로 「보고서 작성」 단계를 이수진에게 나눔", "app._collabSavePeople([{name:'이수진',dept:'사하소방서 행정과',rank:'소방교'}]);app._collabSetMe({dept:'사하소방서 행정과',rank:'소방장',name:'김민수'});app._collabSetMyName('김민수');const w=byT('[연습] 월간 업무 실적 보고');"
  "app.openCollabModal(w.id,'send');await W(800);[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('주소록에서 추가')).click();await W(700);[...document.querySelectorAll('#abModal .ab-person')].find(p=>p.querySelector('.ab-p-name').textContent==='이수진').click();await W(250);app._abConfirm();await W(800);const sid=w.checklist[ix(w,'보고서 작성')].itemId;const e=[...document.querySelectorAll('#collabModal select')].find(x=>(x.getAttribute('onchange')||'').includes(`'${sid}','assignee'`));if(!e)return '고르는 칸 없음 | '+dlg();e.value='이수진';e.dispatchEvent(new Event('change',{bubbles:true}));await W(500);"
  "[...document.querySelectorAll('#collabModal button')].find(b=>b.textContent.includes('요청 파일 만들기')).click();await W(2800);return '파일='+(window.__saved.at(-1)?.name||'없음')+' | '+steps(w)")
S.append({"b": "B", "saveTo": "fl2_request.json"})
C("2-4 이수진 PC: 요청 열기 → 처리 → 최종 회신", "closeAll();return 'ok'")
S.append({"b": "C", "setFile": {"sel": "#templateFileInput", "file": "fl2_request.json"}})
C("2-4b", PICK + WORK + REPLY + "await pick('이수진');const w=byT('[연습] 월간 업무 실적 보고');app.focusWorkflow(w.id);await W(900);await work(w,'표·그래프 정리','10월 실적 표 3개 정리','10월 실적표.pdf');const f=await reply(w,'final');return '회신='+f+' | '+done(w)")
S.append({"b": "C", "saveTo": "fl2_reply.json"})
B("2-5 김민수가 회신을 끌어다 놓아 합침", "app.closeCollabModal&&app.closeCollabModal(true);document.getElementById('collabModal')?.remove();closeAll();const w=byT('[연습] 월간 업무 실적 보고');app.openCollabModal(w.id,'status');await W(900);const txt=await (await fetch('./tools/fl2_reply.json')).text();const dt=new DataTransfer();dt.items.add(new File([txt],'회신.json',{type:'application/json'}));"
  "document.getElementById('collabModalBody').dispatchEvent(new DragEvent('drop',{bubbles:true,cancelable:true,dataTransfer:dt}));await W(1800);const t=dlg();clickBtn('닫기')||clickBtn('확인');return '창='+t.slice(0,80)+' | 보고서 작성 끝='+w.checklist[ix(w,'보고서 작성')].completed+' | '+steps(w)")
B("2-6 진행상황 출력", "app.closeCollabModal&&app.closeCollabModal(true);document.getElementById('collabModal')?.remove();closeAll();const w=byT('[연습] 월간 업무 실적 보고');app.openProgressReport(w.id);await W(1200);const txt=document.getElementById('prPage').innerText;app.closeProgressReport();return '표 줄='+txt.split('\\n').length+' | 이수진 결과='+txt.includes('실적 표 3개')")

# ───────── 흐름 3: 공유 창 ─────────
A("3-1 [공유] 창에서 2개 골라 [업무 파일 만들기]", "closeAll();app.exitFocusMode?.();await W(400);app.showShareModal();await W(800);const rows=[...document.querySelectorAll('.share-modal tbody tr')];const pick=rows.filter(r=>/\\[연습\\]/.test(r.textContent)).slice(0,2);for(const r of pick){r.querySelector('input[type=checkbox]')?.click();await W(150);}"
  "const sel=app._sh.sel.size;document.getElementById('shareGoBtn').click();await W(3000);return '고른 수='+sel+' | 파일='+(window.__saved.at(-1)?.name||'없음')+' | 알림='+toast().slice(0,60)")
S.append({"b": "A", "saveTo": "fl_share.json"})
C("3-2 이수진 PC: [업무 가져오기] → 복사하여 시작", "closeAll();return 'ok'")
S.append({"b": "C", "setFile": {"sel": "#templateFileInput", "file": "fl_share.json"}})
C("3-2b", "await W(800);document.querySelector('input[name=pkgImportMode][value=new]').click();await W(100);app._confirmPackageImport();await W(3000);closeAll();return '업무 수='+app.allData.workflows.filter(w=>!w.isDeleted).length+' | 제목='+app.allData.workflows.filter(w=>!w.isDeleted).map(w=>w.title.slice(0,16)).join(' / ')")

json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps_flow.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('steps_flow.json', len(S))
