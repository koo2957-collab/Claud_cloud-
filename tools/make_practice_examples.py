# 연습 업무 「배제사유 확인 · 각서 받기」의 업무팁 예시·사진 2장 — 가상 업체로 채운 작성례를 A4 문서 모양 그림(PNG)으로
#   ① 각서 작성례(가상 업체).png — 서식(각서(수의계약 배제사유).hwpx)과 같은 칸, 기입한 곳은 파란 글자
#   ② 배제사유 확인 결과(작성례).png — 담당자가 남기는 확인 메모 예시
# 헤드리스 크롬으로 HTML을 찍음(글꼴: 바탕). 실행: (tools 폴더에서) python make_practice_examples.py  → practice/
import os, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'practice')
CHROME = os.environ.get('CHROME_PATH') or ('C:/Program Files/Google/Chrome/Application/chrome.exe' if os.name == 'nt' else 'google-chrome')

CSS = '''*{box-sizing:border-box;margin:0}body{width:1240px;height:1754px;background:#e5e7eb;font-family:'Batang','바탕','HYSinMyeongJo',serif;color:#111}
.pg{position:absolute;left:70px;top:60px;width:1100px;height:1634px;background:#fff;box-shadow:0 6px 24px rgba(0,0,0,.18);padding:80px 90px}
.top{font-size:21px;border-bottom:4px solid #111;padding-bottom:8px;display:flex;justify-content:space-between}
.tag{font-family:'Malgun Gothic',sans-serif;font-size:20px;font-weight:700;color:#7c3aed;background:rgba(139,92,246,.12);border-radius:16px;padding:2px 16px}
.box{border:4px solid #111;border-top:none;padding:70px 56px;height:1330px}
h1{text-align:center;font-size:44px;letter-spacing:40px;font-weight:700;margin:20px 0 70px}
table{width:100%;border-collapse:collapse;font-size:26px}td{border:2px solid #111;padding:16px 18px;height:70px;word-break:keep-all}td.l{width:26%;text-align:center;font-weight:700}
.v{color:#1d4ed8;font-family:'Malgun Gothic',sans-serif;font-weight:600}p{font-size:26px;line-height:1.9;margin:0 0 26px}.c{text-align:center}.r{text-align:right}
.seal{display:inline-block;width:64px;height:64px;border:3px solid #dc2626;border-radius:50%;color:#dc2626;font-size:22px;line-height:58px;text-align:center;transform:rotate(-8deg);margin-left:6px;font-family:'Malgun Gothic',sans-serif;font-weight:700}
.foot{font-family:'Malgun Gothic',sans-serif;font-size:19px;color:#475569;margin-top:16px;display:flex;justify-content:space-between}'''

def page(top, body, foot):
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="pg"><div class="top"><span>{top}</span><span class="tag">작성례 · 가상 업체</span></div><div class="box">{body}</div><div class="foot"><span>{foot}</span><span>업무 내비게이터 연습 업무</span></div></div>'

V = lambda t: f'<span class="v">{t}</span>'
GAK = page('[연습용 양식] 집행기준 제5장 [별지 제1호 서식] 각서',
    '<h1>각서</h1><table>'
    f'<tr><td class="l">업 체 명</td><td>{V("○○상사(가상)")}</td></tr><tr><td class="l">대 표 자</td><td>{V("김○○")}</td></tr>'
    f'<tr><td class="l">소 재 지</td><td>{V("부산광역시 ○○구 ○○로 00 (가상 주소)")}</td></tr><tr><td class="l">업종(등록)</td><td>{V("도매업 — 의료용품")}</td></tr></table>'
    '<p style="margin-top:70px">　상기 본인(법인)은 귀 기관과 수의계약을 체결함에 있어서 붙임 배제사유 중 어느 사유에도 해당되지 않으며, '
    '차후에 이러한 사실이 발견된 경우 계약의 해제·해지 및 부정당업자 제재 처분을 받아도 이의를 제기하지 않겠습니다.</p>'
    '<p>　붙임　수의계약 배제사유 1부.</p>'
    f'<p class="c" style="margin-top:90px">{V("2026.　10.　20.")}</p>'
    f'<p class="r" style="margin-top:50px">업체명 : {V("○○상사(가상)")}　　　<br>대표자 : {V("김○○")}　<span class="seal">인</span></p>'
    '<p style="margin-top:60px;font-weight:700">　재무관 또는 분임재무관 귀하</p>',
    '파란 글자 = 업체가 적는 곳 · 연습용 가상 자료')

ROWS = [('부도·파산·해산·영업정지 등', '업체 서류'), ('입찰참가자격 제한 기간 중', '나라장터 조회'),
        ('최근 3개월 안 계약 포기·해지', '계약 대장'), ('그 밖의 [별표 1] 배제사유', '각서 받음')]
CHK = page('[작성례] 배제사유 확인 결과 (담당자 메모)',
    '<h1 style="letter-spacing:6px">배제사유 확인 결과</h1>'
    f'<p>　업　체 : {V("○○상사(가상)")}<br>　품　목 : {V("구급 소모품(일회용 장갑·마스크)")}<br>　금　액 : {V("15,000,000원 (1인 견적 수의계약)")}</p>'
    '<table style="margin-top:30px"><tr><td class="l" style="width:42%">확인 사항</td><td class="l" style="width:17%">결과</td><td class="l" style="width:14%">확인일</td><td class="l" style="width:27%">확인 방법</td></tr>'
    + ''.join(f'<tr style="font-size:24px"><td>{a}</td><td class="c" style="white-space:nowrap">{V("해당 없음")}</td><td class="c" style="white-space:nowrap">{V("10. 20.")}</td><td class="c">{V(b)}</td></tr>' for a, b in ROWS) +
    '</table><p style="margin-top:50px;font-size:23px;color:#374151">　※ 확인에 시간이 걸리면 각서를 받고 먼저 계약할 수 있습니다(집행기준 제5장).</p>'
    f'<p class="r" style="margin-top:110px">확인자 : {V("○○팀 주무관 ○○○")}</p>',
    '파란 글자 = 담당자가 적는 곳 · 연습용 가상 자료')

for name, html in [('각서 작성례(가상 업체).png', GAK), ('배제사유 확인 결과(작성례).png', CHK)]:
    with tempfile.TemporaryDirectory() as td:
        h = os.path.join(td, 'p.html'); open(h, 'w', encoding='utf-8').write(html)
        out = os.path.join(OUT, name)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={os.path.join(td, "prof")}',
                        '--window-size=1240,1754', f'--screenshot={out}', 'file:///' + h.replace('\\', '/')], capture_output=True, timeout=60)
        print(name, os.path.getsize(out) // 1024, 'KB')
