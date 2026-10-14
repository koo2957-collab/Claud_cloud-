# 일하는 화면 체크리스트 줄 표시(한 줄 · 「1/2」 숫자 · 마우스를 올리면 버튼 줄) 시험 대본 → steps3.json
# 실행: python tools/mk_row_test.py && node tools/cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7301);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(body): return P + body + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
# 줄 찾기: 제목으로 카드 헤더를 찾고, 그 안의 요소 가운데 좌표를 돌려준다
ROW = "const row=t=>[...document.querySelectorAll('[id^=\"focus-checklist-scroll-\"] .checklist-card')].find(c=>c.querySelector('.item-title-text')?.textContent.trim().startsWith(t));"
def pt(title, sel=".checklist-card-header", dx=None):
    x = f"b.left+{dx}" if dx is not None else "b.left+b.width/2"
    S.append({"pt": True, "js": J(ROW + f"const el=row('{title}').querySelector('{sel}');const b=el.getBoundingClientRect();return JSON.stringify([{x},b.top+b.height/2])")})

# 날짜는 브라우저(그 컴퓨터 시간대) 기준으로 만든다
step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const ds=n=>{const d=new Date();d.setDate(d.getDate()+n);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};"
     "const cl=[['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0],['징계 의결서 수령',1],['처분 결과 통보와 인사기록 반영',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7301,type:'manual',title:'줄 표시 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "wf().checklist[2].tip={type:'text',content:'출석통지서는 회의 3일 전까지 도달',saved:true};wf().checklist[3].formats=[{name:'의결서 수령 확인서.hwp'}];wf().checklist[2].deadline=ds(3);wf().checklist[5].deadline=ds(10);"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7301);await W(900);app.toggleChecklistItem(7301,1);await W(1500);return 'ok'")
step("A 평소 줄 모양", ROW + "const r=t=>{const c=row(t);if(!c)return t+' 못찾음 '+window.__t.join('|');return t+' | 숫자='+(c.querySelector('.stage-num')?.textContent||'-')+' 날짜='+(c.querySelector('.cl-dl-face')?.innerText.trim()||'(없음)')+' 점='+(c.querySelector('.cl-has-dot')?'•':'-')+' 빈📅='+!!c.querySelector('.cl-dl-face svg')+' 막대='+!!c.querySelector('.stage-bar')+' 높이='+Math.round(c.querySelector('.checklist-card-header').getBoundingClientRect().height)};"
     "window.__t=[...document.querySelectorAll('.checklist-card .item-title-text')].map(x=>x.textContent.trim().slice(0,12));return ['징계위원회','위원 구성','출석통지서','심의·의결','처분 결과'].map(r).join(' || ')")
S.append({"shot": "row_a.png"})
pt("출석통지서", ".item-title-text", 20)
S.append({"hoverpt": True})
step("B 마우스를 올린 줄", ROW + "const c=row('출석통지서');const bar=c.querySelector('.cl-hbar');const v=getComputedStyle(bar).display+'/'+getComputedStyle(bar).visibility;const face=getComputedStyle(c.querySelector('.cl-dl-face')).visibility;"
     "return 'bar='+v+' 날짜자리='+face+' 버튼='+[...bar.querySelectorAll('.cl-hb')].map(b=>(b.querySelector('svg')?'[그림]':'[글자]')+b.textContent.trim()+'('+getComputedStyle(b).color+')').join(' ')+' 이모지남음='+/[💡📄📅✨⋯]/u.test(bar.textContent)+' | 다른줄 bar='+getComputedStyle(row('처분 결과').querySelector('.cl-hbar')).visibility")
S.append({"shot": "row_b.png"})
pt("출석통지서", ".cl-hb.tip")
S.append({"clickpt": 1, "wait": 100})
step("C 💡 누르면 업무팁 탭", "await W(700);const t=document.querySelector('.cim-tab-active');return 'modal='+!!document.getElementById('cimOverlay')+' 탭='+(t?.textContent.trim()||'?')+' 펼침안됨='+!document.querySelector('.cl-peek')")
step("C2 닫기", "app.closeChecklistItemModal();await W(500);return 'ok'")
pt("징계위원회", ".stage-num")
S.append({"clickpt": 1})
step("D 「1/2」 누르면 접기", ROW + "await W(500);return '숫자='+row('징계위원회').querySelector('.stage-num').textContent+' folded='+row('징계위원회').querySelector('.stage-num').classList.contains('folded')+' 할일보임='+!!row('위원 구성')")
S.append({"shot": "row_d.png"})
pt("징계위원회", ".stage-num")
S.append({"clickpt": 1})
step("D2 다시 펼치기", ROW + "await W(500);return '할일보임='+!!row('위원 구성')")
pt("처분 결과", ".item-title-text", 20)
S.append({"hoverpt": True})
pt("처분 결과", ".cl-hb-more")
S.append({"clickpt": 1})
step("E ⋯ 메뉴 (오른쪽 클릭과 같은 목록)", "await W(300);const m=document.getElementById('checklistItemMenu');return m?[...m.querySelectorAll('button')].map(b=>(b.querySelector('svg')?'[그림]':'')+b.textContent.trim()).join(' / ')+' 이모지남음='+/[💡📄📅✨📝]/u.test(m.textContent):'메뉴 없음'")
S.append({"shot": "row_e.png"})
S.append({"key": "Escape", "vk": 27})
pt("처분 결과", ".item-title-text", 20)
S.append({"rclickpt": True})
step("E2 오른쪽 클릭 메뉴", "const m=document.getElementById('checklistItemMenu');const r=m?[...m.querySelectorAll('button')].map(b=>b.textContent.trim()).join(' / '):'메뉴 없음';app._closeChecklistItemMenu();return r")
pt("처분 결과", ".item-title-text", 20)
S.append({"hoverpt": True})
pt("처분 결과", ".cl-hb.dl")
S.append({"clickpt": 1})
step("F 📅 누르면 날짜 입력칸", ROW + "await W(300);return '오류 없음 · 입력칸='+!!document.getElementById('dl-input-7301-5')+' 값='+document.getElementById('dl-input-7301-5')?.value")
S.append({"key": "Escape", "vk": 27})
step("G 할 일을 다 끝내면 단계 숫자 초록", ROW + "app.toggleChecklistItem(7301,2);await W(1200);return '단계 숫자='+row('징계위원회').querySelector('.stage-num').textContent+' done='+row('징계위원회').querySelector('.stage-num').classList.contains('done')")
S.append({"shot": "row_g.png"})
step("H 긴 제목: 한 줄 유지, 버튼 줄이 제목 끝을 가림", ROW + "wf().checklist[5].text='처분 결과 통보와 인사기록 반영 — 징계 처분 사유 설명서 교부, 인사혁신처 공무원 인사기록 시스템 입력, 감사 부서 통보까지 모두 끝내기';app.saveData();app.focusWorkflow(7301);await W(1200);const t=row('처분 결과').querySelector('.item-title-text');const h=row('처분 결과').querySelector('.checklist-card-header').getBoundingClientRect().height;return '헤더 높이='+Math.round(h)+' 말줄임='+(t.scrollWidth>t.clientWidth)+' 전체제목 말풍선='+(t.title.length>40)")
pt("처분 결과", ".item-title-text", 20)
S.append({"hoverpt": True})
S.append({"shot": "row_h.png"})
pt("처분 결과", ".item-title-text", 20)
S.append({"clickpt": 1})
step("H2 눌러서 펼치면 제목 전체", ROW + "await W(600);const h=row('처분 결과').querySelector('.checklist-card-header').getBoundingClientRect().height;return '펼침='+!!row('처분 결과').querySelector('.cl-peek')+' 헤더 높이='+Math.round(h)")
S.append({"shot": "row_h2.png"})
step("I 레퍼런스(본보기): 📅 없음 · ⋯ 있음(보기 메뉴), 숫자 「n개」", ROW + "wf().isReference=true;app.saveData();app.focusWorkflow(7301);await W(1200);const c=row('징계위원회');return '숫자='+(c.querySelector('.stage-badge')?.textContent)+' 버튼 수='+row('출석통지서').querySelectorAll('.cl-hb').length+' ⋯있음='+!!row('출석통지서').querySelector('.cl-hb-more')+' 📅있음='+!!row('출석통지서').querySelector('.cl-hb.dl, .cl-hb[title*=마감일]')")
step("정리", "wf().isReference=false;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7301);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
