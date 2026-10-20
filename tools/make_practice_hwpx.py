# 연습 업무카드의 서식을 한글(HWPX)로 만든다 — 실제 한글 서식 파일(practice/_틀_별지13호_각서.hwpx)을 틀로 삼아
# 글꼴·글자 모양·쪽 설정은 그대로 두고 본문(section0.xml)만 새로 쓴다. 빈 칸 정보는 한글이 열 때 다시 계산함.
#   빈 양식(서식): 각서(수의계약 배제사유).hwpx · 수의계약 공개내역서.hwpx  → practice/
# 틀 파일: 「지방계약법 시행규칙」 [별지 제13호서식] 각서(보증금으로 낸 주식의 진위) — 연습 업무에는 내용을 쓰지 않고 모양만 씀
# 실행: (tools 폴더에서) python make_practice_hwpx.py
import os, re, sys, zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'practice')
TPL = os.path.join(OUT, '_틀_별지13호_각서.hwpx')
z = zipfile.ZipFile(TPL)
SEC = z.read('Contents/section0.xml').decode('utf-8')
HEAD = z.read('Contents/header.xml').decode('utf-8')

# 기입한 글자(작성례)용 파란 글자 모양 하나를 더함: charPr 2(본문 12pt)를 복사해 id·색만 바꿈
BLUE = 13
m = re.search(r'<hh:charPr id="2" .*?</hh:charPr>', HEAD, re.S)
cp = re.sub(r'id="2"', f'id="{BLUE}"', m.group(0), count=1)
cp = re.sub(r'textColor="#[0-9A-Fa-f]{6}"', 'textColor="#1D4ED8"', cp, count=1)
assert 'textColor="#1D4ED8"' in cp
HEAD = HEAD.replace('</hh:charProperties>', cp + '</hh:charProperties>', 1)
HEAD = re.sub(r'<hh:charProperties itemCnt="(\d+)"', lambda k: f'<hh:charProperties itemCnt="{int(k.group(1)) + 1}"', HEAD, count=1)

# 쪽 설정(secPr)이 든 첫 문단의 앞부분 — 틀 표가 시작되기 전까지
PRE = SEC[:SEC.index('<hp:tbl ')]
POST = '<hp:t/></hp:run></hp:p></hs:sec>'

PID = '2147483648'
def run(t, c=2): return f'<hp:run charPrIDRef="{c}"><hp:t>{escape(t)}</hp:t></hp:run>' if t else f'<hp:run charPrIDRef="{c}"/>'
def para(*runs, pp=0):
    """runs: 글자 또는 (글자, 글자모양 id). pp: 0 양쪽 · 2 가운데 · 3 오른쪽"""
    rs = ''.join(run(r) if isinstance(r, str) else run(*r) for r in runs) or run('')
    return f'<hp:p id="{PID}" paraPrIDRef="{pp}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">{rs}</hp:p>'
BL = para()

_tid = [1700000000]
def tc(col, row, w, h, paras, bf=2, cs=1, va='CENTER'):
    return (f'<hp:tc name="" header="0" hasMargin="1" protect="0" editable="0" dirty="0" borderFillIDRef="{bf}">'
            f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{va}" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">{paras}</hp:subList>'
            f'<hp:cellAddr colAddr="{col}" rowAddr="{row}"/><hp:cellSpan colSpan="{cs}" rowSpan="1"/><hp:cellSz width="{w}" height="{h}"/>'
            f'<hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>')
def tbl(rows, widths, h=2400):
    """rows: 줄마다 [(글자 또는 [runs…], 칸 수), …] — 칸 수를 늘리면 오른쪽 칸과 합침. 첫 칸은 굵게·가운데."""
    _tid[0] += 1
    trs = []
    hs = []
    for r, row in enumerate(rows):
        rh = h * 2 if any(isinstance(c, tuple) and len(c) > 2 for c in row) else h
        hs.append(rh)
        col, cells = 0, []
        for k, c in enumerate(row):
            txt, cs = (c[0], c[1]) if isinstance(c, tuple) else (c, 1)
            w = sum(widths[col:col + cs])
            label = k % 2 == 0 and cs == 1
            runs = txt if isinstance(txt, list) else [(txt, 6 if label else 2)] if txt else []
            cells.append(tc(col, r, w, rh, para(*runs, pp=2 if label else 0)))
            col += cs
        trs.append('<hp:tr>' + ''.join(cells) + '</hp:tr>')
    W = sum(widths)
    return (f'<hp:tbl id="{_tid[0]}" zOrder="1" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="0" '
            f'rowCnt="{len(rows)}" colCnt="{len(widths)}" cellSpacing="0" borderFillIDRef="2" noAdjust="0">'
            f'<hp:sz width="{W}" widthRelTo="ABSOLUTE" height="{sum(hs)}" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>'
            + ''.join(trs) + '</hp:tbl>')
def tpara(t): return f'<hp:p id="{PID}" paraPrIDRef="2" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="2">{t}<hp:t/></hp:run></hp:p>'

def frame(top, body, foot):
    """틀과 같은 모양: 위 칸(서식 번호) · 굵은 테두리 본문 · 아래 칸(크기 안내)"""
    W = 45061
    rows = [tc(0, 0, W, 1766, para((top, 5)), bf=3), tc(0, 1, W, 61913, ''.join(body), bf=5), tc(0, 2, W, 3686, ''.join(para((f, 3), pp=3) for f in foot), bf=4)]
    return (f'<hp:tbl id="1558659839" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="NONE" repeatHeader="1" rowCnt="3" colCnt="1" cellSpacing="0" borderFillIDRef="2" noAdjust="0">'
            f'<hp:sz width="{W}" widthRelTo="ABSOLUTE" height="67365" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            '<hp:outMargin left="141" right="141" top="141" bottom="141"/><hp:inMargin left="283" right="283" top="283" bottom="283"/>'
            + ''.join(f'<hp:tr>{r}</hp:tr>' for r in rows) + '</hp:tbl>')

def save(name, title, top, body, foot, prv):
    sec = PRE + frame(top, body, foot) + POST
    hpf = z.read('Contents/content.hpf').decode('utf-8')
    hpf = re.sub(r'<opf:title>.*?</opf:title>', f'<opf:title>{escape(title)}</opf:title>', hpf)
    hpf = re.sub(r'(<opf:meta name="lastsaveby" content="text">).*?(</opf:meta>)', r'\1업무 내비게이터\2', hpf)
    p = os.path.join(OUT, name)
    with zipfile.ZipFile(p, 'w') as o:
        for it in [i for i in z.infolist()]:
            if it.filename == 'Contents/section0.xml': data = sec.encode('utf-8')
            elif it.filename == 'Contents/header.xml': data = HEAD.encode('utf-8')
            elif it.filename == 'Contents/content.hpf': data = hpf.encode('utf-8')
            elif it.filename == 'Preview/PrvText.txt': data = prv.encode('utf-8')
            else: data = z.read(it.filename)
            zi = zipfile.ZipInfo(it.filename, it.date_time); zi.compress_type = it.compress_type   # 틀의 ZipInfo를 그대로 쓰면 틀 읽기가 깨짐
            o.writestr(zi, data)   # mimetype은 압축 없이 맨 앞(틀과 같은 순서·방식)
    return p

V = lambda t: (t, BLUE)   # 작성례에서 기입한 글자(파란색)
NOTE = '연습용 양식 — 실제 업무 전 최신 「지방자치단체 입찰 및 계약 집행기준」 서식을 확인하세요'

# ── 각서(수의계약 배제사유) — 집행기준 제5장 [별지 제1호 서식]의 항목 ──
def gakseo(f=None):
    f = f or {}
    g = lambda k: [V(f[k])] if k in f else ''
    body = [BL, BL, para(('각    서', 9), pp=2), BL, BL,
            tpara(tbl([['업 체 명', g('co')], ['대 표 자', g('ceo')], ['소 재 지', g('addr')], ['업종(등록)', g('biz')]], [10000, 32000])),
            BL, BL,
            para('   상기 본인(법인)은 귀 기관과 수의계약을 체결함에 있어서 붙임 배제사유 중 어느 사유에도 해당되지 않으며, '
                 '차후에 이러한 사실이 발견된 경우 계약의 해제·해지 및 부정당업자 제재 처분을 받아도 이의를 제기하지 않겠습니다.'),
            BL, para('   붙임  수의계약 배제사유 1부.'), BL, BL, BL,
            para(*( [V(f['date'])] if 'date' in f else ['20      .      .      .']), pp=2), BL, BL,
            para('업체명 : ', V(f['co']) if 'co' in f else '                    ', '          ', pp=3),
            para('대표자 : ', V(f['ceo']) if 'ceo' in f else '                    ', '   (인)   ', pp=3),
            BL, BL, BL, para(('   재무관 또는 분임재무관 귀하', 6)), BL, BL]
    return body

save('각서(수의계약 배제사유).hwpx', '각서(수의계약 배제사유)', '[연습용 양식] 집행기준 제5장 [별지 제1호 서식] 각서', gakseo(),
     [NOTE, '210㎜×297㎜'], '각서(수의계약 배제사유)\r\n연습용 빈 양식')

# ── 수의계약 공개내역서 — 집행기준 제5장 제8절의 공개 항목 ──
def gonggae():
    # 칸 합치기는 한글에서 표가 깨져서 쓰지 않음 — 이름 | 적는 칸 두 칸짜리 표(각서와 같은 모양)
    rows = [[t, [('※ 관련 법령 근거와 구체적인 사유를 적음', 3)] if t == '수의계약 사유' else '']
            for t in ['사 업 명', '계약 개요', '계약일자', '계약기간', '예정가격(A)', '계약금액(B)', '계약률(B/A)',
                      '업 체 명', '대 표 자', '업체 주소', '수의계약 사유', '사업 장소', '기    타']]
    return [BL, para(('수의계약 공개내역서', 9), pp=2), BL, tpara(tbl(rows, [11000, 31000])), BL]

save('수의계약 공개내역서.hwpx', '수의계약 공개내역서', '[연습용 양식] 집행기준 제5장 제8절 수의계약 공개', gonggae(),
     [NOTE, '210㎜×297㎜'], '수의계약 공개내역서\r\n연습용 빈 양식')

print('practice/ 에 HWPX 빈 양식 2개')
# 작성례 그림(업무팁 「예시·사진」)은 make_practice_examples.py가 만든다(같은 각서 모양을 A4 그림으로)
