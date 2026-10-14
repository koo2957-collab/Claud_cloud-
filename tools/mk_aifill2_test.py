# AI로 체크리스트 채우기 개선 시험 대본 → steps3.json  (AI 허용판 `ai_test .html`로 실행, 진짜 AI 대신 정해진 답을 돌려주는 가짜 AI)
# 보안 안내 · 첨부 PDF 참고 자료 연결 체크 · 진행 시간과 [취소] · 미리 보기(고르기·단계를 풀면 할 일도·업무팁 표시·건너뛰기 후보) ·
# 고른 것 넣기(업무팁·건너뛰기 버튼·참고 자료) · [되돌리기] · 지금 절차 뒤에 더하기 · [다시 만들기]·[버리기] · 예전 답 형식
# 실행: (tools 폴더에서) python mk_aifill2_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json, os
ANS = {"items": [
    {"text": "구매 준비", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "금액 기준 확인", "indent": 1, "warn": ["추정가격은 부가세를 뺀 금액"], "tip": "예산서와 맞춰 봅니다", "basis": ["지방계약법 시행령 제30조 (3쪽)"]},
    {"text": "견적서 받기", "indent": 1, "warn": [], "tip": "2곳 이상에서 받습니다", "basis": []},
    {"text": "나라장터 공고", "indent": 1, "warn": [], "tip": "", "basis": []},
    {"text": "계약", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "계약서 작성", "indent": 1, "warn": ["계약 보증금 확인", "인지세 확인"], "tip": "", "basis": []}],
    "branches": [{"at": 1, "label": "2천만원 이하", "skip": [3]}, {"at": 99, "label": "잘못된 후보", "skip": [1]}]}
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);"
     "const pdf=n=>new File([new Blob(['%PDF-1.4\\n1 0 obj<<>>endobj\\ntrailer<<>>\\n%%EOF'],{type:'application/pdf'})],n,{type:'application/pdf'});"
     "const wf=()=>app.allData.workflows.find(w=>w.id===app._nw?.wfId);const rows=()=>[...document.querySelectorAll('#checklistItems .checklist-edit-item')].map(r=>(r.dataset.indent==='1'?'└':'')+r.querySelector('input').value);"
     "const prev=()=>[...document.querySelectorAll('#aiFillPreview .aip-list')][0];const prow=i=>prev().querySelectorAll('.aip-row')[i];"
     "const sel=()=>[...prev().querySelectorAll('.aip-row')].map(r=>r.querySelector('input').checked?'☑':'☐').join('');"
     "const toast=()=>{const t=$('toast');return t&&t.classList.contains('show')?$('toastMessage').textContent.trim():'(알림 없음)'};"
     "const refs=()=>((app.checklistDetails['project-'+(wf()||{}).id]||{}).linkedLibraryDocs||[]).length;")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(12,b.width/2),b.top+b.height/2])")})
def click(expr): pt(expr); S.append({"clickpt": 1})
def stub(ms, ans=None):
    a = json.dumps(ans if ans is not None else ANS, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
    return "window.__calls=0;app.callAIWithDocuments=app.callAI=async(p)=>{window.__calls++;window.__prompt=p;await new Promise(r=>setTimeout(r," + str(ms) + "));return '" + a + "'};"

step("준비: 새 업무 ② · AI 칸 펼침", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();localStorage.setItem('tipNwTab','1');app.checkBackupReminder=()=>{};"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app.openModal('manualModal');await W(800);app.updateManualAiFillButtonState();$('manualProjectName').value='AI 개선 시험';app._nwGo(2);await W(500);app._toggleManualAiSection();await W(300);"
     "return '보안 안내='+($('aifSecure')?$('aifSecure').textContent.trim():'없음')")
step("A PDF 2개 첨부 → 참고 자료 연결 체크(기본 켜짐)", "const inp=$('manualDocUpload');const dt=new DataTransfer();dt.items.add(pdf('계약 지침.pdf'));dt.items.add(pdf('집행기준.pdf'));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));await W(1500);const c=document.querySelector('#uploadedFilesList .aif-link input');return '첨부='+app.uploadedFiles.map(f=>f.name).join(',')+' | 연결 체크='+(c?c.checked:'없음')")
step("B0 가짜 AI(2.5초) · 내용 적기", stub(2500) + "$('manualContent').value='물품 구매 계약 절차';return 'ok'")
click("$('manualAiFillBtn')")
step("B 만드는 중: 단계·초·[취소] · 버튼 막힘", "await W(1300);const s=$('aiFillStatus');return '진행 줄='+(s.hidden?'숨김':s.textContent.replace(/\\s+/g,' ').trim())+' | 버튼 막힘='+$('manualAiFillBtn').disabled")
step("C 미리 보기", "await W(2000);const b=$('aiFillPreview');return '보임='+!b.hidden+' | 머리='+b.querySelector('.aip-head b').textContent+' | 고름='+sel()+' | 업무팁 표시='+[...b.querySelectorAll('.aip-b')].map(x=>x.textContent).join(',')+' | 건너뛰기 후보='+b.querySelectorAll('.aip-list')[1]?.querySelectorAll('.aip-row').length+' (기본 고름='+b.querySelectorAll('.aip-list')[1]?.querySelector('input').checked+') | 넣는 방법 고르기='+!!b.querySelector('.aip-mode')+' | 진행 줄 숨김='+$('aiFillStatus').hidden+' | 요청 글에 근거·갈림길 규칙='+(/basis/.test(window.__prompt)&&/branches/.test(window.__prompt))")
S.append({"shot": "aif2_preview.png"})
click("prow(0).querySelector('input')")
step("D 단계 「구매 준비」를 풀면 그 할 일도", "await W(150);return '고름='+sel()")
click("prow(2).querySelector('input')")
step("D2 할 일 「견적서 받기」를 고르면 그 단계도", "await W(150);return '고름='+sel()+' | 넣기 단추='+$('aiFillInsertBtn').textContent")
click("prow(1).querySelector('input')")
click("document.querySelectorAll('#aiFillPreview .aip-list')[1].querySelector('input')")
step("E 건너뛰기 후보 고름", "await W(150);return '고름='+sel()+' | 후보='+document.querySelectorAll('#aiFillPreview .aip-list')[1].querySelector('input').checked")
click("$('aiFillInsertBtn')")
step("F 고른 것 넣기 → 절차·업무팁·건너뛰기 버튼·참고 자료", "await W(2000);const w=wf();const c=w.checklist;const br=c.find(x=>x.text==='금액 기준 확인');return '줄='+rows().join(' / ')+' | 업무팁='+c.filter(x=>x.tip&&x.tip.content).map(x=>x.text+'['+x.tip.content.replace(/\\n/g,'⏎')+']').join(' ; ')+' | 건너뛰기='+(br&&br.branchOptions?br.branchOptions.map(o=>o.label+'→'+o.targetItemIds.map(id=>c.find(x=>x.itemId===id).text).join(',')).join(''):'없음')+' | 참고 자료='+refs()+' | 미리 보기 닫힘='+$('aiFillPreview').hidden+' | 알림='+toast()")
S.append({"shot": "aif2_inserted.png"})
click("document.querySelector('#toastMessage .toast-undo-btn')")
step("G [되돌리기] → 넣기 전으로", "await W(600);return '줄='+JSON.stringify(rows())+' | 업무 항목='+(wf()?wf().checklist.length:0)+' | 참고 자료(그대로)='+refs()")
# 지금 절차가 있을 때 → 뒤에 더하기
step("H0 절차 두 줄 직접 쓰기 · AI 칸 다시 펼침", "const c=$('checklistItems');c.innerHTML='';c.appendChild(app._mkChecklistItemEl(0,'직접 쓴 단계',0));c.appendChild(app._mkChecklistItemEl(1,'직접 쓴 할 일',1));app.updateChecklistNumbers();app._toggleManualAiSection();await W(200);" + stub(300) + "app.fillChecklistWithAI();await W(900);const b=$('aiFillPreview');return '넣는 방법='+(b.querySelector('.aip-mode')?b.querySelector('.aip-mode').textContent.replace(/\\s+/g,' ').trim():'없음')")
click("$('aiFillInsertBtn')")
step("H 뒤에 더하기 · 참고 자료는 다시 넣지 않음", "await W(1500);return '줄 수='+rows().length+' | 맨 앞='+rows().slice(0,2).join(' / ')+' | 참고 자료='+refs()")
# 취소
step("I0 느린 가짜 AI(5초)", "app._toggleManualAiSection();await W(200);" + stub(5000) + "app.fillChecklistWithAI();await W(1200);return '진행 줄='+!$('aiFillStatus').hidden")
click("$('aiFillStatus').querySelector('button')")
step("I [취소] → 진행 줄 사라짐·버튼 다시 됨·나중 답은 버림", "await W(300);const a='진행 줄 숨김='+$('aiFillStatus').hidden+' | 버튼 됨='+!$('manualAiFillBtn').disabled+' | 알림='+toast().slice(0,20);await W(5200);return a+' | 5초 뒤 미리 보기='+!$('aiFillPreview').hidden")
# 다시 만들기 · 버리기 · 예전 답 형식
step("J [다시 만들기]·[버리기]", stub(200) + "app.fillChecklistWithAI();await W(600);const before=window.__calls;[...document.querySelectorAll('#aiFillPreview .aip-foot button')].find(b=>b.textContent.includes('다시')).click();await W(600);const again=window.__calls>before&&!$('aiFillPreview').hidden;[...document.querySelectorAll('#aiFillPreview .aip-foot button')].find(b=>b.textContent.includes('버리기')).click();await W(200);return '다시 만듦='+again+' | 버리기 뒤 숨김='+$('aiFillPreview').hidden")
step("K 예전 답 형식([{text,indent}])도 읽음", "const r=app._aiFillParse('[{\"text\":\"단계\",\"indent\":0},{\"text\":\"할 일\",\"indent\":1}]');const t=app._aiFillParse('[체크리스트]\\n- 접수\\n- 검토');return '배열='+r.items.map(x=>x.indent+x.text).join(',')+' | 줄 글='+t.items.map(x=>x.text).join(',')")
step("L 다크 모드", "document.documentElement.classList.add('dark-mode');" + stub(100) + "app.fillChecklistWithAI();await W(500);return 'ok'")
S.append({"shot": "aif2_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app._aiFillPreviewClose();app.closeModal?.('manualModal');app.uploadedFiles=[];app.allData.workflows=app.allData.workflows.filter(w=>!/AI 개선 시험/.test(w.title||''));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
