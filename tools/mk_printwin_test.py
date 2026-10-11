# 인쇄는 작은 별도 창에서 — 진행상황 출력 [인쇄 · PDF] · 팝업이 막혔을 때 · 다른 새 창 크기 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_printwin_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===8971);const M=()=>document.getElementById('progressReportModal');"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
# 새 창을 기록 (실제 window.open 그대로 부르고 돌려받은 창과 크기 설정만 적어 둠)
SPY = "if(!window.__owo){window.__owo=window.open;window.open=function(){const w=window.__owo.apply(window,arguments);window.__pw=w;window.__pwArgs=[...arguments];return w;};}"

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "app._collabSetMe({dept:'사하소방서 감사팀',rank:'소방위',name:'홍길동',phone:'4521'});app._prTab=null;" + SPY +
     "const cl=[['접수',0],['사건 배당',1],['조사',0],['문답서 작성',1],['종결',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:8971,type:'manual',title:'인쇄 창 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(8971);await W(1200);app.openProgressReport(8971);await W(900);return 'ok'")
pt("const b=[...M().querySelectorAll('button')].find(x=>x.textContent.trim()==='인쇄 · PDF');const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("A [인쇄 · PDF] → 작은 별도 창", "await W(1200);const w=window.__pw;if(!w)return '창 없음';const d=w.document;return '창 설정='+window.__pwArgs[2]+' | 제목='+d.title+' | 단추='+[...d.querySelectorAll('.pw-b')].map(b=>b.textContent).join(',')+' | A4 쪽='+d.querySelectorAll('.pr-pg').length+' | 프로그램 숨은 인쇄틀='+!!document.getElementById('prPrintFrame')+' | 프로그램 창 그대로='+!!M()")
step("B 인쇄용 모양: 위 단추 줄은 인쇄에 안 나옴", "const d=window.__pw.document;const css=[...d.styleSheets].flatMap(s=>[...s.cssRules]).map(r=>r.cssText).join(' ');return '인쇄때 단추줄 숨김='+/@media print[^}]*\\.pw-bar\\s*\\{\\s*display:\\s*none/.test(css)+' | 용지='+(/size: A4 portrait/.test(css)?'A4 세로':css.match(/size:[^;]+/)?.[0])")
step("C [닫기] → 인쇄 창만 닫히고 프로그램은 그대로", "window.__pw.document.getElementById('pwClose').click();await W(500);return '인쇄 창 닫힘='+window.__pw.closed+' | 프로그램 출력 창='+!!M()+' | 업무='+!!wf()")
step("D0 가로로 바꿈", "window.__pw=null;M().querySelector('[data-land=\"1\"]').click();await W(500);return 'ok'")
pt("const b=[...M().querySelectorAll('button')].find(x=>x.textContent.trim()==='인쇄 · PDF');const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("D 가로 체크리스트는 넓은 창 · 가로 용지", "await W(1000);const w=window.__pw;if(!w)return '창 없음';const css=[...w.document.styleSheets].flatMap(s=>[...s.cssRules]).map(r=>r.cssText).join(' ');const r='창 너비='+window.__pwArgs[2].match(/width=(\\d+)/)[1]+' | 용지='+(/landscape/.test(css)?'가로':'세로');M().querySelector('[data-land=\"0\"]').click();await W(300);w.close();return r")
step("E0", "window.__pw=null;await W(300);return 'ok'")
pt("const b=[...M().querySelectorAll('button')].find(x=>x.textContent.trim()==='인쇄 · PDF');const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("E Esc → 인쇄 창 닫힘", "await W(1000);const w=window.__pw;if(!w)return '창 없음';w.document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));await W(400);return '닫힘='+w.closed")
step("F 팝업이 막히면 알리고 예전처럼 이 화면에서 인쇄", "const keep=window.open;window.open=()=>null;app._prPrint(8971);await W(800);window.open=keep;const t=[...document.querySelectorAll('.toast')].map(x=>x.textContent).join(' ');const f=document.getElementById('prPrintFrame');const r='알림='+/팝업이 막혀/.test(t)+' | 숨은 인쇄틀='+!!f;f&&f.remove();return r")
step("G0 보고서 탭", "M().querySelector('.pr-tabs [data-tab=report]').click();await W(700);window.__pw=null;return 'ok'")
pt("const b=[...M().querySelectorAll('button')].find(x=>x.textContent.trim()==='인쇄 · PDF');const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("G 보고서 탭 인쇄도 같은 작은 창", "await W(1000);const w=window.__pw;const r=w?('제목='+w.document.title+' | 쪽='+w.document.querySelectorAll('.pr-pg').length+' | 고치는 칸 흔적='+w.document.querySelectorAll('[contenteditable=true]').length+' (false 표시만='+w.document.querySelectorAll('[contenteditable=false]').length+')'):'창 없음';w&&w.close();return r")
step("정리", "window.open=window.__owo;delete window.__owo;app.closeProgressReport();app._prTab=null;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==8971);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
