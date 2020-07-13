#!/usr/bin/python3 

import json
import time
import pandas
import math
import bot

# from watchdog.observers import Observer
# BugFix use this if the same event is being fired multiple times when using Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
import sys

class BotInputHandler(PatternMatchingEventHandler):
    patterns = [sys.argv[1] + '/game_status.json']

    def __init__(self, cards, weights, bot_id, path_bot_log):
        super().__init__()
        self.card_data = cards
        self.weights_data = weights
        self.bot_id = bot_id
        self.path_bot_log = path_bot_log

    # takes action when game_status.json updated or created
    def process(self, event):
        print(event.src_path, event.event_type)
        game_state, players_state = read_json('../Game/io/game_status.json')
        # game_state, players_state = read_json('game_info/game_status.json')

        # # calls the bot module to make some action
        bot.play(self.card_data, self.weights_data, game_state, players_state, self.bot_id, self.path_bot_log)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


# open json file
def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)

    game_status = data['game']
    players_status = data['players']

    return game_status, players_status


# remove card names underline
def transform_card_names(data):
    cards = data.loc[0: 78, 'card_name']
    for index in range(78):
        print(cards.loc[index])
        cards.loc[index] = cards.loc[index].replace('_', ' ')


# transformation by removing '*' and replacing nan with 1
def transform_cards_weight(data):
    weights = data.loc[:, 'card_weight']

    for i in range(0, len(weights) - 1):
        weight = data.loc[i, 'card_weight']

        if isinstance(weight, str):
            weight = weight.replace('*', '')
        elif math.isnan(weight):
            weight = 1

        data.loc[i, 'card_weight'] = weight


if __name__ == '__main__':

    cards_data = pandas.read_csv('./data/cards.csv')
    weight_cards_data = pandas.read_csv('./data/weights_military.csv')

    transform_card_names(cards_data)
    transform_cards_weight(weight_cards_data)

    args = sys.argv[1:]
    if len(args) != 2:
        print('$ main.py <pasta io> <bot_id>')
        sys.exit()

    # create directory for bot match log
    dir_path = './match_logs/bot_{}/'.format(int(args[1]) + 1)
    file_name = 'match_{}.csv'.format(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))

    empty_csv = pandas.DataFrame(columns=['card_1', 'card_2', 'card_3', 'card_4', 'card_5', 'card_6', 'card_7', 'card_played', 'action'])
    empty_csv.to_csv(dir_path + file_name, index=False, header=True)

    observer = Observer()
    observer.event_queue.maxsize = 0
    observer.schedule(BotInputHandler(cards_data, weight_cards_data, int(args[1]), dir_path + file_name), path=args[0] if args else '.')
    observer.start()

    # watch for changes in game_status.json
    print('Watching {} ...'.format(args[0]))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
