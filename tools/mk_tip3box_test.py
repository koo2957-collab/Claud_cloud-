# 업무팁 세 칸 입력(놓치기 쉬운 것 · 업무 팁 · 근거) 시험 대본 → steps3.json
# 실제 클릭·타자로 세 칸에 쓰기 → 합친 글로 저장 · 칸끼리 옮겨도 보기 화면으로 안 바뀜 · 밖을 누르면 보기 화면 ·
# 업무 절차 패널에 빨간 상자 2줄·근거 · 예전 글(「주의:」·섞인 줄)을 세 칸에 나눠 보여 줌 · 정리 단추는 가운데만 · 창을 닫아도 저장 · 레퍼런스는 못 고침
# 실행: (tools 폴더에서) python mk_tip3box_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>/소모품/.test(w.title)&&/^\\[연습\\]/.test(w.title));"
     "const ix=t=>wf().checklist.findIndex(i=>i.text===t);const g=k=>document.getElementById('tip3-'+k+'-'+wf().id+'-'+window.__i);"
     "const tip=()=>(wf().checklist[window.__i].tip||{}).content||'';const box=()=>document.getElementById('tip3-'+wf().id+'-'+window.__i);"
     "const D=()=>document.getElementById('aiPanelOfflineDashboard');")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr, dx="Math.min(40,b.width/2)"): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음');const b=el.getBoundingClientRect();return JSON.stringify([b.left+" + dx + ",b.top+b.height/2])")})
def click(expr): pt(expr); S.append({"clickpt": 1})
def typ(t): S.append({"text": t})
def key(k, vk=0, ktext=None): S.append({"key": k, "vk": vk, **({"ktext": ktext} if ktext else {})})

step("준비", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));await app.insertPracticeWorkflows();await W(1500);app.focusWorkflow(wf().id);await W(1500);return 'ok'")
# ① 이미 쓴 업무팁(놓치기 쉬운 것 2줄 + 근거) → 보기 화면 → 누르면 세 칸에 나뉘어 들어감
step("A0 납품·검사 항목 창 업무팁 탭", "window.__i=ix('납품·검사');app.showChecklistItemModal(wf().id,window.__i,'tip');await W(800);return '보기 화면='+(document.getElementById('tip-view-'+wf().id+'-'+window.__i).style.display)+' | 세 칸='+box().style.display")
click("document.getElementById('tip-view-'+wf().id+'-'+window.__i)")
step("A 보기 화면 누름 → 세 칸에 나뉨", "await W(300);return '세 칸 보임='+box().style.display+' | 놓치기 쉬운 것='+JSON.stringify(g('warn').value)+' | 업무 팁='+JSON.stringify(g('body').value.slice(0,40))+' | 근거='+JSON.stringify(g('basis').value)+' | 칸 이름='+[...box().querySelectorAll('.tip3-lab')].map(l=>l.childNodes[1]?l.textContent.split('·')[0].trim():'').join('/')")
S.append({"shot": "tip3_a.png"})
step("A2 닫기", "app.closeChecklistItemModal();await W(500);return '바뀐 것 없음='+(tip()===wf().checklist[window.__i].tip.content)")
# ② 비어 있는 항목에 실제 타자로 세 칸 쓰기
step("B0 업무팁 없는 항목", "const k=window.__i+1;wf().checklist[k].tip={content:''};app.saveData();window.__i=k;app.showChecklistItemModal(wf().id,k,'tip');await W(800);return wf().checklist[k].text+' | 세 칸 바로 보임='+box().style.display")
S.append({"shot": "tip3_empty.png"})
step("B0b 세 칸이 스크롤 없이 다 보임", "const bx=box().getBoundingClientRect();const r=k=>g(k).getBoundingClientRect();const inside=k=>r(k).top>=bx.top-1&&r(k).bottom<=bx.bottom+1;return '놓치기 쉬운 것='+inside('warn')+' 업무 팁='+inside('body')+' 근거='+inside('basis')+' | 업무 팁 칸 높이='+Math.round(r('body').height)+' | 세 칸 스크롤='+(box().scrollHeight>box().clientHeight+1)")
click("g('warn')")
typ("검사 기한 14일 지키기"); key("Enter", 13, "\r"); typ("검사조서에 서명 받기")
click("g('body')")
typ("검사 담당자를 정해 공문으로 알립니다")
step("B1 칸을 옮겨도 고치기 화면 그대로", "await W(300);return '세 칸='+box().style.display+' | 숨은 칸='+JSON.stringify(document.getElementById('main-checklist-tip-content-'+wf().id+'-'+window.__i).value)")
click("g('basis')")
typ("지방계약법 시행령 제64조")
click("document.querySelector('#cimOverlay .mat-title')")
step("B2 밖을 누름 → 저장 · 보기 화면", "await W(900);return '저장된 글='+JSON.stringify(tip())+' | 세 칸='+box().style.display+' | 보기 빨간 상자 줄='+document.querySelectorAll('#tip-view-'+wf().id+'-'+window.__i+' .tip-warn-li').length+' | 근거 줄='+document.querySelectorAll('#tip-view-'+wf().id+'-'+window.__i+' .tip-basis-li').length")
S.append({"shot": "tip3_view.png"})
step("C 업무 절차 패널에도 빨간 상자 2줄·근거", "app.closeChecklistItemModal();await W(500);app.toggleStageOpen(wf().id,ix('납품·검사'));await W(700);const r=document.querySelector('.checklist-card[data-workflow-id=\"'+wf().id+'\"][data-index=\"'+window.__i+'\"] .item-title-text');r.scrollIntoView({block:'center'});await W(200);r.click();await W(900);const p=D();return '빨간 상자 줄='+p.querySelectorAll('.tip-warn .tip-warn-li').length+' | 근거='+[...p.querySelectorAll('.tip-basis-li')].map(x=>x.textContent).join(',')")
S.append({"key": "Escape"})
# ③ 예전 방식 글(주의: · 섞인 줄 · 근거가 가운데)도 세 칸에 나눠 보여 줌
step("D 예전 글 나누기", "const it=wf().checklist[window.__i];it.tip.content='1. 첫 순서\\n주의: 예전 표시 줄\\n2. 둘째 순서\\n⚖ 예전 근거 표시';app.saveData();app.showChecklistItemModal(wf().id,window.__i,'tip');await W(700);app.switchTipToEditMode(wf().id,window.__i);await W(200);return '놓치기 쉬운 것='+JSON.stringify(g('warn').value)+' | 업무 팁='+JSON.stringify(g('body').value)+' | 근거='+JSON.stringify(g('basis').value)+' | 고치기 전 저장 글 그대로='+(tip().startsWith('1. 첫 순서'))")
# 정리 단추는 가운데만
step("E 정리 단추(가운데 칸만)", "g('body').value='- 하나\\n\\n\\n- 둘';app._tip3Sync(wf().id,window.__i);app.organizeTipRuleBased(wf().id,window.__i);await W(300);return '업무 팁='+JSON.stringify(g('body').value)+' | 저장 글='+JSON.stringify(tip())")
# ④ 창을 닫아도 저장 (고치는 중에 ✕)
click("g('warn')")
key("End", 35); typ(" (추가)")
step("F 고치는 중 창 닫기 → 저장", "await W(200);app.closeChecklistItemModal();await W(900);return '저장 글='+JSON.stringify(tip())")
# ⑤ 레퍼런스는 고칠 수 없음
step("G 레퍼런스", "wf().isReference=true;app.saveData();app.focusWorkflow(wf().id);await W(1200);app.showChecklistItemModal(wf().id,window.__i,'tip');await W(700);app.switchTipToEditMode(wf().id,window.__i);await W(200);const r='세 칸 잠김='+[g('warn'),g('body'),g('basis')].every(t=>t&&t.disabled);app.closeChecklistItemModal();await W(400);wf().isReference=false;app.saveData();return r")
step("H 다크 모드", "document.documentElement.classList.add('dark-mode');app.focusWorkflow(wf().id);await W(1000);app.showChecklistItemModal(wf().id,window.__i,'tip');await W(700);app.switchTipToEditMode(wf().id,window.__i);await W(300);return 'ok'")
S.append({"shot": "tip3_dark.png"})
step("정리", "app.closeChecklistItemModal();document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]/.test(w.title));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
