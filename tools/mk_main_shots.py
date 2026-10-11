import json, sys
# 메인 화면 판단용 촬영: 카드형·목록형, 마감 임박 배너, 스크롤 시 검색·정렬 줄, 내보내기 창, 길잡이 참고 자료(긴 제목) → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
if len(sys.argv) > 1: S.append({'viewport': [int(v) for v in sys.argv[1].split('x')]})
def step(label, body): S.append({"label": label, "js": P + body + E})
step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};const ago=n=>new Date(Date.now()-n*864e5).toISOString();"
     "const T=[['구급대원 폭행 사건 내사(+수사) 처리 절차 — 구급활동 방해 피의자 3명 입건 여부 검토',2,5],['소방시설 자체점검 미실시 과태료 부과',-1,12],['소방장 품위유지의무 위반 징계처분',6,1],['물품 구매 계약(소방 장비 교체)',20,30],['감찰조사 — 근무지 무단이탈',3,3],['화재조사 보고서 작성',null,8],['민원 처리 — 소방차 전용구역 주차',1,0.5],['청렴 교육 계획 수립',40,60],['소방특별사법경찰 수사 서류 정리',null,90],['구조대 장비 점검표 정비',10,15],['위험물 안전관리자 선임 신고 확인',4,2],['안전문화 캠페인',null,100]];"
     "T.forEach(([t,dl,a],k)=>{const cl=[];for(let s=1;s<=4;s++){cl.push({text:'단계 '+s,indent:0,completed:k%4>=s,completedAt:k%4>=s?ago(a):null});}app.allData.workflows.unshift({id:9100+k,type:'manual',title:t,checklist:cl,date:'2026. 10. '+(1+k)+'.',createdAt:ago(a+5),lastProgressAt:ago(a),deadline:dl==null?undefined:D(dl),folderPath:''});});"
     "app.saveData();app.displayWorkflows();await W(800);return '정렬='+app.currentSortMethod+' 보기='+app.viewMode")
step("카드형", "app.setViewMode('grid');await W(600);return document.querySelectorAll('.workflow-card').length+'장'")
S.append({"shot": "ms_grid.png"})
step("카드형 아래로 스크롤", "const sc=[...document.querySelectorAll('*')].filter(x=>x.scrollHeight>x.clientHeight+20&&/(auto|scroll)/.test(getComputedStyle(x).overflowY)&&x.querySelector('.workflow-card'))[0]||document.scrollingElement;sc.scrollTop=600;await W(400);const s=document.getElementById('sortSelect').getBoundingClientRect();return '스크롤 상자='+(sc.id||sc.className||sc.tagName)+' | 정렬칸 위치='+Math.round(s.top)")
S.append({"shot": "ms_grid_scroll.png"})
step("목록형", "const sc=[...document.querySelectorAll('*')].filter(x=>x.scrollTop>0);sc.forEach(x=>x.scrollTop=0);app.setViewMode('list');await W(600);return 'ok'")
S.append({"shot": "ms_list.png"})
step("마감 임박 배너", "app.setViewMode('grid');await W(400);app.showDeadlineBanner(app.getUrgentWorksList(),3);await W(800);const b=document.getElementById('deadlineBanner').getBoundingClientRect();return '배너 '+Math.round(b.left)+','+Math.round(b.top)+' '+Math.round(b.width)+'x'+Math.round(b.height)+' | 창 '+innerWidth+'x'+innerHeight")
S.append({"shot": "ms_banner.png"})
step("내보내기 창(일하는 화면)", "app.hideDeadlineBanner&&app.hideDeadlineBanner();app.focusWorkflow(9102);await W(1500);app.exportOrHandOver(9102);await W(700);return [...document.querySelectorAll('.modal.show button')].map(b=>b.textContent.trim()).join(' / ')")
S.append({"shot": "ms_export.png"})
step("길잡이 참고 자료(긴 제목)", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));const wf=app.allData.workflows.find(w=>w.id===9102);const ids=[];for(const n of ['소방공무원 징계령 시행규칙 별표 1 징계기준 및 징계부가금 부과기준 (제2조 관련) 2024년 개정 전문.pdf','공무원 징계령.txt','소방공무원 복무규정 및 같은 규정 시행규칙에 따른 품위유지 의무 해석 사례집 — 인사혁신처 질의회신 모음 2023.hwpx']){ids.push(await app.dbManager.saveFile('lawLibrary',{name:n,size:30000,blob:new Blob(['x']),type:'text/plain',uploadedAt:new Date().toISOString()}).catch(e=>null));}"
     "wf.attachments=wf.attachments||[];wf.lawRefs=ids.filter(x=>x!=null);app.saveData();await app.showChecklistHelp(9102,1);await W(1500);const chips=[...document.querySelectorAll('[id^=aiGuideModal_] .ref-chip')];return '참고 자료 칩='+chips.length+' | '+chips.map(c=>Math.round(c.getBoundingClientRect().width)+'x'+Math.round(c.getBoundingClientRect().height)).join(', ')")
S.append({"shot": "ms_guide.png"})
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
