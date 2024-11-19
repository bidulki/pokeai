from pydantic import BaseModel
from entity import NPC
from agents import Agent
from typing import List, Literal

class NpcOutput(BaseModel):
    message: str
    choices: List[str]

class NPCAgent(Agent):
    def __init__(self, npc_chat):
        super().__init__(npc_chat.conversation)
        self.npc = NPC(npc_chat.npcInfo)
        self.name = self.npc.name
    
    def __call__(self):
        pass

