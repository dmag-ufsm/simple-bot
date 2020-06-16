import json
import time
import pandas
import math

# from watchdog.observers import Observer
# BugFix use this if the same event is being fired multiple times when using Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler
import sys


class BotInputHandler(PatternMatchingEventHandler):
    patterns = ["*/game_status.json"]

    def __init__(self, cards, weights):
        self.cards_data = cards
        self.weights_data = weights

    # takes action when game_status.json updated or created
    @staticmethod
    def process(event):
        print(event.src_path, event.event_type)
        game_state, player_state = read_json('./game_info/game_status.json', '0')
        print(game_state)
        print(player_state)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


# open json file
def read_json(path, player_id):
    with open(path) as json_file:
        data = json.load(json_file)

    game_status = data['game']
    player_status = data['players'][player_id]

    return game_status, player_status


# remove card names underline
def transform_card_names(data):
    cards = data.loc[0: 77, 'card_name']
    for index in range(77):
        cards.loc[index] = cards.loc[index].replace('_', ' ')


# transformation by removing '*' and replacing nan with 1
def transform_cards_weight(data):
    for index in range(1, 79):
        weight = data['Military Strategy'][index]

        if isinstance(weight, str):
            weight = weight.replace('*', '')

        elif math.isnan(weight):
            weight = 1

        data['Military Strategy'][index] = weight


if __name__ == '__main__':

    cards_data = pandas.read_csv('./data/cards.csv')
    weight_cards_data = pandas.read_csv('./data/weightPerCard.csv')

    transform_card_names(cards_data)
    transform_cards_weight(weight_cards_data)

    args = sys.argv[1:]
    observer = Observer()
    observer.event_queue.maxsize = 0
    observer.schedule(BotInputHandler(cards_data, weight_cards_data), path=args[0] if args else '.')
    observer.start()

    # watch for changes in game_status.json
    print('Watching {} ...'.format(args[0]))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
