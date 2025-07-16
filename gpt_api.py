from openai import OpenAI
import streamlit as st
import json

# OpenRouter API 설정
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

def generate_scenario(theme):
    prompt = f"""
다음은 머더 미스터리 게임의 설정입니다. 다음 형식으로 한국어로 시나리오를 만들어주세요.

- 장소 및 설정: {theme} 배경
- 등장인물: 4명, 이름과 비밀 포함
- 피해자: 반드시 명시

형식:
{{
  "setting": "...",
  "victim": "...",
  "characters": [
    {{"name": "...", "secret": "..."}},
    ...
  ]
}}
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]

    scenario_prompt = f"""
[설정]
{session_state.scenario['setting']}

[플레이어의 역할]
이름: {character_name}
비밀: {session_state.role['secret']}

[등장인물]
{session_state.scenario['characters']}

[이전 대화 기록]
{context}

[플레이어 입력]
{user_input}

[응답]
상황을 묘사하고, 단서나 의심을 유도할 만한 요소를 포함한 한국어 응답을 생성해주세요.
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": scenario_prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()

def generate_interrogation_response(target, question, session_state):
    scenario = session_state.scenario
    role = session_state.role
    prompt = f"""
당신은 머더 미스터리 게임의 AI 마스터입니다. 다음 정보를 참고해, 추궁에 대한 자연스러운 한국어 응답을 생성하세요.

[설정]
{scenario['setting']}

[플레이어 캐릭터]
이름: {role['name']}, 비밀: {role['secret']}

[등장인물]
{scenario['characters']}

[질문 대상]
{target}

[플레이어 질문]
"{question}"

[응답]
상황을 묘사하고, 해당 인물의 비밀을 감안해 추리의 실마리가 될 수 있는 대답을 한국어로 생성하세요.
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()

def evaluate_guess(guess, session_state):
    prompt = f"""
머더 미스터리 게임의 시나리오가 다음과 같습니다:

[설정]
{session_state.scenario['setting']}

[등장인물]
{session_state.scenario['characters']}

[플레이어 추리]
"{guess}"

이 추리가 맞았는지 여부를 판단하고, 간단한 이유를 덧붙여 한국어로 알려주세요.
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )
    return response.choices[0].message.content.strip()
