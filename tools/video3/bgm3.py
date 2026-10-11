# 배경음악 만들기: 녹화한 장면 시각(marks.json)에 맞춰 합성 → 영상작업/bgm.wav
# 흐름: 문제(어둡고 잔잔) → 제목(쿵 + 반짝) → 시연(밝은 박자) → 3.5초 끌어올림 → 클라이맥스(안전, 조 올림·꽉 찬 소리) → 마무리(여운)
# 내레이션이 나오는 동안은 음악을 낮춤(덕킹). 크롬 OfflineAudioContext로 실제 시간보다 빠르게 만듦
# 실행: python tools/video3/bgm3.py [marks.json 경로]
import json, os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__))
work = os.path.join(here, '..', '..', '영상작업')
mk = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(work, 'marks.json'), encoding='utf-8'))
seg = {s['id']: s for s in json.load(open(os.path.join(work, 'seg.json'), encoding='utf-8'))}
M = {m['id']: m for m in mk['marks']}
cfg = dict(total=round(mk['total'] + 0.3, 3), title=M['title']['t0'], demo=M['d1']['t0'], climax=M['s1']['t0'], outro=M['e1']['t0'], end=M['end']['t0'],
           voice=[[m['voiceAt'], m['voiceAt'] + seg[m['id']]['dur'], 1 if m['kind'] == 'card' else 0] for m in mk['marks']])
page = r'''<!doctype html><meta charset="utf-8"><script>
const C = ''' + json.dumps(cfg) + r''';
(async () => { try {
const SR = 48000, ac = new OfflineAudioContext(2, Math.ceil(C.total * SR), SR);
const N = m => 440 * Math.pow(2, (m - 69) / 12);
// 마스터: 컴프레서 → 출력, 리버브 보냄
const comp = ac.createDynamicsCompressor(); comp.threshold.value = -16; comp.ratio.value = 3; comp.attack.value = 0.01; comp.release.value = 0.25; comp.connect(ac.destination);
const master = ac.createGain(); master.gain.value = 0.9; master.connect(comp);
const duck = ac.createGain(); duck.connect(master);           // 내레이션 덕킹
const bus = ac.createGain(); bus.connect(duck);               // 모든 악기
const rv = ac.createConvolver(); { const len = SR * 2.8, b = ac.createBuffer(2, len, SR); for (let c = 0; c < 2; c++) { const d = b.getChannelData(c); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.6); } rv.buffer = b; }
const rvg = ac.createGain(); rvg.gain.value = 0.32; rv.connect(rvg); rvg.connect(duck);
const noiseBuf = (() => { const b = ac.createBuffer(1, SR * 2, SR), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; return b; })();
function env(g, t, v, a, d, r) { g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + a); g.gain.setValueAtTime(v, t + a + d); g.gain.exponentialRampToValueAtTime(0.0001, t + a + d + r); }
function osc(type, f, t, dur, v, a, r, o = {}) {
  const x = ac.createOscillator(); x.type = type; x.frequency.value = f; if (o.det) x.detune.value = o.det;
  const g = ac.createGain(); env(g, t, v, a, Math.max(0, dur - a), r);
  let n = x; if (o.lp) { const f2 = ac.createBiquadFilter(); f2.type = 'lowpass'; f2.frequency.value = o.lp; f2.Q.value = o.q || 0.7; x.connect(f2); n = f2; }
  n.connect(g); g.connect(o.to || bus); if (o.rv) { const s = ac.createGain(); s.gain.value = o.rv; g.connect(s); s.connect(rv); }
  if (o.pan !== undefined) { /* 간단히 생략 */ }
  x.start(t); x.stop(t + dur + r + 0.05);
}
function noise(t, dur, v, type, f, q, a = 0.002, r = 0.08, to = bus) { const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const fl = ac.createBiquadFilter(); fl.type = type; fl.frequency.value = f; fl.Q.value = q || 0.7; const g = ac.createGain(); env(g, t, v, a, Math.max(0, dur - a), r); s.connect(fl); fl.connect(g); g.connect(to); s.start(t); s.stop(t + dur + r + 0.05); return fl; }
const kick = (t, v = 0.9) => { const x = ac.createOscillator(), g = ac.createGain(); x.frequency.setValueAtTime(130, t); x.frequency.exponentialRampToValueAtTime(45, t + 0.16); g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.38); x.connect(g); g.connect(bus); x.start(t); x.stop(t + 0.4); };
const snare = (t, v = 0.35) => { noise(t, 0.02, v, 'bandpass', 1900, 0.8, 0.001, 0.16); osc('triangle', 190, t, 0.02, v * 0.6, 0.001, 0.09); const s = ac.createGain(); s.gain.value = 0.25; };
const clap = (t, v = 0.28) => { for (const d of [0, 0.012, 0.024]) noise(t + d, 0.01, v, 'bandpass', 1400, 1.2, 0.001, 0.12); };
const hat = (t, v = 0.07) => noise(t, 0.01, v, 'highpass', 8000, 0.7, 0.001, 0.05);
const crash = (t, v = 0.22) => { noise(t, 0.05, v, 'highpass', 5000, 0.5, 0.001, 2.2); };
const pad = (ch, t, dur, v, lp = 1800, a = 0.6) => ch.forEach(m => { for (const det of [-9, 0, 9]) osc('sawtooth', N(m), t, dur, v / 3, a, 0.9, { det, lp, rv: 0.6 }); });
const pluck = (m, t, v) => { osc('triangle', N(m), t, 0.04, v, 0.004, 0.45, { rv: 0.35 }); osc('sine', N(m + 12), t, 0.02, v * 0.35, 0.003, 0.3); };
const bass = (m, t, dur, v = 0.32) => { osc('sine', N(m), t, dur, v, 0.01, 0.12); osc('triangle', N(m), t, dur, v * 0.3, 0.01, 0.1, { lp: 600 }); };
const impact = (t, v = 0.9) => { const x = ac.createOscillator(), g = ac.createGain(); x.frequency.setValueAtTime(90, t); x.frequency.exponentialRampToValueAtTime(30, t + 1.2); g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.001, t + 1.8); x.connect(g); g.connect(bus); x.start(t); x.stop(t + 1.9); noise(t, 0.1, 0.25, 'lowpass', 900, 0.7, 0.002, 1.2); };
const riser = (t0, t1, v = 0.22) => { const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const f = ac.createBiquadFilter(); f.type = 'bandpass'; f.Q.value = 2.5; f.frequency.setValueAtTime(400, t0); f.frequency.exponentialRampToValueAtTime(7000, t1); const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(v, t1 - 0.05); g.gain.linearRampToValueAtTime(0.0001, t1 + 0.02); s.connect(f); f.connect(g); g.connect(bus); s.start(t0); s.stop(t1 + 0.1);
  const x = ac.createOscillator(); x.type = 'sawtooth'; x.frequency.setValueAtTime(N(45), t0); x.frequency.exponentialRampToValueAtTime(N(69), t1); const g2 = ac.createGain(); g2.gain.setValueAtTime(0.0001, t0); g2.gain.exponentialRampToValueAtTime(0.05, t1 - 0.05); g2.gain.linearRampToValueAtTime(0.0001, t1 + 0.02); const lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 2500; x.connect(lp); lp.connect(g2); g2.connect(bus); x.start(t0); x.stop(t1 + 0.1);
  // 스네어 롤(점점 빠르게)
  let t = t0 + (t1 - t0) * 0.35, step = 0.2; while (t < t1 - 0.03) { snare(t, 0.08 + 0.22 * (t - t0) / (t1 - t0)); t += step; step = Math.max(0.045, step * 0.86); } };
const BPM = 100, B = 60 / BPM, BAR = 4 * B;
// 코드: 1도-5도-6도-4도
const prog = k => [[48, 52, 55, 60], [43, 50, 55, 59], [45, 52, 57, 60], [41, 48, 53, 57]].map(c => c.map(m => m + k));
// ① 문제: 어둡고 느린 패드 + 낮은 맥박 + 피아노 몇 음
{ const ch = [[45, 52, 57, 60], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 62]]; let t = 0.2, i = 0;
  while (t < C.title - 0.2) { const d = Math.min(BAR * 1.5, C.title - t); pad(ch[i % 4].map(m => m - 12 + 12), t, d, 0.05, 900, 1.4); bass(ch[i % 4][0] - 12, t, d * 0.9, 0.16);
    [0, 2, 3].forEach((k, j) => { if (t + k * B * 1.5 < C.title - 0.5) pluck(ch[i % 4][(j + 1) % 4] + 12, t + k * B * 1.5, 0.08); }); t += BAR * 1.5; i++; }
  for (let p = 0.4; p < C.title - 0.3; p += B * 2) osc('sine', N(33), p, 0.05, 0.12, 0.01, 0.5); // 심장박동 같은 낮은 맥박
  riser(C.title - 2.2, C.title, 0.14); }
// ② 제목: 쿵 + 반짝이는 고음
impact(C.title, 0.85); crash(C.title, 0.18); [72, 76, 79, 84].forEach((m, k) => pluck(m, C.title + 0.15 + k * 0.12, 0.09));
pad(prog(0)[0], C.title, C.demo - C.title + 0.4, 0.07, 2200, 0.3);
{ const ch = prog(0)[0]; for (let t = C.title + 0.9, e = 0; t < C.demo - 0.05; t += B / 2, e++) pluck(ch[[0, 1, 2, 3, 2, 1][e % 6]] + 12, t, 0.03 + 0.04 * Math.min(1, (t - C.title) / (C.demo - C.title))); for (let t = C.title + 1.2; t < C.demo - 0.05; t += B) osc('sine', N(36), t, 0.05, 0.14, 0.01, 0.35); }
// ③ 시연: 밝은 박자(킥 1·3, 클랩 2·4, 하이햇 8분, 아르페지오, 베이스)
{ const P = prog(0), arp = [0, 1, 2, 3, 2, 1, 2, 3]; let bar = 0;
  for (let t = C.demo; t < C.climax - 3.5 - 0.01; t += BAR, bar++) {
    const ch = P[bar % 4], end = C.climax - 3.5;
    pad(ch, t, Math.min(BAR, end - t), 0.05, 1500, 0.25);
    for (let b = 0; b < 4; b++) { const tb = t + b * B; if (tb >= end) break;
      if (b % 2 === 0) kick(tb, bar < 2 ? 0.5 : 0.75); else clap(tb, bar < 2 ? 0.14 : 0.22);
      hat(tb + B / 2, 0.05); if (bar >= 4) hat(tb, 0.035);
      bass(ch[0] - 12, tb, B * 0.8, 0.26); }
    for (let e = 0; e < 8; e++) { const te = t + e * B / 2; if (te < end) pluck(ch[arp[e]] + 12, te, bar < 2 ? 0.05 : 0.07); }
  }
  riser(C.climax - 3.5, C.climax, 0.24); }
// ④ 클라이맥스: 조를 올리고(장2도) 꽉 찬 소리 — 4박 킥, 넓은 패드, 멜로디
{ const P = prog(2), mel = [[76, 74, 72, 74], [74, 71, 74, 79], [76, 72, 76, 81], [77, 76, 74, 72]]; let bar = 0;
  impact(C.climax, 0.7); crash(C.climax, 0.3);
  for (let t = C.climax; t < C.outro - 0.01; t += BAR, bar++) {
    const ch = P[bar % 4], end = C.outro;
    pad(ch, t, Math.min(BAR, end - t), 0.11, 3200, 0.05); pad(ch.map(m => m + 12), t, Math.min(BAR, end - t), 0.04, 4000, 0.05);
    for (let b = 0; b < 4; b++) { const tb = t + b * B; if (tb >= end) break; kick(tb, 0.95); if (b % 2) { clap(tb, 0.3); snare(tb, 0.18); } hat(tb + B / 2, 0.08); bass(ch[0] - 12, tb, B * 0.45, 0.3); bass(ch[0] - 12, tb + B / 2, B * 0.4, 0.22); }
    mel[bar % 4].forEach((m, k) => { const tm = t + k * B; if (tm < end) { osc('square', N(m + 2), tm, B * 0.8, 0.035, 0.01, 0.25, { lp: 3000, rv: 0.5 }); osc('sawtooth', N(m + 2), tm, B * 0.8, 0.03, 0.01, 0.25, { lp: 2500, det: 7, rv: 0.5 }); } });
    for (let e = 0; e < 8; e++) { const te = t + e * B / 2; if (te < end) pluck(ch[[0, 1, 2, 3, 2, 3, 1, 2][e]] + 24, te, 0.05); }
  } }
// ⑤ 마무리: 박자를 빼고 넓은 패드 + 피아노, 마지막 화면에 긴 화음
{ const P = prog(2); let i = 0; crash(C.outro, 0.16);
  for (let t = C.outro; t < C.end - 0.01; t += BAR, i++) { pad(P[i % 4], t, Math.min(BAR, C.end - t) + 0.3, 0.08, 1800, 0.4); bass(P[i % 4][0] - 12, t, Math.min(BAR, C.end - t), 0.2); [0, 1, 2, 3].forEach(k => { if (t + k * B < C.end) pluck(P[i % 4][(k * 2 + 1) % 4] + 12, t + k * B, 0.07); }); }
  impact(C.end, 0.5); const fin = [50, 57, 62, 66, 69, 74]; pad(fin, C.end, C.total - C.end - 1.5, 0.12, 2600, 0.2); [74, 78, 81, 86].forEach((m, k) => pluck(m, C.end + 0.3 + k * 0.18, 0.08)); }
// 덕킹: 내레이션 동안 음악을 낮춤 (큰 글씨 장면은 조금 덜 낮춤)
const BG = 0.9, DUCK = 0.33, DUCKC = 0.45;
duck.gain.setValueAtTime(0, 0); duck.gain.linearRampToValueAtTime(BG, 1.2);
for (const [a, b, card] of C.voice) { const lv = (a >= C.climax && a < C.outro) ? 0.62 : card ? DUCKC : DUCK; duck.gain.setTargetAtTime(lv, a - 0.25, 0.08); duck.gain.setTargetAtTime(BG, b + 0.15, 0.3); }
duck.gain.setTargetAtTime(0.0001, C.total - 2.2, 0.6);
const buf = await ac.startRendering();
// WAV(16비트)로
const L = buf.getChannelData(0), R = buf.getChannelData(1), n = L.length, out = new DataView(new ArrayBuffer(44 + n * 4));
const ws = (o, s) => { for (let i = 0; i < s.length; i++) out.setUint8(o + i, s.charCodeAt(i)); };
ws(0, 'RIFF'); out.setUint32(4, 36 + n * 4, true); ws(8, 'WAVE'); ws(12, 'fmt '); out.setUint32(16, 16, true); out.setUint16(20, 1, true); out.setUint16(22, 2, true); out.setUint32(24, SR, true); out.setUint32(28, SR * 4, true); out.setUint16(32, 4, true); out.setUint16(34, 16, true); ws(36, 'data'); out.setUint32(40, n * 4, true);
let pk = 0; for (let i = 0; i < n; i++) pk = Math.max(pk, Math.abs(L[i]), Math.abs(R[i])); const k = pk > 0.98 ? 0.98 / pk : 1;
for (let i = 0; i < n; i++) { out.setInt16(44 + i * 4, Math.max(-1, Math.min(1, L[i] * k)) * 32767, true); out.setInt16(46 + i * 4, Math.max(-1, Math.min(1, R[i] * k)) * 32767, true); }
const u8 = new Uint8Array(out.buffer); let s = ''; for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
window.__b64 = btoa(s); window.__done = 1;
} catch (e) { window.__err = e.message + ' ' + e.stack; window.__done = 1; } })();
</script>'''
pf = os.path.join(work, 'bgm3.html')
open(pf, 'w', encoding='utf-8').write(page)
r = subprocess.run(['node', os.path.join(here, 'render3.mjs'), pf, os.path.join(work, 'bgm.wav')], capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip(), r.stderr.strip()[:500])
