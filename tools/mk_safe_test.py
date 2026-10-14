# 저장 안전장치 시험 대본 → steps3.json
# ① 켜는 중(불러오기 전) 저장은 건너뜀 ② 다른 창에서 새로 만든 업무는 지우지 않음 ③ 목록이 빈 채 저장 → 멈추고 알림, 다시 열면 그대로
# ④ 남는 것보다 많이(5개 이상) 한꺼번에 지우려 하면 멈춤 ⑤ 하나씩 지우기는 그대로 ⑥ 일부러 허락한 경우(보관·백업 복원)는 지움 ⑦ 창 두 개면 알림
# 실행: (tools 폴더에서) python mk_safe_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const db=async()=>(await app.dbManager.getAllProjects()).length;"
     "const toast=()=>{const t=document.getElementById('toast');return t&&t.classList.contains('show')?document.getElementById('toastMessage').textContent.trim():'(알림 없음)'};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})

step("준비: 업무 8개", "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));document.getElementById('welcomeModal')?.remove();"
     "for(let k=0;k<6;k++){app.allData.workflows.push({id:900100+k,type:'manual',title:'안전 시험 '+(k+1),checklist:[{text:'할 일',indent:0,completed:false}],date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});}"
     "await app.insertPracticeWorkflows();await W(1200);await app.saveDataImmediate();return '메모리='+app.allData.workflows.length+' | 저장소='+(await db())")
# ① 켜는 중 저장: 다시 열면서, 불러오기가 끝나기 전에 저장을 부름
step("A0 다시 열기", "location.reload();return 'ok'")
S.append({"label": "A 불러오기 전 저장 시도", "js": "(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));for(let i=0;i<200&&!window.app;i++)await W(10);const loaded=!!app._dataLoaded;const n=app.allData.workflows.length;await app.saveDataImmediate();return '불러오기 끝남='+loaded+' | 그때 메모리 업무='+n+' | 저장 시도함'})()"})
step("A2 다 불러온 뒤", "await W(3500);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return '메모리='+app.allData.workflows.length+' | 저장소='+(await db())")
# ② 다른 창에서 새로 만든 업무 (이 창은 모름)
step("B 다른 창이 만든 업무는 지우지 않음", "await app.dbManager.saveProject({id:424242,type:'manual',title:'다른 창에서 만든 업무',checklist:[],date:'2026. 10. 14.',createdAt:new Date().toISOString(),folderPath:''});await app.saveDataImmediate();const all=await app.dbManager.getAllProjects();return '저장 뒤에도 있음='+all.some(p=>p.id===424242)+' | 저장소='+all.length+' | 이 창 메모리='+app.allData.workflows.length")
# ③ 목록이 빈 채 저장
step("C 목록이 빈 채 저장 → 멈춤", "window.__keep=app.allData.workflows;app.allData.workflows=[];await app.saveDataImmediate();const r='저장소='+(await db())+' | 알림='+toast();app.allData.workflows=window.__keep;return r")
step("C2 다시 열면 그대로", "location.reload();return 'ok'")
step("C3", "await W(4000);document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));return '메모리='+app.allData.workflows.length+' | 저장소='+(await db())+' | 다른 창 업무 보임='+app.allData.workflows.some(w=>w.id===424242)")
# ④ 한꺼번에 많이
step("D 9개 중 7개를 한꺼번에 지우려 함 → 멈춤", "app._massDeleteWarned=false;const keep=app.allData.workflows;app.allData.workflows=keep.slice(0,2);await app.saveDataImmediate();const r='저장소='+(await db())+' | 알림='+toast().slice(0,40);app.allData.workflows=keep;await app.saveDataImmediate();return r")
# ⑤ 하나씩 지우기
step("E 하나 지우기는 그대로", "const b=await db();app.allData.workflows=app.allData.workflows.filter(w=>w.id!==900100);await app.saveDataImmediate();return '저장소 '+b+' → '+(await db())")
step("E2 영구 삭제(휴지통)도 그대로", "const b=await db();await app.permanentDeleteWorkflow(900101);await W(300);await app.saveDataImmediate();return '저장소 '+b+' → '+(await db())")
# ⑦ 창 두 개 (같은 파일을 하나 더 띄움)
step("F 같은 프로그램을 다른 창에 하나 더", "app._tabWarned=false;const f=document.createElement('iframe');f.style.cssText='position:fixed;left:-3000px;width:800px;height:600px';f.src=location.href;document.body.appendChild(f);await W(6000);return '이 창 알림='+toast().slice(0,40)+' | 새 창 알림='+(f.contentWindow.app&&f.contentWindow.app._tabWarned)")
step("F2 새 창 닫기", "document.querySelectorAll('iframe').forEach(f=>f.remove());await W(300);return 'ok'")
# ⑥ 일부러 허락 (보관 정리·백업 복원)
step("G 허락하면 지움 (보관·백업 복원과 같은 길)", "const b=await db();const keep=app.allData.workflows;app.allData.workflows=keep.filter(w=>!(w.id>=900102&&w.id<=900105));app._allowMassDelete=true;await app.saveDataImmediate();return '저장소 '+b+' → '+(await db())+' | 허락은 한 번만='+!app._allowMassDelete")
step("정리", "app.allData.workflows=app.allData.workflows.filter(w=>!/^\\[연습\\]|안전 시험|다른 창에서/.test(w.title));app._allowMassDelete=true;await app.saveDataImmediate();return '저장소='+(await db())")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
