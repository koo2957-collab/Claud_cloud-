# 내레이션 만들기: Microsoft 신경망 음성(edge-tts) → 영상작업/tts/{id}.mp3 + 문장 시각 tts.json
# 실행: python tools/video3/tts.py   (pip install edge-tts imageio-ffmpeg, 인터넷 필요)
import asyncio, json, os, sys, subprocess, re
import edge_tts, imageio_ffmpeg
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from script import SEG, VOICE, RATE
out = os.path.join(here, '..', '..', '영상작업', 'tts')
os.makedirs(out, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()

def dur(p):
    e = subprocess.run([FF, '-i', p], capture_output=True, text=True, encoding='utf-8', errors='ignore').stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', e).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

async def one(s):
    p = os.path.join(out, s['id'] + '.mp3')
    sents = []
    with open(p, 'wb') as f:
        async for ch in edge_tts.Communicate(s['voice'], VOICE, rate=RATE).stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] in ('SentenceBoundary', 'WordBoundary'):
                sents.append(dict(t=ch['offset'] / 1e7, d=ch['duration'] / 1e7, text=ch['text']))
    return dict(id=s['id'], dur=round(dur(p), 3), sents=sents)

async def main():
    res = [await one(s) for s in SEG]
    json.dump(res, open(os.path.join(out, 'tts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for r in res: print(r['id'], r['dur'], len(r['sents']))
    print('합계', round(sum(r['dur'] for r in res), 1), '초')
asyncio.run(main())
