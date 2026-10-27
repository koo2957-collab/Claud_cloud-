# 업무팁 세 칸(놓치기 쉬운 것·순서·근거) · 「지난번엔 이렇게」 시험 대본 → steps3.json
# 실행: (tools 폴더에서) python mk_tip3_test.py && node cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7601);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
S = []
def step(label, body): S.append({"label": label, "js": J(body)})
def pt(expr): S.append({"pt": True, "js": J("const el=" + expr + ";const b=el.getBoundingClientRect();return JSON.stringify([b.left+Math.min(30,b.width/2),b.top+b.height/2])")})
NL = "'+String.fromCharCode(10)+'"
step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const mkcl=()=>[['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "const now=new Date().toISOString();"
     "const past=(id,title,extra,txt,day)=>{const w={id,type:'manual',title,checklist:mkcl(),date:'2026. 9. 1.',createdAt:now,folderPath:'',...extra};w.checklist[2].result={text:txt,summary:''};w.checklist[2].completed=true;w.checklist[2].completedAt='2026-'+day+'T10:00:00';return w;};"
     "app.allData.workflows.unshift(past(7602,'지난 징계 (소방위 A)',{},'9.12.(금) 등기 발송, 9.15.(월) 수령 확인 — 회의 4일 전 도달','09-15'),past(7605,'더 지난 징계 (소방장 B)',{},'8.1. 직접 교부, 확인서 받음','08-01'),past(7606,'가장 오래된 징계',{},'7.1. 등기 발송','07-01'),past(7603,'본보기(레퍼런스)',{isReference:true},'레퍼런스 결과','09-20'),past(7604,'지운 업무',{isDeleted:true,deletedAt:now},'지운 결과','09-25'));"
     "app.allData.workflows.unshift({id:7601,type:'manual',title:'업무팁 세 칸 시험',checklist:mkcl(),date:'2026. 10. 11.',createdAt:now,folderPath:''});app.allData.workflows.forEach(w=>(w.checklist||[]).forEach(it=>app.ensureChecklistItemId(it)));"
     "wf().checklist[2].tip={type:'text',content:'⚠ 회의 3일 전까지 「도달」해야 함 (발송일 아님)" + NL + "1. 등기우편으로 발송" + NL + "2. 문자로도 함께 안내" + NL + "근거: 공무원 징계령 제10조',saved:true};"
     "wf().checklist[1].tip={type:'text',content:'1. 위원 5명 이상 구성" + NL + "2. 회의 날짜 확정',saved:true};"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7601);await W(900);app.toggleChecklistItem(7601,1);await W(1500);return 'ok'")
step("A 패널: 세 칸 + 지난번엔 이렇게", "const d=document.querySelector('#aiPanelOfflineDashboard .proc-step-detail');if(!d)return '상자 없음';"
     "const w=d.querySelector('.tip-warn'),b=d.querySelector('.tip-basis'),p=[...d.querySelectorAll('.proc-past-item')];"
     "return '놓치기쉬운것='+(w?w.querySelector('.tip-warn-li').textContent:'없음')+' | 순서첫줄='+(d.querySelector('.tip-sec-body')?.textContent.trim().slice(0,12))+' | 근거='+(b?b.querySelector('.tip-basis-li').textContent:'없음')+' | 지난번='+p.length+'개: '+p.map(x=>x.querySelector('.proc-past-src').textContent).join(' / ')+' | 레퍼런스·지운것 섞임='+/레퍼런스|지운/.test(d.textContent)")
S.append({"shot": "tip3_a.png"})
pt("document.querySelector('#aiPanelOfflineDashboard .proc-past-item')")
S.append({"clickpt": 1})
step("B 지난 기록을 누르면 그 업무의 항목 창(처리결과)", "await W(900);const o=document.getElementById('cimOverlay');const r='창='+!!o+' 내용에 그때 결과='+(!!o&&(o.innerHTML.includes('9.12.(금) 등기 발송')))+' 지금 업무 그대로='+(app.focusedWorkflowId===7601);app.closeChecklistItemModal();await W(500);return r")
step("C 항목 창 업무팁 보기도 세 칸", "await app.showChecklistItemModal(7601,2,'tip');await W(800);const o=document.getElementById('cimOverlay');return '빨간상자='+!!o.querySelector('.tip-warn')+' 근거='+!!o.querySelector('.tip-basis')")
step("D 고치기 모드: 세 칸(놓치기 쉬운 것 · 업무 팁 · 근거)으로 나뉨 · 기호 줄에 ⚠·근거 단추 없음", "app.switchTipToEditMode(7601,2);await W(500);const g=k=>document.getElementById('tip3-'+k+'-7601-2');const ta=g('body');ta.focus();await W(300);const bar=ta.previousElementSibling;return '기호줄='+!!(bar&&bar.classList.contains('ol-bar'))+' ⚠·근거 단추='+bar.querySelectorAll('.ol-tag').length+' | 놓치기 쉬운 것='+JSON.stringify(g('warn').value)+' | 근거='+JSON.stringify(g('basis').value)")
S.append({"shot": "tip3_d.png"})
step("E 표시 없는 예전 팁은 그대로", "app.closeChecklistItemModal();await W(500);await app.showChecklistItemModal(7601,1,'tip');await W(700);const o=document.getElementById('cimOverlay');const r='세칸틀='+!!o.querySelector('.tip-sec')+' 번호줄='+o.querySelectorAll('.tol-li').length;app.closeChecklistItemModal();await W(400);return r")
step("F 업무 길잡이에도 세 칸", "await app.showChecklistHelp(7601,2);await W(1200);const m=[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>/_content$/.test(x.id)).pop();const r='빨간상자='+!!(m&&m.querySelector('.tip-warn'))+' 근거='+!!(m&&m.querySelector('.tip-basis'));[...document.querySelectorAll('[id^=aiGuideModal_]')].filter(x=>!/_(content|closeBtn|footerCloseBtn)$/.test(x.id)).forEach(x=>x.remove());document.body.style.overflow='';document.body.style.position='';return r")
S.append({"shot": "tip3_f.png"})
step("G 다크 모드", "[...document.querySelectorAll('[id^=aiGuideModal_]')].forEach(x=>x.remove());document.documentElement.classList.add('dark-mode');app.refreshAIPanelDashboardIfNeeded();await W(800);return 'ok'")
S.append({"shot": "tip3_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>![7601,7602,7603,7604,7605,7606].includes(w.id));app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
