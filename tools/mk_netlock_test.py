# 외부 통신 잠금: 배포판(index.html)은 외부 서버로 나가는 fetch·XHR을 막고, 이 PC 안의 파일·data:·blob:은 그대로 — 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_netlock_test.py && node cdp3.mjs <index.html 경로>   (시험판은 "<ai_test .html 경로>")
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})

step("A 잠금 상태", "return '잠금='+NET_LOCKED+' | 안내 보임='+(document.getElementById('aiPolicyLock').style.display!=='none')")
step("B 외부 AI 주소 fetch", "try{await fetch('https://api.openai.com/v1/models');return '나감(잠금 아님)';}catch(e){return '막힘: '+e.message}")
step("C 법제처 주소 fetch", "try{await fetch('https://www.law.go.kr/DRF/lawSearch.do?target=law');return '나감(잠금 아님)';}catch(e){return '막힘: '+e.message}")
step("D XHR 외부", "try{const x=new XMLHttpRequest();x.open('GET','https://generativelanguage.googleapis.com/');return '열림(잠금 아님)';}catch(e){return '막힘: '+e.message}")
step("E fetch 바꿔치기 시도", "const f0=window.fetch;try{window.fetch=()=>1;}catch(e){}const ok=window.fetch.toString().includes('isLocalUrl')||!NET_LOCKED;if(!NET_LOCKED)window.fetch=f0;return '그대로='+ok;return '그대로='+(window.fetch.toString().includes('isLocalUrl')||!NET_LOCKED)")
step("F 이 PC 안 파일·data:·blob:은 됨", "const a=await (await fetch('data:text/plain,ok')).text();const b=await (await fetch(URL.createObjectURL(new Blob(['ok2'])))).text();let c='';try{c=(await (await fetch('./vendor/pdf.min.js')).text()).length>1000?'ok3':'짧음';}catch(e){c='file 막힘/불가: '+e.message}return a+','+b+','+c")
step("G AI 키가 있어도 AI 안 씀", "const k=app.allData.chatgptApiKey,p=app.allData.provider;app.allData.provider='chatgpt';app.allData.chatgptApiKey='sk-test';const r=app.isAIAvailable();app.allData.provider=p;app.allData.chatgptApiKey=k;return 'isAIAvailable='+r")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
