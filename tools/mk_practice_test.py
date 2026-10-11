# 연습 업무 넣기: 새 업무 만들기 ▾ → 연습 업무 넣기(실제 클릭) → 업무 2개·마감일이 오늘 기준·업무팁·서식·예시 그림·참고 자료·건너뛰기 버튼 확인
# → 건너뛰기 버튼 [1인 견적(2천만원 이하)]·[5천만원 이하]를 실제로 눌러 진행 → 가져오기용 .json도 [업무 가져오기]로 열어 봄 → steps3.json
# 실행: (tools 폴더에서) python mk_practice_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const PR=()=>app.allData.workflows.filter(w=>w.isPractice&&!w.isDeleted);"
     "const buy=()=>PR().find(w=>w.title.includes('소모품'));const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};"
     "const ix=(w,t)=>w.checklist.findIndex(i=>i.text===t);")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
def click(sel_js): pt("const b=" + sel_js + ";if(!b)throw new Error('단추 없음');b.scrollIntoView({block:'center'});await W(200);const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])"); S.append({"clickpt": 1, "wait": 300})

step("seed", "window.confirm=()=>true;localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "app.allData.workflows.filter(w=>w.isPractice).forEach(w=>w.isDeleted=true);app.saveData();app.displayWorkflows();await W(400);return 'ok'")
click("document.querySelector('.sidebar-newwork-more')")
click("[...document.querySelectorAll('#newWorkMenu .mi')].find(x=>x.textContent.includes('연습 업무 넣기'))")
step("A 연습 업무 넣기 (실제 클릭)", "await W(3500);const t=[...document.querySelectorAll('.toast')].map(x=>x.textContent.replace(/\\s+/g,' ')).join(' / ');return '연습 업무='+PR().map(w=>w.title).join(' , ')+' | 알림='+t.slice(0,120)")
S.append({"shot": "pr_a_main.png"})
step("B 마감일은 오늘 기준", "const w=buy();const r=w.checklist[ix(w,'구매 요청 받기 — 품목·수량·규격 확인')];const rep=PR().find(x=>x.title.includes('월간'));"
     "return '첫 할 일 마감='+r.deadline+' (오늘+3='+D(3)+') 같음='+(r.deadline===D(3))+' | 업무 마감 같음='+(w.deadline===D(55))+' | 월간 보고 마감 같음='+(rep.deadline===D(4))+' 끝낸 줄='+rep.checklist.filter(i=>i.completed).length")
step("C 업무팁·서식·예시·참고 자료", "const w=buy();const tips=w.checklist.filter(i=>i.tip&&i.tip.content).length;const fm=w.checklist.filter(i=>(i.linkedDocs||[]).length).map(i=>i.text);"
     "const tk=Object.keys(app.checklistDetails).filter(k=>k.startsWith(w.id+'-t-')).map(k=>(app.checklistDetails[k].attachments||[]).map(a=>a.name).join()).filter(Boolean);"
     "const refs=(app.checklistDetails['project-'+w.id]?.linkedLibraryDocs||[]).length;await app._loadRepoDocMetaCache?.();"
     "return '업무팁 줄='+tips+'/'+w.checklist.length+' | 서식 붙은 줄='+fm.join(', ')+' | 예시='+tk.join()+' | 참고 자료='+refs+' | 건너뛰기 단추='+w.checklist.filter(i=>i.branchOptions).map(i=>i.branchOptions.length).join('+')")
step("D 업무 열기", "app.focusWorkflow(buy().id);await W(1500);return '열림='+app.focusMode")
S.append({"shot": "pr_d_focus.png"})
step("E 01 단계 할 일 4개 체크(예정가격 작성은 해당 없음으로)", "const w=buy();for(const t of ['구매 요청 받기 — 품목·수량·규격 확인','추정가격 정하기','거래실례가격 조사 (2곳 이상)']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}"
     "app.markNotApplicable(w.id,[ix(w,'예정가격 작성')],'1인 견적 소액 수의계약');await W(1500);return '01 끝남='+w.checklist[0].completed+' | 지금 단계 펼침='+!!document.querySelector('.branch-run-btn')")
S.append({"shot": "pr_e_branch.png"})
click("[...document.querySelectorAll('.branch-run-btn')].find(b=>b.textContent.trim().endsWith('1인 견적'))")
step("F 건너뛰기 [1인 견적] 누르면 미리 보기", "await W(500);const m=document.getElementById('branchPreviewConfirmBtn');return '확인 창='+!!m+' | 내용='+(m?m.closest('.modal,div[id]').textContent.replace(/\\s+/g,' ').slice(0,140):'')")
click("document.getElementById('branchPreviewConfirmBtn')")
step("G 실행 → 2인 이상 견적 줄은 건너뜀", "await W(1200);const w=buy();const s=w.checklist[ix(w,'나라장터 수의계약 안내공고 (2인 이상 견적)')];return '건너뜀='+!!s.skipped+' 사유='+s.skipReason+' | 1인 견적 줄 남음='+!w.checklist[ix(w,'1인 견적서 받기')].skipped")
step("H 02 나머지 체크 → 03 단계로", "const w=buy();for(const t of ['1인 견적서 받기','수의계약 근거서류 갖추기']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}return '02 끝남='+w.checklist[ix(w,'계약 방법 정하기')].completed")
step("I 03 앞 할 일 3개 체크", "const w=buy();for(const t of ['배제사유 확인 · 각서 받기','수의계약 체결 제한 대상인지 확인','청렴서약서 받기']){app.toggleChecklistItem(w.id,ix(w,t));await W(1300);}return 'ok'")
click("[...document.querySelectorAll('.branch-run-btn')].find(b=>b.textContent.includes('5천만원 이하'))")
click("document.getElementById('branchPreviewConfirmBtn')")
step("J [5천만원 이하] → 계약서·보증금 건너뜀", "await W(1200);const w=buy();return ['계약서 작성','계약보증금 받기 (계약금액의 10% 이상)','청구서·각서 등 증거서류 받기 (계약서 생략 시)'].map(t=>t.slice(0,8)+'='+(w.checklist[ix(w,t)].skipped?'건너뜀':'남음')).join(' ')")
S.append({"shot": "pr_j_panel.png"})
step("K 업무 절차 패널: 건너뛴 줄 알약", "const pills=[...document.querySelectorAll('#aiPanelOfflineDashboard .proc-skip-pill')].map(p=>p.textContent.trim());return '알약='+pills.join(', ')+' | 진행 줄='+(document.querySelector('#procProg .proc-prog-text')?.textContent||'')")
step("K2 진행상황 출력(체크리스트): 직접 뺀 줄은 「해당 없음」, 건너뛰기 버튼은 「건너뜀」 + 「⤼ 버튼 이름」", "const w=buy();app._collabSetMe({dept:'사하소방서 행정과',rank:'소방위',name:'홍길동',phone:'4521'});localStorage.setItem('progressReportOpts',JSON.stringify({clResult:true,clSkipped:true}));app.openProgressReport(w.id);await W(1300);"
     "const rows=[...document.querySelectorAll('#prPage tr')].map(r=>[...r.cells].map(c=>c.textContent.trim()));const f=t=>rows.find(r=>r[0]&&r[0].replace(/^○\\s*/,'')===t)||[];"
     "const na=f('예정가격 작성'),sk=f('나라장터 수의계약 안내공고 (2인 이상 견적)'),sk2=f('계약서 작성');app.closeProgressReport();await W(300);"
     "return '예정가격(직접 뺌)='+na.slice(1).join('|')+' || 나라장터(건너뛰기)='+sk.slice(1).join('|')+' || 계약서='+sk2.slice(1).join('|')")
S.append({"shot": "pr_k2_report.png"})
step("L e호조 예시 그림 미리보기", "const w=buy();app.previewTipFile(w.id,ix(w,'지출 처리 (e호조)'),0);await W(1500);const im=[...document.querySelectorAll('.pv-win #previewContent img')].pop();return '그림='+(im?im.naturalWidth+'x'+im.naturalHeight:'없음')")
S.append({"shot": "pr_l_flow.png"})
step("M 닫기", "document.querySelectorAll('.pv-modal').forEach(m=>m.querySelector('.close-preview-modal')?.click());await W(400);app.exitFocusMode();await W(500);return 'ok'")
step("N 가져오기용 .json을 [업무 가져오기]로 (복사하여 시작)", "const before=app.allData.workflows.length;const txt=await (await fetch('./'+encodeURIComponent('사용설명서')+'/'+encodeURIComponent('연습업무.json'))).text();"
     "app._restoreFromFile([new File([txt],'연습업무.json',{type:'application/json'})]);await W(1200);const m=document.getElementById('packageImportChoiceModal');const r='고르는 창='+!!m;"
     "document.querySelector('input[name=pkgImportMode][value=new]').click();await W(100);app._confirmPackageImport();await W(4000);const nw=app.allData.workflows.slice(0).filter(w=>w.title.startsWith('[연습]')&&!w.isPractice&&!w.isDeleted);"
     "return r+' | 들어온 업무='+nw.length+' | 체크 비움='+nw.every(w=>w.checklist.every(i=>!i.completed))+' | 건너뛰기 단추 그대로='+nw.some(w=>w.checklist.some(i=>i.branchOptions))")
step("O 연습 업무를 한 번 더 넣으면 묻지 않고 (2)", "window.__cm=[];window.confirm=m=>{window.__cm.push(m);return true;};await app.insertPracticeWorkflows();await W(2500);const t=PR().map(w=>w.title).filter(x=>x.endsWith('(2)'));const libs=(await app._getAllLibraryFiles()).filter(f=>f.name.startsWith('지방계약법')).length;return '(2) 붙은 업무='+t.length+' | 물어본 것='+window.__cm.length+' | 법령 파일 겹침 없음='+(libs===2)")
step("정리", "app.allData.workflows.filter(w=>w.title.startsWith('[연습]')).forEach(w=>{w.isDeleted=true;});app.saveData();app.displayWorkflows();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
