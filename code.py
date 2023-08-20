from src.config import config
from src.train_board import TrainBoard
from src.metro_api import MetroApi, MetroApiOnFireException
from src.wifi import init_wifi
from adafruit_datetime import datetime, timedelta


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
train_board = TrainBoard(wifi)
mode = 1

next_refresh = datetime.now()

while True:
    
    button_up.update()
    button_down.update()
    if button_up.fell:
        mode += 1 
        print(mode)
    if button_down.fell:
        mode -= 1 
        print(mode)
    
    if mode == 1 and datetime.now() >= next_refresh:
        print("Refreshing the board.....")
        upated_successful = train_board.refresh()
        time_change = timedelta(seconds=config["refresh_interval"])
        next_refresh = datetime.now() + time_change
        print(f"Next refresh at {next_refresh}")
       
      
        

