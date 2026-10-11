# 내보내기에서 업무팁 예시·사진 빼기: 저장은 묻지 않고 바로, 알림에 「예시·사진 n개 포함」 + [예시·사진 빼고 다시 저장] — 시험 대본 → steps3.json
# (내보내기·공유·업무 분담 요청 파일 모두 같은 함수) 실행: (tools 폴더에서) python mk_tipexclude_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const buy=()=>app.allData.workflows.find(w=>w.isPractice&&!w.isDeleted&&w.title.includes('소모품'));"
     "const toast=()=>{const t=[...document.querySelectorAll('.toast')].pop();return t?t.textContent.replace(/\\s+/g,' ').trim():'없음'};"
     "const act=()=>[...document.querySelectorAll('.toast button')].find(b=>b.textContent.includes('빼고 다시 저장'));"
     "const tips=p=>Object.entries(p.attachmentsData||{}).filter(([k])=>/-t-/.test(k)).reduce((n,[,v])=>n+v.length,0);")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})

step("seed", "window.confirm=()=>true;localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "await app.insertPracticeWorkflows();await W(2500);window.__files=[];app._saveFileWithPicker=async(b,n)=>{window.__files.push({n,t:await b.text()});return true;};"
     "app.focusWorkflow(buy().id);await W(1500);return 'ok'")
pt("const b=[...document.querySelectorAll('button, .fap-btn')].find(x=>x.textContent.trim()==='내보내기'&&x.offsetParent);const r=b.getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 2500})
step("A [내보내기] → 묻지 않고 저장 · 알림에 예시·사진 개수와 [빼고 다시 저장]", "const f=window.__files[0];const p=JSON.parse(f.t);return '저장 수='+window.__files.length+' 파일='+f.n+' | 예시·사진 들어감='+tips(p)+' | 알림='+toast().slice(-80)+' | 단추='+!!act()")
pt("const r=act().getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1, "wait": 2500})
step("B [예시·사진 빼고 다시 저장] → 두 번째 파일에는 예시·사진 없음", "const f=window.__files[1];const p=JSON.parse(f.t);const keep=Object.keys(p.attachmentsData||{}).length;"
     "return '저장 수='+window.__files.length+' | 예시·사진='+tips(p)+' | 서식·법령은 그대로='+(p.repoDocumentsData.files.length)+'/'+(p.lawLibraryData.files.length)+' | 업무팁 글은 그대로='+p.workflows[0].checklist.filter(i=>i.tip&&i.tip.content).length+' | 알림='+toast().slice(-40)+' | 또 단추='+!!act()")
step("C 이 PC의 예시·사진은 그대로", "const k=Object.keys(app.checklistDetails).filter(k=>k.startsWith(buy().id+'-t-'));return '남은 예시='+k.reduce((n,x)=>n+(app.checklistDetails[x].attachments||[]).length,0)")
step("D 예시·사진이 없는 업무는 단추 없음", "const rep=app.allData.workflows.find(w=>w.isPractice&&!w.isDeleted&&w.title.includes('월간'));await app.exportMultipleWorkflowPackages([rep.id]);await W(800);return '알림='+toast().slice(0,40)+' | 단추='+!!act()")
step("정리", "app.exitFocusMode?.();app.allData.workflows.filter(w=>w.isPractice).forEach(w=>w.isDeleted=true);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
