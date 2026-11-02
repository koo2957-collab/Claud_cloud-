import json
# 법령·매뉴얼 올리기 실시간 표시(임베딩 중에도 목록에 바로) · 길잡이 긴 제목에서 가·⤢·✕ 단추가 창 안에 남는지 → steps3.json
# AI 허용판(ai_test .html)에서 임베딩이 오래 걸리는 것을 흉내 내야 드러남 — 배포판은 키가 없어 임베딩을 건너뜀
# 실행: python mk_livelaw_test.py && node cdp3.mjs "<ai_test .html 절대 경로>"
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message}})()"
H = ("const pw=()=>app.allData.workflows.find(w=>/소모품 구매/.test(w.title)&&!w.isReference&&!w.isDeleted);"
     "const has=(sel,n)=>{const e=document.querySelector(sel);return e?(e.textContent.includes(n)?'보임':'안 보임'):'(없음)'};"
     "const cnt=()=>document.querySelector('#lawLibraryModal .fb-side').textContent.match(/모든 자료\\s*(\\d+)/)?.[1];"
     "const gm=()=>[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();"
     "const ctr=e=>{const r=e.getBoundingClientRect();return JSON.stringify([Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)])};")
S = []
def step(label, body, **kw): S.append({"label": label, "js": P + H + body + E, **kw})

step("준비", "localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.insertPracticeWorkflows();await W(2500);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return pw()?.title")

# L 법령·매뉴얼: 파일 두 개, 하나당 임베딩 6초 흉내
step("L1 법령·매뉴얼 두 개 올리기 — 첫 파일 저장 직후 목록·개수에 보임",
     "app.allData.geminiApiKey=app.allData.geminiApiKey||'AIzaFAKEKEY';window.__origEmb=app._generateAndStoreLibraryEmbeddings;"
     "app._generateAndStoreLibraryEmbeddings=async(id,k,cb)=>{cb&&cb(2);await W(2000);cb&&cb(3);await W(4000);const f=await app.dbManager.getFile('lawLibrary',id);f.embeddedAt=new Date().toISOString();f.embeddedChunkCount=3;await app.dbManager.saveFile('lawLibrary',f);return {success:true,successCount:3,totalCount:3};};"
     "await app.openLawLibrary();await W(800);window.__c0=+cnt();const inp=document.getElementById('lawLibraryFileInput');const dt=new DataTransfer();"
     "dt.items.add(new File(['제1조(목적) 실시간 시험. '.repeat(20)],'실시간_법령A.txt',{type:'text/plain'}));dt.items.add(new File(['제2조(정의) 실시간 시험. '.repeat(20)],'실시간_법령B.txt',{type:'text/plain'}));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));await W(1500);"
     "const ok=has('#lawLibraryModal .fb-tbody','실시간_법령A')==='보임'&&+cnt()===window.__c0+1&&!!document.getElementById('library-upload-progress');"
     "return (ok?'✓':'✗')+' A='+has('#lawLibraryModal .fb-tbody','실시간_법령A')+' · B='+has('#lawLibraryModal .fb-tbody','실시간_법령B')+' · 모든 자료 '+window.__c0+'→'+cnt()+' · 진행 표시='+!!document.getElementById('library-upload-progress')")
step("L2 첫 파일 임베딩 끝 → 「의미 검색」 표시 · 둘째 파일도 바로 보임",
     "await W(6000);const row=[...document.querySelectorAll('#lawLibraryModal .fb-tbody tr')].find(r=>r.textContent.includes('실시간_법령A'));const tag=!app.isAIAvailable()||(!!row&&row.textContent.includes('의미 검색'));"
     "const ok=tag&&has('#lawLibraryModal .fb-tbody','실시간_법령B')==='보임'&&+cnt()===window.__c0+2;"
     "return (ok?'✓':'✗')+' A 의미 검색='+tag+' · B='+has('#lawLibraryModal .fb-tbody','실시간_법령B')+' · 모든 자료 '+cnt()")
step("L3 모두 끝 → 진행 표시 사라짐 · 올리기 단추 다시 켜짐",
     "for(let k=0;k<100&&document.getElementById('library-upload-progress');k++)await W(200);const prog=!!document.getElementById('library-upload-progress');const dis=document.getElementById('lawLibraryFileInput').disabled;"
     "app._generateAndStoreLibraryEmbeddings=window.__origEmb;return (!prog&&!dis?'✓':'✗')+' 진행 표시='+prog+' · 입력 막힘='+dis")
step("L4 닫기", "app.closeModal('lawLibraryModal');await W(400);return 'ok'")

# G 길잡이 긴 제목
LONG = "수의계약 대상자 선정 결과에 따른 계약상대자 결격 사유 및 배제 사유 확인과 청렴계약 이행 각서 징구 및 수의계약 내역 공개 절차 진행"
CHK = ("const m=gm();const c=document.getElementById(m.id+'_content').getBoundingClientRect();const bs=[...m.querySelector('.gd-title').closest('div[ondblclick]').querySelectorAll('button')];"
       "const inside=bs.every(b=>{const r=b.getBoundingClientRect();return r.left>=c.left&&r.right<=c.right+0.5&&document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)?.closest('button')===b});"
       "const t=m.querySelector('.gd-title-t');const ell=t.scrollWidth>t.clientWidth;")
step("G1 길잡이 · 긴 제목 → 단추 셋 창 안·누를 수 있음 · 제목 말줄임",
     "const w=pw();const i=w.checklist.findIndex(x=>x.indent>0);window.__gi=i;window.__gt=w.checklist[i].text;w.checklist[i].text='" + LONG + "';app.focusWorkflow(w.id);await W(1500);await app.showChecklistHelp(w.id,i);await W(1500);"
     + CHK + "return ((inside&&ell&&t.title.length>20)?'✓':'✗')+' 단추 '+bs.length+'개 창 안·누를 수 있음='+inside+' · 말줄임='+ell+' · 마우스 올리면 전체 제목='+(t.title.length>20)")
step("G2 ⤢ 실제 클릭 → 넓게", "return ctr(gm().querySelector('.mx-btn:not(.rd-btn)'))", pt=True)
S.append({"clickpt": 1})
step("G3 넓게 된 뒤에도 단추 창 안", "await W(600);" + CHK + "const wide=c.width>800;return ((inside&&wide)?'✓':'✗')+' 창 너비='+Math.round(c.width)+' · 단추 창 안='+inside")
step("G4 ✕ 실제 클릭 → 닫힘", "return ctr(document.getElementById(gm().id+'_closeBtn'))", pt=True)
S.append({"clickpt": 1})
step("G5 닫혔는지", "await W(800);const m=gm();const open=!!m&&m.offsetParent!==null;return (!open?'✓':'✗')+' 길잡이 열림='+open")
step("G6 짧은 제목 → 단추는 늘 오른쪽 끝",
     "const w=pw();w.checklist[window.__gi].text='계약서 확인';await app.showChecklistHelp(w.id,window.__gi);await W(1500);" + CHK +
     "const x=document.getElementById(m.id+'_closeBtn').getBoundingClientRect();const edge=c.right-x.right<40;"
     "document.getElementById(m.id+'_closeBtn').click();await W(500);w.checklist[window.__gi].text=window.__gt;return ((inside&&edge)?'✓':'✗')+' 단추 창 안='+inside+' · ✕ 오른쪽 끝에서 '+Math.round(c.right-x.right)+'px'")
step("정리", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
