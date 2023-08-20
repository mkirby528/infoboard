import time
from src.config import config
from src.train_board import TrainBoard
from src.metro_api import MetroApi, MetroApiOnFireException
from src.wifi import init_wifi

import busio
import board
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

STATION_CODES = config['metro_station_codes']
TRAIN_GROUPS_1 = list(zip(STATION_CODES, config['train_groups_1']))
TRAIN_GROUPS_2 = list(zip(STATION_CODES, config['train_groups_2'])) if config['swap_train_groups'] else TRAIN_GROUPS_1
train_groups = TRAIN_GROUPS_1

train_board = TrainBoard(lambda: api.refresh_trains(train_groups,wifi))
wifi = init_wifi()
api = MetroApi()


while True:
    train_board.refresh()
    train_board.turn_on_display()
    if config['swap_train_groups']:
        train_groups = TRAIN_GROUPS_1 if train_groups == TRAIN_GROUPS_2 else TRAIN_GROUPS_2
    time.sleep(config["refresh_interval"])
