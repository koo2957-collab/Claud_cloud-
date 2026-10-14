# AI로 다시 정리 시험 대본 → steps3.json  (AI 허용판 `ai_test .html`로 실행, 가짜 AI)
# 옛날식 업무(모두 단계) → 업무 화면 왼쪽 [AI로 다시 정리] → 참고 자료 PDF·보안 안내 → [정리 시작](진행·취소) → 원래↔새 비교(유지·수정·이동·추가,
# 빠진 원래 항목 다시 넣기, AI가 뺀 항목) → 건너뛰기 후보 → [고른 것을 사본에 넣기] → 사본: 단계/할 일·업무팁 세 칸·서식 따라옴·건너뛰기 버튼·원본 그대로 →
# [되돌리기]로 사본 지움 · 목록 오른쪽 클릭 메뉴
# 실행: (tools 폴더에서) python mk_rs_test.py && node cdp3.mjs "<저장소>/ai_test .html"
#       배포판: python mk_rs_test.py locked && node cdp3.mjs <저장소>/index.html
import json, os, sys
ANS = {"items": [
    {"text": "접수", "indent": 0, "from": ["o0"], "change": "수정", "note": "이름을 짧게", "warn": [], "tip": "접수 대장에 적습니다", "basis": []},
    {"text": "출석요구서 발송 (회의 5일 전)", "indent": 1, "from": ["o1"], "change": "이동", "note": "접수 단계의 할 일로", "warn": ["회의 5일 전까지 도달"], "tip": "", "basis": ["공무원 징계령 제10조 (4쪽)"]},
    {"text": "진술 기회 부여", "indent": 1, "from": ["o2", "o6"], "change": "수정", "note": "진술서 받기와 중복 항목을 합침", "warn": [], "tip": "", "basis": []},
    {"text": "진술 영상 녹화", "indent": 1, "from": [], "change": "추가", "note": "규정상 필요", "warn": [], "tip": "", "basis": []},
    {"text": "징계 의결", "indent": 0, "from": ["o3"], "change": "유지", "note": "", "warn": [], "tip": "", "basis": []},
    {"text": "처분 통보", "indent": 1, "from": ["o4", "없는번호"], "change": "이동", "note": "", "warn": [], "tip": "", "basis": []}],
    "removed": [], "branches": [{"at": 2, "label": "진술 포기", "skip": [3]}]}
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7801;"
     "const orig=()=>app.allData.workflows.find(w=>w.id===ID);const copy=()=>app.allData.workflows.find(w=>/\\(AI 정리본\\)/.test(w.title||'')&&!w.isDraft);"
     "const toast=()=>{const t=$('toast');return t&&t.classList.contains('show')?$('toastMessage').textContent.trim():'(알림 없음)'};"
     "const pdf=n=>new File([new Blob(['%PDF-1.4\\n1 0 obj<<>>endobj\\ntrailer<<>>\\n%%EOF'],{type:'application/pdf'})],n,{type:'application/pdf'});")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음');el.scrollIntoView({block:'nearest'});await W(150);const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(14,b.width/2),b.top+b.height/2])")})
def click(expr): pt(expr); S.append({"clickpt": 1})
a = json.dumps(ANS, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
STUB = lambda ms: "window.__calls=[];app.callAIWithDocuments=app.callAI=async(p,f)=>{window.__calls.push({p,f:Array.isArray(f)?f.map(x=>x.name):[]});await new Promise(r=>setTimeout(r," + str(ms) + "));return '" + a + "'};"
SETUP = ("document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
         "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&!/AI 정리본/.test(w.title||''));"
         "const cl=[['사건 접수','접수 대장에 적기'],['출석요구서 발송',''],['진술서 받기',''],['징계위원회 개최',''],['처분 통보',''],['사건 종결 보고',''],['중복 항목','']].map(([t,tip])=>({text:t,indent:0,completed:false,...(tip?{tip:{type:'text',content:tip,saved:true}}:{})}));"
         "cl[1].linkedDocs=[11];cl[0].completed=true;"
         "app.allData.workflows.unshift({id:ID,type:'manual',title:'징계 처분 절차',checklist:cl,date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});cl.forEach(it=>app.ensureChecklistItemId(it));window.__ids=cl.map(it=>it.itemId);await app.saveDataImmediate();")

if len(sys.argv) > 1 and sys.argv[1] == 'locked':
    step("배포판: 왼쪽 단추 흐림 · 목록 메뉴에 없음", SETUP + "app.focusWorkflow(ID);await W(1200);const b=[...document.querySelectorAll('.fap-btn')].find(x=>x.textContent.includes('AI로 다시 정리'));const r='단추 흐림(ai-off)='+document.body.classList.contains('ai-off')+' 단추 있음='+!!b;app.exitFocusMode();await W(800);return r")
    pt("document.querySelector('[data-sel-key=\"7801\"]')")
    S.append({"rclickpt": 1})
    step("목록 오른쪽 클릭", "await W(200);const m=document.querySelector('.mini-menu, .ctx-menu, #miniMenu');return '메뉴에 AI로 다시 정리='+!!(m&&m.textContent.includes('AI로 다시 정리'))")
else:
    step("준비: 옛날식 업무(모두 단계 7줄) + 참고 자료 PDF", SETUP + "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();await app.addRefFilesToWorkflow(ID,[pdf('공무원 징계령.pdf')]);await W(500);app.focusWorkflow(ID);await W(1500);return '줄='+orig().checklist.length+' | 참고 자료='+((app.checklistDetails['project-'+ID]||{}).linkedLibraryDocs||[]).length")
    click("[...document.querySelectorAll('.fap-btn')].find(x=>x.textContent.includes('AI로 다시 정리'))")
    step("A 창 열림: 보안 안내·참고 자료 PDF·함께 만들 것", "await W(600);const m=$('aiRsModal');return '창='+!!m+' | 제목='+m.querySelector('h3').textContent+' | 보안='+m.querySelector('.aif-secure').textContent.slice(0,40)+' | PDF='+[...m.querySelectorAll('.rs-sec')[0].querySelectorAll('label')].map(l=>l.textContent.trim()+(l.querySelector('input').checked?'☑':'☐')).join(',')+' | 사본 이름 안내='+m.textContent.includes('(AI 정리본)')")
    S.append({"shot": "rs_setup.png"})
    step("B0 가짜 AI(2초)", STUB(2000) + "return 'ok'")
    click("[...document.querySelectorAll('#aiRsFoot button')].find(b=>b.textContent.includes('정리 시작'))")
    step("B 정리 중: 진행 줄·[취소]", "await W(900);const s=$('aiRsStatus');return '진행='+(s&&!s.hidden?s.textContent.replace(/\\s+/g,' ').trim().slice(0,40):'없음')")
    step("C 비교 화면", "await W(2000);const m=$('aiRsModal');const cols=m.querySelectorAll('.rs-col');const old=[...cols[0].querySelectorAll('.rs-old')].map(r=>r.querySelector('span').textContent+r.querySelector('.rs-to').textContent);const nw=[...cols[1].querySelectorAll('.aip-row')].map(r=>(r.classList.contains('sub')?'└':'')+r.querySelector('.aip-text').textContent+'['+r.querySelector('.rs-ch').textContent+']');const lost=[...m.querySelectorAll('.rs-lost .aip-row')].map(r=>r.textContent.replace(/\\s+/g,' ').trim()+(r.querySelector('input').checked?'☑':'☐'));"
         "return '원래='+old.join(' / ')+' || 새='+nw.join(' / ')+' || 머리='+cols[1].querySelector('.rs-col-h span').textContent+' || 없는 원래 항목='+lost.join(' / ')+' || 보낸 PDF='+window.__calls[0].f.join(',')+' || 요청 글에 원래 업무팁='+window.__calls[0].p.includes('접수 대장에 적기')")
    S.append({"shot": "rs_review.png"})
    click("document.querySelectorAll('#aiRsModal .aip-list')[2].querySelector('input')")
    step("D 건너뛰기 후보 고름", "await W(150);return '후보='+document.querySelectorAll('#aiRsModal .aip-list')[2].querySelector('input').checked+' | 넣기 단추='+$('aiRsApplyBtn').textContent")
    click("$('aiRsApplyBtn')")
    step("E 사본에 넣기 → 사본 열림", "await W(3000);const c=copy(),o=orig();const L=c?c.checklist:[];const tipOf=t=>{const x=L.find(i=>i.text===t);return x&&x.tip?x.tip.content.replace(/\\n/g,'⏎'):''};const br=L.find(i=>i.text==='진술 기회 부여');"
         "return '사본='+(c?c.title:'없음')+' | 열린 업무='+(app.focusedWorkflowId===(c&&c.id))+' | 줄='+L.map(i=>(i.indent?'└':'')+i.text).join(' / ')+' | 출석요구서 업무팁='+tipOf('출석요구서 발송 (회의 5일 전)')+' | 서식 따라옴='+JSON.stringify((L.find(i=>i.text.startsWith('출석요구서'))||{}).linkedDocs)+' 같은 번호='+((L.find(i=>i.text.startsWith('출석요구서'))||{}).itemId===window.__ids[1])+' | 건너뛰기='+(br&&br.branchOptions?br.branchOptions.map(b=>b.label+'→'+b.targetItemIds.map(id=>L.find(i=>i.itemId===id).text)).join(''):'없음')+' | 체크 모두 풀림='+L.every(i=>!i.completed)+' | 원본 그대로='+(o.checklist.length===7&&o.checklist[0].text==='사건 접수'&&o.checklist[0].completed===true)+' | 알림='+toast().slice(0,60)")
    S.append({"shot": "rs_copy.png"})
    click("document.querySelector('#toastMessage .toast-undo-btn')")
    step("F [되돌리기] → 사본 지움, 원본 그대로", "await W(1200);return '사본='+!!copy()+' | 원본='+!!orig()+' | 알림='+toast()")
    step("G 취소: 정리 중에 [취소]", "app.focusWorkflow(ID);await W(1200);" + STUB(4000) + "await app.openAiRestructure(ID);await W(300);app._aiRsStart();await W(800);app._aiRsCancel();await W(300);const a='화면='+(document.querySelector('#aiRsModal .rs-cols')?'비교':'설정')+' | 알림='+toast().slice(0,16);await W(4200);return a+' | 4초 뒤에도 설정 화면='+!document.querySelector('#aiRsModal .rs-cols')")
    step("H 닫기 · 목록 오른쪽 클릭 메뉴", "app._aiRsClose();app.exitFocusMode();await W(900);return 'ok'")
    pt("document.querySelector('[data-sel-key=\"7801\"]')")
    S.append({"rclickpt": 1})
    step("H2 메뉴에 「AI로 다시 정리」", "await W(200);const m=[...document.querySelectorAll('body > div')].reverse().find(d=>d.textContent.includes('폴더로 옮기기'));return '있음='+!!(m&&m.textContent.includes('AI로 다시 정리'))")
    step("I 다크 모드", "document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));document.documentElement.classList.add('dark-mode');" + STUB(100) + "await app.openAiRestructure(ID);await W(300);await app._aiRsStart();await W(400);return 'ok'")
    S.append({"shot": "rs_dark.png"})
    step("정리", "app._aiRsClose();document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&!/AI 정리본/.test(w.title||''));app._allowMassDelete=true;await app.saveDataImmediate();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
