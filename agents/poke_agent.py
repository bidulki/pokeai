from pydantic import BaseModel
from entity import Pokemon
from agents import Agent
from prompts import POKE_CHAT_PROMPT

class PokeChatOutput(BaseModel):
    narration: str

class PokeAgent(Agent):
    def __init__(self, poke_chat):
        super().__init__(poke_chat.conversation)
        self.pokemon = Pokemon(poke_chat.pokeInfo)
        self.name = self.pokemon.name
        self.load_vectorDB()

    def load_vectorDB(self):
        # vectorDB 로딩
        pass

    def update_vectorDB(self):
        # 대화 종료시 chatHistory를 벡터 DB에 업로드
        pass

    def search_vectorDB(self):
        # 정보를 벡터 DB에서 검색
        pass

    def make_response(self, output):
        response_json = {}
        response_json['narration'] = output.narration
        return response_json

    def __call__(self):
        if self.user_action.action == "quit":
            self.update_vectorDB()
            output = PokeChatOutput(emotion=None, naration=None)
        else:
            user_action = self.user_action_message(self.name)
            self.chat_history.append(user_action)
            messages = self.chat_history
            # searched = self.search_vectorDB()
            # messages.append(searched)
            
            if self.user.first_pokemon == None:
                first_pokemon_info = "없음"
            else:
                first_pokemon_info = self.user.first_pokemon.info
            poke_chat_prompt = POKE_CHAT_PROMPT.format(
                name=self.pokemon.name, 
                info=self.pokemon.info,
                user_name=self.user.name,
                first_pokemon_info= first_pokemon_info 
                )
            total_messages = self.make_total_messages(poke_chat_prompt, messages)
            print(total_messages)
            output = self.get_response(total_messages, PokeChatOutput)

        response = self.make_response(output)
        return response

