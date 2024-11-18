from pydantic import BaseModel
from typing import Literal, List

# 포켓몬 정보
class PokeInfo(BaseModel):
    dexNum: int # 포켓몬 도감번호
    hp: int # 체력 퍼센트
    status: Literal["NOR", "PSN", "BRN", "PAR", "SLP", "FRZ"] # 상태이상: 정상, 독, 화상, 마비, 잠듦, 얼음 

# 사용자 정보
class UserInfo(BaseModel):
    name: str # 이름
    sex: Literal["male", "female"] # 성별
    firstPoke: PokeInfo # 선두 포켓몬

# 아이템 정보
class ItemInfo(BaseModel):
    id: int # 아이템 id
    num: int # 갯수

# 퀘스트 정보
class QuestInfo(BaseModel):
    info: str # 정보
    clear: bool # 클리어 여부

# 사용자 행동
class UserAction(BaseModel):
    action: Literal["chat", "battle", "give", "exchange", "catch", "quit"]
    chat: str # 사용자 chat
    itemId: int # 건네줄 물건 id
    pokemon: PokeInfo # 교환할 포켓몬

# NPC 정보
class NpcInfo(BaseModel):
    id: int # NPC id
    pokeList: List[PokeInfo] # 소지 포켓몬

# 대화 정보
class Conversation(BaseModel):
    userInfo: UserInfo # 사용자 정보
    chatHistory: list # 사용자와 NPC의 대화기록
    userAction: UserAction # 사용자의 행동
    locationId: int # 장소 id

# NPC 대화
class NpcChat(BaseModel):
    npcInfo: NpcInfo # NPC 정보
    conversation: Conversation # 대화 정보

# 포켓몬 대화
class PokeChat(BaseModel):
    pokeInfo: PokeInfo # 포켓몬 정보
    conversation: Conversation # 대화 정보
    