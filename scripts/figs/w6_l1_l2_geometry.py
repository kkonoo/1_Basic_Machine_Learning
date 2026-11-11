# W6 §2.3 왜 L1만 0을 만드는가: 손실 등고선이 제약 영역(L2 원, L1 마름모)에 처음 닿는 점이 해.
# 마름모는 꼭짓점이 축 위에 있어 w1 = 0에서 닿기 쉽다. 등고선 모양은 설명용으로 고른 값.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.environ.get("FIG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w6"))

L = {
    "ko": dict(p=["① Ridge (L2) — 원", "② Lasso (L1) — 마름모"], ols="최소제곱 해", contour="손실 등고선",
               ridge="처음 닿는 점 = 해\nw₁, w₂ 모두 0이 아님", lasso="꼭짓점에서 닿음\n→ w₁ = 0"),
}

C = np.array([0.8, 1.3])                    # least-squares estimate (illustrative)
rot = -0.5
Rm = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
A = Rm @ np.diag([1, 3]) @ Rm.T             # loss = (w - C)^T A (w - C)


def q(P):
    d = P - C
    return np.einsum("ij,jk,ik->i", d, A, d)


th = np.linspace(0, 2 * np.pi, 20001)
CIRCLE = np.c_[np.cos(th), np.sin(th)]
s = np.linspace(-1, 1, 20001)
DIAMOND = np.r_[np.c_[s, 1 - abs(s)], np.c_[s[::-1], -(1 - abs(s[::-1]))]]
gx, gy = np.meshgrid(np.linspace(-1.5, 2.45, 400), np.linspace(-1.35, 2.7, 400))
GQ = q(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)


def panel(ax, region, fc, title, note, accent, t, show_contour_label):
    k = np.argmin(q(region)); hit = region[k]; lev = q(region)[k]
    ax.axhline(0, color="#9AA1AB", lw=1, zorder=1); ax.axvline(0, color="#9AA1AB", lw=1, zorder=1)
    ax.fill(region[:, 0], region[:, 1], color=mix(fc, 0.2), zorder=2)
    ax.plot(region[:, 0], region[:, 1], color=fc, lw=2, zorder=3)
    ax.contour(gx, gy, GQ, levels=[lev * 0.08, lev * 0.35, lev], colors=TEXT2, linewidths=[1, 1, 1.4], zorder=3)
    ax.plot(*C, "o", color=TEXT, ms=5, zorder=5)
    ax.text(C[0] + 0.12, C[1] + 0.12, t["ols"], fontsize=11, color=TEXT, ha="left", va="bottom")
    ax.plot(*hit, "o", color=fc, ms=9, mec="white", mew=1.5, zorder=6)
    col = ACCENT_INK if accent else TEXT
    ax.annotate(note, xy=hit, xytext=(-1.45, 2.3), fontsize=11, fontweight="bold" if accent else "regular",
                color=col, ha="left", va="center", linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.3, shrinkB=6, connectionstyle="arc3,rad=-0.2"))
    if show_contour_label:
        ax.text(2.4, 0.25, t["contour"], fontsize=11, color=TEXT2, ha="right")
    ax.text(2.42, -0.1, "w₁", fontsize=12, ha="right", va="top", color=TEXT)
    ax.text(0.08, 2.68, "w₂", fontsize=12, ha="left", va="top", color=TEXT)
    ax.text(0.47, -1.5, title, fontsize=12, fontweight="bold", color=fc, ha="center", va="top")
    ax.set_xlim(-1.5, 2.45); ax.set_ylim(-1.35, 2.7); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    return hit


def draw(lang):
    t = L[lang]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 4.6), gridspec_kw={"wspace": 0.06})
    h1 = panel(a1, CIRCLE, CAT[1], t["p"][0], t["ridge"], False, t, True)
    h2 = panel(a2, DIAMOND, CAT[0], t["p"][1], t["lasso"], True, t, False)
    print(lang, "ridge hit", h1.round(3), "lasso hit", h2.round(3))
    a1.axison = True
    save(fig, os.path.join(OUT, "l1_l2_geometry" + ".png"))


for lang in L:
    draw(lang)
