// 「서로 맞아야 하는 것」 검사기 — 페이지 안에서 실행하는 식 하나 (cdp3·monkey·run_all이 단계마다 부름)
// 돌려주는 값: { e: [오류...], w: [주의...] }  — 오류 = 데이터·화면이 서로 어긋남, 주의 = 정리하면 좋은 것
// 앱 함수 중 부수효과가 있는 것(저장·다시 그리기·타이머)은 부르지 않고 읽기만 한다
(async () => {
  const e = [], w = [];
  try {
    if (typeof app === 'undefined' || !app.allData) return { e: ['앱이 아직 준비되지 않음'], w };
    const A = app.allData, wfs = A.workflows || [];
    const live = wfs.filter(x => !x.isDeleted && !x.isDraft);
    const done = it => app.normalizeCompleted(it) === true;
    const sub = it => app._isSubEntry(it);
    // ── 1. 업무 하나하나 ──
    const ids = new Set();
    for (const wf of wfs) {
      const T = `「${(wf.title || '').slice(0, 20)}」`;
      if (ids.has(wf.id)) e.push(`${T} 업무 번호가 겹침 (${wf.id})`);
      ids.add(wf.id);
      const cl = wf.checklist || [];
      const itemIds = new Set();
      cl.forEach((it, i) => {
        if (typeof it.text !== 'string') e.push(`${T} ${i}번 줄 이름이 글이 아님`);
        if (it.itemId) { if (itemIds.has(it.itemId)) e.push(`${T} 항목 번호 겹침 ${it.itemId}`); itemIds.add(it.itemId); }
        if (sub(it) && i === 0) e.push(`${T} 첫 줄이 할 일(단계 없이 시작)`);
      });
      if (wf.isDeleted || wf.isDraft) continue;
      // 단계 ↔ 할 일: 건너뛰지 않은 할 일이 모두 끝났으면 단계도 끝, 단계가 할 일 덕에 끝났으면 할 일도 모두 끝
      cl.forEach((it, i) => {
        if (sub(it) || it.skipped === true) return;
        const subs = [];
        for (let k = i + 1; k < cl.length && sub(cl[k]); k++) subs.push(cl[k]);
        if (!subs.length) return;
        const open = subs.filter(s => s.skipped !== true && !done(s));
        if (!open.length && subs.some(s => s.skipped !== true) && !done(it)) e.push(`${T} 「${it.text}」 할 일이 다 끝났는데 단계가 안 끝남`);
        if (done(it) && open.length && !wf.isReference) e.push(`${T} 「${it.text}」 단계는 끝났는데 안 끝난 할 일 ${open.length}개 (${open.map(s => s.text).slice(0, 2).join(', ')})`);
      });
      // 건너뛰기 표시: 건너뛴 줄에 체크가 남아 있으면 안 됨
      cl.forEach(it => { if (it.skipped === true && done(it)) e.push(`${T} 건너뛴 「${it.text}」에 체크가 남음`); });
      // 업무 분담: 맡긴 단계가 실제로 있어야
      const c = wf.collab;
      if (c && c.steps) Object.keys(c.steps).forEach(sid => { if (!itemIds.has(sid)) w.push(`${T} 업무 분담에 없는 항목(${sid})이 남음`); });
      if (wf.completedProcessed && wf.isReference) e.push(`${T} 처리완료이면서 레퍼런스`);
    }
    // ── 2. 자료 연결: 업무가 가리키는 법령·서식이 실제로 있어야 ──
    if (app.dbReady && app.dbManager) {
      const libIds = new Set(await app.dbManager.getAllFileKeys('lawLibrary').catch(() => []));
      const repoIds = new Set(await app.dbManager.getAllFileKeys('repoDocuments').catch(() => []));
      for (const wf of live) {
        const T = `「${(wf.title || '').slice(0, 20)}」`;
        (app.checklistDetails[`project-${wf.id}`]?.linkedLibraryDocs || []).forEach(id => { if (!libIds.has(id)) e.push(`${T} 참고 자료가 법령·매뉴얼에 없음 (${id})`); });
        (wf.checklist || []).forEach(it => (it.linkedDocs || []).forEach(id => { if (!repoIds.has(id)) e.push(`${T} 「${it.text}」 서식이 서식·문서함에 없음 (${id})`); }));
      }
    }
    // 세부 정보가 지운(영구 삭제) 업무를 가리키면 정리 대상
    const orphan = Object.keys(app.checklistDetails || {}).filter(k => { const m = k.match(/^(?:project-)?(\d+)/); return m && !ids.has(Number(m[1])); });
    if (orphan.length) w.push(`없는 업무의 세부 정보 ${orphan.length}개 (예: ${orphan[0]})`);
    // ── 3. 화면 ──
    const visible = el => !!el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
    const modals = [...document.querySelectorAll('.modal.show, #cimOverlay, .sched-overlay, #branchPreviewOverlay, #branchPickerOverlay, #naPickerOverlay, .nap-overlay, .olh-overlay, #progressReportModal')].filter(visible)
      .concat([...document.querySelectorAll('[id^="aiGuideModal_"]')].filter(x => /^aiGuideModal_\d+$/.test(x.id) && visible(x)));
    if (document.body.style.position === 'fixed' && !modals.length) e.push('창이 없는데 화면이 잠김(스크롤 안 됨)');
    // 지운·작성 중 업무가 목록 카드에 나오면 안 됨
    wfs.filter(x => x.isDeleted || x.isDraft).forEach(x => { if (visible(document.getElementById('workflow-' + x.id))) e.push(`지운/작성 중 업무가 목록에 보임 「${x.title}」`); });
    // 일하는 화면
    if (app.focusMode) {
      const wf = wfs.find(x => x.id === app.focusedWorkflowId);
      if (!wf) e.push('일하는 화면인데 업무가 없음');
      else if (wf.isDeleted) e.push(`지운 업무가 일하는 화면에 열려 있음 「${wf.title}」`);
      else if (!app.focusEditMode && !wf.isReference && (wf.checklist || []).length) {  // 레퍼런스는 빈 모양으로 보여 줌
        const p = app.calculateProgress(wf) + '%';
        const fap = document.getElementById('focusActionPanel');
        const hasPct = el => !el || !visible(el) || el.textContent.includes(p);
        if (fap && visible(fap) && /%/.test(fap.textContent) && !hasPct(fap)) e.push(`왼쪽 진행률이 ${p}이 아님 (${(fap.textContent.match(/\d+%/) || [''])[0]})`);
        const prog = document.getElementById('procProg');
        // 단계가 넘어가는 체크는 패널을 가운데 목록이 접히는 때(약 1초 뒤)에 바꾸므로 체크 직후 2초는 비교하지 않음
        const settling = app._stageHold || (app._lastCheckAt && Date.now() - app._lastCheckAt < 2000);
        if (!settling && prog && visible(prog) && /%/.test(prog.textContent) && !hasPct(prog)) e.push(`오른쪽 업무 절차 진행률이 ${p}이 아님 (${(prog.textContent.match(/\d+%/) || [''])[0]})`);
        const head = [...document.querySelectorAll(`#focus-checklist-scroll-${wf.id} *`)].find(x => x.children.length < 4 && /^\s*체크리스트/.test(x.textContent) && /%/.test(x.textContent));
        if (head && !head.textContent.includes(p)) e.push(`가운데 체크리스트 진행률이 ${p}이 아님`);
      }
    }
    // 같은 창이 두 번 떠 있으면 안 됨
    const idc = {};
    document.querySelectorAll('.modal.show[id]').forEach(m => { idc[m.id] = (idc[m.id] || 0) + 1; });
    Object.entries(idc).forEach(([k, n]) => { if (n > 1) e.push(`창 「${k}」가 ${n}개`); });
    const menus = ['fbCtxMenu', 'wfmCtxMenu', 'checklistItemMenu'].map(id => document.getElementById(id)).filter(visible);
    if (menus.length > 1) e.push('오른쪽 클릭 메뉴가 두 개 이상 떠 있음');
  } catch (err) { e.push('검사기 오류: ' + err.message); }
  return { e, w };
})()
