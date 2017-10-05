import argparse
import sys
import pandas as pd
import os
import json


parser = argparse.ArgumentParser()
parser.add_argument("--src", metavar="source",
                    help="Source file - csv")
parser.add_argument("--dest", metavar="destinantion",
                    help="""Destination file name 
                            (specify along with path to destinantion folder).""")
parser.add_argument("--key", metavar="key column",
                    help="key column in csv file")
parser.add_argument("--compress", metavar="compress key",
                    help="""Compress the keys or not (default: True)
                         Possible inputs:
                            True: true, t, yes, y, 1
                            False: false, f, no, n, 0
                         Note: Possible inputs are not case sensitive.""")
args = parser.parse_args()


def str2bool(s2b):
    """
    Converts String to boolean
    params:
        s2b - a string parameter to be converted to boolean
        Possible inputs:
            True: true, t, yes, y, 1
            False: false, f, no, n, 0
        Note: Possible inputs are not case sensitive.
    returns: True or False
    """
    if s2b == None:
        return True
    if s2b.lower() in ('true', 't', 'yes', 'y', '1'):
        return True
    if s2b.lower() in ('false', 'f', 'no', 'n', '0'):
        return False
    ValueError('Error: Incorrect Compress Value')


def generate_keys(df, key_col, compress=True):
    """
    Generate keys for the json dictionary of elements
    params:
        df: pandas.DataFrame object of the CSV file
        key_col: Column to be taken as keys
        compress: Keyword argument - if true keys are compressed as follows:
                  key "John Doe" is converted to JD and if JD is already in 
                  list then it is converted to JD2 and so on.
    returns: list of keys
    """
    if not compress:
        return list(df[key_col])

    # compress keys
    keys = []
    for key in df[key_col]:
        st = ''.join([s[0] for s in key.split()])
        if st in keys:
            i = 2
            while (st + str(i)) in keys:
                st += 1
            st = st + str(i)
        keys.append(st)
    return keys


def df_to_json(df, head_name, key_col, compress=True):
    """
    Convert pandas.DataFrame object to a JSON.
    params:
        df: pandas.DataFrame object to be converted
        head_name: Top Most key of JSON
        key_col: Keys Column for key-value pair of row-wise details
        compress: Keyword argument - if true keys are compressed as follows:
                  key "John Doe" is converted to JD and if JD is already in 
                  list then it is converted to JD2 and so on.
    returns: json dictionary of the DataFrame
        Note: JSON Format-
            {
                head_name: {
                    "keys": ["key1", "key2"...],
                    "details": {
                        "key1": # details of row 1 as dictionary,
                        "key2": # details of row 2 as dictionary,
                        ...
                    }
                }
            }
    """
    json_dict = {}
    keys = generate_keys(df, key_col,
                         compress=compress)
    json_dict[head_name] = { 
            "keys": keys,
            "details": {}
    }

    for r in range(df.shape[0]):
        dt = df.loc[r].astype(str).to_dict()
        json_dict[head_name]["details"][keys[r]] = dt
    return json_dict


if args.src == None:
    sys.exit("Error: Path source file Missing")


if args.dest == None:
    args.dest = args.src.split('.')[-2] + '.json'


if '.json' not in args.dest.split('\\')[-1]:
    args.dest = args.dest + args.src.split('\\')[-1].split('.')[-2] + '.json'


df = pd.read_csv(args.src)

if args.key not in list(df.columns.values):
    sys.exit("Error: Key Column Missing")


head_name = args.dest.split('\\')[-1].split('.')[-2]
with open(args.dest, 'w') as outfile:
    json.dump(df_to_json(df, head_name, 
                          args.key, 
                          compress=str2bool(args.compress)),
                          outfile)