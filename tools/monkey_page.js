// 무작위 사용자(몽키) — 페이지 안에서 실행. monkey.mjs가 넣고 __monkey.step()을 수천 번 부름
// 같은 씨앗(seed)이면 같은 순서 → 실패한 순서를 그대로 다시 만들어 고칠 수 있음
// 되돌릴 수 있는 동작은 절반쯤 바로 되돌리고 「하기 전과 똑같은지」(__canon 비교)도 확인
(function () {
  const W = ms => new Promise(r => setTimeout(r, ms));
  let seed = 1;
  const rnd = () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const R = n => Math.floor(rnd() * n);
  const pick = a => a.length ? a[R(a.length)] : null;
  const live = () => app.allData.workflows.filter(w => !w.isDeleted && !w.isDraft);
  const cur = () => app.focusMode ? app.allData.workflows.find(w => w.id === app.focusedWorkflowId) : null;
  const vis = el => !!el && el.getClientRects().length > 0;
  const esc = () => (document.activeElement || document.body).dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true, cancelable: true }));
  const ctrlZ = () => (document.activeElement || document.body).dispatchEvent(new KeyboardEvent('keydown', { key: 'z', code: 'KeyZ', ctrlKey: true, bubbles: true, cancelable: true }));
  const choice = () => [...document.querySelectorAll('.modal.show')].reverse().find(m => m.querySelector('button[data-choice]'));
  const undoBtn = () => document.querySelector('#toastMessage .toast-undo-btn, #toastMessage button');
  const D = n => { const d = new Date(Date.now() + n * 864e5); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
  const sub = it => app._isSubEntry(it);
  const AI = () => !!window.__monkeyAI;
  let practiceN = 0;
  // 앞에 떠 있는 것 정리(사람이 흔히 하는 것: 묻는 창 아무 단추·Esc)
  async function settle() {
    for (let k = 0; k < 4; k++) {
      const c = choice();
      if (c) { const bs = [...c.querySelectorAll('button[data-choice]')]; pick(bs)?.click(); await W(250); continue; }
      const ov = document.getElementById('branchPreviewOverlay'); if (ov) { (rnd() < 0.5 ? document.getElementById('branchPreviewConfirmBtn') : document.getElementById('branchPreviewCancelBtn'))?.click(); await W(400); continue; }
      const rr = document.getElementById('refRegisterModal'); if (rr) { rr.querySelector(rnd() < 0.5 ? '[data-act=ok]' : '[data-act=cancel]')?.click(); await W(600); continue; }
      const pk = document.getElementById('packageImportChoiceModal'); if (pk && pk.classList.contains('show')) { if (rnd() < 0.7) app._confirmPackageImport(); else app._closePackageImportChoice(); await W(1500); continue; }
      break;
    }
  }
  // ── 동작들: [이름, 무게, 함수(되돌릴 수 있으면 true 돌려줌)] ──
  const A = [
    ['업무 열기', 10, async () => { const w = pick(live()); if (!w) return 'x'; app.focusWorkflow(w.id); await W(900); return w.title.slice(0, 12); }],
    ['체크(클릭)', 18, async () => { const w = cur(); if (!w || app.focusEditMode) return 'x'; const cs = [...document.querySelectorAll(`#focus-checklist-scroll-${w.id} .checklist-card`)].filter(vis); const c = pick(cs); const cb = c && c.querySelector('input.checkbox,.cl-check,.checkbox'); if (!cb || !vis(cb)) return 'x'; cb.click(); await W(1300); return w.checklist[+c.dataset.index]?.text?.slice(0, 14); }],
    ['해당 없음', 5, async () => { const w = cur(); if (!w || app.focusEditMode || w.isReference || w.completedProcessed) return 'x'; const ix = w.checklist.map((it, i) => i).filter(i => sub(w.checklist[i]) && !w.checklist[i].skipped && !app.normalizeCompleted(w.checklist[i])); const i = pick(ix); if (i == null) return 'x'; app.markNotApplicable(w.id, [i], '시험'); await W(1200); return { undo: true, t: w.checklist[i].text.slice(0, 14) }; }],
    ['해당 없음 되살리기', 3, async () => { const w = cur(); if (!w || app.focusEditMode) return 'x'; const i = w.checklist.findIndex(it => it.skipped && it.skipManual); if (i < 0) return 'x'; app.restoreNotApplicable(w.id, i); await W(1000); return w.checklist[i].text.slice(0, 14); }],
    ['건너뛰기 버튼', 6, async () => { const w = cur(); if (!w || app.focusEditMode || w.isReference || w.completedProcessed) return 'x'; const ix = w.checklist.map((it, i) => i).filter(i => (w.checklist[i].branchOptions || []).some(o => app.isBranchOptionConfigured(o)) && !w.checklist[i].branchActionTaken && !w.checklist[i].skipped); const i = pick(ix); if (i == null) return 'x'; const os = w.checklist[i].branchOptions.map((o, k) => k).filter(k => app.isBranchOptionConfigured(w.checklist[i].branchOptions[k])); app.handleBranchOption(w.id, i, pick(os)); await W(500); if (rnd() < 0.15) { esc(); await W(300); return '미리 보기 Esc'; } document.getElementById('branchPreviewConfirmBtn')?.click(); await W(1300); return { undo: true, t: w.checklist[i].text.slice(0, 14) }; }],
    ['건너뛰기 취소', 3, async () => { const w = cur(); if (!w || app.focusEditMode) return 'x'; const i = w.checklist.findIndex(it => it.branchActionTaken); if (i < 0) return 'x'; app._cancelBranchFromItem(w.id, i); await W(1000); return w.checklist[i].text.slice(0, 14); }],
    ['되돌리기 단추', 4, async () => { const b = undoBtn(); if (!b || !vis(b)) return 'x'; b.click(); await W(1000); return 'ok'; }],
    ['Ctrl+Z', 3, async () => { ctrlZ(); await W(800); return 'ok'; }],
    ['Esc', 8, async () => { esc(); await W(400); return 'ok'; }],
    ['항목 창·처리결과', 6, async () => { const w = cur(); if (!w || app.focusEditMode) return 'x'; const i = R(w.checklist.length); app.showChecklistItemModal(w.id, i, pick(['result', 'tip', 'formats'])); await W(700); const ta = document.getElementById(`main-checklist-result-text-${w.id}-${i}`); if (ta && !ta.disabled && rnd() < 0.7) { ta.value = (ta.value ? ta.value + ' / ' : '') + '처리 ' + R(100); ta.dispatchEvent(new Event('input', { bubbles: true })); } if (rnd() < 0.5) esc(); else app.closeChecklistItemModal(); await W(500); return w.checklist[i]?.text?.slice(0, 14); }],
    ['길잡이', 4, async () => { const w = cur(); if (!w || app.focusEditMode) return 'x'; const i = R(w.checklist.length); await app.showChecklistHelp(w.id, i); await W(900); if (rnd() < 0.3) { const n = [...document.querySelectorAll('[id^="aiGuideModal_"] button')].find(b => /다음 할 일/.test(b.textContent)); n?.click(); await W(900); } esc(); await W(400); return 'ok'; }],
    ['마감일', 3, async () => { const w = cur(); if (!w || app.focusEditMode || w.isReference) return 'x'; const i = R(w.checklist.length); app.saveChecklistItemDeadlineDirect(w.id, i, rnd() < 0.3 ? null : D(R(40) - 5)); await W(500); return 'ok'; }],
    ['줄 고르기(미리 보기)', 3, async () => { const w = cur(); if (!w || app.focusEditMode) return 'x'; app.toggleChecklistPeek(w.id, R(w.checklist.length)); await W(500); return 'ok'; }],
    ['체크리스트 편집', 7, async () => {
      const w = cur(); if (!w || w.completedProcessed) return 'x';
      if (!app.focusEditMode) { app.enterFocusEditMode(); await W(700); }
      for (let k = 0; k < 1 + R(3); k++) {
        const rows = [...document.querySelectorAll(`[id^="fci-"] .fci-title-text`)].filter(vis); const r = pick(rows); if (!r) break;
        r.click(); await W(200);
        const cmd = pick(['del', 'up', 'down', 'indent', 'outdent', 'del', 'addSub']);
        app._fciCmd(cmd); await W(400);
        const inp = document.activeElement; if (inp && inp.classList.contains('fci-title-input')) { inp.value = '새 줄 ' + R(99); inp.blur(); await W(300); }
      }
      const end = R(3); if (end === 0) app.exitFocusEditMode(); else if (end === 1) { app.cancelFocusEditMode(); await W(400); await settle(); } else esc();
      await W(800); return 'ok';
    }],
    ['진행상황 출력', 3, async () => { const w = cur(); if (!w) return 'x'; app.openProgressReport(w.id); await W(1200); const a = document.getElementById('authorInfoModal'); if (a) { document.getElementById('authorSave')?.click(); await W(1000); } const t = pick([...document.querySelectorAll('.pr-tabs [data-tab]')]); t?.click(); await W(600); if (rnd() < 0.5) esc(); else app.closeProgressReport?.(); await W(500); return 'ok'; }],
    ['일정', 2, async () => { app.openSchedule(cur() ? cur().id : null); await W(800); esc(); await W(400); return 'ok'; }],
    ['업무 관리 삭제', 3, async () => { app.openWorkflowManager(); await W(800); const w = pick(live().filter(x => !x.isReference)); if (w) { app._wfmDeleteItems([w.id], []); await W(700); } if (rnd() < 0.5) { const b = undoBtn(); b?.click(); await W(700); } app.closeModal('workflowManagerModal'); await W(400); return w ? { undo: false, t: w.title.slice(0, 12) } : 'x'; }],
    ['완료 처리', 3, async () => { const w = pick(live().filter(x => !x.isReference && !x.completedProcessed && x.checklist.length && x.checklist.every(it => app.normalizeCompleted(it) || it.skipped))); if (!w) return 'x'; app.markWorkflowDone(w.id); await W(900); return { undo: true, t: w.title.slice(0, 12) }; }],
    ['모두 끝내기', 2, async () => { const w = cur(); if (!w || app.focusEditMode || w.isReference || w.completedProcessed || w.checklist.length > 12) return 'x'; for (let k = 0; k < 2; k++) for (let i = 0; i < w.checklist.length; i++) { const it = w.checklist[i]; if (!it.skipped && !app.normalizeCompleted(it) && (k || sub(it))) { app.toggleChecklistItem(w.id, i); await W(1200); await settle(); } } return 'ok'; }],
    ['완료 취소', 2, async () => { const w = pick(live().filter(x => x.completedProcessed)); if (!w) return 'x'; app.undoMarkWorkflowDone(w.id); await W(800); return 'ok'; }],
    ['레퍼런스 등록', 2, async () => { const w = pick(live().filter(x => x.completedProcessed && !x.isReference)); if (!w) return 'x'; app.registerAsReference(w.id); await W(600); await settle(); await W(800); return 'ok'; }],
    ['복사하여 시작', 2, async () => { const w = pick(live().filter(x => x.isReference)); if (!w) return 'x'; app.duplicateWorkflow(w.id); await W(700); const m = [...document.querySelectorAll('.modal.show')].pop(); const b = m && [...m.querySelectorAll('button')].find(b => /시작하기/.test(b.textContent)); if (b && rnd() < 0.7) b.click(); else esc(); await W(1200); return 'ok'; }],
    ['업무 삭제', 2, async () => { const w = pick(live().filter(x => !x.isReference)); if (!w) return 'x'; await app.deleteWorkflow(w.id); await W(700); return { undo: true, t: w.title.slice(0, 12) }; }],
    ['휴지통 복구', 2, async () => { const w = pick(app.allData.workflows.filter(x => x.isDeleted)); if (!w) return 'x'; app.trashRestoreOne(w.id); await W(700); return 'ok'; }],
    ['내보내기→가져오기', 2, async () => { const w = pick(live()); if (!w) return 'x'; let blob = null; const o = app._saveFileWithPicker; app._saveFileWithPicker = async (b) => { blob = b; return true; }; await app.exportMultipleWorkflowPackages([w.id]); app._saveFileWithPicker = o; await W(500); if (!blob) return 'x'; app._restoreFromFile([new File([await blob.text()], 'x.json')]); await W(900); await settle(); await W(1500); return w.title.slice(0, 12); }],
    ['업무 분담 지정', 3, async () => { const w = cur(); if (!w || app.focusEditMode || w.isReference || w.completedProcessed || (w.collab && w.collab.role === 'assignee')) return 'x'; app._collabSavePeople([{ name: '김민수', dept: '시험과', rank: '소방장' }]); app._collabAddTeam(w, '김민수'); app.openCollabModal(w.id, 'send'); await W(900); const sel = pick([...document.querySelectorAll('#collabModal select')].filter(s => /assignee/.test(s.getAttribute('onchange') || ''))); if (sel) { sel.value = rnd() < 0.8 ? '김민수' : ''; sel.dispatchEvent(new Event('change', { bubbles: true })); await W(500); } if (rnd() < 0.5) esc(); else app.closeCollabModal(); await W(500); await settle(); await W(300); if (document.getElementById('collabModal')) app.closeCollabModal(true); await W(300); return 'ok'; }],
    ['홈', 3, async () => { app.goHome(); await W(700); await settle(); return 'ok'; }],
    ['연습 업무 넣기', 1, async () => { if (practiceN >= 2) return 'x'; practiceN++; await app.insertPracticeWorkflows(); await W(2500); return 'ok'; }],
    ['새 업무 만들기', 3, async () => {
      if (app.focusEditMode) return 'x';
      app.openModal('manualModal'); await W(600); await settle(); await W(300);
      if (!document.getElementById('manualModal').classList.contains('show')) return 'x';
      document.getElementById('manualProjectName').value = '몽키 업무 ' + R(999); app._nwGo(2); await W(400);
      const first = document.querySelector('#checklistItems .checklist-edit-item input'); if (first && !first.value) first.value = '1단계';
      for (let k = 0; k < 1 + R(4); k++) app.addChecklistItem('할 일 ' + k, R(2));
      await W(200); const end = R(4);
      if (end === 0) await app._nwFinish(); else if (end === 1) { document.querySelector('#manualModal .nw-reset')?.click(); await W(400); if (rnd() < 0.5) { undoBtn()?.click(); await W(600); } app.closeModal('manualModal'); await W(400); await settle(); }
      else { app.closeModal('manualModal'); await W(400); await settle(); }
      await W(800); return 'end' + end;
    }],
    ['넓게·글자 크기', 2, async () => { if (rnd() < 0.5) app.toggleProcWide(); else app.setReadScale(pick(['90', '100', '115', '130'])); await W(500); return 'ok'; }],
    ['법령 새 판으로', 2, async () => { const fs = await app._getAllLibraryFiles(); const f = pick(fs); if (!f) return 'x'; app._fbReplaceVersionWith('law', f.id, new File(['%PDF-1.4 ' + R(1e6)], `몽키 법령 ${R(999)}.pdf`, { type: 'application/pdf' })); await W(700); const c = choice(); if (c) { (rnd() < 0.7 ? c.querySelector('button[data-choice="0"]') : c.querySelector('button[data-choice="cancel"]'))?.click(); } await W(1200); return { undo: true, t: f.name.slice(0, 12) }; }],
    ['서식 같은 이름 올리기', 1, async () => { const ds = await app._getAllRepoDocuments(); const d = pick(ds); if (!d) return 'x'; app._fbCfg('repo').upload([new File(['새 판 ' + R(1e6)], d.name, { type: d.type || 'application/octet-stream' })], d.folderId ?? null); await W(1200); const b = pick(['owOverwriteBtn', 'owNumberedBtn', 'owCancelBtn']); document.getElementById(b)?.click(); await W(1000); return b; }],
    ['자료함 열고 닫기', 2, async () => { if (rnd() < 0.5) await app.openLawLibrary(); else await app.openDocumentRepo(); await W(800); esc(); await W(300); esc(); await W(300); esc(); await W(300); return 'ok'; }],
    ['처음 화면 목록 Delete', 1, async () => { if (app.focusMode || document.querySelector('.modal.show')) return 'x'; const c = pick([...document.querySelectorAll('#workflowList [data-sel-key]')].filter(vis)); if (!c) return 'x'; c.click(); await W(300); document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'Delete', bubbles: true })); await W(700); return 'ok'; }],
    // ── AI (허용판·가짜 AI) ──
    ['AI 업무파트너 질문', 3, async () => { if (!AI() || !app.focusMode) return 'x'; app.setAiPanelView?.('chat'); await W(500); const i = document.getElementById('aiInput'); if (!i || !vis(i)) return 'x'; i.value = pick(['이 할 일의 근거 조문은?', '수의계약 금액 기준 알려줘', '다음에 할 일은?']); i.dispatchEvent(new Event('input', { bubbles: true })); document.getElementById('aiSendBtn')?.click(); await W(2000); app.setAiPanelView?.('procedure'); await W(300); return 'ok'; }],
    ['AI 이 할 일 묻기', 2, async () => { const w = cur(); if (!AI() || !w || app.focusEditMode) return 'x'; app.askAboutItem?.(w.id, R(w.checklist.length)); await W(1200); app.setAiPanelView?.('procedure'); await W(300); return 'ok'; }],
    ['AI 편집', 2, async () => { const w = cur(); if (!AI() || !w || w.isReference || w.completedProcessed) return 'x'; await app.openAiRestructure(w.id); await W(900); if (rnd() < 0.3) { app._aiRsClose(); await W(300); return '닫기'; } await app._aiRsStart(); await W(1500); if (rnd() < 0.6) await app._aiRsApply?.(); else app._aiRsClose(); await W(1000); await settle(); if (app.focusEditMode) { if (rnd() < 0.5) app.exitFocusEditMode(); else { app.cancelFocusEditMode(); await W(400); await settle(); } } await W(800); return 'ok'; }],
  ];
  const total = A.reduce((s, a) => s + a[1], 0);
  window.__monkey = {
    init(s, ai) { seed = s; window.__monkeyAI = !!ai; practiceN = 0; return 'ok'; },
    async step() {
      let x = rnd() * total, act = A[0];
      for (const a of A) { if ((x -= a[1]) < 0) { act = a; break; } }
      const before = window.__canon ? await window.__canon({ times: false }) : null;
      let r;
      try { r = await act[2](); } catch (err) { return { name: act[0], err: 'ACTION ' + err.message }; }
      await settle();
      // 되돌릴 수 있는 동작: 반쯤은 바로 [되돌리기] → 하기 전과 같은지
      if (r && r.undo && before && rnd() < 0.5) {
        const b = undoBtn();
        if (b && vis(b)) {
          b.click(); await W(1300); await settle();
          const after = await window.__canon({ times: false });
          const d = window.__diff(before, after, 6);
          if (d.length) return { name: act[0], t: r.t, undoDiff: d };
          return { name: act[0] + ' → 되돌리기', t: r.t };
        }
      }
      return { name: act[0], t: typeof r === 'object' ? r.t : r };
    },
  };
  return 'monkey ok';
})();
