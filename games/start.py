from utils import print_and_wait
import os
import shutil

class Start:
    def __init__(self, savedata_dir):
        self.savedata_dir = savedata_dir
        print_and_wait("『포켓몬스터 AI』")
        print_and_wait("게임을 시작한다")
        self.check_savedata()

    def check_savedata(self):
        if os.path.isdir(self.savedata_dir):
            self.continue_or_restart()
        else:
            self.new()
    
    def continue_or_restart(self):
        select = input("1. 모험을 계속한다\n2. 새로운 모험을 시작한다\n입력: ")
        input(">>")
        if select == "1":
            pass
        elif select == "2":
            select2 = input("기존 데이터가 삭제됩니다. 괜찮습니까?\n1. 예 2. 아니오\n입력: ")
            input(">>")
            if select2 == "1":
                shutil.rmtree(self.savedata_dir)
                self.new()
            else:
                self.continue_or_restart()
        else:
            self.continue_or_restart()

    def new(self):
        print_and_wait("오박사: 포켓몬스터의 세계에 잘 왔다!")
        print_and_wait("나는 포켓몬 박사로 존경받는 오박사란다!")
        print_and_wait("그리고 이 세계에는 포켓몬이라고 불리는 생명체가 도처에 살고있다!")
        print_and_wait("사람들은 이 포켓몬이라는 생명체를 애완동물로 기르거나 승부를 하지만......")
        print_and_wait("나는 포켓몬을 전문적으로 연구하고 있지!")
        print_and_wait("자... 그러면 이제 너에 대해 알려다오")
        print_and_wait("너의 이름은 뭐지?")
        print_and_wait(f"음... 『레드』 이구나?")
        print_and_wait(f"레드! 준비는 되었는가?")        
        print_and_wait("드디어 이제부터 너의 이야기가 시작되어진다")
        print_and_wait("즐거운 것도 괴로운 것도 잔뜩 널 기다리고 있을 것이다!")
        print_and_wait("꿈과 모험과! 포켓몬스터의 세계로")
        print_and_wait("렛츠 고!")
