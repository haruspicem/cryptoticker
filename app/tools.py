from ruamel import yaml
import pandas as pd
import os
import sys

def getConfig(config_name):
    with open("config/{}.yml".format(config_name), 'r') as stream:
        try:
            result = yaml.safe_load(stream)
            return result
        except yaml.YAMLError as exc:
            print(exc)
            return 0

def append_to_csv(batch, path, sep=",", columns=['market', 'bids', 'asks', 'ts']):
    """Append the provided dataframe to an existing one, else writes as new."""
    df = pd.DataFrame.from_records(batch, columns=columns)
    if not os.path.isfile(path):
        df.to_csv(path, mode='a', index=False, sep=sep)
    else:
        df.to_csv(path, mode='a', index=False, sep=sep, header=False)