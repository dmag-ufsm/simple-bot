#!/usr/bin/python3

import json
import time
import pandas
import math

# from watchdog.observers import Observer
# BugFix use this if the same event is being fired multiple times when using Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
import sys

class BotInputHandler(PatternMatchingEventHandler):
    patterns = [sys.argv[1] + '/game_status.json']

    def __init__(self):
        super().__init__()

    # takes action when game_status.json updated or created
    def process(self, event):
        print(event.src_path, event.event_type)
        # game_state, players_state = read_json('../Game/io/game_status.json')
        data = read_json('game_info/game_status.json')

        # game end
        if (data['game']['era'] == 3) & (data['game']['turn'] == 20):
            file_name = 'match_{}.json'.format(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
            with open('match_logs/match/{}'.format(file_name), 'w') as fp:
                print('saving match data...')
                json.dump(data, fp)


    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


# open json file
def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) != 1:
        print('$ main.py <pasta io>')
        sys.exit()

    observer = Observer()
    observer.event_queue.maxsize = 0
    observer.schedule(BotInputHandler(), path=args[0] if args else '.')
    observer.start()

    # watch for changes in game_status.json
    print('Watching end of match{} ...'.format(args[0]))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
