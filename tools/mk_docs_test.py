# 참고 자료 형식 넓히기 시험 대본 → steps3.json  (AI 허용판 `ai_test .html`로 실행, 가짜 AI가 받은 글·파일을 기록)
# AI로 다시 정리: 연결된 DOCX·HWPX는 「글만 읽음」, PDF는 「파일 그대로」, 예전 HWP는 「못 읽음」(흐림·까닭) → 글은 요청에 붙고 파일은 PDF만
# AI로 체크리스트 채우기: DOCX·HWPX 첨부 가능, HWP는 까닭 알림 → 글로 붙여 보냄
# 준비: tools/_tmp_docs/ 에 「징계 규정.hwpx」「옛 규정.hwp」(파이썬으로 만듦), tools/practice/ 의 DOCX·PDF 사용
# 실행: (tools 폴더에서) python mk_docs_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
# 시험용 한글 파일 만들기 (HWPX: 본문 + 표 안 글, HWP: 예전 형식 서명만) — tools/_tmp_docs/ 는 저장소에 안 올림
import zipfile
os.makedirs(HERE + '/_tmp_docs', exist_ok=True)
with zipfile.ZipFile(HERE + '/_tmp_docs/징계 규정.hwpx', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr(zipfile.ZipInfo('mimetype'), 'application/hwp+zip')
    z.writestr('Contents/section0.xml', '<?xml version="1.0" encoding="UTF-8"?><hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section" xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph"><hp:p><hp:run><hp:t>제12조(진술 기회) 진술 기회는 </hp:t><hp:t>10일 이상 주어야 한다.</hp:t></hp:run></hp:p><hp:p><hp:run><hp:tbl><hp:tr><hp:tc><hp:subList><hp:p><hp:run><hp:t>표 안 글: 출석 통지 5일 전</hp:t></hp:run></hp:p></hp:subList></hp:tc></hp:tr></hp:tbl></hp:run></hp:p></hs:sec>')
open(HERE + '/_tmp_docs/옛 규정.hwp', 'wb').write(bytes.fromhex('d0cf11e0a1b11ae1') + bytes(120))
FILES = [(HERE + '/practice/각서(수의계약 배제사유).docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
         (HERE + '/_tmp_docs/징계 규정.hwpx', ''),
         (HERE + '/_tmp_docs/옛 규정.hwp', ''),
         (HERE + '/practice/지방계약법 시행령(2026.6.3. 시행).pdf', 'application/pdf')]
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7811;"
     "const load=(u,t)=>new Promise((ok,no)=>{const x=new XMLHttpRequest();x.open('GET',encodeURI('file:///'+u));x.responseType='blob';x.onload=()=>ok(new File([x.response],u.split('/').pop(),{type:t||''}));x.onerror=()=>no(new Error('못 읽음 '+u));x.send();});"
     "const toast=()=>{const t=$('toast');return t&&t.classList.contains('show')?$('toastMessage').textContent.trim():'(알림 없음)'};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
ANS = json.dumps({"items": [{"text": "접수", "indent": 0, "from": ["o0"], "change": "유지", "warn": [], "tip": "", "basis": ["징계 규정.hwpx 제12조"]}], "removed": [], "branches": []}, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
STUB = "window.__calls=[];app.callAIWithDocuments=app.callAI=async(p,f)=>{window.__calls.push({p,f:Array.isArray(f)?f.map(x=>x.name):'(글만)'});await new Promise(r=>setTimeout(r,300));return '" + ANS + "'};"
files_js = json.dumps(FILES, ensure_ascii=False)
step("준비: 업무 + 참고 자료 4개(DOCX·HWPX·HWP·PDF)를 법령·매뉴얼에 넣고 연결",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.allData.workflows.unshift({id:ID,type:'manual',title:'징계 절차',checklist:[{text:'사건 접수',indent:0,completed:false}],date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});app.ensureChecklistItemId(app.allData.workflows[0].checklist[0]);"
     "const ids=[];for(const [u,t] of " + files_js + "){const f=await load(u,t);const id=await app.dbManager.saveFile('lawLibrary',{name:f.name,type:f.type,size:f.size,blob:f,uploadDate:new Date().toISOString(),groupId:null});ids.push(id);}await app._linkLibraryDocs(ID,ids);await app.saveDataImmediate();"
     "const hw=await app._extractTextFromBlob((await app._getLibraryFileById(ids[1])).blob,'징계 규정.hwpx');const dx=await app._extractTextFromBlob((await app._getLibraryFileById(ids[0])).blob,'각서.docx');const old=await app._extractTextFromBlob((await app._getLibraryFileById(ids[2])).blob,'옛 규정.hwp');"
     "return '연결='+ids.length+' | HWPX 글='+JSON.stringify(hw)+' | DOCX 글 앞='+JSON.stringify((dx||'').slice(0,30))+' | HWP 글='+old")
step("A AI로 다시 정리 창: 형식 표시", "await app.openAiRestructure(ID);await W(500);const rows=[...document.querySelectorAll('#aiRsModal .rs-sec')[0].querySelectorAll('label')];return rows.map(l=>l.textContent.replace(/\\s+/g,' ').trim()+(l.querySelector('input').disabled?'(흐림)':l.querySelector('input').checked?'☑':'☐')).join(' / ')")
S.append({"shot": "docs_setup.png"})
step("B 정리 시작 → 글은 요청에, 파일은 PDF만", STUB + "await app._aiRsStart();await W(400);const c=window.__calls[0];return 'AI에 보낸 파일='+JSON.stringify(c.f)+' | 요청 글에 DOCX='+c.p.includes('### 문서: 각서(수의계약 배제사유).docx')+' HWPX='+c.p.includes('10일 이상 주어야 한다')+' 표 안 글='+c.p.includes('출석 통지 5일 전')+' HWP='+c.p.includes('옛 규정.hwp')+' | 근거 규칙(조문)='+c.p.includes('문서 이름과 조문만')+' | 비교 화면='+!!document.querySelector('#aiRsModal .rs-cols')")
step("C 창 닫기", "app._aiRsClose();return 'ok'")
# AI로 체크리스트 채우기
step("D AI로 채우기: DOCX·HWPX·HWP 첨부", "app.openModal('manualModal');await W(800);app.updateManualAiFillButtonState();$('manualProjectName').value='형식 시험';app._nwGo(2);await W(400);app._toggleManualAiSection();await W(200);const inp=$('manualDocUpload');const dt=new DataTransfer();for(const [u,t] of " + json.dumps(FILES[:3], ensure_ascii=False) + "){dt.items.add(await load(u,t));}inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));await W(1500);return '받은 파일='+app.uploadedFiles.map(f=>f.name).join(',')+' | 첨부 칸 accept='+inp.accept+' | 안내='+$('docDropZone').textContent.replace(/\\s+/g,' ').trim().slice(0,60)")
step("D2 HWP는 까닭 알림", "return '알림 기록='+((app._notifyLog||[]).slice(-3).map(n=>n.message||n.body||'').join(' / ')||toast())")
step("E AI로 채우기 → 글로 붙여 보냄", STUB + "$('manualContent').value='징계 절차';await app.fillChecklistWithAI();await W(400);const c=window.__calls[0];return 'AI에 보낸 파일='+JSON.stringify(c.f)+' | 요청 글에 DOCX='+c.p.includes('### 문서: 각서')+' HWPX='+c.p.includes('10일 이상 주어야 한다')+' | 미리 보기='+!$('aiFillPreview').hidden")
step("정리", "app._aiFillPreviewClose();app.closeModal?.('manualModal');app.uploadedFiles=[];app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&!/형식 시험/.test(w.title||''));app._allowMassDelete=true;await app.saveDataImmediate();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
