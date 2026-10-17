# 화면 비교: 설명서 촬영(mkman2 → cdp2)으로 새로 찍은 tools/man2/*.png 를 기준 사진(사용설명서/img/*.png)과 비교
# 바뀐 칸의 비율(%)을 재고, 기준을 넘는 장면은 「기준 | 지금 | 다른 곳(빨강)」 사진을 tools/_vd/에 만들어 visual_diff.html로 보여 줌
# 날짜(D-n)·시각처럼 날마다 바뀌는 글 때문에 1% 안팎은 늘 다를 수 있음 → 기본 기준 2%
# 실행: (tools 폴더에서) python visual_diff.py [기준%=2]
import os, sys, io, html
from PIL import Image, ImageChops
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
here = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(here, '..', '사용설명서', 'img')
new_dir = os.path.join(here, 'man2')
out_dir = os.path.join(here, '_vd')
os.makedirs(out_dir, exist_ok=True)
TH = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
rows, changed = [], 0
for name in sorted(os.listdir(base_dir)):
    if not name.endswith('.png'): continue
    nb = os.path.join(new_dir, name)
    if not os.path.exists(nb):
        rows.append((name, None, '새로 찍은 사진 없음')); continue
    a = Image.open(os.path.join(base_dir, name)).convert('RGB')
    b = Image.open(nb).convert('RGB')
    if a.size != b.size: b = b.resize(a.size)
    d = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > 24 else 0)
    hist = d.histogram()
    pct = hist[255] / (a.size[0] * a.size[1]) * 100
    note = ''
    if pct > TH:
        changed += 1
        w, h = a.size
        sm = (w // 3, h // 3)
        red = Image.new('RGB', a.size, (255, 0, 0))
        over = Image.composite(red, b.convert('RGB'), d).resize(sm)
        sheet = Image.new('RGB', (sm[0] * 3 + 20, sm[1]), 'white')
        sheet.paste(a.resize(sm), (0, 0)); sheet.paste(b.resize(sm), (sm[0] + 10, 0)); sheet.paste(over, (sm[0] * 2 + 20, 0))
        sheet.save(os.path.join(out_dir, name))
        note = f'_vd/{name}'
    rows.append((name, pct, note))
body = ''.join(f"<tr class='{'ch' if (p or 0) > TH else ''}'><td>{html.escape(n)}</td><td>{'-' if p is None else f'{p:.2f}%'}</td><td>{('<img src=\"' + note + '\" style=\"max-width:900px\">') if note.startswith('_vd') else html.escape(note)}</td></tr>" for n, p, note in rows)
open(os.path.join(here, 'visual_diff.html'), 'w', encoding='utf-8').write(
    f"<!doctype html><meta charset='utf-8'><title>화면 비교</title><style>body{{font-family:'Malgun Gothic',sans-serif;margin:20px}}td{{border-bottom:1px solid #ddd;padding:6px;vertical-align:top}}.ch td:first-child{{color:#c00;font-weight:700}}</style>"
    f"<h2>화면 비교 — 기준(설명서 사진) | 지금 | 다른 곳(빨강) · 기준 {TH}%</h2><p>바뀐 장면 {changed} / {len(rows)}</p><table>{body}</table>")
for n, p, note in rows:
    if p is None or p > TH: print(f"{n}: {'사진 없음' if p is None else f'{p:.2f}% 바뀜'}")
print(f'VISUAL 결과 바뀐 장면={changed} / {len(rows)} (기준 {TH}%) — tools/visual_diff.html')
