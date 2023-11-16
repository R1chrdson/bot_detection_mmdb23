import json
from pathlib import Path

from tqdm import tqdm
import pandas as pd
DATASET_PATH = Path('data')


def main():
    validation_set = pd.read_csv('data/validation_set_transformed.csv')
    whitelist_users = set(validation_set['user'].tolist())
    dataset_in_file = DATASET_PATH / 'dataset_2weeks.jsonl'
    dataset_out_file = DATASET_PATH / 'dataset_validation_stream.jsonl'
    with (
        open(dataset_in_file) as infile,
        open(dataset_out_file, 'w') as outfile,
    ):
        for line in tqdm(infile, total=sum(1 for _ in open(dataset_in_file))):
            change = json.loads(line)
            if (change['user'] in whitelist_users):
                json.dump(change, outfile)
                outfile.write('\n')


if __name__ == "__main__":
    main()
