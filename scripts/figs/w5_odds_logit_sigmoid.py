# W5 §5.2 Odds → logit → sigmoid: 확률 p를 odds, logit으로 바꾸면 선형식 wᵀx + b와 같아지고, sigmoid가 그 선형식을 거꾸로 0–1 확률로 돌려준다.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w5")

LIN = r"$\mathbf{w}^{\mathsf{T}}\mathbf{x} + b$"
BOXES = [  # name, formula, range
    ("확률", r"$p$", "0 ~ 1에 갇힘"),
    ("odds", r"$\dfrac{p}{1-p}$", "0 ~ ∞"),
    ("logit", r"$\log\dfrac{p}{1-p}$", "실수 전체"),
    ("선형식", r"$z = \mathbf{w}^{\mathsf{T}}\mathbf{x} + b$", "실수 전체"),
]

W, HT, HB = 8.3, 2.85, 3.3
H = HT + HB
fig = plt.figure(figsize=(W, H))

# ── ① 위: 흐름 ────────────────────────────────────────────────────────────
ax = fig.add_axes([0, HB / H, 1, HT / H])
ax.set_xlim(0, W); ax.set_ylim(0, HT); ax.axis("off")
label(ax, 0.1, 2.55, "① 확률 → 선형식", fs=12, w="semibold", ha="left")

bw, gap, x0, by, bh = 1.74, 0.34, 0.1, 0.95, 1.35
cols = ramp(4)
cx = []
for i, ((nm, f, rg), c) in enumerate(zip(BOXES, cols)):
    x = x0 + i * (bw + gap)
    box(ax, x, by, bw, bh, fc=c, ec="none", r=0.1)
    tc = on(c)
    label(ax, x + bw / 2, by + bh - 0.22, nm, fs=12, w="bold", c=tc)
    label(ax, x + bw / 2, by + bh / 2 - 0.02, f, fs=14 if i < 3 else 12, c=tc)
    label(ax, x + bw / 2, by + 0.2, rg, fs=11, c=tc)
    cx.append(x + bw / 2)
    if i:
        xa = x - gap
        if i < 3:
            arrow(ax, xa + 0.05, by + bh / 2, x - 0.05, by + bh / 2, color="#6B7280", lw=1.8, ms=14)
        else:
            label(ax, x - gap / 2, by + bh / 2, "=", fs=18, w="bold", c=TEXT)

# 되돌아가는 길: sigmoid
yl = 0.35
ax.plot([cx[3], cx[3]], [by - 0.05, yl], color=PRIMARY, lw=1.8, zorder=3, solid_capstyle="round")
ax.plot([cx[3], cx[0]], [yl, yl], color=PRIMARY, lw=1.8, zorder=3, solid_capstyle="round")
arrow(ax, cx[0], yl, cx[0], by - 0.05, color=PRIMARY, lw=1.8, ms=14)
ax.text((cx[0] + cx[3]) / 2, yl, r"sigmoid로 되돌리기:  $p = \sigma(z) = \dfrac{1}{1 + e^{-z}}$",
        fontsize=12, color=PRIMARY, ha="center", va="center", zorder=5,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))

# ── ② 아래: sigmoid 곡선 ───────────────────────────────────────────────────
a2 = fig.add_axes([0.11, 0.09, 0.84, (HB - 1.0) / H])
z = np.linspace(-7, 7, 400)
a2.axhline(0, color=LINE, lw=1, ls="--", zorder=1)
a2.axhline(1, color=LINE, lw=1, ls="--", zorder=1)
a2.plot(z, 1 / (1 + np.exp(-z)), color=PRIMARY, lw=2.6, zorder=3)
a2.set_xlim(-7, 7); a2.set_ylim(-0.08, 1.12)
a2.set_xticks([0]); a2.set_yticks([0, 1])
a2.tick_params(labelsize=11)
a2.set_xlabel(r"$z = \mathbf{w}^{\mathsf{T}}\mathbf{x} + b$  (실수 전체)", fontsize=12)
a2.set_ylabel(r"$p = \sigma(z)$", fontsize=12)
a2.text(-6.8, 0.2, "$z$가 작아질수록\n$p \\to 0$", fontsize=11, color=TEXT2, ha="left", va="center", linespacing=1.4)
a2.text(6.8, 0.8, "$z$가 커질수록\n$p \\to 1$", fontsize=11, color=TEXT2, ha="right", va="center", linespacing=1.4)
fig.text(0.1 / W, (HB - 0.08) / H, "② sigmoid 곡선 — 어떤 $z$도 0 ~ 1 안으로", fontsize=12, fontweight="semibold",
         color=TEXT, ha="left", va="top")

save(fig, os.path.join(OUT, "odds_logit_sigmoid.png"))
