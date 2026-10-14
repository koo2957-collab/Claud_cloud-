# 새 업무 ② 절차 「AI로 체크리스트 채우기」 시험 대본 → steps3.json  (AI 허용판 `ai_test .html`로 실행)
# 「Tab 한 번으로 할 일」 안내가 AI 칸을 가리지 않음 · PDF를 끌어다 놓은 뒤 안내막이 남지 않음 · 파일 고르기로도 첨부 ·
# 다른 곳에 놓으면 참고 자료로(안내막은 꺼짐) · AI 키가 없을 때 안내 문구 (배포판은 「보안정책」, 허용판은 「AI 키를 넣어 주세요」)
# 실행: (tools 폴더에서) python mk_aifill_test.py && node cdp3.mjs "<저장소>/ai_test .html"
#       배포판 문구 확인: python mk_aifill_test.py locked && node cdp3.mjs <저장소>/index.html
import json, os, sys
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ov=()=>$('gDropOverlay').classList.contains('on');"
     "const pdf=n=>new File([new Blob(['%PDF-1.4\\n1 0 obj<<>>endobj\\ntrailer<<>>\\n%%EOF'],{type:'application/pdf'})],n||'지침.pdf',{type:'application/pdf'});"
     "const drag=(el,type,f)=>{const dt=new DataTransfer();if(f)dt.items.add(f);const r=el.getBoundingClientRect();el.dispatchEvent(new DragEvent(type,{bubbles:true,cancelable:true,dataTransfer:dt,clientX:r.left+10,clientY:r.top+10}));};"
     "const hit=el=>{const r=el.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return !!t&&(t===el||el.contains(t))};"
     "const toast=()=>{const t=$('toast');return t&&t.classList.contains('show')?$('toastMessage').textContent.trim():'(알림 없음)'};"
     "const over=(a,b)=>{const x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return !(x.right<y.left||x.left>y.right||x.bottom<y.top||x.top>y.bottom)};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr): S.append({"pt": True, "js": J("const el=" + expr + ";if(!el)throw new Error('대상 없음');const b=el.getBoundingClientRect();return JSON.stringify([b.left+b.width/2,b.top+b.height/2])")})
def click(expr): pt(expr); S.append({"clickpt": 1})

if len(sys.argv) > 1 and sys.argv[1] == 'locked':
    step("배포판: AI 키 없음 → 보안정책 안내", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();const ok=app.checkApiKey();await W(200);return '통신 잠금='+(typeof NET_LOCKED!=='undefined'&&NET_LOCKED)+' | 결과='+ok+' | 알림='+toast()+' | AI 칸 보임='+getComputedStyle($('manualAiSectionWrapper')).display")
else:
    step("준비: 새 업무 ② 절차 (처음이라 Tab 안내가 뜸)", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();localStorage.removeItem('tipNwTab');"
         "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app.openModal('manualModal');await W(800);app.updateManualAiFillButtonState();$('manualProjectName').value='AI 채우기 시험';app._nwGo(2);await W(900);"
         "const tip=$('nwTabTip');return 'Tab 안내='+!!tip+' | 안내 위치=절차 안내 줄 안('+!!(tip&&tip.closest('.nw-sticky'))+') | AI 칸 보임='+getComputedStyle($('manualAiSectionWrapper')).display")
    click("$('manualAiToggleBtn')")
    step("A AI 칸 펼침 → Tab 안내가 AI 칸을 가리지 않음", "await W(300);const tip=$('nwTabTip'),w=$('manualAiSectionWrapper');return 'Tab 안내 있음='+!!tip+' | AI 칸과 겹침='+(tip?over(tip,w):false)+' | [AI로 채우기] 누를 수 있음='+hit($('manualAiFillBtn'))+' | PDF 칸 누를 수 있음='+hit($('docDropZone'))")
    S.append({"shot": "aif_open.png"})
    step("B 파일을 끌고 창 위를 지나감 → 안내막", "drag(document.querySelector('.nw-pane[data-pane=\"2\"] .nw-sticky'),'dragover',pdf());await W(100);return '안내막='+ov()")
    step("C AI 칸(PDF)으로 옮김 → 안내막 꺼짐", "drag($('docDropZone'),'dragover',pdf());await W(100);return '안내막='+ov()")
    step("D PDF를 놓음 → 첨부 · 안내막 없음", "drag($('docDropZone'),'drop',pdf());await W(1200);return '안내막='+ov()+' | 첨부='+app.uploadedFiles.map(f=>f.name).join(',')+' | 참고 자료로 잘못 감='+((app._nw&&app.allData.workflows.find(w=>w.id===app._nw.wfId))?JSON.stringify((app.checklistDetails['project-'+app._nw.wfId]||{}).linkedLibraryDocs||[]):'[]')")
    S.append({"shot": "aif_dropped.png"})
    step("E 파일 고르기로도 첨부", "const inp=$('manualDocUpload');const dt=new DataTransfer();dt.items.add(pdf('공문.pdf'));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));await W(1200);return '첨부='+app.uploadedFiles.map(f=>f.name).join(',')")
    step("F 절차 쪽(AI 칸 밖)에 놓으면 참고 자료로 · 안내막은 꺼짐", "const it=$('checklistItems');drag(it,'dragover',pdf('참고.pdf'));await W(100);const on=ov();drag(it,'drop',pdf('참고.pdf'));await W(1500);return '놓기 전 안내막='+on+' | 놓은 뒤 안내막='+ov()+' | 알림='+toast().slice(0,30)")
    step("G 스크롤해도 Tab 안내는 「Tab」 아래에 따라감", "localStorage.removeItem('tipNwTab');$('nwTabTip')?.remove();app._nwTabTip();await W(100);const b=document.querySelector('#manualModal .nw-body');b.scrollTop=200;await W(200);const tip=$('nwTabTip'),k=document.querySelector('#manualModal .nw-keys span:nth-child(2)');const d=tip.getBoundingClientRect().top-k.getBoundingClientRect().bottom;return 'Tab 아래 거리='+Math.round(d)+'px | AI 칸과 겹침='+over(tip,$('manualAiSectionWrapper'))")
    step("G2 [알겠어요] → 닫힘·기억", "$('nwTabTip').querySelector('button').click();await W(100);return '안내='+!!$('nwTabTip')+' | 기억='+localStorage.getItem('tipNwTab')")
    step("H AI 키가 없을 때(허용판) → 키를 넣어 달라는 안내 + AI 연결 설정", "app.allData.geminiApiKey='';$('manualContent').value='징계 절차';const ok=app.checkApiKey();await W(400);const r='결과='+ok+' | 알림='+toast()+' | 설정 창='+($('prefsModal')?.classList.contains('show'))+' | 분류='+app._prefsTab;app.closeModal('prefsModal');return r")
    S.append({"shot": "aif_nokey.png"})
    step("정리", "app.closeModal?.('manualModal');app.uploadedFiles=[];app.allData.workflows=app.allData.workflows.filter(w=>!/AI 채우기 시험/.test(w.title||''));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
