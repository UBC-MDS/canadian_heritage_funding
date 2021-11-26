# author: Wenxin Xiang
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

from sklearn.compose import make_column_transformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, f1_score, SCORERS
from sklearn.model_selection import (
    RandomizedSearchCV,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
)
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

opt = docopt(__doc__)

def main(test, out_dir)

    # Load and wrangle test data
    test_data = pd.read_csv(test)
    X_test = test_data.drop(columns=["amount_category"])
    y_test = test_data["amount_category"]
    
    # Load model and predict
    final_model = pickle.load(open("../results/final_rf_model.pickle", 'rb'))
    y_predict = final_model.predict(X_test)
    
    # Assess model accuracy
    model_quality = f1_score(y_test, y_predict, sample_weight=())

if __name__ == "__main__":
    main(opt["--"])
    
    
    import pickle
