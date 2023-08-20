import time

from src.config import config
from src.secrets import secrets
from src.config import config
class MetroApiOnFireException(Exception):
    pass

class MetroApi:
    def __init__(self) -> None:
        self.STATION_CODES = config['metro_station_codes']
        self.TRAIN_GROUPS_1 = list(zip(self.STATION_CODES, config['train_groups_1']))
        self.TRAIN_GROUPS_2 = list(zip(self.STATION_CODES, config['train_groups_2']))
        self.TRAIN_GROUPS = self.TRAIN_GROUPS_1
    
    def refresh_trains(self,wifi) -> [dict]:
        try:
            trains = self.fetch_train_predictions(wifi, self.STATION_CODES, self.TRAIN_GROUPS)
            if self.TRAIN_GROUPS == self.TRAIN_GROUPS_1:
                self.TRAIN_GROUPS = self.TRAIN_GROUPS_2
            else:
                self.TRAIN_GROUPS = self.TRAIN_GROUPS_1

        except MetroApiOnFireException:
            print(config['source_api'] + ' API might be on fire. Resetting wifi ...')
            wifi.reset()
            return None
        return trains

    def fetch_train_predictions(self, wifi, station_codes, groups) -> [dict]:
        return self._fetch_train_predictions(wifi, station_codes, groups, retry_attempt=0)

    def _fetch_train_predictions(self, wifi, station_codes, groups,retry_attempt: int) -> [dict]:
        try:
            print(f'Fetching metro info... for train group {groups}')
            start = time.time()

            if config['source_api'] == 'WMATA':
                # WMATA Method
                api_url = config['wmata_api_url'] + ','.join(set(station_codes))
                response = wifi.get(api_url, headers={'api_key': config['wmata_api_key']}, timeout=30).json()
                trains = list(filter(lambda t: (t['LocationCode'], t['Group']) in groups, response['Trains']))

            print('Received response from ' + config['source_api'] + ' api...')
            TIME_BUFFER = round((time.time() - start)/60) + 1
            trains = [self._normalize_train_response(t, TIME_BUFFER) for t in trains]
            
           
            
            if len(groups) > 1:
                trains = sorted(trains, key=lambda t: self.arrival_map(t['arrival']))
            
            print("Trains returned by api: " + str(trains))
            print('Time to Update: ' + str(time.time() - start))
            return trains

        except Exception as e:
            print(e)
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return self._fetch_train_predictions(wifi, station_codes, groups,retry_attempt + 1)
            else:
                raise MetroApiOnFireException()

    def arrival_map(self, arr):
        if arr == 'BRD':
            return 0
        elif arr == 'ARR':
            return 1
        elif arr.isdigit():
            return int(arr)
        else:
            return 100 # DLY would fall into this case, but not sure how to handle it without storing what the previous time was

    def _normalize_train_response(self, train: dict, buff:int) -> dict:
        line = train['Line']
        destination = train['Destination']
        loc = train['LocationCode']

        arrival = train["Min"]
       
        
        if arrival.isdigit():
            arrival = int(arrival) - buff
            if arrival <= 0:
                arrival = 'ARR'
            else:
                arrival = str(arrival)



        return {
            'line_color': self._get_line_color(line),
            'destination': destination[:config['destination_max_characters']],
            'arrival': arrival,
            'loc': loc
        }

    def _get_line_color(self, line: str) -> int:
        if line == 'RD':
            return 0xFF0000
        elif line == 'OR':
            return 0xFF5500
        elif line == 'YL':
            return 0xFFFF00
        elif line == 'GR':
            return 0x00FF00
        elif line == 'BL':
            return 0x0000FF
        else:
            return 0xAAAAAA
