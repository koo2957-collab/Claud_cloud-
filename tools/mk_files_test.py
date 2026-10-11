import json
# 예시 사진 넘기기(창 그대로·내용만 바뀜) + 파일 줄 통일(상자 없음·34px·작은 형식 표) 시험 → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===8801);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
pv = "const pvm=()=>[...document.querySelectorAll('.modal.show')].reverse().find(m=>m.querySelector('.pv-nav'));const st=()=>{const m=pvm();if(!m)return '미리보기 없음';return '창 같음='+(m===window.__pvm)+' | '+m.querySelector('.pv-nav-n').textContent+' 「'+m.querySelector('h2').textContent.trim()+'」 | 창 바뀐 횟수='+window.__mods+' | 열린 미리보기='+document.querySelectorAll('.modal.show .pv-nav').length};"
step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[{text:'출석통지',indent:0,completed:false},{text:'출석요구서 발송',indent:1,completed:false}];app.allData.workflows.unshift({id:8801,type:'manual',title:'파일 줄 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "const mk=async(label,col)=>{const cv=document.createElement('canvas');cv.width=1400;cv.height=900;const g=cv.getContext('2d');g.fillStyle=col;g.fillRect(0,0,1400,900);g.fillStyle='#fff';g.font='bold 90px sans-serif';g.fillText(label,100,480);return await new Promise(r=>cv.toBlob(r,'image/png'))};"
     "const files=[new File([await mk('사진 1','#2563eb')],'등기 수령증 예시.png',{type:'image/png'}),new File([await mk('사진 2','#059669')],'시스템 화면 캡처.png',{type:'image/png'}),new File([await mk('사진 3','#d97706')],'현장 사진.png',{type:'image/png'}),new File(['%PDF-1.4 '+'0'.repeat(4000)],'출석요구서 작성례.pdf',{type:'application/pdf'})];"
     "await app.addTipFiles(8801,1,{files,value:''},{silent:true,noShrink:true});"
     "const id=await app.dbManager.saveFile('repoDocuments',{name:'출석요구서 양식(소방공무원 징계령 별지 제3호 서식) 2024 개정.hwpx',size:21000,blob:new Blob(['x'.repeat(21000)]),type:'application/octet-stream',folderId:null,uploadedAt:new Date().toISOString(),updatedAt:new Date().toISOString(),tags:[]});await app._loadRepoDocMetaCache();wf().checklist[1].linkedDocs=[id];"
     "await app.addResultFiles(8801,1,{files:[new File(['%PDF-1.4 '+'0'.repeat(9000)],'발송 대장.pdf',{type:'application/pdf'}),files[0]],value:''});"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(8801);await W(1500);return '예시='+app._tipFiles(8801,wf().checklist[1].itemId).length")
step("미리보기 열기(1/4)", pv + "await app.previewTipFile(8801,1,0);await W(900);window.__pvm=pvm();window.__mods=0;new MutationObserver(ms=>ms.forEach(m=>[...m.addedNodes,...m.removedNodes].forEach(n=>{if(n.classList&&n.classList.contains('modal'))window.__mods++}))).observe(document.body,{childList:true});return st()")
S.append({"shot": "fl_pv1.png"})
S.append({"key": "ArrowRight", "vk": 39})
step("→ 키(2/4) — 창이 닫혔다 열리지 않음", pv + "const t0=performance.now();await W(500);return st()")
S.append({"shot": "fl_pv2.png"})
step("› 버튼 실제 클릭 준비", "const b=[...document.querySelectorAll('.modal.show .pv-nav button')].pop().getBoundingClientRect();window.__pt=[b.left+b.width/2,b.top+b.height/2];return 'ok'")
S.append({"pt": True, "js": P + "return JSON.stringify(window.__pt)" + E})
S.append({"clickpt": 1, "wait": 100})
step("› 버튼(3/4)", pv + "await W(500);return st()")
S.append({"key": "ArrowRight", "vk": 39})
step("→ (4/4 PDF)", pv + "await W(900);return st()+' | PDF 보기='+!!pvm().querySelector('#previewContent iframe, #previewContent embed, #previewContent object, #previewContent canvas')")
S.append({"key": "ArrowRight", "vk": 39})
S.append({"key": "ArrowRight", "vk": 39})
S.append({"key": "ArrowRight", "vk": 39})
step("→ 세 번 빠르게(4→1→2→3)", pv + "await W(1500);return st()")
S.append({"key": "ArrowLeft", "vk": 37})
step("← (2/4)", pv + "await W(600);return st()")
step("내려받기는 지금 보는 파일", pv + "let nm='';const oc=HTMLAnchorElement.prototype.click;HTMLAnchorElement.prototype.click=function(){nm=this.download};pvm().querySelector('.pv-dl').click();HTMLAnchorElement.prototype.click=oc;return '내려받는 이름='+nm")
step("닫기", "[...document.querySelectorAll('.modal.show')].reverse().forEach(m=>m.querySelector('.close-preview-modal')?.click());await W(500);return '남은 미리보기='+document.querySelectorAll('.modal.show .pv-nav').length")
# 파일 줄
rows = "const rows=sel=>[...document.querySelectorAll(sel)].filter(x=>x.offsetParent).map(r=>{const cs=getComputedStyle(r);const ico=r.querySelector('.rf-ico,.rf-thumb');const ir=ico?ico.getBoundingClientRect():null;return Math.round(r.getBoundingClientRect().height)+'px'+(cs.borderLeftWidth!=='0px'?' 상자':'')+(ir?' 표 '+Math.round(ir.width)+'x'+Math.round(ir.height):'')}).join(', ');"
step("항목 창 서식 탭 줄", rows + "await app.showChecklistItemModal(8801,1,'formats');await W(800);return rows('#cimOverlay .rf-row')")
S.append({"shot": "fl_fm.png"})
step("항목 창 처리결과 첨부 줄", rows + "app.switchChecklistItemTab(8801,1,'result');await W(600);return rows('#cimOverlay .rf-box .rf-row')")
step("항목 창 업무팁 예시 줄", rows + "app.switchChecklistItemTab(8801,1,'tip');await W(800);return rows('#cimOverlay .tf-box .rf-row')")
S.append({"shot": "fl_tip.png"})
step("길잡이 서식 줄", "app.closeChecklistItemModal();await W(400);await app.showChecklistHelp(8801,1);await W(1400);const c=[...document.querySelectorAll('.gd-modal .gd-card')];return c.map(x=>{const cs=getComputedStyle(x);const ico=x.querySelector('.rf-ico').getBoundingClientRect();return Math.round(x.getBoundingClientRect().height)+'px 테두리='+cs.borderLeftWidth+' 표 '+Math.round(ico.width)+'x'+Math.round(ico.height)+' ⬇보임='+getComputedStyle(x.querySelector('.attach-file-btn')||x).opacity}).join(' / ')")
S.append({"shot": "fl_guide.png"})
step("정리", "document.querySelectorAll('.gd-modal').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
