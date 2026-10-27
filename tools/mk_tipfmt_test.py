# 업무팁 표시 통일(기호 = 단계) · [정리 ▾] 시험 대본 → steps3.json
#   항목 창·길잡이·업무 절차 패널이 같은 기호·같은 단계로 · 정리(기호 맞추기) 실제 클릭·[되돌리기]
#   ▾ AI로 다시 나누기(가짜 AI): 미리 보기·원문과 다른 낱말 알림·Esc·[넣기]·[되돌리기] · 업무 파트너 답도 같은 표시
# 실행: (tools 폴더에서) python mk_tipfmt_test.py && node cdp3.mjs "<저장소>/ai_test .html"
#       배포판: python mk_tipfmt_test.py locked && node cdp3.mjs "<저장소>/index.html"   (▾ 없음 · 정리는 그대로)
import json, os, sys
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
ID = 7971
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=" + str(ID) + ";"
     "const NL=String.fromCharCode(10);const wf=()=>app.allData.workflows.find(w=>w.id===ID);const tip=()=>wf().checklist[1].tip?.content||'';"
     "const vis=el=>!!el&&el.offsetParent!==null;const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';"
     "const syms=root=>root?[...root.querySelectorAll('.tol-li')].map(li=>li.querySelector('.tol-m').textContent+li.style.getPropertyValue('--d')).join(' '):'(없음)';")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(sel_js): S.append({"pt": True, "js": P + "const b=" + sel_js + ";b.scrollIntoView({block:'nearest'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E}); S.append({"clickpt": 1})
J = lambda lines: "[" + ",".join(json.dumps(l, ensure_ascii=False) for l in lines) + "].join(NL)"
T = J(["⚠ 출석 통지는 회의 5일 전까지", "□ 징계 의결 요구", "  ○ 요구서 작성", "    - 비위 사실", "  ○ 처분권자 결재", "1. 일정 잡기", "  가. 위원 연락", "메모 한 줄", "근거: 징계 규정 제2조"])
M = J(["- 하나", "* 둘", "    • 둘 아래", "", "", "주의: 기한 넘기지 말 것", "- 근거: 행정절차법 제21조"])
TIDY = J(["⚠ 기한 넘기지 말 것", "□ 하나", "□ 둘", "  ○ 둘 아래", "근거: 행정절차법 제21조"])
AI_BAD = J(["⚠ 기한을 넘기지 말 것", "□ 하나", "  ○ 둘", "    - 둘 아래", "근거: 행정절차법 제21조"])
AI_OK = J(["⚠ 기한 넘기지 말 것", "□ 하나", "  ○ 둘", "    - 둘 아래", "근거: 행정절차법 제21조"])
AI_OK_FINAL = J(["⚠ 기한 넘기지 말 것", "□ 하나", "  ○ 둘", "    - 둘 아래", "근거: 행정절차법 제21조"])
ANS = J(["**답** 출석 통지는 회의 5일 전까지 보냅니다.", "", "**근거**", "- [1] 징계 규정 제2조: “회의 5일 전까지”", "", "□ 통지서 작성", "  ○ 위원 명단 확인", "⚠ 기한을 넘기면 다시 통지"])

step("준비: 업무 만들고 열기(지금 할 일에 업무팁)",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};localStorage.setItem('deadlineNotifyMode','off');"
     + ("" if LOCKED else "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();") +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i)=>{const o={text:t,indent:i,completed:false};app.ensureChecklistItemId(o);return o};"
     "const cl=[mk('징계 준비',0),mk('출석 통지',1),mk('위원회',1)];cl[1].tip={type:'text',content:" + T + ",saved:true};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'업무팁 표시 시험',checklist:cl,date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();"
     "app.focusWorkflow(ID);await W(1300);if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(400);app.setAiPanelView?.('procedure');await W(600);return 'ok'")
step("A 업무 절차 패널: 적은 기호 그대로·기호로 단계(□0 ○1 -2, 1.0 가.1) · ▸● 덧붙임 없음",
     "const d=document.querySelector('#aiPanelOfflineDashboard .proc-step-detail');return '기호='+syms(d)+' | 빨간 상자='+!!d?.querySelector('.tip-warn')+' 근거='+!!d?.querySelector('.tip-basis')+' | 글에 ▸●='+/[▸●]/.test(tx(d?.querySelector('.tol')))")
S.append({"shot": "tipfmt_panel.png"})
step("B 항목 창 업무팁: 패널과 같은 기호·단계 · 1단계 굵게",
     "await app.showChecklistItemModal(ID,1,'tip');await W(700);const v=$('tip-view-'+ID+'-1');const top=v.querySelector('.tol-top .tol-t');return '기호='+syms(v)+' | 굵게='+getComputedStyle(top).fontWeight+' | 정리 단추='+tx($('tip-tidy-'+ID+'-1'))+' ▾='+!!document.querySelector('#cimOverlay .tip-tidy-more')")
S.append({"shot": "tipfmt_cim.png"})
step("C 길잡이: 같은 기호·단계",
     "app.closeChecklistItemModal();await W(500);await app.showChecklistHelp(ID,1);await W(1300);const m=[...document.querySelectorAll('.gd-tip')].pop();const r='기호='+syms(m);"
     "[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>!/_(content|closeBtn|footerCloseBtn)$/.test(x.id)).forEach(x=>x.remove());document.body.style.overflow='';document.body.style.position='';await W(300);return r")
step("D 준비: 어지러운 글로 바꾸고 항목 창",
     "wf().checklist[1].tip.content=" + M + ";app.saveData();await app.showChecklistItemModal(ID,1,'tip');await W(700);return JSON.stringify(tip())")
click("$('tip-tidy-'+ID+'-1')")
step("D2 [정리] 실제 클릭 → 기호 맞추기(보고서식)·주의:/근거: 제 칸·빈 줄 하나 · [되돌리기] 알림",
     "await W(500);const t=[...document.querySelectorAll('.toast')].map(x=>tx(x)).filter(Boolean).pop()||'';return '같음='+(tip()===" + TIDY + ")+' | 글='+JSON.stringify(tip())+' | 보기='+vis($('tip-view-'+ID+'-1'))+' | 알림='+t")
click("[...document.querySelectorAll('.toast-undo-btn')].pop()")
step("D3 [되돌리기] → 원래 글", "await W(400);return '원래대로='+(tip()===app._tip3Combine(splitTipSections(" + M + ").warn.join(NL),splitTipSections(" + M + ").body,splitTipSections(" + M + ").basis.join(NL))||tip()===" + M + ")+' | 보기 기호='+syms($('tip-view-'+ID+'-1'))")
if LOCKED:
    step("배포판: ▾ 없음", "return '▾='+!!document.querySelector('#cimOverlay .tip-tidy-more')")
else:
    step("E 준비: 가짜 AI(글자 하나 바꿈)", "window.__ai=" + AI_BAD + ";app.callAI=async()=>{await W(150);return window.__ai};return 'ok'")
    click("document.querySelector('#cimOverlay .tip-tidy-more')")
    step("E2 ▾ 메뉴", "await W(300);return [...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')].map(x=>tx(x)).join(' / ')")
    click("[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')][1]")
    step("E3 AI로 다시 나누기 → 미리 보기 · 다른 낱말 알림 · 아직 안 바뀜",
         "for(let i=0;i<30&&!$('tipAiPrev');i++)await W(100);const m=$('tipAiPrev');return '미리 보기='+vis(m?.querySelector('.tap-box'))+' | 머리='+tx(m?.querySelector('.tap-head'))+' | 다른 곳='+tx(m?.querySelector('.tap-diff'))+' | 글 그대로='+(tip()===app._tip3Combine(splitTipSections(" + M + ").warn.join(NL),splitTipSections(" + M + ").body,splitTipSections(" + M + ").basis.join(NL))||tip()===" + M + ")")
    S.append({"shot": "tipfmt_prev.png"})
    S.append({"key": "Escape"})
    step("E4 Esc → 미리 보기만 닫힘 · 글 그대로 · 항목 창은 남음", "await W(300);return '미리 보기='+!!$('tipAiPrev')+' | 항목 창='+!!$('cimOverlay')+' | 글 그대로='+(tip()===app._tip3Combine(splitTipSections(" + M + ").warn.join(NL),splitTipSections(" + M + ").body,splitTipSections(" + M + ").basis.join(NL))||tip()===" + M + ")")
    step("F 준비: 가짜 AI(글자 그대로)", "window.__ai=" + AI_OK + ";return 'ok'")
    click("document.querySelector('#cimOverlay .tip-tidy-more')")
    click("[...document.querySelectorAll('#fbCtxMenu .wfm-ctx-item')][1]")
    step("F2 미리 보기 「글자는 원문 그대로」", "for(let i=0;i<30&&!$('tipAiPrev');i++)await W(100);return tx($('tipAiPrev')?.querySelector('.tap-head'))")
    click("$('tipAiPrevOk')")
    step("F3 [넣기] → 바뀜 · [되돌리기] 알림", "await W(500);return '같음='+(tip()===" + AI_OK_FINAL + ")+' | 글='+JSON.stringify(tip())+' | 알림='+([...document.querySelectorAll('.toast')].map(x=>tx(x)).filter(Boolean).pop()||'')")
    click("[...document.querySelectorAll('.toast-undo-btn')].pop()")
    step("F4 [되돌리기] → 원래 글", "await W(400);return '원래대로='+(tip()===app._tip3Combine(splitTipSections(" + M + ").warn.join(NL),splitTipSections(" + M + ").body,splitTipSections(" + M + ").basis.join(NL))||tip()===" + M + ")")
    step("G 업무 파트너 답: 기호 줄·⚠은 업무팁과 같은 표시",
         "app.closeChecklistItemModal();await W(500);app.setAiPanelView('chat');await W(300);window.__ans=" + ANS + ";app._tryGeminiChainStream=async(p,k,chain,contents,on)=>{await W(100);on(window.__ans,window.__ans);return window.__ans};"
         "await app.askAIHelp('출석 통지 기한은?');for(let i=0;i<50&&app._aiHelpPending;i++)await W(100);const a=[...document.querySelectorAll('#chatBox .ai-ans')].pop();"
         "return '기호='+syms(a)+' | 빨간 상자='+!!a?.querySelector('.tip-warn')+' | ul 목록='+a?.querySelectorAll('ul').length+' | 굵게='+[...a.querySelectorAll('strong')].map(x=>x.textContent).join(',')")
    S.append({"shot": "tipfmt_chat.png"})
    step("H AI 길잡이 점검 목록: 보라 「-」·다른 점은 빨간 상자",
         "const u=document.createElement('ul');u.className='gd-ai-list';u.innerHTML='<li>가</li>';const w=document.createElement('ul');w.className='gd-ai-list warn';w.innerHTML='<li>나</li>';document.body.append(u,w);"
         "const r='기호='+getComputedStyle(u.firstChild,'::before').content+' 색='+getComputedStyle(u.firstChild,'::before').color+' | 다른 점 테두리='+getComputedStyle(w).borderLeftColor+' 목록 점='+getComputedStyle(u).listStyleType;u.remove();w.remove();return r")
step("정리", "app.closeChecklistItemModal?.();app.exitFocusMode?.();await W(500);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
