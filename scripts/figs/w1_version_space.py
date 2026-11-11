# W1 Hypothesis space와 version space: 모든 model(장난감 문제 65개) 중 training data와 모순되지 않는 것이 version space, 여러 개가 남고 inductive bias가 그중 하나를 고른다.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *
import matplotlib.patches as mp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w1")

N_ALL = 65          # 본문: feature 3개짜리 장난감 문제의 후보 수
N_VS = 7            # version space에 남은 수 — 설명용
GRAY = "#9AA1AB"

# outer = hypothesis space, inner = version space (inches)
OX, OY, OW, OH = 0.1, 0.45, 5.3, 3.05
IX, IY, IW, IH = 3.25, 0.65, 1.95, 1.85


def poisson(rng, n, xlo, xhi, ylo, yhi, dmin, reject):
    pts = []
    for _ in range(200000):
        p = np.array([rng.uniform(xlo, xhi), rng.uniform(ylo, yhi)])
        if reject(p) or any(np.hypot(*(p - q)) < dmin for q in pts):
            continue
        pts.append(p)
        if len(pts) == n:
            return np.array(pts)
    raise RuntimeError(f"placed only {len(pts)} of {n}")


def draw():
    fig, ax = new(8.4, 3.6)
    rng = np.random.default_rng(3)

    # hypothesis space
    box(ax, OX, OY, OW, OH, fc=FAINT, ec=GRAY, lw=1.2, r=0.18, z=1)
    label(ax, OX + 0.22, OY + OH - 0.25, "Hypothesis space", fs=13, w="bold", ha="left")
    label(ax, OX + 0.22, OY + OH - 0.55, "알고리즘이 고려할 수 있는 모든 model", fs=11, c=TEXT2, ha="left")

    # version space
    box(ax, IX, IY, IW, IH, fc=STEPS[3], ec=PRIMARY, lw=1.6, r=0.14, z=2)
    label(ax, IX + IW / 2, IY + IH - 0.24, "Version space", fs=12.5, w="bold", c=PRIMARY)
    label(ax, IX + IW / 2, IY + IH - 0.52, "training data와\n모순되지 않는 것", fs=11, c=TEXT2, va="top",
          linespacing=1.25)

    pad = 0.16
    def outside_ok(p):
        in_inner = (IX - pad < p[0] < IX + IW + pad) and (IY - pad < p[1] < IY + IH + pad)
        in_label = p[0] < OX + 3.15 and p[1] > OY + OH - 0.78
        return in_inner or in_label
    out = poisson(rng, N_ALL - N_VS, OX + 0.22, OX + OW - 0.18, OY + 0.2, OY + OH - 0.2, 0.3, outside_ok)
    ins = poisson(rng, N_VS, IX + 0.22, IX + IW - 0.22, IY + 0.22, IY + 0.82, 0.3, lambda p: False)

    ax.scatter(out[:, 0], out[:, 1], s=42, facecolors="white", edgecolors=GRAY, linewidths=1.3, zorder=3)
    pick = int(np.argmax(ins[:, 0]))
    others = np.delete(ins, pick, axis=0)
    ax.scatter(others[:, 0], others[:, 1], s=52, color=PRIMARY, zorder=4)
    chosen = ins[pick]
    ax.scatter([chosen[0]], [chosen[1]], s=120, color=ACCENT, edgecolors=ACCENT_INK, linewidths=1.4, zorder=5)

    # right column: why one is chosen
    rx = 5.85
    label(ax, rx, 3.3, "유한한 training data로는\nversion space가 하나로\n좁혀지지 않습니다", fs=11.5,
          ha="left", va="top", linespacing=1.35)
    label(ax, rx, 2.2, "남은 후보는 training data에서\n모두 똑같이 완벽합니다", fs=11, c=TEXT2,
          ha="left", va="top", linespacing=1.35)

    ax.annotate("", xy=(chosen[0] + 0.13, chosen[1]), xytext=(rx - 0.05, 0.98),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_INK, lw=1.4, shrinkA=0, shrinkB=2,
                                mutation_scale=13, connectionstyle="arc3,rad=0.25"), zorder=6)
    label(ax, rx, 1.12, "inductive bias가", fs=12, w="bold", c=ACCENT_INK, ha="left")
    label(ax, rx, 0.84, "그중 하나를 고름", fs=12, w="bold", c=ACCENT_INK, ha="left")

    # legend
    ly = 0.15
    ax.scatter([0.25], [ly], s=42, facecolors="white", edgecolors=GRAY, linewidths=1.3, zorder=3)
    label(ax, 0.42, ly, "training data와 모순되는 model", fs=11, c=TEXT2, ha="left")
    ax.scatter([3.3], [ly], s=52, color=PRIMARY, zorder=3)
    label(ax, 3.47, ly, "모순되지 않는 model", fs=11, c=TEXT2, ha="left")

    save(fig, os.path.join(OUT, "version_space.png"))


draw()
