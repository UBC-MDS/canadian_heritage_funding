# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-25

"""Perform train-test-split on data

Usage: clean.py --data=<data> --train=<train> --test=<test>

Options:
--data=<data>                file path of the csv file to read
--train=<train>              file path of the train split output file
--test=<test>                file path of the test split output file
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)


def main(data, train, test):
    data = pd.read_csv(data, encoding="ISO-8859-1")
    train_df, test_df = train_test_split(data, test_size=0.20, random_state=1233)
    try:
        
        train_df.to_csv(train, index=False)
    except:
        os.makedirs(os.path.dirname(train))
        train_df.to_csv(train, index=False)
        
    try:
        test_df.to_csv(test, index=False)
    except:
        os.makedirs(os.path.dirname(test))
        test_df.to_csv(test, index=False)




if __name__ == "__main__":
    main(opt["--data"], opt["--train"], opt["--test"])
