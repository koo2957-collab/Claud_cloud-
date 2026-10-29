# AI 체크리스트 만들기·편집 개선 시험 대본 → steps3.json  (가짜 AI · 가짜 임베딩)
#   AI 편집: 진행 중 업무는 단계 고정(이름·순서 그대로·잠금·끝낸 할 일 지킴·빠뜨린 할 일은 그 단계 안에) · 업무팁 고쳐 쓰기(같은 뜻 안 덧붙임)
#            · 기준/보충 두 칸·오른쪽 클릭으로 기준 바꾸기 · 긴 기준 자료는 목차 + 조문 · 보충 조문은 뜻으로도 찾음 · [↻ 다시] · 단계 오른쪽 클릭 「이 단계 할 일 채우기」
#   AI로 채우기: 기준/보충 두 칸 · 2번째 처리(보충 자료로 할 일 보탬·+출처·건너뛰기 번호 맞춤) · ⚠ 손볼 곳 · 이름 두 번 눌러 고치기 · [↻ 다시] · 법령·매뉴얼에도 넣기
# 실행: (tools 폴더에서) python mk_aiplus_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json, os
ID = 7981
def js(o): return json.dumps(json.dumps(o, ensure_ascii=False), ensure_ascii=False)   # 자바스크립트 문자열 글자로
LOCKED = {"stages": [
    {"id": "o0", "tasks": [{"text": "품의서 작성", "from": ["o1"], "change": "유지"}, {"text": "예산 확인 및 품의", "from": ["o2"], "change": "수정", "note": "이름 다듬음"}]},
    {"id": "o3", "tasks": [{"text": "견적서 받기", "from": ["o4"], "change": "유지", "edits": [{"n": 2, "text": "견적서를 2곳 이상에서 받는다"}], "warn": ["기한 7일 안에 통지해야 함", "계약 전 보증보험 확인"]},
                           {"text": "개인정보 수집 동의서 받기", "from": [], "change": "추가", "src": "개인정보 보호법 제15조"}]},
    {"id": "oX", "tasks": [{"text": "엉뚱한 단계", "from": []}]}],
    "removed": [{"id": "o1", "reason": "중복"}], "branches": []}
REDO_RS = {"tasks": [{"text": "품의서 작성", "from": ["o1"]}, {"text": "예산 확인하기", "from": ["o2"]}, {"text": "구매 계획 세우기", "from": []}]}
FILL = {"items": [
    {"text": "구매 준비", "indent": 0}, {"text": "품의서 작성하기", "indent": 1}, {"text": "예산 확인 및 견적 요청", "indent": 1},
    {"text": "계약", "indent": 0}, {"text": "계약서 작성하기", "indent": 1, "warn": ["계약 기한 확인"]},
    {"text": "빈 단계", "indent": 0}], "branches": [{"at": 1, "label": "소액", "skip": [5]}]}
SUP = {"add": [{"stage": 3, "text": "개인정보 수집 동의서 받기", "src": "개인정보 보호법 제15조", "warn": [], "tip": "", "basis": []},
               {"stage": 3, "text": "계약서 작성", "src": "개인정보 보호법 제17조"}],
       "notes": [{"item": 4, "warn": ["기준 규정은 7일, 개인정보 보호법은 10일 — 확인 필요", "계약 기한을 확인"], "basis": ["개인정보 보호법 제17조"]}]}
REDO_FILL = {"tasks": [{"text": "계약 상대 정하기"}, {"text": "계약서 작성하기", "warn": ["계약 기한 확인"]}]}

P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const vis=el=>!!el&&el.offsetParent!==null;const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';const NL=String.fromCharCode(10);"
     "const wf=()=>app.allData.workflows.find(w=>w.id===ID);const lines=()=>wf().checklist.map(x=>(x.indent?'└':'')+x.text+(app.normalizeCompleted(x)?'✓':'')).join(' / ');"
     "const rsRows=()=>[...document.querySelectorAll('#aiRsModal .rs-col:last-child .aip-row')].map(r=>(r.classList.contains('sub')?'└':'')+tx(r.querySelector('.aip-text'))+(r.classList.contains('lock')?'🔒':'')+(r.querySelector('.aip-b.q')?'⚠':'')+(r.querySelector('.aip-b.src')?'+출처':'')+(r.querySelector('.aip-b.ed')?'+고침':'')).join(' / ');"
     "const fillRows=()=>[...(document.querySelector('#aiFillPreview .aip-list')||document.body).querySelectorAll('.aip-row')].map(r=>(r.querySelector('.aip-dot')?'○':'['+tx(r.querySelector('.aip-num'))+']')+tx(r.querySelector('.aip-text'))+(r.querySelector('.aip-b.q')?'⚠':'')+(r.querySelector('.aip-b.src')?'('+tx(r.querySelector('.aip-b.src'))+')':'')).join(' / ');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(expr): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(b.width/2,40),b.top+b.height/2])" + E})
def click(expr): pt(expr); S.append({"clickpt": 1})
def rclick(expr): pt(expr); S.append({"rclickpt": 1})

STUB = ("window.__calls=[];window.__R={L:JSON.parse(" + js(LOCKED) + "),RR:JSON.parse(" + js(REDO_RS) + "),F:JSON.parse(" + js(FILL) + "),S:JSON.parse(" + js(SUP) + "),RF:JSON.parse(" + js(REDO_FILL) + ")};"
        "const ai=async(p,f)=>{window.__calls.push({p,f:Array.isArray(f)?f.map(x=>x.name):null});await W(250);const R=window.__R;"
        "if(/단계의 할 일만 다시 만들어/.test(p))return JSON.stringify(/\\(o\\d/.test(p)?R.RR:R.RF);if(/\"stages\"/.test(p))return JSON.stringify(R.L);if(/보충 자료의 조문을 보고/.test(p))return JSON.stringify(R.S);return JSON.stringify(R.F)};"
        "app.callAI=ai;app.callAIWithDocuments=ai;window.generateEmbedding=async()=>[1,0,0];")
# 긴 기준 규정(6만 자 넘게) · 보충 법령(제목 낱말과 겹치지 않음 → 뜻으로만 찾힘)
LIBS = ("const longT=Array.from({length:170},(_,k)=>'제'+(k+1)+'조(구매 절차 '+(k+1)+') '+(k%9===0?'견적서는 두 곳 이상에서 받고 예산 범위 안에서 품의한다. ':'')+'담당자는 물품 구매 업무를 기록하고 관리한다. '.repeat(16)).join(NL);"
        "const sup15='제15조(개인정보의 수집·이용) 개인정보처리자는 정보주체의 동의를 받아 수집할 수 있다.';const supT=sup15+NL+'제17조(제공) 개인정보처리자는 정보주체의 동의를 받아 제3자에게 제공할 수 있다.'+NL+'제22조(동의를 받는 방법) 계약서를 작성할 때 개인정보 수집 동의서를 따로 받아야 한다.'+NL+'제30조(처리방침) 처리방침을 정하여 공개한다.';"
        "for(const f of await app._getAllLibraryFiles()){if(/물품관리 기준 규정|개인정보 보호법|구매 메모/.test(f.name))await app.dbManager.deleteFile('lawLibrary',f.id);}"
        "const bf=new File([longT],'물품관리 기준 규정.txt',{type:'text/plain'}),sf=new File([supT],'개인정보 보호법.txt',{type:'text/plain'});"
        "window.__base=await app.dbManager.saveFile('lawLibrary',{name:bf.name,type:bf.type,size:bf.size,blob:bf,uploadDate:new Date().toISOString(),groupId:null});"
        "window.__sup=await app.dbManager.saveFile('lawLibrary',{name:sf.name,type:sf.type,size:sf.size,blob:sf,uploadDate:new Date().toISOString(),groupId:null,chunkEmbeddings:[{text:sup15,embedding:[1,0,0]}]});")

step("준비: 진행 중 업무(01-1 끝냄) + 법령·매뉴얼 2개(긴 기준 규정·보충 법령) 연결 → 편집 → AI 편집",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};window.confirm=()=>true;"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB + LIBS +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
     "const cl=[mk('준비',0),mk('품의서 작성',1),mk('예산 확인',1),mk('계약',0),mk('견적서 받기',1,'⚠ 기한 7일 안에 통지'+NL+'견적서를 받는다'),mk('계약서 작성',1),mk('검사',0),mk('검사조서 받기',1)];cl[1].completed=true;cl[1].completedAt=new Date().toISOString();"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'물품 구매',checklist:cl,date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});"
     "app.checklistDetails['project-'+ID]={attachments:[],forms:[],linkedLibraryDocs:[window.__base,window.__sup]};app.saveData();"
     "app.focusWorkflow(ID);await W(1300);app.enterFocusEditMode();await W(400);await app.openAiRestructure(ID);await W(700);"
     "const m=$('aiRsModal');return '제목='+tx(m.querySelector('h3'))+' | 고르기='+tx(m.querySelector('.rs-mode.on b'))+' | 기준 칸='+tx(m.querySelector('.aif-sec.base'))+' | 보충 칸='+tx(m.querySelector('.aif-sec.sup'))")
S.append({"shot": "aiplus_rs_setup.png"})
rclick("[...document.querySelectorAll('#aiRsModal .aif-sec.sup .aif-src')][0]")
step("A2 보충 자료 오른쪽 클릭 메뉴", "await W(250);return [...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>tx(x)).join(' / ')")
click("[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')][0]")
step("A3 「이 자료를 기준으로」 → 두 칸이 바뀜 → (원래대로 되돌려 둠)", "await W(250);const m=$('aiRsModal');const r='기준 칸='+tx(m.querySelector('.aif-sec.base .aif-src'))+' | 보충 칸='+tx(m.querySelector('.aif-sec.sup .aif-src'));app._aiRs.baseKey=null;app._aiRsRender();return r")
click("[...document.querySelectorAll('#aiRsModal .rs-mode')][2]")   # 진행 중이면 「빠진 할 일 더하기」가 먼저 — 이 대본은 「할 일 다듬기 🔒」
click("[...document.querySelectorAll('#aiRsFoot .btn-primary')].pop()")
step("B 정리 시작 → 단계 고정 답 · 보낸 글(단계 고정 규칙·업무팁 줄 번호·예시·목차·보충 조문 뜻으로 찾음)",
     "for(let i=0;i<60&&!document.querySelector('#aiRsModal .rs-cols');i++)await W(100);const p=window.__calls.at(-1).p;"
     "return '부른 수='+window.__calls.length+' | 단계 고정 규칙='+/단계 이름·순서·개수는 바꾸지 않습니다/.test(p)+' 줄 번호='+p.includes('[1] ⚠ 기한 7일')+' 예시='+p.includes('좋은 예시')+' 정의='+p.includes('결과물(문서·결재')"
     "+' | 목차='+p.includes('[목차]')+' 기준 이름='+p.includes('기준 자료: 물품관리 기준 규정')+' | 보충 제15조(뜻으로)='+(p.includes('### 보충 자료: 개인정보 보호법')&&p.includes('제15조'))+' | 아래 안내='+tx($('aiRsFoot').querySelector('.rs-note')).slice(0,80)")
step("B2 검토 화면: 단계 이름·순서 그대로(🔒) · 엉뚱한 단계 없음 · 끝낸 할 일 지킴 · 빠뜨린 할 일은 그 단계 안 · ⚠ · +출처 · 업무팁 고침",
     "return '안내='+tx(document.querySelector('#aiRsModal .rs-locknote'))+' || '+rsRows()")
S.append({"shot": "aiplus_rs_review.png"})
click("document.querySelector('#aiRsModal .aip-row.lock input')")
step("B3 잠긴 단계 체크 풀기 → 그대로 넣음", "await W(200);const i=document.querySelector('#aiRsModal .aip-row.lock input');return '체크='+i.checked+' 막힘='+i.disabled")
click("[...document.querySelectorAll('#aiRsModal .aip-redo')][0]")
step("C 「준비」 [↻ 다시] → 그 단계 할 일만 바뀜(⚠ 사라짐) · 다른 단계 그대로",
     "for(let i=0;i<40&&app._aiRs&&app._aiRs.redoing!=null;i++)await W(100);await W(200);return '보낸 글에 원래 번호='+/\\(o1\\)/.test(window.__calls.at(-1).p)+' || '+rsRows()")
click("$('aiRsApplyBtn')")
step("D 넣기 → 편집 중 체크리스트: 단계 그대로 · 끝낸 할 일 ✓ · 업무팁은 그 줄을 고침(같은 뜻은 안 덧붙임) · 출처는 근거로",
     "await W(800);const c=wf().checklist;const t=c.find(x=>x.text==='견적서 받기').tip.content;const g=(c.find(x=>/동의서/.test(x.text))||{}).tip;"
     "return '줄='+lines()+' || 견적서 업무팁='+JSON.stringify(t)+' || 동의서 업무팁='+JSON.stringify(g&&g.content)")
step("D2 편집 취소 → 원래대로", "app.cancelFocusEditMode();await W(500);const d=[...document.querySelectorAll('.modal.show')].pop();const nb=d&&[...d.querySelectorAll('button')].find(b=>/저장 안 함/.test(b.textContent));if(nb)nb.click();await W(900);return '편집='+app.focusEditMode+' | 줄='+lines()")
rclick("document.querySelector('.checklist-card[data-workflow-id=\"'+ID+'\"][data-index=\"3\"] .item-title-text')")
step("E 단계 오른쪽 클릭 메뉴에 「✨ 이 단계 할 일 채우기」", "await W(300);return [...document.querySelectorAll('#checklistItemMenu button[data-i]')].map(b=>tx(b)).filter(t=>/AI|이 단계/.test(t)).join(' / ')")
click("[...document.querySelectorAll('#checklistItemMenu button[data-i]')].find(b=>/이 단계 할 일 채우기/.test(b.textContent))")
step("E2 그 단계만: 제목·고르기 글",
     "for(let i=0;i<40&&!$('aiRsModal');i++)await W(100);await W(500);const m=$('aiRsModal');return '편집='+app.focusEditMode+' | 제목='+tx(m.querySelector('h3'))+' | 고르기='+tx(m.querySelector('.rs-mode.on b'))+' | 건너뛰기 추천 기본='+app._aiRs.wantBranch")
click("[...document.querySelectorAll('#aiRsFoot .btn-primary')].pop()")
step("E3 보낸 글에는 「계약」 단계만 · 검토는 다른 단계 그대로",
     "for(let i=0;i<60&&!document.querySelector('#aiRsModal .rs-cols');i++)await W(100);const p=window.__calls.at(-1).p;const part=p.split('[다듬을 단계와 할 일]')[1]||'';"
     "return '다듬을 곳에 계약='+/o3 \\| 단계 \\| 계약/.test(part)+' 준비 빠짐='+!/o0 \\| 단계/.test(part.split('【')[0])+' | 안내='+tx(document.querySelector('#aiRsModal .rs-locknote'))+' || '+rsRows()")
step("E4 닫기 → 편집 취소", "app._aiRsClose();await W(200);app.cancelFocusEditMode();await W(500);const d=[...document.querySelectorAll('.modal.show')].pop();const nb=d&&[...d.querySelectorAll('button')].find(b=>/저장 안 함/.test(b.textContent));if(nb)nb.click();await W(900);app.exitFocusMode?.();await W(600);return '편집='+app.focusEditMode")

# ── AI로 채우기 ──
step("F 새 업무 ② AI 칸: 법령·매뉴얼 2개 + 내 PC 메모 → 기준·보충 두 칸 · 법령·매뉴얼에도 넣기(기본 켬)",
     "window.__calls=[];app.openModal('manualModal');await W(800);$('manualProjectName').value='사무용품 구매';$('manualProjectName').dispatchEvent(new Event('input',{bubbles:true}));app._nwGo(2);await W(400);if($('manualAiSection').style.display==='none')app._toggleManualAiSection();await W(300);"
     "app._aiBaseKey=null;app._aiLibIds=[window.__base,window.__sup];app._aiLibFiles=[];for(const id of app._aiLibIds){const f=await app._getLibraryFileById(id);app._aiLibFiles.push({id:f.id,name:f.name,size:f.size,type:f.type||''});}"
     "const inp=$('manualDocUpload');const dt=new DataTransfer();dt.items.add(new File(['구매 메모: 사무용품은 분기마다 산다.'],'구매 메모.txt',{type:'text/plain'}));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));await W(1500);"
     "const L=$('uploadedFilesList');return '기준 칸='+[...L.querySelectorAll('.aif-sec.base .uploaded-file-name')].map(tx).join(',')+' | 보충 칸='+[...L.querySelectorAll('.aif-sec.sup .uploaded-file-name')].map(tx).join(',')+' | 넣기 칸='+[...L.querySelectorAll('.aif-link')].map(l=>tx(l).slice(0,60)+(l.querySelector('input').checked?'☑':'☐')).join(' / ')")
S.append({"shot": "aiplus_fill_list.png"})
rclick("[...document.querySelectorAll('#uploadedFilesList .aif-sec.sup .aif-src')].find(r=>/기준 규정/.test(r.textContent))")
click("[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')][0]")
step("F2 오른쪽 클릭 「이 자료를 기준으로」 → 기준 칸", "await W(300);return '기준 칸='+[...document.querySelectorAll('#uploadedFilesList .aif-sec.base .uploaded-file-name')].map(tx).join(',')")
click("$('manualAiFillBtn')")
step("G AI로 채우기 → 2번 부름(만들기 + 보충 자료) · 보충 조문은 뜻으로 · 미리 보기 체크리스트 모양",
     "for(let i=0;i<80&&!vis(document.querySelector('#aiFillPreview .aip-row'));i++)await W(100);await W(300);const c=window.__calls;"
     "return '부른 수='+c.length+' | 만들기 글: 예시='+c[0].p.includes('좋은 예시')+' 보충 역할='+c[0].p.includes('보충 자료:')+' 목차='+c[0].p.includes('[목차]')+' 첫 글에 보충 제15조(뜻으로)='+c[0].p.includes('제15조')+' | 보충 처리 글 있음='+!!(c[1]&&/보충 자료의 조문을 보고/.test(c[1].p))"
     "+' || 머리='+tx(document.querySelector('#aiFillPreview .aip-head span'))+' || '+fillRows()+' || 네모='+document.querySelectorAll('#aiFillPreview .aip-num').length+' 동그라미='+document.querySelectorAll('#aiFillPreview .aip-dot').length")
S.append({"shot": "aiplus_fill_prev.png"})
step("G2 보충 자료가 이미 있는 할 일을 다시 더하지 않음 · 같은 뜻 놓치기 쉬운 것 한 번 · 건너뛰기 후보 번호 맞음",
     "const st=app._aiFillState;const it=st.items.find(x=>x.text==='계약서 작성하기');return '「계약서 작성」 중복 추가='+st.items.filter(x=>/계약서 작성/.test(x.text)).length+' | 계약서 작성하기 warn='+JSON.stringify(it.warn)+' basis='+JSON.stringify(it.basis)+' | 건너뛰기='+st.branches.map(b=>st.items[b.at].text+'→'+b.skip.map(k=>st.items[k].text).join(',')).join(';')")
step("H 단계 이름 두 번 눌러 고치기(계약 → 계약 체결)",
     "const r=[...document.querySelectorAll('#aiFillPreview .aip-row.stage')].find(x=>tx(x.querySelector('.aip-text'))==='계약');r.querySelector('.aip-text').dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));await W(150);const inp=document.querySelector('#aiFillPreview .aip-ren');if(!inp)return '입력칸 없음';inp.value='계약 체결';inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));await W(200);return fillRows()")
click("[...document.querySelectorAll('#aiFillPreview .aip-row.stage')].find(x=>/계약 체결/.test(x.textContent)).querySelector('.aip-redo')")
step("H2 [↻ 다시] → 고친 이름으로 그 단계 할 일만", "for(let i=0;i<40&&app._aiFillState&&app._aiFillState.redoing!=null;i++)await W(100);await W(200);return '보낸 글에 「계약 체결」='+window.__calls.at(-1).p.includes('「계약 체결」 단계의 할 일만')+' || '+fillRows()")
click("$('aiFillInsertBtn')")
step("I 넣기 → 절차 줄 · 참고 자료 연결 · 내 PC 메모도 법령·매뉴얼에 저장됨",
     "await W(800);const t=[...document.querySelectorAll('.toast')].map(x=>tx(x)).filter(Boolean).pop()||'';const rows=[...document.querySelectorAll('#checklistItems .checklist-edit-item')].map(r=>(parseInt(r.dataset.indent||0)?'└':'')+(r.querySelector('input')?.value||'')).join(' / ');"
     "let lib=null;for(let i=0;i<30&&!lib;i++){await W(200);lib=await app._getLibraryFileByName('구매 메모.txt');}return '알림='+t.slice(0,90)+' || 줄='+rows+' || 법령·매뉴얼에 들어감='+!!lib")
step("J 업무팁 같은 뜻 판단(조사·띄어쓰기) · 고쳐 쓰기",
     "const T=(a,b)=>app._tipSame(a,b);const m=app._aiMergeTip('⚠ 기한 7일 안에 통지'+NL+'□ 견적서를 받는다'+NL+'근거: 규정 제3조',{edits:[{n:2,text:'견적서를 2곳 이상에서 받는다'},{n:3,text:'근거: 규정 제3조 제2항'}],warn:['기한 7일 안에 통지해야 함'],tip:'견적서를 받는다.',basis:['규정 제3조']});"
     "return '같음: '+[T('기한 7일 안에 통지','기한 7일 안에 통지해야 함'),T('접수 대장에 적기','접수 대장에 적습니다'),T('출석 통지서는 회의 5일 전까지 보낸다','출석통지서를 회의 5일 전까지 보냄')].join(',')+' | 다름: '+[T('예산 확인','검사조서 받기'),T('계약서 작성','계약 상대 정하기')].join(',')+' || 합친 글='+JSON.stringify(m)")
step("정리", "app._aiFillPreviewClose?.();app.closeModal?.('manualModal');await W(500);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "for(const f of await app._getAllLibraryFiles()){if(/물품관리 기준 규정|개인정보 보호법|구매 메모/.test(f.name))await app.dbManager.deleteFile('lawLibrary',f.id);}"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&!/사무용품 구매/.test(w.title||''));app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
