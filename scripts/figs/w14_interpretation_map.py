# W14 §1.2 해석의 분류: global/local × model-specific/model-agnostic 2×2 지도에 이 장의 방법을 배치 (ICE 평균 = PDP, SHAP 평균 = 전역 요약)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.environ.get("FIG_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w14"))

L = {
    "ko": dict(
        cols=[("Model-specific", "모델 내부를 씀"), ("Model-agnostic", "predict()만 있으면 됨")],
        rows=[("Global", "모델 전체가\n무엇에 기대는가"), ("Local", "이 한 예측은\n왜 이렇게 나왔나")],
        mdi=("불순도 감소 (MDI)", "트리 split마다 줄어든\n불순도의 합 · 학습 데이터"),
        perm=("Permutation importance", "test에서 변수 하나를 섞을 때 성능 감소"),
        pdp=("PDP", "값을 고정한 뒤\n평균 예측"),
        mshap=("평균 |SHAP|", "여러 환자의\nSHAP 요약"),
        ice=("ICE", "환자 한 명당\n곡선 하나"),
        shap=("SHAP", "한 예측을\nfeature별 기여로"),
        avg="평균",
        none="이 장에서 다루지 않음",
    ),
}

C_MDI, C_PERM, C_PDP, C_SHAP = shade(CAT[3], 0.3), CAT[0], CAT[1], CAT[2]
GREY = "#9AA1AB"


def item(ax, x, y, w, h, name, note, c):
    box(ax, x, y, w, h, fc="white", ec=mix(c, 0.55), lw=1.4, r=0.08, z=3)
    box(ax, x, y + 0.1, 0.07, h - 0.2, fc=c, ec="none", r=0.03, z=4)
    label(ax, x + 0.2, y + h - 0.24, name, fs=12, w="bold", c=c, ha="left")
    label(ax, x + 0.2, y + h - 0.44, note, fs=11, c=TEXT2, ha="left", va="top", linespacing=1.3)


def draw(lang):
    t = L[lang]
    fig, ax = new(8.4, 5.0)

    # grid geometry
    hx, cx = [0.0, 1.55], [(1.65, 2.75), (4.5, 3.85)]          # (x, w) for each column
    ry = [(1.85, 2.3), (0.2, 1.45)]                            # (y, h) for global, local rows
    for (x, w) in cx:
        for (y, h) in ry:
            box(ax, x, y, w, h, fc=FAINT, ec="none", r=0.1, z=1)

    # column headers
    for i, ((x, w), (en, ko)) in enumerate(zip(cx, t["cols"])):
        label(ax, x + w / 2, 4.78, en, fs=13, w="bold", c=TEXT)
        if i == 1:   # the one must-see point: every method in this chapter only needs predict()
            pill(ax, x + w / 2, 4.42, ko, fc=ACCENT, tc=ON_ACCENT, fs=11, h=0.32)
        else:
            label(ax, x + w / 2, 4.42, ko, fs=11, c=TEXT2)

    # row headers
    for (y, h), (en, ko) in zip(ry, t["rows"]):
        label(ax, 0.05, y + h - 0.3, en, fs=13, w="bold", ha="left")
        label(ax, 0.05, y + h - 0.58, ko, fs=11, c=TEXT2, ha="left", va="top", linespacing=1.3)

    # global × specific
    x, w = cx[0]
    item(ax, x + 0.15, 3.0, w - 0.3, 1.0, *t["mdi"], C_MDI)
    # local × specific
    label(ax, x + w / 2, ry[1][0] + ry[1][1] / 2, t["none"], fs=11, c=TEXT2)

    # model-agnostic column
    x, w = cx[1]
    iw = (w - 0.45) / 2
    xl, xr = x + 0.15, x + 0.3 + iw
    item(ax, xl, 3.25, w - 0.3, 0.75, t["perm"][0], "", C_PERM)
    label(ax, xl + 0.2, 3.25 + 0.2, t["perm"][1], fs=11, c=TEXT2, ha="left", va="center")
    for (nm, note), c, xx in [(t["pdp"], C_PDP, xl), (t["mshap"], C_SHAP, xr)]:
        item(ax, xx, 2.05, iw, 1.0, nm, note, c)
    for (nm, note), c, xx in [(t["ice"], C_PDP, xl), (t["shap"], C_SHAP, xr)]:
        item(ax, xx, 0.4, iw, 1.0, nm, note, c)
        arrow(ax, xx + iw / 2, 1.42, xx + iw / 2, 2.03, color=GREY, lw=1.5, ms=11, z=5)
        label(ax, xx + iw / 2 + 0.1, 1.74, t["avg"], fs=11, c=TEXT2, ha="left")

    save(fig, os.path.join(OUT, "interpretation_map" + ".png"))


for lang in L:
    draw(lang)
