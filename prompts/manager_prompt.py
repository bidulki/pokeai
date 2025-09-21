MANAGER_SYSTEM_PROMPT="""You are an Agent in the Pokémon game.
Your role is to select appropriate functions considering the current situation.
"""

CHOOSE_ACTION_PROMPT="""
**Current Game State Information**
    - Current map: {current_map_name}
    - Details: {current_map_info}
    - Character information in map: {character_info}
    - Player character: 레드 (cannot be directly controlled)

**Action Selection**
    Analyze the current situation and call one of the following two functions:

    1. choose_character(character_name)
        - Purpose: Activate an NPC character to progress the game
        - Required conditions:
            - Only NPCs other than the player character (레드) can be selected
            - If one character has been speaking continuously, another character must be selected to maintain conversation diversity

        - Character action options:
            - Pokémon transfer: Can give possessed Pokémon to another character
            - Item transfer: Can give items in inventory to another character
            - Dialogue progression: Provide information or hints necessary for story progression
            - Map movement: Move to another map
            - Spot movement: Move to another spot within the same map
            - Call character: Call a character from a distance to start a conversation

    2. next_scene
        - Purpose: End current interaction and proceed to the next step
        - Even if the player character (레드) does not respond, if conditions are satisfied, call next_scene.
        - Call conditions:
            - When an NPC has completed delivery of key information/items (additional conversation unnecessary)
            - When the player or NPC shows clear farewell greetings or intention to end the conversation
            - When no new information is provided in the current conversation
            - When repetitive conversation patterns occur
"""

RECOMMEND_USER_CHAT_PROMPT="""현재 게임 상황:
- 현재 맵: {current_map_name}: {current_map_info}
- 현재 맵에 있는 캐릭터에 대한 설명: {character_info}

플레이어(레드)가 현재 상대방에게 할 적절한 대사를 추천합니다.
단 레드는 혼잣말을 하지 않습니다.
"""
