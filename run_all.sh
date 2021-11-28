# run_all.sh
# Artan Zandian, Joyce Wang, Amelia Tang, Wenxin Xiang, Nov 2021

# download data
python src/download_data.py --url=https://open.canada.ca/data/dataset/92984c11-6fd4-40c4-b23c-e8832e1f4cd5/resource/148841f0-11c9-4f45-8700-d0a4717dea2f/download/capf_en.csv --file_path=data/raw/capf_en.csv

# clean data
python src/clean.py --data data/raw/capf_en.csv --output data/processed/heritage_clean.csv

# split data
python src/split_data.py --data data/processed/heritage_clean.csv --train data/processed/heritage_train_unexpanded.csv --test data/processed/heritage_test_unexpanded.csv

# create exploratory data analysis figure and write to file 
python src/eda_plots.py --data data/processed/heritage_train_unexpanded.csv --table results/target_feature_counts.csv --plot1 results/target_distr_plot.png --plot2 results/funding_year_discipline_plot.png --plot3 results/feature_counts_plot.png


# expand columns with list of values
python src/expand.py --train_data=data/processed/heritage_train_unexpanded.csv --test_data=data/processed/heritage_test_unexpanded.csv --train_output=data/processed/heritage_train.csv --test_output=data/processed/heritage_test.csv

# model selection & optimization
python src/model_selection.py --data=data/processed/heritage_train.csv --models_score=results/model_comparison.csv --best_model=results/final_rf_model.pickle

# test model
python src/test_results.py --test=data/processed/heritage_test.csv --model=results/final_rf_model.pickle --out_dir=results/test_result.csv

# render final report
