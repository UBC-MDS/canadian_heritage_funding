# run_all.sh
# Artan Zandian, Joyce Wang, Amelia Tang, Wenxin Xiang, Nov 2021

# This driver script completes the report on the prediction of 
# Canadian Heritage Funding approval amount prediction analysis

# example usage:
# make all

all : doc/canadian_heritage_funding_report.md

# download data
data/raw/capf_en.csv : src/download_data.py
		python src/download_data.py --url=https://open.canada.ca/data/dataset/92984c11-6fd4-40c4-b23c-e8832e1f4cd5/resource/148841f0-11c9-4f45-8700-d0a4717dea2f/download/capf_en.csv --file_path=data/raw/capf_en.csv

# clean data
data/processed/heritage_clean.csv : data/raw/capf_en.csv src/clean.py
		python src/clean.py --data data/raw/capf_en.csv --output data/processed/heritage_clean.csv

# split data
data/processed/heritage_train_unexpanded.csv data/processed/heritage_test_unexpanded.csv : data/processed/heritage_clean.csv src/split_data.py
		python src/split_data.py --data data/processed/heritage_clean.csv --train data/processed/heritage_train_unexpanded.csv --test data/processed/heritage_test_unexpanded.csv

# create exploratory data analysis figure and write to file 
results/target_feature_counts.csv results/target_distr_plot.png results/funding_year_discipline_plot.png results/feature_counts_plot.png : data/processed/heritage_train_unexpanded.csv src/eda_plots.py
		python src/eda_plots.py --data data/processed/heritage_train_unexpanded.csv --table results/target_feature_counts.csv --plot1 results/target_distr_plot.png --plot2 results/funding_year_discipline_plot.png --plot3 results/feature_counts_plot.png


# expand columns with list of values
data/processed/heritage_train.csv data/processed/heritage_test.csv : data/processed/heritage_train_unexpanded.csv data/processed/heritage_test_unexpanded.csv src/expand.py
		python src/expand.py --train_data=data/processed/heritage_train_unexpanded.csv --test_data=data/processed/heritage_test_unexpanded.csv --train_output=data/processed/heritage_train.csv --test_output=data/processed/heritage_test.csv

# model selection & optimization
results/model_comparison.csv results/final_rf_model.pickle : data/processed/heritage_train.csv src/model_selection.py
		python -W"ignore" src/model_selection.py --data=data/processed/heritage_train.csv --models_score=results/model_comparison.csv --best_model=results/final_rf_model.pickle

# test model
results/test_result.csv : src/test_results.py data/processed/heritage_test.csv results/final_rf_model.pickle
		python src/test_results.py --test=data/processed/heritage_test.csv --model=results/final_rf_model.pickle --out_dir=results/test_result.csv

# render final report
doc/canadian_heritage_funding_report.md : doc/canadian_heritage_funding_report.Rmd results/target_feature_counts.csv \
results/model_comparison.csv results/test_result.csv results/target_distr_plot.png \
results/funding_year_discipline_plot.png results/feature_counts_plot.png doc/can_heritage_reference.bib
		Rscript -e "rmarkdown::render('doc/canadian_heritage_funding_report.Rmd', output_format = 'github_document')"

clean :
		rm -rf data/raw/capf_en.csv
		rm -rf data/processed/heritage_clean.csv
		rm -rf data/processed/heritage_train_unexpanded.csv data/processed/heritage_test_unexpanded.csv
		rm -rf results/target_feature_counts.csv results/target_distr_plot.png results/funding_year_discipline_plot.png results/feature_counts_plot.png
		rm -rf data/processed/heritage_train.csv data/processed/heritage_test.csv
		rm -rf results/model_comparison.csv results/final_rf_model.pickle
		rm -rf results/test_result.csv 
		rm -rf doc/canadian_heritage_funding_report.html 
		
