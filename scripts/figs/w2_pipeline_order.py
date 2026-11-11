# W2 §6.4 올바른 순서: 먼저 분할하고, 결측 대치·scaling·feature selection·재샘플링·모델 학습은 fold 안에서 training fold로만, 평가는 fold 밖에서 변환만 (본문 ASCII 도식을 다시 그림)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w2")

GREY = "#9AA1AB"
STEPS_IN = [("결측 대치", "training fold로만 학습"),
            ("Scaling", "training fold의 평균·표준편차"),
            ("Feature selection", "training fold의 통계량"),
            ("재샘플링(SMOTE)", "training fold에만"),
            ("모델 학습", None)]

fig, ax = new(8.4, 6.2)
bx, bw, bh = 1.0, 2.9, 0.44          # step column
cx = bx + bw / 2

# 전체 데이터 → 분할
y = 5.7
box(ax, bx, y, bw, bh, fc="white", ec=GREY, lw=1.2)
label(ax, cx, y + bh / 2, "전체 데이터", fs=12, w="semibold")
arrow(ax, cx, y - 0.04, cx, 4.98, color=GREY, lw=1.6)
label(ax, cx + 0.2, 5.27, "분할 (train / test, 또는 CV fold)", fs=11.5, w="semibold", ha="left")

# fold 안 영역
iy0, iy1 = 1.6, 4.9
box(ax, 0.3, iy0, 6.75, iy1 - iy0, fc=FAINT, ec=LINE, r=0.12, z=1)
label(ax, 0.48, iy1 - 0.2, "fold 안", fs=11.5, w="semibold", c=TEXT2, ha="left")

cols = ramp(len(STEPS_IN))
ys = [4.28 - i * 0.62 for i in range(len(STEPS_IN))]
for (name, note), c, yy in zip(STEPS_IN, cols, ys):
    box(ax, bx, yy, bw, bh, fc=c, ec="none")
    label(ax, cx, yy + bh / 2, name, fs=12, w="semibold", c=on(c))
    if note:
        arrow(ax, bx + bw + 0.75, yy + bh / 2, bx + bw + 0.12, yy + bh / 2, color=GREY, lw=1.3, ms=10)
        label(ax, bx + bw + 0.88, yy + bh / 2, note, fs=11.5, c=TEXT, ha="left")
for a, b in zip(ys[:-1], ys[1:]):
    arrow(ax, cx, a - 0.02, cx, b + bh + 0.02, color=GREY, lw=1.4, ms=9)

# fold 밖: 평가
arrow(ax, cx, ys[-1] - 0.02, cx, 0.55 + bh + 0.04, color=GREY, lw=1.6)
label(ax, 0.48, 1.22, "fold 밖", fs=11.5, w="semibold", c=TEXT2, ha="left")
ey = 0.55
box(ax, bx, ey, bw, bh, fc="white", ec=PRIMARY, lw=1.4)
label(ax, cx, ey + bh / 2, "평가", fs=12, w="semibold", c=PRIMARY)
label(ax, bx + bw + 0.2, ey + bh / 2 + 0.13, "test fold는 변환만 적용", fs=11.5, c=TEXT, ha="left")
label(ax, bx + bw + 0.2, ey + bh / 2 - 0.15, "재학습 금지", fs=11.5, w="bold", c=ACCENT_INK, ha="left")

save(fig, os.path.join(OUT, "pipeline_order.png"))
