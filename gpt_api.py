import streamlit as st
from openai import OpenAI
import json

# OpenRouter API 클라이언트
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

def generate_scenario():
    prompt = """
다음과 같은 형식의 랜덤 머더미스터리 시나리오를 JSON으로 만들어줘.
- 등장인물은 4명 (각각 이름과 비밀 포함)
- 설정(setting): 사건 장소와 배경
- 피해자도 반드시 포함
예시 형식:
{
  "setting": "...",
  "characters": [
    {"name": "홍길동", "secret": "사실 피해자의 전 연인이다"},
    {"name": "이몽룡", "secret": "범행 당시의 알리바이를 조작했다"},
    ...
  ]
}
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]
    secret = session_state.role["secret"]

    scenario_prompt = f"""
[시나리오 설정]
{session_state.scenario['setting']}

[당신의 역할]
{character_name} - {secret}

[등장인물 목록]
{json.dumps(session_state.scenario['characters'], ensure_ascii=False)}

[이전 대화 기록]
{context}

[플레이어 입력]
{user_input}

[AI 응답]
플레이어의 행동에 대해 게임 마스터처럼 서술적으로 반응해줘. 단서, 긴장감, 새로운 정보가 포함되면 좋겠어.
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": scenario_prompt}]
    )
    return response.choices[0].message.content.strip()
