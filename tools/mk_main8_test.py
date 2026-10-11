import json, sys
# 메인 화면 8가지 시험 → steps3.json  (쓰는 법: python mk_main8_test.py [1366x768])
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wfOf=id=>app.allData.workflows.find(w=>w.id===id);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
if len(sys.argv) > 1: S.append({'viewport': [int(v) for v in sys.argv[1].split('x')]})
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
mc = "const mc=document.querySelector('.main-content');"
first = "const firstT=()=>{const c=document.querySelector('.workflow-card .card-title-text, .wf-row .wf-row-title');return c?c.textContent.trim().slice(0,22):'-'};"

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};const ago=n=>new Date(Date.now()-n*864e5).toISOString();"
     "const T=[['감찰조사 — 근무지 무단이탈',3,3],['소방시설 자체점검 미실시 과태료 부과',-1,12],['소방장 품위유지의무 위반 징계처분',6,1],['물품 구매 계약(소방 장비 교체)',20,30],['구급대원 폭행 사건 내사(+수사) 처리 절차',2,5],['화재조사 보고서 작성',null,8],['민원 처리 — 소방차 전용구역 주차',1,0.5],['청렴 교육 계획 수립',40,60],['구조대 장비 점검표 정비',10,15],['위험물 안전관리자 선임 신고 확인',4,2],['안전문화 캠페인',null,100],['소방특별사법경찰 수사 서류 정리',null,90]];"
     "T.forEach(([t,dl,a],k)=>{const cl=[];for(let s=1;s<=4;s++)cl.push({text:'단계 '+s,indent:0,completed:k%4>=s,completedAt:k%4>=s?ago(a):null});app.allData.workflows.unshift({id:9100+k,type:'manual',title:t,checklist:cl,date:'2026. 10. 1.',createdAt:ago(a+5),lastProgressAt:ago(a),deadline:dl==null?undefined:D(dl),folderPath:''});});"
     # 방금 가져온 업무(옛 진행 기록) · 방금 복사한 업무(체크 없음)
     "app.allData.workflows.push({id:9200,type:'manual',title:'【가져옴】 다른 서 감찰 사례',checklist:[{text:'단계',indent:0,completed:true,completedAt:ago(200)}],date:'2026. 3. 1.',createdAt:'2026-03-01',lastProgressAt:ago(200),importedAt:new Date().toISOString(),folderPath:''});"
     "app.allData.workflows.push({id:9201,type:'manual',title:'【복사함】 징계처분 사본',checklist:[{text:'단계',indent:0,completed:false}],date:'2026. 10. 11.',createdAt:new Date(Date.now()-60000).toISOString(),folderPath:''});"
     "app.saveData();app.setViewMode('grid');app.displayWorkflows();await W(800);" + first + "return '처음 정렬='+app.currentSortMethod+' 칸 값='+document.getElementById('sortSelect').value+' | 맨 앞 카드='+firstT()")
S.append({"shot": "m8_grid.png"})
# ⑧ 고정
step("⑧ 카드형: 아래로 내려도 검색·정렬 줄 고정", mc + "mc.scrollTop=700;await W(400);const b=document.getElementById('controlBar').getBoundingClientRect(),m=mc.getBoundingClientRect();return '스크롤='+mc.scrollTop+' | 검색 줄 위치(상자 위 기준)='+Math.round(b.top-m.top)+' 높이='+Math.round(b.height)+' | 보임='+(b.top>=m.top-1)")
S.append({"shot": "m8_grid_scroll.png"})
# ③ 목록형
step("③ 목록형 모양", mc + "mc.scrollTop=0;app.setViewMode('list');await W(600);const r=document.querySelector('.wf-row');const cs=getComputedStyle(r);const h=document.querySelector('.wf-row-header');return '줄 테두리='+cs.borderTopWidth+'/'+cs.borderLeftWidth+' 아래선='+cs.borderBottomWidth+' 둥근 모서리='+cs.borderRadius+' | 색 점='+document.querySelectorAll('.wf-row .wf-dot').length+' | 제목 줄 정렬 표시='+[...h.querySelectorAll('[data-sort]')].map(x=>x.textContent.trim()).join(',')")
S.append({"shot": "m8_list.png"})
step("③⑧ 목록형: 내려도 제목 줄이 검색 줄 바로 아래", mc + "mc.scrollTop=500;await W(400);const b=document.getElementById('controlBar').getBoundingClientRect(),h=document.querySelector('.wf-row-header').getBoundingClientRect();return '검색 줄 아래='+Math.round(b.bottom)+' 제목 줄 위='+Math.round(h.top)+' 차이='+Math.round(h.top-b.bottom)+'px'")
S.append({"shot": "m8_list_scroll.png"})
pt(mc + "mc.scrollTop=0;await W(300);const x=document.querySelector('.wf-row-header [data-sort=title]').getBoundingClientRect();return JSON.stringify([x.left+15,x.top+x.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("③ 제목 줄 「제목」 실제로 누름 → 제목순·기억", first + "await W(500);return '정렬='+app.currentSortMethod+' 칸 값='+document.getElementById('sortSelect').value+' 저장='+localStorage.getItem('workflowSortMethod')+' | 맨 앞='+firstT()+' | 표시='+document.querySelector('.wf-row-header .on')?.textContent.trim()")
step("② 다시 켜기(새로 고침)", "setTimeout(()=>location.reload(),50);return 'reload'")
S.append({"wait": 5000})
step("② 다시 켠 뒤 정렬 기억", first + "await W(800);return '정렬='+app.currentSortMethod+' 칸 값='+document.getElementById('sortSelect').value+' | 맨 앞='+firstT()")
step("② 최근 진행순으로 바꾸면 방금 복사·가져온 업무가 맨 위", first + "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.sortWorkflows('recent');await W(500);const t=[...document.querySelectorAll('.wf-row .wf-row-title, .workflow-card .card-title-text')].slice(0,3).map(x=>x.textContent.trim().slice(0,14));return t.join(' / ')")
# ① 마감 알림
step("① 켤 때 마감 알림 → 가운데", "app.setViewMode('grid');await W(300);localStorage.setItem('deadlineNotifyMode','always');app.checkDeadlineNotifications({startup:true});await W(900);const b=document.getElementById('deadlineBanner');const r=b.getBoundingClientRect();const items=[...b.querySelectorAll('.cs-row')];const it=items[0]?.getBoundingClientRect();return '가운데='+b.classList.contains('center')+' 위치 '+Math.round(r.left+r.width/2)+','+Math.round(r.top+r.height/2)+' (창 가운데 '+innerWidth/2+','+innerHeight/2+') | 배경='+!!document.getElementById('dbBackdrop')+' | 줄 수='+items.length+' | 첫 줄 왼쪽 여백='+(it?Math.round(it.left-r.left):'-')+' 오른쪽 여백='+(it?Math.round(r.right-it.right):'-')+' | 닫기 버튼 보임='+!!b.querySelector('.db-dismiss').offsetParent")
S.append({"shot": "m8_banner.png"})
S.append({"key": "Escape", "vk": 27})
step("① Esc로 닫힘", "await W(300);return '보임='+document.getElementById('deadlineBanner').classList.contains('show')+' 배경='+!!document.getElementById('dbBackdrop')")
step("① 다른 창이 떠 있으면 닫힌 뒤에 뜸", "app.openModal('manualModal');await W(500);app.checkDeadlineNotifications({startup:true});await W(1200);const a=document.getElementById('deadlineBanner').classList.contains('show');app.closeModal?app.closeModal('manualModal'):document.getElementById('manualModal').classList.remove('show');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));await W(1500);const b=document.getElementById('deadlineBanner').classList.contains('show');app.hideDeadlineBanner();return '창 떠 있을 때 보임='+a+' → 닫은 뒤 보임='+b")
step("① 설정에서 바꿀 때는 오른쪽 아래(지금처럼)", "app.checkDeadlineNotifications();await W(800);const b=document.getElementById('deadlineBanner');const r=b.getBoundingClientRect();const res='가운데='+b.classList.contains('center')+' 오른쪽 여백='+Math.round(innerWidth-r.right)+' 아래 여백='+Math.round(innerHeight-r.bottom);app.hideDeadlineBanner();localStorage.setItem('deadlineNotifyMode','off');return res")
S.append({"shot": "m8_banner_corner.png"})
# ⑦ 새 업무 버튼
pt("const b=document.querySelector('.nw-split .sidebar-newwork-btn').getBoundingClientRect();window.__nwh=Math.round(b.height);return JSON.stringify([b.left+b.width/2,b.top+b.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("⑦ 왼쪽 「새 업무 만들기」 실제로 누름 → 바로 만들기 창", "await W(700);const r='버튼 높이='+window.__nwh+' | 만들기 창='+!!document.querySelector('#manualModal.show');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.closeModal&&app.closeModal('manualModal');await W(300);return r")
pt("document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const b=document.querySelector('.nw-split .sidebar-newwork-more').getBoundingClientRect();return JSON.stringify([b.left+b.width/2,b.top+b.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("⑦ 오른쪽 ▾ 실제로 누름 → 다른 방법 메뉴", "await W(400);const m=document.getElementById('newWorkMenu');return '메뉴 보임='+(getComputedStyle(m).display!=='none')+' | '+[...m.querySelectorAll('.mi')].map(x=>x.textContent.trim().slice(0,10)).join(' / ')+' | 만들기 창='+!!document.querySelector('#manualModal.show')")
S.append({"shot": "m8_newbtn.png"})
# ④ 내보내기
step("④ 일하는 화면 [내보내기] → 묻지 않고 바로 저장", "app.closeAllDropdowns&&app.closeAllDropdowns();window.__saved=[];window.showSaveFilePicker=async(o)=>({createWritable:async()=>({write:async()=>{},close:async()=>{window.__saved.push(o.suggestedName)}})});app.focusWorkflow(9102);await W(1500);app.exportOrHandOver(9102);await W(1500);const dlg=[...document.querySelectorAll('.modal.show')].map(m=>m.textContent.trim().slice(0,30)).join('|');return '저장='+window.__saved.join(',')+' | 묻는 창='+(dlg||'없음')")
step("④ 업무 분담 창 머리에 「다른 사람에게 넘기기」", "localStorage.setItem('collabMyName','홍길동');app.openCollabModal(9102);await W(900);const l=document.querySelector('#collabModal .cb-head-link');const r=l?l.textContent.trim():'없음';return r")
S.append({"shot": "m8_collab.png"})
# ⑤⑥ 길잡이
step("⑤ 길잡이 참고 자료(긴 이름)", "app.closeCollabModal&&app.closeCollabModal();await W(300);app.checklistDetails['project-9102']={attachments:[{name:'소방공무원 징계령 시행규칙 별표 1 징계기준 및 징계부가금 부과기준 (제2조 관련) 2024년 개정 전문 — 인사혁신처 고시 해설 포함.pdf'},{name:'공무원 징계령.txt'},{name:'소방공무원 복무규정 및 같은 규정 시행규칙에 따른 품위유지 의무 해석 사례집 — 질의회신 모음 2023.hwpx'}]};await app.showChecklistHelp(9102,1);await W(1500);"
     "const m=[...document.querySelectorAll('.gd-modal')].pop();const cards=[...m.querySelectorAll('.gd-sec')].find(s=>/참고 자료/.test(s.textContent))?.querySelectorAll('.gd-card')||[];const box=m.firstElementChild.getBoundingClientRect();return '참고 자료 카드='+cards.length+' | 높이='+[...cards].map(c=>Math.round(c.getBoundingClientRect().height)).join(',')+' | 칸 밖으로 넘침='+[...cards].some(c=>{const n=c.querySelector('.gd-card-name');return n.scrollHeight>n.clientHeight+2&&getComputedStyle(n).webkitLineClamp!=='2'})+' | 이름 줄 제한='+getComputedStyle(cards[0].querySelector('.gd-card-name')).webkitLineClamp+' | 형식 표시='+[...cards].map(c=>c.querySelector('.rf-ico')?.textContent).join(',')")
S.append({"shot": "m8_guide.png"})
pt("const b=[...document.querySelectorAll('.gd-modal .mx-btn')].pop().getBoundingClientRect();return JSON.stringify([b.left+b.width/2,b.top+b.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("⑥ 길잡이 ⤢ 실제로 누름 → 전체화면", "await W(400);const m=[...document.querySelectorAll('.gd-modal')].pop();const r=m.firstElementChild.getBoundingClientRect();return '전체화면='+m.classList.contains('gd-full')+' 크기='+Math.round(r.width)+'x'+Math.round(r.height)+' (창 '+innerWidth+'x'+innerHeight+') 버튼 눌림='+m.querySelector('.mx-btn').getAttribute('aria-pressed')")
S.append({"shot": "m8_guide_full.png"})
step("⑥ 닫고 다시 열면 기본 크기", "document.querySelectorAll('.gd-modal').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(500);await app.showChecklistHelp(9102,1);await W(1200);const m=[...document.querySelectorAll('.gd-modal')].pop();const r=m.firstElementChild.getBoundingClientRect();const res='전체화면='+m.classList.contains('gd-full')+' 너비='+Math.round(r.width);m.querySelector('[id$=_closeBtn]')?.click();return res")
step("⑥ 제목 줄 두 번 누르기", "await W(400);await app.showChecklistHelp(9102,1);await W(1200);const m=[...document.querySelectorAll('.gd-modal')].pop();const h=m.querySelector('[ondblclick]');h.dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));await W(300);const a=m.classList.contains('gd-full');h.dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));await W(300);const b=m.classList.contains('gd-full');m.querySelector('[id$=_closeBtn]')?.click();return '한 번='+a+' 두 번째='+b")
step("다크 모드: 고정 줄·목록 제목 줄 배경", mc + "app.exitFocusMode&&app.exitFocusMode();await W(600);document.documentElement.classList.add('dark-mode');app.setViewMode('list');await W(600);mc.scrollTop=300;await W(300);const r='검색 줄='+getComputedStyle(document.getElementById('controlBar')).backgroundColor+' 제목 줄='+getComputedStyle(document.querySelector('.wf-row-header')).backgroundColor;return r")
S.append({"shot": "m8_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
