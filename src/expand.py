# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-25

"""Reads data csv file, then expand columns with list of values

Usage: expand.py --train_data=<train_data> --test_data=<test_data> --train_output=<train_output> --test_output=<test_output>

Options:
--train_data=<train_data>        file path of the train csv file to read
--test_data=<test_data>          file path of the test csv file to read
--train_output=<train_output>    file path and file name of the output file
--test_output=<test_output>      file path and file name of the output file
"""

import os
import pandas as pd
import numpy as np
from docopt import docopt

opt = docopt(__doc__)

def main(train_data, test_data, train_output, test_output):
    """
    Main function which reads data file, call data cleaning and transforming 
    functions, and writes to file

    Parameters
    ----------
    train_data : str
        file path to data
    test_data : str
        file path to data
    train_output : str
        file path for output file
    test_output : str
        file path for output file
    """
    train_data = pd.read_csv(train_data, encoding="ISO-8859-1")
    test_data = pd.read_csv(test_data, encoding="ISO-8859-1")
    
    train_data = expand_column(train_data, train_data, "disciplines")
    train_data = expand_column(train_data, train_data, "audiences")
    
    test_data = expand_column(train_data, test_data, "disciplines")
    test_data = expand_column(train_data, test_data, "audiences")
    
    try:
        train_data.to_csv(train_output, index=False)
    except:
        os.makedirs(os.path.dirname(output))
        train_data.to_csv(train_output, index=False)
    
    try:
        test_data.to_csv(test_output, index=False)
    except:
        os.makedirs(os.path.dirname(output))
        test_data.to_csv(test_output, index=False)




def expand_column(data1, data2, column):
    """
    Expand input column containing list of categories into one
    new column per category, True for if the original column contains
    the category and False otherwise

    Parameters
    ----------
    data1 : dataframe
        data to get columns from
    data2 : dataframe
        data to expand
    column : str
        column to expand

    Returns
    -------
    dataframe
        expanded dataframe
    """
    data2[column] = data2[column].str.split(", ", expand=False)
    categories = data1.explode(column)[column].unique().tolist()
    for category in categories:
        data2[f"{column}_{category}".lower().replace(" ", "_")] = data2[column].apply(lambda x: category in x)

    return data2



if __name__ == "__main__":
    main(opt["--train_data"], opt["--test_data"], opt["--train_output"], opt["--test_output"])