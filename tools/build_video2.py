# 광고형 시연 영상 페이지 만들기: 1920x1080 캔버스 + 내레이션(TTS wav) + 합성 배경음악 → MediaRecorder
import json, os, re, sys, base64, wave
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from video_script import SEG
short = len(sys.argv) > 1 and sys.argv[1] == 'short'
hl = {}
for line in open(os.path.join(here, 'man2_out.txt'), encoding='utf-8'):
    m = re.match(r'> (\S+) => "(.*)"\s*$', line)
    if m:
        try: hl[m.group(1)] = json.loads(json.loads('"' + m.group(2) + '"')).get('hl')
        except Exception: pass
PAD = {'hook': 1.5, 'title': 1.6, 'scene': 1.1, 'effect': 1.5, 'end': 3.2}
LEAD = {'hook': 0.5, 'title': 0.7, 'scene': 0.45, 'effect': 0.5, 'end': 0.8}
tl, imgs, voices = [], {}, []
segs = SEG[:4] + SEG[4:6] if short else SEG
for i, s in enumerate(segs):
    idx = SEG.index(s)
    w = wave.open(os.path.join(here, 'tts', '%02d.wav' % idx)); vd = w.getnframes() / w.getframerate(); w.close()
    d = dict(s); d['vlead'] = LEAD[s['kind']]; d['dur'] = round(LEAD[s['kind']] + vd + PAD[s['kind']], 2); d['v'] = len(voices)
    voices.append('data:audio/wav;base64,' + base64.b64encode(open(os.path.join(here, 'tts', '%02d.wav' % idx), 'rb').read()).decode())
    if s['kind'] == 'scene':
        r = hl.get(s['img'])
        if r and (r['w'] >= 1430 and r['h'] >= 800): r = None
        r = {'01_main': {'x': 62, 'y': 165, 'w': 220, 'h': 245}, '26_sidebar': {'x': 62, 'y': 208, 'w': 220, 'h': 345}}.get(s['img'], r)
        d['hl'] = r
        if s['img'] not in imgs:
            imgs[s['img']] = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(here, 'man2', s['img'] + '.png'), 'rb').read()).decode()
    tl.append(d)
total = round(sum(x['dur'] for x in tl) + 0.6, 2)
page = r'''<!doctype html><html><head><meta charset="utf-8"><title>video</title>
<style>html,body{margin:0;background:#000;}canvas{display:block;}</style></head><body>
<canvas id="c" width="1920" height="1080"></canvas>
<script>
const TL = ''' + json.dumps(tl, ensure_ascii=False) + r''';
const IM = ''' + json.dumps(imgs) + r''';
const VO = ''' + json.dumps(voices) + r''';
const TOTAL = ''' + str(total) + r''';
const W = 1920, H = 1080, K = 4 / 3, FPS = 30;
const c = document.getElementById('c'), g = c.getContext('2d');
const FONT = "'Malgun Gothic','Pretendard',sans-serif";
const imgs = {};
const ease = t => t <= 0 ? 0 : t >= 1 ? 1 : t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
let start = 0; for (const s of TL) { s.t0 = start; start += s.dur; }
function rr(x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
// 검은 배경 큰 글씨 (줄마다 조금씩 늦게 떠오름)
function bigText(s, t, opt) {
  g.fillStyle = opt.bg; g.fillRect(0, 0, W, H);
  const lines = s.text.split('\n'), lh = opt.size * 1.32, y0 = H / 2 - (lines.length - 1) * lh / 2 - (s.sub ? 28 : 0);
  g.textAlign = 'center'; g.textBaseline = 'middle';
  lines.forEach((ln, i) => {
    const p = ease(clamp((t - 0.15 - i * 0.35) / 0.9, 0, 1));
    g.globalAlpha = p; g.font = `700 ${opt.size}px ${FONT}`;
    if (opt.grad) { const w = g.measureText(ln).width; const gr = g.createLinearGradient(W / 2 - w / 2, 0, W / 2 + w / 2, 0); gr.addColorStop(0, '#60a5fa'); gr.addColorStop(1, '#c084fc'); g.fillStyle = gr; } else g.fillStyle = '#f8fafc';
    g.fillText(ln, W / 2, y0 + i * lh + (1 - p) * 26);
  });
  if (s.sub) { const p = ease(clamp((t - 0.9) / 0.8, 0, 1)); g.globalAlpha = p * 0.75; g.font = `500 30px ${FONT}`; g.fillStyle = '#94a3b8'; g.fillText(s.sub, W / 2, y0 + (lines.length - 1) * lh + 104); }
  g.globalAlpha = 1; g.textAlign = 'left'; g.textBaseline = 'alphabetic';
}
function titleCard(s, t) {
  const gr = g.createLinearGradient(0, 0, W, H); gr.addColorStop(0, '#1e3a8a'); gr.addColorStop(0.55, '#111c3d'); gr.addColorStop(1, '#0b1020');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  // 은은한 빛
  const rg = g.createRadialGradient(W * 0.5, H * 0.42, 10, W * 0.5, H * 0.42, 700); rg.addColorStop(0, 'rgba(96,165,250,0.22)'); rg.addColorStop(1, 'rgba(96,165,250,0)'); g.fillStyle = rg; g.fillRect(0, 0, W, H);
  g.textAlign = 'center'; g.textBaseline = 'middle';
  const p = ease(clamp((t - 0.1) / 1.0, 0, 1));
  g.globalAlpha = p * 0.8; g.font = `600 30px ${FONT}`; g.fillStyle = '#93c5fd'; g.fillText('소방청 프로그램 시연회', W / 2, H / 2 - 150);
  g.globalAlpha = p; g.font = `800 ${Math.round(118 + 6 * p)}px ${FONT}`; g.fillStyle = '#fff'; g.fillText('✦ ' + s.text, W / 2, H / 2 - 30);
  const p2 = ease(clamp((t - 0.8) / 0.9, 0, 1));
  g.globalAlpha = p2 * 0.9; g.font = `500 40px ${FONT}`; g.fillStyle = '#e2e8f0'; g.fillText(s.sub, W / 2, H / 2 + 90);
  g.globalAlpha = 1; g.textAlign = 'left'; g.textBaseline = 'alphabetic';
}
function view(s) {
  // 강조 영역으로 다가가는 확대 (CSS 1440 기준 → 화면 1920)
  const r = s.hl;
  if (!r) return { z: 1.05, cx: W / 2, cy: H / 2 };
  const x = r.x * K, y = r.y * K, w = r.w * K, h = r.h * K;
  const z = clamp(Math.min(0.78 * W / w, 0.72 * H / h), 1.06, 1.55);
  const cx = clamp(x + w / 2, W / (2 * z), W - W / (2 * z)), cy = clamp(y + h / 2 + 40 / z, H / (2 * z), H - H / (2 * z));
  return { z, cx, cy };
}
function sceneDraw(s, t) {
  g.fillStyle = '#0b1020'; g.fillRect(0, 0, W, H);
  const v = view(s), p = ease(clamp((t - 0.25) / 1.6, 0, 1)), drift = 1 + 0.018 * clamp(t / s.dur, 0, 1);
  const z = (1 + (v.z - 1) * p) * drift, cx = W / 2 + (v.cx - W / 2) * p, cy = H / 2 + (v.cy - H / 2) * p;
  g.save(); g.translate(W / 2, H / 2); g.scale(z, z); g.translate(-cx, -cy);
  g.drawImage(imgs[s.img], 0, 0, W, H);
  let hx = W / 2, hy = H / 2, hb = 0;
  if (s.hl) {
    const x = s.hl.x * K, y = s.hl.y * K, w = s.hl.w * K, h = s.hl.h * K; hx = x + Math.min(w * 0.5, 160); hy = y + Math.min(h * 0.5, 54); hb = (y + h - cy) * z + H / 2;
    const q = ease(clamp((t - 1.5) / 0.5, 0, 1)), pulse = 0.5 + 0.5 * Math.sin(t * 4.2);
    g.globalAlpha = q; g.lineWidth = 5 / z; g.strokeStyle = '#f59e0b'; rr(x - 6, y - 6, w + 12, h + 12, 12); g.stroke();
    g.globalAlpha = q * (0.2 + 0.25 * pulse); g.lineWidth = 14 / z; g.strokeStyle = '#fbbf24'; rr(x - 12, y - 12, w + 24, h + 24, 16); g.stroke();
    g.globalAlpha = 1;
  }
  g.restore();
  // 마우스: 화면 좌표로 바꿔 그림 (오른쪽 아래에서 강조 위치로)
  if (s.hl) {
    const sx = (hx - cx) * z + W / 2, sy = (hy - cy) * z + H / 2;
    const m = ease(clamp((t - 0.6) / 1.1, 0, 1)), px = W * 0.86 + (sx - W * 0.86) * m, py = H * 0.8 + (sy - H * 0.8) * m;
    if (t > 1.7 && t < 2.4) { const k = (t - 1.7) / 0.7; g.globalAlpha = (1 - k) * 0.45; g.fillStyle = '#3b82f6'; g.beginPath(); g.arc(px, py, 10 + 34 * k, 0, 7); g.fill(); g.globalAlpha = 1; }
    g.fillStyle = '#111827'; g.strokeStyle = '#fff'; g.lineWidth = 2.5; const a = 1.25;
    g.beginPath(); g.moveTo(px, py); g.lineTo(px, py + 26 * a); g.lineTo(px + 7 * a, py + 20 * a); g.lineTo(px + 12 * a, py + 31 * a); g.lineTo(px + 17 * a, py + 29 * a); g.lineTo(px + 12 * a, py + 18 * a); g.lineTo(px + 20 * a, py + 18 * a); g.closePath(); g.fill(); g.stroke();
  }
  // 아래 가운데 자막 상자 (STEP 라벨 + 한 줄)
  const ap = ease(clamp((t - 0.3) / 0.6, 0, 1));
  g.font = `800 44px ${FONT}`; const cw = g.measureText(s.cap).width; g.font = `700 26px ${FONT}`; const lw = g.measureText(s.step).width;
  const bw = Math.max(cw, lw) + 96, bh = 136, bx = W / 2 - bw / 2, top = hb > H - bh - 70, by = (top ? 48 : H - bh - 48) + (1 - ap) * 20 * (top ? -1 : 1);
  g.globalAlpha = ap * 0.86; g.fillStyle = '#0b1222'; rr(bx, by, bw, bh, 26); g.fill();
  g.globalAlpha = ap; g.textAlign = 'center';
  g.fillStyle = '#60a5fa'; g.font = `700 26px ${FONT}`; g.fillText(s.step, W / 2, by + 46);
  g.fillStyle = '#fff'; g.font = `800 44px ${FONT}`; g.fillText(s.cap, W / 2, by + 104);
  g.textAlign = 'left'; g.globalAlpha = 1;
}
function draw(s, t) {
  if (s.kind === 'scene') sceneDraw(s, t);
  else if (s.kind === 'title' || s.kind === 'end') titleCard(s, t);
  else bigText(s, t, s.kind === 'effect' ? { bg: '#000', size: 84, grad: true } : { bg: '#05070d', size: 78 });
}
// ── 소리: 내레이션 + 합성 배경음악 (96 BPM, 은은한 패드·베이스·아르페지오·하이햇)
let ac, dest, master, bgm, vbus;
const N = n => 440 * Math.pow(2, (n - 69) / 12);
const CH = [[48, 52, 55, 59, 62], [45, 48, 52, 55, 60], [41, 45, 48, 52, 57], [43, 47, 50, 55, 59]]; // Cmaj9 · Am7 · Fmaj7 · G
const BEAT = 60 / 96, BAR = BEAT * 4;
let noise;
function tone(type, f, t, dur, peak, att, rel, out, cut) {
  const o = ac.createOscillator(), e = ac.createGain(); o.type = type; o.frequency.value = f;
  e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(peak, t + att); e.gain.setValueAtTime(peak, t + Math.max(att, dur - rel)); e.gain.linearRampToValueAtTime(0, t + dur);
  if (cut) { const lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = cut; o.connect(lp); lp.connect(e); } else o.connect(e);
  e.connect(out); o.start(t); o.stop(t + dur + 0.05);
}
function hat(t, v) { const s = ac.createBufferSource(); s.buffer = noise; const hp = ac.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 7500; const e = ac.createGain(); e.gain.setValueAtTime(v, t); e.gain.exponentialRampToValueAtTime(0.0008, t + 0.07); s.connect(hp); hp.connect(e); e.connect(bgm); s.start(t); s.stop(t + 0.1); }
function kick(t, v) { const o = ac.createOscillator(), e = ac.createGain(); o.frequency.setValueAtTime(110, t); o.frequency.exponentialRampToValueAtTime(42, t + 0.18); e.gain.setValueAtTime(v, t); e.gain.exponentialRampToValueAtTime(0.001, t + 0.32); o.connect(e); e.connect(bgm); o.start(t); o.stop(t + 0.35); }
let nextBar = 0, barNo = 0, base = 0;
function scheduleMusic(until) {
  while (base + nextBar < until) {
    const t = base + nextBar, ch = CH[barNo % 4], full = barNo >= 2;
    ch.forEach(n => { tone('triangle', N(n), t, BAR + 0.4, 0.035, 0.5, 0.7, bgm, 1600); tone('sine', N(n) * 1.003, t, BAR + 0.4, 0.03, 0.6, 0.7, bgm); });
    tone('sine', N(ch[0] - 12), t, BEAT * 1.8, 0.16, 0.02, 0.4, bgm); tone('sine', N(ch[0] - 12), t + BEAT * 2, BEAT * 1.8, 0.13, 0.02, 0.4, bgm);
    if (full) {
      const arp = [ch[0] + 12, ch[2] + 12, ch[3] + 12, ch[4] + 12, ch[3] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 12];
      arp.forEach((n, k) => tone('sine', N(n), t + k * BEAT / 2, BEAT * 0.45, 0.026, 0.005, 0.25, bgm));
      for (let k = 0; k < 4; k++) hat(t + k * BEAT + BEAT / 2, 0.05);
      kick(t, 0.22); kick(t + BEAT * 2, 0.16);
    }
    nextBar += BAR; barNo++;
  }
}
async function setupAudio() {
  ac = new AudioContext({ sampleRate: 48000 }); dest = ac.createMediaStreamDestination();
  const comp = ac.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 3;
  master = ac.createGain(); master.gain.value = 0.95; master.connect(comp); comp.connect(dest);
  bgm = ac.createGain(); bgm.gain.value = 0; bgm.connect(master);
  vbus = ac.createGain(); vbus.gain.value = 1.0; vbus.connect(master);
  noise = ac.createBuffer(1, ac.sampleRate * 0.2, ac.sampleRate); const d = noise.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const bufs = await Promise.all(VO.map(async u => ac.decodeAudioData(await (await fetch(u)).arrayBuffer())));
  return bufs;
}
async function run() {
  await Promise.all(Object.entries(IM).map(([k, src]) => new Promise(res => { const i = new Image(); i.onload = () => { imgs[k] = i; res(); }; i.src = src; })));
  const bufs = await setupAudio();
  if (ac.state !== 'running') await ac.resume();
  const stream = c.captureStream(FPS); stream.addTrack(dest.stream.getAudioTracks()[0]);
  const cands = ['video/mp4;codecs=avc1.640028,mp4a.40.2', 'video/mp4', 'video/webm;codecs=vp9,opus'];
  const mime = cands.find(m => MediaRecorder.isTypeSupported(m)); window.__mime = mime;
  const rec = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 3500000, audioBitsPerSecond: 160000 });
  const chunks = []; rec.ondataavailable = e => e.data.size && chunks.push(e.data);
  draw(TL[0], 0);
  rec.start(1000);
  const t0 = ac.currentTime + 0.3; base = t0;
  // 배경음악: 처음 2.5초 동안 커지고, 목소리 나올 때 낮춤, 끝에서 줄어듦
  const BG = 0.38, DUCK = 0.1;
  bgm.gain.setValueAtTime(0, t0); bgm.gain.linearRampToValueAtTime(BG, t0 + 2.5);
  TL.forEach(s => {
    const vs = t0 + s.t0 + s.vlead, ve = vs + bufs[s.v].duration;
    const src = ac.createBufferSource(); src.buffer = bufs[s.v]; src.connect(vbus); src.start(vs);
    if (s.t0 > 0) { bgm.gain.setTargetAtTime(DUCK, vs - 0.35, 0.12); bgm.gain.setTargetAtTime(BG, ve + 0.15, 0.35); }
    else { bgm.gain.setTargetAtTime(DUCK, vs + 0.1, 0.4); bgm.gain.setTargetAtTime(BG, ve + 0.15, 0.35); }
  });
  bgm.gain.setTargetAtTime(0, t0 + TOTAL - 3.0, 0.8);
  await new Promise(done => {
    function frame() {
      const T = ac.currentTime - t0;
      scheduleMusic(ac.currentTime + 4);
      if (T >= TOTAL) { done(); return; }
      let i = 0; while (i < TL.length - 1 && TL[i].t0 + TL[i].dur <= T) i++;
      const s = TL[i], t = Math.max(0, T - s.t0);
      g.globalAlpha = 1;
      // 앞 장면과 0.5초 겹쳐 바뀜
      if (i > 0 && t < 0.5) { draw(TL[i - 1], TL[i - 1].dur); const oc = offc; const og = oc.getContext('2d'); og.drawImage(c, 0, 0); draw(s, t); g.globalAlpha = 1 - ease(t / 0.5); g.drawImage(oc, 0, 0); g.globalAlpha = 1; }
      else draw(s, t);
      if (T > TOTAL - 1.2) { g.globalAlpha = clamp((T - (TOTAL - 1.2)) / 1.2, 0, 1); g.fillStyle = '#000'; g.fillRect(0, 0, W, H); g.globalAlpha = 1; }
      window.__prog = Math.round(T / TOTAL * 100);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  });
  rec.stop();
  await new Promise(r => rec.onstop = r);
  const blob = new Blob(chunks, { type: mime.split(';')[0] });
  const fr = new FileReader();
  fr.onload = () => { window.__b64 = fr.result.split(',')[1]; window.__done = true; };
  fr.readAsDataURL(blob);
}
const offc = document.createElement('canvas'); offc.width = W; offc.height = H;
window.__total = TOTAL;
run().catch(e => { window.__err = String(e && e.stack || e); window.__done = true; });
</script></body></html>'''
open(os.path.join(here, 'video2.html'), 'w', encoding='utf-8').write(page)
print('segments', len(tl), 'seconds', total, 'MB', round(len(page) / 1e6, 1))
