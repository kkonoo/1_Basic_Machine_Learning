# W13 §10.2 오믹스 데이터에서의 표준 흐름: 정규화·유전자 선택 → PCA → PC 공간에서 군집화·kNN → t-SNE/UMAP은 시각화만 → 해석
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w13")

STEPS5 = [
    ("정규화 · 유전자 선택", "정규화 + log 변환 → 변동이 큰 유전자 선택 (W2)"),
    ("PCA", "parallel analysis 등으로 잡음 위의 PC만 (보통 10~50개)"),
    ("군집화 · kNN 그래프", "그 PC 공간에서 (군집화는 W12)"),
    ("t-SNE / UMAP", "시각화만"),
    ("해석", "필요하면 PCA loading, NMF 프로그램, 또는 군집별 marker"),
]

fig, ax = new(8.4, 4.3)
cols = ramp(len(STEPS5))
bx, bw, bh, pitch = 0.5, 2.45, 0.56, 0.86
top = 4.3 - 0.1
for i, ((name, desc), c) in enumerate(zip(STEPS5, cols)):
    y = top - i * pitch - bh
    yc = y + bh / 2
    num(ax, 0.18, yc, i + 1, fc=c)
    box(ax, bx, y, bw, bh, fc=c, ec="none", r=0.08)
    label(ax, bx + bw / 2, yc, name, fs=12.5, w="bold", c=on(c))
    dx = bx + bw + 0.25
    if i == 3:
        # t-SNE/UMAP 결과로 생물학적 주장을 하지 않는다 (본문 경고 상자)
        t = label(ax, dx, yc, desc, fs=12, w="bold", c=TEXT, ha="left")
        fig.canvas.draw()
        dx2 = dx + t.get_window_extent().width / fig.dpi + 0.18
        label(ax, dx2, yc, "군집 크기·거리·배치로 주장하지 않음", fs=11.5, w="semibold",
              c=ACCENT_INK, ha="left")
    else:
        label(ax, dx, yc, desc, fs=11.5, c=TEXT2, ha="left")
    if i < len(STEPS5) - 1:
        arrow(ax, bx + bw / 2, y - 0.03, bx + bw / 2, y - (pitch - bh) + 0.03,
              color="#9AA1AB", lw=1.5, ms=11)

save(fig, os.path.join(OUT, "omics_flow.png"))
