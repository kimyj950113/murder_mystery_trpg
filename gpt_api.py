# gpt_api.py
from openai import OpenAI
import streamlit as st
import json

# OpenRouter 전용 클라이언트 설정
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

def generate_scenario(theme="무작위"):
    prompt = f"""
    아래 형식에 따라 랜덤 머더미스터리 시나리오를 만들어줘. 인물은 4명이며, 각 인물은 서로 다른 비밀을 갖고 있어야 해. 
    주제는 "{theme}"이고 장소, 피해자 정보도 포함해줘. 결과는 반드시 JSON으로 반환해.

    형식 예시:
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
        model="mistralai/mixtral-8x7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000  # 제한 설정
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]
    scenario_prompt = f"""
    [시나리오 설정]
    {session_state.scenario['setting']}

    [피해자]
    {session_state.scenario.get('victim', '')}

    [당신의 역할]
    {character_name} - {session_state.role['secret']}

    [등장인물 목록]
    {session_state.scenario['characters']}

    [이전 대화 기록]
    {context}

    [플레이어의 입력]
    {user_input}

    [AI 응답]
    플레이어의 행동에 대해 상황을 서술적으로 묘사하고, 조사 결과나 NPC의 반응을 포함해줘.
    """
    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[{"role": "user", "content": scenario_prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def generate_interrogation_response(target, question, session_state):
    scenario = session_state.scenario
    context = "\n".join(session_state.history[-6:])
    interrogation_prompt = f"""
    [시나리오 설정]
    {scenario['setting']}

    [피해자]
    {scenario.get('victim', '')}

    [플레이어 캐릭터]
    {session_state.character} - {session_state.role['secret']}

    [대상 캐릭터]
    {target}

    [플레이어의 질문]
    {question}

    [최근 대화 기록]
    {context}

    대상 캐릭터의 입장에서 자연스럽고 의심스러운 답변을 해줘. 그의 비밀을 완전히 드러내지 않도록 하되, 단서를 조금 흘릴 수 있어.
    """
    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[{"role": "user", "content": interrogation_prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def evaluate_guess(guess, session_state):
    prompt = f"""
    [시나리오 설정]
    {session_state.scenario['setting']}

    [등장인물]
    {session_state.scenario['characters']}

    [플레이어 추리]
    범인으로 지목된 사람: {guess}

    위 정보를 바탕으로, 플레이어의 추리가 정답인지 "맞았습니다" 또는 "틀렸습니다" 중 하나로만 답해주세요.
    """
    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
