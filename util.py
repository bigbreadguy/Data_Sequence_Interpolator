import numpy as np
import pandas as pd
import glob
from functools import reduce

def load_df(path : str):
    ext = path.split(".")[-1]
    try:    
        if ext == "csv":
            df = pd.read_csv(path)
        elif ext == "xlsx":
            df = pd.read_excel(path, engine="openpyxl")
        if "Unnamed: 0" in df:
            df.drop("Unnamed: 0", axis=1, inplace=True)
        return df
    except:
        print("File format not supported!")

def split_df(df, has_ts=False, ts_start=0):
    sequence_start = abs(1-ts_start)
    if has_ts:
        xs = [df[col].dropna().to_numpy() for col in df.copy().iloc[:,ts_start::2]]
        ys = [df[col].dropna().to_numpy() for col in df.copy().iloc[:,sequence_start::2]]
        return xs, ys
    else:
        xs = [np.arange(len(df[col].dropna())) for col in df]
        ys = [df[col].dropna().to_numpy() for col in df.copy()]
        return xs, ys

def check_pairing(sequence):
    is_pair_all = True
    for ts, val in zip(sequence[0], sequence[1]):
        is_pair = len(ts)==len(val)
        if is_pair_all:
            is_pair_all = is_pair_all

def interpolate(sequence, cols, align_max:bool=True, ts_name:str="Time[s]", align_length:int=1000):
    max_xs = reduce(lambda a, b : a if len(a) > len(b) else b, sequence[0])
    
    if align_max:
        align_length = len(max_xs)
        
    max_val = reduce(lambda a, b : np.max(a) if np.max(a) > np.max(b) else np.max(b), sequence[0])
    min_val = reduce(lambda a, b : np.min(a) if np.min(a) < np.min(b) else np.min(b), sequence[0])
    target_xs = np.linspace(min_val, max_val, num=align_length)
    print(f"\ntarget timestamp : length {align_length}/ min {min_val}/ max {max_val}")
    result = {key:np.interp(target_xs, sequence[0][i], sequence[1][i]) for i, key in enumerate(cols)}
    result[ts_name] = target_xs
    res_df = pd.DataFrame(data=result)
    return res_df