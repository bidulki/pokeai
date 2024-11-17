from openai import OpenAI
from pydantic import BaseModel
from entity import NPC
from agent import Agent

class NPCAgent(Agent):
    def __init__(self, npc_chat):
        super().__init__(npc_chat.conversation)
        self.npc = NPC(npc_chat.npcInfo)    
