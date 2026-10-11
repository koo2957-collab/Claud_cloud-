import json, os, re, shutil, sys, html
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from manual_data2 import CHAPTERS, KEYS
out_dir = sys.argv[1]
img_dir = os.path.join(out_dir, 'img')
os.makedirs(img_dir, exist_ok=True)
# 강조 위치 (시나리오 실행 결과)
hl = {}
for line in open(os.path.join(here, 'man2_out.txt'), encoding='utf-8'):
    m = re.match(r'> (\S+) => "(.*)"\s*$', line)
    if m:
        try: hl[m.group(1)] = json.loads(json.loads('"' + m.group(2) + '"')).get('hl')
        except Exception: pass
W, H = 1440, 810
toc, body = [], []
n = 0
for ci, (title, intro, scenes) in enumerate(CHAPTERS):
    cid = f'ch{ci}'
    toc.append(f'<li><a href="#{cid}">{html.escape(title)}</a></li>')
    sec = [f'<section class="ch" id="{cid}"><h2>{html.escape(title)}</h2><p class="intro">{intro}</p>']
    for (name, stitle, lines, _cap) in scenes:
        n += 1
        shutil.copyfile(os.path.join(here, 'man2', name + '.png'), os.path.join(img_dir, name + '.png'))
        r = hl.get(name)
        box = ''
        if r and not (r['w'] >= W - 2 and r['h'] >= H - 2):
            box = f'<span class="hl" style="left:{r["x"]/W*100:.2f}%;top:{r["y"]/H*100:.2f}%;width:{r["w"]/W*100:.2f}%;height:{r["h"]/H*100:.2f}%"></span>'
        lis = ''.join(f'<li>{l}</li>' for l in lines)
        sec.append(f'''<figure class="scene" id="s-{name}">
  <figcaption><span class="no">{n}</span>{html.escape(stitle)}</figcaption>
  <div class="shot"><img src="img/{name}.png" alt="{html.escape(stitle)} 화면" loading="lazy">{box}</div>
  <ul class="how">{lis}</ul>
</figure>''')
    sec.append('</section>')
    body.append('\n'.join(sec))
keys = ''.join(f'<h3>{html.escape(t)}</h3><table class="keys">' + ''.join(f'<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>' for k, v in rows) + '</table>' for t, rows in KEYS)
page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>업무 내비게이터 사용 설명서</title>
<style>
:root {{ --accent:#2563eb; --text:#1e2d47; --muted:#64748b; --line:#e2e8f0; --bg:#f6f8fb; --white:#fff; --hl:#f59e0b; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family:'Pretendard','Malgun Gothic',-apple-system,sans-serif; color:var(--text); background:var(--bg); line-height:1.65; }}
.wrap {{ display:grid; grid-template-columns:260px 1fr; max-width:1280px; margin:0 auto; }}
nav {{ position:sticky; top:0; align-self:start; height:100vh; overflow:auto; padding:28px 18px; border-right:1px solid var(--line); background:var(--white); }}
nav h1 {{ font-size:1.05rem; margin:0 0 4px; }} nav .ver {{ font-size:.78rem; color:var(--muted); margin-bottom:18px; }}
nav ul {{ list-style:none; padding-left:0; margin:0; font-size:.88rem; }} nav li {{ margin:6px 0; }} nav a {{ color:var(--text); text-decoration:none; }} nav a:hover {{ color:var(--accent); }}
main {{ padding:36px 44px 80px; min-width:0; }}
.cover {{ background:var(--white); border:1px solid var(--line); border-radius:14px; padding:28px 32px; margin-bottom:28px; }}
.cover h1 {{ margin:0 0 6px; font-size:1.6rem; }} .cover p {{ margin:6px 0; color:var(--muted); }}
.flow {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:14px; font-size:.82rem; }} .flow span {{ background:#eef4ff; color:var(--accent); border-radius:999px; padding:3px 10px; font-weight:600; }}
.ch {{ margin:44px 0; }} .ch h2 {{ font-size:1.3rem; border-left:4px solid var(--accent); padding-left:10px; margin:0 0 8px; }}
.intro {{ color:var(--muted); margin:0 0 18px; }}
.scene {{ margin:0 0 30px; background:var(--white); border:1px solid var(--line); border-radius:12px; overflow:hidden; }}
.scene figcaption {{ padding:12px 18px; font-weight:700; border-bottom:1px solid var(--line); }}
.no {{ display:inline-flex; align-items:center; justify-content:center; min-width:24px; height:24px; margin-right:8px; border-radius:6px; background:var(--accent); color:#fff; font-size:.75rem; }}
.shot {{ position:relative; line-height:0; background:#0f172a; }} .shot img {{ width:100%; height:auto; display:block; }}
.hl {{ position:absolute; border:3px solid var(--hl); border-radius:8px; box-shadow:0 0 0 4px rgba(245,158,11,.25); pointer-events:none; }}
.how {{ margin:0; padding:14px 22px 16px 38px; font-size:.92rem; }} .how li {{ margin:4px 0; }}
kbd {{ display:inline-block; padding:0 6px; border:1px solid #cbd5e1; border-bottom-width:2px; border-radius:5px; background:#f8fafc; font-family:inherit; font-size:.8rem; line-height:1.5; }}
.keys {{ border-collapse:collapse; width:100%; background:var(--white); margin:6px 0 18px; font-size:.9rem; }}
.keys th, .keys td {{ border:1px solid var(--line); padding:7px 12px; text-align:left; vertical-align:top; }} .keys th {{ width:38%; background:#f8fafc; font-weight:600; }}
@media (max-width:900px) {{ .wrap {{ grid-template-columns:1fr; }} nav {{ position:static; height:auto; border-right:none; border-bottom:1px solid var(--line); }} main {{ padding:20px 16px 60px; }} }}
@media print {{ nav {{ display:none; }} .wrap {{ display:block; }} .scene {{ break-inside:avoid; }} body {{ background:#fff; }} }}
</style></head><body><div class="wrap">
<nav><h1>업무 내비게이터</h1><div class="ver">사용 설명서 · v1.4.0</div><ul>{''.join(toc)}<li><a href="#keys">부록 · 마우스와 단축키</a></li></ul></nav>
<main>
<div class="cover"><h1>업무 내비게이터 사용 설명서</h1>
<p>예시 업무(징계처분 · 물품 구매 계약 · 감찰조사)로, 업무를 만들고 → 일하고 → 나누어 맡기고 → 공유하고 → 레퍼런스로 남기고 → 보관하는 흐름 순서로 설명합니다.</p>
<p>사진의 <b style="color:#d97706">주황 테두리</b>가 그 단계에서 누르거나 볼 곳입니다. (AI 기능은 이 설명서에서 다루지 않습니다.)</p>
<div class="flow"><span>마감 임박 알림</span><span>새 업무 만들기</span><span>일하기</span><span>체크리스트 편집</span><span>일정</span><span>업무 분담·회신 대기</span><span>공유</span><span>처리완료</span><span>레퍼런스</span><span>보관</span><span>조직 자료</span><span>백업</span></div></div>
{''.join(body)}
<section class="ch" id="keys"><h2>부록 · 마우스와 단축키</h2>{keys}</section>
</main></div></body></html>'''
open(os.path.join(out_dir, '업무내비게이터_사용설명서.html'), 'w', encoding='utf-8').write(page)
print('scenes', n)
