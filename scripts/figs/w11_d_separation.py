# W11 §6.3 d-분리: 선형·분기에서는 b를 알면 a–c 경로가 닫히고, 합류에서는 거꾸로 열린다 (본문 표를 그림으로)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *
import matplotlib.patches as mp

OUT = os.environ.get("FIG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w11"))

L = {
    "ko": dict(panels=["① 선형 (머리-꼬리)", "② 분기 (꼬리-꼬리)", "③ 합류 (머리-머리)"],
               closed="b를 알면 폐쇄", open="b를 알면 개방",
               indep="a ⊥ c | b", dep="원래 독립이던 a, c가 의존하게 됨",
               legend="색칠한 node = 값을 아는 변수 (조건으로 둔 변수)"),
}

# edge directions per panel: +1 means left→right, -1 means right→left, for (a–b, b–c)
DIRS = [(+1, +1), (-1, +1), (+1, -1)]
R = 0.27
EDGE = "#6B7280"


def node(ax, x, y, name, known):
    ax.add_patch(mp.Circle((x, y), R, fc=PRIMARY if known else "white",
                           ec=PRIMARY if known else "#9AA1AB", lw=1.6, zorder=4))
    label(ax, x, y, name, fs=14, w="semibold", c="white" if known else TEXT, z=6)


def edge(ax, x1, x2, y, d):
    a, b = (x1 + R + 0.04, x2 - R - 0.06) if d > 0 else (x2 - R - 0.04, x1 + R + 0.06)
    arrow(ax, a, y, b, y, color=EDGE, lw=1.8, ms=14)


def draw(lang):
    t = L[lang]
    fig, ax = new(8.4, 2.95)
    pw = 2.8
    for i in range(3):
        x0 = i * pw
        cx = x0 + pw / 2
        label(ax, cx, 2.6, t["panels"][i], fs=12, w="semibold", c=TEXT)
        xs = [cx - 0.95, cx, cx + 0.95]
        y = 1.85
        for xx, nm in zip(xs, "abc"):
            node(ax, xx, y, nm, nm == "b")
        edge(ax, xs[0], xs[1], y, DIRS[i][0])
        edge(ax, xs[1], xs[2], y, DIRS[i][1])
        if i < 2:
            label(ax, cx, 1.18, t["closed"], fs=11.5, w="bold", c=TEXT)
            label(ax, cx, 0.86, t["indep"], fs=12, c=TEXT2)
        else:   # the one exception the text warns about
            pill(ax, cx, 1.18, t["open"], fc=ACCENT, tc=ON_ACCENT, fs=11.5, h=0.34)
            label(ax, cx, 0.86, t["dep"], fs=11.5, w="semibold", c=ACCENT_INK)
        if i < 2:
            ax.plot([x0 + pw, x0 + pw], [0.75, 2.75], color=LINE, lw=1, zorder=1)
    # legend
    ax.add_patch(mp.Circle((0.2, 0.28), 0.11, fc=PRIMARY, ec=PRIMARY, zorder=4))
    label(ax, 0.4, 0.28, t["legend"], fs=11, c=TEXT2, ha="left")
    save(fig, os.path.join(OUT, "d_separation" + ".png"))


for lang in L:
    draw(lang)
