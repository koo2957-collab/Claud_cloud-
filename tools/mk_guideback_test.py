# 길잡이 → 항목 창에서 고치기 → 닫으면 길잡이로 돌아오기 시험 대본 → steps3.json
# 확인: [업무팁 고치기](AI 칸)·[항목 창에서 고치기](아래 단추) → 항목 창 → 닫기(Esc)·저장하고 닫기 → 같은 할 일 길잡이 다시 열림·고친 업무팁 보임
#       · (AI) 안 고쳤으면 예전 점검 그대로(AI 안 부름) · 고쳤으면 AI 안 부르고 「업무팁이 바뀌었습니다 [다시 점검]」+흐린 예전 결과 → [다시 점검] 누르면 한 번 부름
#       · 항목 창에서 홈으로 가면 돌아오지 않음
# 실행: (tools 폴더에서) python mk_guideback_test.py && node cdp3.mjs "<저장소>/ai_test .html"  /  python mk_guideback_test.py locked && node cdp3.mjs "<저장소>/index.html"
import json, os, sys
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7951;"
     "const gm=()=>document.querySelector('.gd-modal');const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';"
     "const st=()=>'[gd수='+document.querySelectorAll('.gd-modal').length+' cim수='+document.querySelectorAll('#cimOverlay').length+' ret='+JSON.stringify(app._guideReturn||null)+'] 길잡이='+(gm()?tx(gm().querySelector('.gd-title')):'닫힘')+' 항목 창='+!!$('cimOverlay')+' AI 부름='+(window.__ai||0);")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(sel_js): S.append({"pt": True, "js": P + "const b=" + sel_js + ";b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E}); S.append({"clickpt": 1})
STUB = "window.__ai=0;app.callAI=async(p)=>{window.__ai++;await W(150);return JSON.stringify({must:[{text:'통지서는 회의 5일 전까지',ref:1,quote:''}],diff:[{text:'업무팁의 3일 전은 규정과 다름',ref:1,quote:''}],missing:[]})};"
step("준비", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     + ("" if LOCKED else "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();" + STUB) +
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i,tip)=>{const o={text:t,indent:i,completed:false};if(tip)o.tip={type:'text',content:tip,saved:true};app.ensureChecklistItemId(o);return o};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'돌아오기 시험',checklist:[mk('징계 의결 요구',0),mk('출석 통지서 보내기',1,'회의 3일 전까지 보냅니다'),mk('징계위원회 의결',1)],date:'2026. 10. 15.',createdAt:new Date().toISOString(),folderPath:''});"
     + ("" if LOCKED else "const f=new File(['제12조(진술 기회) 징계위원회는 출석 통지서를 회의 5일 전까지 보내야 한다.'],'징계 규정 시험.txt',{type:'text/plain'});window.__lid=await app.dbManager.saveFile('lawLibrary',{name:f.name,type:f.type,size:f.size,blob:f,uploadDate:new Date().toISOString(),groupId:null});await app._linkLibraryDocs(ID,[window.__lid]);") +
     "await app.saveDataImmediate();await app.showChecklistHelp(ID,1);await W(900);return st()")
if not LOCKED:
    click("gm().querySelector('.gd-ai-fix')")
    step("A [업무팁 고치기] → 항목 창", "await W(900);return st()")
    S.append({"key": "Escape", "vk": 27})
    step("A2 안 고치고 Esc → 길잡이로 돌아옴, 예전 점검 그대로", "await W(1200);return st()+' | 바뀜 안내='+!!gm()?.querySelector('.gd-ai-changed')+' | 점검 칸='+tx(gm()?.querySelector('.gd-ai-h'))")
click("[...gm().querySelectorAll('button')].find(b=>b.textContent.trim()==='항목 창에서 고치기')")
step("B [항목 창에서 고치기] → 항목 창, 업무팁을 「5일 전」으로 고침", "await W(900);const t=document.querySelector('[id^=main-checklist-tip-content-]');t.value='회의 5일 전까지 보냅니다';return st()")
S.append({"key": "Escape", "vk": 27})
step("B2 닫음 → 길잡이로 돌아옴·고친 업무팁 보임" + ("" if LOCKED else "·AI 안 부르고 안내"),
     "await W(1200);const g=gm();return st()+' | 업무팁='+tx(g?.querySelector('.gd-tip'))+' | 바뀜 안내='+tx(g?.querySelector('.gd-ai-changed'))+' | 예전 결과 흐림='+(g?.querySelector('.gd-ai-old')?getComputedStyle(g.querySelector('.gd-ai-old')).opacity:'없음')")
S.append({"shot": "guideback.png"})
if not LOCKED:
    click("gm().querySelector('.gd-ai-changed .mat-btn')")
    step("B3 [다시 점검] → AI 한 번 부름, 안내 사라짐", "await W(900);return st()+' | 바뀜 안내='+!!gm().querySelector('.gd-ai-changed')+' | 점검 칸='+tx(gm().querySelector('.gd-ai-h'))")
    step("B4 닫고 다시 열면 새 점검 그대로(AI 안 부름)", "document.querySelectorAll('.gd-modal').forEach(m=>m.remove());await app.showChecklistHelp(ID,1);await W(600);return st()+' | 바뀜 안내='+!!gm().querySelector('.gd-ai-changed')")
if not LOCKED:
    click("gm().querySelector('.gd-ai-re')")
    step("E1 같은 창에서 「다시 점검」 글자 누름 → AI 한 번 더", "await W(900);return st()+' | 점검 칸='+tx(gm().querySelector('.gd-ai-h'))")
    step("E2 길잡이 닫고 다시 열기(저장된 점검)", "document.querySelectorAll('.gd-modal').forEach(m=>m.remove());await app.showChecklistHelp(ID,1);await W(600);return st()")
    click("gm().querySelector('.gd-ai-re')")
    step("E3 다시 연 창에서 「다시 점검」 글자 누름 → AI 한 번 더", "await W(900);return st()+' | 점검 칸='+tx(gm().querySelector('.gd-ai-h'))")
click("[...gm().querySelectorAll('button')].find(b=>b.textContent.trim()==='항목 창에서 고치기')")
step("C 항목 창에서 홈으로 가면", "await W(900);const a=st();app.goHome();await W(1300);return a+' → '+st()")
step("D 길잡이 없이 연 항목 창은 닫아도 길잡이 안 열림", "app.showChecklistItemModal(ID,1,'tip');await W(800);app.closeChecklistItemModal();await W(600);return st()")
step("정리", "document.querySelectorAll('.gd-modal').forEach(m=>m.remove());document.body.style.position='';document.body.style.overflow='';app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);if(window.__lid)await app.dbManager.deleteFile('lawLibrary',window.__lid);app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
