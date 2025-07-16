# gpt_api.py
from openai import OpenAI
import streamlit as st
import json

# OpenRouter용 OpenAI 클라이언트 생성
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url=st.secrets["OPENROUTER_BASE_URL"]
)

def generate_scenario(theme):
    prompt = f"""
    머더 미스터리 시나리오를 JSON 형식으로 만들어줘.
    - 배경 테마: {theme}
    - 인물 수: 4명
    - 각 인물의 이름과 비밀 포함
    - 설정 설명, 장소 설명, 피해자 이름 포함
    - 출력은 JSON 형식, 키는 영어. 예시:

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
        model="gpt-3.5-turbo",  # 무료 계정 호환 모델
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200
    )
    return json.loads(response.choices[0].message.content)

def generate_response(user_input, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]
    character_secret = session_state.role["secret"]
    setting = session_state.scenario['setting']
    characters = session_state.scenario['characters']

    prompt = f"""
    [시나리오 설정]
    {setting}

    [당신의 역할]
    {character_name} - {character_secret}

    [등장인물 목록]
    {characters}

    [이전 대화 기록]
    {context}

    [플레이어의 입력]
    {user_input}

    [응답 규칙]
    - 반드시 한국어로 응답할 것
    - 플레이어의 행동에 대해 서술적으로 반응
    - NPC나 주변 환경을 마스터처럼 묘사할 것
    - 새로운 단서가 있다면 명확히 드러내기

    지금 바로 반응을 출력하세요.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4o (유료 계정)
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

def generate_interrogation_response(target, question, session_state):
    context = "\n".join(session_state.history[-6:])
    character_name = session_state.role["name"]
    character_secret = session_state.role["secret"]
    setting = session_state.scenario['setting']
    characters = session_state.scenario['characters']

    prompt = f"""
    [시나리오 설정]
    {setting}

    [플레이어 캐릭터]
    {character_name} - {character_secret}

    [등장인물]
    {characters}

    [상황]
    플레이어가 {target}에게 다음 질문을 합니다: "{question}"

    [응답 규칙]
    - 반드시 한국어로 출력
    - {target}의 말투와 감정을 묘사
    - NPC의 비밀을 직접 드러내지 않되 의심을 유도할 수 있음

    [출력 형식]
    🎭 {target}: "..."
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

def evaluate_guess(guess_name, session_state):
    setting = session_state.scenario['setting']
    victim = session_state.scenario.get("victim", "피해자 정보 없음")
    characters = session_state.scenario['characters']
    clues = session_state.clues

    prompt = f"""
    [시나리오 설정]
    {setting}

    [피해자]
    {victim}

    [등장인물 목록]
    {characters}

    [수집된 단서]
    {clues}

    [플레이어의 최종 추리]
    범인은 {guess_name}이라고 지목했습니다.

    [응답 규칙]
    - 한국어로 출력
    - 플레이어의 추리가 맞는지 판정하고 이유 설명
    - 진짜 범인이 누구였는지 밝혀주세요

    결과를 알려주세요.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content.strip()
