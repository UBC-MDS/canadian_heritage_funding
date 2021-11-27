# author: Wenxin Xiang, Joyce Wang, Amelia Tang, Artan Zandian
# date: 2021-11-26

"""Test selected model's accuracy on test data set.

Usage: src/test_results.py  --test=<test> --out_dir=<out_dir>

Options:
--test=<test>         Path and file name to test data
--out_dir=<out_dir>   Path to directory where the plots should be saved
"""

import pandas as pd
import numpy as np
import os
import string
import pickle
from docopt import docopt

from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, SCORERS, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
)

opt = docopt(__doc__)

def main(test, out_dir):
    """
    Assess best model's accuracy on test data set.
    Report classification report of weighted_f1 score.
    
    Parameters
    ----------
    test: str
        file path and file name of the test data set
    out_dir: str
        file path and file name of the model_quality report
    """

    # Load and wrangle test data
    test_data = pd.read_csv(test)
    X_test = test_data.drop(columns=["amount_category", "amount_approved", "audiences_none"])
    y_test = test_data["amount_category"]
    
    # Load model and predict
    final_model = pickle.load(open("results/final_rf_model.pickle", 'rb'))
    y_predict = final_model.predict(X_test)
    
    # Assess model performance
    model_quality = pd.DataFrame(classification_report(y_test, y_predict, output_dict=True)).T
    
    # Save model_quality to results
    try:
        model_quality.to_csv(out_dir)
    except:
        os.makedirs(os.path.dirname(out_dir))
        model_quality.to_csv(out_dir)
    

if __name__ == "__main__":
    main(opt["--test"], opt["--out_dir"])
    
