# W12 §5.1 DBSCAN: ε-이웃 원 안의 점 수(자기 자신 포함)로 core / border / noise를 가른다. MinPts = 5는 §5.2 실습 값, 점 배치는 설명용
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *
import matplotlib.patches as mp

OUT = os.environ.get("FIG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w12"))

MINPTS = 5          # §5.2 실습: dbscan_(Xm, eps = 0.15, minpts = 5)
EPS = 0.70         # 그림 좌표(인치)에서의 반지름 — 설명용

L = {
    "ko": dict(core="core point", border="border point", noise="noise",
               core_n="이웃 {n}개 ≥ MinPts", border_n="이웃 {n}개 < MinPts\n원 안에 core가 있음",
               noise_n="이웃 {n}개 (자기 자신)\n원 안에 core 없음 → 군집에 배정 안 함",
               eps="ε", rule="MinPts = 5 · 이웃 수는 원 안의 점 수 (자기 자신 포함)"),
}

# hand-placed points (inches); classification is computed below and checked
P = np.array([
    [1.30, 2.05], [1.70, 2.45], [1.85, 1.90], [2.25, 2.20], [2.15, 1.55],
    [1.55, 1.50], [2.60, 1.80], [2.05, 2.75], [1.25, 2.60], [2.60, 2.45],
    [3.15, 2.05],                          # border (right edge)
    [0.95, 1.30],                          # border (lower-left edge)
    [4.35, 1.25],                          # noise
])
CORE_I, BORDER_I, NOISE_I = 3, 10, 12      # the three points whose ε-circles are drawn

D = np.linalg.norm(P[:, None] - P[None], axis=2)
NB = D <= EPS
CNT = NB.sum(1)
CORE = CNT >= MINPTS
BORDER = ~CORE & (NB & CORE[None]).any(1)
NOISE = ~CORE & ~BORDER
assert CORE[CORE_I] and BORDER[BORDER_I] and NOISE[NOISE_I], (CNT, CORE, BORDER)
assert NOISE.sum() == 1

C_CORE, C_BORDER, C_NOISE = CAT[0], CAT[2], "#9AA1AB"


def draw(lang):
    t = L[lang]
    fig, ax = new(8.4, 3.7)
    ax.set_aspect("equal")

    # ε-circles for the three representatives
    for i, c in [(CORE_I, C_CORE), (BORDER_I, C_BORDER), (NOISE_I, C_NOISE)]:
        ax.add_patch(mp.Circle(P[i], EPS, fc=mix(c, 0.08), ec=c, lw=1.4, ls=(0, (4, 3)), zorder=1))
    # radius marker on the core circle
    cx, cy = P[CORE_I]
    ang = np.deg2rad(80)
    ex, ey = cx + EPS * np.cos(ang), cy + EPS * np.sin(ang)
    ax.plot([cx, ex], [cy, ey], color=TEXT2, lw=1.2, zorder=2)
    label(ax, (cx + ex) / 2 + 0.1, (cy + ey) / 2, t["eps"], fs=13, c=TEXT2, ha="left")

    # points
    for i, (x, y) in enumerate(P):
        if CORE[i]:
            ax.add_patch(mp.Circle((x, y), 0.085, fc=C_CORE, ec="white", lw=1.2, zorder=4))
        elif BORDER[i]:
            ax.add_patch(mp.Circle((x, y), 0.085, fc="white", ec=C_BORDER, lw=2.2, zorder=4))
        else:
            ax.plot(x, y, marker="x", ms=10, mew=2.4, color=TEXT2, zorder=4)

    # annotations
    def note(i, xt, yt, head, body, c, ha="left"):
        label(ax, xt, yt, head, fs=12, w="bold", c=c, ha=ha, va="bottom")
        label(ax, xt, yt - 0.06, body, fs=11, c=TEXT, ha=ha, va="top", linespacing=1.35)

    note(CORE_I, 0.3, 3.55, t["core"], t["core_n"].format(n=CNT[CORE_I]), C_CORE)
    arrow(ax, 1.55, 3.25, cx - 0.08, cy + 0.12, color=C_CORE, lw=1.2, ms=10, rad=0.25)
    bx, by = P[BORDER_I]
    note(BORDER_I, 3.95, 3.15, t["border"], t["border_n"].format(n=CNT[BORDER_I]), C_BORDER)
    arrow(ax, 3.9, 2.85, bx + 0.12, by + 0.06, color=C_BORDER, lw=1.2, ms=10, rad=0.2)
    nx, ny = P[NOISE_I]
    note(NOISE_I, 5.2, 1.55, t["noise"], t["noise_n"].format(n=CNT[NOISE_I]), TEXT2)

    label(ax, 0.3, 0.2, t["rule"], fs=11, c=TEXT2, ha="left")
    print("counts", dict(core=int(CNT[CORE_I]), border=int(CNT[BORDER_I]), noise=int(CNT[NOISE_I])),
          "n_core", int(CORE.sum()))
    save(fig, os.path.join(OUT, "dbscan_points" + ".png"))


for lang in L:
    draw(lang)
