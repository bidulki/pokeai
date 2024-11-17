from fastapi import FastAPI
from config import get_settings
from model import NpcChat, PokeChat
from agents import NpcAgent, PokeAgent

app = FastAPI()

@app.get("")
async def index():
    settings = get_settings()
    return settings.env

@app.post("/api/chat/npc")
async def npc_conversation(npc_chat: NpcChat):
    npc_chat_agent = NpcAgent(npc_chat)
    response = npc_chat_agent()
    return response

@app.post("/api/chat/poke")
async def poke_conversation(poke_chat: PokeChat):
    poke_chat_agent = PokeAgent(poke_chat)
    response = poke_chat_agent()
    return response