from adafruit_bitmap_font import bitmap_font

config = {
    #########################
    # Network Configuration #
    #########################

    # WIFI Network SSID
    'wifi_ssid': "",

    # WIFI Password
    'wifi_password': '',

    #########################
    # Metro Configuration   #
    #########################
    'source_api': 'WMATA', # WMATA or MetroHero

    # WMATA / MetroHero API Key
    'wmata_api_key': '',

    # Metro Station Codes
    'metro_station_codes': ['C05'],

    # Metro Train Groups
    'swap_train_groups': True,
    'train_groups_1': ['1'],
    'train_groups_2': ['2'],


    # Walking Distance Times, ignore trains arriving in less than this time

    # WMATA API
    'wmata_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',

    # # MetroHero API

    'metro_api_retries': 5,
    'refresh_interval': 5, # 5 seconds is a good middle ground for updates, as the processor takes its sweet ol time




    #########################
    # Display Configuration #
    #########################
    'matrix_width': 64,
    'num_trains': 3,
    'font': bitmap_font.load_font('lib/5x7.bdf'),

    'character_width': 5,
    'character_height': 6,
    'text_padding': 2,
    'text_color': 0xFFFFFF,

    'loading_destination_text': 'Loading',
    'loading_min_text': '---',
    'loading_line_color': 0xFF00FF, # Something something Purple Line joke

    'heading_text': '   Rosslyn   ',
    'heading_color': 0x00FFFF,

    'train_line_height': 6,
    'train_line_width': 6,

    'min_label_characters': 3,
    'destination_max_characters': 8,
}