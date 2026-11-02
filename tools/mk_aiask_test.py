# AI 편집 「더 바라는 것 (선택)」 한 줄 시험 대본 → steps3.json  (가짜 AI, 실제 클릭·타자)
#   설정 화면: 세 칸 아래 한 줄·칸마다 예시 글·보안 안내에 「써 넣은 요청」 · 실제 타자 → Enter = 시작
#   · 보내는 글에 요청이 규칙 뒤·JSON 형식 앞에 · 비우면 예전과 같은 글 · 입력칸에서 Delete·Backspace가 체크리스트를 안 지움
#   검토 화면: 맨 위 같은 칸(쓴 글 그대로) · 고쳐 Enter → 새 요청으로 다시 · 단계 [↻ 다시]도 같은 요청 · 업무팁·근거만/빠진 할 일 더하기도 요청이 들어감
#   진행 중 업무: 요청이 「단계 합쳐 줘」여도 단계 고정 규칙은 그대로 앞에 있음
# 실행: (tools 폴더에서) python mk_aiask_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json
ID = 7986
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';const M=()=>$('aiRsModal');"
     "const wf=()=>app.allData.workflows.find(w=>w.id===ID);const last=()=>window.__calls[window.__calls.length-1]||'';"
     "const blk=p=>{const k=p.indexOf('【사용자가 더 바라는 것】');return k<0?'(없음)':p.slice(k+15,p.indexOf('\\n',k)).trim()};"
     "const order=p=>{const a=p.indexOf('【사용자가 더 바라는 것】'),r=p.indexOf('【규칙】'),j=p.lastIndexOf('다음 JSON 형식으로만');return a>r&&a<j};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(expr): S.append({"pt": True, "js": P + "const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(b.width/2,30),b.top+b.height/2])" + E})
def click(expr): pt(expr); S.append({"clickpt": 1})
def key(k, vk, text=None):
    d = {"key": k, "vk": vk}
    if text: d["ktext"] = text
    S.append(d)

STUB = ("window.__calls=[];"
        "const ai=async(p)=>{window.__calls.push(p);await W(250);"
        "if(/할 일만 다시 만들어/.test(p))return JSON.stringify({tasks:[{text:'품의서 작성',from:['o1']},{text:'결재 받기',from:[]}]});"
        "if(/빠진 할 일만 찾아/.test(p))return JSON.stringify({adds:[]});"
        "if(/만 만들어 주세요/.test(p))return JSON.stringify({items:[{id:'o1',warn:['감사 지적: 예산 과목 확인']}],branches:[]});"
        "if(/진행 중인 업무라/.test(p))return JSON.stringify({stages:[{id:'o0',tasks:[]}],removed:[],branches:[]});"
        "return JSON.stringify({items:[{text:'준비',indent:0,from:['o0']},{text:'품의서 작성',indent:1,from:['o1']},{text:'결재 받기',indent:1,from:[]},{text:'계약',indent:0,from:['o3']},{text:'견적서 받기',indent:1,from:['o4']}],removed:[],branches:[]})};"
        "app.callAI=ai;app.callAIWithDocuments=ai;")
MK = ("const mk=(t,i)=>{const o={text:t,indent:i,completed:false};app.ensureChecklistItemId(o);return o};"
      "const cl=[mk('준비',0),mk('품의서 작성',1),mk('예산 확인',1),mk('계약',0),mk('견적서 받기',1)];")
OPEN = "app.focusWorkflow(ID);await W(1300);app.enterFocusEditMode();await W(400);await app.openAiRestructure(ID);await W(700);"
CLOSE = ("app._aiRsClose?.();await W(200);if(app.focusEditMode){app.cancelFocusEditMode();await W(500);const d=[...document.querySelectorAll('.modal.show')].pop();const nb=d&&[...d.querySelectorAll('button')].find(b=>/저장 안 함/.test(b.textContent));if(nb)nb.click();await W(800);}")

step("A1 준비: 시작 전 업무 → AI 편집 → 세 칸 아래 「더 바라는 것」 한 줄 · 예시 글 · 보안 안내",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);" + MK +
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'물품 구매',checklist:cl,date:'2026. 11. 2.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();" + OPEN +
     "const a=$('aiRsAsk');const modes=M().querySelector('.rs-modes').getBoundingClientRect();const r=a.getBoundingClientRect();"
     "const ok=!!a&&r.top>modes.bottom&&a.value===''&&/결재/.test(a.placeholder)&&/써 넣은 요청/.test(tx(M().querySelector('.rs-secure')));"
     "return (ok?'✓':'✗')+' 칸='+!!a+' · 세 칸 아래='+(r.top>modes.bottom)+' · 예시='+a.placeholder+' · 보안 안내='+tx(M().querySelector('.rs-secure span'))")
step("A2 칸을 바꾸면 예시 글이 바뀜 · 쓴 글은 그대로",
     "const a=$('aiRsAsk');a.value='남김';a.dispatchEvent(new Event('input'));app._aiRsMode('keep');await W(200);const p1=$('aiRsAsk').placeholder,v1=$('aiRsAsk').value;app._aiRsMode('add');await W(200);const p2=$('aiRsAsk').placeholder;app._aiRsMode('restructure');await W(200);$('aiRsAsk').value='';$('aiRsAsk').dispatchEvent(new Event('input'));"
     "const ok=/감사 지적/.test(p1)&&/계약 전/.test(p2)&&v1==='남김';return (ok?'✓':'✗')+' 업무팁·근거만='+p1+' · 빠진 할 일='+p2+' · 쓴 글 남음='+(v1==='남김')")
click("$('aiRsAsk')")
S.append({"text": "결재 받는 일을 따로 빼 줘"})
step("A3 실제 타자 → 칸에 들어감 · Delete·Backspace 눌러도 체크리스트 그대로",
     "window.__n=document.querySelectorAll('.focus-mode [data-index]').length;return '칸='+$('aiRsAsk').value+' · 포커스='+(document.activeElement===$('aiRsAsk'))")
key("Delete", 46)
key("Backspace", 8)
S.append({"text": "줘"})
step("A4 체크리스트 줄 수 그대로 · 글 맞음",
     "const n=document.querySelectorAll('.focus-mode [data-index]').length;const ok=n===window.__n&&app._aiRs.ask==='결재 받는 일을 따로 빼 줘'&&!!M();return (ok?'✓':'✗')+' 줄 '+window.__n+'→'+n+' · 요청='+app._aiRs.ask")
key("Enter", 13, "\r")
step("A5 Enter = 정리 시작 → 보내는 글에 요청이 규칙 뒤·JSON 앞에 → 검토 화면",
     "for(let k=0;k<30&&app._aiRs&&app._aiRs.phase!=='review';k++)await W(200);const p=last();const ok=window.__calls.length===1&&blk(p)==='결재 받는 일을 따로 빼 줘'&&order(p)&&app._aiRs.phase==='review';"
     "return (ok?'✓':'✗')+' 부른 수='+window.__calls.length+' · 요청='+blk(p)+' · 규칙 뒤 JSON 앞='+order(p)+' · 단계='+app._aiRs.phase")
S.append({"shot": "aiask_review.png"})
step("B1 검토 화면 맨 위 같은 칸(쓴 글 그대로 · Enter 안내)",
     "const a=$('aiRsAsk');const bar=a&&a.closest('.rs-askbar');const first=bar&&$('aiRsBody').firstElementChild===bar;const ok=!!bar&&first&&a.value==='결재 받는 일을 따로 빼 줘'&&/Enter = \\[다시 정리\\]/.test(tx(bar));"
     "return (ok?'✓':'✗')+' 맨 위='+first+' · 값='+(a&&a.value)+' · 안내='+tx(bar&&bar.querySelector('.rs-ask-k'))")
click("$('aiRsAsk')")
key("End", 35)
S.append({"text": " · 할 일 이름은 짧게"})
key("Enter", 13, "\r")
step("B2 고쳐 Enter → 새 요청으로 다시 정리",
     "await W(400);for(let k=0;k<30&&app._aiRs&&app._aiRs.phase!=='review';k++)await W(200);const p=last();const ok=window.__calls.length===2&&blk(p)==='결재 받는 일을 따로 빼 줘 · 할 일 이름은 짧게'&&app._aiRs.phase==='review'&&$('aiRsAsk').value===app._aiRs.ask;"
     "return (ok?'✓':'✗')+' 부른 수='+window.__calls.length+' · 요청='+blk(p)")
click("[...M().querySelectorAll('.aip-redo')][0]")
step("B3 단계 [↻ 다시]도 같은 요청",
     "for(let k=0;k<30&&app._aiRs&&app._aiRs.redoing!=null;k++)await W(200);const p=last();const ok=window.__calls.length===3&&/할 일만 다시 만들어/.test(p)&&blk(p)==='결재 받는 일을 따로 빼 줘 · 할 일 이름은 짧게'&&order(p);"
     "return (ok?'✓':'✗')+' 부른 수='+window.__calls.length+' · 요청='+blk(p)+' · JSON 앞='+order(p)")
step("B4 요청을 비우고 다시 → 요청 줄 없음(예전과 같은 글)",
     "const a=$('aiRsAsk');a.value='';a.dispatchEvent(new Event('input'));app._aiRsAskEnter();await W(400);for(let k=0;k<30&&app._aiRs&&app._aiRs.phase!=='review';k++)await W(200);const p=last();const same=p===app._aiRsPromptBase(app._aiRs);"
     "return ((blk(p)==='(없음)'&&same)?'✓':'✗')+' 요청 줄='+blk(p)+' · 예전 글과 같음='+same")
step("C1 업무팁·근거만 보태기에도 요청",
     "app._aiRs.phase='setup';app._aiRsMode('keep');await W(200);const a=$('aiRsAsk');a.value='감사 지적 사례 위주로';a.dispatchEvent(new Event('input'));app._aiRsAskEnter();await W(400);for(let k=0;k<30&&app._aiRs&&app._aiRs.phase!=='review';k++)await W(200);const p=last();"
     "const bar=!!$('aiRsAsk')?.closest('.rs-askbar');const ok=blk(p)==='감사 지적 사례 위주로'&&order(p)&&bar&&/다시 만들기/.test(tx($('aiRsAsk').closest('.rs-askbar')));return (ok?'✓':'✗')+' 요청='+blk(p)+' · 검토 칸='+bar")
step("C2 정리", CLOSE + "return 'ok'")
step("D1 진행 중 업무 → 빠진 할 일 더하기에 요청 · 단계 고정 규칙은 앞에 그대로",
     "const w=wf();w.checklist[1].completed=true;w.checklist[1].completedAt=new Date().toISOString();app.saveData();" + OPEN +
     "const mode=app._aiRs.mode;const a=$('aiRsAsk');a.value='단계를 하나로 합쳐 줘';a.dispatchEvent(new Event('input'));app._aiRsAskEnter();await W(400);for(let k=0;k<30&&app._aiRs&&app._aiRs.phase!=='review';k++)await W(200);const p1=last();"
     "app._aiRs.phase='setup';app._aiRsMode('restructure');await W(200);app._aiRsAskEnter();await W(400);for(let k=0;k<30&&app._aiRs&&app._aiRs.phase!=='review';k++)await W(200);const p2=last();"
     "const lockRule=p2.indexOf('단계 이름·순서·개수는 바꾸지 않습니다'),ask=p2.indexOf('【사용자가 더 바라는 것】');const st=app._aiRs.items.filter(x=>!x.indent).map(x=>x.text).join('/');"
     "const ok=mode==='add'&&blk(p1)==='단계를 하나로 합쳐 줘'&&order(p1)&&lockRule>0&&ask>lockRule&&/규칙을 따르세요/.test(p2)&&st==='준비/계약';"
     "return (ok?'✓':'✗')+' 먼저 골라진 칸='+mode+' · 더하기 요청='+blk(p1)+' · 고정 규칙 뒤 요청='+(ask>lockRule)+' · 결과 단계='+st")
step("정리", CLOSE + "app.exitFocusMode?.();await W(400);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.saveData();return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
