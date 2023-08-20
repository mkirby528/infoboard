from src.config import config
from src.train_board import TrainBoard
from src.weather_board import WeatherBoard
from src.wifi import init_wifi
from adafruit_datetime import datetime


import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer


pin_down = DigitalInOut(board.BUTTON_DOWN)
pin_down.switch_to_input(pull=Pull.UP)
button_down = Debouncer(pin_down)
pin_up = DigitalInOut(board.BUTTON_UP)
pin_up.switch_to_input(pull=Pull.UP)
button_up = Debouncer(pin_up)


wifi = init_wifi()
mode = 0
boards = [TrainBoard(wifi), WeatherBoard(wifi)]


next_refresh = datetime.now()
while True:

    button_up.update()
    button_down.update()
    mode_changed = False
    if button_up.fell:
        mode = 0 if mode == len(boards) - 1 else mode + 1
        mode_changed = True
        print(mode)
    if button_down.fell:
        mode = len(boards) - 1 if mode == 0 else mode - 1
        mode_changed = True
        print(mode)
    boards[mode].show()
