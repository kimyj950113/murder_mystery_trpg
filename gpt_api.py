
import streamlit as st
from openai import OpenAI
import json

# OpenRouter용 OpenAI 클라이언트
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

def generate_scenario():
    prompt = '''
    랜덤 머더미스터리 시나리오를 JSON 형식으로 만들어줘. 
    인물은 4명, 각각의 비밀을 포함해줘. 설정, 장소, 피해자도 포함해줘.

    예시:
    {
      "setting": "...",
      "characters": [
        {"name": "...", "secret": "..."},
        ...
      ]
    }
    '''
    response = client.chat.completions.create(
        model="openrouter/gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]

    prompt = f"""
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
    response = client.chat.completions.create(
        model="openrouter/gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
