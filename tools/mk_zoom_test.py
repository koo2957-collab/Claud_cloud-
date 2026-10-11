# 사진 미리보기 확대·축소: 누른 곳 중심 확대(왼쪽에 붙지 않음) · Ctrl+휠 · 끌어 옮기기 · [－ 100% ＋ 맞춤] · 다음 예시에서 맞춤으로 → steps3.json
# 실행: (tools 폴더에서) python mk_zoom_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===8991);const PC=()=>[...document.querySelectorAll('.pv-win #previewContent')].pop();const IM=()=>PC()&&PC().querySelector('img');const BAR=()=>[...document.querySelectorAll('.pv-zbar')].pop();"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def pt(body): S.append({"pt": True, "js": P + body + E})
# 상태: 배율 글자 · 사진 크기 · 사진 가운데가 창 가운데에서 벗어난 정도 · 스크롤
ST = "const st=()=>{const pc=PC(),im=IM(),r=im.getBoundingClientRect(),p=pc.getBoundingClientRect();return '배율='+BAR().querySelector('.pv-zpct').textContent+' 사진='+Math.round(r.width)+'x'+Math.round(r.height)+' 가운데 어긋남(가로,세로)='+Math.round((r.left+r.width/2)-(p.left+p.width/2))+','+Math.round((r.top+r.height/2)-(p.top+p.height/2))+' 스크롤='+pc.scrollLeft+','+pc.scrollTop;};"
# 누른 화면 자리의 사진 지점(비율)이 확대 뒤에도 같은 자리에 있는지
MARK = "window.__mk=(x,y)=>{const r=IM().getBoundingClientRect();return [(x-r.left)/r.width,(y-r.top)/r.height];};"

step("seed", "localStorage.setItem('startupPromptShown','1');localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const mk=async(w,h,c,t)=>{const cv=document.createElement('canvas');cv.width=w;cv.height=h;const g=cv.getContext('2d');g.fillStyle=c;g.fillRect(0,0,w,h);g.fillStyle='#fff';g.font='bold '+Math.round(h/10)+'px sans-serif';g.fillText(t,w*0.05,h*0.15);g.fillStyle='#ef4444';g.fillRect(w*0.75,h*0.6,w*0.05,h*0.08);return await new Promise(r=>cv.toBlob(r,'image/png'));};"
     "const cl=[['출석통지서 발송',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:8991,type:'manual',title:'사진 확대 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));app.saveData();"
     "await app.addTipFiles(8991,0,{files:[new File([await mk(3000,2000,'#2563eb','큰 화면 캡처')],'큰 캡처.png',{type:'image/png'}),new File([await mk(300,200,'#059669','작은 사진')],'작은 사진.png',{type:'image/png'}),new File(['%PDF-1.4 '+'0'.repeat(3000)],'작성례.pdf',{type:'application/pdf'})],value:''});await W(600);"
     "app.displayWorkflows();await W(300);app.focusWorkflow(8991);await W(1000);app.previewTipFile(8991,0,0);await W(1500);return 'ok'")
step("A 열면 창에 맞춤 + 아래 조절 막대", ST + "return st()+' | 막대='+[...BAR().querySelectorAll('button')].map(b=>b.textContent+(b.disabled?'(흐림)':'')).join(' ')")
S.append({"shot": "zm_a.png"})
# 사진의 빨간 네모(오른쪽 아래 쪽)를 누름
pt(MARK + "const r=IM().getBoundingClientRect();window.__cx=r.left+r.width*0.775;window.__cy=r.top+r.height*0.64;window.__before=window.__mk(window.__cx,window.__cy);return JSON.stringify([window.__cx,window.__cy])")
S.append({"clickpt": 1})
step("B 누른 곳 중심으로 100% 확대 — 왼쪽에 붙지 않음", ST + "await W(300);const a=window.__mk(window.__cx,window.__cy),b=window.__before;return st()+' | 누른 지점 그대로='+(Math.abs(a[0]-b[0])<0.01&&Math.abs(a[1]-b[1])<0.01)+' ('+a.map(v=>v.toFixed(3))+' / '+b.map(v=>v.toFixed(3))+')'")
S.append({"shot": "zm_b.png"})
pt("const p=PC().getBoundingClientRect();return JSON.stringify([p.left+p.width/2,p.top+p.height/2])")
S.append({"drag": [-200, -120]})
step("C 끌어서 옮기기", ST + "return st()")
pt(MARK + "const p=PC().getBoundingClientRect();window.__cx=p.left+p.width*0.3;window.__cy=p.top+p.height*0.4;window.__before=window.__mk(window.__cx,window.__cy);return JSON.stringify([window.__cx,window.__cy])")
S.append({"wheel": 120, "mods": 2})
S.append({"wheel": 120, "mods": 2})
step("D Ctrl+휠 아래로 두 번 → 마우스 자리 중심으로 축소", ST + "await W(300);const a=window.__mk(window.__cx,window.__cy),b=window.__before;return st()+' | 마우스 지점 그대로='+(Math.abs(a[0]-b[0])<0.01&&Math.abs(a[1]-b[1])<0.01)")
S.append({"wheel": -120, "mods": 2})
step("D2 Ctrl+휠 위로 → 확대", ST + "await W(300);return st()")
step("E 휠만(Ctrl 없이)은 스크롤", ST + "const pc=PC(),t0=pc.scrollTop;pc.dispatchEvent(new WheelEvent('wheel',{deltaY:120,bubbles:true,cancelable:true}));await W(200);return '배율 그대로='+BAR().querySelector('.pv-zpct').textContent")
pt("const p=PC().getBoundingClientRect();return JSON.stringify([p.left+p.width*0.4,p.top+p.height*0.4])")
S.append({"clickpt": 1})
step("F 확대된 사진을 다시 누르면 맞춤 · 가운데", ST + "await W(300);return st()+' | 맞춤 단추 흐림='+BAR().querySelector('[data-z=fit]').disabled")
step("G 막대 [＋] 두 번 → 가운데 기준 확대", ST + "BAR().querySelector('[data-z=in]').click();await W(150);BAR().querySelector('[data-z=in]').click();await W(300);return st()")
step("G2 [100%]", ST + "BAR().querySelector('[data-z=\"100\"]').click();await W(300);return st()")
step("G3 [맞춤]", ST + "BAR().querySelector('[data-z=fit]').click();await W(300);return st()")
S.append({"key": "+", "vk": 187})
step("H 키보드 ＋", ST + "await W(200);return st()")
S.append({"key": "0", "vk": 48})
step("H2 키보드 0 → 맞춤", ST + "await W(200);return st()")
S.append({"key": "ArrowRight", "vk": 39})
step("I 다음 예시(작은 사진)로 넘기면 맞춤 · 가운데", ST + "await W(1200);return st()")
S.append({"shot": "zm_i.png"})
pt("const r=IM().getBoundingClientRect();return JSON.stringify([r.left+r.width/2,r.top+r.height/2])")
S.append({"clickpt": 1})
step("J 작은 사진을 누르면 2배, 여전히 가운데", ST + "await W(300);return st()")
S.append({"key": "ArrowRight", "vk": 39})
step("K 다음 예시가 PDF면 확대 막대 숨김", "await W(1500);const b=BAR();return '사진 없음='+!IM()+' 막대 숨김='+(!b||b.hidden)")
S.append({"key": "ArrowRight", "vk": 39})
step("K2 다시 큰 사진으로 → 막대 다시 보이고 맞춤", "await W(1500);return '막대 보임='+!BAR().hidden+' 배율='+BAR().querySelector('.pv-zpct').textContent")
step("정리", "document.querySelectorAll('.pv-modal').forEach(m=>m.querySelector('.close-preview-modal')?.click());await W(300);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==8991);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
