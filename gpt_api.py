import openai
import streamlit as st
import json

# OpenRouter 전용 OpenAI 클라이언트 설정
client = openai.OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# OpenRouter 지원 모델 중 유효한 모델 ID 사용 (예: openrouter/gpt-3.5-turbo)
MODEL_ID = "openai/gpt-4o"

def generate_scenario(theme):
    prompt = f"""
    아래 조건을 반영한 머더 미스터리 시나리오를 JSON 형식으로 생성해줘:
    - 장소: {theme} 테마
    - 인물 수: 4명 (각각 고유한 이름과 비밀 포함)
    - 피해자 1명 포함

    형식 예시:
    {{
      "setting": "...",
      "characters": [
        {{"name": "...", "secret": "..."}},
        ...
      ],
      "culprit": "..."
    }}
    """
    response = client.chat.completions.create(
        model=MODEL_ID,
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
    플레이어의 행동에 대해 서술적인 반응과 새로운 단서를 포함해 묘사해줘. 반드시 한국어로 응답해줘.
    """
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_interrogation_response(target, question, session_state):
    character_name = session_state.role["name"]

    prompt = f"""
    [시나리오 설정]
    {session_state.scenario['setting']}

    [등장인물 목록]
    {session_state.scenario['characters']}

    [플레이어의 역할]
    {character_name} - {session_state.role['secret']}

    [플레이어의 추궁]
    대상: {target}
    질문: {question}

    [응답 방식]
    반드시 한국어로 해당 인물이 대답하도록 구성하고, 캐릭터의 비밀이나 단서를 일부 드러내도 좋아. 다만 모든 진실을 바로 말하지는 마. 추리의 여지를 남겨줘.
    """
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def evaluate_guess(guess, session_state):
    culprit = session_state.scenario.get("culprit", "")
    if guess == culprit:
        return f"정답입니다! 범인은 바로 {culprit}였습니다."
    else:
        return f"아쉽습니다. 범인은 {culprit}였습니다. 당신의 추리는 틀렸어요."
