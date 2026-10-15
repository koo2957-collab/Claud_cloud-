# AI 업무파트너·AI 길잡이 「조문 단위 찾기」 시험 대본 → steps3.json  (AI 허용판 `ai_test .html`로 실행, 가짜 AI)
# 확인: 조문 나누기 · 질문 낱말/조문 번호로 찾기 · 업무 자료에서 못 찾으면 전체에서 · 찾은 근거 상자 먼저 → 답(받는 대로)
#       · 인용 ✓/확인 필요 · [번호]·단추 → 원문 창(Esc) · AI 호출은 답 한 번(요약 없음) · ChatGPT(한 번에) 경로
#       · 머리 줄 「참고 중」 [빼기]/[업무 넣기] · 질문 예시 단추 · 법제처 보강(가짜 응답) · AI 길잡이 = 일반 길잡이 화면 + 「법령·매뉴얼 점검」
# 실행: (tools 폴더에서) python mk_law_test.py && node cdp3.mjs "<저장소>/ai_test .html"
#       잠금판 확인: python mk_law_test.py locked && node cdp3.mjs "<저장소>/index.html"
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
PDF = HERE + '/practice/지방계약법 시행령(2026.6.3. 시행).pdf'
RULE = "제1조(목적) 이 규정은 소방공무원 징계 절차를 정한다.\\n제12조(진술 기회) ① 징계위원회는 혐의자에게 출석 통지서를 회의 5일 전까지 보내야 한다.\\n② 진술 기회는 충분히 주어야 하며, 제13조에 따른 기한을 지킨다.\\n제13조(의결 기한) 징계위원회는 징계 의결 요구를 받은 날부터 30일 이내에 의결하여야 한다.\\n제14조(통보) 의결 결과는 지체 없이 알린다."
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7921,ID2=7922;"
     "const load=(u,t)=>new Promise((ok,no)=>{const x=new XMLHttpRequest();x.open('GET',encodeURI('file:///'+u));x.responseType='blob';x.onload=()=>ok(new File([x.response],u.split('/').pop(),{type:t||''}));x.onerror=()=>no(new Error('못 읽음 '+u));x.send();});"
     "const vis=el=>!!el&&el.offsetParent!==null;const txt=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(body): S.append({"pt": True, "js": J(body)})

# 가짜 AI: 받은 글 기록, 답은 [찾은 근거] 1번의 실제 글 일부 + 지어낸 인용 하나
STUB = ("window.__ai=[];window.__fetch=[];if(!window.__of){window.__of=window.fetch;window.fetch=function(u,o){window.__fetch.push(String(u).slice(0,60));return window.__of.apply(this,arguments)};}"
        "const mk=p=>{const m=p.match(/\\[1\\][^\\n]*\\n([^\\n]{12,})/);const real=m?m[1].trim().replace(/^[①-⑳]\\s*/,'').slice(0,22):'없음';return '**답** 출석 통지는 회의 5일 전까지 보내야 합니다 [1].\\n**근거**\\n- [1] 징계 규정 제12조: “'+real+'”\\n- [2] 지어낸 인용: “회의 3일 전까지 보내면 된다”\\n**확인할 점** 기관 내부 규정도 함께 보세요.'};"
        "app._tryGeminiChainStream=async(p,k,chain,contents,on)=>{const t=contents[contents.length-1].parts[0].text;window.__ai.push({kind:'stream',t});const a=mk(t);on(a.slice(0,30),a.slice(0,30));await W(150);on(a,a);return a};"
        "app.callAIWithHistory=async(msgs)=>{const t=msgs[msgs.length-1].content;window.__ai.push({kind:'once',t});await W(150);return mk(t)};"
        "app.callAI=app.callAIWithDocuments=async(p)=>{window.__ai.push({kind:'callAI',t:p});await W(200);const m=p.match(/\\[1\\][^\\n]*\\n([^\\n]{12,})/);const real=m?m[1].trim().replace(/^[①-⑳]\\s*/,'').slice(0,20):'';return JSON.stringify({must:[{text:'출석 통지서는 회의 5일 전까지 보냅니다',ref:1,quote:real}],diff:[{text:'업무팁의 「3일 전」은 규정의 5일 전과 다릅니다',ref:1,quote:'회의 5일 전까지 보내야 한다'}],missing:[{text:'진술 기회 부여 기록',ref:1}]})};")

if not LOCKED:
    step("준비: 업무 2개(연결 자료 있음/없음) + 법령·매뉴얼 2개(시행령 PDF·징계 규정 TXT)",
         "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app.allData.lawApiKey='';app._syncAiOff?.();app.updateManualAiFillButtonState?.();"
         "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&w.id!==ID2);"
         "const mkIt=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
         "app.allData.workflows.unshift({id:ID,type:'manual',title:'징계 절차 시험',checklist:[mkIt('징계 의결 요구',0),mkIt('출석 통지서 보내기',1,'회의 3일 전까지 보냅니다\\n근거: 징계 규정 제12조'),mkIt('징계위원회 의결',1),mkIt('계약 방법 정하기',0),mkIt('수의계약 사유 확인',1)],date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});"
         "app.allData.workflows.unshift({id:ID2,type:'manual',title:'자료 없는 업무',checklist:[mkIt('보고서 쓰기',0)],date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});"
         "const old=await app._getAllLibraryFiles();for(const f of old){if(/징계 규정|지방계약법 시행령/.test(f.name))await app.dbManager.deleteFile('lawLibrary',f.id);}"
         "const pdf=await load('" + PDF + "','application/pdf');const rule=new File([\"" + RULE + "\"],'징계 규정.txt',{type:'text/plain'});"
         "const ids=[];for(const f of [rule,pdf]){const id=await app.dbManager.saveFile('lawLibrary',{name:f.name,type:f.type,size:f.size,blob:f,uploadDate:new Date().toISOString(),groupId:null});ids.push(id);}"
         "await app._linkLibraryDocs(ID,ids);await app.saveDataImmediate();window.__ids=ids;"
         "const t0=performance.now();const docs=await app._lawDocs(ID);const t1=performance.now();"
         "const u=docs.map(d=>d.filename.slice(0,10)+' '+app._lawUnits(d).length+'조각('+app._lawUnits(d).filter(x=>x.no).length+'조문)').join(' / ');"
         "return '자료='+docs.length+' | '+u+' | 첫 읽기 '+Math.round(t1-t0)+'ms | 규정 조문='+app._lawUnits(docs.find(d=>/징계/.test(d.filename))).map(x=>x.no+(x.title?'('+x.title+')':'')).join(',')")
    step("A 찾기: 낱말(조사 떼기) · 조문 번호 · 문서 이름 · 걸린 시간",
         "const show=R=>R.hits.slice(0,6).map(h=>h.n+'.'+app._lawShortName(h.file)+' '+(h.no||h.title.slice(0,10))+'('+h.score+')').join(' · ');"
         "const t0=performance.now();const A=await app._lawRetrieve(ID,'출석 통지서는 회의 며칠 전까지 보내야 하나요?');const t1=performance.now();"
         "const B=await app._lawRetrieve(ID,'시행령 제25조 내용 알려줘');const C=await app._lawRetrieve(ID,'수의계약을 할 수 있는 추정가격 기준은?');"
         "return '낱말='+JSON.stringify(app._lawTerms('출석 통지서는 회의 며칠 전까지 보내야 하나요?'))+' | ① '+show(A)+' ['+Math.round(t1-t0)+'ms] | ② 제25조 → '+show(B)+' | ③ '+show(C)")
    step("A2 연결 자료 없는 업무 → 법령·매뉴얼 전체에서 찾음",
         "const R=await app._lawRetrieve(ID2,'징계 의결 기한은 며칠?');return 'scope='+R.scope+' 자료='+R.docCount+' 첫 근거='+(R.hits[0]?app._lawShortName(R.hits[0].file)+' '+R.hits[0].no:'없음')")
    # 업무파트너
    step("B 업무 열고 업무파트너 보기 → 머리 줄 「참고 중」·질문 예시",
         STUB + "app.focusWorkflow(ID);await W(1200);if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(500);app.setAiPanelView('chat');await W(400);"
         "return 'selectedProjectId='+(app.selectedProjectId===ID)+' | 머리 줄='+txt($('aiCtxLine'))+' | 예전 단추 보임='+vis(document.querySelector('#aiContextBar .ai-context-label'))+' | 질문 예시='+[...document.querySelectorAll('#aiSuggest .ai-sug')].map(b=>b.textContent).join(' / ')+' 보임='+vis($('aiSuggest'))")
    S.append({"shot": "law_chat0.png"})
    step("B2 [빼기] → 업무 없이 / [업무 넣기] → 다시",
         "document.querySelector('#aiCtxLine .ai-ctx-x').click();await W(100);const a=txt($('aiCtxLine'));const off=app._aiCtxWf();document.querySelector('#aiCtxLine .ai-ctx-x').click();await W(100);return '빼기 뒤='+a+' (참고 업무 '+(off?off.title:'없음')+') | 넣기 뒤='+txt($('aiCtxLine'))")
    step("C 질문 입력", "const i=$('aiInput');i.focus();i.value='출석 통지서는 회의 며칠 전까지 보내야 하나요?';return 'ok'")
    pt("document.querySelectorAll('.toast,#toast').forEach(t=>t.classList.remove('show'));const r=$('aiSendBtn').getBoundingClientRect();const top=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);if(!top||!top.closest('#aiSendBtn'))console.log('send covered by',top?.className);return JSON.stringify([r.x+r.width/2,r.y+r.height/2])")
    S.append({"clickpt": 1})
    step("C2 보낸 직후(0.1초): 찾은 근거 상자가 먼저", "await W(60);const last=[...document.querySelectorAll('#chatBox .ai-message .message-content')].pop();return '근거 상자='+!!last.querySelector('.ai-src')+' 칩='+last.querySelectorAll('.ai-chip').length+' | 답 칸='+txt(last.querySelector('.ai-ans')).slice(0,30)")
    step("C3 답 끝: 모양·인용 확인·AI 호출 수",
         "for(let i=0;i<100&&app._aiHelpPending;i++)await W(100);const last=[...document.querySelectorAll('#chatBox .ai-message .message-content')].pop();const ans=last.querySelector('.ai-ans');if(!ans)return '답 칸 없음: '+txt(last).slice(0,200);"
         "const p=window.__ai[0]?.t||'';return 'AI 호출='+window.__ai.length+'번('+window.__ai.map(x=>x.kind).join(',')+') 구글 직접 호출='+JSON.stringify(window.__fetch.filter(u=>/googleapis/.test(u)).map(u=>u.split('?')[0].slice(-40)))+' | 받은 글에 [찾은 근거]='+p.includes('[찾은 근거]')+' 조문 번호='+/\\[1\\] 징계 규정\\.txt · 제12조/.test(p)+' 답 모양 규칙='+p.includes('**답**')+' | 받은 글 길이='+p.length+' | 근거칩='+[...last.querySelectorAll('.ai-chip')].map(c=>c.textContent).join(' / ')+' | ✓='+ans.querySelectorAll('.ai-q.ok').length+' 확인 필요='+ans.querySelectorAll('.ai-q.chk').length+' [번호] 단추='+ans.querySelectorAll('.ai-cite').length+' | 질문 예시 숨김='+$('aiSuggest').hidden")
    S.append({"shot": "law_chat1.png"})
    pt("const b=[...document.querySelectorAll('#chatBox .ai-src-chips')].pop().querySelector('.ai-chip');b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])")
    S.append({"clickpt": 1})
    step("D 근거 단추 누름 → 원문 창(찾은 낱말 밝게·원본 열기)", "await W(200);const m=$('lawHitModal');return '창='+!!m+' | '+txt(m?.querySelector('.lh-head'))+' | 밝힌 낱말='+(m?m.querySelectorAll('mark').length:0)+' | 원본 열기 단추='+!!m?.querySelector('[data-open]')")
    S.append({"shot": "law_hit.png"})
    S.append({"key": "Escape", "vk": 27})
    step("D2 Esc → 원문 창만 닫힘", "await W(150);return '원문 창='+!!$('lawHitModal')+' 업무파트너 그대로='+vis($('chatBox'))")
    pt("const b=[...document.querySelectorAll('#chatBox .ai-ans .ai-q.ok')].pop();b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])")
    S.append({"clickpt": 1})
    step("D3 ✓ 누름 → 같은 원문 창", "await W(200);const m=$('lawHitModal');const r='창='+!!m+' '+txt(m?.querySelector('.lh-no'));m?.remove();return r")
    step("E ChatGPT(한 번에 받기) 경로", "app.allData.provider='chatgpt';app.allData.chatgptApiKey='TEST';window.__ai=[];await app.askAIHelp('징계 의결 기한은 며칠인가요?');const last=[...document.querySelectorAll('#chatBox .ai-message .message-content')].pop();const r='AI 호출='+window.__ai.map(x=>x.kind).join(',')+' | 근거칩='+[...last.querySelectorAll('.ai-chip')].slice(0,2).map(c=>c.textContent).join(' / ')+' | ✓='+last.querySelectorAll('.ai-q.ok').length+' 확인 필요='+last.querySelectorAll('.ai-q.chk').length;app.allData.provider='gemini';return r")
    step("F 법제처 보강(가짜 응답): 질문에 「건축법」, 올린 자료엔 없음",
         "app.allData.lawApiKey='TESTOC';window.__law=[];window.fetch=async function(u,o){u=String(u);if(/law\\.go\\.kr/.test(u)){window.__law.push(u.includes('lawSearch')?'검색':'본문');const j=u.includes('lawSearch')?{LawSearch:{law:[{MST:'123','법령명한글':'건축법','시행일자':'20260701'}]}}:{'법령':{'조문':{'조문단위':[{'조문번호':'11','조문제목':'건축허가','조문여부':'조문','조문내용':'제11조(건축허가) ① 건축물을 건축하거나 대수선하려는 자는 특별자치시장ㆍ특별자치도지사 또는 시장ㆍ군수ㆍ구청장의 허가를 받아야 한다.','항':[{'항내용':'② 허가권자는 건축허가를 하기 전에 안전 기준을 확인하여야 한다.'}]},{'조문번호':'12','조문제목':'다른 일','조문여부':'조문','조문내용':'제12조(다른 일) 관계 없는 조문.'}]}}};return new Response(JSON.stringify(j),{headers:{'Content-Type':'application/json'}})}return window.__of.apply(this,arguments)};"
         "window.__ai=[];await app.askAIHelp('건축법 제11조 건축허가는 누구에게 받나요?');const last=[...document.querySelectorAll('#chatBox .ai-message .message-content')].pop();const r='법제처 부름='+window.__law.join(',')+' | 근거칩='+[...last.querySelectorAll('.ai-chip')].map(c=>c.textContent+(c.classList.contains('api')?'(현행)':'')).join(' / ')+' | 머리='+txt(last.querySelector('.ai-src-h'))+' | 받은 글에 현행 조문='+(window.__ai[0]?.t||'').includes('법제처 현행');app.allData.lawApiKey='';return r")
    step("F2 법제처 키 없으면 부르지 않음", "window.__law=[];await app.askAIHelp('건축법 제11조 건축허가는?');return '법제처 부름='+window.__law.length")
    # 길잡이
    step("G AI 길잡이: 창이 바로 열림 + 일반 길잡이와 같은 화면 + 맨 위 점검 칸",
         "app.setAiPanelView('procedure');window.__ai=[];const t0=performance.now();await app.showChecklistHelp(ID,1);const t1=performance.now();const m=document.querySelector('[id^=aiGuideModal_]');"
         "return '열리기까지 '+Math.round(t1-t0)+'ms | 머리='+txt(m.querySelector('.gd-title'))+' | 묶음='+[...m.querySelectorAll('.gd-sec-h')].map(h=>h.textContent.trim().slice(0,12)).join(' / ')+' | 예전 이모지 본문(1️⃣)='+m.textContent.includes('1️⃣')+' | 점검 칸 처음='+txt(m.querySelector('.gd-ai-body')).slice(0,40)")
    step("G2 점검 칸 채워짐: 지켜야 할 것·다른 점([업무팁 고치기])·빠진 절차·인용 확인",
         "await W(900);const m=document.querySelector('[id^=aiGuideModal_]');const b=m.querySelector('.gd-ai-body');return 'AI 호출='+window.__ai.length+' | 받은 글 조문='+/제12조/.test(window.__ai[0]?.t||'')+' | 제목들='+[...b.querySelectorAll('.gd-ai-h')].map(x=>x.textContent).join(' / ')+' | ✓='+b.querySelectorAll('.ai-q.ok').length+' 확인 필요='+b.querySelectorAll('.ai-q.chk').length+' | 고치기 단추='+!!b.querySelector('.gd-ai-fix')+' | 근거칩='+b.querySelectorAll('.ai-chip').length")
    S.append({"shot": "law_guide.png"})
    step("G3 같은 할 일 다시 열면 저장해 둔 점검(AI 다시 안 부름)",
         "document.querySelectorAll('[id^=aiGuideModal_]').forEach(x=>x.remove());window.__ai=[];await app.showChecklistHelp(ID,1);await W(300);const m=document.querySelector('[id^=aiGuideModal_]');return 'AI 호출='+window.__ai.length+' 점검 칸='+txt(m.querySelector('.gd-ai-h'))")
    pt("const b=document.querySelector('[id^=aiGuideModal_] .gd-ai-fix');const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])")
    S.append({"clickpt": 1})
    step("G4 [업무팁 고치기] → 항목 창 업무팁 탭", "await W(700);const mm=document.querySelector('[id^=main-checklist-tip-content-]');return '항목 창(업무팁 칸)='+!!mm+' | 길잡이 남음='+!!document.querySelector('[id^=aiGuideModal_]')+' | 업무팁 탭='+(document.querySelector('.modal.show .cim-tab.active,.modal.show [aria-selected=true]')?.textContent||'').trim().slice(0,10)")
    step("G5 연결 자료 없는 업무의 길잡이 → 전체에서 찾거나 안내", "const R5=await app._lawRetrieve(ID2,'보고서 쓰기');window.__r5=R5.hits.map(h=>h.no+'('+h.score+')').join(',');document.querySelectorAll('.modal.show').forEach(m=>{m.classList.remove('show')});document.querySelectorAll('[id^=aiGuideModal_]').forEach(x=>x.remove());await app.showChecklistHelp(ID2,0);await W(900);const m=document.querySelector('[id^=aiGuideModal_]');const r='점수='+window.__r5+' | '+txt(m.querySelector('.gd-ai-body')).slice(0,80);m.remove();document.body.style.position='';document.body.style.overflow='';return r")
    step("정리", "app.exitFocusMode?.();await W(500);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID&&w.id!==ID2);for(const id of window.__ids||[])await app.dbManager.deleteFile('lawLibrary',id);app._allowMassDelete=true;app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
else:
    step("잠금판: 길잡이에 점검 칸 없음 · 업무파트너 막힘",
         "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const o={text:'할 일',indent:0,completed:false,tip:{type:'text',content:'팁 글',saved:true}};app.ensureChecklistItemId(o);app.allData.workflows.unshift({id:ID,type:'manual',title:'잠금 시험',checklist:[o],date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});"
         "await app.showChecklistHelp(ID,0);const m=document.querySelector('[id^=aiGuideModal_]');const r='AI 사용 가능='+app.isAIAvailable()+' | 점검 칸='+!!m.querySelector('.gd-ai')+' | 묶음='+[...m.querySelectorAll('.gd-sec-h')].map(h=>h.textContent.trim()).join(' / ')+' | 머리='+txt(m.querySelector('.gd-title'));m.remove();document.body.style.position='';document.body.style.overflow='';"
         "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.saveData();return r")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
