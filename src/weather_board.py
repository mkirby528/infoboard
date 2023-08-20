import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix
from src.metro_api import MetroApi
from src.config import config


class WeatherBoard():
    def __init__(self, wifi):
        self.display = Matrix().display
        self.parent_group = displayio.Group(scale=1, x=0, y=3)
        self.heading_label = Label(config['font'], anchor_point=(0,0))
        self.heading_label.color = config['heading_color']
        self.heading_label.text="Weather"
        self.parent_group.append(self.heading_label)       
        self.wifi = wifi
                   
    def refresh(self) -> bool:
        print('Refreshing weather information...')
    
    def show(self):
        self.display.show(self.parent_group)

