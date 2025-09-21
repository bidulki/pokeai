from entity import Move
import random
import json
import os

class Pokemon:
    def __init__(self):
        self.type = "pokemon"

    def make_pokemon(self, pokedex, level, master, map, status, hp=None):
        self.name = pokedex
        self.map = map
        self.pokedex = pokedex
        self.level = level
        self.master = master
        self.status = status
        self.hp = hp
        self.exp = 0
        self.Ivs = None
        self.Evs = None
        self.chat_history = []
        self.load_pokedex()
        self.load_stats()
        self.set_random_moves()
        self.set_max_exp()
    
    def load_pokemon(self, pokemon_data):
        self.type = "pokemon"
        self.name = pokemon_data['name']
        self.map = pokemon_data['map']
        self.pokedex = pokemon_data['pokedex']
        self.level = pokemon_data['level']
        self.master = pokemon_data['master']
        self.status = pokemon_data['status']
        self.hp = pokemon_data['hp']
        self.exp = pokemon_data['exp']
        self.Ivs = pokemon_data['Ivs']
        self.Evs = pokemon_data['Evs']
        self.chat_history = pokemon_data['chat_history']
        self.load_pokedex()
        self.load_stats()
        self.load_moves(pokemon_data['moves'])
        self.set_max_exp()

    def load_pokedex(self):
        pokedex_path = os.path.join("./gamedata/pokedex", f"{self.pokedex}.json")
        with open(pokedex_path, "r", encoding="utf-8") as f:
            pokedex_data = json.load(f)
        self.id = pokedex_data['id']
        self.category = pokedex_data['category']
        try:
            self.description = pokedex_data['description']
        except:
            print(f"{self.pokedex} 도감 설명이 없습니다.")
        self.types = pokedex_data['type']
        self.height = pokedex_data['height']
        self.weight = pokedex_data['weight']
        self.base_stat = pokedex_data['base_stat']
        self.evolution = pokedex_data['evolution']
        self.initial_move = pokedex_data['initial_move']
        self.learn_move = pokedex_data['learn_move']
        self.EV = pokedex_data['EV']
        self.base_exp = pokedex_data['Base_EXP']
        self.catch_rate = pokedex_data['catch_rate']
        self.grow_rate = pokedex_data['grow_rate']

    def set_Ivs(self):
        if self.Ivs == None:
            self.Ivs = {
                "HP": random.randint(0, 31),
                "Attack": random.randint(0, 31),
                "Defense": random.randint(0, 31),
                "Special Attack": random.randint(0, 31),
                "Special Defense": random.randint(0, 31),
                "Speed": random.randint(0, 31)
            }    

    def set_Evs(self):
        if self.Evs == None:
            self.Evs = {
                "HP": 0,
                "Attack": 0,
                "Defense": 0,
                "Special Attack": 0,
                "Special Defense": 0,
                "Speed": 0
            }

    def load_stats(self):
        self.set_Ivs()
        self.set_Evs()
        stat_list = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]
        self.stats = dict()
        for stat in stat_list:
            if stat == "HP":
                self.stats["HP"] = (self.base_stat["HP"]*2 + self.Ivs["HP"] + int(self.Evs["HP"]/4))
                self.stats["HP"] = int(self.stats["HP"]*self.level/100 + 10 + self.level)
            else:
                self.stats[stat] = (self.base_stat[stat]*2 + self.Ivs[stat] + int(self.Evs[stat]/4))
                self.stats[stat] = int(self.stats[stat]*self.level/100 + 5)
        
        if self.hp == None:
            self.hp = self.stats["HP"]
    
    def load_moves(self, move_name_list):
        self.moves = []
        for move_name in move_name_list:
            move = Move(move_name)
            self.moves.append(move)
    
    def set_random_moves(self):
        possible_moves = self.initial_move
        for level in self.learn_move.keys():
            if level <= self.level:
                possible_moves.append(self.learn_move[level])
        moves = random.sample(possible_moves, min(4, len(possible_moves)))
        self.load_moves(moves)
    
    def get_info(self):
        info = f"도감설명: {self.description}\n"
        info += f"체력정보: {self.get_hp_info()}\n"
        info += f"상태정보: {self.get_status_info()}\n"
        info += f"타입: {self.types}\n"
        info += f"카테고리: {self.category}\n"
        info += f"기술 정보: {self.get_moves_info()}\n"
        info += self.get_moves_info()
        return info

    def get_hp_info(self):
        hp = int(self.hp/self.stats["HP"])*100
        if hp==0:
            hp_info = f"{self.name}은 체력이 없어 기절상태이다."
        elif hp<=20:
            hp_info = f"{self.name}의 체력이 매우 부족하여 기절하기 직전이다."
        elif hp<=50:
            hp_info = f"{self.name}의 체력이 부족하지만 아직 버틸만 하다."
        elif hp<100:
            hp_info = f"{self.name}의 체력이 충분히 남아있다."
        else:
            hp_info = f"{self.name}의 체력이 가득찬 상태이다."
        return hp_info
    
    def get_status_info(self):
        if self.status == "정상":
            status_info = f"{self.name}은 상태이상에 걸리지 않았다."
        elif self.status == "독":
            status_info = f"{self.name}은 독 상태이상에 걸렸다. 독 상태에는 전투 중 매턴 전체 HP의 1/8만큼 화상 데미지를 입는다."
        elif self.status == "화상":
            status_info = f"{self.name}은 화상 상태이상에 걸렸다. 화상 상태에는 물리공격의 위력이 약해지고, 전투 중 매턴 전체 HP의 1/16만큼 화상 데미지를 입는다."
        elif self.status == "마비":
            status_info = f"{self.name}은 마비 상태이상에 걸렸다. 마비 상태에는 몸이 저려서 행동이 느려지고, 때때로 행동이 불가능하다."
        elif self.status == "잠듦":
            status_info = f"{self.name}은 잠듦 상태이상에 걸렸다. 잠듦 상태에는 잠들어 버려서 행동할 수 없다."
        elif self.status == "얼음":
            status_info = f"{self.name}은 얼음 상태이상에 걸렸다. 얼음 상태에는 몸이 얼어붙어 행동할 수 없다."
        elif self.status == "기절":
            status_info = f"{self.name}은 기절했다. 기절 상태에는 의식을 잃어 전투를 할 수 없다."
        return status_info

    def get_moves_info(self):
        moves_info = f"{self.name}의 기술 정보\n"
        for move in self.moves:
            moves_info += f"{move.description}\n"
        return moves_info
    
    def can_evolve(self, stone=None):
        if self.evolution['type'] == "impossible":
            return False
        elif self.evolution['type'] == "level":
            if self.level >= self.evolution['level']:
                return True
            else:
                return False
        elif self.evolution['type'] == "stone":
            if stone == self.evolution['stone']:
                return True
            else:
                return False
        else:
            return False
    
    def evolve(self):
        self.pokedex = self.evolution['next']
        self.load_pokedex()
    
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.set_max_exp()
        self.load_stats()

    def set_max_exp(self):
        current_total_exp = self.total_exp(self.grow_rate, self.level)
        next_total_exp = self.total_exp(self.grow_rate, self.level+1)
        self.max_exp = next_total_exp - current_total_exp
        self.max_exp = int(self.max_exp)
    
    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.max_exp:
            remain_exp = self.exp - self.max_exp
            self.level_up()
            self.set_max_exp()
            is_level_up = True
            return is_level_up, remain_exp
        else:
            is_level_up = False
            return is_level_up, 0

    def total_exp(self, grow_rate, level):
        if level == 1:
            total_exp = 0
            return total_exp

        if grow_rate == "fast":
            total_exp = (level)**3
        elif grow_rate == "medium":
            total_exp = 1.2*(level)**3 - 15*(level)**2 + 100*level - 140
        elif grow_rate == "slow":
            total_exp =  1.25*(level)**3
        return total_exp
    
    def check_learn_move(self):
        for level in self.learn_move.keys():
            if level == self.level:
                return self.learn_move[level]
        return None

    def learn_move_at_level(self, level, forget=None):
        if forget:
            self.moves.remove(forget)
        new_move = Move(self.learn_move[level])
        self.moves.append(new_move)

    def initialize_battle_status(self):
        self.confusion = False
        self.rank = {
            "Attack": 0,
            "Defense": 0,
            "Special Attack": 0,
            "Special Defense": 0,
            "Speed": 0,
            "Accuracy": 0,
            "Evasion": 0,
            "Critical": 0
        }
    
    def get_confusion(self):
        if self.confusion == True:
            return f"{self.name}은 이미 혼란상태에 빠졌다."
        else:
            self.confusion = True
            return f"{self.name}은 혼란에 빠져 있다!"
    
    def rank_name(self, rank):
        rank_name_dict = {
            "Attack": "공격",
            "Defense": "방어",
            "Special Attack": "특수공격",
            "Special Defense": "특수방어",
            "Speed": "스피드",
            "Accuracy": "명중률",
            "Evasion": "회피율",
            "Critical": "급소율"
        }
        return rank_name_dict[rank]
    
    def rank_up(self, rank, num):
        rank_name = self.rank_name(rank)
        if self.rank[rank] == 6:
            return f"{self.name}의 {rank_name}은 더 이상 오르지 않는다."
        else:
            shift_amount = min(6-self.rank[rank], num)
            self.rank[rank] += shift_amount
            if shift_amount == 1:
                return f"{self.name}의 {rank_name}이/가 올랐다."
            elif shift_amount == 2:
                return f"{self.name}의 {rank_name}이/가 크게 올랐다."
            else:
                return f"{self.name}의 {rank_name}이/가 매우 크게 올랐다."
        
    def rank_down(self, rank, num):
        rank_name = self.rank_name(rank)
        if self.rank[rank] == -6:
            return f"{self.name}의 {rank_name}은 더 이상 내려가지 않는다."
        else:
            shift_amount = min(self.rank[rank]+6, num)
            self.rank[rank] -= shift_amount
            if shift_amount == 1:
                return f"{self.name}의 {rank_name}이/가 떨어졌다."
            elif shift_amount == 2:
                return f"{self.name}의 {rank_name}이/가 크게 떨어졌다."
            else:
                return f"{self.name}의 {rank_name}이/가 매우 크게 떨어졌다."
    
    def get_status(self, status):
        status_name_dict = {
            "독": f"{self.name}의 몸에 독이 퍼졌다!",
            "화상": f"{self.name}은 화상을 입었다!",
            "마비": f"{self.name}은 마비되어 기술이 나오기 어려워졌다!",
            "잠듦": f"{self.name}은 잠들어 버렸다!",
            "얼음": f"{self.name}은 얼어붙었다!",
            "기절": f"{self.name}은 기절했다!"
        }
        return status_name_dict[status]
    
    def status_shift(self, status):
        if self.status != "정상":
            return f"{self.name}은 이미 상태이상에 걸려있다."
        else:
            self.status = status
            return self.get_status(status)

    def to_json(self):
        pokemon_data = {
            "name": self.name,
            "map": self.map,
            "pokedex": self.pokedex,
            "level": self.level,
            "master": self.master,
            "status": self.status,
            "moves": [move.name for move in self.moves],
            "hp": self.hp,
            "exp": self.exp,
            "Ivs": self.Ivs,
            "Evs": self.Evs,
            "chat_history": self.chat_history
        }
        return pokemon_data