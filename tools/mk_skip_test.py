import json
P = "(async()=>{try{"
seed = ("window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown','autoStartPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
 "const cl=[['징계 의결 요구',0],['감찰 결과 보고서 접수',1],['징계의결요구서 작성',1],['심의·의결',0],['징계 의결서 수령',1],['징계 처분',0],['처분사유설명서 작성',1],['처분사유설명서 교부',1],['종결',0],['종결 보고',1]].map(([t,i])=>({text:t,indent:i,completed:false}));"
 "app.allData.workflows.unshift({id:7001,type:'manual',title:'건너뛰기 테스트',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();app.displayWorkflows();await new Promise(r=>setTimeout(r,500));"
 "app.focusWorkflow(7001);await new Promise(r=>setTimeout(r,900));app.enterFocusEditMode();await new Promise(r=>setTimeout(r,800));document.querySelectorAll('.toast').forEach(t=>t.remove());return 'seeded'")
state = ("const wf=app.allData.workflows.find(w=>w.id===7001);const m=document.getElementById('checklistItemMenu');const fb=document.getElementById('fbCtxMenu');"
 "const modal=document.getElementById('cimOverlay');const a=document.activeElement;const toast=[...document.querySelectorAll('.toast')].map(t=>t.textContent.trim().slice(0,50)).join(' / ');document.querySelectorAll('.toast').forEach(t=>t.remove());"
 "return JSON.stringify({"
 "rows:wf.checklist.map(x=>(app._isSubEntry(x)?'└':'')+(x.text||'(빈줄)')+((x.branchOptions||[]).length?'['+x.branchOptions.map(o=>o.label+':'+app.resolveBranchTargets(wf,o).items.map(t=>t.item?t.item.text:t.id).length).join(',')+']':'')).join(' | '),"
 "pick:app._branchPick?{label:app._branchPick.label,n:app._branchPick.selected.size}:null,"
 "edit:!!app.focusEditMode,"
 "menu:m&&m.isConnected?m.innerText.replace(/\\s+/g,' ').trim():null,"
 "ctx:fb&&fb.style.display!=='none'?fb.innerText.replace(/\\s+/g,' ').trim():null,"
 "modal:modal?(modal.innerText.includes('건너뛰기')?'모달(건너뛰기 탭 있음)':'모달'):null,"
 "active:a&&a.className?a.className.split(' ')[0]+(a.value!==undefined?'='+a.value:''):'',"
 "toast})")
POS = ("const card=t=>[...document.querySelectorAll('.checklist-card')].find(c=>{const e=c.querySelector('.fci-title-text,.bp-title');return e&&e.textContent.trim()===t});"
       "const ctr=r=>JSON.stringify([Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]);")
def pt(js): return {"label": "pt", "js": "(()=>{" + POS + js + "})()", "pt": True}
def row(t, frac=0.7): return pt(f"card('{t}').scrollIntoView({{block:'center'}});const r=card('{t}').querySelector('.checklist-card-header').getBoundingClientRect();return JSON.stringify([Math.round(r.left+r.width*{frac}),Math.round(r.top+r.height/2)])")
def txt(t): return pt(f"card('{t}').scrollIntoView({{block:'center'}});const r=card('{t}').querySelector('.fci-title-text').getBoundingClientRect();return JSON.stringify([Math.round(r.left+12),Math.round(r.top+r.height/2)])")
def btn(c): return pt(f"return ctr(document.querySelector('.fci-bar [data-cmd=\"{c}\"]').getBoundingClientRect())")
def pill(t): return pt(f"card('{t}').scrollIntoView({{block:'center'}});return ctr(card('{t}').querySelector('.fci-mark-branch').getBoundingClientRect())")
def menuitem(sel, txt_): return pt(f"const it=[...document.querySelectorAll('{sel}')].find(e=>e.textContent.includes('{txt_}'));return ctr(it.getBoundingClientRect())")
def empty(): return pt("const r=document.querySelector('[id^=focus-checklist-scroll-]').getBoundingClientRect();return JSON.stringify([Math.round(r.left+r.width/2),Math.round(r.bottom-30)])")
CLICK = lambda n=1: {"clickpt": n}
RCLICK = {"rclickpt": 1}
def chk(l): return {"label": l, "js": P + state + "}catch(e){return 'ERR '+e.message}})()"}
def key(k, vk=0, shift=False): return {"key": k, "vk": vk, "shift": shift}
def text(t): return {"text": t}
W = lambda ms: {"wait": ms}
S = [{"label": "seed", "js": P + seed + "}catch(e){return 'ERR '+e.message}})()"}]
S += [
 # T1 버튼 없는 줄에서 명령 줄 [건너뛰기] → 바로 고르기 모드 (모달 없음)
 row('징계 의결서 수령'), CLICK(), btn('skip'), CLICK(), chk('T1 명령 줄 건너뛰기 → 고르기 모드'), {"shot": "s_t1.png"},
 # T2 고르기 모드: 앞쪽 줄은 못 고름 / 단계 고르면 할 일까지 / 이름 없이 Enter → 안내
 row('감찰 결과 보고서 접수'), CLICK(), chk('T2a 기준 앞 줄 클릭 → 변화 없음'),
 row('징계 처분'), CLICK(), chk('T2b 단계 클릭 → 할 일까지 3개'),
 key('Enter', 13), chk('T2c 이름 없이 Enter → 안내, 모드 유지'),
 pt("const e=document.getElementById('bpLabel').getBoundingClientRect();return ctr(e)"), CLICK(), text('불문·경고 의결'),
 key('Enter', 13), chk('T2d 이름 쓰고 Enter → 저장'), {"shot": "s_t2.png"},
 # T3 버튼 있는 줄에서 [건너뛰기] → 작은 메뉴 → 새 버튼 → Esc 취소
 row('징계 의결서 수령'), CLICK(), btn('skip'), CLICK(), chk('T3a 버튼 있는 줄 → 작은 메뉴'), {"shot": "s_t3.png"},
 menuitem('#checklistItemMenu *', '새 건너뛰기 버튼'), CLICK(), chk('T3b 새 버튼 → 고르기 모드'),
 key('Escape', 27), chk('T3c Esc → 취소, 편집 모드 유지'),
 # T4 알약 클릭 → 메뉴 → 기존 버튼 고치기 (선택 유지 3개) → 하나 풀고 저장
 pill('징계 의결서 수령'), CLICK(), chk('T4a 알약 → 메뉴(건너뛰기만)'),
 menuitem('#checklistItemMenu *', '불문·경고 의결'), CLICK(), chk('T4b 기존 버튼 고치기 → 3개 선택된 채'),
 row('처분사유설명서 교부'), CLICK(), key('Enter', 13), chk('T4c 하나 풀고 저장 → 2개'),
 # T5 오른쪽 클릭 메뉴: 명령 줄과 같은 순서
 row('종결 보고'), RCLICK, chk('T5a 오른쪽 클릭 메뉴 항목'), {"shot": "s_t5.png"},
 menuitem('#fbCtxMenu .wfm-ctx-item', '건너뛰기'), CLICK(), chk('T5b 메뉴 건너뛰기(버튼 없는 줄) → 고르기 모드'), key('Escape', 27),
 row('징계 의결서 수령'), RCLICK, menuitem('#fbCtxMenu .wfm-ctx-item', '건너뛰기'), CLICK(), chk('T5c 메뉴 건너뛰기(버튼 있는 줄) → 작은 메뉴'), key('Escape', 27),
 # T6 오른쪽 클릭 ＋ 할 일 → 빈 줄 → 빈 곳 클릭 → 빈 줄 자동 삭제
 row('심의·의결'), RCLICK, menuitem('#fbCtxMenu .wfm-ctx-item', '＋ 할 일'), CLICK(), chk('T6a ＋할 일 → 빈 줄에 커서'),
 empty(), CLICK(), W(400), chk('T6b 빈 곳 클릭 → 빈 줄 사라짐'),
 # T7 ＋ 단계 → 이름 쓰고 Enter → 다음 빈 줄 → 빈 곳 클릭 → 이름 있는 줄만 남음
 row('종결'), CLICK(), btn('addStage'), CLICK(), text('결과 통보'), key('Enter', 13), chk('T7a 이름 쓰고 Enter → 다음 빈 줄'),
 empty(), CLICK(), W(400), chk('T7b 빈 곳 클릭 → 「결과 통보」만 남음'),
 # T8 빈 줄이 있을 때 다른 줄 두 번 클릭 → 빈 줄 지워지고 이름 고치기 유지
 row('징계 의결 요구'), CLICK(), btn('addSub'), CLICK(), txt('종결 보고'), CLICK(2), W(400), chk('T8 빈 줄 + 다른 줄 두 번 클릭 → 이름 고치기 유지'),
 text(' 작성'), key('Enter', 13), W(200), empty(), CLICK(), W(400), chk('T8b 이어서 입력 반영'),
 # T9 할 일이 딸린 단계 이름을 지워도 단계는 남음
 txt('심의·의결'), CLICK(2), pt("return '[0,0]'"), {"label": "clear", "js": "(()=>{const e=document.activeElement;e.value='';return e.className})()"}, empty(), CLICK(), W(400), chk('T9 할 일 딸린 단계 이름 비움 → 남음'),
 # T10 명령 줄 단축 동작: 한 번 클릭 고르기 → ↑ / 삭제
 row('결과 통보'), CLICK(), btn('up'), CLICK(), chk('T10a ↑'),
 btn('del'), CLICK(), chk('T10b 삭제'),
 # T11 편집 중 항목 창에는 건너뛰기 탭 없음
 {"label": "T11", "js": P + "app.showChecklistItemModal(7001,4,'branch');await new Promise(r=>setTimeout(r,600));const tabs=[...document.querySelectorAll('#cimOverlay .cim-tab')].map(t=>t.textContent.trim());app.closeChecklistItemModal();return 'tabs: '+tabs.join(', ')" + "}catch(e){return 'ERR '+e.message}})()"},
 # T12 저장 → 일하는 화면에서 건너뛰기 버튼 동작
 {"label": "T12", "js": P + "document.querySelector('[onclick*=\"saveFocusEdit\"], [onclick*=\"exitFocusEditMode\"]')?.click();await new Promise(r=>setTimeout(r,900));const b=[...document.querySelectorAll('button')].find(x=>x.textContent.includes('불문·경고'));return 'edit='+!!app.focusEditMode+' 버튼='+(b?b.textContent.trim():'없음')" + "}catch(e){return 'ERR '+e.message}})()"},
 {"shot": "s_t12.png"},
]
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
