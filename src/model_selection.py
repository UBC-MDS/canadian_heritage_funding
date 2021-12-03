# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-26

"""Reads train_data csv file, perform scoring on multiple classification models, 
and then select the results in a csv file. Then, it will run hyperprameter optimization
on the best model and saves the model in a pickle format

Usage: model_selection.py --data=<data> --models_score=<csv_path> --best_model=<model_path>

Options:
--data=<data>               file path of the clean train data 
--models_score=<csv_path>   path and file name of the model_selection scores csv file
--best_model=<model_path>   path and file name of the best model to be saved
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
from sklearn.model_selection import (
    RandomizedSearchCV,
    cross_validate,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
)
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

from docopt import docopt

opt = docopt(__doc__)


def main(data, csv_path, model_path):
    """
    Main function which reads train data, generates train scores for multiple classifiers,
    tunes the best model, and saves both results and best model.

    Parameters
    ----------
    data : str
        file path to data
    csv_path : str
        path and file name of the model_selection scores csv file
    model_path : str
        path and file name of the best model to be saved
    """
    # read train data
    train_data = pd.read_csv(data)

    # separate X and y
    X_train = train_data.drop(
        columns=["amount_category", "amount_approved", "audiences_none"]
    )
    y_train = train_data["amount_category"]
    
    # # define preprocessor
    preprocessor = preprocess(X_train)

    # generate model scores
    results = generate_scores(preprocessor, X_train, y_train)
    try:
        results.to_csv(csv_path, encoding="utf-8")
    except:
        os.makedirs(os.path.dirname(csv_path))
        open(csv_path, "wb").write(results.content)

    # # tune and save model
    best_model = tune_model(preprocessor, RandomForestClassifier(), X_train, y_train)
    pickle.dump(best_model, open(model_path, "wb"))



def preprocess(X_train):
    """
    Sets the feature types and defines a column transformer to be used
    for the preprocessing of the data before giving it to the classifiers.

    Parameters
    ----------
    X_train : dataframe
        dataframe extract column names
    Returns
    -------
    preprocessor
        A column transformer that could be given to a model pipeline
    """
    # Identify Feature Categories
    drop_feature = [
        "fiscal_year",
        "region",
        "disciplines_other",
        "organization_name",
    ]  # droping region as provice is already an indicator of region
    text_countvec = "project_name"
    categorical_ohe = ["city", "province", "project_type"]
    ordinal = ["community_type"]
    Community_order = [
        ["Remote", "Rural", "Small Urban", "Medium Urban", "Large Urban"]
    ]

    binary = list(
        set(X_train.columns.tolist())
        - set(drop_feature)
        - set([text_countvec])
        - set(categorical_ohe)
        - set(ordinal)
    )

    # Set Column Transformers
    preprocessor = make_column_transformer(
        (CountVectorizer(max_features=400, stop_words="english"), text_countvec),
        (
            OneHotEncoder(
                handle_unknown="ignore",
            ),
            categorical_ohe,
        ),
        (OneHotEncoder(drop="if_binary", handle_unknown="ignore"), binary),
        (
            OrdinalEncoder(
                categories=Community_order,
            ),
            ordinal,
        ),
    )

    return preprocessor


def generate_scores(preprocessor, X_train, y_train):
    """
    Gives score by applying different models to the train data

    Parameters
    ----------
    preprocessor
        column transformer object
    X_train : dataframe
        X portion of train dataset
    y_train : dataframe
        y portion of train dataset
    """
    # Scoring methods to be used for multilabel classification
    scoring = ["f1_weighted", "recall_weighted", "precision_weighted"]

    # define models
    models = {
        "Dummy Classifier": DummyClassifier(),
        "Logistic Regression": LogisticRegression(
            max_iter=1000, class_weight="balanced"
        ),
        "Multinomial Naive Bayes": MultinomialNB(),
        "SVC": SVC(class_weight="balanced"),
        "Random Forest": RandomForestClassifier(class_weight="balanced"),
    }

    # generate results
    np.warnings.filterwarnings("ignore")
    results = pd.DataFrame()
    for name, classifier in models.items():
        pipe = make_pipeline(preprocessor, classifier)
        result = pd.DataFrame(
            cross_validate(pipe, X_train, y_train, cv=5, scoring=scoring)
        ).mean()
        results = pd.concat([results, pd.DataFrame(result, columns=[name])], axis=1)

    return results


def tune_model(preprocessor, model, X_train, y_train):
    """
    Finds the best combination of hyperparameters and returns the best model
    fitted on those hyperparameters.

    Parameters
    ----------
    preprocessor
        column transformer object
    model
        the classifier model (Randomforest) to be used for tuning
    X_train : dataframe
        X portion of train dataset
    y_train : dataframe
        y portion of train dataset

    Returns
    -------
    final_model
        fitted model with best hyperparameters
    """
    # Scoring methods to be used for multilabel classification
    scoring = ["f1_weighted", "recall_weighted", "precision_weighted"]

    param_distributions = {
        "columntransformer__countvectorizer__max_features": [400, 500, 600, 700, 800],
        "randomforestclassifier__max_depth": [None, 10, 20, 30, 40, 50, 60],
        "randomforestclassifier__max_features": ["auto", "log2"],
        "randomforestclassifier__class_weight": ["balanced", None],
    }

    best_model = RandomizedSearchCV(
        make_pipeline(preprocessor, model),
        param_distributions=param_distributions,
        n_jobs=-1,
        scoring=scoring,
        n_iter=30,
        cv=5,
        refit="f1_weighted",
    )

    final_model = best_model.fit(X_train, y_train)
    return final_model


if __name__ == "__main__":
    main(opt["--data"], opt["--models_score"], opt["--best_model"])
