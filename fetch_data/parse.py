import json
from pathlib import Path

from pywikibot.comms.eventstreams import EventStreams
from tqdm import tqdm

from helpers.graceful_killer import GracefulKiller

DATASET_PATH = Path('data')

killer = GracefulKiller()

stream = EventStreams(streams=['recentchange'], since='2023-11-07T12:43:00Z')
stream.register_filter(server_name='en.wikipedia.org')

with tqdm() as pbar:
    with open(DATASET_PATH / 'dataset.jsonl', 'a') as outfile:
        while not killer.kill_now:
            change = next(stream)
            json.dump(change, outfile)
            outfile.write('\n')
            pbar.update()
