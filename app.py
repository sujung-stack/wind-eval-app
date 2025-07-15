
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm

st.set_page_config(layout="centered")
st.title("보행자 풍환경 기준 노모그램")

# 나눔고딕 폰트 설정
font_path = "NanumGothicBold.ttf"  # 로컬 또는 업로드 경로
fontprop = fm.FontProperties(fname=font_path, size=13)
plt.rcParams['font.family'] = fontprop.get_name()

# 색상 코드 정의
colors_nen = ['#0000FF', '#00BFFF', '#00FFFF', '#7CFC00', '#FF0000']
colors_lawson = ['#0000FF', '#00BFFF', '#00FFFF', '#7CFC00', '#FFFF00', '#FFA500', '#FF0000']
colors_murakami = ['#0000FF', '#00BFFF', '#7CFC00', '#FF0000']

# 등급/범위 라벨
def draw_nomogram():
    labels_nen = ['A', 'B', 'C', 'D', 'E']
    ranges_nen = ['<2.5%', '<5%', '<10%', '<20%', '≥20%']
    labels_lawson = ['A', 'B', 'C', 'D', 'E', 'S1', 'S2']
    ranges_lawson = ['4m/s\n(<5%)', '6m/s\n(<5%)', '8m/s\n(<5%)', '10m/s\n(<5%)',
                     '10m/s\n(>5%)', '15m/s\n(>0.023%)', '20m/s\n(>0.023%)']
    labels_murakami = ['1', '2', '3', '4']
    ranges_murakami = ['1.0%', '<1.1%', '<1.5%', '>1.5%']

    bar_width = 0.12
    start_x = [0, 1, 2]
    fig, ax = plt.subplots(figsize=(7, 9))

    def draw_column(x_center, heights, colors, grades, labels):
        bottom = 0
        for h, c, g, l in zip(heights, colors, grades, labels):
            ax.add_patch(patches.Rectangle(
                (x_center - bar_width/2, bottom - 0.001), bar_width, h + 0.002,
                color=c, linewidth=0
            ))
            ax.text(x_center - bar_width/2 - 0.03, bottom + h/2, g,
                    va='center', ha='right', fontproperties=fontprop, fontsize=12)
            ax.text(x_center + bar_width/2 + 0.03, bottom + h/2, l,
                    va='center', ha='left', fontproperties=fontprop, fontsize=11)
            bottom += h

    height_nen = [1/5]*5
    height_lawson = [1/7]*7
    height_murakami = [1/4]*4

    draw_column(start_x[0], height_nen, colors_nen, labels_nen, ranges_nen)
    draw_column(start_x[1], height_lawson, colors_lawson, labels_lawson, ranges_lawson)
    draw_column(start_x[2], height_murakami, colors_murakami, labels_murakami, ranges_murakami)

    # 연결선
    line_x = [start_x[0], start_x[1], start_x[2]]
    line_y = [0.72, 0.67, 0.62]
    ax.plot(line_x, line_y, color='black', linewidth=2)

    # 축 설정
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(0, 1)
    ax.set_xticks(start_x)
    ax.set_xticklabels(['NEN8100 (%)', 'Lawson 2001 (m/s)', 'Murakami (V/V₀)'],
                       fontproperties=fontprop, fontsize=13)
    ax.set_ylabel('Normalization 0–1', fontproperties=fontprop, fontsize=14)
    ax.set_title('Nomogram', fontproperties=fontprop, fontsize=18, weight='bold')

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig

# Streamlit 버튼으로 실행
if st.button("노모그램 생성하기"):
    fig = draw_nomogram()
    st.pyplot(fig)
    st.success("노모그램이 성공적으로 생성되었습니다.")
