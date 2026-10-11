import sys, os, re
# 사용: python tools/sync.py [저장소 폴더]  (생략하면 tools의 상위 폴더)
os.chdir(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
t = open('index.html', encoding='utf-8').read()
big = max(re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', t, re.S), key=len)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.js'), 'w', encoding='utf-8').write(big)
pairs = [('    <title>업무 내비게이터</title>', '    <title>업무 내비게이터 [TEST - 관리자 전용]</title>'),
('''                <!-- 사내 보안정책 잠금 안내: 외부 AI·법제처 API 입력 UI를 대체 -->
                <div id="aiPolicyLock" style="text-align:center;padding:22px 10px 8px;">''', '''                <!-- [TEST 전용 사본] 사내 보안정책 잠금 안내 - 테스트 파일에서는 비노출 -->
                <div id="aiPolicyLock" style="display:none;text-align:center;padding:22px 10px 8px;">'''),
('''                <!-- 아래 입력 UI는 사내 AI 연동 시 관리자가 활성화하는 용도로 보존(화면 비노출) -->
                <div style="display:none;">''', '''                <!-- [TEST 전용 사본] 관리자 테스트용으로 잠금 해제됨(display:none 제거) -->
                <div>''')]
for a, b in pairs:
    assert t.count(a) == 1, a[:40]
    t = t.replace(a, b)
open('ai_test .html', 'w', encoding='utf-8', newline='').write(t)
print('synced')
