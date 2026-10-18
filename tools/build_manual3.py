# 사용 설명서 만들기 (v4 · 기능 하나 = A4 한 쪽)
#   python build_manual3.py ../사용설명서        → 업무내비게이터_사용설명서.html + img/
#   node mk_manual_pdf.mjs                        → 업무내비게이터_사용설명서.pdf (쪽 넘침 검사 포함)
# 내용은 manual_data3.py, 사진·강조 위치는 cdp2.mjs 촬영 결과(man2/*.png · man2_out.txt)
import json, os, re, sys, html
from PIL import Image   # pip install pillow
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from manual_data3 import CHAPTERS, KEYS, FAQ, TERMS

_m = re.search(r"const APP_VERSION = '([^']+)'", open(os.path.join(here, '..', 'index.html'), encoding='utf-8').read())
APP_VER = _m.group(1) if _m else ''
out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', '사용설명서')
img_dir = os.path.join(out_dir, 'img')
os.makedirs(img_dir, exist_ok=True)
esc = html.escape
made = {}   # 만든 사진 파일 → 자른 자리

# ── 강조 위치 (촬영 결과, 1440×810 화면 기준) ──
SW, SH = 1440, 810
hl = {}
for line in open(os.path.join(here, 'man2_out.txt'), encoding='utf-8'):
    m = re.match(r'> (\S+) => "(.*)"\s*$', line)
    if m:
        try: hl[m.group(1)] = json.loads(json.loads('"' + m.group(2) + '"')).get('hl')
        except Exception: pass

# ── 사진 자르기: 주황 테두리 둘레를 잘라 A4에서도 글자가 보이게 ──
IMG_W, IMG_HMAX = 178.0, 122.0   # mm (본문 폭 · 사진 최대 높이)
def crop_rect(name, crop):
    r = hl.get(name)
    if r and (r['w'] < 4 or r['h'] < 4 or (r['w'] >= SW - 2 and r['h'] >= SH - 2)): r = None
    if isinstance(crop, tuple): return crop, r
    if crop == 'full' or not r: return (0, 0, SW, SH), r
    pad = 36
    x0, y0, x1, y1 = r['x'] - pad, r['y'] - pad, r['x'] + r['w'] + pad, r['y'] + r['h'] + pad
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = max(w, 820)                       # 너무 크게 키우지 않음(최대 약 1.8배)
    if w / h > 2.1: h = w / 2.1           # 가로로 너무 길면 위아래 여유
    if w / h < 1.45: w = min(SW, h * 1.45)  # 세로로 길면 옆으로 넓힘
    w, h = min(w, SW), min(h, SH)
    x = min(max(0, cx - w / 2), SW - w); y = min(max(0, cy - h / 2), SH - h)
    return (round(x), round(y), round(w), round(h)), r

def shot_html(name, title, crop, hmax=IMG_HMAX, mark=True):
    (x, y, w, h), r = crop_rect(name, crop)
    wmm = min(IMG_W, hmax * w / h)
    box = ''
    if r and mark:
        bx, by = (r['x'] - x) / w * 100, (r['y'] - y) / h * 100
        bw, bh = r['w'] / w * 100, r['h'] / h * 100
        box = f'<span class="hl" style="left:{bx:.2f}%;top:{by:.2f}%;width:{bw:.2f}%;height:{bh:.2f}%"></span>'
    # 잘라 낸 사진을 JPG로 저장 (큰 PNG를 그대로 넣으면 PDF 만들기가 멈추고 파일도 큼)
    fn = f'{name}.jpg'
    if fn not in made:
        im = Image.open(os.path.join(here, 'man2', name + '.png')).convert('RGB')
        k = im.width / SW
        im = im.crop((round(x * k), round(y * k), round((x + w) * k), round((y + h) * k)))
        if im.width > 1700: im = im.resize((1700, round(im.height * 1700 / im.width)), Image.LANCZOS)
        im.save(os.path.join(img_dir, fn), quality=88, optimize=True)
        made[fn] = (x, y, w, h)
    assert made[fn] == (x, y, w, h), f'{name}: 같은 사진을 다르게 자름'
    return (f'<div class="shot" style="width:{wmm:.1f}mm;aspect-ratio:{w}/{h}">'
            f'<img src="img/{fn}" alt="{esc(title)} 화면">{box}</div>')

# ── 쪽 목록 만들기 ──
# 쪽: dict(kind, chap, body, id)   쪽 번호는 순서대로(표지 제외 표시)
pages = []
def add(kind, body, chap='', pid=''):
    pages.append(dict(kind=kind, body=body, chap=chap, id=pid))

feat_pages = []   # (장 번호, 기능 번호, 제목, id)
for ci, (ctitle, cintro, feats) in enumerate(CHAPTERS, 1):
    for fi, f in enumerate(feats, 1):
        feat_pages.append((ci, fi, f['title'], f['img']))

APPX = [('keys', '마우스와 단축키'), ('faq', '자주 묻는 질문'), ('terms', '용어 풀이')]

# 목차 줄 수로 목차 쪽 수 정하기
TOC_PER_PAGE = 36
toc_lines = len(CHAPTERS) + len(feat_pages) + 1 + len(APPX) + 3
n_toc = (toc_lines + TOC_PER_PAGE - 1) // TOC_PER_PAGE

# 앞쪽: 표지(1) · 목차(n_toc) · 보는 법(1) · 빠른 시작(1)
FRONT = 1 + n_toc + 2
# 기능 쪽 번호 미리 계산 (부록 쪽 수는 아래에서 정함)
pno = {}
p = FRONT + 1
for (ci, fi, t, pid) in feat_pages:
    pno[pid] = p; p += 1
# 부록 쪽 나눔(넘치면 여기 숫자를 고침): 단축키 묶음 / 질문 / 용어
KEY_SPLIT = [[0, 1, 2], [3, 4]]
FAQ_SPLIT = [FAQ[:5], FAQ[5:]]
appx_first = {}
appx_first['keys'] = p; p += len(KEY_SPLIT)
appx_first['faq'] = p; p += len(FAQ_SPLIT)
appx_first['terms'] = p; p += 1
pno.update(appx_first)
pno['quick'] = FRONT; pno['howto'] = FRONT - 1

def ref(pid):
    return f'<a href="#p-{pid}">{pno[pid]}쪽</a>'

title_of = {pid: t for (_, _, t, pid) in feat_pages}
title_of.update({'keys': '마우스와 단축키', 'faq': '자주 묻는 질문', 'terms': '용어 풀이'})

# 표지
add('cover', f'''<div class="cover">
  <div class="cv-top">소방 공무원을 위한 업무 관리 프로그램</div>
  <h1>업무 내비게이터<br><span>사용 설명서</span></h1>
  <div class="cv-ver">v{esc(APP_VER)} · 2026. 10.</div>
  <div class="cv-shot">{shot_html("01_main", "첫 화면", "full", mark=False)}</div>
  <ul class="cv-pts"><li>업무를 <b>단계와 할 일</b> 체크리스트로</li><li>일하면서 <b>처리결과 · 업무팁 · 서식</b>을 쌓아</li><li>다음 담당자에게 <b>그대로 물려줍니다</b></li></ul>
  <div class="cv-foot">설치 없이 · 서버 없이 · 이 PC 안에만 저장</div>
</div>''', pid='cover')

# 목차
toc = []
toc.append(('h', '처음에', ''))
toc.append(('i', '이 설명서 보는 법', 'howto'))
toc.append(('i', '5분 만에 시작하기', 'quick'))
for ci, (ctitle, cintro, feats) in enumerate(CHAPTERS, 1):
    toc.append(('h', f'{ci}장 {ctitle}', feats[0]['img']))
    for fi, f in enumerate(feats, 1):
        toc.append(('i', f'{ci}-{fi} {f["title"]}', f['img']))
toc.append(('h', '부록', 'keys'))
for pid, t in APPX: toc.append(('i', t, pid))
for k in range(n_toc):
    rows = toc[k * TOC_PER_PAGE:(k + 1) * TOC_PER_PAGE]
    lis = ''.join(
        (f'<li class="toc-h"><a href="#p-{pid}"><span>{esc(t)}</span><i></i><em>{pno[pid] if pid else ""}</em></a></li>' if kind == 'h' and pid else
         f'<li class="toc-h"><span>{esc(t)}</span></li>' if kind == 'h' else
         f'<li><a href="#p-{pid}"><span>{esc(t)}</span><i></i><em>{pno[pid]}</em></a></li>') for kind, t, pid in rows)
    add('toc', f'<h1 class="pt">목차</h1><ul class="toc">{lis}</ul>' if k == 0 else f'<ul class="toc">{lis}</ul>', '목차', 'toc' if k == 0 else '')

# 보는 법
add('front', f'''<h1 class="pt">이 설명서 보는 법</h1>
<p class="lead">기능 하나를 한 쪽에 담았습니다. 모든 쪽은 같은 순서로 되어 있어, 필요한 기능만 찾아 읽으면 됩니다.</p>
<div class="howto">
 <div class="ht-row"><b>제목</b><span>그 쪽에서 할 수 있는 일 (예: 「업무팁 적기」)</span></div>
 <div class="ht-row"><b>사진</b><span><span class="hl-sample"></span> 주황 테두리가 누르거나 볼 곳입니다. 사진은 필요한 부분만 잘라 크게 보여 줍니다.</span></div>
 <div class="ht-row"><b>따라 하기</b><span>번호 순서대로 누르면 됩니다.</span></div>
 <div class="ht-row"><b>알아 두기 · 주의</b><span>알면 편한 것과 꼭 지켜야 할 것입니다.</span></div>
</div>
<h2 class="sh">표기</h2>
<table class="tbl"><tr><th><b>[시작하기]</b></th><td>화면의 단추 · 메뉴 이름 (화면과 똑같이 적었습니다)</td></tr>
<tr><th><kbd>Ctrl</kbd>+<kbd>Z</kbd></th><td>키보드 키 (동시에 누름)</td></tr>
<tr><th>오른쪽 클릭</th><td>마우스 오른쪽 단추로 누르면 그 자리에서 할 수 있는 명령이 나옵니다.</td></tr></table>
<div class="note tip"><span class="nl">알아 두기</span><p>알면 더 편한 방법과 참고할 내용입니다.</p></div>
<div class="note warn"><span class="nl">주의</span><p>자료를 잃거나 문제가 될 수 있는 것입니다.</p></div>
<h2 class="sh">시작 전에</h2>
<ul class="dots">
 <li>프로그램은 HTML 파일 하나입니다. <b>엣지</b>나 <b>크롬</b>으로 열면 바로 쓸 수 있고, 설치할 것이 없습니다.</li>
 <li>자료는 서버가 아니라 <b>이 PC의 브라우저 안</b>에만 저장됩니다. 늘 같은 브라우저로 여세요.</li>
 <li>사진은 프로그램 안에 들어 있는 <b>연습 업무</b>(가상 자료)로 찍었습니다. 「연습 업무 넣기」({ref("39_practice")})로 똑같이 따라 해 볼 수 있습니다.</li>
 <li>AI 기능은 이 설명서에서 다루지 않습니다.</li>
</ul>''', '처음에', 'howto')

# 빠른 시작
qs = [("연습 업무 넣기", "왼쪽 위 [새 업무 만들기] 옆 ▾ → 연습 업무 넣기", "39_practice"),
      ("업무 열기", "「[연습] 소모품 구매」 카드를 누릅니다.", "13_focus"),
      ("체크하기", "할 일 앞 동그라미를 누릅니다. 단계가 끝나면 다음 단계가 펼쳐집니다.", "17_work"),
      ("처리결과 남기기", "줄을 한 번 누르고 한 줄 적은 뒤 Enter.", "17_work"),
      ("업무팁·서식 보기", "오른쪽 업무 절차에서 놓치기 쉬운 것과 근거를 확인합니다.", "17b_thumbs"),
      ("갈림길 고르기", "「금액 기준 확인」 줄의 [1인 견적] → [실행].", "40_practice_skip"),
      ("보고서 출력", "왼쪽 [진행상황 출력] → [인쇄 · PDF].", "22d_checklist"),
      ("내 업무 만들기", "[새 업무 만들기] → 이름 → 단계와 할 일 → [바로 시작].", "05_step1")]
qhtml = ''.join(f'<li><span class="qn">{i}</span><div><b>{esc(a)}</b><p>{esc(b)}</p></div><em>{ref(pid)}</em></li>' for i, (a, b, pid) in enumerate(qs, 1))
add('front', f'''<h1 class="pt">5분 만에 시작하기</h1>
<p class="lead">연습 업무로 이 프로그램의 핵심 흐름을 한 번 해 봅니다. 자세한 방법은 오른쪽 쪽 번호를 보세요.</p>
<ol class="quick">{qhtml}</ol>
<div class="note tip"><span class="nl">알아 두기</span><p>연습 업무는 다 해 본 뒤 지우면 됩니다. 내 업무와 섞이지 않게 제목 앞에 [연습]이 붙어 있습니다.</p></div>''', '처음에', 'quick')

# 기능 쪽
for ci, (ctitle, cintro, feats) in enumerate(CHAPTERS, 1):
    for fi, f in enumerate(feats, 1):
        band = (f'<div class="band"><div class="band-no">{ci}</div><div><div class="band-t">{esc(ctitle)}</div>'
                f'<div class="band-i">{cintro}</div></div></div>') if fi == 1 else ''
        steps = ''.join(f'<li>{s}</li>' for s in f['steps'])
        notes = ''.join(f'<div class="note {k}"><span class="nl">{"알아 두기" if k == "tip" else "주의"}</span><p>{t}</p></div>' for k, t in f['notes'])
        see = ''
        if f['see']:
            see = '<div class="see">함께 보기 ' + ' · '.join(f'<a href="#p-{s}">{esc(title_of[s])} <em>{pno[s]}쪽</em></a>' for s in f['see']) + '</div>'
        body = f'''{band}<div class="ft"><span class="fno">{ci}-{fi}</span><h2>{esc(f["title"])}</h2></div>
<p class="lead">{f["lead"]}</p>
{shot_html(f["img"], f["title"], f["crop"], IMG_HMAX - (16 if band else 0))}
<div class="steps-h">따라 하기</div><ol class="steps">{steps}</ol>
{notes}{see}'''
        add('feat', body, f'{ci}장 {ctitle}', f['img'])

# 부록 — 단축키
for k, grp in enumerate(KEY_SPLIT):
    tb = ''
    for gi in grp:
        t, rows = KEYS[gi]
        tb += f'<h2 class="sh">{esc(t)}</h2><table class="tbl keys">' + ''.join(f'<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>' for a, b in rows) + '</table>'
    add('appx', (f'<h1 class="pt">부록 · 마우스와 단축키</h1><p class="lead">윈도우 탐색기와 같은 방식입니다: 한 번 누르면 고르기, 두 번 누르면 열기, 오른쪽 클릭은 메뉴.</p>' if k == 0 else '') + tb,
        '부록', 'keys' if k == 0 else '')
# 부록 — 자주 묻는 질문
for k, part in enumerate(FAQ_SPLIT):
    qa = ''.join(f'<div class="qa"><div class="q">Q. {esc(q)}</div><p>{a}</p></div>' for q, a in part)
    add('appx', (f'<h1 class="pt">부록 · 자주 묻는 질문</h1>' if k == 0 else '') + qa, '부록', 'faq' if k == 0 else '')
# 부록 — 용어
add('appx', '<h1 class="pt">부록 · 용어 풀이</h1><table class="tbl terms">' + ''.join(f'<tr><th>{esc(a)}</th><td>{b}</td></tr>' for a, b in TERMS) + '</table>', '부록', 'terms')

# 쪽 번호 확인 (미리 계산한 것과 실제 순서가 같은지)
for i, pg in enumerate(pages, 1):
    if pg['id'] and pg['id'] in pno and pg['id'] not in ('cover', 'toc'):
        assert pno[pg['id']] == i, (pg['id'], pno[pg['id']], i)

# ── 쓰지 않는 사진 지우기 ──
for fn in os.listdir(img_dir):
    if fn not in made: os.remove(os.path.join(img_dir, fn))
used = made

# ── HTML ──
body = []
for i, pg in enumerate(pages, 1):
    head = '' if pg['kind'] == 'cover' else f'<div class="ph"><span>업무 내비게이터 사용 설명서</span><span>{esc(pg["chap"])}</span></div>'
    foot = '' if pg['kind'] == 'cover' else f'<div class="pf">{i}</div>'
    pid = f' id="p-{pg["id"]}"' if pg['id'] else ''
    body.append(f'<section class="pg pg-{pg["kind"]}"{pid}>{head}<div class="pb">{pg["body"]}</div>{foot}</section>')

CSS = '''
:root { --ac:#2563eb; --ac2:#eef4ff; --tx:#1e2d47; --mu:#64748b; --ln:#e2e8f0; --hl:#f59e0b; --warn:#dc2626; --warnbg:#fef2f2; --tipbg:#eff6ff; --page:#fff; --desk:#e7eaf0; }
* { box-sizing:border-box; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body { margin:0; background:var(--desk); color:var(--tx); font-family:'Pretendard','Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif; font-size:10.5pt; line-height:1.6; word-break:keep-all; overflow-wrap:break-word; }
a { color:inherit; text-decoration:none; }
.pg { scroll-margin-top:14mm; position:relative; width:210mm; height:297mm; margin:10mm auto; background:var(--page); box-shadow:0 2px 12px rgba(15,23,42,.12); overflow:hidden; }
.pb { position:absolute; left:16mm; right:16mm; top:20mm; bottom:16mm; overflow:hidden; }
.ph { position:absolute; left:16mm; right:16mm; top:9mm; display:flex; justify-content:space-between; font-size:8pt; color:var(--mu); border-bottom:.3mm solid var(--ln); padding-bottom:1.6mm; }
.ph span:last-child { color:var(--ac); font-weight:700; }
.pf { position:absolute; left:0; right:0; bottom:7mm; text-align:center; font-size:8.5pt; color:var(--mu); }
kbd { display:inline-block; padding:0 1.4mm; border:.25mm solid #cbd5e1; border-bottom-width:.6mm; border-radius:1.2mm; background:#f8fafc; font-family:inherit; font-size:8.5pt; line-height:1.45; }
.lead { margin:0 0 4mm; font-size:10.5pt; color:#334155; }
/* 장 띠 */
.band { display:flex; gap:4mm; align-items:center; background:var(--ac2); border-radius:3mm; padding:3.5mm 5mm; margin:0 0 6mm; }
.band-no { flex:none; width:12mm; height:12mm; border-radius:2.5mm; background:var(--ac); color:#fff; font-size:17pt; font-weight:800; display:flex; align-items:center; justify-content:center; }
.band-t { font-size:13pt; font-weight:800; color:var(--ac); }
.band-i { font-size:9pt; color:#475569; line-height:1.5; }
/* 기능 제목 */
.ft { display:flex; align-items:baseline; gap:3mm; margin:0 0 2mm; }
.ft h2 { margin:0; font-size:17pt; letter-spacing:-.02em; }
.fno { font-size:10pt; font-weight:800; color:var(--ac); }
/* 사진 */
.shot { position:relative; overflow:hidden; margin:0 auto 5mm; border:.3mm solid #cbd5e1; border-radius:2mm; background:#0f172a; }
.shot img { display:block; width:100%; height:100%; }
.hl { position:absolute; border:.7mm solid var(--hl); border-radius:1.5mm; box-shadow:0 0 0 .9mm rgba(245,158,11,.25); }
/* 따라 하기 */
.steps-h { font-size:9pt; font-weight:800; color:var(--ac); letter-spacing:.05em; margin:0 0 1.5mm; }
.steps { list-style:none; counter-reset:s; margin:0 0 4mm; padding:0; }
.steps li { counter-increment:s; position:relative; padding:0 0 0 9mm; margin:0 0 2.2mm; }
.steps li::before { content:counter(s); position:absolute; left:0; top:.3mm; width:5.6mm; height:5.6mm; border-radius:50%; background:var(--ac); color:#fff; font-size:8.5pt; font-weight:800; display:flex; align-items:center; justify-content:center; line-height:1; }
/* 알아 두기 · 주의 */
.note { border-left:1.1mm solid var(--ac); background:var(--tipbg); border-radius:0 2mm 2mm 0; padding:2.2mm 4mm; margin:0 0 2.5mm; font-size:9.5pt; }
.note .nl { display:block; font-size:8.5pt; font-weight:800; color:var(--ac); margin-bottom:.3mm; }
.note p { margin:0; }
.note.warn { border-left-color:var(--warn); background:var(--warnbg); }
.note.warn .nl { color:var(--warn); }
.see { margin-top:3mm; font-size:9pt; color:var(--mu); }
.see a { color:var(--ac); margin-left:1.5mm; } .see em { font-style:normal; color:var(--mu); }
/* 앞쪽 · 부록 */
.pt { font-size:20pt; margin:0 0 4mm; letter-spacing:-.02em; }
.sh { font-size:11.5pt; margin:6mm 0 2.5mm; color:var(--ac); }
.tbl { width:100%; border-collapse:collapse; font-size:9.5pt; margin:0 0 2mm; }
.tbl th, .tbl td { border:.25mm solid var(--ln); padding:1.8mm 3mm; text-align:left; vertical-align:top; }
.tbl th { width:38%; background:#f8fafc; font-weight:700; }
.terms th { width:30%; }
.dots { margin:0; padding-left:5mm; } .dots li { margin:0 0 1.8mm; }
.howto { border:.3mm solid var(--ln); border-radius:2.5mm; overflow:hidden; }
.ht-row { display:flex; gap:4mm; padding:2.4mm 4mm; border-top:.3mm solid var(--ln); } .ht-row:first-child { border-top:0; }
.ht-row b { flex:none; width:30mm; color:var(--ac); }
.hl-sample { display:inline-block; width:8mm; height:4mm; border:.6mm solid var(--hl); border-radius:1mm; vertical-align:-.6mm; }
.quick { list-style:none; margin:0 0 5mm; padding:0; }
.quick li { display:flex; align-items:center; gap:4mm; padding:3mm 0; border-bottom:.3mm solid var(--ln); }
.quick .qn { flex:none; width:8mm; height:8mm; border-radius:50%; background:var(--ac); color:#fff; font-weight:800; display:flex; align-items:center; justify-content:center; }
.quick div { flex:1; } .quick p { margin:.3mm 0 0; color:#475569; font-size:9.5pt; }
.quick em { font-style:normal; color:var(--ac); font-size:9pt; flex:none; }
.qa { margin:0 0 5mm; } .qa .q { font-weight:800; color:var(--ac); margin-bottom:1mm; } .qa p { margin:0; }
/* 목차 */
.toc { list-style:none; margin:0; padding:0; }
.toc li { font-size:9.8pt; line-height:1.55; padding:.45mm 0 .45mm 6mm; }
.toc li.toc-h { padding-left:0; margin-top:2.6mm; font-weight:800; color:var(--ac); font-size:10.5pt; }
.toc a { display:flex; align-items:baseline; gap:2mm; }
.toc i { flex:1; border-bottom:.3mm dotted #94a3b8; transform:translateY(-1mm); }
.toc em { font-style:normal; min-width:7mm; text-align:right; }
/* 표지 */
.pg-cover .pb { top:22mm; bottom:18mm; }
.cover { height:100%; display:flex; flex-direction:column; }
.cv-top { color:var(--ac); font-weight:700; font-size:11pt; }
.cover h1 { font-size:34pt; line-height:1.2; margin:3mm 0 2mm; letter-spacing:-.03em; }
.cover h1 span { font-size:22pt; color:#475569; font-weight:700; }
.cv-ver { color:var(--mu); margin-bottom:10mm; }
.cv-shot .shot { box-shadow:0 3mm 8mm rgba(15,23,42,.18); }
.cv-pts { list-style:none; padding:0; margin:6mm 0 0; font-size:12pt; } .cv-pts li { padding:1.5mm 0 1.5mm 6mm; position:relative; }
.cv-pts li::before { content:''; position:absolute; left:0; top:4mm; width:2.4mm; height:2.4mm; border-radius:50%; background:var(--ac); }
.cv-foot { margin-top:auto; border-top:.3mm solid var(--ln); padding-top:4mm; color:var(--mu); font-size:10pt; }
/* 화면에서 볼 때 */
.topbar { position:sticky; top:0; z-index:5; display:flex; justify-content:center; gap:3mm; padding:2.5mm; background:rgba(231,234,240,.92); backdrop-filter:blur(4px); font-size:10pt; }
.topbar a { background:#fff; border:1px solid #cbd5e1; border-radius:999px; padding:1mm 4mm; }
@media screen and (max-width:820px) {
  .pg { width:auto; height:auto; margin:12px; }
  .pb, .ph, .pf { position:static; }
  .pb { padding:16px; } .ph { padding:12px 16px 6px; margin:0 16px; } .pf { padding:8px 0 14px; }
  .shot { width:100% !important; }
}
@media print {
  @page { size:A4; margin:0; }
  body { background:#fff; }
  .topbar { display:none; }
  .pg { margin:0; box-shadow:none; break-after:page; }
}
'''
page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>업무 내비게이터 사용 설명서</title>
<style>{CSS}</style></head><body>
<div class="topbar"><a href="#p-toc">목차</a><a href="#p-quick">5분 만에 시작하기</a><a href="#p-faq">자주 묻는 질문</a></div>
{''.join(body)}
</body></html>'''
open(os.path.join(out_dir, '업무내비게이터_사용설명서.html'), 'w', encoding='utf-8', newline='\r\n').write(page)
print('pages', len(pages), 'features', len(feat_pages), 'images', len(used))
