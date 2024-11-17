from openai import OpenAI
from pydantic import BaseModel
from entity import Pokemon
from agent import Agent

class PokeAgent(Agent):
    def __init__(self, poke_chat):
        super().__init__(poke_chat.conversation)
        self.pokemon = Pokemon(poke_chat.pokeInfo)    
