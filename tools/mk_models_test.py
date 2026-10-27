# 제미나이 무료 모델 정리 시험 대본 → steps3.json
# 무료 비율 제한 표(2026-10)에 한도가 있는 모델만: 3.7·3.5 Flash·3.1 Pro 빠짐, Gemma 4 한도 30/16K/14,400
# 실행: (tools 폴더에서) python mk_models_test.py && node cdp3.mjs "<저장소>/ai_test .html"
import json, os
P = ("(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));const $=id=>document.getElementById(id);"
     "const vis=el=>!!el&&el.offsetParent!==null;const tx=el=>el?el.textContent.replace(/\\s+/g,' ').trim():'(없음)';")
E = "}catch(e){return 'ERR '+e.message+' '+(e.stack||'').split('\\n')[1]}})()"
S = []
def step(label, body): S.append({"label": label, "js": P + body + E})
def click(sel_js): S.append({"pt": True, "js": P + "document.querySelectorAll('.toast').forEach(t=>t.classList.remove('show'));const b=" + sel_js + ";b.scrollIntoView({block:'nearest'});const r=b.getBoundingClientRect();return JSON.stringify([r.x+r.width/2,r.y+r.height/2])" + E}); S.append({"clickpt": 1})
step("준비: 키 넣고 업무 파트너 열기",
     "document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));$('welcomeModal')?.remove();app.checkBackupReminder=()=>{};"
     "app.allData.provider='gemini';app.allData.geminiApiKey='TEST-KEY';app._syncAiOff?.();app.updateAIPanelAvailabilityUI?.();"
     "const ID=7962;app.allData.workflows=app.allData.workflows.filter(w=>w.id!==ID);const o={text:'할 일',indent:0,completed:false};app.ensureChecklistItemId(o);"
     "app.allData.workflows.unshift({id:ID,type:'manual',title:'모델 시험 업무',checklist:[o],date:'2026. 10. 27.',createdAt:new Date().toISOString(),folderPath:''});app.saveData();app.focusWorkflow(ID);await W(1300);"
     "if($('aiPanel').classList.contains('hidden'))app.toggleAiPanel();await W(400);app.setAiPanelView?.('chat');await W(400);return '패널 열림='+!$('aiPanel').classList.contains('hidden')")
click("$('aiModelPill')")
step("A 모델 고르기 목록(실제 클릭으로 엶)",
     "await W(300);const o=[...document.querySelectorAll('#aiModelDropdown .ai-model-opt')];return '열림='+vis(o[0])+' | '+o.map(x=>x.dataset.model||'자동').join(', ')+' | 칸막이='+document.querySelectorAll('#aiModelDropdown .ai-model-divider').length")
S.append({"shot": "models_dd.png"})
step("A2 Gemma 한도 문구", "return [...document.querySelectorAll('#aiModelDropdown .ai-model-opt')].filter(x=>(x.dataset.model||'').startsWith('gemma')).map(x=>tx(x)).join(' / ')")
click("document.querySelector('#aiModelDropdown .ai-model-opt[data-model=\"gemini-3.6-flash\"]')")
step("B 3.6 Flash 누름 → 직접 고름·단추 이름", "await W(300);return app.allData.modelMode+' '+app.allData.manualModel+' | 단추='+tx($('aiModelPillLabel'))")
step("C 자동 모드 체인·대체 순서",
     "app.setModelMode('auto');await W(200);const t=app._getAutoThinkingChain().map(m=>m.model).join('>');const l=app._getAutoLiteChain().map(m=>m.model).join('>');"
     "const f=app._buildFallbackChain('gemini-3.8-flash',{thinkingConfig:{thinkingBudget:1024}}).map(m=>m.model).join('>');"
     "const r=app.resolveAIConfig('제3조 시행령 해석을 검토해 주세요 부탁합니다');return 'Thinking='+t+' | Lite='+l+' | 대체='+f+' | 복잡한 질문 모델='+r.model+' 사고='+r.thinking")
step("D 한도표", "return ['gemini-3.8-flash','gemini-3.6-flash','gemini-3.5-flash-lite','gemma-4-31b-it','gemma-4-26b-a4b-it','gemini-3.7-flash','gemini-3.1-pro-preview'].map(m=>m+'='+JSON.stringify(app.getModelLimits(m))).join(' | ')")
step("F 예전 설정(3.7 Flash 직접 고름) 저장", "app.setModelMode('manual','gemini-3.7-flash');await app.saveDataImmediate();const a=JSON.parse(localStorage.getItem('appSettings_v5.2')||'{}');return '저장된 모델='+a.manualModel")
S.append({"reload": 2500})
step("F2 다시 켜면 3.8 Flash로 옮겨짐", "await W(500);return app.allData.modelMode+' '+app.allData.manualModel+' | 단추='+tx($('aiModelPillLabel'))")
step("정리", "app.setModelMode('auto');app.exitFocusMode?.();await W(500);app.allData.workflows=app.allData.workflows.filter(w=>w.id!==7962);app.allData.geminiApiKey='';await app.saveDataImmediate();return 'ok'")
json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steps3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('steps3.json', len(S))
