def speak(npc_name, character_list, provider):
    if provider == "anthropic":
        return {
            "name": "speak",
            "description": "NPC가 캐릭터에게 말을 걸어 채팅을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "string",
                        "enum": character_list,
                        "description": "말을 걸 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "NPC가 말할 채팅을 입력합니다."
                    }
                },
                "required": ["name", "target", "chat"]
            }
        }
    elif provider == "google":
        return {
            "name": "speak",
            "description": "NPC가 캐릭터에게 말을 걸어 채팅을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "말을 걸 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "STRING",
                        "description": "NPC가 말할 채팅을 입력합니다."
                    }
                },
                "required": ["name", "target", "chat"]
            }
        }

def give_pokemon(npc_name, pokemon_list, character_list, provider):
    if provider == "anthropic":
        return {
            "name": "give_pokemon",
            "description": "NPC가 캐릭터에게 포켓몬을 주고 채팅을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "NPC가 말할 채팅을 입력합니다."
                    },
                    "target": {
                        "type": "string",
                        "enum": character_list,
                        "description": "포켓몬을 줄 캐릭터를 입력합니다."
                    },
                    "pokemon": {
                        "type": "string",
                        "enum": pokemon_list,
                        "description": "줄 포켓몬을 입력합니다."
                    }
                },
                "required": ["name", "chat", "target", "pokemon"]
            }
        }
    elif provider == "google":
        return {
            "name": "give_pokemon",
            "description": "NPC가 캐릭터에게 포켓몬을 주고 채팅을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "chat": {
                        "type": "STRING",
                        "description": "NPC가 말할 채팅을 입력합니다."
                    },
                    "target": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "포켓몬을 줄 캐릭터를 입력합니다."
                    },
                    "pokemon": {
                        "type": "STRING",
                        "enum": pokemon_list,
                        "description": "줄 포켓몬을 입력합니다."
                    }
                },
                "required": ["name", "chat", "target", "pokemon"]
            }
        }

def give_item(npc_name, item_list, character_list, provider):
    if provider == "anthropic":
        return {
            "name": "give_item",
            "description": "NPC가 캐릭터에게 아이템을 주고 채팅을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "NPC가 말할 채팅을 입력합니다."
                    },
                    "target": {
                        "type": "string",
                        "enum": character_list,
                        "description": "아이템을 줄 캐릭터를 입력합니다."
                    },
                    "item": {
                        "type": "string",
                        "enum": item_list,
                        "description": "줄 아이템을 입력합니다."
                    },
                    "num": {
                        "type": "integer",
                        "description": "줄 아이템의 개수를 입력합니다."
                    }
                },
                "required": ["name", "chat", "target", "item", "num"]
            }
        }
    elif provider == "google":
        return {
            "name": "give_item",
            "description": "NPC가 캐릭터에게 아이템을 주고 채팅을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "chat": {
                        "type": "STRING",
                        "description": "NPC가 말할 채팅을 입력합니다."
                    },
                    "target": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "아이템을 줄 캐릭터를 입력합니다."
                    },
                    "item": {
                        "type": "STRING",
                        "enum": item_list,
                        "description": "줄 아이템을 입력합니다."
                    },
                    "num": {
                        "type": "INTEGER",
                        "description": "줄 아이템의 개수를 입력합니다."
                    }
                },
                "required": ["name", "chat", "target", "item", "num"]
            }
        }

def call_character(npc_name, character_list, provider):
    if provider == "anthropic":
        return {
            "name": "call_character",
            "description": "NPC가 다른 캐릭터를 불러오는 행동을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "string",
                        "enum": character_list,
                        "description": "불러올 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "NPC가 캐릭터를 부르는 말을 입력합니다."
                    }
                },
                "required": ["name", "target"]
            }
        }
    elif provider == "google":
        return {
            "name": "call_character",
            "description": "NPC가 다른 캐릭터를 불러오는 행동을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "불러올 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "NPC가 캐릭터를 부르는 말을 입력합니다."
                    }
                },
                "required": ["name", "target"]
            }
        }

def move_map(npc_name, map_list, provider):
    if provider == "anthropic":
        return {
            "name": "move_map",
            "description": "NPC가 다른 맵으로 이동하는 행동을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "map": {
                        "type": "string",
                        "enum": map_list,
                        "description": "이동할 맵을 입력합니다."
                    },
                    "behavior": {
                        "type": "string",
                        "description": "이동한 맵에서 하는 행동을 입력합니다."
                    }
                },
                "required": ["name", "map"]
            }
        }
    elif provider == "google":
        return {
            "name": "move_map",
            "description": "NPC가 다른 맵으로 이동하는 행동을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "map": {
                        "type": "STRING",
                        "enum": map_list,
                        "description": "이동할 맵을 입력합니다."
                    },
                    "behavior": {
                        "type": "STRING",
                        "description": "이동한 맵에서 하는 행동을 입력합니다."
                    }
                },
                "required": ["name", "map"]
            }
        }

def move_spot(npc_name, spot_list, provider):
    if provider == "anthropic":
        return {
            "name": "move_spot",
            "description": "NPC가 다른 위치로 이동하는 행동을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "spot": {
                        "type": "string",
                        "enum": spot_list,
                        "description": "이동할 위치를 입력합니다."
                    },
                    "behavior": {
                        "type": "string",
                        "description": "이동한 위치에서 하는 행동을 입력합니다."
                    }
                },
                "required": ["name", "spot"]
            }
        }
    elif provider == "google":
        return {
            "name": "move_spot",
            "description": "NPC가 다른 위치로 이동하는 행동을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "spot": {
                        "type": "STRING",
                        "enum": spot_list,
                        "description": "이동할 위치를 입력합니다."
                    },
                    "behavior": {
                        "type": "STRING",
                        "description": "이동한 위치에서 하는 행동을 입력합니다."
                    }
                },
                "required": ["name", "spot"]
            }
        }

def initiate_battle(npc_name, character_list, provider):
    if provider == "anthropic":
        return {
            "name": "initiate_battle",
            "description": "NPC가 캐릭터와 포켓몬 배틀을 시작하는 행동을 생성합니다.",
            "input_schema":{
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "string",
                        "enum": character_list,
                        "description": "배틀을 시작할 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "string",
                        "description": "NPC가 배틀을 시작할 때의 대사를 입력합니다."
                    }
                },
                "required": ["name", "target", "chat"]
            }
        }
    elif provider == "google":
        return {
            "name": "initiate_battle",
            "description": "NPC가 캐릭터와 포켓몬 배틀을 시작하는 행동을 생성합니다.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING",
                        "enum": [npc_name],
                        "description": "NPC의 이름을 입력합니다."
                    },
                    "target": {
                        "type": "STRING",
                        "enum": character_list,
                        "description": "배틀을 시작할 캐릭터를 입력합니다."
                    },
                    "chat": {
                        "type": "STRING",
                        "description": "NPC가 배틀을 시작할 때의 대사를 입력합니다."
                    }
                },
                "required": ["name", "target", "chat"]
            }
        }
    

def choose_action(npc_name, untalkable_character_list, talkable_character_list, map_list, spot_list, pokemon_list, item_list, battle_available, provider):
    tools = []
    if len(talkable_character_list) >= 1:
        tools.append(speak(npc_name, talkable_character_list, provider))
        if len(pokemon_list) >= 1:
            tools.append(give_pokemon(npc_name, pokemon_list, talkable_character_list, provider))
        if len(item_list) != 0:
            tools.append(give_item(npc_name, item_list, talkable_character_list, provider))
    if len(untalkable_character_list) >= 1:
        tools.append(call_character(npc_name, untalkable_character_list, provider))
    if len(map_list) >= 1:
        tools.append(move_map(npc_name, map_list, provider))
    if len(spot_list) >= 1:
        tools.append(move_spot(npc_name, spot_list, provider))
    if battle_available:
        tools.append(initiate_battle(npc_name, talkable_character_list, provider))
    return tools