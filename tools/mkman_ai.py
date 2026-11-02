import json, os, sys
# AI 허용판 설명서 촬영 대본 → steps_ai.json  (`ai_test .html`로: STEPS=steps_ai.json node cdp2.mjs "<ai_test .html 절대 경로>" > man2ai_out.txt)
#   오프라인판(mkman2.py)과 같은 준비(연습 업무·내 정보)를 한 뒤 AI 장면만 찍는다 → man2/ai_*.png
#   진짜 AI·키는 쓰지 않는다: callAI·업무 파트너 스트림을 가짜로 바꿔, 연습 업무에 맞춘 예시 답을 돌려줌
#   (근거 인용은 연습 업무에 붙은 법령 PDF에서 찾은 [1]번 조문의 실제 글을 옮겨 ✓가 붙게 함)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkman2 as base   # HL·W·준비 장면을 그대로 씀 (불러오면 steps.json도 다시 써지지만 내용은 같음)
W, HL = base.W, base.HL
S = []
def scene(name, code, hl=None, keepToast=False):
    ret = f"return JSON.stringify({{hl: R({hl})}})" if hl else "return JSON.stringify({hl:null})"
    S.append({"label": name, "js": "(async()=>{try{" + HL + code + ("" if keepToast else "toastOff();") + W(300) + ret + "}catch(e){return JSON.stringify({err:e.message})}})()"})
    S.append({"wait": 300, "shot": "man2/" + name + ".png"})

seed = next(s for s in base.S if s.get('label') == '00_seed')
welcome = next(s for s in base.S if s.get('label') == '00a_welcome')
S.append(welcome)   # 환영 창을 닫는 준비(찍지 않음)
S.append(dict(seed))

def J(o): return json.dumps(o, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")
# AI로 채우기 답: 「복합기 임차」 — 기준 자료(지방계약법 시행령)의 절차대로
FILL = {"items": [
    {"text": "임차 준비", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "사용 부서 요구 사항 받기 (대수·사양·기간)", "indent": 1, "warn": [], "tip": "월 출력 매수와 컬러 비율을 함께 받습니다", "basis": []},
    {"text": "추정가격 정하기 (임차 기간 전체 금액)", "indent": 1, "warn": ["임차는 계약 기간 전체 금액으로 추정가격을 정합니다"], "tip": "", "basis": ["지방계약법 시행령(2026.6.3. 시행) 제7조"]},
    {"text": "계약 방법 정하기", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "금액 기준 확인", "indent": 1, "warn": ["추정가격 2천만원 초과면 1인 견적 불가"], "tip": "", "basis": ["지방계약법 시행령(2026.6.3. 시행) 제30조"]},
    {"text": "1인 견적서 받기", "indent": 1, "warn": [], "tip": "임차 조건(유지보수·소모품 포함 여부)을 견적서에 적게 합니다", "basis": []},
    {"text": "2인 이상 견적 (나라장터 안내공고)", "indent": 1, "warn": [], "tip": "", "basis": []},
    {"text": "계약", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "배제사유 확인 · 각서 받기", "indent": 1, "warn": [], "tip": "", "basis": []},
    {"text": "임차 계약서 작성", "indent": 1, "warn": ["계약 기간·월 임차료·해지 조건을 꼭 적습니다"], "tip": "", "basis": []},
    {"text": "설치·검수", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "설치 확인·검수조서 작성", "indent": 1, "warn": [], "tip": "", "basis": []},
    {"text": "임차료 지급", "indent": 0, "warn": [], "tip": "", "basis": []},
    {"text": "월 임차료 지급 (청구일부터 5일 안)", "indent": 1, "warn": ["청구서를 받은 날부터 5일 안에 지급"], "tip": "", "basis": ["지방계약법 시행령(2026.6.3. 시행) 제67조"]}],
    "branches": [{"at": 4, "label": "2천만원 이하", "skip": [6]}]}
# 업무 파트너 답(법령): [1]번 근거의 실제 글을 인용
STUB = ("window.confirm=()=>true;app.allData.provider='gemini';app.allData.geminiApiKey='AIzaSy-example-key-0000';app._syncAiOff&&app._syncAiOff();app.updateManualAiFillButtonState&&app.updateManualAiFillButtonState();"
 "app._lawEmbedBoost=async()=>new Map();app._generateAndStoreLibraryEmbeddings=async()=>({success:false});app.checkBackupReminder=()=>{};"
 "window.__real=p=>{const m=String(p).match(/\\[1\\][^\\n]*\\n([^\\n]{16,})/);return m?m[1].trim().replace(/^[①-⑳]\\s*/,'').slice(0,40):''};"
 "window.__oid=(p,name)=>{const m=String(p).match(new RegExp('(o\\\\d+) \\\\| [^|]+\\\\| '+name.replace(/[()]/g,'\\\\$&')));return m?m[1]:'o0'};"
 "const law=p=>'**답** 추정가격이 2천만원 이하인 물품 구매는 1인 견적으로 수의계약을 할 수 있습니다 [1]. 2천만원을 넘으면 나라장터 안내공고로 2인 이상에게서 견적을 받아야 합니다.\\n**근거**\\n- [1] 「'+window.__real(p)+'」\\n**확인할 점**\\n- 추정가격은 부가가치세를 뺀 금액입니다\\n- 기관 내부 계약 지침에 더 엄격한 기준이 있는지 보세요';"
 "const write=()=>'의자 20개·책상 10개 구매와 관련하여 조달청 가격정보 등 3곳의 거래실례가격을 비교한 결과, 최저가는 13,980,000원으로 확인되었습니다. 추정가격이 2천만원 이하이므로 1인 견적에 의한 수의계약으로 추진하겠습니다.';"
 "const ans=t=>/보고서 문장으로 다듬어/.test(t)?write():law(t);"
 "app._tryGeminiChainStream=async(p,k,chain,contents,on)=>{const t=contents[contents.length-1].parts[0].text;const a=ans(t);on(a.slice(0,40),a.slice(0,40));await new Promise(r=>setTimeout(r,250));on(a,a);return a};"
 "app.callAIWithHistory=async(msgs)=>ans(msgs[msgs.length-1].content);"
 "app.callAI=app.callAIWithDocuments=async(p)=>{await new Promise(r=>setTimeout(r,300));p=String(p);"
 "if(/빠진 할 일만 찾아/.test(p))return JSON.stringify({adds:[{after:window.__oid(p,'수의계약 체결 제한 대상인지 확인'),text:'수의계약 체결 제한 대상 여부를 지방자치단체 누리집에서 확인',why:'기준 자료의 계약 상대자 확인 절차가 빠짐',warn:['계약 체결 전에 확인해야 합니다'],tip:'',basis:[],src:''},{after:window.__oid(p,'검사 결과 서면 통지'),text:'검사조서 사본을 지출 서류에 붙이기',why:'대가 지급 때 검사조서가 필요함',warn:[],tip:'',basis:[],src:''}]});"
 "if(/보충 자료의 조문을 보고/.test(p))return JSON.stringify({add:[],notes:[]});"
 "if(/다음 업무팁을 읽기 쉽게/.test(p)){const src=(p.split('[원본]')[1]||'').split('\\n').map(x=>x.trim()).filter(Boolean);return src.map(l=>/^(⚠|주의|근거)/.test(l)?l:'□ '+l.replace(/^([□○\\-·]|\\d+[.)]|[가-하][.)])\\s*/,'')).join('\\n')}"
 "if(/\\[찾은 근거\\]/.test(p)&&/must/.test(p)){const q=window.__real(p);return JSON.stringify({must:[{text:'추정가격 2천만원 이하일 때만 1인 견적서로 계약할 수 있습니다',ref:1,quote:q},{text:'견적서는 계약 상대자가 될 업체에서 직접 받습니다',ref:1,quote:q}],diff:[],missing:[{text:'견적서 받은 날짜가 계약일보다 앞서는지 확인',ref:1}]})}"
 "return '" + J(FILL) + "'};")
scene("ai_ready", STUB + "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));app.displayWorkflows();" + W(600))
S.pop()   # 준비 장면은 찍지 않음

# 1. AI 설정
scene("ai01_settings", "app.openPreferences('ai');" + W(1200), "'#prefsModal .modal-content'")
# 2. AI 길잡이 법령·매뉴얼 점검 (연습 업무 1인 견적서 받기)
scene("ai05_guide", "app.closeModal('prefsModal');" + W(300) + "app.focusWorkflow(window.__pw);" + W(1500) + "await app.showChecklistHelp(window.__pw,px('1인 견적서 받기'));"
 "for(let k=0;k<60;k++){const b=[...document.querySelectorAll('.gd-ai .gd-ai-body')].pop();if(b&&!b.querySelector('.chat-status'))break;" + W(250) + "}" + W(400) +
 "{const s=[...document.querySelectorAll('.gd-ai')].pop();const sc=s&&s.closest('.gd-scroll');if(sc)sc.scrollTop+=s.getBoundingClientRect().top-sc.getBoundingClientRect().top-12;}" + W(300),
 "[...document.querySelectorAll('.gd-ai')].pop()")
# 3. 업무 파트너: 법령 질문 → 근거 상자 + 답
scene("ai06_partner", "closeGuides();" + W(300) + "if(document.getElementById('aiPanel').classList.contains('hidden'))app.toggleAiPanel();" + W(400) + "app.setAiPanelView('chat');" + W(500) +
 "await app.askAIHelp('수의계약 1인 견적은 추정가격 얼마까지 할 수 있나요?');for(let k=0;k<60&&app._aiHelpPending;k++)" + W(200) + W(600) +
 "const cb=document.getElementById('chatBox');if(cb)cb.scrollTop=cb.scrollHeight;", "'#aiPanel'")
# 4. 업무 파트너: 글 다듬기 → [처리결과에 넣기]
scene("ai07_insert", "await app.askAIHelp('거래실례가격 조사 처리결과를 보고서 문장으로 다듬어 줘');for(let k=0;k<60&&app._aiHelpPending;k++)" + W(200) + W(600) +
 "const cb=document.getElementById('chatBox');if(cb)cb.scrollTop=cb.scrollHeight;" + W(300),
 "[...document.querySelectorAll('#chatBox .ai-message')].pop()")
# 5. 업무팁 AI로 다시 나누기 (1인 견적서 받기의 업무팁에 정리 안 된 글을 넣고)
scene("ai04_tipai", "const i=px('추정가격 정하기');const it=pw().checklist[i];it.tip={type:'text',content:['물품 수량과 규격을 먼저 정한다','조달청 가격정보와 업체 견적을 참고해 단가를 정함','부가세는 빼고 계산','주의: 2천만원 넘으면 1인 견적 불가','근거: 시행령 제7조'].join(" + base.NL + "),saved:true};app.saveData();"
 "await app.showChecklistItemModal(window.__pw,i,'tip');" + W(800) + "app.switchTipToEditMode(window.__pw,i);" + W(300) + "await app.aiOrganizeTip(window.__pw,i);" + W(800), "'#tipAiPrev .tap-box'")
# 6. AI 편집: 진행 중 업무 → 「빠진 할 일 더하기」 + 더 바라는 것
scene("ai02_edit", "app._tipAiPrevClose&&app._tipAiPrevClose();app.closeChecklistItemModal();" + W(400) + "app.enterFocusEditMode();" + W(800) + "await app.openAiRestructure(window.__pw);" + W(900) +
 "const a=document.getElementById('aiRsAsk');if(a){a.value='계약 전에 확인할 것 위주로 찾아 줘';a.dispatchEvent(new Event('input'));}", "'#aiRsModal .rs-box'")
scene("ai03_editadd", "app._aiRsStart();for(let k=0;k<60&&app._aiRs&&app._aiRs.phase!=='review';k++)" + W(200) + W(600) +
 "{const r=[...document.querySelectorAll('#aiRsModal .aip-list .aip-row')].find(x=>!x.classList.contains('fixed'));r&&r.scrollIntoView({block:'center'});}" + W(300), "'#aiRsModal .rs-box'")
# 7. 새 업무 ② AI로 체크리스트 채우기 (맨 끝 — 새 업무 창을 닫지 않아도 되게)
scene("ai08_fill", "app._aiRsClose();" + W(200) + "app.cancelFocusEditMode();" + W(600) + "{const d=[...document.querySelectorAll('.modal.show')].pop();const nb=d&&[...d.querySelectorAll('button')].find(b=>/저장 안 함/.test(b.textContent));nb&&nb.click();}" + W(600) +
 "app.exitFocusMode&&app.exitFocusMode();" + W(500) + "app.openModal('manualModal');" + W(700) + "const n=document.getElementById('manualProjectName');n.value='복합기 임차 계약 (2027년)';n.dispatchEvent(new Event('input',{bubbles:true}));app._nwGo(2);" + W(500) + "app._toggleManualAiSection();" + W(400) +
 "document.querySelector('.aif-lib-btn').click();" + W(1200) + "const fs=await app._getAllLibraryFiles();fs.filter(f=>/지방계약법/.test(f.name)).forEach(f=>app._fbPick.sel.add(f.id));app._fbPickBars('law');" + W(300) +
 "[...document.querySelectorAll('#lawLibraryModal .fb-pick-foot button')].find(b=>/연결하기/.test(b.textContent)).click();" + W(1500) +
 "const c=document.getElementById('manualContent');if(c)c.value='복합기 2대를 3년 동안 임차합니다. 추정가격 약 1,800만원(부가세 별도), 유지보수·토너 포함.';", "'#manualAiSection'")
scene("ai09_fillprev", "app.fillChecklistWithAI();for(let k=0;k<80&&document.getElementById('aiFillPreview')?.hidden!==false;k++)" + W(200) + W(800) +
 "const b=document.getElementById('aiFillPreview');b&&b.scrollIntoView({block:'start'});", "'#aiFillPreview'")
json.dump(S, open('steps_ai.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(S))
