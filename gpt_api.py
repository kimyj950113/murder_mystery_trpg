import openai
import streamlit as st

def generate_scenario():
    # 간단한 GPT 기반 시나리오 생성
    prompt = """
    '랜덤 머더미스터리 시나리오를 JSON 형식으로 만들어줘. 
    인물은 4명, 각각의 비밀을 포함해줘. 설정, 장소, 피해자도 포함해줘.'

    형식 예시:
    {
      "setting": "...",
      "characters": [
        {"name": "...", "secret": "..."},
        ...
      ]
    }
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=st.secrets["OPENAI_API_KEY"]
    )
    return eval(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]

    scenario_prompt = f"""
    [시나리오 설정]
    {session_state.scenario['setting']}

    [당신의 역할]
    {character_name} - {session_state.role['secret']}

    [등장인물 목록]
    {session_state.scenario['characters']}

    [이전 대화 기록]
    {context}

    [플레이어의 입력]
    {user_input}

    [AI 응답]
    플레이어의 행동에 대해 서술적인 반응과 새로운 단서를 포함해 묘사해줘. 게임 마스터처럼 NPC/상황을 컨트롤하는 느낌으로.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": scenario_prompt}],
        api_key=st.secrets["OPENAI_API_KEY"]
    )
    return response.choices[0].message.content.strip()
