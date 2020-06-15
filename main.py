import json
import time

# from watchdog.observers import Observer
# BugFix use this if the same event is being fired multiple times when using Observer
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler
import sys


class JSONHandler(PatternMatchingEventHandler):
    patterns = ["*/game_status.json"]

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


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.event_queue.maxsize = 0
    observer.schedule(JSONHandler(), path=args[0] if args else '.')
    observer.start()

    # watch for changes in game_status.json
    print('Watching {} ...'.format(args[0]))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



