# 🌬️ 풍환경 종합 안전평가 시스템 (Streamlit 기반)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("🌬️ 풍환경 종합 안전평가 시스템")
st.markdown("""
CSV 파일을 업로드하면, 각 지점별 **Lawson / NEN8100 / Murakami 기준 등급**, 
그리고 종합 안전성 평가를 자동으로 수행하고, 노모그램으로 시각화합니다.
""")

uploaded_file = st.file_uploader("CSV 파일 업로드 (예: data.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def classify_lawson(v):
        if v < 4: return "A"
        elif v < 6: return "B"
        elif v < 8: return "C"
        elif v < 10: return "D"
        elif v < 15: return "E"
        elif v < 20: return "S"
        else: return "S+"

    def classify_nen(p):
        if p < 2.5: return "A"
        elif p < 5: return "B"
        elif p < 10: return "C"
        elif p < 20: return "D"
        else: return "E"

    def classify_murakami(r):
        if r < 0.15: return "1"
        elif r < 0.3: return "2"
        elif r < 0.5: return "3"
        else: return "4"

    def evaluate_safety(l, n, m):
        danger_count = sum([l in ["E", "S", "S+"], n in ["D", "E"], m in ["3", "4"]])
        if danger_count >= 2:
            return "위험"
        elif danger_count == 1:
            return "주의"
        else:
            return "안전"

    # 등급 및 평가 계산
    results = []
    for _, row in df.iterrows():
        lawson = classify_lawson(row["풍속 (m/s)"])
        nen = classify_nen(row["초과확률 (%)"])
        murakami = classify_murakami(row["풍속비 (V/Vref)"])
        safety = evaluate_safety(lawson, nen, murakami)
        results.append((row["지점"], lawson, nen, murakami, safety))

    # 표 출력
    st.subheader("📋 평가 결과 요약")
    result_df = pd.DataFrame(results, columns=["지점", "Lawson 등급", "NEN8100 등급", "Murakami 등급", "종합 평가"])
    st.dataframe(result_df)

    # 노모그램 시각화
    st.subheader("📈 노모그램 시각화")
    fig, ax = plt.subplots(figsize=(10, 6))
    y_levels = {"A": 0.9, "B": 0.75, "C": 0.6, "D": 0.45, "E": 0.3, "S": 0.15, "S+": 0.05,
                "1": 0.85, "2": 0.6, "3": 0.35, "4": 0.1}

    for i, (point, lawson, nen, murakami, safety) in enumerate(results):
        x_vals = [0.1, 0.5, 0.9]
        y_vals = [y_levels[lawson], y_levels[nen], y_levels[murakami]]
        ax.plot(x_vals, y_vals, marker="o", linestyle="--", label=f"{point} ({safety})")

    ax.text(0.1, 1.02, "Lawson", ha='center', fontsize=12, weight='bold')
    ax.text(0.5, 1.02, "NEN8100", ha='center', fontsize=12, weight='bold')
    ax.text(0.9, 1.02, "Murakami", ha='center', fontsize=12, weight='bold')
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.05)
    ax.axis('off')
    ax.legend()
    st.pyplot(fig)

    # 평가 결과 다운로드 옵션
    st.download_button("📥 결과 CSV 다운로드", result_df.to_csv(index=False).encode('utf-8-sig'), file_name="평가결과.csv", mime="text/csv")
else:
    st.info("왼쪽 사이드바 또는 위에서 CSV 파일을 업로드해주세요.")
