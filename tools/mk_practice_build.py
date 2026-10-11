# 연습 업무카드 만들기: practice_data.py의 내용을 실제 프로그램 안에서 업무로 만들고(업무팁·건너뛰기 버튼·서식·예시 그림·마감일),
# 프로그램의 [업무 파일 만들기]와 같은 함수로 내보내 사용설명서/연습업무.json 으로 저장 → steps3.json
# 실행: (tools 폴더에서) python mk_practice_build.py && node cdp3.mjs <index.html 경로>  →  python embed_practice.py
import json, os
import practice_data as PD

P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body, **kw): S.append({"label": label, "js": P + body + E, **kw})

SPEC = {
    "cards": [
        {"id": 9101, "title": PD.PURCHASE_TITLE, "deadline": 55, "items": PD.PURCHASE_ITEMS, "skips": PD.PURCHASE_SKIPS,
         "forms": PD.PURCHASE_FORMS, "tipfiles": PD.PURCHASE_TIPFILES, "refs": PD.PURCHASE_REFS},
        {"id": 9102, "title": PD.REPORT_TITLE, "deadline": 4, "items": PD.REPORT_ITEMS, "skips": [], "forms": [], "tipfiles": [], "refs": [],
         "done": 3},
    ]
}

# e호조 흐름 그림 — 실제 화면이 아니라 앱이 그린 설명용 그림 (프로그램 글꼴 Pretendard, 앱 색)
DRAW = r"""
const drawFlow=async()=>{await document.fonts.load('700 30px Pretendard');await document.fonts.load('400 22px Pretendard');
const cv=document.createElement('canvas');cv.width=1600;cv.height=620;const g=cv.getContext('2d');
g.fillStyle='#ffffff';g.fillRect(0,0,1600,620);
g.fillStyle='#0f172a';g.font='700 34px Pretendard';g.fillText('e호조 지출 — 큰 순서',60,78);
g.fillStyle='#8b5cf6';g.font='700 22px Pretendard';const tag='설명용 그림 · 실제 화면 아님';const tw=g.measureText(tag).width;
g.fillStyle='rgba(139,92,246,0.12)';g.beginPath();g.roundRect(60+g.measureText('').width+430,50,tw+32,40,20);g.fill();g.fillStyle='#7c3aed';g.fillText(tag,60+446,78);
const boxes=[['1','지출결의','대금청구서 · 세금계산서','검사조서를 붙여 올림'],['2','결재','기관 결재선에 따라','(기관마다 다름)'],['3','지급명령','결재가 끝나면','지급을 명령'],['4','지급 확인','업체 계좌 입금 확인','청구일부터 5일 안']];
const x0=60,y0=170,w=330,h=250,gap=60;
boxes.forEach(([n,t,a,b],i)=>{const x=x0+i*(w+gap);
 g.fillStyle='#f8fafc';g.strokeStyle='#cbd5e1';g.lineWidth=3;g.beginPath();g.roundRect(x,y0,w,h,22);g.fill();g.stroke();
 g.fillStyle=i===3?'#10b981':'#2563eb';g.beginPath();g.roundRect(x+28,y0+30,58,58,12);g.fill();
 g.fillStyle='#fff';g.font='700 30px Pretendard';g.textAlign='center';g.fillText(n,x+57,y0+70);g.textAlign='left';
 g.fillStyle='#0f172a';g.font='700 32px Pretendard';g.fillText(t,x+104,y0+71);
 g.fillStyle='#475569';g.font='400 23px Pretendard';g.fillText(a,x+30,y0+150);g.fillText(b,x+30,y0+190);
 if(i<3){const ax=x+w+8,ay=y0+h/2;g.strokeStyle='#94a3b8';g.lineWidth=5;g.beginPath();g.moveTo(ax,ay);g.lineTo(ax+gap-20,ay);g.stroke();
  g.fillStyle='#94a3b8';g.beginPath();g.moveTo(ax+gap-8,ay);g.lineTo(ax+gap-26,ay-13);g.lineTo(ax+gap-26,ay+13);g.closePath();g.fill();}});
g.fillStyle='#dc2626';g.font='700 23px Pretendard';g.fillText('⚠ 메뉴 이름 · 결재선은 기관마다 다릅니다 — 내 기관 화면은 직접 캡처해 「예시·사진」에 붙여 두세요 (Ctrl+V)',60,520);
g.fillStyle='#64748b';g.font='400 21px Pretendard';g.fillText('업무 내비게이터 연습 업무 · 근거: 지방계약법 시행령 제67조(대가의 지급)',60,566);
return await new Promise(r=>cv.toBlob(r,'image/png'));};
"""

BUILD = r"""
const SPEC=__SPEC__;
const D=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));
const out=[];
for(const c of SPEC.cards){
 app.allData.workflows=app.allData.workflows.filter(w=>w.id!==c.id);
 const now=new Date().toISOString();
 const cl=c.items.map(([t,lv,tip,dd])=>{const it={text:t,indent:lv,completed:false};if(tip)it.tip={type:'text',content:tip,saved:true};if(dd!=null)it.deadline=D(dd);return it;});
 const wf={id:c.id,type:'manual',title:c.title,checklist:cl,date:new Date().toLocaleDateString('ko-KR'),createdAt:now,folderPath:'',deadline:D(c.deadline)};
 app.allData.workflows.unshift(wf);wf.checklist.forEach(it=>app.ensureChecklistItemId(it));
 const idx=t=>{const i=wf.checklist.findIndex(it=>it.text===t);if(i<0)throw new Error('없는 줄: '+t);return i;};
 for(const [base,label,targets] of c.skips){const b=wf.checklist[idx(base)];(b.branchOptions=b.branchOptions||[]).push({label,action:'',targetItemIds:targets.map(t=>wf.checklist[idx(t)].itemId),selfSkip:false});}
 if(c.done){for(let i=0;i<c.done;i++){wf.checklist[i].completed=true;wf.checklist[i].completedAt=now;}wf.lastProgressAt=now;}
 for(const [t,name] of c.forms){const blob=await (await fetch('./tools/practice/'+encodeURIComponent(name))).blob();
  const f=new File([blob],name,{type:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
  const h=await app.computeFileHash(f);const ex=await app.findDuplicateRepoDocument(f,h);const id=ex?ex.id:await app._createRepoDocumentRecord(f,h,null);
  const it=wf.checklist[idx(t)];it.linkedDocs=it.linkedDocs||[];if(!it.linkedDocs.includes(id))it.linkedDocs.push(id);}
 app.saveData();
 if(c.refs.length){const files=[];for(const name of c.refs){const blob=await (await fetch('./tools/practice/'+encodeURIComponent(name))).blob();files.push(new File([blob],name,{type:'application/pdf'}));}
  window._askLibraryDuplicateKeep=app._askLibraryDuplicate;app._askLibraryDuplicate=async()=>'keep';
  const res=await app.addLawLibraryFiles({type:'change',target:{files,value:''}});app._askLibraryDuplicate=window._askLibraryDuplicateKeep;
  const pk='project-'+c.id;app.checklistDetails[pk]=app.checklistDetails[pk]||{attachments:[],forms:[]};app.checklistDetails[pk].linkedLibraryDocs=res.map(r=>r.id).filter(Boolean);
  await app.dbManager.saveChecklistDetails(pk,app.checklistDetails[pk]);}
 for(const [t,name] of c.tipfiles){const blob=await drawFlow();await app.addTipFiles(c.id,idx(t),{files:[new File([blob],name,{type:'image/png'})],value:''},{noShrink:true});}
 out.push(c.title+': 줄 '+cl.length+' · 건너뛰기 '+c.skips.length+' · 서식 '+c.forms.length+' · 예시 '+c.tipfiles.length+' · 참고 자료 '+c.refs.length);
}
app.saveData();app.displayWorkflows();await W(600);
return out.join(' | ');
"""

step("만들기", DRAW + BUILD.replace("__SPEC__", json.dumps(SPEC, ensure_ascii=False)))
step("모양 확인 (구매)", "app.focusWorkflow(9101);await W(1500);const wf=app.allData.workflows.find(w=>w.id===9101);return '단계='+wf.checklist.filter(i=>!i.indent).length+' 할 일='+wf.checklist.filter(i=>i.indent).length+' 건너뛰기 단추 줄='+wf.checklist.filter(i=>i.branchOptions).map(i=>i.text+'('+i.branchOptions.map(o=>o.label).join('/')+')').join(', ')")
S.append({"shot": "practice_focus.png"})
step("내보내기 (프로그램의 업무 파일 만들기와 같은 함수)",
     "let txt=null;const keep=app._saveFileWithPicker;app._saveFileWithPicker=async(b)=>{txt=await b.text();return true;};"
     "await app.exportMultipleWorkflowPackages([9101,9102]);app._saveFileWithPicker=keep;window.__pkg=txt;"
     "const p=JSON.parse(txt);return '업무='+p.workflows.length+' 법령·매뉴얼='+(p.lawLibraryData?.files?.length||0)+' 서식·문서='+(p.repoDocumentsData?.files?.length||0)+' 첨부='+Object.values(p.attachmentsData||{}).flat().length+' 크기='+Math.round(txt.length/1024)+'KB'")
step("저장", "return window.__pkg", save="../사용설명서/연습업무.json")
step("정리", "app.exitFocusMode?.();app.allData.workflows=app.allData.workflows.filter(w=>w.id!==9101&&w.id!==9102);app.saveData();return 'ok'")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
