# AI 편집 「빠진 할 일 더하기」·「무엇을 할까요」 한 줄 세 칸 시험 대본 → steps3.json  (가짜 AI)
#   세 칸이 한 줄(왼쪽 업무팁·근거만 → 빠진 할 일 → 다시 정리) · 진행 중이면 「빠진 할 일 더하기」가 먼저 · 건너뛰기 칸 숨김 · [찾기 시작]
#   · 원래 줄은 회색(못 고름)·새 할 일만 초록(+ 새 할 일·까닭·+ 출처) · 이미 있는 일·엉뚱한 번호는 버림 · 끝난 단계에 들어가면 알림
#   · 넣기 → 원래 항목 그대로(체크·업무팁·번호) + 새 할 일은 그 자리에 · 끝난 단계는 다시 진행 중 · [되돌리기]
#   · 시작 전 업무는 「다시 정리」가 먼저 · 단계 오른쪽 클릭은 그 단계에만 · 좁은 화면이면 쌓임 · 찾은 것이 없으면 안내
# 실행: (tools 폴더에서) python mk_addmode_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json
ID = 7985
def js(o): return json.dumps(json.dumps(o, ensure_ascii=False), ensure_ascii=False)
ADDS = {"adds": [
    {"after": "o3", "text": "계약 보증금 받기", "why": "보충 자료 제22조의 보증금 절차가 빠짐", "src": "계약 시험 지침 제22조", "warn": ["계약 체결 전까지 받아야 함"]},
    {"after": "o5", "text": "계약 내용 공개", "why": "수의계약은 공개해야 함", "tip": "누리집에 올립니다"},
    {"after": "o1", "text": "구매 요청서 확인", "why": "요청 내용 확인이 빠짐"},
    {"after": "o4", "text": "견적서 받기", "why": "이미 있는 일(버려야 함)"},
    {"after": "o99", "text": "엉뚱한 번호", "why": "없는 번호(버려야 함)"}]}
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';const NL=String.fromCharCode(10);const M=()=>$('aiRsModal');"
     "const wf=()=>app.allData.workflows.find(w=>w.id===ID);const lines=()=>wf().checklist.map(x=>(x.indent?'└':'')+x.text+(app.normalizeCompleted(x)?'✓':'')).join(' / ');"
     "const cards=()=>[...M().querySelectorAll('.rs-mode')].map(c=>(c.classList.contains('on')?'●':'○')+tx(c.querySelector('b'))).join(' | ');"
     "const oneRow=()=>{const r=[...M().querySelectorAll('.rs-mode')].map(c=>Math.round(c.getBoundingClientRect().top));return r.length===3&&r.every(t=>t===r[0])};"
     "const rows=()=>[...M().querySelectorAll('.aip-list .aip-row')].map(r=>(r.classList.contains('fixed')?'':'[+]')+(r.classList.contains('sub')?'└':'')+tx(r.querySelector('.aip-text > span')||r.querySelector('.aip-text'))+(r.classList.contains('off')?'(안 고름)':'')+(r.querySelector('.aip-b.src')?'(출처)':'')+(r.querySelector('.aip-b.warn')?'(⚠)':'')).join(' / ');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(expr): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(b.width/2,30),b.top+b.height/2])" + E})
def click(expr): pt(expr); S.append({"clickpt": 1})
def rclick(expr): pt(expr); S.append({"rclickpt": 1})

STUB = ("window.__calls=[];window.__A=JSON.parse(" + js(ADDS) + ");window.__empty=false;"
        "const ai=async(p)=>{window.__calls.push(p);await W(250);if(/빠진 할 일만 찾아/.test(p))return JSON.stringify(window.__empty?{adds:[]}:window.__A);return JSON.stringify({items:[{text:'준비',indent:0,from:['o0']}],removed:[],branches:[]})};"
        "app.callAI=ai;app.callAIWithDocuments=ai;")
MK = ("const mk=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
      "const cl=[mk('준비',0),mk('품의서 작성',1),mk('예산 확인',1),mk('계약',0),mk('견적서 받기',1,'⚠ 기한 7일 안에 통지'),mk('계약서 작성',1),mk('검사',0),mk('검사조서 받기',1)];")
OPEN = "app.focusWorkflow(ID);await W(1300);app.enterFocusEditMode();await W(400);await app.openAiRestructure(ID);await W(700);"
CLOSE = ("app._aiRsClose?.();await W(200);if(app.focusEditMode){app.cancelFocusEditMode();await W(500);const d=[...document.querySelectorAll('.modal.show')].pop();const nb=d&&[...d.querySelectorAll('button')].find(b=>/저장 안 함/.test(b.textContent));if(nb)nb.click();await W(800);}"
         "")
LEAVE = "app.exitFocusMode?.();await W(600);"

step("준비: 진행 중 업무(준비 단계 끝냄) → 편집 → AI 편집 → 세 칸 한 줄·순서·먼저 골라진 것",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);" + MK +
     "cl[0].completed=true;cl[1].completed=true;cl[2].completed=true;cl.slice(0,3).forEach(x=>x.completedAt=new Date().toISOString());"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'물품 구매',checklist:cl,date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});window.__before=JSON.stringify(cl);app.saveData();" + OPEN +
     "return '한 줄='+oneRow()+' | '+cards()+' | 아래='+tx(M().querySelector('.rs-scale'))+' | 건너뛰기 칸='+[...M().querySelectorAll('.rs-chk')].some(x=>/건너뛰기/.test(x.textContent))+' | 단추='+tx([...M().querySelectorAll('#aiRsFoot .btn-primary')].pop())")
S.append({"shot": "addmode_setup.png"})
click("[...M().querySelectorAll('.rs-mode')][0]")
step("A2 「업무팁·근거만 보태기」 누름 → 건너뛰기 칸 보임·단추 「만들기 시작」", "await W(200);return cards()+' | 건너뛰기 칸='+[...M().querySelectorAll('.rs-chk')].some(x=>/건너뛰기/.test(x.textContent))+' | 단추='+tx([...M().querySelectorAll('#aiRsFoot .btn-primary')].pop())")
click("[...M().querySelectorAll('.rs-mode')][2]")
step("A3 오른쪽 칸 누름 → 「할 일 다듬기 🔒」·단추 「정리 시작」", "await W(200);return cards()+' | 단추='+tx([...M().querySelectorAll('#aiRsFoot .btn-primary')].pop())")
click("[...M().querySelectorAll('.rs-mode')][1]")
click("[...M().querySelectorAll('#aiRsFoot .btn-primary')].pop()")
step("B [찾기 시작] → 보낸 글(바꾸지 말라·after·adds) · 검토 화면", "for(let i=0;i<60&&!M().querySelector('.rs-locknote');i++)await W(100);await W(200);const p=window.__calls.at(-1);"
     "return '부른 수='+window.__calls.length+' | 규칙='+/원래 항목\\(이름·순서·단계\\/할 일·업무팁\\)은 하나도 바꾸지 말고/.test(p)+' after='+/after = 새 할 일 바로 앞에/.test(p)+' 끝냄 표시='+p.includes('o1 | 할 일 | 품의서 작성 (끝냄)')+' | 안내='+tx(M().querySelector('.rs-locknote'))+' | 끝난 단계 알림='+tx(M().querySelector('.rs-reopen'))")
step("B2 줄: 원래는 회색·새 할 일만 [+] 그 자리에 · 이미 있는 일·없는 번호는 버림", "return rows()+' || 회색 체크칸 막힘='+[...M().querySelectorAll('.aip-row.fixed input')].every(i=>i.disabled)+' | 새 할 일 표시='+M().querySelectorAll('.aip-b.new').length+' | 까닭='+tx(M().querySelector('.aip-why'))+' | 단추='+tx($('aiRsApplyBtn'))")
S.append({"shot": "addmode_review.png"})
click("[...M().querySelectorAll('.aip-row.add input')].find(i=>/구매 요청서/.test(i.closest('.aip-row').textContent))")
step("C 「구매 요청서 확인」 풀기 → 끝난 단계 알림 사라짐·단추 수", "await W(200);return '알림='+tx(M().querySelector('.rs-reopen'))+' | 단추='+tx($('aiRsApplyBtn'))")
step("C2 이름 두 번 눌러 고치기 → Enter", "const sp=[...M().querySelectorAll('.aip-row.add .aip-text > span')].find(s=>/계약 내용 공개/.test(s.textContent));sp.dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));await W(200);const inp=M().querySelector('.aip-ren');inp.value='수의계약 내용 공개';inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));await W(200);"
     "const f=M().querySelector('.aip-row.fixed');f.dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));await W(150);return rows()+' | 원래 줄 고치기 칸='+!!M().querySelector('.aip-ren')")
step("D0 넣기 직전 사진", "window.__before=JSON.stringify(wf().checklist);return 'ok'")
click("$('aiRsApplyBtn')")
step("D 넣기 → 원래 항목 그대로(번호·체크·업무팁) + 새 할 일 그 자리 · 출처는 근거로", "await W(700);const c=wf().checklist,b=JSON.parse(window.__before);const bad=[];b.forEach(o=>{const x=c.find(y=>y.itemId===o.itemId);if(!x){bad.push(o.text+':없음');return}const kx=JSON.stringify(x),ko=JSON.stringify(o);if(kx!==ko)bad.push(o.text+':'+Object.keys({...o,...x}).filter(k=>JSON.stringify(o[k])!==JSON.stringify(x[k])).join(','))});const same=bad.length?bad.join(';'):true;"
     "const g=c.find(x=>x.text==='계약 보증금 받기');return '창='+!!M()+' | 줄='+lines()+' || 원래 그대로='+same+' | 보증금 업무팁='+JSON.stringify(g&&g.tip&&g.tip.content)+' | 알림='+tx($('toastMessage')).slice(0,50)")
step("D2 [되돌리기] → 넣기 전으로", "const b=[...document.querySelectorAll('#toast button')].find(x=>/되돌리기/.test(x.textContent));b.click();await W(500);return '줄='+lines()+' | 전과 같음='+(JSON.stringify(wf().checklist)===window.__before)")
step("E 끝난 단계에 넣으면 그 단계는 다시 진행 중", "await app.openAiRestructure(ID);await W(300);await app._aiRsStart();for(let i=0;i<40&&app._aiRs.phase!=='review';i++)await W(100);app._aiRsApply();await W(600);return '줄='+lines()")
step("E2 정리 → 편집 취소", CLOSE + "return '편집='+app.focusEditMode+' | 줄='+lines()")
rclick("document.querySelector('.checklist-card[data-workflow-id=\"'+ID+'\"][data-index=\"3\"] .item-title-text')")
click("[...document.querySelectorAll('#checklistItemMenu button[data-i]')].find(b=>/이 단계 할 일 채우기/.test(b.textContent))")
step("F 단계 오른쪽 클릭 → 「다시 정리(이 단계)」가 먼저 · 세 칸", "for(let i=0;i<40&&!M();i++)await W(100);await W(500);return cards()")
click("[...M().querySelectorAll('.rs-mode')][1]")
click("[...M().querySelectorAll('#aiRsFoot .btn-primary')].pop()")
step("F2 「계약」 단계에서 빠진 할 일 → 다른 단계 것은 버림", "for(let i=0;i<60&&!M().querySelector('.rs-locknote');i++)await W(100);await W(200);return '보낸 글 이 단계만='+window.__calls.at(-1).includes('after에는 「계약」 단계와')+' | '+rows().split(' / ').filter(x=>x.startsWith('[+]')).join(' / ')")
step("F3 찾은 것이 없으면 안내", "window.__empty=true;await app._aiRsStart();for(let i=0;i<40&&app._aiRs.phase!=='review';i++)await W(100);await W(200);const r=tx(M().querySelector('.rs-empty'))+' | 넣기 막힘='+$('aiRsApplyBtn').disabled;window.__empty=false;return r")
step("F4 정리", CLOSE + LEAVE + "return '편집='+app.focusEditMode")
step("G 시작 전 업무 → 「체크리스트 다시 정리」가 먼저", "wf().checklist.forEach(x=>{x.completed=false;x.completedAt=null});app.saveData();" + OPEN + "return cards()")
S.append({"viewport": [460, 900]})
step("H 좁은 창(460px) → 세 칸이 쌓임", "await W(400);return '한 줄='+oneRow()+' | 칸 너비='+[...M().querySelectorAll('.rs-mode')].map(c=>Math.round(c.getBoundingClientRect().width)).join(',')")
S.append({"viewport": [1440, 900]})
step("정리", CLOSE + LEAVE + "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app._allowMassDelete=true;app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(S), 'steps')
