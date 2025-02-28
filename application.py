import streamlit as st
import json
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="지원서 요약 확인",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 최소한의 커스텀 CSS 적용
st.markdown(
    """
<style>
    .info-highlight {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0d6efd;
        color: #212529;
        font-size: 16px;
        margin: 10px 0;
    }
    
    .applicant-card {
        background-color: white;
        color: black;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    
    .applicant-card:hover {
        transform: translateY(-5px);
    }
    
    .summary-header {
        color: #0d6efd;
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 10px;
    }
    
    .tag {
        background-color: #e7f0fd;
        color: #0d6efd;
        padding: 3px 8px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 5px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 데이터 로드
@st.cache_data
def load_data():
    with open("evaluation_results_enhanced_ver2.json", "r", encoding="utf-8") as f:
        return json.load(f)


evaluation_results = load_data()


# Lottie 애니메이션 로드
@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_search = load_lottie_url(
    "https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json"
)
lottie_document = load_lottie_url(
    "https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json"
)

# 사이드바 메뉴
with st.sidebar:
    st.image(
        "https://www.yonsei.ac.kr/_res/yonsei/img/intro/img_symbol01.png", width=100
    )
    st.title("연세대학교 BIT")

    selected = option_menu(
        menu_title="메뉴",
        options=["홈", "전체 지원자 보기", "지원자 검색"],
        icons=["house", "list-ul", "search"],
        menu_icon="cast",
        default_index=0,
    )

    st.divider()
    st.subheader("📊 통계")

    # 간단한 통계 계산
    total_applicants = len(evaluation_results)

    # 성별 통계
    gender_counts = {"남": 0, "여": 0}
    for applicant in evaluation_results:
        gender = applicant["user_sex"]
        gender_counts[gender] = gender_counts.get(gender, 0) + 1

    # 통계 시각화
    fig = px.pie(
        values=list(gender_counts.values()),
        names=list(gender_counts.keys()),
        title="성별 분포",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4,
    )
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

    # 지원자 수 표시
    st.metric("총 지원자 수", f"{total_applicants}명")


# 평가 항목 정의
@st.cache_data
def get_evaluation_criteria():
    return {
        "지원 동기 및 진정성": {
            "description": "지원 동기란에서 확인할 수 있는 goal-alignment에 대한 평가",
            "criteria": {
                "A": "높은 목표의식, BIT와 본인의 목표가 명확하게 연계됨 (상위 7%)",
                "B": "적절한 목표의식, 일반적인 연계성 (약 53%)",
                "C": "불명확한 목표의식 또는 연계성 부족 (약 40%)",
            },
            "color": "#047857",
        },
        "논리적 표현력": {
            "description": "글이 논리적인 흐름으로 작성되어 읽기 편한지에 대한 평가",
            "criteria": {
                "A": "명확하고 논리적인 표현, 우수한 구성력 (상위 7%)",
                "B": "적절한 논리성과 표현력 (약 53%)",
                "C": "논리적 흐름 부족 또는 이해가 어려운 표현 (약 40%)",
            },
            "color": "#CA8A04",
        },
        "활동경험": {
            "description": "높은 목표의식과 발전적 태도를 짐작할 수 있는 활동 이력 평가",
            "criteria": {
                "G": "특출나고 특별한 경험을 보유 (상위 3%)",
                "NP": "일반적인 활동 경험 (약 97%)",
            },
            "color": "#0369A1",
        },
        "성실성(성의)": {
            "description": "제출 기한 및 기본 양식 준수, GPT 사용 여부, 오탈자 등 평가",
            "criteria": {"P": "성실하게 작성됨", "NP": "성실성 부족"},
            "color": "#7C3AED",
        },
    }


evaluation_criteria = get_evaluation_criteria()

# 홈 페이지
if selected == "홈":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("지원서 요약 확인 시스템")

        # 시스템 안내 카드 스타일 적용
        st.markdown(
            """
        <div class="applicant-card text-black">
            <h3>👋 환영합니다</h3>
            <p>이 시스템은 연세대학교 BIT 지원자들의 지원서 요약을 확인할 수 있는 대시보드입니다.</p>
            <p>사이드바의 메뉴를 통해 다양한 기능을 이용해보세요:</p>
            <ul>
                <li><b>전체 지원자 보기</b>: 모든 지원자의 기본 정보와 지원서 요약을 확인합니다.</li>
                <li><b>지원자 검색</b>: 특정 지원자의 이름으로 검색하여 상세 정보를 확인합니다.</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # 기본 통계
        st.subheader("지원자 통계")
        col_stat1, col_stat2 = st.columns(2)

        # 성별 분포
        with col_stat1:
            st.metric("남성 지원자", f"{gender_counts['남']}명")
            st.metric("여성 지원자", f"{gender_counts['여']}명")

        # 연령대 통계 (생년월일 기반)
        with col_stat2:
            # 생년월일 기반 나이 계산
            import datetime

            current_year = datetime.datetime.now().year

            age_groups = {
                "20대 초반": 0,
                "20대 중반": 0,
                "20대 후반": 0,
                "30대 이상": 0,
            }

            for applicant in evaluation_results:
                try:
                    birth_year = int(applicant["user_birth"].split("-")[0])
                    age = current_year - birth_year

                    if age < 23:
                        age_groups["20대 초반"] += 1
                    elif age < 27:
                        age_groups["20대 중반"] += 1
                    elif age < 30:
                        age_groups["20대 후반"] += 1
                    else:
                        age_groups["30대 이상"] += 1
                except:
                    pass

            # 연령 분포 시각화 - 개선된 디자인
            age_df = pd.DataFrame(
                {"연령대": list(age_groups.keys()), "인원수": list(age_groups.values())}
            )

            # 색상 팔레트 개선
            color_scale = px.colors.qualitative.Pastel1

            fig = px.bar(
                age_df,
                x="연령대",
                y="인원수",
                text="인원수",
                title="연령대별 지원자 분포",
                color="연령대",
                color_discrete_sequence=color_scale,
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="지원자 수",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor="rgba(0,0,0,0.1)"),
            )

            fig.update_traces(textposition="outside")

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st_lottie(lottie_document, height=300, key="document")

        # 빠른 검색 기능 - 카드 디자인 적용
        st.markdown(
            '<div class="summary-header">빠른 검색</div>', unsafe_allow_html=True
        )
        quick_search = st.text_input(
            "지원자 이름 입력", key="quick_search", placeholder="이름을 입력하세요"
        )
        if st.button("검색", key="quick_search_button", use_container_width=True):
            if quick_search:
                # 세션 스테이트에 검색어 저장하고 검색 페이지로 이동
                st.session_state.search_name = quick_search
                st.session_state.page = "지원자 검색"
                st.experimental_rerun()

# 전체 지원자 보기
elif selected == "전체 지원자 보기":
    st.title("전체 지원자 정보")

    # 필터링 옵션
    col_filter1, col_filter2 = st.columns([1, 3])

    with col_filter1:
        gender_filter = st.selectbox("성별 필터", ["전체", "남", "여"])

    with col_filter2:
        name_filter = st.text_input("이름 검색", placeholder="이름으로 검색...")

    # 데이터프레임 생성을 위한 데이터 준비
    applicant_data = []
    filtered_applicants = []

    for applicant in evaluation_results:
        name = applicant["user_name"]
        sex = applicant["user_sex"]
        birth = applicant["user_birth"]

        # 필터링 적용
        if (gender_filter == "전체" or sex == gender_filter) and (
            not name_filter or name_filter.lower() in name.lower()
        ):

            # 문항 개수 확인
            problem_count = len(applicant["summarization"])

            applicant_data.append(
                {"이름": name, "성별": sex, "생년월일": birth, "문항 수": problem_count}
            )

            filtered_applicants.append(applicant)

    # 검색 결과 메시지
    if name_filter or gender_filter != "전체":
        st.info(f"검색 결과: {len(filtered_applicants)}명의 지원자를 찾았습니다.")

    df = pd.DataFrame(applicant_data)

    # 데이터프레임 표시 - 깔끔한 형태로
    st.dataframe(
        df,
        use_container_width=True,
        height=250,
        column_config={
            "이름": st.column_config.TextColumn("이름", width="medium"),
            "성별": st.column_config.TextColumn("성별", width="small"),
            "생년월일": st.column_config.TextColumn("생년월일", width="medium"),
            "문항 수": st.column_config.NumberColumn(
                "문항 수", help="지원서 문항 개수", width="small"
            ),
        },
    )

    # 각 지원자별 상세 요약 정보 - Expander 사용
    st.markdown("### 지원자 상세 정보")

    # 추가 필터 및 정렬 옵션
    col_sort1, col_sort2 = st.columns(2)
    with col_sort1:
        sort_option = st.selectbox("정렬 기준", ["이름", "생년월일"])
    with col_sort2:
        sort_order = st.radio("정렬 순서", ["오름차순", "내림차순"], horizontal=True)

    # 정렬 적용
    if sort_option == "이름":
        filtered_applicants.sort(
            key=lambda x: x["user_name"], reverse=(sort_order == "내림차순")
        )
    else:
        filtered_applicants.sort(
            key=lambda x: x["user_birth"], reverse=(sort_order == "내림차순")
        )

    # Expander로 각 지원자 정보 표시
    for i, applicant in enumerate(filtered_applicants):
        with st.expander(
            f"📄 {applicant['user_name']} ({applicant['user_sex']}, {applicant['user_birth']})"
        ):
            col1, col2 = st.columns([1, 2])

            with col1:
                # 지원자 기본 정보 카드
                st.markdown(
                    f"""
                <div class="applicant-card">
                    <h4>{applicant['user_name']}</h4>
                    <p><span class="tag">{applicant['user_sex']}</span> <span class="tag">{applicant['user_birth']}</span></p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # 추가 정보 표시 (있을 경우)
                if "user_email" in applicant:
                    st.write(f"**이메일:** {applicant['user_email']}")
                if "user_phone" in applicant:
                    st.write(f"**연락처:** {applicant['user_phone']}")

            with col2:
                # 요약 정보 탭으로 구성
                if len(applicant["summarization"]) > 0:
                    sum_tabs = st.tabs(
                        [f"문항 {i+1}" for i in range(len(applicant["summarization"]))]
                    )

                    for i, (problem, summary) in enumerate(
                        applicant["summarization"].items()
                    ):
                        with sum_tabs[i]:
                            st.markdown(
                                f'<div class="summary-header">{problem}</div>',
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f'<div class="info-highlight">{summary}</div>',
                                unsafe_allow_html=True,
                            )
                else:
                    st.info("요약된 지원서 정보가 없습니다.")

# 지원자 검색
elif selected == "지원자 검색":
    st.title("지원자 검색")

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.container():
            st.info("지원자의 이름을 입력하여 상세 정보를 확인하세요.")

        # 세션에서 검색어 가져오기
        search_default = ""
        if hasattr(st.session_state, "search_name"):
            search_default = st.session_state.search_name
            # 사용 후 세션에서 제거
            del st.session_state.search_name

        search_name = st.text_input(
            "지원자 이름", value=search_default, placeholder="예: 홍길동"
        )

        if search_name:
            found = False
            matched_applicants = []

            for applicant in evaluation_results:
                if search_name in applicant["user_name"]:
                    found = True
                    matched_applicants.append(applicant)

            if found:
                st.success(
                    f"'{search_name}' 검색 결과: {len(matched_applicants)}명의 지원자를 찾았습니다!"
                )

                if len(matched_applicants) > 1:
                    # 여러 지원자가 검색된 경우, 선택할 수 있게 함
                    selected_name = st.selectbox(
                        "확인할 지원자를 선택하세요",
                        [
                            f"{a['user_name']} ({a['user_birth']})"
                            for a in matched_applicants
                        ],
                    )

                    # 선택된 지원자 정보 가져오기
                    selected_applicant = None
                    for applicant in matched_applicants:
                        if (
                            f"{applicant['user_name']} ({applicant['user_birth']})"
                            == selected_name
                        ):
                            selected_applicant = applicant
                            break
                else:
                    # 한 명의 지원자만 검색된 경우
                    selected_applicant = matched_applicants[0]

                # 선택된 지원자 정보 표시
                if selected_applicant:
                    st.divider()

                    # 지원자 정보를 카드 형태로 표시
                    st.markdown(
                        f"""
                    <div class="applicant-card">
                        <h2>{selected_applicant['user_name']}</h2>
                        <p>
                            <span class="tag">{selected_applicant['user_sex']}</span>
                            <span class="tag">{selected_applicant['user_birth']}</span>
                        </p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # 지원서 요약 정보 표시
                    st.markdown("### 지원서 요약")

                    # 각 문항별 요약 정보
                    tabs = st.tabs(
                        [
                            f"문항 {i+1}"
                            for i in range(len(selected_applicant["summarization"]))
                        ]
                    )

                    for i, (problem, summary) in enumerate(
                        selected_applicant["summarization"].items()
                    ):
                        with tabs[i]:
                            st.markdown(
                                f'<div class="summary-header">{problem}</div>',
                                unsafe_allow_html=True,
                            )

                            # 요약 텍스트를 하이라이트된 박스에 표시 - 검은색 텍스트로 가독성 향상
                            st.markdown(
                                f'<div class="info-highlight">{summary}</div>',
                                unsafe_allow_html=True,
                            )

                            # 워드 클라우드 또는 텍스트 분석 추가 (선택적)
                            if st.checkbox("텍스트 분석 보기", key=f"analysis_{i}"):
                                # 간단한 텍스트 분석 - 단어 빈도
                                from collections import Counter
                                import re

                                # 불용어 정의
                                stopwords = [
                                    "있는",
                                    "하는",
                                    "그리고",
                                    "그런",
                                    "이런",
                                    "저는",
                                    "이것",
                                    "정도",
                                ]

                                # 텍스트 전처리 및 단어 추출
                                words = re.findall(r"\w+", summary)
                                words = [
                                    w
                                    for w in words
                                    if len(w) > 1 and w not in stopwords
                                ]

                                # 단어 빈도 계산
                                word_counts = Counter(words).most_common(10)

                                # 단어 빈도 시각화
                                if word_counts:
                                    word_df = pd.DataFrame(
                                        word_counts, columns=["단어", "빈도"]
                                    )

                                    col_a, col_b = st.columns([3, 2])

                                    with col_a:
                                        fig = px.bar(
                                            word_df,
                                            x="단어",
                                            y="빈도",
                                            title="주요 단어 빈도",
                                            color="빈도",
                                            color_continuous_scale=px.colors.sequential.Blues,
                                        )
                                        fig.update_layout(
                                            xaxis_title="",
                                            yaxis_title="단어 빈도",
                                            coloraxis_showscale=False,
                                        )
                                        st.plotly_chart(fig, use_container_width=True)

                                    with col_b:
                                        # 단어 빈도 테이블
                                        st.dataframe(
                                            word_df,
                                            hide_index=True,
                                            use_container_width=True,
                                            column_config={
                                                "단어": st.column_config.TextColumn(
                                                    "주요 단어"
                                                ),
                                                "빈도": st.column_config.ProgressColumn(
                                                    "빈도",
                                                    min_value=0,
                                                    max_value=(
                                                        max([c[1] for c in word_counts])
                                                        if word_counts
                                                        else 10
                                                    ),
                                                    format="%d",
                                                ),
                                            },
                                        )
                                else:
                                    st.info("분석할 단어가 충분하지 않습니다.")

            else:
                st.error(f"'{search_name}' 이름의 지원자를 찾을 수 없습니다.")

    with col2:
        st_lottie(lottie_search, height=200, key="search")

        # 검색 팁과 함께 카드 디자인 적용
        st.markdown(
            """
        <div class="applicant-card">
            <h4>검색 팁</h4>
            <ul>
                <li>정확한 이름을 입력하세요</li>
                <li>성과 이름 사이에 공백 없이 입력하세요</li>
                <li>부분 이름으로도 검색이 가능합니다</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # 최근 검색 기록 (세션 상태 활용)
        if not hasattr(st.session_state, "recent_searches"):
            st.session_state.recent_searches = []

        if search_name and search_name not in st.session_state.recent_searches:
            st.session_state.recent_searches.append(search_name)
            if len(st.session_state.recent_searches) > 5:
                st.session_state.recent_searches.pop(0)

        if st.session_state.recent_searches:
            st.markdown("<h4>최근 검색</h4>", unsafe_allow_html=True)

            # 최근 검색어 버튼 스타일링
            for recent in st.session_state.recent_searches:
                if st.button(recent, key=f"recent_{recent}"):
                    st.session_state.search_name = recent
                    st.experimental_rerun()
