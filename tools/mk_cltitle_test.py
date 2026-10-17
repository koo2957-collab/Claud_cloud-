# 진행상황 출력: 체크리스트 탭이 먼저 · 체크리스트/점검표 제목 고치기(업무마다 기억, 인쇄·복사에도) 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_cltitle_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===8961);const M=()=>document.getElementById('progressReportModal');const T=()=>document.querySelector('#prPage .pr-ed[data-k^=clTitle]');"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "app._collabSetMe({dept:'사하소방서 감사팀',rank:'소방위',name:'홍길동',phone:'4521'});app._prTab=null;"
     "const cl=[['접수',0],['사건 배당',1],['조사',0],['문답서 작성',1],['종결',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:8961,type:'manual',title:'감찰조사',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(8961);await W(1200);return 'ok'")
pt("const b=[...document.querySelectorAll('[onclick^=\"app.openProgressReport(8961\"]')].find(x=>x.getClientRects().length&&x.getBoundingClientRect().width);const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("A 처음 열면 체크리스트 탭이 먼저", "await W(900);const tabs=[...M().querySelectorAll('.pr-tabs [data-tab]')];return '탭 순서='+tabs.map(b=>b.textContent).join(',')+' | 열린 탭='+tabs.find(b=>b.classList.contains('on'))?.textContent+' | 제목='+T()?.textContent")
S.append({"shot": "clt_a.png"})
pt("const r=T().getBoundingClientRect();return JSON.stringify([r.right-4,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 100})
S.append({"key": "End", "vk": 35})
S.append({"text": " (2차 점검)"})
S.append({"key": "Enter", "vk": 13})
step("B 제목을 눌러 고치고 Enter → 저장", "await W(600);return '보이는 제목='+T().textContent+' | 저장='+app._prSaved(wf()).clTitle+' | 초점 빠짐='+(document.activeElement!==T())")
step("C 인쇄 창 제목(PDF 파일 이름)도 고친 제목", "const pw=async(id)=>{window.__lastPW=null;const o0=window.open;window.open=function(){const w=o0.apply(window,arguments);window.__lastPW=w;return w;};app._prPrint(id);window.open=o0;await W(900);const w=window.__lastPW;const f=document.getElementById('prPrintFrame');return w?{doc:w.document,html:w.document.documentElement.outerHTML,done:()=>w.close(),via:'작은 창'}:f?{doc:f.contentDocument,html:f.srcdoc,done:()=>f.remove(),via:'숨은 틀'}:null;};const P=await pw(8961);const t=P&&P.doc.title;const h=P&&P.doc.body.innerHTML;P&&P.done();return '인쇄 제목='+t+' | 인쇄 본문에 고치는 칸 없음='+!/contenteditable/.test(h||'')")
step("D 한글 붙여넣기용 복사에도 고친 제목", "const h=app._checklistFlatHtml(wf(),app._prOpts());return '복사 본문에 제목='+h.includes('감찰조사 체크리스트 (2차 점검)')+' | 고치는 칸 없음='+!/contenteditable/.test(h)")
step("E 빈 점검표는 따로(기본 제목)", "M().querySelector('[data-opt=clBlank]').click();await W(600);return '점검표 제목='+T().textContent+' 키='+T().dataset.k")
step("E2 점검표로 돌아왔다 다시 진행표 → 고친 제목 그대로", "M().querySelector('[data-opt=clBlank]').click();await W(600);return T().textContent")
step("F 닫고 다시 열면 고친 제목 그대로 · 마지막에 본 탭", "app.closeProgressReport();await W(300);app.openProgressReport(8961);await W(800);return '탭='+M().querySelector('.pr-tabs .on').textContent+' | 제목='+T().textContent")
pt("const r=T().getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("G 제목을 모두 지우고 나가면 처음 제목으로", "const t=T();const s=getSelection();const r=document.createRange();r.selectNodeContents(t);s.removeAllRanges();s.addRange(r);document.execCommand('delete');await W(200);t.blur();await W(600);return '보이는 제목='+T().textContent+' | 저장='+JSON.stringify(app._prSaved(wf()).clTitle)")
step("H Esc는 제목 칸만 끝내고 창은 그대로", "T().focus();await W(200);document.activeElement.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}));await W(500);return '창 열림='+!!M()")
step("I 진행상황 보고 탭은 그대로 동작", "M().querySelector('.pr-tabs [data-tab=report]').click();await W(800);return '보고서 쪽='+document.querySelectorAll('#prPage .pr-pg').length+' 고치는 줄='+document.querySelectorAll('#prPage .pr-ed[contenteditable=true]').length")
step("정리", "app.closeProgressReport();app._prTab=null;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==8961);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
