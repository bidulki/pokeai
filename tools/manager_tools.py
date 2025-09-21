def choose_character(character_list, provider):
    if provider == "anthropic":
        return {
            "name": "choose_character",
            "description": "선택된 캐릭터가 게임 내에서 행동합니다. 주어진 캐릭터 목록에서 선택합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": character_list,
                        "description": "선택할 캐릭터를 입력합니다."
                    }
                },
                "required": ["name"]
            }
        }
    elif provider == "google":
        return {
            "name": "choose_character",
            "description": "선택된 캐릭터가 게임 내에서 행동합니다. 주어진 캐릭터 목록에서 선택합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "선택할 캐릭터를 입력합니다."
                    }
                },
                "required": ["name"]
            }
        }

def recommend_user_chat(provider):
    if provider == "anthropic":
        return [{
            "name": "recommend_user_chat",
            "description": "게임 내에서 사용자에게 추천할 채팅을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": ["레드"],
                        "description": "사용자의 이름을 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "추천할 채팅을 입력합니다."
                    }
                },
                "required": ["name", "chat"]
            }
        }]
    elif provider == "google":
        return [{
            "name": "recommend_user_chat",
            "description": "게임 내에서 사용자에게 추천할 채팅을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": ["레드"],
                        "description": "사용자의 이름을 입력합니다."
                    },
                    "chat": {
                        "type": "STRING",
                        "description": "추천할 채팅을 입력합니다."
                    }
                },
                "required": ["name", "chat"]
            }
        }]

def next_scene(provider):
    if provider == "anthropic":
        return {
            "name": "next_scene",
            "description": "현재 상호작용 종료 및 다음 단계로 진행",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    elif provider == "google":
        return {
            "name": "next_scene",
            "description": "현재 상호작용 종료 및 다음 단계로 진행",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "dummy": {
                        "type": "STRING",
                        "description": "사용하지 않는 더미 속성입니다."
                    }
                },
                "required": []
            }
        }

def choose_action(character_list, provider, talk_target=None):
    tools = [] 
    if talk_target==None:
        tools.append(next_scene(provider))
    else:
        character_list = [talk_target]
    if len(character_list) >= 1:
        tools.append(choose_character(character_list, provider))
    
    return tools