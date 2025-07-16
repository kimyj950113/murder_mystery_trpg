
import random

def generate_scenario():
    # 단순 무작위 시나리오 생성 예시
    return {
        "setting": "당신은 한 외딴 저택에서 열린 파티에 참석했다. 다음 날 아침, 저택 주인이 살해된 채 발견되었다.",
        "characters": [
            {"name": "김탐정", "secret": "사건 전날 피해자와 격렬히 말다툼을 했다."},
            {"name": "이하인", "secret": "피해자의 유산을 노리고 있었다."},
            {"name": "박서기", "secret": "피해자에게 해고당할 위기에 처해 있었다."},
            {"name": "최요리사", "secret": "피해자의 비밀을 알고 있었다."}
        ]
    }

def generate_response(user_input, session_state):
    # 간단한 응답 시뮬레이션 (GPT 대신 임시 반응)
    character = session_state["role"]["name"]
    return f"{character}은(는) 주변을 살펴보며 말했다: '{user_input}'... 음, 흥미롭군요.'"
