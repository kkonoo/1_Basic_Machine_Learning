# W3 §6.3 Nested CV: 바깥 fold 하나를 빼 두고, 남은 데이터 안에서만 CV로 설정을 고른 뒤, 빼 둔 fold로 평가
# (본문의 ASCII 도식을 다시 그림. fold 수는 §6.4 실습과 같은 바깥 5 · 안쪽 5)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.environ.get("FIG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w3"))

L = {
    "ko": dict(outer="바깥 fold {k}", leg=["바깥 test fold", "안쪽 검증 fold", "학습에 쓰는 데이터"],
               inner="안쪽 루프 (하이퍼파라미터 선택)", inner2="남은 데이터만으로 CV",
               best="최적 설정", fit="선택한 설정으로 학습", ev="fold 1에서 평가",
               score="점수 {k}", same="같은 과정", avg="점수 1–5의 평균 = 정직한 추정",
               never="튜닝에 한 번도\n쓰지 않음"),
}

TEST, VAL, TRAIN = CAT[0], CAT[2], STEPS[2]
GREY = "#9AA1AB"


def bar(ax, x, y, n, seg_w, h, special, fc_special, gap=0.04):
    for i in range(n):
        fc = fc_special if i == special else TRAIN
        box(ax, x + i * seg_w + gap / 2, y, seg_w - gap, h, fc=fc, ec="none", r=0.05)


def draw(lang):
    t = L[lang]
    fig, ax = new(8.4, 5.45)

    # legend (top row)
    lx = 0.05
    for c, s in zip([TEST, VAL, TRAIN], t["leg"]):
        box(ax, lx, 5.12, 0.26, 0.2, fc=c, ec="none", r=0.04)
        tt = label(ax, lx + 0.36, 5.22, s, fs=11, c=TEXT2, ha="left")
        fig.canvas.draw()
        lx += 0.36 + tt.get_window_extent().width / fig.dpi + 0.4

    # outer folds: rows 1, 2, …, 5 (row k holds out fold k)
    seg, h, bx = 0.56, 0.42, 1.5
    rows = {1: 3.85, 2: 1.95, 5: 0.95}
    for k, y in rows.items():
        label(ax, 0.05, y + h / 2, t["outer"].format(k=k), fs=11.5, w="semibold", ha="left")
        bar(ax, bx, y, 5, seg, h, k - 1, TEST)
    label(ax, bx + 2.5 * seg, 1.62, "⋮", fs=14, c=TEXT2)

    # the one must-see point: the held-out fold never enters tuning
    cx = bx + seg / 2
    label(ax, cx, 3.3, t["never"], fs=11, w="bold", c=ACCENT_INK, va="top", linespacing=1.3)
    arrow(ax, cx, 3.34, cx, 3.8, color=ACCENT_INK, lw=1.4, ms=10)

    # inner loop for outer fold 1: the four training blocks are re-split into 5 inner folds
    px, py, pw, ph = 4.55, 3.3, 3.8, 1.62
    box(ax, px, py, pw, ph, fc=FAINT, ec=LINE, r=0.1, z=1)
    label(ax, px + 0.15, py + ph - 0.22, t["inner"], fs=11.5, w="semibold", ha="left")
    label(ax, px + 0.15, py + ph - 0.5, t["inner2"], fs=11, c=TEXT2, ha="left")
    arrow(ax, bx + 5 * seg + 0.08, rows[1] + h / 2, px - 0.06, rows[1] + h / 2, color=GREY, lw=1.4, ms=10)
    iseg, ih = 0.26, 0.13
    for j in range(5):
        yy = py + 0.86 - j * 0.18
        bar(ax, px + 0.18, yy, 5, iseg, ih, j, VAL, gap=0.03)
    ix = px + 0.18 + 5 * iseg + 0.12
    arrow(ax, ix, py + 0.57, ix + 0.35, py + 0.57, color=GREY, lw=1.4, ms=10)
    pill(ax, ix + 0.43, py + 0.57, t["best"], fc=VAL, fs=11, ha="left")

    # after the inner loop: train with the chosen setting, score on fold 1
    sx = 7.8                                   # score column
    arrow(ax, px + 0.3, py - 0.05, px + 0.3, 2.68, color=GREY, lw=1.4, ms=10)
    label(ax, px + 0.45, 3.0, t["fit"], fs=11, ha="left")
    label(ax, px + 0.45, 2.73, t["ev"], fs=11, ha="left")
    arrow(ax, sx - 0.75, 2.86, sx - 0.42, 2.86, color=GREY, lw=1.4, ms=10)
    pill(ax, sx, 2.86, t["score"].format(k=1), fc=mix(TEST, 0.14), tc=TEST, fs=11)
    for k in (2, 5):
        yc = rows[k] + h / 2
        label(ax, px + 0.45, yc, t["same"], fs=11, c=TEXT2, ha="left")
        arrow(ax, sx - 0.75, yc, sx - 0.42, yc, color=GREY, lw=1.4, ms=10)
        pill(ax, sx, yc, t["score"].format(k=k), fc=mix(TEST, 0.14), tc=TEST, fs=11)
    label(ax, sx, 1.62, "⋮", fs=14, c=TEXT2)

    # mean of the outer scores
    yb = 0.3
    arrow(ax, sx, rows[5] + h / 2 - 0.17, sx, yb + 0.21, color=GREY, lw=1.4, ms=10)
    pill(ax, sx - 1.25, yb, t["avg"], fc=PRIMARY, fs=12, h=0.38, ha="center")
    save(fig, os.path.join(OUT, "nested_cv" + ".png"))


for lang in L:
    draw(lang)
