import os
import glob
import argparse
from tqdm import tqdm
from util import load_df, split_df, interpolate

class opts():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Interpolator",
                                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
        self.parser.add_argument("-T", "--has_timestamp", default=False, choices=[True, False], type=bool, dest="has_ts")
        self.parser.add_argument("--ts_first", default=True, choices=[True, False], type=bool, dest="ts_first")
        self.parser.add_argument("--align_max", default=True, choices=[True, False], type=bool, dest="align_max")
        self.parser.add_argument("-L", "--align_length", default=1000, type=int, dest="align_length")

    def parse(self, args : str = None):
        if args == None:
            opt = self.parser.parse_args()
        else:
            opt = self.parser.parse_args(args)
        
        return opt

def load_dir(file_pattern):
    return glob.glob(file_pattern)

if __name__ == "__main__":
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data", "*")
    path_list = load_dir(data_dir)

    print(f"Data Loaded from {os.path.join(cwd, "data")}")
    target_files = [os.path.basename(d) for d in path_list]
    for tf in target_files:
        print(f"{tf} Loaded!")

    args = opts().parse()
    has_ts = args.has_ts
    if has_ts:
        if args.ts_first:
            ts_start = 0
        else:
            ts_start = 1
    align_max = args.align_max
    align_length = args.align_length

    result_dir = os.path.join(cwd, "result")
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    for path in tqdm(path_list):
        df = load_df(path)
        if has_ts:
            sequence_start = abs(1-ts_start)
            cols = list(df.iloc[:,sequence_start::2])
        else:
            cols = list(df)
        
        sequence = split_df(df)

        result = interpolate(sequence, cols)
        basename = os.path.basename(path)
        save_dir = os.path.join(result_dir, basename)

        ext = basename.split(".")[-1]
        if ext == "csv":
            result.to_csv(save_dir)
        elif ext == "xlsx":
            result.to_excel(save_dir, engine="openpyxl")
        
        print(f"{basename} has been Interpolated.")
    
    print("Interpolation Complete!")