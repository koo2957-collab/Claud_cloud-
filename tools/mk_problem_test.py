# 오류 기록 · 문제 보고 파일 시험 → steps3.json
# 오류가 나면 기록됨(같은 오류 연달아는 한 줄·횟수) · 환경설정 → 정보에 건수 · [문제 보고 파일 만들기] → 파일에 업무 제목·내용이 없음 · [기록 지우기]
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message}})()"
S = []
def step(l, b): S.append({"label": l, "js": P + b + E, "nocheck": True})
step("준비", "localStorage.setItem('welcomeShown','1');document.getElementById('welcomeModal')?.remove();localStorage.removeItem('appErrorLog');window.__dl=[];app._downloadJsonFile=(o,n)=>window.__dl.push({o,n});await app.insertPracticeWorkflows();await W(2500);return '업무='+app.allData.workflows.length")
step("오류 일으키기(같은 것 3번 + 다른 것 1번 + 처리 안 된 약속)", "for(let k=0;k<3;k++)setTimeout(()=>{throw new Error('시험 오류 A')},0);setTimeout(()=>{throw new Error('시험 오류 B')},10);Promise.reject(new Error('시험 거부'));await W(500);const L=app._errLogGet();return '줄='+L.length+' · '+L.map(x=>x.k+':'+x.m+(x.n?'×'+x.n:'')+' @'+x.at).join(' | ')")
step("환경설정 → 정보", "app.openPreferences('about');await W(600);const t=document.querySelector('#prefsModal').textContent.replace(/\\s+/g,' ');const i=t.indexOf('오류 기록');return t.slice(i,i+150)")
S.append({"shot": "problem_about.png"})
step("[문제 보고 파일 만들기]", "[...document.querySelectorAll('#prefsModal button')].find(b=>/문제 보고 파일/.test(b.textContent)).click();await W(1500);const d=window.__dl.pop();const s=JSON.stringify(d.o);const titles=app.allData.workflows.map(w=>w.title);const leak=titles.filter(t=>s.includes(t)).length+app.allData.workflows.flatMap(w=>w.checklist.map(i=>i.text)).filter(t=>t.length>6&&s.includes(t)).length;return '파일='+d.n+' · 오류='+d.o.errors.length+' · 업무 수='+d.o.counts.workflows+' · 점검='+d.o.issues.length+' · 제목·할 일 글이 들어감='+leak")
step("[기록 지우기]", "[...document.querySelectorAll('#prefsModal button')].find(b=>/기록 지우기/.test(b.textContent)).click();await W(600);return '남은 기록='+app._errLogGet().length+' · 화면='+document.querySelector('#prefsModal').textContent.includes('기록된 오류가 없습니다')")
step("정리", "app.closeModal('prefsModal');return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
