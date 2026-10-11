# 크롬 MediaRecorder WebM에는 Segment > Info 안에 Duration(재생 길이)이 없다 → 넣어 준다 (진행 막대로 찾아가기 가능하게)
import struct, sys
path, dur_ms = sys.argv[1], float(sys.argv[2])
b = bytearray(open(path, 'rb').read())

def read_vint(buf, i):
    first = buf[i]
    length = 1
    mask = 0x80
    while length <= 8 and not (first & mask):
        mask >>= 1; length += 1
    val = first & (mask - 1)
    for k in range(1, length):
        val = (val << 8) | buf[i + k]
    return val, length

def enc_size(val, length):
    # length 바이트 vint로 (맨 앞 비트 표시)
    out = val | (1 << (7 * length))
    return out.to_bytes(length, 'big')

INFO = b'\x15\x49\xA9\x66'
i = b.find(INFO)
assert i >= 0, 'Info 없음'
size, sl = read_vint(b, i + 4)
data_start = i + 4 + sl
info = bytes(b[data_start:data_start + size])
if b'\x44\x89' in info:
    print('이미 Duration이 있음'); sys.exit(0)
dur_el = b'\x44\x89\x88' + struct.pack('>d', dur_ms)
new_size = size + len(dur_el)
assert new_size < (1 << (7 * sl)) - 1, 'Info 크기 칸이 모자람'
b[i + 4:i + 4 + sl] = enc_size(new_size, sl)
b[data_start + size:data_start + size] = dur_el
open(path, 'wb').write(b)
print('Duration', dur_ms, 'ms 넣음 · Info 크기', size, '→', new_size)
