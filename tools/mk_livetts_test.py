# AI 음성안내 라이브 모델 보강 시험 대본 → steps3.json
# TTS 모델 4개를 다 쓰면(429) 라이브 음성 모델(웹소켓)로 이어 읽고, 그것도 안 되면 기본 음성.
# 가짜 통신: fetch(모델 목록·TTS 429)와 WebSocket(setupComplete → 음성 조각 → turnComplete)을 흉내 냄
# 실행: (tools 폴더에서) python mk_livetts_test.py && node cdp3.mjs "<저장소>/ai_test .html"
#       배포판: python mk_livetts_test.py locked && node cdp3.mjs "<저장소>/index.html"   (웹소켓 막힘 → 라이브 음성 없음)
import json, os, sys
LOCKED = len(sys.argv) > 1 and sys.argv[1] == 'locked'
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);"
     "const vis=el=>!!el&&el.offsetParent!==null;const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(sel_js): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const b=" + sel_js + ";b.scrollIntoView({block:'nearest'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E}); S.append({"clickpt": 1})

# 가짜 통신: window.__lv 에 기록. __lv.fail = 실패시킬 라이브 모델 이름 목록(1008로 닫음), __lv.ttsOk = TTS가 성공할지
MOCK = r"""
window.__lv={ttsCalls:[],setups:[],sent:[],fail:[],ttsOk:false,toasts:[]};
const _st=app.showToast.bind(app);app.showToast=(t,i,m,...r)=>{window.__lv.toasts.push(m);return _st(t,i,m,...r)};
const nf=window.__nativeFetch||window.fetch;window.__nativeFetch=nf;
const pcmB64=(sec)=>{const n=Math.round(24000*sec)*2;const u=new Uint8Array(n);for(let i=0;i<n;i+=2){const v=Math.round(Math.sin(i/2*2*Math.PI*440/24000)*3000);u[i]=v&255;u[i+1]=(v>>8)&255}let s='';for(let i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s)};
window.fetch=async(u,o)=>{u=String(u&&u.url||u);if(/^(data|blob):/.test(u))return nf(u,o);
 if(/models\?pageSize=1&/.test(u))return new Response('{"models":[]}',{status:200});
 if(/models\?pageSize=1000/.test(u))return new Response(JSON.stringify({models:[
   {name:'models/gemini-3.8-flash',supportedGenerationMethods:['generateContent']},
   {name:'models/gemini-3.8-live-preview',supportedGenerationMethods:['bidiGenerateContent']},
   {name:'models/gemini-3.5-transcribe-live',supportedGenerationMethods:['bidiGenerateContent']},
   {name:'models/gemini-3.8-live-extended-thinking',supportedGenerationMethods:['bidiGenerateContent']},
   {name:'models/gemini-2.5-flash-native-audio-preview-12-2025',supportedGenerationMethods:['bidiGenerateContent']}]}),{status:200});
 if(/tts.*:generateContent/.test(u)){window.__lv.ttsCalls.push(u.split('/models/')[1].split(':')[0]);
   if(window.__lv.ttsOk)return new Response(JSON.stringify({candidates:[{content:{parts:[{inlineData:{mimeType:'audio/L16;rate=24000',data:pcmB64(0.4)}}]}}]}),{status:200});
   return new Response('{}',{status:429});}
 return new Response('{}',{status:404});};
class FakeWS{constructor(url){this.url=url;this.readyState=0;setTimeout(()=>{this.readyState=1;this.onopen&&this.onopen()},30)}
 send(d){const m=JSON.parse(d);const L=window.__lv;
  if(m.setup){L.setups.push(m.setup);const mdl=m.setup.model.replace('models/','');this._mdl=mdl;
    if(L.fail.includes(mdl)){setTimeout(()=>{this.readyState=3;this.onclose&&this.onclose({code:1008,reason:'model not found'})},30);return}
    setTimeout(()=>this.onmessage&&this.onmessage({data:new Blob([JSON.stringify({setupComplete:{}})])}),30);return}
  if(m.clientContent){L.sent.push({model:this._mdl,text:m.clientContent.turns[0].parts[0].text});
    [0,1,2].forEach(i=>setTimeout(()=>this.onmessage&&this.onmessage({data:JSON.stringify({serverContent:{modelTurn:{parts:[{inlineData:{mimeType:'audio/pcm;rate=24000',data:pcmB64(0.3)}}]}}})}),40+i*20));
    setTimeout(()=>{this.onmessage&&this.onmessage({data:JSON.stringify({serverContent:{turnComplete:true},usageMetadata:{totalTokenCount:321}})})},120);}}
 close(){if(this.readyState===3)return;this.readyState=3;setTimeout(()=>this.onclose&&this.onclose({code:1000,reason:''}),10)}}
try{window.WebSocket=FakeWS}catch(e){}
app._ttsLiveList=null;app._ttsNet=null;app._ttsExhausted=new Map();app._ttsCache=new Map();
const dur=async(url)=>{const a=new Audio(url);await new Promise(r=>{a.onloadedmetadata=r;a.onerror=r;setTimeout(r,3000)});return Math.round(a.duration*10)/10};window.__dur=dur;
"""
MOCK_JS = MOCK.replace('\n', '')

step("준비: 키 넣고 업무 열기·업무 파트너 패널",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();"
     "const ID=7963;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const o={text:'할 일',indent:0,completed:false};app.ensureChecklistItemId(o);"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'음성 시험 업무',checklist:[o],date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();app.focusWorkflow(ID);await W(1300);"
     "if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(400);app.setAiPanelView?.('chat');await W(400);"
     + MOCK_JS + "return '패널 열림='+!$('aiPanel').classList.contains('hidden')+' | 웹소켓 바꿈='+(window.WebSocket.name)")
if LOCKED:
    step("배포판: 라이브 음성 없음(웹소켓 막힘)",
         "let r;try{r=await app._ttsGenerateLive('시험');}catch(e){r='예외 '+e.message}return '결과='+r+' | 웹소켓='+(window.WebSocket.name||'막힘')")
else:
    step("A 라이브 모델 고르기: 음성 대화 먼저, 받아쓰기·번역·깊은 생각 모델 뺌",
         "return (await app._ttsLiveModels('TEST-KEY')).join(' > ')")
    step("B TTS 4개 모두 429 → 라이브 음성으로 읽을 음성 만들기",
         "const url=await app._ttsGenerateGemini('출석 통지서는 회의 5일 전까지 보냅니다.');const L=window.__lv;"
         "return 'TTS 시도='+L.ttsCalls.join(',')+' | 라이브 연결='+L.setups.map(s=>s.model).join(',')+' | 음성='+(url?'있음 '+(await window.__dur(url))+'초':'없음')"
         "+' | 그대로 읽기 지시='+/한 글자도/.test(L.setups[0]?.systemInstruction?.parts?.[0]?.text||'')+' | 보낸 글에 원문='+(L.sent[0]?.text||'').includes('출석 통지서는 회의 5일 전까지')+' | 음성만='+JSON.stringify(L.setups[0]?.generationConfig?.responseModalities)")
    step("B2 TTS 한도 기억: 다시 읽을 때 TTS는 건너뛰고 바로 라이브",
         "window.__lv.ttsCalls=[];window.__lv.setups=[];const url=await app._ttsGenerateGemini('두 번째 글입니다.');return 'TTS 시도='+window.__lv.ttsCalls.length+' | 라이브='+window.__lv.setups.map(s=>s.model).join(',')+' | 음성='+(url?'있음':'없음')")
    step("C 첫 라이브 모델이 없으면(1008) 다음 모델로 · 그 모델은 1시간 쉼",
         "app._ttsExhausted=new Map();app._ttsLiveList=null;window.__lv.ttsCalls=[];window.__lv.setups=[];window.__lv.fail=['gemini-2.5-flash-native-audio-preview-12-2025'];"
         "const url=await app._ttsGenerateGemini('세 번째 글입니다.');const w=(app._ttsExhausted.get('gemini-2.5-flash-native-audio-preview-12-2025')||0)-Date.now();"
         "return '라이브 연결='+window.__lv.setups.map(s=>s.model).join(' → ')+' | 음성='+(url?'있음':'없음')+' | 쉬는 시간='+Math.round(w/60000)+'분'")
    step("C2 TTS가 되면 라이브는 안 씀",
         "app._ttsExhausted=new Map();app._ttsCache=new Map();window.__lv.fail=[];window.__lv.ttsOk=true;window.__lv.ttsCalls=[];window.__lv.setups=[];"
         "const url=await app._ttsGenerateGemini('네 번째 글입니다.');window.__lv.ttsOk=false;return 'TTS 시도='+window.__lv.ttsCalls.join(',')+' | 라이브 연결='+window.__lv.setups.length+' | 음성='+(url?'있음 '+(await window.__dur(url))+'초':'없음')")
    step("D 준비: TTS 모두 429 · 라이브 정상 · 답변 줄의 🔊 찾기",
         "app._ttsExhausted=new Map();app._ttsCache=new Map();window.__lv.setups=[];window.__lv.toasts=[];app.addAIMessage('ai','징계 의결 요구서는 처분권자에게 보냅니다. 기한을 꼭 확인하세요.');await W(400);"
         "const b=[...document.querySelectorAll('#chatBox .ai-message .tts-btn')].pop();return '🔊 단추='+!!b+' 보임='+vis(b)")
    click("[...document.querySelectorAll('#chatBox .ai-message .tts-btn')].pop()")
    step("D2 🔊 실제 클릭 → 라이브 음성으로 재생 · 기본 음성 알림 없음",
         "let st=[];for(let i=0;i<40;i++){await W(100);st.push(app._ttsAudio?'재생':(app._ttsLoading?'준비':'-'))}"
         "const s=[...new Set(st)].join('→');return '상태='+s+' | 라이브 연결='+window.__lv.setups.length+' | 알림='+(window.__lv.toasts.join(' / ')||'없음')")
    step("E 라이브 모델도 모두 실패 → 기본 음성으로 넘어감(알림)",
         "app.ttsStop();await W(200);app._ttsExhausted=new Map();app._ttsCache=new Map();app._ttsLiveList=null;window.__lv.toasts=[];"
         "window.__lv.fail=['gemini-2.5-flash-native-audio-preview-12-2025','gemini-3.8-live-preview','gemini-2.5-flash-native-audio-preview-09-2025'];"
         "app.addAIMessage('ai','다른 답변입니다. 기본 음성으로 읽힐 글입니다.');await W(400);return 'ok'")
    click("[...document.querySelectorAll('#chatBox .ai-message .tts-btn')].pop()")
    step("E2 결과", "for(let i=0;i<40&&!window.__lv.toasts.length;i++)await W(100);app.ttsStop();return '알림='+(window.__lv.toasts.join(' / ')||'없음')")
step("정리", "app.ttsStop?.();app.exitFocusMode?.();await W(500);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7963);app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
