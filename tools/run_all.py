# 한 줄로 모든 시험 돌리기 → 결과 표(tools/test_report.html · 화면 요약)
#   python run_all.py            기본: 기능 시험 전부(배포판·AI 허용판) + 왕복 + 많은 자료 + 예전 판 파일 + 업무 분담(브라우저 3개) + 무작위 사용자
#   python run_all.py --quick    빠르게: 전체 기능 시험·왕복·추천·문제 보고·무작위 짧게 (약 15분)
#   python run_all.py --matrix   + 환경 바꿔 돌리기(노트북 1366×768 · 다크 모드 · Edge)
#   python run_all.py --visual   + 화면 비교(설명서 촬영 → visual_diff.html)
#   python run_all.py --only 이름,이름   일부만 (이름 일부만 맞아도 됨)
# 모든 cdp3 시험은 SELFCHECK=1(단계마다 「서로 맞아야 하는 것」 검사기)로 돌림
# 실패로 보는 것: 단계 값이 「ERR …」 · ✗ 표시 · 검사기 위반 · 페이지 오류(EXC/console.error) · 실행기 비정상 종료·시간 초과 · 무작위/예전 판 문제 수 > 0
import io, os, re, sys, json, time, shutil, subprocess, threading, html
from concurrent.futures import ThreadPoolExecutor
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.dirname(here)
IDX = os.path.join(repo, 'index.html')
AIF = os.path.join(repo, 'ai_test .html')
EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
args = sys.argv[1:]
QUICK, MATRIX, VISUAL = '--quick' in args, '--matrix' in args, '--visual' in args
ONLY = args[args.index('--only') + 1].split(',') if '--only' in args else None
os.makedirs(os.path.join(here, '_ra'), exist_ok=True)

# (이름, 대본 만들기 [파일, 인자...], 앱, 추가 환경)
T = []
def cdp(name, gen, app=IDX, env=None, timeout=1500): T.append(('cdp3', name, gen, app, env or {}, timeout))
cdp('전체 기능(16부)', ['mk_full_test.py', 'all'], timeout=2700)
cdp('추천 1~4', ['mk_reco_test.py'])
cdp('왕복(새로 고침·되돌리기·내보내기·백업)', ['mk_roundtrip_test.py'])
cdp('문제 보고·오류 기록', ['mk_problem_test.py'])
if not QUICK:
    cdp('많은 자료(업무 300개)', ['mk_bigdata_test.py', '300'])
    for t in ['row', 'zoom', 'printwin', 'cltitle', 'skippanel', 'tip3', 'panel', 'skip', 'tip', 'icon', 'pick_panel', 'main8', 'report3', 'report', 'files',
              'common', 'hold', 'practice', 'skipbtn', 'ctxmenu', 'wide', 'tip3box', 'me', 'safe', 'home', 'tipexclude', 'netlock', 'done']:
        cdp(t, [f'mk_{t}_test.py'])
    cdp('perf(72줄)', ['mk_perf_test.py'])
    for t in ['read', 'guideback', 'tabs', 'law', 'aiedit', 'aifill']:
        cdp(t + ' (배포판: AI 숨김)', [f'mk_{t}_test.py', 'locked'])
    # AI 허용판(가짜 AI)
    for t in ['aifill', 'aifill2', 'docs', 'law', 'read', 'guideback', 'tabs', 'aisrc', 'aiedit', 'split', 'netlock']:
        cdp(t + ' (AI)', [f'mk_{t}_test.py'], app=AIF)
    cdp('왕복 (AI)', ['mk_roundtrip_test.py', 'ai'], app=AIF)
if MATRIX:
    cdp('전체 기능 · 노트북 1366×768', ['mk_full_test.py', 'all'], env={'VW': '1366', 'VH': '768'}, timeout=2700)
    cdp('전체 기능 · 다크 모드', ['mk_full_test.py', 'all'], env={'DARK': '1'}, timeout=2700)
    if os.path.exists(EDGE):
        cdp('전체 기능 · Edge', ['mk_full_test.py', 'all'], env={'CHROME_PATH': EDGE}, timeout=2700)
        cdp('왕복 · Edge', ['mk_roundtrip_test.py'], env={'CHROME_PATH': EDGE})
OTHER = []
if not QUICK:
    OTHER.append(('flow', '업무 분담 전체 흐름(브라우저 3개)', None))
    OTHER.append(('old', '예전 판(v1.4.0·v1.5.6) 파일', None))
MONKEYS = [(1, 600, False), (2, 600, False), (3, 600, False), (11, 400, True), (12, 400, True)] if not QUICK else [(1, 150, False), (11, 100, True)]
if ONLY:
    keep = lambda n: any(o in n for o in ONLY)
    T = [t for t in T if keep(t[1])]
    OTHER = [o for o in OTHER if keep(o[1])]
    MONKEYS = [m for m in MONKEYS if keep(f'무작위 {m[0]}')]

gen_lock = threading.Lock()
results = []
def judge(out, rc, timed_out):
    steps = len(re.findall(r'^> ', out, re.M))
    errs = [l for l in out.splitlines() if re.match(r'^> .*=> "ERR ', l)]
    bad = [l for l in out.splitlines() if l.startswith('> ') and '✗' in l]
    sc = [l for l in out.splitlines() if l.startswith('SELFCHECK')]
    logs = []
    m = re.search(r'^LOGS[^:]*:(.*)', out, re.M | re.S)
    if m: logs = [l for l in m.group(1).splitlines() if l.strip() and ('EXC' in l or 'ERR' in l) and 'favicon' not in l and not re.search(r'시험 오류|시험 거부|외부 통신 막음|시험: 외부 통신', l)]
    crash = rc != 0 or timed_out or ('LOGS' not in out and 'MONKEY 결과' not in out and 'OLDFILES 결과' not in out)
    problems = errs + bad + sc + logs + (['실행기가 끝까지 가지 못함(비정상 종료·시간 초과)' + (' · ' + out.strip().splitlines()[-1][:200] if out.strip() else '')] if crash else [])
    return steps, problems

def run_cdp(t, slot):
    _, name, gen, app, env, timeout = t
    sf = f'_ra/{re.sub(r"[^0-9A-Za-z가-힣]+", "_", name)}.json'
    with gen_lock:
        g = subprocess.run([sys.executable, gen[0], *gen[1:]], cwd=here, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if g.returncode != 0:
            return (name, 0, ['대본 만들기 실패: ' + (g.stderr or g.stdout)[-300:]], 0)
        shutil.copyfile(os.path.join(here, 'steps3.json'), os.path.join(here, sf))
    e = dict(os.environ, SELFCHECK='1', STEPS=sf, CDP_PORT='auto', CDP_PROF=f'chrome-ra-{slot}', **env)
    t0 = time.time(); to = False
    try:
        r = subprocess.run(['node', 'cdp3.mjs', app], cwd=here, env=e, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
        out, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as x:
        out, rc, to = (x.stdout or b'').decode('utf-8', 'replace') if isinstance(x.stdout, bytes) else (x.stdout or ''), 1, True
    open(os.path.join(here, sf.replace('.json', '.out.txt')), 'w', encoding='utf-8').write(out)
    steps, probs = judge(out, rc, to)
    return (name, steps, probs, round(time.time() - t0))

def run_other(kind, name):
    t0 = time.time()
    if kind == 'flow':
        subprocess.run([sys.executable, 'mk_flow_test.py'], cwd=here, capture_output=True)
        r = subprocess.run(['node', 'collab2.mjs', IDX, 'steps_flow.json'], cwd=here, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
        out = r.stdout + r.stderr
        for f in ['fl2_reply.json', 'fl2_request.json', 'fl_export.json', 'fl_reply_B.json', 'fl_reply_C1.json', 'fl_reply_C2.json', 'fl_request.json', 'fl_share.json']:
            subprocess.run(['git', 'checkout', '--', 'tools/' + f], cwd=repo, capture_output=True)  # 시험이 덮어쓴 예시 파일 되돌리기
        steps = len(re.findall(r'^\[[ABC]\] .* => ', out, re.M))
        probs = [l for l in out.splitlines() if re.search(r'=> "?ERR |✗', l)] + [l for l in out.splitlines() if re.match(r'LOGS [ABC]: \S', l)]
        if r.returncode != 0 or 'LOGS A' not in out: probs.append('실행기가 끝까지 가지 못함')
        open(os.path.join(here, '_ra/flow.out.txt'), 'w', encoding='utf-8').write(out)
        return (name, steps, probs, round(time.time() - t0))
    if kind == 'old':
        r = subprocess.run([sys.executable, 'oldfiles_test.py'], cwd=here, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
        out = r.stdout + r.stderr
        probs = [l.strip() for l in out.splitlines() if '✗' in l or 'SELFCHECK' in l or 'EXC' in l]
        if 'OLDFILES 결과' not in out: probs.append('끝까지 가지 못함 ' + out[-200:])
        open(os.path.join(here, '_ra/old.out.txt'), 'w', encoding='utf-8').write(out)
        return (name, len(re.findall(r'=> ', out)), probs, round(time.time() - t0))

def run_monkey(seed, n, ai):
    t0 = time.time()
    try:
        r = subprocess.run(['node', 'monkey.mjs', AIF if ai else IDX, str(seed), str(n)] + (['ai'] if ai else []), cwd=here, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=n * 12 + 600)
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired as x:
        out = '시간 초과'
    m = re.search(r'MONKEY 결과 .*동작=(\d+) .*문제=(\d+)', out)
    probs = [l for l in out.splitlines() if l.startswith('문제 #')]
    if not m: probs.append('끝까지 가지 못함 ' + out[-200:])
    open(os.path.join(here, f'_ra/monkey_{seed}{"_ai" if ai else ""}.out.txt'), 'w', encoding='utf-8').write(out)
    return (f'무작위 사용자 {seed}{" (AI)" if ai else ""}', int(m.group(1)) if m else 0, probs, round(time.time() - t0))

start = time.time()
print(f'시험 {len(T)}개 + 기타 {len(OTHER)} + 무작위 {len(MONKEYS)} 시작 ({time.strftime("%H:%M")})', flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = [ex.submit(run_monkey, *m) for m in MONKEYS]
    futs += [ex.submit(run_other, *o[:2]) for o in OTHER]
    slots = list(range(3))
    slot_lock = threading.Lock()
    def with_slot(t):
        with slot_lock: s = slots.pop(0)
        try: return run_cdp(t, s)
        finally:
            with slot_lock: slots.append(s)
    with ThreadPoolExecutor(max_workers=3) as ex2:
        for r in ex2.map(with_slot, T):
            results.append(r); print(f"{'✓' if not r[2] else '✗'} {r[0]} — {r[1]}단계 · {r[3]}초" + (f" · 문제 {len(r[2])}" if r[2] else ''), flush=True)
    for f in futs:
        r = f.result(); results.append(r); print(f"{'✓' if not r[2] else '✗'} {r[0]} — {r[1]}단계 · {r[3]}초" + (f" · 문제 {len(r[2])}" if r[2] else ''), flush=True)
if VISUAL:
    t0 = time.time()
    subprocess.run([sys.executable, 'mkman2.py'], cwd=here, capture_output=True)
    subprocess.run(['node', 'cdp2.mjs', IDX], cwd=here, capture_output=True, timeout=1800)
    r = subprocess.run([sys.executable, 'visual_diff.py'], cwd=here, capture_output=True, text=True, encoding='utf-8', errors='replace')
    ch = [l for l in r.stdout.splitlines() if '바뀜' in l or '없음' in l]
    results.append(('화면 비교(설명서 60장면)', 60, [f'(확인) {l}' for l in ch], round(time.time() - t0)))
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '화면 비교 실패')

ok = [r for r in results if not r[2] or all(p.startswith('(확인)') for p in r[2])]
total_steps = sum(r[1] for r in results)
mins = round((time.time() - start) / 60)
rows = ''.join(f"<tr class='{'ok' if r in ok else 'ng'}'><td>{'✓' if r in ok else '✗'}</td><td>{html.escape(r[0])}</td><td>{r[1]}</td><td>{r[3]}초</td><td>{'<br>'.join(html.escape(p[:400]) for p in r[2][:15])}</td></tr>" for r in sorted(results, key=lambda r: (r in ok, r[0])))
open(os.path.join(here, 'test_report.html'), 'w', encoding='utf-8').write(
    f"<!doctype html><meta charset='utf-8'><title>시험 결과</title><style>body{{font-family:'Malgun Gothic',sans-serif;margin:20px}}table{{border-collapse:collapse}}td,th{{border:1px solid #ddd;padding:6px 8px;vertical-align:top;font-size:13px}}.ng td{{background:#fff1f1}}.ok td:first-child{{color:#16a34a}}.ng td:first-child{{color:#dc2626;font-weight:700}}</style>"
    f"<h2>시험 결과 — {time.strftime('%Y-%m-%d %H:%M')} · 통과 {len(ok)}/{len(results)} · {total_steps}단계 · {mins}분</h2><table><tr><th></th><th>시험</th><th>단계</th><th>걸린 시간</th><th>문제</th></tr>{rows}</table>"
    f"<p>자세한 출력: tools/_ra/*.out.txt · 무작위 사용자 실패 화면: tools/monkey_fail_*.png · 화면 비교: tools/visual_diff.html</p>")
print(f'\nRUN_ALL 결과 통과 {len(ok)}/{len(results)} · {total_steps}단계 · {mins}분 — tools/test_report.html')
sys.exit(0 if len(ok) == len(results) else 1)
