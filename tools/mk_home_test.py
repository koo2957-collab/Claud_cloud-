# 홈(왼쪽 위 로고) 시험 대본 → steps3.json
# 확인: 목록에서 누르면 검색어 지움·맨 위로 · 일하는 화면+항목 창/길잡이에서 누르면 모두 닫고 목록으로 · 편집 중 바꾼 것 있으면 묻기([취소]=계속 편집, [저장]=저장 후 홈)
#       · 작성 중인 새 업무 창은 그 창이 묻고 멈춤 · 키보드 Enter · 페이지를 다시 읽지 않음
# 실행: (tools 폴더에서) python mk_home_test.py && node cdp3.mjs "<저장소>/index.html"
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7931;"
     "const st=()=>'일하는 화면='+!!app.focusMode+' 편집='+!!app.focusEditMode+' 열린 창='+document.querySelectorAll('.modal.show').length+' 길잡이='+document.querySelectorAll('.gd-modal').length+' 검색어=\"'+($('mainSearchInput')?.value||'')+'\" 페이지 표시='+window.__mark;")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def logo(): S.append({"pt": True, "js": P + "const r=document.querySelector('.brand-home').getBoundingClientRect();return JSON.stringify([r.x+30,r.y+r.height/2])" + E}); S.append({"clickpt": 1})
step("준비: 업무 하나 + 페이지 표시(다시 읽으면 사라짐)",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};window.__mark='그대로';"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i)=>{const o={text:t,indent:i,completed:false};app.ensureChecklistItemId(o);return o};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'홈 시험 업무',checklist:[mk('단계 하나',0),mk('할 일 하나',1),mk('할 일 둘',1)],date:'2026. 10. 15.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();app.displayWorkflows();"
     "const h=document.querySelector('.brand-home');return '로고 title='+h.title+' 커서='+getComputedStyle(h).cursor")
step("A 목록에서 검색어 넣고 아래로", "$('mainSearchInput').value='홈 시험';app.filterWorkflows();window.scrollTo(0,300);await W(200);return st()")
logo()
step("A2 로고 누름 → 검색어 지움·맨 위", "await W(700);return st()+' | 스크롤='+Math.round(window.scrollY)")
step("B 일하는 화면(창 없음)", "app.focusWorkflow(ID);await W(1200);return st()")
logo()
step("B2 로고 → 목록으로", "await W(1200);return st()")
step("C 일하는 화면 + 항목 창 → 로고는 창 배경에 가려 눌리지 않음(대화 상자 약속)", "app.focusWorkflow(ID);await W(1200);app.showChecklistItemModal(ID,1,'tip');await W(800);const r=document.querySelector('.brand-home').getBoundingClientRect();const top=document.elementFromPoint(r.x+30,r.y+r.height/2);return st()+' | 로고 위에 있는 것='+(top.closest('.brand-home')?'로고':(top.className||top.tagName))")
step("C2 (코드로 홈을 부르면) 항목 창·길잡이 모두 닫고 목록으로", "await app.showChecklistHelp(ID,1);await W(300);const a=st();app.goHome();await W(1200);return a+' → '+st()+' | 화면 고정 풀림='+(document.body.style.position==='')")
step("D 편집에서 항목 이름 바꿈", "app.focusWorkflow(ID);await W(1200);app.enterFocusEditMode();await W(600);app.allData.workflows.find(w=>w.id===ID).checklist[2].text='할 일 둘(고침)';return st()")
logo()
step("D2 로고 → 저장할지 물음", "await W(400);const d=[...document.querySelectorAll('.modal.show')].pop();window.__d=d;return st()+' | 창='+(d?d.querySelector('h2').textContent:'없음')+' 단추='+(d?[...d.querySelectorAll('button')].map(b=>b.textContent.trim()).join('/'):'')")
step("D3 [취소] → 계속 편집", "window.__d.querySelector('[data-choice=cancel]').click();await W(400);return st()")
logo()
S.append({"pt": True, "js": P + "await W(400);const b=[...document.querySelectorAll('.modal.show button')].find(x=>x.textContent.trim()==='저장');const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E})
S.append({"clickpt": 1})
step("D4 [저장] → 저장되고 목록으로", "await W(1300);return st()+' | 고친 이름 남음='+(app.allData.workflows.find(w=>w.id===ID).checklist[2].text)")
step("E 새 업무 창에 이름 적음 → (코드로) 홈", "app.openModal('manualModal');await W(700);$('manualProjectName').value='쓰는 중';$('manualProjectName').dispatchEvent(new Event('input',{bubbles:true}));app.goHome();await W(500);const d=[...document.querySelectorAll('.modal.show')].pop();return st()+' | 물음='+(d.querySelector('h2')?.textContent||'')")
step("E2 [버리기] → 정리", "const d=[...document.querySelectorAll('.modal.show')].pop();[...d.querySelectorAll('button')].find(b=>b.textContent.trim()==='버리기')?.click();await W(600);return st()")
step("F 키보드: 로고에 초점 두고 Enter", "app.focusWorkflow(ID);await W(1200);document.querySelector('.brand-home').focus();return st()")
S.append({"key": "Enter", "vk": 13})
step("F2 Enter → 목록으로", "await W(1200);return st()")
step("정리", "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.saveData();app.displayWorkflows();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
