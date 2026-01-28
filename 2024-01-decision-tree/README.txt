This project (April 2023 - January 2024) builds machine learning models to predict the following post-transplant outcomes for deceased donor kidney recipients:
1. cancer occurrence (target: malig)
2. graft failure (target: GSTATUS_KI)

I choose to model using decision trees due to interpretability for clinical settings. Due to a class imbalance, I include an oversampling option to improve recall.

eda.py: exploratory data analysis in conjunction with other sources to engineer feature selection pipeline

dt.py: train and evaluate using DecisionTreeCalssifier with selected features, runs with and without oversampling, and includes confusion matrix and tree visualizations

paper.pdf: full report of feature selection pipeline and model performance on UNOS dataset

