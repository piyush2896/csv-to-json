# CSV to JSON
This Command Line utility Converts a CSV file to a JSON file.

## Usage
```
csv-to-json.py [-h] [--src source] [--dest destinantion]
               [--key key column] [--compress compress key]

optional arguments:
  -h, --help            show this help message and exit
  --src source          Source file - csv
  --dest destinantion   Destination file name (specify along with path to
                        destinantion folder).
  --key key column      key column in csv file
  --compress compress key
                        Compress the keys or not (default: True) Possible
                        inputs: True: true, t, yes, y, 1 False: false, f, no,
                        n, 0 Note: Possible inputs are not case sensitive.
```

## Dependencies
Only one dependency - **Pandas**