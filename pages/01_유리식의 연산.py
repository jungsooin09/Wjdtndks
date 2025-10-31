import streamlit as st

# 5문제 퀴즈 데이터 정의
# 문제, 보기, 정답 인덱스(0부터 시작)를 포함합니다.
quiz_data = [
    {
        "question": r"Q1. 다음 유리식 $\frac{x^2 - 4}{x^2 - 5x + 6}$ 를 간단히 하시오.",
        "options": [r"$\frac{x-2}{x+3}$", r"$\frac{x+2}{x-3}$", r"$\frac{x+2}{x+3}$", r"$\frac{x-3}{x+2}$"],
        "correct_index": 1,
        "rationale": r"분자 $x^2-4 = (x-2)(x+2)$, 분모 $x^2-5x+6 = (x-2)(x-3)$을 인수분해하여 공통 인수 $(x-2)$를 약분합니다."
    },
    {
        "question": r"Q2. $\frac{1}{x} + \frac{1}{x+1}$ 을 계산하시오.",
        "options": [r"$\frac{2}{x(x+1)}$", r"$\frac{2x+1}{x(x+1)}$", r"$\frac{x+1}{x^2+x}$", r"$\frac{x+1}{2x+1}$"],
        "correct_index": 1,
        "rationale": r"공통분모 $x(x+1)$로 통분하면 $\frac{x+1}{x(x+1)} + \frac{x}{x(x+1)} = \frac{2x+1}{x(x+1)}$ 입니다."
    },
    {
        "question": r"Q3. $\frac{x}{x-1} - \frac{1}{1-x}$ 을 계산하시오.",
        "options": [r"$\frac{x-1}{x-1}$", r"$\frac{x+1}{x-1}$", r"$\frac{x-1}{2}$", r"$1$"],
        "correct_index": 1,
        "rationale": r"$\frac{1}{1-x} = \frac{-1}{x-1}$ 이므로 $\frac{x}{x-1} - \frac{-1}{x-1} = \frac{x+1}{x-1}$ 입니다."
    },
    {
        "question": r"Q4. $\frac{x+2}{x^2 - 1} \times \frac{x-1}{x^2 + 4x + 4}$ 을 간단히 하시오.",
        "options": [r"$\frac{x-1}{(x-1)(x+2)}$", r"$\frac{1}{(x+1)(x+2)}$", r"$\frac{1}{x+1}$", r"$\frac{1}{x+2}$"],
        "correct_index": 1,
        "rationale": r"$\frac{x+2}{(x-1)(x+1)} \times \frac{x-1}{(x+2)^2}$ 로 인수분해하여 약분하면 $\frac{1}{(x+1)(x+2)}$ 입니다."
    },
    {
        "question": r"Q5. $(\frac{1}{a} - \frac{1}{b}) \div \frac{b^2 - a^2}{a^2 b^2}$ 을 계산하시오.",
        "options": [r"$\frac{a+b}{ab}$", r"$\frac{1}{a+b}$", r"$\frac{ab}{a+b}$", r"$a+b$"],
        "correct_index": 2,
        "rationale": r"$\frac{b-a}{ab} \times \frac{a^2 b^2}{(b-a)(b+a)}$ 이 되어 약분하면 $\frac{ab}{a+b}$ 입니다."
    }
]

# Streamlit 세션 상태 초기화
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = [False] * len(quiz_data)
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False

# 고양이 그림을 점수에 따라 단계별로 그리는 함수 (ASCII Art)
def draw_cat(score):
    if score == 0:
        cat_art = r"""
 /\_/\  (0점: 시작!)
( o.o ) 
 > ^ <
        """
    elif score == 1:
        cat_art = r"""
 /\_/\  (1점: 귀 하나)
( o.o ) 
 > ^ < 
  ( )
        """
    elif score == 2:
        cat_art = r"""
 /\_/\  (2점: 머리와 몸통)
( o.o )
 > ^ <
  (   )
 (  .  )
        """
    elif score == 3:
        cat_art = r"""
 /\_/\  (3점: 꼬리 추가)
( o.o )
 > ^ <   
  (   )
 (  .  )
/      \
        """
    elif score == 4:
        cat_art = r"""
 /\_/\  (4점: 다리와 발)
( o.o )
 > ^ <   
  (   )
 (  .  )
/      \
|  /\  |
        """
    elif score == 5:
        cat_art = r"""
 /\_/\  (5점: 완전한 고양이!) 😸
( *.* )  <- 유리식 연산 마스터!
 > ^ <
  (   )
 (  .  )
/      \
|  /\  |
| /  \ |
~~~~~~~~
        """
    else:
        cat_art = "고양이 그리기 오류"

    st.markdown(f"```\n{cat_art}\n```")
    st.progress(score / len(quiz_data))
    st.markdown(f"**현재 점수: {score} / 5**")


# 퀴즈 제출 핸들러
def submit_answer(selected_option_index):
    current_q = quiz_data[st.session_state.current_q_index]

    if st.session_state.correct_answers[st.session_state.current_q_index]:
        # 이미 맞춘 문제인 경우, 제출을 막거나 안내를 할 수 있습니다.
        st.error("이미 맞춘 문제입니다. 다음 문제로 이동해 주세요.")
        return

    # 정답 확인
    if selected_option_index == current_q["correct_index"]:
        st.success("🎉 정답입니다! 다음 고양이 조각을 얻었어요!")
        
        # 정답 처리
        st.session_state.score += 1
        st.session_state.correct_answers[st.session_state.current_q_index] = True
        
        if st.session_state.score == len(quiz_data):
            st.session_state.quiz_finished = True
        
        # 잠시 후 다음 문제로 이동 (바로 이동하지 않고 정답 확인 후 버튼을 누르게 유도)
        
    else:
        st.error("❌ 오답입니다. 다시 한번 생각해 보세요.")
        st.markdown(f"**정답 해설:** {current_q['rationale']}")

# 메인 앱
def app():
    st.title("😸 유리식 연산 마스터 퀴즈")
    st.subheader("정답을 맞힐 때마다 고양이가 완성됩니다!")
    st.latex(r"\text{현재 진행률 (고양이 완성도)}")
    draw_cat(st.session_state.score)
    st.markdown("---")
    
    # 퀴즈가 끝나지 않았을 경우 문제 표시
    if not st.session_state.quiz_finished:
        q_index = st.session_state.current_q_index
        current_q = quiz_data[q_index]

        st.header(f"문제 {q_index + 1}.")
        st.latex(current_q["question"])
        
        # 라디오 버튼으로 보기 표시
        # 라디오 버튼은 선택 시 바로 콜백 함수를 호출하도록 함
        selected_option = st.radio(
            "답을 선택하세요:",
            options=current_q["options"],
            key=f
