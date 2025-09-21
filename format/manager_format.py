from pydantic import BaseModel
from typing import Literal, Union

def choose_character(character_list):
    class ChooseCharacter(BaseModel):
        type: Literal["choose_character"]
        reason: str
        name: Literal[tuple(character_list)] # type: ignore

    return ChooseCharacter 

class RecommendUserChat(BaseModel):
    type: Literal["recommend_user_chat"]
    name: Literal["레드"]
    chat: str

class NextScene(BaseModel):
    type: Literal["next_scene"]

def choose_action(character_list):
    action_list = [NextScene]
    if len(character_list) >= 1:
        action_list.append(choose_character(character_list))
   
    class ChooseAction(BaseModel):
        action: Union[tuple(action_list)] # type: ignore
    
    return ChooseAction