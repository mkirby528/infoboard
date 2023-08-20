from src.config import config
from src.train_board import TrainBoard
from src.metro_api import MetroApi, MetroApiOnFireException
from src.wifi import init_wifi

wifi = init_wifi()
train_board = TrainBoard(wifi)

train_board.run_board()

