// 상태 사진(canon) · 비교(diff) — 왕복 시험·무작위 사용자 시험이 함께 씀 (페이지에 한 번 넣으면 window.__canon / window.__diff)
// __canon({ ids, times }) : 업무·세부 정보·법령·서식을 비교하기 좋은 모양으로 (ids=false면 업무 번호 대신 제목으로 짝짓기, times=false면 시각 빼기)
// __diff(a, b, max)      : 서로 다른 곳 경로 목록
window.__canon = async function ({ ids = true, times = true, live = false } = {}) {
  const A = app.allData;
  const T = v => (times ? v || null : undefined);
  const wfs = (A.workflows || []).filter(w => !w.isDraft && (!live || !w.isDeleted));
  const key = w => (ids ? String(w.id) : String(w.title || '').replace(/ \((가져옴|\d+)\)$/, ''));
  const files = arr => (arr || []).map(f => [f.name || f.fileName || '', f.size || 0]).sort();
  const out = { wf: {}, lib: [], repo: [] };
  for (const w of wfs) {
    const d = app.checklistDetails || {};
    const pd = d[`project-${w.id}`] || {};
    out.wf[key(w)] = {
      title: ids ? w.title : undefined, deadline: w.deadline || null, folder: ids ? (w.folderPath || '') : undefined,
      ref: ids ? !!w.isReference : undefined, done: ids ? !!w.completedProcessed : undefined, del: ids ? !!w.isDeleted : undefined,
      collab: ids && w.collab ? Object.values(w.collab.steps || {}).map(s => (s.assignee || '') + ':' + (s.status || '')).sort() : undefined,
      refs: files(pd.attachments), lib: (pd.linkedLibraryDocs || []).length,
      cl: (w.checklist || []).map(it => {
        const k = `${w.id}-${it.itemId}`;
        return {
          t: it.text, i: it.indent || 0, c: app.normalizeCompleted(it) === true, s: it.skipped === true ? (it.skipManual ? 'na' : 'br') : '',
          r: (it.result && it.result.text) || '', tip: (it.tip && it.tip.content) || '', dl: it.deadline || null, at: T(it.completedAt),
          docs: (it.linkedDocs || []).length, fm: (it.formats || []).length,
          br: (it.branchOptions || []).map(o => o.label).join('|'), taken: it.branchActionTaken ? it.branchActionTaken.label : '',
          rf: files((d[`${w.id}-r-${it.itemId}`] || {}).attachments), tf: files((d[`${w.id}-t-${it.itemId}`] || {}).attachments),
        };
      }),
    };
  }
  try { out.lib = (await app._getAllLibraryFiles()).map(f => [f.id, f.name, f.size]).sort((a, b) => a[0] - b[0]); } catch (e) {}
  try { out.repo = (await app._getAllRepoDocuments()).map(f => [f.id, f.name, f.size]).sort((a, b) => a[0] - b[0]); } catch (e) {}
  // 법령·서식 고유번호는 백업 복원 때 새로 매겨질 수 있음(업무의 연결은 따라 바뀜) → 이름·크기로만 비교
  out.lib = out.lib.map(x => x.slice(1)).sort(); out.repo = out.repo.map(x => x.slice(1)).sort();
  return JSON.parse(JSON.stringify(out));
};
window.__diff = function (a, b, max = 12) {
  const out = [];
  const walk = (x, y, p) => {
    if (out.length >= max) return;
    if (x === y) return;
    if (typeof x !== 'object' || typeof y !== 'object' || x === null || y === null) { out.push(`${p}: ${JSON.stringify(x)?.slice(0, 60)} → ${JSON.stringify(y)?.slice(0, 60)}`); return; }
    const ks = new Set([...Object.keys(x), ...Object.keys(y)]);
    for (const k of ks) walk(x[k], y[k], p ? `${p}.${k}` : k);
  };
  walk(a, b, '');
  return out;
};
'canon ok'
