# AI 업무 파트너 개선 시험 대본 → steps_partner.json  (AI 허용판 `ai_test .html`로 실행, 가짜 AI)
# 확인: ① 지금 할 일의 업무팁·처리결과·마감일·지난번엔 이렇게·남은 마감일을 함께 보냄 · 이어 묻기(앞 질문 낱말을 가볍게) · 주제가 바뀌면 안 보탬
#       ② 질문 종류별 답 모양(법령·글쓰기·지난 기록·진행) ③ 「지난번엔 어떻게 했나요?」 → 지난 업무 기록 상자·P번호 단추(같은 글은 한 번)
#       ④ 글 답 아래 [처리결과에 넣기]·[보고서 의견에 넣기] 실제 클릭 → [되돌리기] · 질문 예시 단추 · 보내는 글 상한·긴 앞 답 자르기
# 실행: (tools 폴더에서) python mk_partner_test.py && set STEPS=steps_partner.json && node cdp3.mjs "<저장소>/ai_test .html"
import json
RULE = "제1조(목적) 이 규정은 소방공무원 징계 절차를 정한다.\\n제12조(진술 기회) ① 징계위원회는 혐의자에게 출석 통지서를 회의 5일 전까지 보내야 한다.\\n② 진술 기회는 충분히 주어야 한다.\\n제13조(의결 기한) 징계위원회는 징계 의결 요구를 받은 날부터 30일 이내에 의결하여야 한다.\\n제14조(통보) 의결 결과는 지체 없이 알린다."
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7931,ID3=7933,ID4=7934;"
     "const txt=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';const WF=id=>app.allData.workflows.find(w=>w.id===id);"
     "const last=()=>[...document.querySelectorAll('#chatBox .ai-message .message-content')].pop();const P0=()=>(window.__ai[window.__ai.length-1]||{}).t||'';"
     "const mid=el=>{if(!el)return 'ERR 없음';el.scrollIntoView({block:'nearest'});const r=el.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
def click(): S.append({"clickpt": 1, "wait": 100})

# 가짜 AI — 받은 글 종류에 맞춰 답
STUB = ("window.__ai=[];"
        "const mk=p=>{if(p.includes('[쓰는 법'))return '□ 출석 통지서 발송\\n  ○ 2026. 11. 2. 혐의자에게 등기우편으로 보냄 [1]\\n  ○ 담당: 김철수, 회의 \"5일 전\" 기준 지킴';"
        "if(p.includes('**이번에 볼 점**'))return '**답** 지난 5월 「징계 절차(5월)」에서는 등기우편으로 보냈습니다 [P1].\\n**이번에 볼 점** \"회의 6일 전\"처럼 여유를 두세요.';"
        "if(p.includes('지금 할 일·마감일로 한두 문장'))return '**답** 지금은 「출석 통지서 보내기」 차례이고 마감은 3일 남았습니다.';"
        "const m=p.match(/\\[1\\][^\\n]*\\n([^\\n]{12,})/);const real=m?m[1].trim().replace(/^[①-⑳]\\s*/,'').slice(0,22):'없음';return '**답** 회의 5일 전까지 보내야 합니다 [1].\\n**근거**\\n- [1] 징계 규정 제12조: “'+real+'”'};"
        "app._tryGeminiChainStream=async(p,k,chain,contents,on)=>{const t=contents[contents.length-1].parts[0].text;window.__ai.push({t,n:contents.length,hist:contents.slice(0,-1).map(c=>c.parts[0].text.length)});const a=mk(t);await W(100);on(a,a);return a};")

step("준비: 진행 중 업무(업무팁·처리결과·마감일) + 지난 5월 업무(끝남) + 그 레퍼런스 사본 + 징계 규정",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};localStorage.setItem('deadlineNotifyMode','off');localStorage.setItem('authorInfoSet','1');app._collabSetMe({dept:'감사팀',rank:'소방위',name:'시험'});"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app.allData.lawApiKey='';app._syncAiOff?.();"
     "app.allData.workflows=app.allData.workflows.filter(w=>![ID,ID3,ID4].includes(w.id));"
     "const mkIt=(t,i,o={})=>{const x={text:t,indent:i,completed:false,...o};app.ensureChecklistItemId(x);return x};"
     "const d=new Date();d.setDate(d.getDate()+3);const ymd=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'징계 절차 시험',checklist:[mkIt('징계 의결 요구',0,{tip:{type:'text',content:'□ 의결 요구서 받은 날을 기록\\n⚠ 30일 기한 주의',saved:true}}),mkIt('출석 통지서 보내기',1,{deadline:ymd,tip:{type:'text',content:'회의 3일 전까지 보냅니다\\n근거: 징계 규정 제12조',saved:true},result:{text:'11/2 혐의자한테 등기로 보냄 담당 김철수',summary:''}}),mkIt('징계위원회 의결',1),mkIt('결과 통보',0),mkIt('통보서 보내기',1)],date:'2026. 10. 29.',createdAt:new Date().toISOString(),folderPath:''});"
     "const old={id:ID3,type:'manual',title:'징계 절차(5월)',completedProcessed:true,completedAt:'2026-05-20T09:00:00',checklist:[mkIt('징계 의결 요구',0,{completed:true}),mkIt('출석 통지서 보내기',1,{completed:true,completedAt:'2026-05-03T10:00:00',result:{text:'5월 3일 등기우편으로 출석 통지서 발송, 회의 6일 전',summary:''}})],date:'2026. 5. 1.',createdAt:'2026-05-01T09:00:00',folderPath:''};"
     "app.allData.workflows.push(old);app.allData.workflows.push({...JSON.parse(JSON.stringify(old)),id:ID4,isReference:true,completedProcessed:undefined,completedAt:undefined,title:'징계 절차(5월) 레퍼런스'});"
     "const ids0=(await app._getAllLibraryFiles()).filter(f=>/징계 규정/.test(f.name));for(const f of ids0)await app.dbManager.deleteFile('lawLibrary',f.id);"
     "const rule=new File([\"" + RULE + "\"],'징계 규정.txt',{type:'text/plain'});const id=await app.dbManager.saveFile('lawLibrary',{name:rule.name,type:rule.type,size:rule.size,blob:rule,uploadDate:new Date().toISOString(),groupId:null});"
     "await app._linkLibraryDocs(ID,[id]);await app.saveDataImmediate();window.__lid=id;return '업무='+WF(ID).title+' 마감='+ymd")
step("E0 질문 종류 판단·이어 묻기 판단",
     "const K=q=>q+' → '+app._aiQKind(q);const r=['출석 통지서는 며칠 전까지?','처리결과를 다듬어 줘','지금까지 진행상황을 보고 문장 3줄로 써 줘','「출석 통지서 보내기」 지난번엔 어떻게 했나요?','작년엔 어떻게 했지?','다음에 할 일은 뭐야?','이 업무에서 지켜야 할 기한·기간은?'].map(K).join(' | ');"
     "app.aiChatHistory=[{role:'user',content:'출석 통지서는 회의 며칠 전까지 보내야 하나요?'},{role:'assistant',content:'5일 전'}];"
     "const f1=app._aiFollowSoft('그럼 등기로 보내도 돼?'),f2=app._aiFollowSoft('징계위원회 의결 기한은 며칠인가요?');app.aiChatHistory=[];"
     "return r+' || 「그럼 등기로…」 앞 질문 보탬='+!!f1+' · 「징계위원회 의결 기한…」(주제 바뀜) 보탬='+!!f2")
step("E1 이어 묻기 조문 찾기: 앞 질문 없이 / 있을 때",
     "const q='그럼 그건 언제까지야?';const a=await app._lawRetrieve(ID,q);const b=await app._lawRetrieve(ID,q,{soft:'출석 통지서는 회의 며칠 전까지 보내야 하나요?'});"
     "const sh=R=>R.hits.slice(0,3).map(h=>(h.no||'본문')+'('+h.score+')').join(',')||'없음';return '없이='+sh(a)+' | 앞 질문과='+sh(b)+' 가볍게 보탠 낱말='+JSON.stringify(b.softTerms)")
step("B 업무 열고 업무 파트너 → 질문 예시 단추",
     STUB + "app.focusWorkflow(ID);await W(1200);if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(500);app.setAiPanelView('chat');await W(400);app._aiCtxRefresh();await W(100);"
     "return '질문 예시='+[...document.querySelectorAll('#aiSuggest .ai-sug')].map(b=>b.textContent).join(' / ')")
S.append({"shot": "partner0.png"})
# ③ 지난번엔 — 질문 예시 단추 실제 클릭
pt("return mid([...document.querySelectorAll('#aiSuggest .ai-sug')].find(b=>/지난번/.test(b.textContent)))"); click()
step("C1 「지난번엔 어떻게 했나요?」 단추 → 지난 업무 기록 상자·P1 단추",
     "await W(900);const L=last(),p=P0();return '받은 글: [지난 업무 기록]='+p.includes('[지난 업무 기록] —')+' P1='+(p.match(/P1\\. [^\\n]{0,60}/)||[''])[0]+' P2 있음='+/\\nP2\\./.test(p)+' 이번에 볼 점 규칙='+p.includes('**이번에 볼 점**')+' | 상자='+txt(L.querySelector('.ai-src.past'))+' | 근거 상자='+!!L.querySelector('.ai-src:not(.past)')+' | 답 P단추='+L.querySelectorAll('.ai-cite.past').length+' 확인 필요 표시='+L.querySelectorAll('.ai-q.chk').length")
S.append({"shot": "partner_past.png"})
pt("return mid(last().querySelector('.ai-ans .ai-cite.past'))"); click()
step("C1b P1 단추 → 5월 업무의 처리결과 창", "await W(700);const m=[...document.querySelectorAll('.modal.show')].pop();return '창='+(m?m.id:'없음')+' 5월 처리결과 보임='+(m?m.textContent.includes('등기우편으로 출석 통지서 발송'):false)")
S.append({"key": "Escape", "wait": 400})
step("C1c Esc로 닫힘", "await W(200);return '열린 창='+[...document.querySelectorAll('.modal.show')].map(m=>m.id).join(',')")
# ① 법령 질문(직접 타자) — 업무 자료가 함께 가는지
step("C2 법령 질문 입력", "const i=$('aiInput');i.focus();i.value='출석 통지서는 회의 며칠 전까지 보내야 하나요?';return 'ok'")
pt("document.querySelectorAll('.toast,#toast').forEach(t=>t.classList.remove('show'));return mid($('aiSendBtn'))"); click()
step("C2b 받은 글: 지금 할 일의 업무팁·처리결과·마감일·지난번·남은 마감일 · 근거 상자·✓",
     "await W(900);const L=last(),p=P0();return '업무팁='+p.includes('회의 3일 전까지 보냅니다')+' 단계 업무팁='+p.includes('30일 기한 주의')+' 처리결과='+p.includes('처리결과(적어 둔 것): 11/2')+' 마감일='+(p.match(/- 마감일: [^\\n]+/)||['없음'])[0]+' 지난번='+p.includes('지난번엔 이렇게(다른 업무의 같은 할 일): 「징계 절차(5월)」')+' 남은 마감일 목록='+p.includes('[마감일이 있는 남은 할 일]')+' 법령 답 모양='+p.includes('[답하는 모양 — 꼭 지킴]\\n**답** 결론')+' | 받은 글 길이='+p.length+' 앞 대화='+window.__ai[window.__ai.length-1].n+'개 | 근거칩='+[...L.querySelectorAll('.ai-chip')].map(c=>txt(c)).join(' / ')+' ✓='+L.querySelectorAll('.ai-q.ok').length+' 넣기 단추='+L.querySelectorAll('.ai-act').length")
# 이어 묻기(직접 타자)
step("C3 이어 묻기 입력", "const i=$('aiInput');i.focus();i.value='그럼 그건 언제까지야?';return 'ok'")
pt("document.querySelectorAll('.toast,#toast').forEach(t=>t.classList.remove('show'));return mid($('aiSendBtn'))"); click()
step("C3b 이어 묻기: 앞 질문 보고 제12조 찾음",
     "await W(900);const L=last(),p=P0();return '근거칩='+[...L.querySelectorAll('.ai-chip')].map(c=>txt(c)).join(' / ')+' | 받은 글 [1]='+(p.match(/\\[1\\] [^\\n]+/)||['없음'])[0]+' | 앞 대화 '+window.__ai[window.__ai.length-1].n+'개'")
# ④ 글쓰기 — 처리결과 다듬기
step("C4 글쓰기 입력", "const i=$('aiInput');i.focus();i.value='처리결과를 다듬어 줘';return 'ok'")
pt("document.querySelectorAll('.toast,#toast').forEach(t=>t.classList.remove('show'));return mid($('aiSendBtn'))"); click()
step("C4b 글 답: 머리말 규칙·넣기 단추 두 개·따옴표 확인 표시 없음",
     "await W(900);const L=last(),p=P0();return '쓰는 법 규칙='+p.includes('[쓰는 법 — 꼭 지킴]')+' 법령 답 모양 안 붙음='+!p.includes('**답** 결론')+' 처리결과 원문 감='+p.includes('11/2 혐의자한테')+' | 근거 상자='+!!L.querySelector('.ai-src')+' | 단추='+[...L.querySelectorAll('.ai-act')].map(b=>txt(b)).join(' / ')+' | 확인 필요='+L.querySelectorAll('.ai-q.chk').length+' | 근거 없는 [1] 글자 남음='+/\\[1\\]/.test(txt(L.querySelector('.ai-ans')))")
S.append({"shot": "partner_write.png"})
pt("return mid(last().querySelector('.ai-act.res'))"); click()
step("C4c [처리결과에 넣기] → 바뀜·알림",
     "await W(500);const it=WF(ID).checklist[1];const t=[...document.querySelectorAll('.toast')].map(x=>txt(x)).pop()||'';return '처리결과='+JSON.stringify(it.result.text)+' | [1] 빠짐='+!/\\[1\\]/.test(it.result.text)+' | 알림='+t.slice(0,60)")
pt("const b=[...document.querySelectorAll('.toast button')].reverse().find(x=>/되돌리기/.test(x.textContent));return mid(b)"); click()
step("C4d [되돌리기] → 원래 처리결과", "await W(500);return '처리결과='+JSON.stringify(WF(ID).checklist[1].result.text)")
pt("return mid(last().querySelector('.ai-act:not(.res)'))"); click()
step("C4e [보고서 의견에 넣기]", "await W(500);const pr=app.checklistDetails['project-'+ID]?.progressReport;return '의견='+JSON.stringify((pr?.edits?.op||'').slice(0,60))")
pt("const b=[...document.querySelectorAll('.toast button')].reverse().find(x=>/보고서 열기/.test(x.textContent));return mid(b)"); click()
step("C4f [보고서 열기] → 보고서에 의견 보임", "await W(1500);const m=[...document.querySelectorAll('.modal.show')].pop();return '창='+(m?m.id:'없음')+' 의견 보임='+(m?m.textContent.includes('혐의자에게 등기우편으로 보냄'):false)+' (의견 줄='+(m?txt([...m.querySelectorAll('.pr-ed')].find(e=>/등기우편/.test(e.textContent))).slice(0,50):'')+')'")
S.append({"key": "Escape", "wait": 500})
step("C4g 의견 지우기(되돌리기 대신 Ctrl+Z 시험 준비)", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));document.activeElement?.blur?.();return 'ok'")
S.append({"key": "z", "vk": 90, "mods": 2, "wait": 400})
step("C4h Ctrl+Z → 의견 되돌림", "await W(300);const pr=app.checklistDetails['project-'+ID]?.progressReport;return '의견 있음='+!!(pr?.edits&&Object.prototype.hasOwnProperty.call(pr.edits,'op'))")
# 진행 질문
step("C5 진행 질문", "await app.askAIHelp('다음에 할 일은 뭐야?');const L=last(),p=P0();return '진행 답 모양='+p.includes('지금 할 일·마감일로 한두 문장')+' 근거 상자='+!!L.querySelector('.ai-src')+' 넣기 단추='+L.querySelectorAll('.ai-act').length+' | 답='+txt(L.querySelector('.ai-ans')).slice(0,40)")
# 보내는 글 크기
step("D 보내는 글 상한·긴 앞 답 자르기",
     "app.aiChatHistory.push({role:'user',content:'긴 답 시험'},{role:'assistant',content:'가'.repeat(5000)});const m=app.buildChatMessages('x');const mx=Math.max(...m.filter(x=>x.role==='assistant').map(x=>x.content.length));"
     "const all=window.__ai.map(x=>x.t.length+x.hist.reduce((a,b)=>a+b,0));return '앞 답 최대 길이='+mx+' | 보낸 글(앞 대화 포함) 길이들='+all.join(',')+' 최대 '+Math.max(...all)+' (상한 18000)'")
step("F 레퍼런스 업무에서는 넣기 단추 없음", "return '레퍼런스='+JSON.stringify(app._aiActHtml(WF(ID4),'글'))+' · 보통 업무 단추 수='+(app._aiActHtml(WF(ID),'글').match(/ai-act/g)||[]).length")
step("정리", "app.exitFocusMode?.();await W(400);app.allData.workflows=app.allData.workflows.filter(w=>![ID,ID3,ID4].includes(w.id));delete app.checklistDetails['project-'+ID];await app.dbManager.deleteFile('lawLibrary',window.__lid);app._allowMassDelete=true;app.allData.geminiApiKey='';await app.saveDataImmediate();document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return 'ok'")
json.dump(S, open('steps_partner.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
