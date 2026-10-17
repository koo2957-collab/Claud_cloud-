# 새 업무 「AI로 체크리스트 채우기」 자료: 내 PC + [법령·매뉴얼에서] 여러 개 · 업무 제목으로 「기준」 · 오른쪽 클릭으로 바꾸기 ·
# 기준 자료는 전부 / 나머지는 맞는 조문만(관계없는 자료는 안 보냄) · 미리 보기 근거 ✓ / 확인 필요 / 근거 없음 · 원문 창 · 넣으면 참고 자료로 연결
# 실행: (tools 폴더에서) python mk_aisrc_test.py && node cdp3.mjs "<저장소>/ai_test .html"   (가짜 AI)
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
PDF = HERE + '/practice/지방계약법 시행령(2026.6.3. 시행).pdf'
LAW = "제1조(목적) 이 영은 공무원 징계에 관하여 정한다.\\n제10조(출석 통지) 징계위원회는 징계 혐의자에게 출석 통지서를 회의 5일 전까지 보내야 한다.\\n제12조(진술) 징계 혐의자에게 진술할 기회를 주어야 한다.\\n제17조(징계 의결 기한) 징계 의결은 요구를 받은 날부터 30일 이내에 한다."
GUIDE = "제1조(목적) 이 지침은 소방공무원 징계 처분 업무 처리를 정한다.\\n제3조(진술 기회) 진술 기회는 서면 또는 출석으로 주며 진술서를 받는다.\\n제5조(감경) 표창 공적이 있으면 징계를 감경할 수 있다."
EQUIP = "제1조(목적) 이 규정은 소방 장비의 점검과 정비를 정한다.\\n제4조(점검 주기) 장비는 매월 1회 점검한다.\\n제6조(정비 기록) 정비 결과는 대장에 적는다."
ANS = {"items": [
    {"text": "징계 의결 요구", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "출석 통지서 보내기", "indent": 1, "warn": ["회의 5일 전까지"], "tip": "", "basis": ["공무원 징계령 제10조"]},
    {"text": "진술 기회 주기", "indent": 1, "warn": [], "tip": "진술서를 받는다", "basis": ["징계업무 처리지침 제3조"]},
    {"text": "감경 검토", "indent": 1, "warn": [], "tip": "", "basis": ["공무원 징계령 제99조"]},
    {"text": "결과 통보", "indent": 1, "warn": [], "tip": "", "basis": []}], "branches": []}
a = json.dumps(ANS, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);"
     "const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';"
     "const rows=()=>[...document.querySelectorAll('#uploadedFilesList .aif-src')].map(r=>tx(r.querySelector('.uploaded-file-name'))+'['+tx(r.querySelector('.uploaded-file-size')).replace(/.*· /,'')+(r.querySelector('.aif-base')?' · 기준':'')+']').join(' / ');"
     "const load=(u,t)=>new Promise((ok,no)=>{const x=new XMLHttpRequest();x.open('GET',encodeURI('file:///'+u));x.responseType='blob';x.onload=()=>ok(new File([x.response],u.split('/').pop(),{type:t||''}));x.onerror=()=>no(new Error('못 읽음'));x.send();});")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(expr): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+b.width/2,b.top+b.height/2])" + E})
def click(expr): pt(expr); S.append({"clickpt": 1})
step("준비: 법령·매뉴얼 3개(징계령 TXT·시행령 PDF·장비 규정 TXT) + 새 업무 ② AI 칸",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
     "window.__calls=[];app.callAIWithDocuments=app.callAI=async(p,f)=>{window.__calls.push({p,f:Array.isArray(f)?f.map(x=>x.name):'(글만)'});await W(300);return '" + a + "'};"
     "const old=await app._getAllLibraryFiles();for(const f of old){if(/공무원 징계령|장비 관리 규정|지방계약법 시행령/.test(f.name))await app.dbManager.deleteFile('lawLibrary',f.id);}"
     "const mk=(n,t)=>new File([t],n,{type:'text/plain'});const list=[mk('공무원 징계령.txt',\"" + LAW + "\"),await load('" + PDF + "','application/pdf'),mk('소방 장비 관리 규정.txt',\"" + EQUIP + "\")];"
     "window.__lib={};for(const f of list){window.__lib[f.name]=await app.dbManager.saveFile('lawLibrary',{name:f.name,type:f.type,size:f.size,blob:f,uploadDate:new Date().toISOString(),groupId:null});}"
     "app.openModal('manualModal');await W(800);$('manualProjectName').value='소방공무원 징계 처분';$('manualProjectName').dispatchEvent(new Event('input',{bubbles:true}));app._nwGo(2);await W(400);app._toggleManualAiSection();await W(300);"
     "return '법령·매뉴얼 단추='+tx(document.querySelector('.aif-lib-btn'))+' | 설명='+tx(document.querySelector('#manualAiSection > div')).slice(0,60)")
step("A 내 PC에서 지침 TXT 올림 → 목록 1개·기준", "const inp=$('manualDocUpload');const dt=new DataTransfer();dt.items.add(new File([\"" + GUIDE + "\"],'징계업무 처리지침.txt',{type:'text/plain'}));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));await W(1200);return rows()")
click("document.querySelector('.aif-lib-btn')")
step("B [법령·매뉴얼에서] → 고르기 창(새 업무 창 위)", "await W(1200);const m=$('lawLibraryModal');return '창='+(m&&m.classList.contains('show')&&m.classList.contains('fb-picking'))+' z='+(m&&m.style.zIndex)+' 머리='+tx(m&&m.querySelector('.fb-pick-banner b'))")
step("B2 셋 고르기", "for(const n in window.__lib)app._fbPick.sel.add(window.__lib[n]);app._fbPickBars('law');return tx(document.querySelector('.fb-pick-n'))")
click("[...document.querySelectorAll('#lawLibraryModal .fb-pick-foot button')].find(b=>/연결하기/.test(b.textContent))")
step("B3 연결하기 → 목록 4개, 업무 제목으로 기준", "await W(1500);return rows()")
S.append({"shot": "aisrc_list.png"})
pt("[...document.querySelectorAll('#uploadedFilesList .aif-src')].find(r=>/장비/.test(r.textContent))")
S.append({"rclickpt": 1})
step("C 장비 규정 오른쪽 클릭 → 메뉴", "await W(250);const m=$('fbCtxMenu');return tx(m)")
click("[...$('fbCtxMenu').querySelectorAll('.wfm-ctx-item')].find(x=>/기준으로/.test(x.textContent))")
step("C2 「이 자료를 기준으로」 → 기준 바뀜", "await W(300);return rows()")
step("C3 다시 징계령을 기준으로", "app._aiSetBase('l'+window.__lib['공무원 징계령.txt']);await W(200);return rows()")
step("D AI로 채우기 → 보낸 것: 기준 전부·맞는 조문만·관계없는 자료 안 보냄",
     "$('manualContent').value='';const r0=document.querySelector('#checklistItems .checklist-edit-item input');r0.value='징계 의결 요구';r0.dispatchEvent(new Event('input',{bubbles:true}));await app.fillChecklistWithAI();await W(500);const c=window.__calls[0]||{};const p=c.p||'';"
     "return '파일로 보냄='+JSON.stringify(c.f)+' | 기준 표시='+/기준 자료: 공무원 징계령/.test(p)+' 기준 전문(제17조)='+p.includes('30일 이내')+' | 지침 조문='+p.includes('### 참고 자료: 징계업무 처리지침.txt')+' 장비 규정 보냄='+p.includes('매월 1회')+' 시행령 보냄='+p.includes('### 참고 자료: 지방계약법')+' | 근거 규칙='+p.includes('문서 이름 제n조')+' | 업무 제목='+p.includes('[업무 제목')+' 지금 절차='+/지금 적혀 있는 절차[^\\n]*\\n징계 의결 요구/.test(p)")
step("D2 미리 보기: 기준 자료·근거 표시", "const b=$('aiFillPreview');return '머리='+tx(b.querySelector('.aip-head span')).slice(0,40)+' | '+[...b.querySelectorAll('.aip-row')].map(r=>tx(r.querySelector('.aip-text'))+'['+[...r.querySelectorAll('.aip-b')].map(x=>x.textContent).join(',')+']'+(r.querySelector('input').checked?'☑':'☐')).join(' / ')")
S.append({"shot": "aisrc_preview.png"})
click("$('aiFillPreview').querySelector('.aip-b.ok')")
step("E 근거 ✓ 누름 → 원문 창(제10조)·체크는 그대로", "await W(300);const m=$('lawHitModal');const r='창='+!!m+' '+tx(m&&m.querySelector('.lh-head'))+' | 줄 체크 그대로='+$('aiFillPreview').querySelectorAll('.aip-row input:checked').length;m&&m.remove();return r")
step("E2 넣기 단추 위", "const b=$('aiFillInsertBtn');b.scrollIntoView({block:'nearest'});await W(200);const r=b.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return '단추='+JSON.stringify([Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)])+' 막힘='+b.disabled+' 위에 있는 것='+(t?(t.id||t.className||t.tagName):'없음')+' 창='+innerWidth+'x'+innerHeight")
click("$('aiFillInsertBtn')")
step("F 넣기(실제 클릭) + 0.5초 뒤 한 번 더 누름 → 한 번만 들어감 · 참고 자료 연결", "const t0=performance.now();let mid='';for(let k=0;k<200&&!$('aiFillPreview').hidden;k++){await W(100);if(k===5){const b=$('aiFillInsertBtn');mid='0.5초 때 단추='+(b?(b.disabled?'막힘':'눌림 가능')+'('+tx(b)+')':'없음');b&&b.click();}}const ms=Math.round(performance.now()-t0);const id=app._nw&&app._nw.wfId;const d=app.checklistDetails['project-'+id]||{};return '끝나기까지 약 '+ms+'ms · '+mid+' | 연결된 법령·매뉴얼='+(d.linkedLibraryDocs||[]).length+' | 줄='+[...document.querySelectorAll('#checklistItems .checklist-edit-item input')].map(x=>x.value).join('/')")
step("정리", "const id=app._nw&&app._nw.wfId;app._aiFillPreviewClose?.();app._nwClosing=true;app.closeModal('manualModal');app._nwClosing=false;app._nw=null;app.uploadedFiles=[];app._aiFileObjs=[];app._aiLibIds=[];app._aiLibFiles=[];app._aiBaseKey=null;"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==id&&!/소방공무원 징계 처분/.test(w.title||''));for(const n in window.__lib)await app.dbManager.deleteFile('lawLibrary',window.__lib[n]);app._allowMassDelete=true;app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
