# main.py
import streamlit as st
from gpt_api import generate_scenario, generate_response, generate_interrogation_response, evaluate_guess
import random

# 초기 세션 상태 설정
def init_session():
    if "theme" not in st.session_state:
        st.session_state.theme = None
    if "scenario" not in st.session_state:
        st.session_state.scenario = None
    if "character" not in st.session_state:
        st.session_state.character = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "history" not in st.session_state:
        st.session_state.history = []
    if "round" not in st.session_state:
        st.session_state.round = 1
    if "clues" not in st.session_state:
        st.session_state.clues = []
    if "phase" not in st.session_state:
        st.session_state.phase = "play"  # play / interrogate / guess / end

init_session()
st.title("머더 미스터리 TRPG: AI 게임 마스터")

# 1. 테마 선택 단계
if st.session_state.theme is None:
    st.subheader("1단계: 테마 선택")
    theme_choice = st.radio("플레이할 테마를 선택하세요:", ["무작위", "고등학교", "저택", "우주선"])
    if st.button("테마 확정"):
        st.session_state.theme = random.choice(["고등학교", "저택", "우주선"]) if theme_choice == "무작위" else theme_choice
        st.experimental_rerun()

# 2. 시나리오 생성 및 캐릭터 선택
elif st.session_state.scenario is None:
    with st.spinner("시나리오 생성 중..."):
        st.session_state.scenario = generate_scenario(st.session_state.theme)

elif st.session_state.character is None:
    st.subheader("2단계: 캐릭터 선택")
    st.write(f"### 설정: {st.session_state.scenario['setting']}")
    for idx, char in enumerate(st.session_state.scenario["characters"]):
        st.markdown(f"**{idx+1}. {char['name']}**: 비밀은 선택 후 공개됩니다.")
    options = [char["name"] for char in st.session_state.scenario["characters"]]
    selected = st.radio("플레이할 캐릭터를 고르세요:", options)
    if st.button("캐릭터 확정"):
        for c in st.session_state.scenario["characters"]:
            if c["name"] == selected:
                st.session_state.character = selected
                st.session_state.role = c
                break
        st.experimental_rerun()

else:
    # 역할 카드 UI
    with st.sidebar:
        st.header("내 역할 정보")
        st.markdown(f"**이름**: {st.session_state.role['name']}")
        st.markdown(f"**비밀**: {st.session_state.role['secret']}")
        st.markdown(f"**라운드**: {st.session_state.round}")
        st.markdown(f"**단서 수**: {len(st.session_state.clues)}")

    # 메인 단계 분기
    if st.session_state.phase == "play":
        st.subheader(f"Round {st.session_state.round} - 자유 행동")
        user_input = st.text_input("무엇을 하시겠습니까? (조사, 대화 등)", key="play_input")
        if st.button("행동 제출") and user_input:
            response = generate_response(user_input, st.session_state)
            st.session_state.history.append(f"🧑‍💼 너: {user_input}")
            st.session_state.history.append(f"🤖 AI: {response}")
            if "단서" in response or "의심" in response:
                st.session_state.clues.append(response)

        for h in st.session_state.history[-6:]:
            st.markdown(h)

        st.markdown("---")
        st.subheader("발견된 단서")
        if st.session_state.clues:
            for c in st.session_state.clues:
                st.markdown(f"- {c}")
        else:
            st.markdown("(아직 단서 없음)")

        st.markdown("---")
        if st.button("추궁 단계로 이동"):
            st.session_state.phase = "interrogate"
            st.experimental_rerun()

    elif st.session_state.phase == "interrogate":
        st.subheader("특정 인물 추궁하기")
        others = [c["name"] for c in st.session_state.scenario["characters"] if c["name"] != st.session_state.character]
        target = st.selectbox("누구를 추궁할까요?", others)
        question = st.text_input("무엇을 질문하시겠습니까?", key="interrogate_input")
        if st.button("추궁하기"):
            reply = generate_interrogation_response(target, question, st.session_state)
            st.session_state.history.append(f"🧑‍💼 {target}에게: {question}")
            st.session_state.history.append(f"🎭 {target}: {reply}")
            st.experimental_rerun()
        st.markdown("---")
        if st.button("범인 추리 단계로 이동"):
            st.session_state.phase = "guess"
            st.experimental_rerun()

    elif st.session_state.phase == "guess":
        st.subheader("범인은 누구라고 생각하십니까?")
        suspects = [c["name"] for c in st.session_state.scenario["characters"]]
        guess = st.radio("범인으로 지목할 캐릭터:", suspects)
        if st.button("범인 확정!"):
            result = evaluate_guess(guess, st.session_state)
            st.session_state.history.append(f"🎯 최종 추리: {guess}")
            st.session_state.history.append(f"✅ AI 판정: {result}")
            st.session_state.phase = "end"
            st.experimental_rerun()

    elif st.session_state.phase == "end":
        st.subheader("게임 종료")
        for h in st.session_state.history:
            st.markdown(h)
        st.markdown("---")
        st.markdown("게임을 다시 시작하시려면 앱을 새로고침해주세요.")
