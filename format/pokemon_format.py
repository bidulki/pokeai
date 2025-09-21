from pydantic import BaseModel
from typing import Literal, Union

def speak(pokemon_name, character_list):
    class Speak(BaseModel):
        type: Literal["speak"]
        name: Literal[pokemon_name] # type: ignore
        target: Literal[tuple(character_list)] # type: ignore
        chat: str

    return Speak