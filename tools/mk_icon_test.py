import json
# 항목 창 탭·새 업무 창 버튼·첨부/예시 제목 아이콘 통일 시험 + 길잡이 창 「다음 할 일」 확인 → steps3.json
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7301);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(body): return P + body + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(body): S.append({"pt": True, "js": J(body)})
# 탭 안 아이콘 정보: [탭 이름, svg 있음, 아이콘 색, 고른 탭인지]
tabs = ("const tabs=()=>[...document.querySelectorAll('#cimOverlay .cim-tab, .cim-tab')].filter(b=>b.offsetParent).map(b=>{const g=b.querySelector('svg');return b.textContent.trim()+'['+(g?getComputedStyle(g).color:'점')+(b.classList.contains('cim-tab-active')?',고름':'')+']'}).join(' ');"
        "const dots=()=>[...document.querySelectorAll('.cim-tab span[style*=\"border-radius:50%\"]')].length;")
tabPt = "const b=[...document.querySelectorAll('.cim-tab')].find(x=>x.offsetParent&&x.textContent.includes('{t}'));const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])"

step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0],['징계 의결서 수령',1],['결과 통보',1]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7301,type:'manual',title:'아이콘 통일 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "wf().checklist[2].tip={type:'text',content:'1. 출석통지서는 회의 3일 전까지 도달\\n2. 등기우편 + 문자로 함께 알림',saved:true};"
     "const id=await app.dbManager.saveFile('repoDocuments',{name:'출석통지서 서식.hwpx',size:9000,blob:new Blob(['x'.repeat(9000)]),type:'application/octet-stream',folderId:null,uploadedAt:new Date().toISOString(),updatedAt:new Date().toISOString(),tags:[]});await app._loadRepoDocMetaCache();wf().checklist[2].linkedDocs=[id];"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7301);await W(900);app.toggleChecklistItem(7301,1);await W(1200);"
     "await app.addResultFiles(7301,2,{files:[new File(['%PDF-1.4 '+'0'.repeat(3000)],'통지서 발송 대장.pdf',{type:'application/pdf'})],value:''});"
     "const cv=document.createElement('canvas');cv.width=600;cv.height=380;const g=cv.getContext('2d');g.fillStyle='#2563eb';g.fillRect(0,0,600,380);g.fillStyle='#fff';g.font='bold 48px sans-serif';g.fillText('수령증 예시',60,200);const img=await new Promise(r=>cv.toBlob(r,'image/png'));"
     "await app.addTipFiles(7301,2,{files:[new File([img],'등기 수령증 예시.png',{type:'image/png'})],value:''});await W(600);return 'ok'")

step("A1 항목 창 열기(조치결과 탭)", tabs + "await app.showChecklistItemModal(7301,2,'result');await W(800);const t=document.querySelector('#rf-7301-2 .mat-title');return tabs()+' | 남은 색 점='+dots()+' | 첨부 제목='+t.textContent.trim().slice(0,12)+' svg='+!!t.querySelector('svg')+' 이모지📎='+t.textContent.includes('📎')")
S.append({"shot": "ic_a1.png"})
pt(tabPt.replace('{t}', '업무팁'))
S.append({"clickpt": 1, "wait": 100})
step("A2 업무팁 탭을 실제로 누름", tabs + "await W(600);const t=document.querySelector('#tf-7301-2 .mat-title');return tabs()+' | 예시 제목='+t.textContent.trim().slice(0,8)+' svg='+!!t.querySelector('svg')+' 이모지🖼='+t.textContent.includes('🖼')")
S.append({"shot": "ic_a2.png"})
pt(tabPt.replace('{t}', '서식'))
S.append({"clickpt": 1, "wait": 100})
step("A3 서식 탭을 실제로 누름", tabs + "await W(600);return tabs()")
S.append({"shot": "ic_a3.png"})
step("A4 다크 모드", tabs + "document.documentElement.classList.add('dark-mode');await W(400);return tabs()")
S.append({"shot": "ic_a4.png"})
step("A5 레퍼런스: 건너뛰기 탭", tabs + "document.documentElement.classList.remove('dark-mode');app.closeChecklistItemModal();await W(300);wf().isReference=true;app.saveData();await app.showChecklistItemModal(7301,4,'result');await W(800);const r=tabs();app.closeChecklistItemModal();wf().isReference=false;app.saveData();await W(300);return r")
S.append({"shot": "ic_a5.png"})

step("B1 새 업무 ③ 단계 버튼", "app.closeChecklistItemModal();await W(300);app.openModal('manualModal');await W(500);document.getElementById('manualProjectName').value='새 업무 아이콘 시험';app._nwGo(2);await W(400);const first=document.querySelector('#checklistItems .checklist-edit-item input');if(first)first.value='자료 준비';app.addChecklistItem('기안문 작성',1);await W(300);app._nwGo(3);await W(800);"
     "const bs=[...document.querySelectorAll('.nw-mat-btn')];return bs.map(b=>b.textContent.trim()+'('+(b.querySelector('svg')?getComputedStyle(b.querySelector('svg')).color:'아이콘 없음')+')').join(' / ')+' | 이모지 남음='+bs.some(b=>/💡|📄/.test(b.textContent))")
S.append({"shot": "ic_b1.png"})
pt("const b=[...document.querySelectorAll('.nw-mat-btn')].find(x=>x.textContent.includes('업무팁'));const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("B2 업무팁 버튼 실제로 누름 → 항목 창 업무팁 탭", tabs + "await W(800);return tabs()")
S.append({"shot": "ic_b2.png"})

step("C1 길잡이 창(진행 중 항목)", "app.closeChecklistItemModal();await W(300);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));await W(200);app.focusWorkflow(7301);await W(800);await app.showChecklistHelp(7301,2);await W(1500);"
     "const m=document.querySelector('[id^=aiGuideModal_]');const body=[...m.querySelectorAll('div')].find(d=>d.style.overflowY==='auto');const n=m.querySelector('.gd-next');const br=body.getBoundingClientRect(),nr=n?n.getBoundingClientRect():null;"
     "return '본문 높이 '+Math.round(body.clientHeight)+' / 내용 '+body.scrollHeight+' | 다음 할 일='+(n?n.textContent.trim():'없음')+' | 본문 밖(아래 버튼 줄)='+(n?!body.contains(n):'-')+' | 처음 화면에 보임='+(nr?nr.top>=0&&nr.bottom<=innerHeight:false)")
step("C1b 업무팁이 아주 길 때도 처음부터 보임", "const keep=wf().checklist[2].tip.content;wf().checklist[2].tip.content=Array.from({length:40},(_,k)=>(k+1)+'. 긴 업무팁 줄 '+(k+1)).join('\\n');app.saveData();document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(400);await app.showChecklistHelp(7301,2);await W(1500);"
     "const m=[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();const body=[...m.querySelectorAll('div')].find(d=>d.style.overflowY==='auto');const n=m.querySelector('.gd-next');const nr=n.getBoundingClientRect();const r='본문 높이 '+body.clientHeight+' / 내용 '+body.scrollHeight+' | 처음 화면에 보임='+(nr.top>=0&&nr.bottom<=innerHeight)+' | 버튼 너비='+Math.round(nr.width);wf().checklist[2].tip.content=keep;app.saveData();return r")
S.append({"shot": "ic_c1b.png"})
step("C1c 원래 길잡이로", "document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(400);await app.showChecklistHelp(7301,2);await W(1500);return 'ok'")
S.append({"shot": "ic_c1.png"})
gd = ("const gd=()=>{const m=[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).pop();if(!m)return '창 없음';const h=[...m.querySelectorAll('.gd-sec-h')].map(x=>x.textContent.trim().replace(/\\s+/g,'')+(x.querySelector('svg')?'(아이콘)':'(아이콘 없음)'));"
      "const n=m.querySelector('.gd-next');return '제목='+m.querySelector('h2,h3,[class*=title]')?.textContent.trim().slice(0,30)+' | 줄='+m.textContent.match(/\\d\\d-\\d|\\d\\d(?=\\D)/)?.[0]+' | 묶음='+h.join(',')+' | 색 점='+m.querySelectorAll('.gd-dot').length+' | 다음='+(n?n.querySelector('b').textContent+' 테두리='+getComputedStyle(n).borderStyle:'없음')};")
step("C2 묶음 제목 아이콘·다음 할 일 대상", gd + "return gd()")
pt("const n=[...document.querySelectorAll('[id^=aiGuideModal_] .gd-next')].pop();n.scrollIntoView();const r=n.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 100})
step("C3 「다음 할 일」 실제로 누름", gd + "await W(1800);return '열린 길잡이 수='+[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/^aiGuideModal_\\d+$/.test(x.id)).length+' | '+gd()")
S.append({"shot": "ic_c3.png"})
step("C4 마지막 할 일: 다음 없음", gd + "document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(400);await app.showChecklistHelp(7301,5);await W(1500);return gd()")
step("C5 할 일이 모두 건너뛴 단계는 단계 자체가 다음", gd + "document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(400);wf().checklist[4].skipped=true;wf().checklist[5].skipped=true;app.saveData();await app.showChecklistHelp(7301,2);await W(1500);const r=gd();wf().checklist[4].skipped=false;wf().checklist[5].skipped=false;app.saveData();document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());await W(300);return r")
step("C6 단계 다음에 바로 할 일이 아닌 줄", gd + "await app.showChecklistHelp(7301,0);await W(1500);const r=gd();document.querySelectorAll('[id^=aiGuideModal_]').forEach(m=>m.querySelector('[id$=_closeBtn]')?.click());return r")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
