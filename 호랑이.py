import streamlit as st
import random

# --- 설정값 ---
TOTAL_STAGES = 11  # 호랑이 완성에 필요한 단계 (정답 수)
TIGER_THEME = "호랑이 완성 작전"

# 맞힌 횟수에 따라 호랑이의 각 부분이 완성되는 텍스트/이모지 매핑
TIGER_COMPONENTS = {
    0: "⚫️",
    1: "🟫 호랑이의 꼬리 한 조각이 나타났습니다.",
    2: "🔶 호랑이의 뒷다리가 준비되었습니다.",
    3: "🟠 호랑이의 앞다리 한 쌍이 보입니다.",
    4: "🟡 호랑이의 몸통 윤곽이 나타났습니다.",
    5: "🟢 호랑이의 강한 어깨가 형성됩니다.",
    6: "🔵 호랑이의 목이 굵어집니다.",
    7: "🟣 호랑이의 늠름한 머리가 보이기 시작합니다.",
    8: "🔴 호랑이의 날카로운 눈빛이 빛나기 시작합니다.",
    9: "⚫️ 호랑이의 멋진 줄무늬가 그려집니다.",
    10: "👑 호랑이의 왕관 같은 귀가 솟아납니다.",
    11: "🐯 **최종 완성!** 용맹한 백호가 나타났습니다!", 
}


# --- 퀴즈 데이터 (공통수학2 개념을 바탕으로 예시 문제 11개) ---
# 기존의 수학 문제를 그대로 사용합니다.
QUIZ_QUESTIONS = [
    {
        "question": "집합 $A = \{x | x^2 - 3x + 2 = 0\}$ 의 원소의 개수는?",
        "options": ["1개", "2개", "3개", "4개"],
        "answer": "2개",
        "concept": "집합의 표현",
    },
    {
        "question": "두 조건 $p: x > 2$ 와 $q: x > a$ 에 대하여 $p \\to q$ 가 참이 되도록 하는 실수 $a$ 의 최댓값은?",
        "options": ["1", "2", "3", "4"],
        "answer": "2",
        "concept": "명제와 조건",
    },
    {
        "question": "함수 $f(x) = 2x + 1$ 의 역함수 $f^{-1}(x)$ 는?",
        "options": ["$(x-1)/2$", "$x - 1$", "$2x - 1$", "$1/(2x+1)$"],
        "answer": "$(x-1)/2$",
        "concept": "역함수",
    },
    {
        "question": "무리함수 $y = \\sqrt{x-1} + 3$ 의 정의역은?",
        "options": ["$x \\ge 1$", "$x > 1$", "$x \\ge 3$", "실수 전체"],
        "answer": "$x \\ge 1$",
        "concept": "무리함수의 정의역",
    },
    {
        "question": "유리식 $\\frac{x^2 - 4}{x - 2}$ 를 약분하면? (단, $x \\ne 2$)",
        "options": ["$x - 2$", "$x + 2$", "1", "$x^2 - 2$"],
        "answer": "$x + 2$",
        "concept": "유리식의 계산",
    },
    {
        "question": "원 $(x-1)^2 + (y+2)^2 = 9$ 의 중심 좌표는?",
        "options": ["$(1, -2)$", "$(-1, 2)$", "$ (1, 2)$", "$(-1, -2)$"],
        "answer": "$(1, -2)$",
        "concept": "원의 방정식",
    },
    {
        "question": "점 $(1, 3)$ 을 $x$ 축 방향으로 2, $y$ 축 방향으로 $-1$ 만큼 평행이동한 점의 좌표는?",
        "options": ["$(3, 2)$", "$(-1, 4)$", "$(3, 4)$", "$(-1, 2)$"],
        "answer": "$(3, 2)$",
        "concept": "점의 평행이동",
    },
    {
        "question": "직선 $2x - y + 1 = 0$ 을 $y$ 축에 대하여 대칭이동한 직선의 방정식은?",
        "options": ["$-2x - y + 1 = 0$", "$2x + y + 1 = 0$", "$-2x + y + 1 = 0$", "$2x - y - 1 = 0$"],
        "answer": "$2x + y + 1 = 0$",
        "concept": "도형의 대칭이동",
    },
    {
        "question": "합성함수 $f(x) = x+1, g(x) = x^2$ 일 때, $(g \\circ f)(x)$ 는?",
        "options": ["$x^2 + 1$", "$(x+1)^2$", "$2x + 1$", "$x^2 + x$"],
        "answer": "$(x+1)^2$",
        "concept": "합성함수",
    },
    {
        "question": "이차함수 $y = x^2$ 의 그래프를 $x$ 축으로 1만큼, $y$ 축으로 2만큼 평행이동한 그래프의 꼭짓점 좌표는?",
        "options": ["$(-1, -2)$", "$(1, 2)$", "$(-1, 2)$", "$(1, -2)$"],
        "answer": "$(1, 2)$",
        "concept": "포물선의 평행이동",
    },
    {
        "question": "함수 $f(x) = x^3$ 이 일대일 대응인지 판별하시오.",
        "options": ["일대일 대응이다", "일대일 함수이지만 일대일 대응은 아니다", "일대일 함수가 아니다", "대응 관계가 아니다"],
        "answer": "일대일 대응이다",
        "concept": "함수의 종류",
    },
]

# --- 세션 상태 초기화 함수 ---
def init_session_state():
    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0  # 맞힌 문제 수 (호랑이 완성 단계)
    if "current_question_index" not in st.session_state:
        # 문제 순서를 섞고 첫 번째 문제 인덱스로 설정
        st.session_state.question_indices = list(range(len(QUIZ_QUESTIONS)))
        random.shuffle(st.session_state.question_indices)
        st.session_state.current_question_index = 0
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False

# --- 다음 문제로 이동하는 콜백 함수 ---
def check_answer_and_next(question_data, user_answer):
    if st.session_state.quiz_finished:
        return

    # 정답 확인
    if user_answer == question_data["answer"]:
        st.session_state.correct_count += 1
        st.success(f"✅ 정답입니다! (현재 완성 단계: {st.session_state.correct_count}/{TOTAL_STAGES})")
    else:
        st.error(f"❌ 오답입니다. 정답은 **{question_data['answer']}** 였습니다.")

    # 카운트가 최종 단계 수에 도달했는지 확인
    if st.session_state.correct_count >= TOTAL_STAGES:
        st.session_state.quiz_finished = True
    else:
        # 다음 문제로 인덱스 이동
        st.session_state.current_question_index += 1
        # 모든 문제 11개를 풀었으나 정답이 11개가 되지 않은 경우, 재도전을 위해 다시 섞음
        if st.session_state.current_question_index >= len(st.session_state.question_indices):
             st.session_state.question_indices = list(range(len(QUIZ_QUESTIONS)))
             random.shuffle(st.session_state.question_indices)
             st.session_state.current_question_index = 0
             st.info("문제를 모두 풀었습니다. 정답 수가 부족하여 다시 문제를 섞습니다.")


# --- 앱 메인 로직 ---
def main():
    st.set_page_config(page_title="수학 퀴즈 - 호랑이 완성", layout="wide")
    init_session_state()

    st.title(f"🐅 {TIGER_THEME}: 공통수학2 마스터!")
    st.markdown(f"정답을 맞힐 때마다 **호랑이**가 한 단계씩 완성됩니다. **총 {TOTAL_STAGES}단계**를 거쳐 호랑이를 완성하세요!")

    # --- 호랑이 완성 진행 상황 표시 ---
    st.subheader("🌟 현재 호랑이 완성 단계")
    
    # 진행률 표시
    progress_ratio = min(st.session_state.correct_count / TOTAL_STAGES, 1.0)
    st.progress(progress_ratio, text=f"호랑이 완성률: {st.session_state.correct_count} / {TOTAL_STAGES}")
    
    # 호랑이 완성 단계 텍스트 표시
    progress_text = ""
    for i in range(1, TOTAL_STAGES + 1):
        if st.session_state.correct_count >= i:
            # i번째 단계가 완성되었음을 표시 (색상 블록 사용)
            progress_text += "🟩" 
        else:
            # 아직 미완성임을 표시
            progress_text += "⬜️"

    st.markdown(f"### {progress_text}")
    
    # 현재 완성된 부분에 대한 설명
    current_stage = st.session_state.correct_count
    st.info(f"**현재 상태:** {TIGER_COMPONENTS.get(current_stage, '⚫️ 아직 호랑이의 형체가 보이지 않습니다.')}")
    
    st.markdown("---")


    # --- 퀴즈 진행 ---
    if st.session_state.quiz_finished:
        # 최종 완성 메시지
        st.balloons()
        st.success(f"## 🐯 미션 성공! **{TIGER_THEME}** 완료!")
        st.markdown(f"### **11단계 완성!** 용맹하고 위풍당당한 **백호**가 당신 앞에 모습을 드러냈습니다!")
        #  # 시각화를 위한 이미지 태그
        
        st.caption("새로운 퀴즈를 시작하려면 아래 버튼을 클릭하세요.")
        if st.button("🚀 재시작"):
            # 세션 상태 초기화
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    else:
        # 현재 문제 인덱스를 사용하여 퀴즈 데이터 가져오기
        q_idx = st.session_state.question_indices[st.session_state.current_question_index % len(st.session_state.question_indices)]
        current_question = QUIZ_QUESTIONS[q_idx]

        st.subheader(f"💡 {st.session_state.correct_count + 1} 번째 도전 (개념: {current_question['concept']})")
        # LaTeX으로 수식 표시
        st.latex(current_question["question"]) 

        # 선택지
        user_answer = st.radio(
            "정답을 선택하세요:",
            current_question["options"],
            key=f"q_{
