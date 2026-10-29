import json
# 업무 관리 메뉴 조사: ① 아래쪽 줄의 메뉴가 화면 밖으로 잘림 ② ⋯ 더보기 메뉴가 뜬 채 오른쪽 클릭하면 메뉴가 두 개 → steps_wfmmenu.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
H = ("const rows=()=>[...document.querySelectorAll('#workflowManagerModal tbody tr')].filter(x=>x.offsetParent&&!/f:/.test(x.getAttribute('oncontextmenu')||''));"
     "const menus=()=>[...document.querySelectorAll('#wfmCtxMenu, #fbCtxMenu')].filter(m=>m.style.display!=='none'&&m.getClientRects().length).map(m=>{const r=m.getBoundingClientRect();return m.id+'[위 '+Math.round(r.top)+' 아래 '+Math.round(r.bottom)+' / 화면 '+innerHeight+(r.bottom>innerHeight?' → '+Math.round(r.bottom-innerHeight)+'px 잘림':'')+' · 항목 '+m.querySelectorAll('.wfm-ctx-item').length+']'});"
     "const mid=el=>{const r=el.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])};")
S = []
def step(label, body): S.append({"label": label, "js": P + H + body + E})
def pt(body): S.append({"pt": True, "js": P + H + body + E})

S.append({"viewport": [1366, 768]})
step("준비 (연습 업무 여러 번 넣어 줄 늘리기)", "localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));for(let k=0;k<6;k++){app.insertPracticeWorkflows();await W(1800);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));}app.openWorkflowManager();await W(900);const m=document.getElementById('wfmCtxMenu');let p=m.parentElement,chain=[];while(p&&p!==document.body){const cs=getComputedStyle(p);if(cs.transform!=='none'||cs.overflow!=='visible'||cs.contain!=='none')chain.push((p.id||p.className).toString().slice(0,30)+'(transform='+cs.transform.slice(0,12)+',overflow='+cs.overflow+')');p=p.parentElement}return '줄 수='+rows().length+' | 메뉴 위치 부모='+(chain.join(' > ')||'body 바로 아래')")
# ① 맨 아래 보이는 줄 오른쪽 클릭
pt("const rs=rows().filter(r=>r.getBoundingClientRect().bottom<innerHeight-10);const r=rs[rs.length-1];r.scrollIntoView({block:'nearest'});return mid(r)")
S.append({"clickpt": 1})
S.append({"rclickpt": 1})
step("A1 맨 아래 줄 오른쪽 클릭(하나)", "await W(300);return menus().join(' | ')")
S.append({"shot": "wm_a1.png"})
step("A1b 닫기", "document.body.click();await W(200);return menus().join(' | ')||'메뉴 없음'")
# ⋯ 줄 버튼(아래 줄) — 마우스를 올려야 보이는 단추라 먼저 올림
LAST = "const rs=rows().filter(r=>r.getBoundingClientRect().bottom<innerHeight-10&&r.getBoundingClientRect().bottom<document.querySelector('#workflowManagerModal .wfm-table-wrap').getBoundingClientRect().bottom);"
pt(LAST + "return mid(rs[rs.length-1])"); S.append({"hoverpt": 1})
pt(LAST + "const b=rs[rs.length-1].querySelector('.wfm-row-action-btn');return b?mid(b):'ERR ⋯ 없음'")
S.append({"clickpt": 1})
step("A2 맨 아래 줄 ⋯ 버튼", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
step("A2b 닫기", "document.body.click();await W(200);return menus().join(' | ')||'메뉴 없음'")
# 여러 개 고르고 맨 아래 줄 오른쪽 클릭
pt(LAST + "return mid(rs[rs.length-2])"); S.append({"clickpt": 1})
pt(LAST + "return mid(rs[rs.length-1])"); S.append({"clickpt": 1, "mods": 2})
pt(LAST + "return mid(rs[rs.length-1])"); S.append({"rclickpt": 1})
step("A3 두 개 고른 채 맨 아래 줄 오른쪽 클릭(묶음 메뉴)", "await W(300);return '고른 수 '+app._selAdapter('wfm').set.size+' · 보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
S.append({"shot": "wm_a3.png"})
step("A3b Esc로 닫기", "document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));await W(200);return (menus().join(' | ')||'메뉴 없음')+' · 업무 관리 열림='+document.getElementById('workflowManagerModal').classList.contains('show')")
# ② 메뉴 두 개: 메뉴를 띄운 채 오른쪽 클릭 (오른쪽 클릭은 click이 아니라 다른 메뉴를 닫지 않음)
TOP = "document.querySelector('#workflowManagerModal .wfm-table')?.closest('[style*=overflow],.wfm-table-wrap,.wfm-main')?.scrollTo?.(0,0);[...document.querySelectorAll('#workflowManagerModal *')].forEach(x=>{if(x.scrollTop)x.scrollTop=0});"
def pick2():
    step("고르기 풀기", "document.body.click();" + TOP + "app._selAdapter('wfm').set.clear();app.renderWorkflowTree();await W(300);return 'ok'")
    pt("return mid(rows()[0])"); S.append({"clickpt": 1})
    pt("return mid(rows()[1])"); S.append({"clickpt": 1, "mods": 2})
    step("고른 수", "await W(200);return app._selAdapter('wfm').set.size+'개 고름 · 메뉴 '+menus().length")
pick2()
pt("const b=[...document.querySelectorAll('#workflowManagerModal .ab-more')].find(x=>x.getClientRects().length);return b?mid(b):'ERR 더보기 없음'")
S.append({"clickpt": 1})
step("B1 두 개 고르고 명령 줄 ⋯ 더보기", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
pt("return mid(rows()[0])"); S.append({"rclickpt": 1})
step("B2 메뉴 둔 채 고른 줄 오른쪽 클릭", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
pt("return mid(rows()[4])"); S.append({"rclickpt": 1})
step("B3 메뉴 둔 채 고르지 않은 줄 오른쪽 클릭", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
S.append({"shot": "wm_b3.png"})
pick2()
pt("const b=rows()[1].querySelector('.wfm-row-action-btn');return b?mid(b):'ERR 줄 ⋯ 없음'")
S.append({"clickpt": 1})
step("C1 두 개 고르고 고른 줄의 ⋯ 버튼", "await W(300);return '고른 수 '+app._selAdapter('wfm').set.size+' · 보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
pt("return mid(rows()[0])"); S.append({"rclickpt": 1})
step("C2 그 메뉴 둔 채 고른 줄 오른쪽 클릭", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
S.append({"shot": "wm_c2.png"})
pick2()
pt("return mid(rows()[0])"); S.append({"rclickpt": 1})
step("D1 두 개 고르고 오른쪽 클릭(묶음 메뉴)", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
pt("return mid(rows()[1].querySelector('.wfm-row-action-btn')||rows()[1])"); S.append({"rclickpt": 1})
step("D2 그 메뉴 둔 채 다른 고른 줄 오른쪽 클릭", "await W(300);return '보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
pt("return mid(rows()[6])"); S.append({"rclickpt": 1})
step("D3 그 메뉴 둔 채 고르지 않은 줄 오른쪽 클릭", "await W(300);return '고른 수 '+app._selAdapter('wfm').set.size+' · 보이는 메뉴 '+menus().length+'개: '+menus().join(' | ')")
S.append({"shot": "wm_d3.png"})
step("정리", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return 'ok'")
json.dump(S, open('steps_wfmmenu.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
