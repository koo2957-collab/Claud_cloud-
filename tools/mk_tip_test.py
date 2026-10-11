import json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7201);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(body): return P + body + E
mkimg = ("const mkImg=async(label,color)=>{const cv=document.createElement('canvas');cv.width=800;cv.height=500;const g=cv.getContext('2d');g.fillStyle=color;g.fillRect(0,0,800,500);g.fillStyle='#fff';g.font='bold 60px sans-serif';g.fillText(label,60,260);"
         "const b=await new Promise(r=>cv.toBlob(r,'image/png'));return b;};")
tipN = "const tipN=i=>app._tipFiles(7201,wf().checklist[i].itemId).map(f=>f.name);"
S = []
def step(label, body): S.append({"label": label, "js": J(mkimg + tipN + body)})
step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0],['징계 의결서 수령',1]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7201,type:'manual',title:'예시 첨부 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "wf().checklist[2].tip={type:'text',content:'1. 출석통지서는 회의 3일 전까지 도달\\n2. 등기우편 + 문자',saved:true};app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7201);await W(900);app.toggleChecklistItem(7201,1);await W(1500);return 'ok'")
step("T1 업무팁 탭 (빈 상태)", "await app.showChecklistItemModal(7201,2,'tip');await W(700);const b=document.getElementById('tf-7201-2');return 'box='+!!b+' upload='+!!b?.querySelector('input[type=file]')+' | '+(b?b.innerText.replace(/\\s+/g,' ').slice(0,160):'')")
S.append({"shot": "tp_t1.png"})
step("T2 올리기 (사진+PDF)", "const img=await mkImg('수령증 예시','#2563eb');await app.addTipFiles(7201,2,{files:[new File([img],'등기 수령증 예시.png',{type:'image/png'}),new File(['%PDF-1.4 '+'0'.repeat(30000)],'출석통지서 작성례.pdf',{type:'application/pdf'})],value:''});await W(900);"
     "const badge=document.getElementById('cim-badge-tip-7201-2')?.textContent;return 'files='+tipN(2).join(',')+' | 탭표시='+badge+' | thumb ready='+document.querySelectorAll('#tf-7201-2 .rf-thumb.ready').length")
step("T3 Ctrl+V 화면 캡처 붙여넣기", "const img=await mkImg('시스템 화면','#059669');const dt=new DataTransfer();dt.items.add(new File([img],'image.png',{type:'image/png'}));const ev=new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true});document.querySelector('#cimOverlay textarea, #cimOverlay').dispatchEvent(ev);await W(1200);return 'prevented='+ev.defaultPrevented+' files='+tipN(2).join(',')")
S.append({"shot": "tp_t3.png"})
step("T3b 글만 붙여넣기 → 첨부 안 됨", "const dt=new DataTransfer();dt.setData('text/plain','글');const ev=new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true});document.querySelector('#cimOverlay').dispatchEvent(ev);await W(400);return 'prevented='+ev.defaultPrevented+' count='+tipN(2).length")
step("T4 미리보기 열기", "app.previewTipFile(7201,2,0);await W(1200);const m=[...document.querySelectorAll('.modal.show')].pop();return 'nav='+(m.querySelector('.pv-nav-n')?.textContent)+' title='+m.querySelector('h2')?.textContent")
S.append({"key": "ArrowRight", "vk": 39})
step("T4b → 키", "await W(1000);const m=[...document.querySelectorAll('.modal.show')].pop();return 'nav='+(m.querySelector('.pv-nav-n')?.textContent)+' title='+m.querySelector('h2')?.textContent+' | 열린 미리보기 수='+document.querySelectorAll('.modal.show .pv-nav').length")
S.append({"shot": "tp_t4.png"})
S.append({"key": "ArrowLeft", "vk": 37})
step("T4c ← 키 (처음으로)", "await W(1000);const m=[...document.querySelectorAll('.modal.show')].pop();return 'nav='+(m.querySelector('.pv-nav-n')?.textContent)")
step("T5 업무 절차 패널 썸네일", "[...document.querySelectorAll('.modal.show')].reverse().forEach(m=>m.querySelector('.close-preview-modal')?.click());await W(300);app.closeChecklistItemModal();await W(600);app.refreshAIPanelDashboardIfNeeded();await W(900);"
     "const t=[...document.querySelectorAll('.proc-thumb')];return 'thumbs='+t.length+' ready='+t.filter(x=>x.classList.contains('ready')).length+' kinds='+t.map(x=>x.className.replace('proc-thumb','').trim()||'img').join(',')")
S.append({"shot": "tp_t5.png"})
step("T5b 썸네일 누르면 미리보기", "document.querySelector('.proc-thumb').click();await W(1200);const m=[...document.querySelectorAll('.modal.show')].pop();const r='title='+m.querySelector('h2')?.textContent+' nav='+m.querySelector('.pv-nav-n')?.textContent;m.querySelector('.close-preview-modal')?.click();await W(300);return r")
step("T5c 줄의 💡 말풍선", "const r=[...document.querySelectorAll('.checklist-card')].find(c=>c.textContent.includes('출석통지서 발송'));const ind=r&&[...r.querySelectorAll('[title]')].map(x=>x.getAttribute('title')).find(t=>t.startsWith('업무팁'));return ind||'없음'")
step("T6 서식 → 업무팁 예시로 옮기기", "const id=await app.dbManager.saveFile('repoDocuments',{name:'출석통지서 예시공문.pdf',size:9000,blob:new Blob(['%PDF-1.4 '+'1'.repeat(9000)],{type:'application/pdf'}),type:'application/pdf',folderId:null,uploadedAt:new Date().toISOString(),updatedAt:new Date().toISOString(),tags:[]});await app._loadRepoDocMetaCache();"
     "wf().checklist[2].linkedDocs=[id];app.saveData();await app.showChecklistItemModal(7201,2,'formats');await W(700);const row=[...document.querySelectorAll('#main-checklist-formats-list-7201-2 [oncontextmenu]')][0];const b=row.getBoundingClientRect();row.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:b.left+80,clientY:b.top+10}));await W(400);"
     "const items=[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>x.textContent.trim());[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].find(x=>x.textContent.includes('업무팁 예시로'))?.click();await W(1200);"
     "const still=!!(await app._getRepoDocumentById(id));return 'menu='+items.join(',')+' | linkedDocs='+wf().checklist[2].linkedDocs.length+' | tip='+tipN(2).join(',')+' | 서식·문서함 원본 남음='+still")
S.append({"shot": "tp_t6.png"})
step("T7 레퍼런스 사본: 업무팁 예시는 복사, 조치결과 첨부는 안 함", "app.closeChecklistItemModal();await W(300);await app.addResultFiles(7201,2,{files:[new File(['x'.repeat(500)],'결과공문.pdf',{type:'application/pdf'})],value:''});"
     "const before=new Set(app.allData.workflows.map(w=>w.id));await app.executeDuplicateWorkflow(7201,{asReference:true,title:'예시 첨부 시험 (레퍼런스)',folder:''});await W(1500);const nw=app.allData.workflows.find(w=>!before.has(w.id));const it=nw.checklist[2];"
     "const tf=app._tipFiles(nw.id,it.itemId);const rf=app._collabResultFiles(nw.id,it.itemId);const blob=tf[0]?await app.dbManager.getFile('projectFiles',tf[0].id):null;window.__refId=nw.id;return 'ref tip='+tf.length+' (원본 '+tipN(2).length+') result='+rf.length+' | 파일 실제 있음='+!!(blob&&blob.blob)+' | 다른 파일 id='+(tf[0]&&tf[0].id!==app._tipFiles(7201,wf().checklist[2].itemId)[0].id)")
step("T8 내보내기 → 다시 가져오기", "window.__saved=[];window.showSaveFilePicker=async(o)=>({createWritable:async()=>{const parts=[];return{write:async x=>{parts.push(x)},close:async()=>{const b=new Blob(parts);window.__saved.push({name:o.suggestedName,text:await b.text()})}}}});"
     "await app.exportMultipleWorkflowPackages([7201]);await W(1500);const sv=window.__saved[0];if(!sv)return '저장 없음';const pkg=JSON.parse(sv.text);const keys=Object.keys(pkg.attachmentsData||pkg.attachments||{}).filter(k=>k.includes('-t-'));"
     "const before=new Set(app.allData.workflows.map(w=>w.id));await app.importTemplateFile([new File([sv.text],sv.name,{type:'application/json'})]);await W(1500);"
     "const dlg=[...document.querySelectorAll('.modal.show')].map(m=>[...m.querySelectorAll('button')].map(b=>b.textContent.trim()).join('/')).join(' || ');const pick=[...document.querySelectorAll('.modal.show button')].find(b=>/이어서|그대로|가져오기|새로 시작/.test(b.textContent));pick&&pick.click();await W(2000);"
     "const nw=app.allData.workflows.find(w=>!before.has(w.id));if(!nw)return 'pkg -t- keys='+keys.length+' | 가져온 업무 없음 | dlg='+dlg;const tf=app._tipFiles(nw.id,nw.checklist[2].itemId);const blob=tf[0]?await app.dbManager.getFile('projectFiles',tf[0].id):null;return 'pkg에 -t- 키='+keys.length+' | 고른 버튼='+(pick?pick.textContent.trim():'-')+' | 가져온 업무 예시='+tf.length+' 파일 있음='+!!(blob&&blob.blob)")
step("T9 담당자 PC에서는 예시 보기만", "const w2=app.allData.workflows.find(w=>w.id===window.__refId);w2.isReference=false;w2.collab={uid:'x',role:'assignee',me:'김민수',owner:'홍길동',steps:{}};app.saveData();await app.showChecklistItemModal(w2.id,2,'tip');await W(700);const b=document.getElementById('tf-'+w2.id+'-2');const r='box='+!!b+' upload='+!!b?.querySelector('input[type=file]')+' del='+!!b?.querySelector('.rf-del')+' rows='+(b?b.querySelectorAll('.rf-row').length:0);app.closeChecklistItemModal();delete w2.collab;app.saveData();return r")
step("T10 새 업무 ③ 단계 업무팁 창에도 예시", "app.closeAllDropdowns&&app.closeAllDropdowns();app.openModal('manualModal');await W(500);document.getElementById('manualProjectName').value='마법사 예시 시험';app._nwGo(2);await W(400);const first=document.querySelector('#checklistItems .checklist-edit-item input');if(first)first.value='단계 하나';app.addChecklistItem('할 일 하나',1);await W(300);app._nwGo(3);await W(600);app._nwOpenItem(1,'tip');await W(800);const w=app._nw&&app.allData.workflows.find(x=>x.id===app._nw.wfId);const b=w&&document.getElementById('tf-'+w.id+'-1');return 'wizard wf='+!!w+' 예시 칸='+!!b+' 올리기='+!!b?.querySelector('input[type=file]')")
S.append({"shot": "tp_t10.png"})
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
