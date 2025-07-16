
import streamlit as st
from gpt_api import generate_scenario, generate_response

# 세션 초기화
if "history" not in st.session_state:
    st.session_state.history = []
if "scenario" not in st.session_state:
    st.session_state.scenario = generate_scenario()
if "role" not in st.session_state:
    st.session_state.role = st.session_state.scenario["characters"][0]  # 임시 선택

st.title("🕵️ 머더 미스터리: AI TRPG")
st.markdown(f"**당신의 역할:** {st.session_state.role['name']}")
st.markdown("### 사건 현장")
st.markdown(st.session_state.scenario["setting"])

# 이전 대화 출력
for line in st.session_state.history:
    st.markdown(line)

# 입력 받기
user_input = st.text_input("당신의 행동이나 질문을 입력하세요", key="input")
if st.button("제출") and user_input:
    response = generate_response(user_input, st.session_state)
    st.session_state.history.append(f"🧑‍💼 너: {user_input}")
    st.session_state.history.append(f"🤖 AI: {response}")
    st.experimental_rerun()
