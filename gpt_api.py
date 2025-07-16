from openai import OpenAI
import streamlit as st
import json

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

def generate_scenario(theme):
    prompt = f"""
    '{theme}'을(를) 배경으로 한 머더미스터리 시나리오를 JSON 형식으로 만들어줘.
    인물은 4명, 각각의 비밀을 포함해줘. 설정, 장소, 피해자 포함.

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
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]

    prompt = f"""
    [설정]: {session_state.scenario['setting']}
    [내 역할]: {character_name} - {session_state.role['secret']}
    [등장인물]: {session_state.scenario['characters']}
    [이전 대화]: {context}
    [플레이어의 입력]: {user_input}

    [AI 응답]: 플레이어 행동에 대한 결과를 서술해줘. 단서나 상황 전개를 포함해줘.
    """
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_interrogation_response(target, question, session_state):
    prompt = f"""
    [설정]: {session_state.scenario['setting']}
    [질문 대상]: {target}
    [질문 내용]: {question}
    [등장인물]: {session_state.scenario['characters']}

    대상 인물이 비밀을 바로 드러내지 않도록 말투와 태도를 조절해 응답해줘.
    """
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def evaluate_guess(guess, session_state):
    prompt = f"""
    [설정]: {session_state.scenario['setting']}
    [등장인물]: {session_state.scenario['characters']}
    [플레이어의 최종 추리]: {guess}

    누가 진범인지, 트릭은 무엇인지, 왜 살인을 저질렀는지 명확히 설명해줘.
    """
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
