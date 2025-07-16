# gpt_api.py
import streamlit as st
import json
import openai

# OpenRouter용 OpenAI client 설정
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

def generate_scenario(theme):
    prompt = f"""
    '{theme}' 테마의 랜덤 머더미스터리 시나리오를 JSON 형식으로 만들어줘. 
    인물은 4명, 각각의 비밀을 포함해줘. 설정, 장소, 피해자도 포함해줘.

    형식 예시:
    {{
      "setting": "...",
      "characters": [
        {{"name": "...", "secret": "..."}},
        ...
      ]
    }}
    """
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048  # 무료 사용자 허용량 고려
    )
    return json.loads(response.choices[0].message.content)

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
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": scenario_prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()

def generate_interrogation_response(target, question, session_state):
    character_name = session_state.role["name"]
    context = "\n".join(session_state.history[-6:])
    prompt = f"""
    [시나리오 설정]
    {session_state.scenario['setting']}

    [당신의 역할]
    {character_name} - {session_state.role['secret']}

    [상대 캐릭터]
    {target}

    [질문]
    {question}

    [이전 대화]
    {context}

    [AI 응답]
    {target}이 플레이어의 질문에 대해 수상하게 혹은 단서를 흘릴 수 있도록 반응하게 해줘.
    """
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()

def evaluate_guess(guess, session_state):
    prompt = f"""
    [시나리오 설정]
    {session_state.scenario['setting']}

    [캐릭터 정보]
    {session_state.scenario['characters']}

    [플레이어가 지목한 인물]
    {guess}

    이 인물이 진짜 범인인지 판정하고, 이유를 설명해줘. 실제 범인을 알려주고 정답 여부를 명확히 판단해줘.
    """
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()
