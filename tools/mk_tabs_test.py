# 오른쪽 패널 「업무 절차 | 업무 파트너」 글자 탭 · 「이 할 일 묻기」 · 「지금 할 일 ›」 · 답 도착 점 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_tabs_test.py && node cdp3.mjs "<저장소>/ai_test .html"   (가짜 AI)
#       배포판: python mk_tabs_test.py locked && node cdp3.mjs "<저장소>/index.html"   (탭 없음·「업무 절차」 제목만·묻기 단추 없음)
import json, os, sys
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7961;"
     "const vis=el=>!!el&&el.offsetParent!==null;const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';"
     "const hd=()=>{const h=document.querySelector('#aiPanel .ai-panel-header');return '머리: 탭='+(vis($('aiPanelViewTabs'))?[...document.querySelectorAll('.ai-panel-view-tab')].map(b=>b.textContent.trim()+(b.classList.contains('active')?'(고름)':'')).join('|'):'숨김')+' 제목='+(vis($('aiPanelTitleText'))?tx($('aiPanelTitleText')):'숨김')+' 넘침='+(h.scrollWidth>h.clientWidth)};"
     "const view=()=>'보는 화면='+app.aiPanelViewMode+' 점='+(vis($('aiPanelChatDot'))?'●':'없음');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(sel_js): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const b=" + sel_js + ";b.scrollIntoView({block:'nearest'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E}); S.append({"clickpt": 1})
STUB = ("window.__wait=150;app._tryGeminiChainStream=async(p,k,chain,contents,on)=>{await W(window.__wait);const a='**답** 회의 5일 전까지입니다.';on(a,a);return a};")
step("준비: 업무 열고 오른쪽 패널(업무 절차)",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     + ("" if LOCKED else "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB) +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'탭 시험 업무',checklist:[mk('징계 의결 요구',0),mk('출석 통지서 보내기',1,'회의 5일 전까지 보냅니다'),mk('징계위원회 의결',1)],date:'2026. 10. 15.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();"
     "app.focusWorkflow(ID);await W(1300);if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(400);app.setAiPanelView('procedure');await W(500);"
     "return hd()+' | '+view()+' | 이 할 일 묻기='+tx(document.querySelector('.proc-ask'))")
S.append({"shot": "tabs_proc.png"})
if LOCKED:
    step("배포판: 넓게 보기에서도 머리 넘침 없음", "app.toggleProcWide();await W(500);const r=hd();app.toggleProcWide();await W(400);return r")
else:
    click("document.querySelector('.proc-ask')")
    step("A 「✨ 이 할 일 묻기」 → 업무 파트너 + 그 할 일 질문 단추", "await W(400);return hd()+' | '+view()+' | 줄='+tx($('aiNowLine'))+' | 질문='+[...document.querySelectorAll('#aiSuggest .ai-sug')].map(b=>b.textContent).join(' / ')+' 보임='+vis($('aiSuggest'))+' | 입력칸 초점='+(document.activeElement===$('aiInput'))")
    S.append({"shot": "tabs_chat.png"})
    click("document.querySelector('#aiSuggest .ai-sug')")
    step("A2 질문 단추 누름 → 답, 질문 단추 거둠·줄은 그대로", "for(let i=0;i<50&&app._aiHelpPending;i++)await W(100);await W(200);const last=[...document.querySelectorAll('#chatBox .user-message .message-content')].pop();return '보낸 질문='+tx(last)+' | 질문 단추 보임='+vis($('aiSuggest'))+' | 줄='+tx($('aiNowLine'))")
    click("$('aiNowLine')")
    step("A3 「업무 절차에서 보기 ›」 → 업무 절차 탭", "await W(500);return view()+' | '+hd()")
    step("B 업무 절차를 보는 동안 답이 옴 → 탭에 점", "app.setAiPanelView('chat');window.__wait=1200;const p=app.askAIHelp('기한은?');await W(150);app.setAiPanelView('procedure');await p;await W(200);window.__wait=150;return view()")
    S.append({"shot": "tabs_dot.png"})
    click("$('aiPanelTabChat')")
    step("B2 「업무 파트너」 탭 누름 → 점 사라짐", "await W(300);return view()")
    step("C 지금 할 일이 아닌 줄에서 묻기(01-2) → 줄에 그 할 일", "app.askAboutItem(ID,2);await W(400);return view()+' | 줄='+tx($('aiNowLine'))")
    click("$('aiNowLine')")
    step("C2 줄 누름 → 업무 절차 + 그 줄을 골라 보여 줌", "await W(700);const it=app.allData.workflows.find(w=>w.id===ID).checklist[2];return view()+' | 고른 줄=' +(app._clPeek&&app._clPeek.itemId===it.itemId?'01-2 징계위원회 의결':JSON.stringify(app._clPeek))")
    step("D 넓게 보기에서 머리 넘침 없음 · 키 빼면 탭 숨김", "app.toggleProcWide();await W(500);const a=hd();app.toggleProcWide();await W(400);app.allData.geminiApiKey='';app.updateAIPanelAvailabilityUI();await W(300);return '넓게: '+a+' || 키 뺌: '+hd()+' | 이 할 일 묻기='+tx(document.querySelector('.proc-ask'))")
step("정리", "app._aiAskItem=null;app.exitFocusMode?.();await W(500);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
