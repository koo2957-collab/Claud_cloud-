# 업무 절차 패널 넓게 보기 시험 대본 → steps3.json
# ⤢ 단추·패널 머리 두 번 누르기로 넓게 ↔ 보통, 왼쪽은 아이콘 줄(56)·패널 564·가운데 너비 그대로, 패널 글자 10% 크게,
# 아이콘 줄 명령(진행상황 출력·체크리스트 편집 → 저장/취소), 다시 열어도 기억, 일하는 화면 밖에서는 단추 없음, 패널 고른 줄 스크롤
# 실행: (tools 폴더에서) python mk_wide_test.py [1366x768] && node cdp3.mjs <index.html 경로>
import json, os, sys
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>/소모품/.test(w.title)&&/^\\[연습\\]/.test(w.title));"
     "const wd=id=>{const e=document.getElementById(id);return e?Math.round(e.getBoundingClientRect().width):0};"
     "const center=()=>Math.round(document.querySelector('.main-content').getBoundingClientRect().width);"
     "const rowX=()=>{const r=document.querySelector('.checklist-card[data-workflow-id=\"'+wf().id+'\"] .item-title-text');return r?Math.round(r.getBoundingClientRect().left):-1};"
     "const D=()=>document.getElementById('aiPanelOfflineDashboard');const wide=()=>document.body.classList.contains('proc-wide');"
     "const st=()=>'넓게='+wide()+' 왼쪽='+wd('focusActionPanel')+' 패널='+wd('aiPanel')+' 가운데='+center()+' 줄시작x='+rowX();")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr, dx="b.width/2"): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음');const b=el.getBoundingClientRect();return JSON.stringify([b.left+" + dx + ",b.top+b.height/2])")})
def click(expr, n=1): pt(expr); S.append({"clickpt": n})

if len(sys.argv) > 1:
    w, h = map(int, sys.argv[1].split('x'))
    S.append({"viewport": [w, h]})

step("준비", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');localStorage.setItem('procWide','0');localStorage.setItem('authorInfoSet','1');app._collabSetMe({dept:'행정과',rank:'소방위',name:'홍길동',phone:'1234'});app._applyProcWide(false);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));await app.insertPracticeWorkflows();await W(1500);app.focusWorkflow(wf().id);await W(1500);window.__c0=center();window.__x0=rowX();return st()")
step("A 보통: ⤢ 단추", "const b=document.getElementById('aiPanelWideBtn');return '단추 보임='+(b&&getComputedStyle(b).display!=='none')+' | 말풍선='+b.title")
S.append({"shot": "wide_a.png"})
click("document.getElementById('aiPanelWideBtn')")
step("B ⤢ 누름 → 넓게", "await W(700);const z=getComputedStyle(D().firstElementChild).zoom;return st()+' | 가운데 같음='+(center()===window.__c0)+' 줄 높이 그대로·왼쪽으로 옮겨 감='+(window.__x0-rowX())+'px'+' | 패널 글자 배율='+z+' | 아이콘 줄='+[...document.querySelectorAll('.fap-rail .fap-rail-btn')].map(b=>b.title).join(',')+' | 진행률='+document.querySelector('.fap-rail-pct').textContent+' | 왼쪽 원래 내용 숨김='+(getComputedStyle(document.querySelector('.fap-title')).display==='none')+' | 단추 말풍선='+document.getElementById('aiPanelWideBtn').title.slice(0,10)")
S.append({"shot": "wide_b.png"})
# 아이콘 줄 명령
click("[...document.querySelectorAll('.fap-rail-btn')].find(b=>b.title==='진행상황 출력')")
step("C1 아이콘 줄 「진행상황 출력」", "await W(900);const r='출력 창='+!!document.getElementById('progressReportModal');app.closeProgressReport&&app.closeProgressReport();await W(400);return r")
click("[...document.querySelectorAll('.fap-rail-btn')].find(b=>b.title==='체크리스트 편집')")
step("C2 아이콘 줄 「체크리스트 편집」 → 저장·취소 아이콘", "await W(900);return '편집 모드='+!!app.focusEditMode+' | 아이콘 줄='+[...document.querySelectorAll('.fap-rail .fap-rail-btn')].map(b=>b.title).join(',')+' | 넓게 유지='+wide()")
click("[...document.querySelectorAll('.fap-rail-btn')].find(b=>b.title==='편집 취소')")
step("C3 「편집 취소」 → 일하는 화면", "await W(900);return '편집 모드='+!!app.focusEditMode+' | '+st()")
# 패널에서 고른 줄이 보이는지 (글자 키운 뒤 스크롤 계산)
click("[...document.querySelectorAll('.checklist-card[data-workflow-id=\"'+wf().id+'\"]')].filter(c=>!c.classList.contains('skipped')).slice(-1)[0].querySelector('.item-title-text')")
step("D 가운데 줄 한 번 누름 → 패널에서 그 항목이 보임", "await W(900);const p=D().querySelector('.is-picked');const r=p?p.getBoundingClientRect():null,dr=D().getBoundingClientRect();return '고른 줄='+!!p+' | 패널 안에 보임='+(r?(r.top>=dr.top-1&&r.top<dr.bottom):false)")
S.append({"key": "Escape"})
# 머리 두 번 누르기
step("E0 머리 위치", "return 'ok'")
pt("document.querySelector('.ai-panel-header .ai-panel-title')")
S.append({"clickpt": 2})
step("E 패널 머리 두 번 누름 → 보통", "await W(700);return st()+' | 가운데 같음='+(center()===window.__c0)")
click("document.getElementById('aiPanelWideBtn')")
step("E2 단추 한 번 → 다시 넓게", "await W(700);return st()")
step("F 다시 열어도 기억", "location.reload();return 'ok'")
step("F2", "await W(3500);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.focusWorkflow(wf().id);await W(1500);return st()+' | 저장값='+localStorage.getItem('procWide')")
step("G 일하는 화면 밖", "app.focusCloseOneLevel?app.focusCloseOneLevel():app.exitFocusMode();await W(1200);const b=document.getElementById('aiPanelWideBtn');return '일하는 화면='+document.body.classList.contains('focus-mode')+' | 단추 보임='+(b&&getComputedStyle(b).display!=='none'&&b.offsetParent!==null)+' | 왼쪽 메뉴='+wd('sidebar')")
step("H 다크 모드", "app.focusWorkflow(wf().id);await W(1500);document.documentElement.classList.add('dark-mode');await W(300);return st()")
S.append({"shot": "wide_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app.toggleProcWide(false);app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
