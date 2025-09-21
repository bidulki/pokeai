opponent_base_exp = 75 # 상대 포켓몬 종족별 기초 경험치
opponent_type = "트레이너" # 상대의 종류 ["트레이너", "야생"]
opponent_level = 5 # 상대 포켓몬의 레벨
battle_join_num = 1 # 배틀에 참여한 나의 포켓몬 수 
# 트레이너-> 1.5배, 야생-> 1배
if opponent_type == "야생":
    exp = opponent_base_exp
else:
    exp = opponent_base_exp * 1.5

# 상대 포켓몬의 레벨에 따라 경험치 증가
exp = exp*opponent_level

# 포켓몬 경험치 분배
exp = exp/(battle_join_num*7) 
exp = int(exp)