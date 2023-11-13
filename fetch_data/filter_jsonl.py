from parse import sample_data_stream
import json
from pathlib import Path

from tqdm import tqdm

DATASET_PATH = Path('data')

def main():
    with (
        open(DATASET_PATH / 'dataset_week.jsonl') as infile,
        tqdm() as pbar
    ):
        for line in infile:
            change = json.loads(line)
            if sample_data_stream(change):
                with open(DATASET_PATH / 'dataset_week20_1.jsonl', 'a') as outfile:
                    json.dump(change, outfile)
                    outfile.write('\n')
            pbar.update()


if __name__ == "__main__":
    main()
