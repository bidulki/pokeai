from pydantic import BaseModel
from typing import Literal, Union

def speak(npc_name, character_list):
    class Speak(BaseModel):
        type: Literal["speak"]
        name: Literal[npc_name] # type: ignore
        target: Literal[tuple(character_list)] # type: ignore
        chat: str

    return Speak

def give_pokemon(npc_name, pokemon_list, character_list):
    class GivePokemon(BaseModel):
        type: Literal["give_pokemon"]
        name: Literal[npc_name] # type: ignore
        chat: str
        target: Literal[tuple(character_list)] # type: ignore
        pokemon: Literal[tuple(pokemon_list)] # type: ignore
    
    return GivePokemon

def give_item(npc_name, item_list, character_list):
    class GiveItem(BaseModel):
        type: Literal["give_item"]
        name: Literal[npc_name] # type: ignore
        chat: str
        target: Literal[tuple(character_list)] # type: ignore
        item: Literal[tuple(item_list)] # type: ignore
        num: int
    
    return GiveItem

def choose_action(npc_name, character_list, pokemon_list, item_list):
    action_list = [speak(npc_name, character_list)]
    if len(pokemon_list) >= 1:
        action_list.append(give_pokemon(npc_name, pokemon_list, character_list))
    if len(item_list) != 0:
        action_list.append(give_item(npc_name, item_list, character_list))
    class ChooseAction(BaseModel):
        action: Union[tuple(action_list)] # type: ignore
    
    return ChooseAction