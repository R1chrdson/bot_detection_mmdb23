import json
from pathlib import Path

from helpers.graceful_killer import GracefulKiller
from pywikibot.comms.eventstreams import EventStreams
from tqdm import tqdm

DATASET_PATH = Path('data')


def sample_data_stream(change: dict, keep_percent:int = 20) -> bool:
    """
    Whether to keep the change in the dataset according to the sampling strategy
    """
    return hash(change['user']) % 100 > (99 - keep_percent)


def main():
    killer = GracefulKiller()

    stream = EventStreams(streams=['recentchange'], since='2023-10-07T12:43:00Z')
    stream.register_filter(server_name='en.wikipedia.org')
    stream.register_filter(sample_data_stream)

    with tqdm() as pbar:
        with open(DATASET_PATH / 'dataset.jsonl', 'a') as outfile:
            while not killer.kill_now:
                change = next(stream)
                json.dump(change, outfile)
                outfile.write('\n')
                pbar.update()


if __name__ == "__main__":
    main()
