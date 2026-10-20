# 배경음악 만들기: 녹화한 장면 시각(marks.json)에 맞춰 합성 → 영상작업/bgm.wav
# 이야기 흐름(2026-10-18 사용자 승인): 같은 4음 주제 선율(1-3-5-4)이 처음엔 단조로 외롭게 → 마지막엔 장조로 크게
#   문제(p1~p3): 단조 피아노 주제 + 어두운 현악 + 낮은 맥박
#   제목: 쿵 + 주제 첫 두 음을 밝게
#   시연(d1~): 다장조 피아노 분산화음 + 부드러운 박자 (내레이션을 가리지 않게)
#   2막 관리자 장면(d10~): 현악 한 옥타브 위·북을 더해 조금씩 쌓기 시작 · 3막 다음 담당자(d9~): 북을 한 단계 더
#   쌓아 올림(s1~s3, 설치 0·서버 0): 큰북 크레셴도 + 현악 부풀림 + 끌어올림 → 0.8초 멈춤
#   클라이맥스(e1 「숙달된 직원의 노하우를, 처음 맡은 직원에게」~): 라장조로 올려 주제 선율을 크게(피아노 옥타브 + 현악 + 글로켄)
#   끝: 주제가 1-3-5-8로 풀리며 긴 화음
# 음색: 피아노(배음을 겹친 소리)·현악(천천히 커지는 톱니파 여럿 + 떨림)·큰북·글로켄 — 예전 사각파 멜로디는 쓰지 않음
# (2026-10-20 동기부여 영상 느낌, 사용자 요청 — 남의 곡은 쓰지 않고 그 장르의 장점만): 문제 장면 맥박 → 심장 박동(쿵-쿵),
#   2막 현악 반복(8분음표, 작게) → 3막 16분음표 → 쌓아 올림에서 현악 반복·금관이 부풀고 북 합주·빨라지는 작은북 → 멈춤 →
#   클라이맥스 첫 박 「브람」(아주 낮은 금관이 확 열림) + 금관 화음·주제 선율을 금관이 함께 → 끝 화음에 금관
# 내레이션 동안은 음악을 낮춤(덕킹). 크롬 OfflineAudioContext로 실제 시간보다 빠르게 만듦
# 실행: python tools/video3/bgm3.py [marks.json 경로]
import json, os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__))
work = os.path.join(here, '..', '..', '영상작업')
mk = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(work, 'marks.json'), encoding='utf-8'))
seg = {s['id']: s for s in json.load(open(os.path.join(work, 'seg.json'), encoding='utf-8'))}
M = {m['id']: m for m in mk['marks']}
cfg = dict(total=round(mk['total'] + 0.3, 3), title=M['title']['t0'], demo=M['d1']['t0'], collab=M['d10']['t0'], act3=M['d9']['t0'], build=M['s1']['t0'],
           climax=M['e1']['t0'], end=M['end']['t0'],
           voice=[[m['voiceAt'], m['voiceAt'] + seg[m['id']]['dur'], 1 if m['kind'] == 'card' else 0] for m in mk['marks']])
page = r'''<!doctype html><meta charset="utf-8"><script>
const C = ''' + json.dumps(cfg) + r''';
(async () => { try {
const SR = 48000, ac = new OfflineAudioContext(2, Math.ceil(C.total * SR), SR);
const N = m => 440 * Math.pow(2, (m - 69) / 12);
// 마스터: 컴프레서 → 출력, 리버브 보냄
const comp = ac.createDynamicsCompressor(); comp.threshold.value = -15; comp.ratio.value = 3; comp.attack.value = 0.01; comp.release.value = 0.3; comp.connect(ac.destination);
const master = ac.createGain(); master.gain.value = 0.9; master.connect(comp);
const duck = ac.createGain(); duck.connect(master);           // 내레이션 덕킹
const bus = ac.createGain(); bus.connect(duck);               // 모든 악기
const rv = ac.createConvolver(); { const len = SR * 3.2, b = ac.createBuffer(2, len, SR); for (let c = 0; c < 2; c++) { const d = b.getChannelData(c); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.4); } rv.buffer = b; }
const rvg = ac.createGain(); rvg.gain.value = 0.38; rv.connect(rvg); rvg.connect(duck);
const send = (node, amt) => { const s = ac.createGain(); s.gain.value = amt; node.connect(s); s.connect(rv); };
const noiseBuf = (() => { const b = ac.createBuffer(1, SR * 2, SR), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; return b; })();
// 쌓아 올림이 끝나고 클라이맥스 전 0.8초는 모든 소리를 멈춤(숨 고르기)
const HUSH0 = C.climax - 0.8, HUSH1 = C.climax;
const cut = (t, len) => (t < HUSH0 && t + len > HUSH0) ? HUSH0 - t : len;
const silent = t => t >= HUSH0 - 0.02 && t < HUSH1 - 0.01;

// ── 악기 ──
// 피아노: 배음 5개를 겹치고 높은 배음일수록 빨리 사라지게
function piano(m, t, v, len = 2.4, rvAmt = 0.45) {
  if (silent(t)) return; len = cut(t, len);
  const out = ac.createGain(); out.gain.value = 1; out.connect(bus); send(out, rvAmt);
  [[1, 1], [2, 0.42], [3, 0.2], [4, 0.1], [5, 0.05]].forEach(([h, a], k) => {
    const x = ac.createOscillator(); x.type = 'sine'; x.frequency.value = N(m) * h * (1 + k * 0.0004);
    const g = ac.createGain(); const dk = len * (1.1 - k * 0.17) * Math.max(0.45, 1 - (m - 60) / 60);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v * a, t + 0.006); g.gain.exponentialRampToValueAtTime(v * a * 0.35, t + 0.18); g.gain.exponentialRampToValueAtTime(0.0001, t + Math.max(0.3, dk));
    x.connect(g); g.connect(out); x.start(t); x.stop(t + Math.max(0.3, dk) + 0.05);
  });
}
// 현악: 톱니파 4개를 살짝 어긋나게 + 떨림(비브라토), 천천히 커지고 천천히 사라짐
function strings(ch, t, dur, v, lp = 1600, a = 0.9, r = 1.4) {
  if (silent(t)) return; dur = cut(t, dur); if (dur <= 0.05) return;
  const f = ac.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp; f.Q.value = 0.5;
  const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + Math.min(a, dur * 0.7)); g.gain.setValueAtTime(v, t + dur); g.gain.exponentialRampToValueAtTime(0.0001, t + dur + (t + dur >= HUSH0 - 0.02 && t < HUSH0 ? 0.08 : r));
  f.connect(g); g.connect(bus); send(g, 0.55);
  const lfo = ac.createOscillator(); lfo.frequency.value = 5.2; const lg = ac.createGain(); lg.gain.value = 7; lfo.connect(lg); lfo.start(t); lfo.stop(t + dur + r + 0.1);
  ch.forEach(m => [-11, -4, 4, 11].forEach(det => { const x = ac.createOscillator(); x.type = 'sawtooth'; x.frequency.value = N(m); x.detune.value = det; lg.connect(x.detune); const s = ac.createGain(); s.gain.value = 1 / (ch.length * 4); x.connect(s); s.connect(f); x.start(t); x.stop(t + dur + r + 0.1); }));
}
function noise(t, dur, v, type, fq, q, a = 0.002, r = 0.08, to = bus) { if (silent(t)) return; const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const fl = ac.createBiquadFilter(); fl.type = type; fl.frequency.value = fq; fl.Q.value = q || 0.7; const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + a); g.gain.setValueAtTime(v, t + a + dur); g.gain.exponentialRampToValueAtTime(0.0001, t + a + dur + r); s.connect(fl); fl.connect(g); g.connect(to); s.start(t); s.stop(t + a + dur + r + 0.05); }
const bass = (m, t, dur, v = 0.28) => { if (silent(t)) return; dur = cut(t, dur); const x = ac.createOscillator(); x.type = 'sine'; x.frequency.value = N(m); const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + 0.02); g.gain.setValueAtTime(v, t + Math.max(0.03, dur - 0.08)); g.gain.exponentialRampToValueAtTime(0.0001, t + dur + 0.12); x.connect(g); g.connect(bus); x.start(t); x.stop(t + dur + 0.2); };
const kick = (t, v = 0.6) => { if (silent(t)) return; const x = ac.createOscillator(), g = ac.createGain(); x.frequency.setValueAtTime(110, t); x.frequency.exponentialRampToValueAtTime(42, t + 0.18); g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.42); x.connect(g); g.connect(bus); x.start(t); x.stop(t + 0.45); };
// 큰북(영화 음악처럼 깊은 북): 낮은 음 + 짧은 잡음
const tom = (t, v = 0.5, f0 = 95) => { if (silent(t)) return; const x = ac.createOscillator(), g = ac.createGain(); x.frequency.setValueAtTime(f0, t); x.frequency.exponentialRampToValueAtTime(f0 * 0.55, t + 0.35); g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.7); x.connect(g); g.connect(bus); send(g, 0.25); x.start(t); x.stop(t + 0.75); noise(t, 0.015, v * 0.3, 'lowpass', 500, 0.7, 0.001, 0.12); };
const shaker = (t, v = 0.03) => noise(t, 0.012, v, 'highpass', 7000, 0.7, 0.003, 0.05);
const rim = (t, v = 0.08) => noise(t, 0.008, v, 'bandpass', 2200, 1.5, 0.001, 0.06);
const crash = (t, v = 0.2) => noise(t, 0.05, v, 'highpass', 5000, 0.5, 0.001, 2.6);
const glock = (m, t, v = 0.05) => { if (silent(t)) return; const x = ac.createOscillator(); x.type = 'sine'; x.frequency.value = N(m); const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + 0.003); g.gain.exponentialRampToValueAtTime(0.0001, t + 1.2); x.connect(g); g.connect(bus); send(g, 0.6); x.start(t); x.stop(t + 1.3); };
const impact = (t, v = 0.8) => { const x = ac.createOscillator(), g = ac.createGain(); x.frequency.setValueAtTime(85, t); x.frequency.exponentialRampToValueAtTime(30, t + 1.3); g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.001, t + 2.0); x.connect(g); g.connect(bus); send(g, 0.3); x.start(t); x.stop(t + 2.1); noise(t, 0.1, 0.22, 'lowpass', 900, 0.7, 0.002, 1.4); };
// 끌어올림: 잡음 필터가 위로 + 북 연타가 점점 빨라짐 (t1에서 딱 멈춤)
const riser = (t0, t1, v = 0.2) => { const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const f = ac.createBiquadFilter(); f.type = 'bandpass'; f.Q.value = 2.2; f.frequency.setValueAtTime(350, t0); f.frequency.exponentialRampToValueAtTime(6500, t1); const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(v, t1 - 0.04); g.gain.linearRampToValueAtTime(0.0001, t1); s.connect(f); f.connect(g); g.connect(bus); s.start(t0); s.stop(t1 + 0.05);
  let t = t0 + (t1 - t0) * 0.3, step = 0.3; while (t < t1 - 0.05) { tom(t, 0.15 + 0.4 * (t - t0) / (t1 - t0), 120); t += step; step = Math.max(0.07, step * 0.85); } };

// ── 동기부여 영상 느낌(2026-10-20 사용자 요청): 짧게 끊는 현악 반복·낮은 금관·북 합주·빨라지는 작은북 ──
// 금관: 톱니파 셋 + 필터가 열리며 커짐(호른·트롬본 느낌)
function brass(ch, t, dur, v, a = 0.3, r = 0.9, open = 2200) {
  if (silent(t)) return; dur = cut(t, dur); if (dur <= 0.05) return; const rr = (t + dur >= HUSH0 - 0.02 && t < HUSH0) ? 0.08 : r;
  const f = ac.createBiquadFilter(); f.type = 'lowpass'; f.Q.value = 1.1; f.frequency.setValueAtTime(260, t); f.frequency.linearRampToValueAtTime(open, t + a); f.frequency.setTargetAtTime(open * 0.6, t + a, 0.7);
  const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + a); g.gain.setValueAtTime(v * 0.85, t + dur); g.gain.exponentialRampToValueAtTime(0.0001, t + dur + rr);
  f.connect(g); g.connect(bus); send(g, 0.45);
  ch.forEach(m => [-7, 0, 7].forEach(d => { const x = ac.createOscillator(); x.type = 'sawtooth'; x.frequency.value = N(m); x.detune.value = d; const s = ac.createGain(); s.gain.value = 1 / (ch.length * 3); x.connect(s); s.connect(f); x.start(t); x.stop(t + dur + rr + 0.1); }));
}
// 「브람」: 아주 낮은 금관 화음이 확 열림(예고편의 쿵—)
const braam = (root, t, v = 0.3) => { brass([root - 24, root - 12, root - 5, root], t, 1.6, v, 0.07, 1.8, 1700); impact(t, 0.7); };
// 짧게 끊는 현악(스피카토)과 반복 음형: 근음-근음-옥타브-근음-5도-근음-옥타브-5도
function spic(m, t, v, lp = 2400) { if (silent(t)) return; const f = ac.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp; const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + 0.006); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.16); f.connect(g); g.connect(bus); send(g, 0.3); [-6, 6].forEach(d => { const x = ac.createOscillator(); x.type = 'sawtooth'; x.frequency.value = N(m); x.detune.value = d; x.connect(f); x.start(t); x.stop(t + 0.2); }); }
const OST = [0, 0, 12, 0, 7, 0, 12, 7];
const ostinato = (root, t, dur, v, div = 4, lp = 2400) => { const st = B / div; for (let k = 0; k * st < dur - 0.01; k++) spic(root + OST[k % 8], t + k * st, v * (k % 4 === 0 ? 1.3 : 1), lp); };
// 북 합주 한 마디: 쿵 · (쿵)쿵 쿵 · 쿵쿵
const taiko = (t, v) => [[0, 1, 70], [1.5, 0.55, 90], [2, 0.85, 70], [3, 0.7, 80], [3.5, 0.6, 95]].forEach(([b, a, f]) => tom(t + b * B, v * a, f));
// 빨라지는 작은북(t0~t1, 커지면서)
const roll = (t0, t1, v = 0.12) => { let t = t0, st = B / 2; while (t < t1 - 0.03) { const p = (t - t0) / (t1 - t0); noise(t, 0.01, v * (0.3 + 0.7 * p), 'bandpass', 1900, 0.9, 0.001, 0.07); t += st; st = Math.max(B / 8, st * 0.9); } };

const BPM = 96, B = 60 / BPM, BAR = 4 * B;
// 주제 선율(1-3-5-4)과 리듬(박): 1 · 3 · 5(길게) · 4(길게)
const MOTIF = [[0, 0, 1], [1, 4, 1], [2, 7, 2], [4, 5, 2.5]];   // [박, 음(반음), 길이(박)]
const motif = (root, t, v, beat, oct = 0, minor = false) => MOTIF.forEach(([b, iv, len]) => { const m = root + (minor && iv === 4 ? 3 : iv) + oct; piano(m, t + b * beat, v, len * beat + 1.6); });

// ① 문제: 가단조 — 외로운 피아노 주제 + 어두운 현악 + 낮은 맥박
{ const ch = [[45, 52, 57, 60], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 62]]; const Bp = 0.8, BARp = 4 * Bp; let t = 0.3, i = 0;
  while (t < C.title - 0.4) { const d = Math.min(BARp * 2, C.title - t); strings(ch[i % 4].map(m => m - 12), t, d, 0.05, 800, 1.6, 1.6); bass(ch[i % 4][0] - 12, t, d * 0.9, 0.12);
    if (t + 6 * Bp < C.title - 0.6) motif(i % 2 ? 64 : 69, t + 0.2, 0.11, Bp, 0, true);   // 가 → 마 단조로 두 번
    t += BARp * 2; i++; }
  // 심장 박동(쿵-쿵): 문제 장면의 긴장
  for (let p = 0.6; p < C.title - 0.4; p += Bp * 2) [[0, 0.12], [0.22, 0.08]].forEach(([o, v]) => { const q = p + o, x = ac.createOscillator(), g = ac.createGain(); x.frequency.setValueAtTime(62, q); x.frequency.exponentialRampToValueAtTime(40, q + 0.2); g.gain.setValueAtTime(0.0001, q); g.gain.linearRampToValueAtTime(v, q + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, q + 0.35); x.connect(g); g.connect(bus); x.start(q); x.stop(q + 0.4); });
  riser(C.title - 2.0, C.title, 0.12); }

// ② 제목: 쿵 + 주제 첫 두 음을 다장조로 밝게 + 반짝
impact(C.title, 0.8); crash(C.title, 0.16);
piano(72, C.title + 0.1, 0.14, 3); piano(76, C.title + 0.1 + B, 0.13, 3); [84, 88, 91, 96].forEach((m, k) => glock(m, C.title + 0.4 + k * 0.14, 0.05));
strings([48, 55, 60, 64], C.title, C.demo - C.title + 0.6, 0.07, 2000, 0.4);

// ③ 시연 + ④ 관리자 장면: 다장조 C-G-Am-F, 피아노 분산화음 + 부드러운 박자. 관리자 장면부터 조금씩 쌓음
const PC = [[48, 52, 55, 60], [43, 50, 55, 59], [45, 52, 57, 60], [41, 48, 53, 57]];
{ const arp = [0, 1, 2, 3, 2, 1, 2, 3]; let bar = 0;
  for (let t = C.demo; t < C.build - 0.01; t += BAR, bar++) {
    const ch = PC[bar % 4], end = C.build, rise = t >= C.collab, rise2 = t >= C.act3;   // 관리자 장면부터 · 3막부터 한 단계 더
    strings(ch, t, Math.min(BAR, end - t), rise ? 0.06 : 0.045, rise ? 2200 : 1500, 0.5, 0.8);
    if (rise) strings(ch.map(m => m + 12), t, Math.min(BAR, end - t), 0.025, 2600, 0.6, 0.8);
    for (let b = 0; b < 4; b++) { const tb = t + b * B; if (tb >= end) break;
      if (b % 2 === 0) kick(tb, bar < 2 ? 0.35 : rise2 ? 0.62 : rise ? 0.55 : 0.45); else rim(tb, rise2 ? 0.11 : rise ? 0.09 : 0.06);
      if (bar >= 2) shaker(tb + B / 2, rise2 ? 0.04 : 0.03); if (rise && b === 3) tom(tb + B / 2, 0.22); if (rise2 && b === 1) tom(tb + B / 2, 0.18, 120);
      bass(ch[0] - 12, tb, B * 0.85, 0.22); }
    for (let e = 0; e < 8; e++) { const te = t + e * B / 2; if (te < end) piano(ch[arp[e]] + 12, te, bar < 2 ? 0.05 : 0.06, 1.2, 0.35); }
    if (rise) ostinato(ch[0], t, Math.min(BAR, end - t), rise2 ? 0.026 : 0.02, rise2 ? 4 : 2, rise2 ? 2000 : 1600);   // 현악 반복: 2막 8분음표 → 3막 16분음표(내레이션 밑에서 작게)
    if (bar % 8 === 4 || (rise && bar % 4 === 0)) motif(72, t, 0.05, B / 2, 12);   // 주제 선율 살짝 (밝게)
  } }

// ⑤ 쌓아 올림(설치 0·서버 0): F-G-Am-A(라장조로 가는 문) — 큰북 크레셴도 + 현악 부풀림, 끝은 0.8초 멈춤
{ const PB = [[41, 48, 53, 57], [43, 50, 55, 59], [45, 52, 57, 60], [45, 49, 52, 57]]; const dur = HUSH0 - C.build; let bar = 0;
  for (let t = C.build; t < HUSH0 - 0.01; t += BAR, bar++) {
    const ch = PB[Math.min(3, Math.floor((t - C.build) / dur * 4))], p = (t - C.build) / dur;
    strings(ch, t, Math.min(BAR, HUSH0 - t), 0.07 + 0.06 * p, 1800 + 2500 * p, 0.3, 0.6);
    strings(ch.map(m => m + 12), t, Math.min(BAR, HUSH0 - t), 0.03 + 0.04 * p, 2500 + 2500 * p, 0.3, 0.6);
    ostinato(ch[0] + 12, t, Math.min(BAR, HUSH0 - t), 0.03 + 0.04 * p, 4, 1800 + 3000 * p);   // 현악 반복이 점점 밝고 크게
    if (p > 0.25) brass(ch.map(m => m - 12), t, Math.min(BAR, HUSH0 - t), 0.04 + 0.09 * p, BAR * 0.6, 0.6, 1200 + 1500 * p);   // 금관이 마디마다 부풀어 오름
    if (p > 0.5) taiko(t, 0.25 + 0.35 * p);
    else for (let b = 0; b < 4; b++) { const tb = t + b * B; if (tb >= HUSH0 - 0.05) break; tom(tb, 0.3 + 0.35 * p); }
    for (let b = 0; b < 4; b++) { const tb = t + b * B; if (tb >= HUSH0 - 0.05) break; bass(ch[0] - 12, tb, B * 0.9, 0.24); }
    for (let e = 0; e < 8; e++) { const te = t + e * B / 2; if (te < HUSH0 - 0.05) piano(ch[[0, 2, 3, 2][e % 4]] + 24, te, 0.035 + 0.03 * p, 0.8, 0.4); }
  }
  riser(Math.max(C.build, HUSH0 - 3.2), HUSH0, 0.15); roll(Math.max(C.build, HUSH0 - 2 * BAR), HUSH0, 0.13); }

// ⑥ 클라이맥스: 라장조 D-A-Bm-G — 주제 선율을 피아노 옥타브로 크게 + 현악 + 글로켄 + 큰북
const PD = [[50, 54, 57, 62], [45, 52, 57, 61], [47, 54, 59, 62], [43, 50, 55, 59]];
{ braam(50, C.climax, 0.32); crash(C.climax, 0.34); let bar = 0;
  for (let t = C.climax; t < C.end - 0.01; t += BAR, bar++) {
    const ch = PD[bar % 4], end = C.end, d = Math.min(BAR, end - t);
    strings(ch, t, d + 0.2, 0.16, 3600, 0.08, 1.0); strings(ch.map(m => m + 12), t, d + 0.2, 0.08, 4200, 0.12, 1.0);
    brass(ch.map(m => m - 12), t, d, 0.1, 0.12, 0.7, 2000);   // 금관 화음
    ostinato(ch[0] + 12, t, d, 0.05, 4, 4200);                  // 현악 반복(16분음표)
    taiko(t, 0.5);
    for (let b = 0; b < 4; b++) { const tb = t + b * B; if (tb >= end) break; kick(tb, 0.5); shaker(tb + B / 2, 0.045); bass(ch[0] - 12, tb, B * 0.45, 0.28); bass(ch[0] - 12, tb + B / 2, B * 0.4, 0.2); }
    if (bar % 2 === 0) { motif(74, t, 0.2, B, 0); motif(74, t, 0.12, B, 12); MOTIF.forEach(([bb, iv]) => glock(74 + iv + 24, t + bb * B, 0.04)); MOTIF.forEach(([bb, iv, len]) => brass([62 + iv], t + bb * B, len * B * 0.9, 0.07, 0.06, 0.4, 2600)); }   // 주제 선율(장조) — 금관이 함께
    else for (let e = 0; e < 8; e++) { const te = t + e * B / 2; if (te < end) piano(ch[[0, 1, 2, 3, 2, 3, 1, 2][e]] + 24, te, 0.06, 1.0); }
  } }

// ⑦ 끝: 주제가 1-3-5-8로 풀리며 라장조 긴 화음
{ impact(C.end, 0.45); crash(C.end, 0.14); const fin = [38, 50, 57, 62, 66, 69, 74];
  strings(fin, C.end, Math.max(1, C.total - C.end - 2.2), 0.13, 2800, 0.25, 2.0); brass([38, 50, 57, 62], C.end, Math.max(1, C.total - C.end - 2.4), 0.1, 0.5, 2.0, 1600);
  [[74, 0], [78, 1], [81, 2], [86, 3.2]].forEach(([m, b]) => { piano(m, C.end + 0.3 + b * 0.55, 0.14, 4); piano(m - 12, C.end + 0.3 + b * 0.55, 0.07, 4); });
  [86, 90, 93, 98].forEach((m, k) => glock(m, C.end + 2.4 + k * 0.16, 0.045)); bass(38, C.end, Math.max(1, C.total - C.end - 2), 0.22); }

// 덕킹: 내레이션 동안 음악을 낮춤 — 쌓아 올림·클라이맥스는 음악이 더 들리게
const BG = 0.9, DUCK = 0.33, DUCKC = 0.45, DUCKB = 0.52, DUCKX = 0.62;
duck.gain.setValueAtTime(0, 0); duck.gain.linearRampToValueAtTime(BG, 1.2);
for (const [a, b, card] of C.voice) { const lv = a >= C.climax ? DUCKX : a >= C.build ? DUCKB : card ? DUCKC : DUCK; duck.gain.setTargetAtTime(lv, a - 0.25, 0.08); duck.gain.setTargetAtTime(BG, b + 0.15, 0.3); }
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
