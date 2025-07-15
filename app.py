import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🌪️ 풍환경 종합 안전평가 시스템")
st.markdown("""
CSV 파일을 업로드하면 각 지점별 **Lawson / NEN8100 / Murakami** 등급과 종합평가를 수행하고 노모그램 위에 시각화합니다.
""")

uploaded_file = st.file_uploader("CSV 파일 업로드 (예: 지점, 풍속, 초과확률, 풍속비)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 등급 기준 정의
    lawson_bins = [0, 4, 6, 8, 10, 15, 20]
    lawson_labels = ['A', 'B', 'C', 'D', 'E', 'E']
    
    nen8100_bins = [0, 2.5, 5, 10, 20, 100]
    nen8100_labels = ['A', 'B', 'C', 'D', 'E']
    
    murakami_bins = [0, 1.0, 1.1, 1.5, 100]
    murakami_labels = ['1', '2', '3', '4']

    # 등급 계산
    df['Lawson 등급'] = pd.cut(df['풍속'], bins=lawson_bins, labels=lawson_labels, right=False)
    df['NEN8100 등급'] = pd.cut(df['초과확률'], bins=nen8100_bins, labels=nen8100_labels, right=False)
    df['Murakami 등급'] = pd.cut(df['풍속비'], bins=murakami_bins, labels=murakami_labels, right=False)

    # 종합 평가
    df['종합 평가'] = df.apply(
        lambda row: '위험' if 'E' in [row['Lawson 등급'], row['NEN8100 등급']] or row['Murakami 등급'] == '4' else '양호',
        axis=1
    )

    st.dataframe(df)

    # 정규화 함수
    def normalize(series, min_val, max_val):
        return (series - min_val) / (max_val - min_val)

    # 정규화된 위치 계산
    lawson_y = normalize(df['풍속'], 4, 20)
    nen8100_y = normalize(df['초과확률'], 0, 20)
    murakami_y = normalize(df['풍속비'], 1.0, 1.5)

    # 시각화
    st.markdown("### 🧭 노모그램 시각화")

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["NEN8100 (%)", "Lawson 2001 (m/s)", "Murakami (V/V⃞)"])
    ax.set_ylabel("Normalization 0-1")
    ax.set_title("Nomogram")

    # 등급 영역 색상 표시 (Lawson 예시로 모두 동일 스타일 적용)
    color_bands = {
        "Lawson": ([0, 4, 6, 8, 10, 15, 20], ['blue', 'dodgerblue', 'cyan', 'yellowgreen', 'orange', 'red']),
        "NEN8100": ([0, 2.5, 5, 10, 20], ['blue', 'skyblue', 'lightgreen', 'orange', 'red']),
        "Murakami": ([0, 1.0, 1.1, 1.5, 2.0], ['blue', 'lightblue', 'yellowgreen', 'red'])
    }

    def draw_band(x_pos, bins, colors):
        for i in range(len(colors)):
            y0 = (bins[i] - bins[0]) / (bins[-1] - bins[0])
            y1 = (bins[i+1] - bins[0]) / (bins[-1] - bins[0])
            ax.fill_betweenx([y0, y1], x_pos - 0.4, x_pos + 0.4, color=colors[i])

    draw_band(0, *color_bands["NEN8100"])
    draw_band(1, *color_bands["Lawson"])
    draw_band(2, *color_bands["Murakami"])

    # 각 지점 위치에 점선 추가
    for y1, y2, y3 in zip(nen8100_y, lawson_y, murakami_y):
        ax.hlines(y=y1, xmin=-0.4, xmax=+0.4, linestyles='dashed', colors='black', linewidth=1)
        ax.hlines(y=y2, xmin=0.6, xmax=1.4, linestyles='dashed', colors='black', linewidth=1)
        ax.hlines(y=y3, xmin=1.6, xmax=2.4, linestyles='dashed', colors='black', linewidth=1)

    st.pyplot(fig, use_container_width=True)

    # 결과 저장
    st.download_button("📥 결과 CSV 다운로드", df.to_csv(index=False).encode('utf-8-sig'), "result.csv", "text/csv")

else:
    st.info("예시 CSV 파일을 업로드하면 등급 분류 및 노모그램 시각화가 수행됩니다.")
