def speak(pokemon_name, character_list, provider):
    if provider == "anthropic":
        return [{
            "name": "speak",
            "description": "포켓몬의 나레이션을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [pokemon_name],
                        "description": "포켓몬의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "string",
                        "enum": character_list,
                        "description": "말을 걸 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "포켓몬의 나레이션을 입력합니다."
                    }
                },
                "required": ["name", "target", "chat"]
            }
        }]
    elif provider == "google":
        return [{
            "name": "speak",
            "description": "포켓몬의 나레이션을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [pokemon_name],
                        "description": "포켓몬의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "말을 걸 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "STRING",
                        "description": "포켓몬의 나레이션을 입력합니다."
                    }
                },
                "required": ["name", "target", "chat"]
            }
        }]