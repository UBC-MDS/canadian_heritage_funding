# run_all.sh
# Artan Zandian, Joyce Wang, Amelia Tang, Wenxin Xiang, Nov 2021

# download data
python src/download_data.py --url=https://open.canada.ca/data/dataset/92984c11-6fd4-40c4-b23c-e8832e1f4cd5/resource/148841f0-11c9-4f45-8700-d0a4717dea2f/download/capf_en.csv --file_path=data/raw/capf_en.csv

# run eda report


# clean data


# split data
 

# create exploratory data analysis figure and write to file 


# model selection & optimization
python src/model_selection.py --data=data/processed/heritage_train.csv --models_score=results/model_comparison.csv --best_model=results/final_rf_model.pickle

# test model
python src/test_results.py --test=data/processed/heritage_test.csv --out_dir=results/test_result.csv

# render final report
