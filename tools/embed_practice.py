# 사용설명서/연습업무.json(mk_practice_build.py로 만든 것)을 index.html 맨 끝 <script type="application/json" id="practicePkg">에 넣는다(있으면 바꿈)
# 실행: python tools/embed_practice.py  → 그다음 python tools/sync.py
import os, re, json
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8', newline='').read()
pkg = json.load(open(os.path.join(root, '사용설명서', '연습업무.json'), encoding='utf-8'))
body = json.dumps(pkg, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
tag = '<script type="application/json" id="practicePkg">' + body + '</script>\n'
s, n = re.subn(r'<script type="application/json" id="practicePkg">.*?</script>\n', lambda m: tag, s, flags=re.S)
if not n:
    i = s.rfind('</body>')
    s = s[:i] + '    <!-- 연습 업무 (새 업무 만들기 ▾ → 연습 업무 넣기) — tools/embed_practice.py가 넣음 -->\n    ' + tag + s[i:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('연습 업무 넣음', round(len(body) / 1024), 'KB')
