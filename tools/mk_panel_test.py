# 우측 업무 절차 패널 아이콘 통일 시험 대본 → steps3.json
# 실행: python tools/mk_panel_test.py && node tools/cdp3.mjs <index.html 경로>
import json, os
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const wf=()=>app.allData.workflows.find(w=>w.id===7401);"
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
def J(b): return P + b + E
EMO = "const emo=el=>(el.textContent.match(/[\\u{1F300}-\\u{1FAFF}\\u2600-\\u27BF\\u23F3]/gu)||[]).join('');"
S = []
def step(label, body): S.append({"label": label, "js": J(EMO + body)})
step("seed", "window.confirm=()=>true;['tipNwTab','tipSkipTargetSeen','startupPromptShown'].forEach(k=>localStorage.setItem(k,'1'));localStorage.setItem('deadlineNotifyMode','off');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));"
     "const cl=[['징계위원회 개최 준비',0],['위원 구성·회의 일정 확정',1],['출석통지서 발송',1],['심의·의결',0],['징계 의결서 수령',1]].map(([t,i])=>({text:t,indent:i,completed:false}));"
     "app.allData.workflows.unshift({id:7401,type:'manual',title:'패널 아이콘 시험',checklist:cl,date:'2026. 10. 11.',createdAt:new Date().toISOString(),folderPath:''});wf().checklist.forEach(it=>app.ensureChecklistItemId(it));"
     "wf().checklist[2].tip={type:'text',content:'출석통지서는 회의 3일 전까지 도달',saved:true};wf().checklist[2].formats=[{name:'출석통지서 서식.hwp'}];"
     "app.saveData();app.displayWorkflows();await W(400);app.focusWorkflow(7401);await W(900);app.toggleChecklistItem(7401,1);await W(1500);return 'ok'")
step("A 패널 머리 아이콘", "const t1=document.getElementById('aiPanelTabProcedure'),t2=document.getElementById('aiPanelTabChat'),x=document.querySelector('.ai-panel-header-close');"
     "return '절차탭 그림='+!!t1.querySelector('svg')+' 색='+getComputedStyle(t1).color+' active='+t1.classList.contains('active')+' | 대화탭 그림='+!!t2.querySelector('svg')+' | 닫기 그림='+!!x.querySelector('svg')+' | 머리 이모지=\"'+emo(document.querySelector('.ai-panel-header'))+'\"'")
step("B 업무팁·서식 상자", "const d=document.querySelector('.proc-step-detail');if(!d)return '상자 없음';"
     "return '묶음제목='+[...d.querySelectorAll('.proc-sec-label')].map(x=>(x.querySelector('svg')?'[그림]':'')+x.textContent.trim()+'('+getComputedStyle(x.querySelector('svg')).color+')').join(' / ')+' | 서식줄 그림='+d.querySelectorAll('.proc-fmt-ico svg').length+' | 상자 이모지=\"'+emo(d)+'\"'")
S.append({"shot": "panel_a.png"})
step("C 다 끝내면 「완료」", "for(const i of [2,4,3,0]){if(!app.normalizeCompleted(wf().checklist[i]))app.toggleChecklistItem(7401,i);await W(900);}await W(800);"
     "const p=document.getElementById('aiPanelOfflineDashboard');const sp=[...p.querySelectorAll('span')].find(x=>x.textContent.trim()==='완료');return '완료표시='+!!sp+' 그림='+!!(sp&&sp.querySelector('svg'))+' | 패널 이모지=\"'+emo(p)+'\"'")
S.append({"shot": "panel_c.png"})
step("D 다크 모드", "app.toggleChecklistItem(7401,4);await W(900);document.documentElement.classList.add('dark-mode');await W(500);const t1=document.getElementById('aiPanelTabProcedure');return '절차탭 색='+getComputedStyle(t1).color")
S.append({"shot": "panel_dark.png"})
step("정리", "document.documentElement.classList.remove('dark-mode');app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7401);app.saveData();return 'ok'")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json')
json.dump(S, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
