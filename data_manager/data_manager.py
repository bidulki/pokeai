import os
from .basic_data_manager import BasicDataManager
from .user_data_manager import UserDataManager
from .npc_data_manager import NPCDataManager
from .pokemon_data_manager import PokemonDataManager
from .map_data_manager import MapDataManager
from .item_data_manager import ItemDataManager
from .pokedex_data_manager import PokedexDataManager

class DataManager(BasicDataManager):
    @classmethod
    def load(cls, savedata_dir, gamedata_dir):
        data = dict()

        userdata_dir = os.path.join(savedata_dir, "user")
        pokemondata_dir = os.path.join(savedata_dir, "pokemon")
        npcdata_dir = os.path.join(savedata_dir, "npc")
        mapdata_dir = os.path.join(savedata_dir, "map")
        pokedex_dir = os.path.join(savedata_dir, "pokedex")
        
        pokemon_gamedata_dir = os.path.join(gamedata_dir, "pokemon")
        npc_gamedata_dir = os.path.join(gamedata_dir, "npc")
        map_gamedata_dir = os.path.join(gamedata_dir, "map")
        item_gamedata_dir = os.path.join(gamedata_dir, "item")
        pokedex_game_data_dir = os.path.join(gamedata_dir, "pokedex")
        
        data = {
            "user": UserDataManager.load(userdata_dir),
            "item": ItemDataManager.load(item_gamedata_dir),
            "pokedex": PokedexDataManager.load(pokedex_dir, pokedex_game_data_dir),
            "pokemon": PokemonDataManager.load(pokemondata_dir, pokemon_gamedata_dir),
            "npc": NPCDataManager.load(npcdata_dir, npc_gamedata_dir),
            "map": MapDataManager.load(mapdata_dir, map_gamedata_dir),
        }

        return data

    @classmethod
    def save(cls, savedata_dir, data):
        userdata_dir = os.path.join(savedata_dir, "user")
        pokemondata_dir = os.path.join(savedata_dir, "pokemon")
        npcdata_dir = os.path.join(savedata_dir, "npc")
        mapdata_dir = os.path.join(savedata_dir, "map")
        pokedexdata_dir = os.path.join(savedata_dir, "pokedex")

        UserDataManager.save(userdata_dir, data['user'])
        PokemonDataManager.save(pokemondata_dir, data['pokemon'])
        NPCDataManager.save(npcdata_dir, data['npc'])
        MapDataManager.save(mapdata_dir, data['map'])
        PokedexDataManager.save(pokedexdata_dir, data['pokedex'])