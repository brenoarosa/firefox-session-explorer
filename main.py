"""
Firefox Utilities

Relevant:
https://github.com/andikleen/lz4json
https://www.jeffersonscher.com/ffu/
"""

import sys
import json
import argparse
import lz4.block


def decompress(input_file, codec="utf8"):
    with open(input_file, "rb") as fin:

        filetype = fin.read(8).decode('utf8')
        if filetype != "mozLz40\x00":
            print("Not mozLz40 file.")
            sys.exit(1)

        uncompressed_sz = int.from_bytes(fin.read(4), byteorder='little')

        compressed_data = fin.read()
        uncompressed = lz4.block.decompress(compressed_data, uncompressed_size=uncompressed_sz)

    values = json.loads(uncompressed.decode(codec))
    #print(json.dumps(values, indent=4, sort_keys=True))
    return values

def extract_open_tabs(values):

    ws = values["windows"]

    for w_i, w in enumerate(ws):
        print(f"---------------- {w_i} ----------------")
        for tab in w['tabs']:
            tab_i = tab['index']
            print(tab['entries'][tab_i-1]['url'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)

    args = parser.parse_args()

    values = decompress(args.input_file)
    extract_open_tabs(values)
