allstate
========

DataMining-AllState
For our project we entered the Kaggle Allstate Purchase Prediction Challenge. This challenge required us to create a model that predicts the exact insurance policy that a customer will purchase. The leading team is currently at 54.5% accuracy. Our team is at 53.8%. We used Naives Bayes classifier to get this far, but we are now experimenting with SVM and Random Forests to try to improve accuracy. 

File List:

..		
config: JSON configuration files for NB features

data	data in different formats with submttions and additional accuracy logs

RF_output_bucket.csv	Random Forest output

change_over.py	Initial data tranformation script to see how people change options over time

change_over_first.py	permutation of the above

change_over_no_demographic_change.py	Final transformation script that flattens data based on internal options

flatten.py	first flattening script using Wrangler

naive_bayse.py Working version of NB Classifier

playtest100000_v2_first_0_last_1.csv	data input for RF

playtest10000_v2_first_0_last_1.csv	data input for RF

playtest1000_v2_first_0_last_1.csvdata input for RF

playtest_v2_first_0_last_1.csv	data input for RF

playtrain100000_first_0_last_1.csv data input for RF

playtrain10000_first_0_last_1.csv	data input for RF

playtrain1000_first_0_last_1.csv	data input for RF

playtrain_first_0_last_1.csv	data input for RF

predictions_for_A_1000.csv	data input for RF

predictions_for_A_10000.csv	data input for RF

renu_forest.py Random Forest Classifer
