import json
# 예시 순서 · 처리결과 이름 · AI 버튼 흐리게 · 진행상황 출력(보고서) 시험 → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===8901);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
tf = "const tfn=()=>[...document.querySelectorAll('#cimOverlay .tf-box .rf-row')].map(r=>r.querySelector('.tf-n')?.textContent+'.'+r.querySelector('.rf-name').textContent.trim().slice(0,10)).join(' / ');"
step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};const ago=n=>new Date(Date.now()-n*864e5).toISOString();"
     "const cl=[{text:'징계 의결 요구',indent:0,completed:true,completedAt:ago(9),result:{text:'의결요구서 제출(징계위원회)'}},"
     "{text:'징계위원회 개최 준비',indent:0,completed:false},{text:'위원 구성·회의 일정 확정',indent:1,completed:true,completedAt:ago(2),result:{text:'위원 5명 구성\\n10.23. 14:00 소회의실'}},{text:'출석통지서 발송',indent:1,completed:true,completedAt:ago(5),result:{text:'등기우편 발송, 수령 확인'}},{text:'진술권 포기서 확인',indent:1,completed:false,deadline:D(3)},"
     "{text:'심의·의결',indent:0,completed:false,deadline:D(12)},{text:'재심사 청구 안내',indent:0,completed:false,skipped:true,skipReason:'청구 없음'},{text:'징계 처분',indent:0,completed:false}];"
     "app.allData.workflows.unshift({id:8901,type:'manual',title:'소방장 품위유지의무 위반 징계처분',checklist:cl,date:'2026. 10. 1.',createdAt:ago(10),deadline:D(19),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "await app.addResultFiles(8901,3,{files:[new File(['%PDF-1.4 x'],'출석통지서_발송본.pdf',{type:'application/pdf'}),new File(['x'],'등기 수령증.jpg',{type:'image/jpeg'})],value:''});"
     "const mk=async(t,c)=>{const cv=document.createElement('canvas');cv.width=300;cv.height=200;const g=cv.getContext('2d');g.fillStyle=c;g.fillRect(0,0,300,200);return new File([await new Promise(r=>cv.toBlob(r,'image/png'))],t,{type:'image/png'})};"
     # 숫자로 시작하는 이름을 거꾸로 골라도 1·2·3 순
     "await app.addTipFiles(8901,3,{files:[await mk('3. 수령증.png','#d97706'),await mk('1. 발송 화면.png','#2563eb'),await mk('2. 등기 영수증.png','#059669')],value:''},{silent:true,noShrink:true});"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(8901);await W(1500);return '예시 순서='+app._tipFiles(8901,wf().checklist[3].itemId).map(f=>f.name).join(', ')")
step("① 항목 창 예시 줄: 번호", tf + "await app.showChecklistItemModal(8901,3,'tip');await W(800);return tfn()")
S.append({"shot": "rp_tf1.png"})
step("① 끌기 준비", "const rows=[...document.querySelectorAll('#cimOverlay .tf-box .rf-row')];const dt=new DataTransfer();rows[2].dispatchEvent(new DragEvent('dragstart',{bubbles:true,dataTransfer:dt}));rows[0].dispatchEvent(new DragEvent('dragover',{bubbles:true,cancelable:true,dataTransfer:dt}));rows[0].dispatchEvent(new DragEvent('drop',{bubbles:true,cancelable:true,dataTransfer:dt}));return 'ok'")
step("① 3번째를 맨 위로 끌어 놓기", tf + "await W(800);return tfn()+' | 저장 순서='+app._tipFiles(8901,wf().checklist[3].itemId).map(f=>f.name.slice(0,4)).join(',')")
step("① 오른쪽 클릭 「↓ 아래로」", tf + "const r=document.querySelectorAll('#cimOverlay .tf-box .rf-row')[0];const b=r.getBoundingClientRect();r.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:b.left+100,clientY:b.top+10}));await W(400);const items=[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')];const t=items.map(x=>x.textContent.trim()).join(' / ');items.find(x=>/아래로/.test(x.textContent)).click();await W(800);return '메뉴=['+t+'] → '+tfn()")
step("① 미리보기 넘기는 순서도 같음", "await app.previewTipFile(8901,3,0);await W(800);const m=[...document.querySelectorAll('.modal.show')].reverse().find(x=>x.querySelector('.pv-nav'));const a=m.querySelector('h2').textContent;await app._tfNav(1);await W(500);const b=m.querySelector('h2').textContent;m.querySelector('.close-preview-modal').click();await W(400);return '1번='+a+' → 2번='+b")
step("② 「처리결과」 이름", "await app.showChecklistItemModal(8901,3,'result');await W(700);const tabs=[...document.querySelectorAll('#cimOverlay .cim-tab')].map(t=>t.textContent.trim()).join(',');const h=[...document.querySelectorAll('#cimOverlay .mat-title')].map(t=>t.textContent.trim().slice(0,8)).join(',');app.closeChecklistItemModal();await W(300);return '탭='+tabs+' | 제목='+h+' | 화면에 남은 「조치결과」='+(document.body.innerText.match(/조치결과/g)||[]).length")
# ③ AI
step("③ AI 버튼 흐리게", "const b=document.querySelector('.fap-btn.ai-only');const cs=getComputedStyle(b);return 'ai-off='+document.body.classList.contains('ai-off')+' | AI 기안 흐림='+cs.opacity+' 커서='+cs.cursor")
pt("const b=document.querySelector('.fap-btn.ai-only').getBoundingClientRect();return JSON.stringify([b.left+b.width/2,b.top+b.height/2])")
S.append({"hoverpt": True, "clickpt": 1, "wait": 100})
step("③ AI 기안 실제로 누름 → 아무것도 안 열림", "await W(700);const b=document.querySelector('.fap-btn.ai-only');return '열린 창='+[...document.querySelectorAll('.modal.show')].map(m=>m.id).join(',')+' | 알림='+([...document.querySelectorAll('.toast')].map(t=>t.textContent.trim().slice(0,30)).pop()||'없음')+' | 말풍선='+b.getAttribute('title')")
S.append({"shot": "rp_ai.png"})
step("③ 문서 관리 메뉴 「보고서 작성」 흐림", "document.querySelector('[onclick*=toolsMenu]').click();await W(400);const mi=[...document.querySelectorAll('#toolsMenu .mi')];const r=mi.map(x=>x.textContent.trim().slice(0,6)+'('+getComputedStyle(x).opacity+')').join(' / ');mi.find(x=>/보고서 작성/.test(x.textContent)).click();await W(500);const open=!!document.querySelector('#reportModal.show');app.closeAllDropdowns&&app.closeAllDropdowns();return r+' | 눌러서 열림='+open")
S.append({"shot": "rp_menu.png"})
# ④ 진행상황 출력
pt("document.body.click();await W(200);const b=[...document.querySelectorAll('.fap-btn')].find(x=>/진행상황 출력/.test(x.textContent)).getBoundingClientRect();return JSON.stringify([b.left+b.width/2,b.top+b.height/2])")
S.append({"clickpt": 1, "wait": 100})
doc = "const doc=()=>[...document.querySelectorAll('#prPage .pr-doc')].map(d=>d.innerText).join(String.fromCharCode(10)).replace(/\\n+/g,' ¶ ');"
step("④ 처음 누르면 작성자 정보 창부터", "await W(600);const m=document.getElementById('authorInfoModal');return '작성자 창='+!!m+' | 보고서 창='+!!document.getElementById('progressReportModal')")
S.append({"shot": "rp_author.png"})
step("④ 소속·직급·이름 적고 [저장하고 계속]", "const m=document.getElementById('authorInfoModal');m.querySelector('#authorDepartment').value='사하소방서 감사팀';m.querySelector('#authorRank').value='소방위';m.querySelector('#authorName').value='홍길동';m.querySelector('[data-ok]').click();await W(700);return '보고서 창='+!!document.getElementById('progressReportModal')+' | 저장='+localStorage.getItem('pdfAuthorInfo')")
step("④ 보고서 내용(단계는 한 번, 할 일은 아래 -)", doc + "document.querySelector('.pr-tabs [data-tab=report]')?.click();await W(700);return doc()")
S.append({"shot": "rp_report.png"})
pt("const t=document.querySelector('.pr-ed[data-k=title]').getBoundingClientRect();return JSON.stringify([t.right-60,t.top+t.height/2])")
S.append({"clickpt": 1, "wait": 100})
S.append({"key": "End", "vk": 35})
S.append({"text": " (제2차)"})
S.append({"key": "Enter", "vk": 13})
pt("const o=document.querySelector('.pr-ed[data-k=op]');const bd=o.closest('.pr-body');bd.scrollTop+=o.getBoundingClientRect().top-bd.getBoundingClientRect().top-200;await W(300);const t=o.getBoundingClientRect();return JSON.stringify([t.left+40,t.top+t.height/2])")
S.append({"clickpt": 1, "wait": 100})
S.append({"text": "출석 일정 조정 요청이 있어 협의 중입니다."})
step("④ 제목·의견 실제로 입력 → 업무별로 기억", "await W(900);const s=app._prSaved(wf()).edits||{};return '저장 제목='+s.title+' | 의견='+s.op")
step("④ 「할 일까지」 끄기 → 단계만", doc + "const c=document.querySelector('[data-opt=subs]');c.click();await W(500);const r=doc();c.click();await W(400);return r")
step("④ 「해당 없음 항목」 켜기", doc + "const c=document.querySelector('[data-opt=skipped]');c.click();await W(500);const r=doc().match(/재심사[^¶]*/)?.[0]||'없음';c.click();await W(300);return r")
step("④ 복사 (한글에 붙여넣기용)", "window.__clip=null;navigator.clipboard.write=async items=>{const it=items[0];window.__clip={types:it.types,html:await (await it.getType('text/html')).text(),text:await (await it.getType('text/plain')).text()}};await app._prCopy(8901);await W(300);const c=window.__clip;return c?'형식='+c.types.join(',')+' | 글 앞부분: '+c.text.split('\\n').slice(0,4).join(' / ')+' | 편집 표시 없음='+!/contenteditable/.test(c.html)+' | 의견 들어감='+/협의 중/.test(c.html):'복사 안 됨'")
step("④ 인쇄·PDF (작은 인쇄 창, 막히면 숨은 틀)", "const pw=async(id)=>{window.__lastPW=null;const o0=window.open;window.open=function(){const w=o0.apply(window,arguments);window.__lastPW=w;return w;};app._prPrint(id);window.open=o0;await W(900);const w=window.__lastPW;const f=document.getElementById('prPrintFrame');return w?{doc:w.document,html:w.document.documentElement.outerHTML,done:()=>w.close(),via:'작은 창'}:f?{doc:f.contentDocument,html:f.srcdoc,done:()=>f.remove(),via:'숨은 틀'}:null;};const P=await pw(8901);const r='A4 인쇄용 문서='+(!!P&&/@page\\{size:A4/.test(P.html))+' | 제목='+(P?P.doc.title:'-')+' | 방식='+(P&&P.via);P&&P.done();return r")
step("④ 닫고 다시 열면 고친 제목·의견 그대로", doc + "app.closeProgressReport();await W(300);app.openProgressReport(8901);await W(600);return doc().slice(0,60)+' … 의견 있음='+/협의 중/.test(doc())")
step("④ 다시 열면 작성자 창 없이 바로", "app.closeProgressReport();await W(300);app.openProgressReport(8901);await W(600);return '작성자 창='+!!document.getElementById('authorInfoModal')+' | 보고서 창='+!!document.getElementById('progressReportModal')")
step("④ [작성자 ✎]로 고치기", "document.querySelector('.pr-author').click();await W(400);const m=document.getElementById('authorInfoModal');m.querySelector('#authorRank').value='소방경';m.querySelector('[data-ok]').click();await W(500);return '단추 글='+document.querySelector('.pr-author').textContent.trim()+' | 보고서 위쪽='+[...document.querySelectorAll('#prPage .pr-doc')].map(d=>d.innerText).join(String.fromCharCode(10)).split(String.fromCharCode(10))[1]")
step("④ 체크리스트 탭(진행표)", "window.__opens=0;const wo=window.open;window.open=function(){window.__opens++;return null};document.querySelector('.pr-tabs [data-tab=checklist]').click();await W(500);const rows=[...document.querySelectorAll('#prPage tbody tr')].map(r=>[...r.children].slice(0,4).map(c=>c.innerText.trim()).join('|'));return '머리='+[...document.querySelectorAll('#prPage thead th')].map(t=>t.textContent).join(',')+' | '+rows.slice(0,5).join(' / ')")
S.append({"shot": "rp_cl.png"})
step("④ 빈 점검표", "document.querySelector('[data-opt=clBlank]').click();await W(400);const r=[...document.querySelectorAll('#prPage thead th')].map(t=>t.textContent).join(',')+' | 첫 줄='+[...document.querySelector('#prPage tbody tr').children].map(c=>c.innerText.trim()).join('|');document.querySelector('[data-opt=clBlank]').click();await W(300);return r")
step("④ 체크리스트 인쇄", "const pw=async(id)=>{window.__lastPW=null;const o0=window.open;window.open=function(){const w=o0.apply(window,arguments);window.__lastPW=w;return w;};app._prPrint(id);window.open=o0;await W(900);const w=window.__lastPW;const f=document.getElementById('prPrintFrame');return w?{doc:w.document,html:w.document.documentElement.outerHTML,done:()=>w.close(),via:'작은 창'}:f?{doc:f.contentDocument,html:f.srcdoc,done:()=>f.remove(),via:'숨은 틀'}:null;};const P=await pw(8901);const r='인쇄용 표='+(!!P&&/<table/.test(P.html))+' | 방식='+(P&&P.via);P&&P.done();return r")
step("④ 예전 체크리스트 출력 경로도 같은 창", "app.closeProgressReport();await W(300);app.openPDFModal(8901);await W(600);return '탭='+document.querySelector('.pr-tabs .on')?.textContent+' | 새 창='+window.__opens+' | 예전 작성자 창='+!!document.querySelector('.pdf-author-modal')")
step("정리", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
