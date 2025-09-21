import sys
sys.path.append("../")

from games.game import Game
from games.start import Start
from data_manager import DataManager
from utils import print_and_wait

savedata_dir = "./savedata"
gamedata_dir = "./gamedata"

if __name__ == "__main__":
    Start(savedata_dir)
    data = DataManager.load(savedata_dir, gamedata_dir)
    game = Game(savedata_dir, data)
    game.run()