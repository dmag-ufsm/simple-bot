import json
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys

class JSONHandler(PatternMatchingEventHandler):
    patterns = ["*/game_status.json"]

    @staticmethod
    def process(event):
        print(event.src_path, event.event_type)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


# open json file in read mode
def read_json(path, player_id):
    with open(path) as json_file:
        data = json.load(json_file)

    game_status = data['game']
    player_status = data['players'][player_id]

    return game_status, player_status


## game_state, player_state = read_json('./game_info/game_status.json', '0')

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(JSONHandler(), path=args[0] if args else '.')
    observer.start()

    print('Watching {} ...'.format(args[0]))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



