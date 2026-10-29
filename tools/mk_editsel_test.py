# 고른 줄 모양 통일 시험 → steps3.json (연습 업무, 실제 마우스): 체크리스트 편집 · 일하는 화면 체크리스트 · 서식·문서함 표 · 메인 목록형
# 모두 「옅은 파랑 바탕 + 얇은 파랑 선(1px)」 하나 (--sel-bg · --sel-line)
# 확인: 편집 고른 줄 = 파란 바탕(올려 둔 줄보다 진함) + 얇은 선 · 마우스를 다른 줄로 옮겨도 남음 · 올려 둔 줄은 옅은 색 그대로
#       · 명령 줄 「n줄 고름」(단계를 고르면 할 일까지 셈) · Ctrl 클릭 여러 줄 · 줄 밖을 누르면 풀림·숫자 숨김(자리는 그대로)
#       · 고른 뒤 [삭제]·[건너뛰기]가 켜짐
# 실행: (tools 폴더에서) python mk_editsel_test.py && node cdp3.mjs "<저장소>/index.html"
import json
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);"
     "const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';"
     "const a=c=>{const m=getComputedStyle(c).backgroundColor.match(/[\\d.]+/g)||[];return m.length>3?+m[3]:(m.length?1:0)};"
     "const ln=el=>{const c=getComputedStyle(el);return /inset/.test(c.boxShadow)&&/0px 0px 0px 1px/.test(c.boxShadow)?'얇은 선':(c.outlineStyle!=='none'&&c.outlineWidth==='1px'?'얇은 선':'없음')};"
     "const look=i=>{const c=$('fci-'+i);return '#'+i+'(고름='+c.classList.contains('fci-selected')+' 바탕='+a(c).toFixed(3)+' 선='+ln(c)+')'};"
     "const bar=()=>{const b=document.querySelector('.fci-bar');const c=b.querySelector('.fci-bar-count');return '숫자='+(c&&getComputedStyle(c).visibility==='visible'?tx(c):'안 보임')+' 켜진 명령='+[...b.querySelectorAll('button[data-need]')].filter(x=>!x.disabled).map(x=>x.textContent.trim()).join(',')+' 막대 높이='+b.offsetHeight};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def at(sel, act="clickpt", mods=None):
    S.append({"pt": True, "js": P + "const b=" + sel + ";b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+Math.min(30,r.width/2),r.y+r.height/2])" + E})
    S.append({act: 1, **({"mods": mods} if mods else {})})  # cdp3 click은 mods(Ctrl=2·Shift=8)를 받음
step("준비: 연습 업무 → 체크리스트 편집",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     "await app.insertPracticeWorkflows();await W(800);document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const w=app.allData.workflows.find(w=>/소모품/.test(w.title));window.__w=w.id;app.focusWorkflow(w.id);await W(1500);app.enterFocusEditMode();await W(800);"
     "return '고르기 전: '+bar()")
at("document.querySelector('#fci-2 .fci-title-text')")
step("A 할 일 글자 한 번 클릭 → 고른 표시", "await W(300);return look(2)+' | '+bar()")
at("document.querySelector('#fci-4 .fci-title-text')", "hoverpt")
step("B 마우스를 다른 줄로 옮김 → 고른 줄은 그대로, 올려 둔 줄은 옅게", "return look(2)+' | 올려 둔 '+look(4)")
S.append({"shot": "editsel_one.png"})
at("document.querySelector('#fci-0 .fci-mark-c')")
step("C 단계 번호 클릭 → 단계 + 그 할 일까지, 숫자 「5줄 고름」", "await W(300);return look(0)+' '+look(1)+' '+look(4)+' | '+bar()")
at("document.querySelector('#fci-7 .fci-title-text')", "clickpt", 2)  # mods 2 = Ctrl
step("D Ctrl 클릭으로 하나 더", "await W(300);return look(0)+' '+look(7)+' | '+bar()")
S.append({"shot": "editsel_multi.png"})
S.append({"pt": True, "js": P + "const b=document.querySelector('.fci-bar');const d=b.querySelector('.fci-bar-del').getBoundingClientRect(),c=b.querySelector('.fci-bar-count').getBoundingClientRect();return JSON.stringify([(d.right+c.left)/2,d.y+d.height/2])" + E}); S.append({"clickpt": 1})  # 삭제 단추와 숫자 사이 빈 곳
step("E 명령 줄 빈 곳 누름 → 고른 것 그대로(명령 줄은 풀지 않음)", "await W(300);return bar()")
at("document.querySelector('.focus-left-panel, .fm-left, #focusLeft')||document.querySelector('.main-layout')")
step("F 줄 밖을 누름 → 풀림·숫자 숨김·명령 줄 높이 그대로", "await W(300);return look(0)+' '+look(7)+' | '+bar()")
step("G 일하는 화면: 할 일 한 번 클릭 → 같은 모양(처리결과 칸까지 한 상자)",
     "app.cancelFocusEditMode?.();await W(600);return '편집 끝'")
at("[...document.querySelectorAll('[id^=focus-checklist-scroll-] .checklist-card.sub-item .item-title-text')][2]")
at("[...document.querySelectorAll('[id^=focus-checklist-scroll-] .checklist-card.sub-item .item-title-text')][0]", "hoverpt")
step("G2 마우스를 다른 줄로 → 고른 줄 그대로", "await W(300);const c=document.querySelector('[id^=focus-checklist-scroll-] .checklist-card:has(> .cl-peek)');const o=document.querySelector('[id^=focus-checklist-scroll-] .checklist-card.sub-item');return '고른 줄=' +tx(c?.querySelector('.item-title-text'))+' 바탕='+a(c).toFixed(3)+' 선='+ln(c)+' | 올려 둔 줄 바탕='+a(o).toFixed(3)+' 선='+ln(o)")
S.append({"shot": "editsel_work.png"})
step("H 서식·문서함 표: 한 번 클릭", "app.exitFocusMode?.();await W(500);app.openDocumentRepo();await W(900);return 'ok'")
at("[...document.querySelectorAll('.modal.show .wfm-table tbody tr')].find(r=>r.offsetParent)")
step("H2 고른 표 줄", "await W(300);const r=document.querySelector('.modal.show .wfm-table tbody tr.wfm-row-selected');return '바탕='+a(r).toFixed(3)+' 선='+ln(r)")
S.append({"shot": "editsel_table.png"})
step("I 메인 목록형: 한 번 클릭", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.setViewMode('list');await W(600);return 'ok'")
at("document.querySelector('.wf-row')")
step("I2 고른 목록 줄", "await W(300);const r=document.querySelector('.wf-row.is-selected');return '바탕='+a(r).toFixed(3)+' 선='+ln(r)")
step("정리", "app.setViewMode('card');app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));await app.saveDataImmediate();return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(S), '단계')
