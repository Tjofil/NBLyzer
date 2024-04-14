# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from collections import defaultdict
from nblyzer.src.nblyzer import NBLyzer
from argparse import ArgumentParser
from nblyzer.src.events import RunBatchEvent
from nblyzer.src.resource_utils.rsrc_mngr import ResourceManager
import csv
import os
from tqdm import tqdm
import json

def benchmark(folder, analyses, level, output):
    mng = ResourceManager()

    dir_list = os.listdir(folder)
    stats_analysis = defaultdict(lambda: [])
    for f in tqdm(dir_list):
        if not f.endswith(".ipynb"):
            continue        
        try:
            notebook = mng.grab_local_json(folder+f)
        except FileNotFoundError:
            notebook = mng.grab_local_json(folder + "\\" + f)
        except json.decoder.JSONDecodeError:
            # print("Warning decode error ")
            continue

        nblyzer = NBLyzer(level=level, filename=f)
        try:
           nblyzer.load_notebook(notebook["cells"])
        except Exception:
            continue

        for start in nblyzer.notebook_IR.keys():
            nblyzer.add_analyses(analyses)

            event = RunBatchEvent(start)
            try:
                results = nblyzer.execute_event(event).dumps(True)
            except:
                pass
        for akey in nblyzer.active_analyses:
            for s in nblyzer.all_analyses[akey].stats:
                stats_analysis[akey].append(s.get_row())

        for s in stats_analysis.keys():
            with open(output + s.replace(" ", "") + f"_{level}.csv", "w+") as f:
                writer = csv.writer(f)
                writer.writerow(["file name", "start cell", "execute time", "avg cell exec time", "max cell exec time", "no. of errors", "true phi rate", "no. fixedpoint", "longest fixedpoint path", "shortest fixedpoint path"])
                for rows in stats_analysis[s]:
                    writer.writerow(rows)

def main():
    parser = ArgumentParser(description="NBLyzer benchmarker version 1.0 ")
    parser.add_argument("-f", "--folder",  type=str, help='Benchmark folder')
    parser.add_argument("-a", "--analyses", nargs="+", type=str, default=[], help='Analyses to perform.')
    parser.add_argument("-l", "--level", nargs="?", type=int, default=1000, help='K-depth to analyze.')
    parser.add_argument("-o", "--output",  type=str, help='Output folder')
    args = parser.parse_args()

    benchmark(args.folder, args.analyses, args.level, args.output)

if __name__ == "__main__":
    main()