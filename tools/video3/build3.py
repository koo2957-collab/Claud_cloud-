# 녹화 준비: 대본(script.py) + 음성 길이·문장 시각(tts.json) → 영상작업/seg.json, 설명서 예시 자료(mkman2 00_seed) → 영상작업/seed.js
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here); sys.path.insert(0, os.path.join(here, '..'))
from script import SEG
work = os.path.join(here, '..', '..', '영상작업')
tts = {t['id']: t for t in json.load(open(os.path.join(work, 'tts', 'tts.json'), encoding='utf-8'))}
out = []
for s in SEG:
    t = tts[s['id']]
    if t.get('text') and t['text'] != s['voice']: raise SystemExit('음성이 대본과 다름: ' + s['id'] + ' — tts.py를 다시 실행')
    out.append(dict(s, dur=t['dur'], sents=t['sents']))
json.dump(out, open(os.path.join(work, 'seg.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
cwd = os.getcwd(); os.chdir(os.path.join(here, '..'))
import mkman2   # steps.json도 새로 쓰지만 해 없음
os.chdir(cwd)
open(os.path.join(work, 'seed.js'), 'w', encoding='utf-8').write(mkman2.S[0]['js'])
print('seg', len(out), '· 음성 합계', round(sum(x['dur'] for x in out), 1), '초')
