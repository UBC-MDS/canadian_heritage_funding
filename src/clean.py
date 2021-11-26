# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-25

"""Reads data csv file, perform data cleaning, and then add a new
column as the prediction target

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
    try:
        data = pd.read_csv(data, encoding="ISO-8859-1")
        data = clean_data(data)
        data = transform_target_col(data)
        data = expand_column(data, "disciplines")
        data = expand_column(data, "audiences")
        data.to_csv(output, index=False)
    except:
        os.makedirs(os.path.dirname(output))
        data.to_csv(output, index=False)



def clean_data(data):
    """
    Clean up column names and dirty data values

    Parameters
    ----------
    data : dataframe
        data to clean up

    Returns
    -------
    dataframe
        cleaned data
    """
    data.columns = data.columns.str.lower().str.replace(" ", "_")
    data = data.rename(columns={"grant_or_contributionution": "grant_or_contribution"})
    data["audiences"] = data["audiences"].str.split(", ", expand=False)
    data["disciplines"] = data["disciplines"].str.split(", ", expand=False)
    return data


def transform_target_col(data):
    """
    Add a new column creating categories for amount_approved 
    based on quantiles

    Parameters
    ----------
    data : dataframe
        data to transform

    Returns
    -------
    dataframe
        transformed data
    """
    q10 = data["amount_approved"].quantile(0.1)
    q25 = data["amount_approved"].quantile(0.25)
    q50 = data["amount_approved"].quantile(0.5)
    q75 = data["amount_approved"].quantile(0.75)

    labeling = [f"${q75/1000}K",
                f"${q50/1000}K",
                f"${q25/1000}K",
                f"${q10/1000}K",
                f"less than ${q10/1000}K"]

    amount = data["amount_approved"]
    data["amount_category"] = np.where(amount > q75, labeling[0],
                                            np.where(amount > q50, labeling[1],
                                                    np.where(amount > q25, labeling[2],
                                                                np.where(amount > q10, labeling[3], labeling[4]))))
    return data


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
    categories = data.explode(column)[column].unique().tolist()
    for category in categories:
        data[f"{column}_{category}".lower().replace(" ", "_")] = data[column].apply(lambda x: category in x)
    data.drop(column, axis=1, inplace=True)

    return data



if __name__ == "__main__":
    main(opt["--data"], opt["--output"])
