# W10 §1.2 Margin의 기하: 분리 초평면 wᵀx+b=0, 양쪽 margin 경계 wᵀx+b=±1, 폭 γ=2/‖w‖, 경계 위의 support vector. 점 배치는 설명용.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w10")

TH = np.deg2rad(30)                                   # direction of w (illustrative)
N = np.array([np.cos(TH), np.sin(TH)])                # unit normal
T = np.array([-np.sin(TH), np.cos(TH)])               # along the hyperplane
M = 1.0                                               # half-width in plot units
O = np.array([0.0, 0.0])


def P(u, v):
    """Point at signed distance u from the hyperplane, v along it."""
    return O + u * N + v * T


# (u, v) positions — illustrative
POS = [(M, -0.9), (M, 1.1), (1.7, 0.2), (2.3, -1.3), (2.0, 1.9), (2.9, 0.6), (3.0, -0.4)]
NEG = [(-M, 0.3), (-1.8, -0.8), (-2.2, 1.0), (-1.6, 2.1), (-2.7, -0.2), (-1.7, -2.6), (-3.0, 1.5)]
SV = [p for p in POS + NEG if abs(abs(p[0]) - M) < 1e-9]

VLIM = 3.0
C_POS, C_NEG = CAT[0], CAT[1]


def line(ax, u, **kw):
    a, b = P(u, -VLIM), P(u, VLIM)
    ax.plot([a[0], b[0]], [a[1], b[1]], **kw)


fig, ax = plt.subplots(figsize=(6.6, 5.0))

line(ax, 0, color=TEXT, lw=2.2, zorder=3)
line(ax, M, color=C_POS, lw=1.5, ls=(0, (5, 3)), zorder=3)
line(ax, -M, color=C_NEG, lw=1.5, ls=(0, (5, 3)), zorder=3)

# margin band
band = np.array([P(-M, -VLIM), P(M, -VLIM), P(M, VLIM), P(-M, VLIM)])
ax.fill(band[:, 0], band[:, 1], color=STEPS[3], zorder=1, lw=0)

for u, v in POS:
    ax.plot(*P(u, v), "o", color=C_POS, ms=10, mec="white", mew=1.2, zorder=5)
for u, v in NEG:
    ax.plot(*P(u, v), "s", color=C_NEG, ms=9.5, mec="white", mew=1.2, zorder=5)
for u, v in SV:
    ax.plot(*P(u, v), "o", ms=21, mfc="none", mec=TEXT, mew=1.6, zorder=6)

# line labels: horizontal, just above the upper end of each line
for u, txt, c, ha in [(-M, r"$\mathbf{w}^{\mathsf{T}}\mathbf{x}+b=-1$", C_NEG, "right"),
                      (0, r"$\mathbf{w}^{\mathsf{T}}\mathbf{x}+b=0$", TEXT, "center"),
                      (M, r"$\mathbf{w}^{\mathsf{T}}\mathbf{x}+b=+1$", C_POS, "left")]:
    p = P(u, VLIM) + np.array([0, 0.12])
    ax.text(*p, txt, fontsize=12, color=c, ha=ha, va="bottom", zorder=7)

# margin width γ — the one must-see quantity
VG = -2.35
a, b = P(-M, VG), P(M, VG)
ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<|-|>", color=ACCENT_INK, lw=1.8,
                                                  mutation_scale=14, shrinkA=0, shrinkB=0), zorder=7)
ax.text(*(P(M, VG) + np.array([0.18, -0.05])), r"$\gamma = 2\,/\,\Vert\mathbf{w}\Vert$", fontsize=14,
        color=ACCENT_INK, ha="left", va="center", zorder=7)

# w direction
w0 = P(0, -1.55)
arrow(ax, *w0, *(w0 + 0.62 * N), color=TEXT, lw=1.6, ms=13, z=6)
ax.text(*(w0 + 0.5 * N + 0.25 * T), r"$\mathbf{w}$", fontsize=13, color=TEXT, ha="center", va="center", zorder=7)

# support vector callout
sv = np.array(P(*SV[1]))
ax.annotate("support vector\n(margin 경계 위의 점)", xy=sv + np.array([0.18, 0.28]), xytext=sv + np.array([0.9, 1.0]),
            fontsize=11.5, color=TEXT, ha="left", va="bottom", linespacing=1.35,
            arrowprops=dict(arrowstyle="-|>", color=TEXT, lw=1.2, shrinkA=2, shrinkB=2,
                            connectionstyle="arc3,rad=0.25"))

# class labels
ax.text(*P(2.7, -2.3), "y = +1", fontsize=12.5, fontweight="bold", color=C_POS, ha="center", va="center")
ax.text(*P(-3.0, -1.0), "y = −1", fontsize=12.5, fontweight="bold", color=C_NEG, ha="center", va="center")

ax.set_aspect("equal")
ax.set_xlim(-3.6, 3.9); ax.set_ylim(-3.0, 3.6)
ax.set_xticks([]); ax.set_yticks([])
for k, sp in ax.spines.items():          # feature-space axes: left and bottom only
    sp.set_visible(k in ("left", "bottom")); sp.set_color("#9AA1AB"); sp.set_zorder(10)
ax.set_xlabel("x₁", fontsize=12, loc="right"); ax.set_ylabel("x₂", fontsize=12, loc="top", rotation=0)
ax.axison = True
save(fig, os.path.join(OUT, "max_margin.png"))
