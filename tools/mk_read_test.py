# 길잡이 순서·AI 회색 상자 / 참고 자료 4개 이상 접기 / 「가」 읽는 글 크기 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_read_test.py && node cdp3.mjs "<저장소>/ai_test .html"   (가짜 AI)
#       배포판: python mk_read_test.py locked && node cdp3.mjs "<저장소>/index.html"   (AI 칸 없음, 나머지 같음)
import json, os, sys
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7941;"
     "const gm=()=>document.querySelector('.gd-modal');const z=el=>el?getComputedStyle(el).zoom:'(없음)';"
     "const secs=()=>[...gm().querySelectorAll('.gd-scroll .gd-sec-h')].map(h=>h.textContent.replace(/\\s+/g,' ').trim().slice(0,10)).join(' → ');"
     "const refs=()=>{const s=[...gm().querySelectorAll('.gd-sec')].find(x=>/참고 자료/.test(x.querySelector('.gd-sec-h').textContent));const v=[...s.querySelectorAll('.gd-card')].filter(c=>c.offsetParent);return '보이는 자료='+v.length+'('+v.map(c=>c.textContent.trim().replace('.txt','').slice(-4)).join(',')+')'+' 단추=\"'+(s.querySelector('.gd-ref-more')?.textContent||'없음')+'\"'};"
     "const closeG=()=>{document.querySelectorAll('.gd-modal').forEach(m=>m.remove());document.body.style.position='';document.body.style.overflow='';};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(sel_js): S.append({"pt": True, "js": P + "const b=" + sel_js + ";b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E}); S.append({"clickpt": 1})
STUB = "app.callAI=async(p)=>{await W(150);return JSON.stringify({must:[{text:'통지서는 5일 전까지',ref:1,quote:''}],diff:[],missing:[]})};"
step("준비: 업무팁 있는 할 일 + 참고 자료 5개(법령·매뉴얼 TXT)",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};localStorage.removeItem('gdRefOpen');localStorage.removeItem('readScale');app._applyReadScale();"
     + ("" if LOCKED else "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB) +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'글자 시험 업무',checklist:[mk('징계 의결 요구',0),mk('출석 통지서 보내기',1,'⚠ 회의 5일 전까지 보냅니다\\n통지서는 등기로 보냅니다\\n근거: 징계 규정 제12조'),mk('징계위원회 의결',1)],date:'2026. 10. 15.',createdAt:new Date().toISOString(),folderPath:''});"
     "const ids=[];for(let i=1;i<=5;i++){const f=new File(['제12조(진술 기회) 출석 통지서는 회의 5일 전까지 보낸다. 자료 '+i],'참고 규정 '+i+'.txt',{type:'text/plain'});ids.push(await app.dbManager.saveFile('lawLibrary',{name:f.name,type:f.type,size:f.size,blob:f,uploadDate:new Date().toISOString(),groupId:null}));}"
     "await app._linkLibraryDocs(ID,ids);await app._loadLinkedLibraryMeta?.(ID);await app.saveDataImmediate();window.__ids=ids;return 'AI='+app.isAIAvailable()+' 자료='+ids.length")
step("A 길잡이 순서: 업무팁 먼저 → AI 점검(회색) → 참고 자료",
     "await app.showChecklistHelp(ID,1);await W(900);const ai=gm().querySelector('.gd-ai');return '순서='+secs()+' | AI 칸 바탕='+(ai?getComputedStyle(ai).backgroundColor:'(없음)')+' 안쪽 근거 상자 바탕='+(ai?.querySelector('.ai-src')?getComputedStyle(ai.querySelector('.ai-src')).backgroundColor:'(없음)')+' | 읽기 글에 AI 칸='+app._ttsPrepareText(gm().querySelector('.ai-guide-tts-body')).includes('법령·매뉴얼 점검')")
S.append({"shot": "read_guide1.png"})
step("B 참고 자료 5개 → 처음 3개", "return refs()")
click("gm().querySelector('.gd-ref-more')")
step("B2 「2개 더 보기」 누름 → 5개·접기, 기억", "await W(200);return refs()+' | 기억='+localStorage.getItem('gdRefOpen')")
step("B3 길잡이 다시 열면 펼친 채", "closeG();await app.showChecklistHelp(ID,1);await W(500);return refs()")
click("gm().querySelector('.gd-ref-h')")
step("B4 묶음 머리 누름 → 다시 3개", "await W(200);return refs()+' | 기억='+localStorage.getItem('gdRefOpen')")
step("C 글자 크기 전: 업무팁 글 크기", "const rb=gm().querySelector('.rd-btn');window.__rb0='단추 글자='+rb.textContent+' 켜짐='+rb.classList.contains('on')+' 알림 글='+rb.title+' 옆 ⤢와 간격='+Math.round(rb.nextElementSibling.getBoundingClientRect().left-rb.getBoundingClientRect().right)+'px | ';const t=gm().querySelector('.gd-tip');window.__fs0=t.getBoundingClientRect().height;return window.__rb0+'줌='+z(gm().querySelector('.gd-scroll > *'))+' 업무팁 높이='+Math.round(window.__fs0)")
click("gm().querySelector('.rd-btn')")
step("C2 「가」 누름 → 4단계 메뉴", "await W(200);const m=$('fbCtxMenu');return '메뉴='+[...m.querySelectorAll('.wfm-ctx-item')].map(x=>x.textContent.replace(/\\s+/g,' ').trim()).join(' / ')")
S.append({"shot": "read_menu.png"})
click("[...$('fbCtxMenu').querySelectorAll('.wfm-ctx-item')].find(x=>/크게/.test(x.textContent)&&!/아주/.test(x.textContent))")
step("C3 「크게」 → 길잡이 글 115%·머리는 그대로", "await W(300);const t=gm().querySelector('.gd-tip');return '줌='+z(gm().querySelector('.gd-scroll > *'))+' 업무팁 높이 '+Math.round(window.__fs0)+'→'+Math.round(t.getBoundingClientRect().height)+' | 머리 줌='+z(gm().querySelector('.gd-title'))+' | 기억='+localStorage.getItem('readScale')+' | 단추 글자='+gm().querySelector('.rd-btn').textContent+' 켜짐='+gm().querySelector('.rd-btn').classList.contains('on')+' 바탕='+getComputedStyle(gm().querySelector('.rd-btn')).backgroundColor+' 알림 글='+gm().querySelector('.rd-btn').title")
S.append({"shot": "read_guide2.png"})
step("D 일하는 화면 업무 절차 패널", "closeG();app.focusWorkflow(ID);await W(1300);if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(400);app.setAiPanelView('procedure');await W(400);const c=$('aiPanelOfflineDashboard').firstElementChild;const fb=$('aiPanelFontBtn');return '패널 「가」 단추 보임='+!!fb.offsetParent+' 글자='+fb.textContent+' 켜짐='+fb.classList.contains('on')+' 바탕='+getComputedStyle(fb).backgroundColor+' 알림 글='+fb.title+' | 패널 줌='+z(c)")
S.append({"shot": "read_panel.png"})
step("D2 넓게 보기 켜면 곱해짐(1.1×1.15)", "app.toggleProcWide();await W(500);const r='넓게+크게 줌='+z($('aiPanelOfflineDashboard').firstElementChild);app.toggleProcWide();await W(400);return r")
click("$('aiPanelFontBtn')")
click("[...$('fbCtxMenu').querySelectorAll('.wfm-ctx-item')].find(x=>/아주 크게/.test(x.textContent))")
step("D3 패널 「가」 → 아주 크게(130%)", "await W(300);return '패널 줌='+z($('aiPanelOfflineDashboard').firstElementChild)")
step("E 환경설정 → 일반 「읽는 글 크기」", "app.openPreferences('general');await W(600);const row=[...document.querySelectorAll('.prefs-row')].find(r=>/읽는 글 크기/.test(r.textContent));return '칸='+!!row+' 고른 것='+(row?.querySelector('.prefs-choice .on')?.textContent||'')")
click("[...[...document.querySelectorAll('.prefs-row')].find(r=>/읽는 글 크기/.test(r.textContent)).querySelectorAll('.prefs-choice button')].find(b=>b.textContent==='보통')")
step("E2 「보통」 → 패널 원래대로", "await W(300);const row=[...document.querySelectorAll('.prefs-row')].find(r=>/읽는 글 크기/.test(r.textContent));const r='고른 것='+row.querySelector('.prefs-choice .on').textContent+' 패널 단추 켜짐='+$('aiPanelFontBtn').classList.contains('on')+' 알림 글='+$('aiPanelFontBtn').title+' | 패널 줌='+z($('aiPanelOfflineDashboard').firstElementChild)+' 기억='+localStorage.getItem('readScale');app.closeModal('prefsModal');return r")
step("정리", "app.exitFocusMode?.();await W(500);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);for(const id of window.__ids||[])await app.dbManager.deleteFile('lawLibrary',id);localStorage.removeItem('readScale');localStorage.removeItem('gdRefOpen');app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
