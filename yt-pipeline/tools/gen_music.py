"""Original, copyright-free music beds + SFX, synthesized from scratch with numpy (no samples, no downloads).
usage: gen_music.py <assets_dir>
writes music_informative.wav, music_exciting.wav, music_suspense.wav, music_drama.wav (~3 min seamless loops),
whoosh.wav, hit.wav
"""
import sys, wave, numpy as np
OUT = sys.argv[1]; SR = 44100
rng = np.random.default_rng(42)

def save(name, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1: x = np.stack([x, x], 1)
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    with wave.open(f"{OUT}/{name}", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def lp(x, cut):                       # one-pole low-pass
    a = np.exp(-2 * np.pi * cut / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y
def lp_fast(x, cut):                  # FFT low-pass for long buffers
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cut) ** 4); return np.fft.irfft(X, len(x))
def hp_fast(x, cut):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (f / cut) ** 4 / (1 + (f / cut) ** 4); return np.fft.irfft(X, len(x))
def env(n, a, r):
    e = np.ones(n); A = int(a * SR); R = int(r * SR)
    if A: e[:A] = np.linspace(0, 1, A)
    if R: e[-R:] *= np.linspace(1, 0, R)
    return e
def note(f): return 440 * 2 ** ((f - 69) / 12)
def saw(fr, t): return 2 * ((fr * t) % 1) - 1
def tri(fr, t): return 2 * np.abs(2 * ((fr * t) % 1) - 1) - 1

def reverb(x, mix=0.25):
    out = x.copy()
    for d, g in [(0.031, .5), (0.047, .42), (0.071, .36), (0.113, .3), (0.167, .24), (0.229, .18)]:
        k = int(d * SR); out[k:] += x[:-k] * g * mix * 2
    return out

def track(bpm, chords, bars_per_chord, style, total_s=180):
    beat = 60 / bpm; bar = 4 * beat
    n = int(total_s * SR); t = np.arange(n) / SR
    pad = np.zeros(n); bass = np.zeros(n); lead = np.zeros(n); drums = np.zeros(n)
    seg = bar * bars_per_chord; nseg = int(np.ceil(total_s / seg))
    for c in range(nseg):
        root, quality = chords[c % len(chords)]
        ints = [0, 3, 7, 10] if quality == "m" else [0, 4, 7, 11]
        s0 = int(c * seg * SR); s1 = min(n, int((c + 1) * seg * SR)); L = s1 - s0
        if L <= 0: break
        tt = np.arange(L) / SR
        e = env(L, 0.6, 0.6)
        for iv in ints:                                  # warm detuned pad
            f = note(root + 12 + iv)
            pad[s0:s1] += (saw(f * 1.003, tt) + saw(f * 0.997, tt)) * e * 0.12
        # bass
        if style in ("informative", "exciting"):
            for b in range(int(seg / beat)):
                b0 = s0 + int(b * beat * SR); bl = int(beat * SR * (0.9 if style == "exciting" else 1.8))
                if b0 >= s1: break
                bl = min(bl, n - b0); tb = np.arange(bl) / SR
                if style == "informative" and b % 2: continue
                bass[b0:b0 + bl] += np.sin(2 * np.pi * note(root - 12) * tb) * np.exp(-tb * 3) * 0.55
        elif style == "suspense":
            bass[s0:s1] += np.sin(2 * np.pi * note(root - 12) * tt) * e * 0.5          # drone
            for b in range(int(seg / (beat / 2))):                                        # ticking pulse
                b0 = s0 + int(b * beat / 2 * SR); bl = min(int(0.06 * SR), n - b0)
                if b0 >= s1: break
                tb = np.arange(bl) / SR
                lead[b0:b0 + bl] += np.sin(2 * np.pi * note(root + 24) * tb) * np.exp(-tb * 60) * 0.25
        else:   # drama: slow piano-like notes
            for b in range(int(seg / beat)):
                b0 = s0 + int(b * beat * SR); bl = min(int(beat * SR * 2.5), n - b0)
                if b0 >= s1: break
                tb = np.arange(bl) / SR; f = note(root + 24 + ints[b % len(ints)])
                tone = sum(np.sin(2 * np.pi * f * h * tb) / h ** 1.6 for h in (1, 2, 3, 4))
                lead[b0:b0 + bl] += tone * np.exp(-tb * 2.2) * 0.32
        # arpeggio (informative / exciting)
        if style in ("informative", "exciting"):
            step = beat / (4 if style == "exciting" else 2)
            for b in range(int(seg / step)):
                b0 = s0 + int(b * step * SR); bl = min(int(step * SR * 0.9), n - b0)
                if b0 >= s1: break
                tb = np.arange(bl) / SR; f = note(root + 24 + ints[b % len(ints)] + (12 if b % 8 >= 4 else 0))
                lead[b0:b0 + bl] += tri(f, tb) * np.exp(-tb * 9) * (0.16 if style == "exciting" else 0.12)
    # drums
    if style in ("informative", "exciting"):
        nb = int(total_s / beat)
        for b in range(nb):
            b0 = int(b * beat * SR)
            if style == "exciting" or b % 2 == 0:                                 # kick
                kl = min(int(0.25 * SR), n - b0); tk = np.arange(kl) / SR
                drums[b0:b0 + kl] += np.sin(2 * np.pi * (50 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 9) * 0.8
            if b % 2 == 1:                                                        # snare-ish noise
                sl = min(int(0.18 * SR), n - b0)
                drums[b0:b0 + sl] += rng.normal(0, 1, sl) * np.exp(-np.arange(sl) / SR * 20) * (0.22 if style == "exciting" else 0.12)
            for hh in (0, 0.5):                                                   # hats
                h0 = b0 + int(hh * beat * SR); hl = min(int(0.04 * SR), n - h0)
                if hl > 0: drums[h0:h0 + hl] += rng.normal(0, 1, hl) * np.exp(-np.arange(hl) / SR * 120) * 0.08
        drums = hp_fast(drums, 30)
    pad = lp_fast(pad, 1400 if style != "suspense" else 700)
    mix = pad * 0.8 + bass + reverb(lead, 0.35) + drums * 0.7
    if style == "suspense": mix += lp_fast(rng.normal(0, 1, n), 300) * 0.05 * (1 + np.sin(2 * np.pi * t / 8))
    # seamless loop: crossfade tail into head
    xf = int(2 * SR); mix[:xf] = mix[:xf] * np.linspace(0, 1, xf) + mix[-xf:] * np.linspace(1, 0, xf); mix = mix[:-xf]
    l = mix + np.roll(mix, int(0.012 * SR)) * 0.15; r = mix + np.roll(mix, int(0.017 * SR)) * 0.15
    return np.stack([l, r], 1)

C = lambda *xs: list(xs)
save("music_informative.wav", track(96,  C((57, "m"), (53, "M"), (48, "M"), (55, "M")), 2, "informative"))
save("music_exciting.wav",    track(118, C((50, "m"), (58, "M"), (53, "M"), (57, "M")), 1, "exciting"))
save("music_suspense.wav",    track(84,  C((52, "m"), (53, "M"), (52, "m"), (47, "M")), 2, "suspense"))
save("music_drama.wav",       track(70,  C((57, "m"), (52, "m"), (53, "M"), (48, "M")), 2, "drama"))
# SFX
n = int(0.6 * SR); tt = np.arange(n) / SR
w = lp(rng.normal(0, 1, n) * np.sin(np.pi * tt / 0.6) ** 2, 2500) + lp(rng.normal(0, 1, n), 700) * np.sin(np.pi * tt / 0.6) ** 3
save("whoosh.wav", w)
n = int(1.2 * SR); tt = np.arange(n) / SR
h = np.sin(2 * np.pi * (45 + 70 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 3.5) + lp(rng.normal(0, 1, n), 1800) * np.exp(-tt * 14) * 0.5
save("hit.wav", reverb(h, 0.4))
n = int(1.6 * SR); tt = np.arange(n) / SR                      # riser
r = np.sin(2 * np.pi * (200 * tt + 600 * tt ** 2)) * (tt / 1.6) ** 2 + lp_fast(rng.normal(0, 1, n), 3000) * (tt / 1.6) ** 3 * 0.6
save("riser.wav", r)
n = int(0.05 * SR); tt = np.arange(n) / SR
save("click.wav", np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 140))
n = int(0.15 * SR); tt = np.arange(n) / SR
save("pop.wav", np.sin(2 * np.pi * (300 + 900 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 30))
n = int(60 * SR); tt = np.arange(n) / SR                         # room-tone ambient bed
a = lp_fast(rng.normal(0, 1, n), 400) * (0.7 + 0.3 * np.sin(2 * np.pi * tt / 15))
xf = int(2 * SR); a[:xf] = a[:xf] * np.linspace(0, 1, xf) + a[-xf:] * np.linspace(1, 0, xf); a = a[:-xf]
save("ambient.wav", a * 0.3 / 0.89)
print("ok")
