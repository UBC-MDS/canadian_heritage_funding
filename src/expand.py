# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-25

"""Reads data csv file, then expand columns with list of values

Usage: clean.py --data=<data> --output=<output>

Options:
--data=<data>                file path of the csv file to read
--output=<output>            file path and file name of the output file
"""

import os
import pandas as pd
import numpy as np
from docopt import docopt

opt = docopt(__doc__)

def main(data, output):
    """
    Main function which reads data file, call data cleaning and transforming 
    functions, and writes to file

    Parameters
    ----------
    data : str
        file path to data
    output : str
        file path for output file
    """
    data = pd.read_csv(data, encoding="ISO-8859-1")
    data = expand_column(data, "disciplines")
    data = expand_column(data, "audiences")
    try:
        data.to_csv(output, index=False)
    except:
        os.makedirs(os.path.dirname(output))
        data.to_csv(output, index=False)




def expand_column(data, column):
    """
    Expand input column containing list of categories into one
    new column per category, True for if the original column contains
    the category and False otherwise

    Parameters
    ----------
    data : dataframe
        data to expand
    column : str
        column to expand

    Returns
    -------
    dataframe
        expanded dataframe
    """
    data[column] = data[column].str.split(", ", expand=False)
    categories = data.explode(column)[column].unique().tolist()
    for category in categories:
        data[f"{column}_{category}".lower().replace(" ", "_")] = data[column].apply(lambda x: category in x)

    return data



if __name__ == "__main__":
    main(opt["--data"], opt["--output"])