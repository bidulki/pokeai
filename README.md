# pokeai
이 프로젝트는 포켓몬스터의 팬게임으로 NPC와 포켓몬에 생성형 AI를 접목시켜,
유저의 행동과 말에 반응하여 변화하는 게임을 목표로 하고 있습니다.

# Install
1. 가상환경 생성& 라이브러리 설치
   ```
   cd pokeai
   conda create -n pokeai python=3.9
   conda activate pokeai
   pip install -r requirements.txt
   ```
2. FASTAPI 실행
   ```
   fastapi dev
   ```
3. client 실행
   ```
   python clients/client.py
   ```



# TODO
대화 시 NPC가 먼저 말하기
아이템 주기 기능 구현
퀘스트 구현
포획 구현
배틀 구현
