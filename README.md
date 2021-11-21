# Canadian Heritage Funding Size for Art Projects 
Data analysis project for DSCI 522 (Data Science Workflows); a course in the Master of Data Science program at the University of British Columbia.
#### Last updated: Nov 20th, 2021
## Contributers
Artan Zandian, Joyce Wang, Amelia Tang, Wenxin Xiang 
## Introduction
For this project, we are trying to answer two intriguing questions: given information non-indicative of artistic merit, such as location, audience, and discipline, what would be the funding size for art projects related to Canadian heritage? Can we make reasonable predictions? The significance of answering the questions lies in our unanimous support for preserving Canadian heritage through artistic expressions. Amidst controversies over governmental involvements in arts, the Canada Council for the Arts (the Council) has been fostering creativity through allocating government funding to selected art projects. The Council’s judging criteria emphasizes artistic merit instead of social and political influences (Santini 2013). 

Meanwhile, under the Department of Canadian Heritage (DCH), the Canada Arts Presentation Fund (the Fund) financially supports art festival presenters and performing arts series presenters in all regions in Canada (Canada 2019). The Fund’s performance is mainly evaluated based on the diversity of the grantees or awardees instead of artistic merit (Canada 2019). Therefore, it is in the interest of us Canadian heritage supporters to predict the size of the fundings based on features not indicative of artistic merit, but those reflecting diversity, socially, culturally and geographically.
## Data Source 
The data set used in this project is provided by the Department of Canadian Heritage (DCH) available on the Government of Canada’s Open Data website (Canada 2018). The data set can be found [here](https://open.canada.ca/data/en/dataset/92984c11-6fd4-40c4-b23c-e8832e1f4cd5). Each row of the dataset represents an art project funded by the Fund and provides the project’s name, location information (community, city, region and province), presenter information (associated organizations, disciplines, festival or series presentations, etc.), grant or contribution, and audience. The size of the funding approved for each art project is reported by the Fund.  
## Exploratory Data Analysis 
To answer the main predictive question on funding sizes, we plan to build a predictive multi-class classification model. We treat this as a classification problem because we are more interested in predicting the overall range of the funding size versus a specific dollar amount in our study. To predict the funding size for art projects, we would first conduct exploratory data analysis. We need to first split the data into a training set and test set (split 80%:20%), and look at the size of the dataset, columns and their data types, the amount of missing values in each column, the distribution of each feature between classes, and determine the transformations we need to perform on the data. For this part, we plan to plot facet bar charts to explore the counts of different features. 

Our target feature, amount approved,  is numerical, we would like to know whether it is continuous in nature by examining its distribution and counting unique values. To achieve this end, we will plot a histogram to show the distribution of the funding amount approved and use a function to obtain the count of unique values in this column. We will also look at the interquartile range of the amount approved to help split them into reasonable classes. After understanding the nature of our predicting target, we will divide them into different classes for building the multi-class classification model.  
## Predictive Models 
In our data set, many predicting features are categorical and our target, after transformation, will also be categorical in nature. Therefore, we consider using the following four algorithms that are suitable for multi-class classification problems: 

- Decision Trees
- k-Nearest Neighbors
- Naive Bayes
- Random Forest

We plan to first preprocess the categorical features (the region, disciplines, etc.) using label encoding. We may also obtain meaningful information from associated organization names and project names, so we will process these text features using text encoding. We will train the models and report k-fold cross validation scores in a table on the report. Based on the nature of our study, we will use the overall accuracies, misclassification errors and macro f1 scores for cross-validation. Then, we will tune the hyperparameters of models that we believe are worth further exploration. We will present the hyperparameter optimization results in a table.  
## Results Reporting
After identifying the best-performing model with optimized hyperparameters, we will re-fit the model on the training data set and evaluate the model on the test data. We will answer our sub-question whether those features non-indicative of artistic merit (location and discipline etc.), can make reasonable predictions on the funding size approved by the the Canada Arts Presentation Fund by examining how well the model can generalize. To achieve this end, we will evaluate our best model by looking at the test scores, including overall accuracy, misclassification errors and macro f1 score. The scores will be presented in a table. We will also plot a confusion matrix for misclassification errors in our final report. 
## Dependencies
xxx
## License
xxx
## References
anada, The Department of Canadian Heritage, Data on funding provided in 2016-2017 and 2017-2018 by the Canada Arts Presentation Fund, Canadian Heritage, 2018, https://open.canada.ca/data/en/dataset/92984c11-6fd4-40c4-b23c-e8832e1f4cd5/resource/148841f0-11c9-4f45-8700-d0a4717dea2f

Canada, Evaluation Services Directorate, Grouped Arts Evaluation: Canada Arts Presentation Fund, Canada Cultural Spaces Fund, and Canada Cultural Investment Fund 2013-14 to 2017-18, 2019, https://www.canada.ca/en/canadian-heritage/corporate/publications/evaluations/grouped-art-evaluation.html#a1 

Santini, Lauryn. “Public Funding of the Visual Arts in Canada: Keeping Creativity at an Arm’s Length.” UMI Dissertations Publishing, 2013. https://www.proquest.com/openview/5dcc1a8c4f06559c3793ba03335019d2 


