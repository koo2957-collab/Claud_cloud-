# 업무 파트너 「Gemini 스트리밍 응답 시간 초과」 고침 시험 → steps3.json (통신만 가짜, 진짜 askAIHelp → 체인 → callGeminiStream)
# 확인: 생각 모델에 생각 요약(includeThoughts) 요청 · 생각 요약이 오는 동안 끊기지 않고 「깊이 생각하는 중 · n초」 · 요약은 답에 안 섞임
#       · 아무 응답 없으면 남은 생각 모델은 건너뛰고 Lite로 다시 물음(알림·모델 이름) · 요약을 못 받는 모델(400)은 요약 없이 같은 모델로
#       · 모두 늦으면 쉬운 말 오류 · 답이 오다 끊기면 Lite로 넘기지 않음(답 두 번 섞임 방지)
# 시간은 짧게: 첫 글자 1.5초 · 끊김 1초 (실제 60초 · 30초)
# 실행: (tools 폴더에서) python mk_stream_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);const ID=7991;"
     "const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';"
     "const last=()=>{const m=[...document.querySelectorAll('#chatBox .chat-message')].pop();return m};"
     "const res=()=>{const m=last();return '답='+tx(m?.querySelector('.ai-ans')||m?.querySelector('.message-content')).slice(0,70)+' | 이름표='+tx(m?.querySelector('.message-label'))};"
     "const reqs=()=>window.__req.map(r=>r.m.replace('gemini-','')+(r.th?'+요약':'')).join(' → ');"
     "const toast=()=>window.__toasts.join(' / ')||'없음';"
     "const ask=async q=>{window.__req=[];window.__toasts=[];window.__seen=[];const p=app.askAIHelp(q);"
     "for(let i=0;i<120&&app._aiHelpPending;i++){await W(100);const st=last()?.querySelector('.chat-status-text');if(st&&!window.__seen.includes(st.textContent))window.__seen.push(st.textContent)}await p;await W(200)};")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
# 가짜 통신: 모델마다 window.__mode[모델] 대로
FETCH = ("if(!window.__of)window.__of=window.fetch;window.__mode={};"
         "window.fetch=async(u,o)=>{u=String(u);if(/^(data|blob):/.test(u))return window.__of(u,o);"
         "if(!u.includes(':streamGenerateContent'))return new Response('{}',{status:404});"
         "const m=u.match(/models\\/([^:]+):/)[1];const body=JSON.parse(o.body);const th=!!body.generationConfig?.thinkingConfig?.includeThoughts;"
         "window.__req.push({m,th,cfg:!!body.generationConfig?.thinkingConfig});const mode=window.__mode[m]||'ok';const sig=o.signal;"
         "const ab=()=>new DOMException('aborted','AbortError');"
         "if(mode==='silent')return new Promise((_,no)=>sig.addEventListener('abort',()=>no(ab())));"
         "if(mode==='nothought400'&&th)return new Response('{\"error\":{\"code\":400}}',{status:400});"
         "const ev=o=>'data: '+JSON.stringify({candidates:[{content:{parts:o}}]})+'\\n\\n';const enc=new TextEncoder();"
         "const plan=mode==='think'?[...Array(6)].map((_,i)=>[400,ev([{text:'**Checking article '+i+'**',thought:true}])]).concat([[100,ev([{text:'**답** 회의 5일 전까지 '}])],[100,ev([{text:'보냅니다.'}])]])"
         ":mode==='partial'?[[100,ev([{text:'**답** 회의 5일'}])],[999999,'']]:[[100,ev([{text:'**답** ('+m+') 회의 5일 전까지 보냅니다.'}])]];"
         "const rs=new ReadableStream({async start(c){sig.addEventListener('abort',()=>{try{c.error(ab())}catch(e){}});"
         "for(const [ms,t] of plan){await new Promise(r=>setTimeout(r,ms));if(sig.aborted)return;if(t)c.enqueue(enc.encode(t))}c.close()}});"
         "return new Response(rs,{status:200,headers:{'Content-Type':'text/event-stream'}})};")
step("준비: 생각 모델(3.8 Flash+사고)로 묻게 · 시간 짧게",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app.allData.lawApiKey='';app._syncAiOff?.();" + FETCH +
     "window.__req=[];window.__toasts=[];const ot=app.showToast.bind(app);app.showToast=(a,b,c,...r)=>{window.__toasts.push(String(c));return ot(a,b,c,...r)};"
     "app._streamTimeouts=[1500,1000];app.resolveAIConfig=()=>({model:'gemini-3.8-flash',thinking:true,thinkingBudget:1024,temperature:0.1});"
     "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const mk=(t,i)=>{const o={text:t,indent:i,completed:false};app.ensureChecklistItemId(o);return o};"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'응답 시간 시험',checklist:[mk('징계 의결 요구',0),mk('출석 통지서 보내기',1)],date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});await app.saveDataImmediate();"
     "app.focusWorkflow(ID);await W(1300);if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(400);app.setAiPanelView('chat');await W(400);return 'ok'")
step("A 생각만 2.4초(첫 글자 기다림 1.5초보다 김) → 끊기지 않고 같은 모델이 답",
     "window.__mode={'gemini-3.8-flash':'think'};await ask('출석 통지 기한은?');"
     "return res()+' | 요청='+reqs()+' | 보인 상태='+window.__seen.filter(t=>/생각/.test(t)).slice(-1)[0]+' | 요약 섞임='+/Checking/.test(tx(last()))+' | 알림='+toast()")
S.append({"shot": "stream_think.png"})
step("B 생각 모델이 아무 응답 없음 → 남은 생각 모델 건너뛰고 Lite로 다시",
     "window.__mode={'gemini-3.8-flash':'silent'};await ask('징계 의결 기한은?');return res()+' | 요청='+reqs()+' | 알림='+toast()")
S.append({"shot": "stream_lite.png"})
step("C 생각 요약을 못 받는 모델(400) → 같은 모델로 요약 없이",
     "app._noThoughtModels=null;window.__mode={'gemini-3.8-flash':'nothought400'};await ask('통지서 서식은?');const r=res()+' | 요청='+reqs()+' | 알림='+toast();"
     "await ask('한 번 더');return r+' || 다음 질문 요청='+reqs()")
step("D 모두 응답 없음 → 쉬운 말 오류",
     "app._noThoughtModels=null;['gemini-3.8-flash','gemini-3.5-flash-lite','gemini-3.1-flash-lite','gemini-2.5-flash-lite'].forEach(m=>window.__mode[m]='silent');await ask('기한은?');return res()+' | 요청='+reqs()")
step("E 답이 오다가 끊김 → Lite로 넘기지 않음(답 섞임 없음)",
     "window.__mode={'gemini-3.8-flash':'partial'};await ask('기한은?');return res()+' | 요청='+reqs()")
step("F 생각 없는 모델(Lite 직접) → 요약 요청 안 붙음 · 그대로 답",
     "window.__mode={};app.resolveAIConfig=()=>({model:'gemini-3.5-flash-lite',thinking:false,temperature:0.1});await ask('기한은?');return res()+' | 요청='+reqs()")
step("정리", "app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);app.allData.geminiApiKey='';await app.saveDataImmediate();if(window.__of)window.fetch=window.__of;return 'ok'")
json.dump(S, open('steps3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(S), '단계')
