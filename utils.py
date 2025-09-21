# 출력 후 대기하는 함수
def print_and_wait(content):
    print(content)
    input(">>") 

def input_and_wait(content):
    select = input(content)
    input(">>")
    return select

def get_user_input():
    text = input("*")
    if text != "":
        input(">>")
    return text

def select_yes_or_no(content):
    print(content)
    print("1: 예")
    print("2: 아니오")
    while True:
        choice = input("선택: ")
        input(">>")
        if choice == "1" or choice == "2":
            return choice
        select_yes_or_no(content)

# 유저가 리스트 중 한개를 선택하는 함수
def select_item_from_list(options:list) -> any:
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    print(f"{len(options)+1}. 그만둔다")
    while True:
        choice = input("선택: ")
        input(">>") 
        if choice.isdigit():
            index = int(choice) -1
            if 0 <= index < len(options):
                return options[index]
            elif index == len(options):
                return None
        select_item_from_list(options)

# 유저가 인벤토리 중 한개를 선택하는 함수
def select_item_from_inventory(inventory):
    for idx, item in enumerate(inventory, start=1):
        print(f"{idx}. {item[0]}: {item[1]}개")
    print(f"{len(inventory)+1}. 그만둔다")
    while True:
        choice = input("선택: ")
        input(">>")
        if choice.isdigit():
            index = int(choice) -1
            if 0 <= index < len(inventory):
                return inventory[index]
            elif index == len(inventory):
                return None
        select_item_from_inventory(inventory)
    

# 종성이 있는 지 확인하는 함수
def has_coda(word):
    return (ord(word[-1]) - 44032) % 28 == 0

# 한글인지 확인하는 함수
def is_hangul(word):
    code = ord(word[-1])
    if 44032 <= code <= 55203:
        return True
    return False

# 알맞은 조사를 붙이는 함수
def josa(word, target="가", middle=""):
    options = [["이", "가"], ["을", "를"], ["은", "는"], ["과", "와"]]
    opt = ["", ""]

    for option in options:
        if target in option:
            opt = option
    
    if not is_hangul(word):
        return word + middle + f"{opt[0]}({opt[1]})"
    
    if has_coda(word):
        return word + middle + opt[1]
    else:
        return word + middle + opt[0]
