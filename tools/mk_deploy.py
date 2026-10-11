# 배포용 압축 파일 만들기: 배포/업무내비게이터_v{버전}.zip (영상 제외)
# 안: 업무내비게이터.html(= index.html, AI 설정 차단판) · 읽어보기.txt · 사용설명서/(설명서 html·img·연습업무.json)
# 실행: python tools/mk_deploy.py   (저장소 맨 위 폴더에서)
import zipfile, os, re
ver = re.search(r"const APP_VERSION = '([^']+)'", open('index.html', encoding='utf-8').read()).group(1)
root = f'업무내비게이터_v{ver}'
os.makedirs('배포', exist_ok=True)
readme = f"""업무 내비게이터 v{ver} — 처음 쓰는 방법

1. 이 압축 파일을 내 PC의 정해 둔 폴더(예: 문서 > 업무내비게이터)에 풉니다.
   - 압축을 푼 뒤 「업무내비게이터.html」을 두 번 눌러 엽니다(크롬 또는 엣지).
   - 압축 파일 안에서 바로 열지 마세요. 입력한 자료가 남지 않을 수 있습니다.

2. 처음이라면 [새 업무 만들기 ▾] → 「연습 업무 넣기」를 눌러 연습 업무로 따라 해 보세요.
   (사용설명서 10장 「연습 업무로 따라 해 보기」)

3. 사용설명서: 사용설명서 폴더의 「업무내비게이터_사용설명서.html」을 엽니다.
   img 폴더는 설명서 그림이니 함께 두어야 합니다.

알아 둘 것
- 설치·서버가 없고, 인터넷 없이 내 PC 브라우저 안에만 저장됩니다(외부 통신 차단).
- 자료는 「쓰던 브라우저」에 저장됩니다. 브라우저의 인터넷 사용 기록·사이트 데이터를 지우면
  자료가 지워질 수 있으니 [설정] → 백업 및 복원으로 가끔 백업 파일을 저장해 두세요.
- 새 판이 나오면 같은 폴더의 「업무내비게이터.html」을 새 파일로 바꾸면 됩니다(바꾸기 전에 백업 권장).
- 「사용설명서/연습업무.json」은 [업무 가져오기]로 연습 업무를 넣는 파일입니다
  (같은 내용이 프로그램 안 「연습 업무 넣기」에도 들어 있습니다).
"""
out = os.path.join('배포', root + '.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.write('index.html', f'{root}/업무내비게이터.html')
    z.writestr(f'{root}/읽어보기.txt', readme.replace('\n', '\r\n').encode('utf-8-sig'))
    for d, _, fs in os.walk('사용설명서'):
        for f in sorted(fs):
            if f.endswith('.mp4'): continue   # 영상은 따로
            p = os.path.join(d, f)
            z.write(p, f'{root}/' + p.replace(os.sep, '/'))
print(out, round(os.path.getsize(out) / 1e6, 1), 'MB')
with zipfile.ZipFile(out) as z:
    n = z.namelist()
    print(len(n), '개 파일')
    for x in n:
        if '/img/' not in x: print(' ', x)
    print('  (설명서 그림', sum('/img/' in x for x in n), '개)')
