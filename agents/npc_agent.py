from pydantic import BaseModel
from entity import NPC
from agents import Agent
from typing import List
from prompts import NPC_CHAT_PROMPT

class NpcChatOutput(BaseModel):
    message: str
    choices: List[str]

class NPCAgent(Agent):
    def __init__(self, npc_chat):
        super().__init__(npc_chat.conversation)
        self.npc = NPC(npc_chat.npcInfo)
        self.name = self.npc.name
    
    def make_response(self, output):
        response_json = {}
        response_json['message'] = output.message
        response_json['choices'] = output.choices
        return response_json
    
    def __call__(self):
        if self.user_action.action == "quit":
            output = NpcChatOutput(message="", choices=[])
        else:
            user_action = self.user_action_message(self.name)
            self.chat_history.append(user_action)
            messages = self.chat_history

            if self.user.first_pokemon == None:
                first_pokemon_info = "없음"
            else:
                first_pokemon_info = self.user.first_pokemon.info
            npc_chat_prompt = NPC_CHAT_PROMPT.format(
                name=self.npc.name,
                info=self.npc.info,
                user_name=self.user.name,
                first_pokemon_info= first_pokemon_info
            )
            total_messages = self.make_total_messages(npc_chat_prompt, messages)
            print(total_messages)
            output = self.get_response(total_messages, NpcChatOutput)
        response = self.make_response(output)
        return response

