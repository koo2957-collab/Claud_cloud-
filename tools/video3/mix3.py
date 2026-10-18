# 마지막 합치기: 녹화 영상(raw) + 내레이션(장면 시각에 맞춰) + 배경음악 → 영상작업/업무내비게이터_시연영상.mp4
# H.264(CRF) 1920×1080 30fps · AAC 160k · 소리 크기 맞춤(loudnorm -15 LUFS)
# 실행: python tools/video3/mix3.py
import json, os, subprocess, sys, glob
import imageio_ffmpeg
here = os.path.dirname(os.path.abspath(__file__))
work = os.path.join(here, '..', '..', '영상작업')
FF = imageio_ffmpeg.get_ffmpeg_exe()
mk = json.load(open(os.path.join(work, 'marks.json'), encoding='utf-8'))
raw = [p for p in glob.glob(os.path.join(work, 'raw.*'))][0]
out = os.path.join(work, '업무내비게이터_시연영상.mp4')
total = mk['total'] + 0.3
args = [FF, '-y', '-hide_banner', '-i', raw, '-i', os.path.join(work, 'bgm.wav')]
for m in mk['marks']: args += ['-i', os.path.join(work, 'tts', m['id'] + '.mp3')]
fl = []
for k, m in enumerate(mk['marks']):
    d = int(round(m['voiceAt'] * 1000))
    fl.append(f"[{k + 2}:a]aresample=48000,adelay={d}|{d},volume=1.0[v{k}]")
n = len(mk['marks'])
fl.append(''.join(f'[v{k}]' for k in range(n)) + f'amix=inputs={n}:normalize=0[nar]')
fl.append('[1:a]volume=0.40[bg]')
fl.append('[nar][bg]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[a]')
fl.append('[0:v]fps=30,scale=1920:1080:flags=lanczos,format=yuv420p[v]')
args += ['-filter_complex', ';'.join(fl), '-map', '[v]', '-map', '[a]', '-t', f'{total:.2f}',
         '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
r = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='ignore')
if r.returncode: print(r.stderr[-2500:]); sys.exit(1)
print('저장', out, round(os.path.getsize(out) / 1e6, 1), 'MB')
