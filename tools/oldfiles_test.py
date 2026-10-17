# 예전 판 파일 시험: git 기록의 예전 프로그램(v1.4.0 · v1.5.6)으로 업무 파일·전체 백업을 실제로 만들고 → 지금 판이 읽는지
import io, sys as _s
_s.stdout = io.TextIOWrapper(_s.stdout.buffer, encoding="utf-8", errors="replace")
# 확인: 업무 수 · 할 일 줄 · 체크 · 처리결과 · 업무팁 · 처리결과 첨부 이름 · (v1.5.6) 연습 업무 건너뛰기·서식 연결 · 검사기
# 실행: (tools 폴더에서) python oldfiles_test.py   → 끝에 「OLDFILES 결과 …」 (예전 프로그램은 tools/_old/ — 저장소에 올리지 않음)
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.dirname(here)
OLD = [('a202b26', '1.4.0'), ('623e25f', '1.5.6')]
os.makedirs(os.path.join(here, '_old'), exist_ok=True)
NODE = 'node'
def run_cdp3(app_path, steps, label):
    sp = os.path.join(here, f'_old/steps_{label}.json')
    json.dump(steps, open(sp, 'w', encoding='utf-8'), ensure_ascii=False)
    env = dict(os.environ, STEPS=f'_old/steps_{label}.json', CDP_PORT='9399', CDP_PROF='chrome-old')
    if label.startswith('new'): env['SELFCHECK'] = '1'
    r = subprocess.run([NODE, os.path.join(here, 'cdp3.mjs'), app_path], cwd=here, env=env, capture_output=True, text=True, encoding='utf-8', timeout=900)
    return r.stdout + r.stderr
P = "(async()=>{try{const W=ms=>new Promise(r=>setTimeout(r,ms));"
E = "}catch(e){return 'ERR '+e.message}})()"
CAPTURE = "window.__blobs=[];const oc=URL.createObjectURL.bind(URL);URL.createObjectURL=b=>{window.__blobs.push(b);return oc(b)};HTMLAnchorElement.prototype.click=function(){};window.confirm=()=>true;window.alert=()=>{};if(app._saveFileWithPicker)app._saveFileWithPicker=async b=>{window.__blobs.push(b);return true};"
lines = []
for commit, ver in OLD:
    old_html = os.path.join(here, f'_old/v{ver}.html')
    src = subprocess.run(['git', 'show', f'{commit}:index.html'], cwd=repo, capture_output=True).stdout
    open(old_html, 'wb').write(src)
    practice = ver >= '1.5'
    make = (P + "localStorage.setItem('welcomeShown','1');document.querySelectorAll('.modal.show').forEach(m=>m.classList.remove('show'));" + CAPTURE +
        ("await app.insertPracticeWorkflows();await W(2500);const w=app.allData.workflows.find(x=>/소모품/.test(x.title));app.focusWorkflow(w.id);await W(1200);for(const i of [1,2,3]){app.toggleChecklistItem(w.id,i);await W(1300);}" if practice else
         "const w={id:Date.now(),type:'manual',title:'예전 판 업무 v" + ver + "',date:'2026. 1. 2.',checklist:[{text:'1단계 접수',indent:0,completed:false},{text:'서류 받기',indent:1,completed:true,result:{text:'1월 2일 받음',summary:''}},{text:'검토',indent:1,completed:false,tip:{type:'text',content:'⚠ 기한 3일\\n근거: 규정 제1조',saved:true}},{text:'2단계 보고',indent:0,completed:false}],deadline:'2026-12-31'};app.allData.workflows.unshift(w);app.ensureChecklistItemId&&w.checklist.forEach(i=>app.ensureChecklistItemId(i));app.saveData();await W(800);") +
        "const w2=app.allData.workflows.find(x=>!x.isDeleted);const i=w2.checklist.findIndex(x=>x.indent);w2.checklist[i].result={text:'예전 판 처리결과',summary:''};app.saveData();"
        "if(app.addResultFiles){try{await app.addResultFiles(w2.id,i,{files:[new File(['%PDF-1.4 old'],'예전 첨부.pdf',{type:'application/pdf'})],value:''});await W(800);app.closeChecklistItemModal&&app.closeChecklistItemModal();}catch(e){}}"
        "window.__blobs=[];await app.exportMultipleWorkflowPackages(app.allData.workflows.filter(x=>!x.isDeleted).map(x=>x.id));await W(1500);const ex=window.__blobs.at(-1);const exTxt=ex?await ex.text():'';"
        "let bk='';try{const o=await app._buildFullBackupObject();bk=JSON.stringify(o);}catch(e){}app._hideProgress&&app._hideProgress();"
        "return JSON.stringify({ver:'" + ver + "',export:exTxt?JSON.parse(exTxt):null,backup:bk?JSON.parse(bk):null,summary:app.allData.workflows.filter(x=>!x.isDeleted).map(x=>({t:x.title,n:x.checklist.length,c:x.checklist.filter(it=>it.completed).length,r:x.checklist.filter(it=>it.result&&it.result.text).length,tip:x.checklist.filter(it=>it.tip&&it.tip.content).length}))})" + E)
    out = run_cdp3(old_html, [{"label": "예전 판에서 만들기", "js": make, "save": f"_old/v{ver}_made.json"}], 'old' + ver)
    made_path = os.path.join(here, f'_old/v{ver}_made.json')
    try:
        made = json.load(open(made_path, encoding='utf-8'))
    except Exception:
        lines.append(f'v{ver}: 예전 판에서 파일을 만들지 못함 ✗ {out[-300:]}'); continue
    exp, bk, summ = made.get('export'), made.get('backup'), made.get('summary')
    lines.append(f"v{ver}: 예전 판에서 만듦 — 업무 {len(summ)}개 · 업무 파일 {'있음' if exp else '없음 ✗'} · 전체 백업 {'있음' if bk else '없음'}")
    json.dump(exp, open(os.path.join(here, f'_old/v{ver}_export.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    if bk: json.dump(bk, open(os.path.join(here, f'_old/v{ver}_backup.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    CMP = ("const want=" + json.dumps(summ, ensure_ascii=False) + ";const got=app.allData.workflows.filter(x=>!x.isDeleted);const bad=[];"
           "want.forEach(s=>{const g=got.find(x=>x.title.replace(/ \\(가져옴\\)$/,'')===s.t);if(!g){bad.push('없음: '+s.t);return;}const c=g.checklist;if(c.length!==s.n)bad.push(s.t.slice(0,10)+' 줄 '+s.n+'→'+c.length);if(c.filter(i=>app.normalizeCompleted(i)).length<s.c)bad.push(s.t.slice(0,10)+' 체크 '+s.c+'→'+c.filter(i=>app.normalizeCompleted(i)).length);if(c.filter(i=>i.result&&i.result.text).length!==s.r)bad.push(s.t.slice(0,10)+' 처리결과 '+s.r+'→'+c.filter(i=>i.result&&i.result.text).length);if(c.filter(i=>i.tip&&i.tip.content).length!==s.tip)bad.push(s.t.slice(0,10)+' 업무팁 '+s.tip+'→'+c.filter(i=>i.tip&&i.tip.content).length);});"
           "const att=Object.entries(app.checklistDetails).filter(([k])=>/-r-/.test(k)).flatMap(([k,v])=>(v.attachments||[]).map(a=>a.name));if(!att.includes('예전 첨부.pdf'))bad.push('처리결과 첨부 없음');")
    steps = [
        {"label": f"v{ver} 업무 파일 → 그대로 가져오기", "js": P + "localStorage.setItem('welcomeShown','1');document.getElementById('welcomeModal')?.remove();window.confirm=()=>true;app.checkBackupReminder=()=>{};"
            "const txt=" + json.dumps(json.dumps(exp, ensure_ascii=False), ensure_ascii=False) + ";app._restoreFromFile([new File([txt],'old.json')]);await W(1200);const m=document.getElementById('packageImportChoiceModal');if(m){m.querySelector('input[value=asIs]').click();app._confirmPackageImport();}await W(4000);" + CMP + "return bad.length?'✗ '+bad.join(' | '):'업무·줄·체크·처리결과·업무팁·첨부 그대로 ✓'" + E},
    ]
    if bk:
        steps.append({"label": f"v{ver} 전체 백업 → 복원", "js": P + "window.confirm=()=>true;app._downloadJsonFile=()=>{};const txt=" + json.dumps(json.dumps(bk, ensure_ascii=False), ensure_ascii=False) + ";app._restoreFromFile([new File([txt],'bk.json')]);await W(7000);" + CMP + "return bad.length?'✗ '+bad.join(' | '):'백업 복원 그대로 ✓ (업무 '+got.length+')'" + E})
    out = run_cdp3(os.path.join(repo, 'index.html'), steps, 'new' + ver)
    for l in out.splitlines():
        if l.startswith('>') or l.startswith('SELFCHECK') or 'EXC' in l: lines.append('   ' + l[:300])
print('\n'.join(lines))
bad = sum(1 for l in lines if '✗' in l or 'SELFCHECK' in l or 'EXC' in l)
print(f'OLDFILES 결과 문제={bad}')
