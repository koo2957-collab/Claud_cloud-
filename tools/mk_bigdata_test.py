# 많은 자료 시험 → steps3.json : 업무 300개(할 일 9,000줄)일 때 걸린 시간과 오류
# 목록 그리기 · 검색 · 업무 열기 · 체크 · 업무 관리 · 일정 · 진행상황 출력 · 내보내기 · 전체 백업 · 저장 · 새로 고침
# 한 번에 5초 넘게 걸리면(다른 시험과 동시에 돌 때도 견디게) 「느림 ✗」, 0.2초 넘는 긴 작업(longtask) 수도 셈
# 실행: python mk_bigdata_test.py [업무 수=300] && SELFCHECK=1 node cdp3.mjs <앱>
import json, os, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
     "const T=async(f)=>{const lt0=window.__lt||0;const t=performance.now();await f();await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const ms=Math.round(performance.now()-t);return ms+'ms'+(ms>5000?' 느림 ✗':'')+' · 긴 작업 '+((window.__lt||0)-lt0)};")
E = "}catch(e){return 'ERR '+e.message}})()"
S = []
def step(l, b, **k): S.append({"label": l, "js": P + b + E, **k})
step("준비 · 긴 작업 세기", "localStorage.setItem('welcomeShown','1');localStorage.setItem('deadlineNotifyMode','off');document.getElementById('welcomeModal')?.remove();app.checkBackupReminder=()=>{};window.confirm=()=>true;"
     "window.__lt=0;try{new PerformanceObserver(l=>{window.__lt+=l.getEntries().length}).observe({entryTypes:['longtask']})}catch(e){}await app.insertPracticeWorkflows();await W(2500);return 'ok'", nocheck=True)
step(f"업무 {N}개 만들기", "const src=app.allData.workflows.find(w=>/소모품/.test(w.title));const base=Date.now();const t=performance.now();"
     f"for(let k=0;k<{N};k++){{const w=JSON.parse(JSON.stringify(src));w.id=base+k*3;w.title='큰 자료 업무 '+(k+1)+' — '+['구매','점검','감찰','보고','교육'][k%5];delete w.isPractice;w.deadline=new Date(Date.now()+((k%60)-20)*864e5).toISOString().slice(0,10);"
     "const done=k%31;const cl=w.checklist;cl.forEach((it,i)=>{it.itemId='it'+k+'_'+i;it.completed=app._isSubEntry(it)&&i<done&&!it.skipped;if(it.completed)it.completedAt=new Date(Date.now()-(done-i)*36e5).toISOString();});cl.forEach((it,i)=>{if(app._isSubEntry(it))return;const subs=[];for(let j=i+1;j<cl.length&&app._isSubEntry(cl[j]);j++)subs.push(cl[j]);if(subs.length&&subs.every(x=>x.skipped||x.completed)){it.completed=true;it.completedViaSubItems=true;}else if(!subs.length&&i<done)it.completed=true;});if(k%23===0)w.isReference=true;else if(k%7===0)w.completedProcessed=true;w.folderPath=['','구매','감찰/2026','보고'][k%4];app.allData.workflows.push(w);}"
     "app.allData.folders=['구매','감찰','감찰/2026','보고'];app.saveData();return '업무='+app.allData.workflows.length+' · 할 일 줄='+app.allData.workflows.reduce((s,w)=>s+w.checklist.length,0)+' · '+Math.round(performance.now()-t)+'ms'", nocheck=True)
step("저장(바로)", "return await T(()=>app.saveDataImmediate())", nocheck=True)
step("목록 그리기", "return await T(()=>{app.displayWorkflows();app.updateStats();})")
step("검색 「감찰」", "return await T(async()=>{const i=document.getElementById('mainSearchInput');if(i){i.value='감찰';app.filterWorkflows();}await W(10);})")
step("검색 지우기", "return await T(async()=>{const i=document.getElementById('mainSearchInput');if(i){i.value='';app.filterWorkflows();}})")
step("업무 열기", "const w=app.allData.workflows.find(x=>/큰 자료 업무 15 /.test(x.title));window.__w=w.id;return await T(async()=>{app.focusWorkflow(w.id);await W(50);})")
step("체크 1번", "const w=app.allData.workflows.find(x=>x.id===window.__w);const i=w.checklist.findIndex((it,i)=>i>0&&!app.normalizeCompleted(it)&&app._isSubEntry(it)&&!it.skipped);return await T(async()=>{app.toggleChecklistItem(w.id,i);await W(1300);})")
step("체크리스트 편집 들어가기·나오기", "return await T(async()=>{app.enterFocusEditMode();await W(50);app.exitFocusEditMode();await W(50);})")
step("진행상황 출력", "localStorage.setItem('authorInfoSet','1');return await T(async()=>{app.openProgressReport(window.__w);await W(800);app.closeProgressReport&&app.closeProgressReport();})")
step("목록으로", "return await T(async()=>{app.exitFocusMode();await W(50);})")
step("업무 관리 열기", "return await T(async()=>{app.openWorkflowManager();await W(50);})")
step("업무 관리 탭 바꾸기 5번", "return await T(async()=>{for(const t of ['done','reference','archive','all','progress'])app.wfmSetTab(t);})")
step("업무 관리 닫기 · 일정", "app.closeModal('workflowManagerModal');return await T(async()=>{app.openSchedule(null);await W(50);app.closeSchedule();})")
step("업무 하나 내보내기", "let b=null;app._saveFileWithPicker=async x=>{b=x;return true};const r=await T(()=>app.exportMultipleWorkflowPackages([window.__w]));return r+' · 파일 '+Math.round((b&&b.size||0)/1024)+'KB'")
step("전체 백업 만들기", "let sz=0;const r=await T(async()=>{const o=await app._buildFullBackupObject();app._hideProgress?.();sz=JSON.stringify(o).length;});return r+' · '+Math.round(sz/1048576)+'MB'")
step("저장 공간", "const e=await navigator.storage.estimate();return Math.round(e.usage/1048576)+'MB 사용'", nocheck=True)
step("저장 뒤 새로 고침 준비", "await app.saveDataImmediate();await W(1500);localStorage.setItem('__bd_n',String(app.allData.workflows.length));localStorage.setItem('__bd_t',String(Date.now()));return 'ok'", nocheck=True)
S.append({"reload": 9000, "label": "새로 고침"})
step("다시 켠 뒤 업무 수 · 켜는 데 걸린 시간", "await W(500);return '업무='+app.allData.workflows.length+'/'+localStorage.getItem('__bd_n')+(String(app.allData.workflows.length)===localStorage.getItem('__bd_n')?' ✓':' ✗')+' · 다시 켜기~지금 '+(Date.now()-Number(localStorage.getItem('__bd_t')))+'ms'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
