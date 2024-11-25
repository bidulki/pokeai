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
        response_json['chatHistory'] = self.chat_history
        return response_json

    def __call__(self):
        if self.user_action.action == "quit":
            end_message = self.make_message("system", f"{self.user.name}이/가 대화를 종료했다.")
            self.chat_history.append(end_message)
            output = PokeChatOutput(narration="")
            
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
            poke_chat_prompt = POKE_CHAT_PROMPT.format(
                name=self.pokemon.name, 
                info=self.pokemon.info,
                user_name=self.user.name,
                first_pokemon_info= first_pokemon_info ,
                location = self.location.name,
                location_info = self.location.description
                )
            total_messages = self.make_total_messages(poke_chat_prompt, messages)
            print(total_messages)
            output = self.get_response(total_messages, PokeChatOutput)
            output_message = self.make_message("assistant", output.narration)
            self.chat_history.append(output_message)

        response = self.make_response(output)
        return response

