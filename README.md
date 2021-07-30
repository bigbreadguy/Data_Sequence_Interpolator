# Data_Sequence_Intepolator

## Introduction
<b>Data Sequence Interpolator</b> takes discrete data sequences with different intervals(that can be converted into a Pandas DataFrame) and returns it back as aligned data. All the sequences would be interpolated into target intervals, and the target interval will be provided as very last column of the data table.

## Getting Started

### 1. clone the repository
```
git clone https://github.com/bigbreadguy/Data_Sequence_Interpolator
```

### 2. install all the requirements
```
pip install -r requirements.txt
```

### 3. run
```
python main.py [-T, --has_timestamp BOOL(default=True){True, False}]
               [--ts_first BOOL(default=True){True, False}]
               [--align_max BOOL(default=True){True, False}]
               [-L, --align_length INT(default=1000)]
```

**has_timestamp** True when time stamps are provides with the sequences.</br>
**ts_first** True when a time stamp comes first in given data frames.</br>
**align_max** True if you want to align sequences following the longest time stamps</br>
**align_length** required when align_max is False, defines the length of target time stamp.</br>