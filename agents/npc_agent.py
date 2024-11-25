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
        response_json['chatHistory'] = self.chat_history
        return response_json
    
    def __call__(self):
        if self.user_action.action == "quit":
            end_message = self.make_message("system", f"{self.user.name}이/가 대화를 종료했다.")
            self.chat_history.append(end_message)
            output = NpcChatOutput(message="", choices=[])
        elif self.user_action.action == "chat":
            user_action = self.user_action_message(self.name)
            if user_action['content']==None:
                start_message = self.make_message("system", f"{self.user.name}이/가 대화를 걸어왔다.")
                self.chat_history.append(start_message)
            else:
                self.chat_history.append(user_action)
            messages = self.chat_history

            if self.user.first_pokemon == None:
                first_pokemon_info = f"{self.user.name}은 현재 데리고 다니는 포켓몬이 없다."
            else:
                first_pokemon_info = f"{self.user.name}은 한 포켓몬을 꺼내서 데리고 다니고 있다. 그 포켓몬에 대한 정보는 다음과 같다.\n{self.user.first_pokemon.info}"
            npc_chat_prompt = NPC_CHAT_PROMPT.format(
                name=self.npc.name,
                info=self.npc.info,
                user_name=self.user.name,
                first_pokemon_info= first_pokemon_info,
                location = self.location.name,
                location_info = self.location.description
            )
            total_messages = self.make_total_messages(npc_chat_prompt, messages)
            print(total_messages)
            output = self.get_response(total_messages, NpcChatOutput)
            output_message = self.make_message("assistant", output.message)
            self.chat_history.append(output_message)
        response = self.make_response(output)
        return response

