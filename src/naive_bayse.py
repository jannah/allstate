#This version runs the classifer for A through G.
import nltk
import csv
features_list=["day", "state", "location", "group_size","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous"]
target_list = ["A","B","C","D","E","F","G"]
header_map = {}

test_file = "data/test_v2_first_0_last_1.csv"
train_file = "data/train_first_0_last_1.csv"
def first_feature (row, target):
#    global features
    features={}
    for item in features_list:
        features[item]=row[header_map[item]]
    features["previous"]=row[header_map["prev_actual_%s"%target]]
    return features
def loadHeader(row):
    global header_map
#    cols = row.split(',')
    for i in range(0,len(row)):
        header_map[row[i]]=i
    print header_map
raw_data = []
test_data=[]
with open(train_file) as csvfile:
	reader = csv.reader(csvfile)
	row_count=0
        for row in reader:
            if row_count==0:
                loadHeader(row)
                row_count+=1
            else:
                raw_data.append(row)
with open(test_file)as csfvile:
    reader = csv.reader(csvfile)
	row_count=0
        for row in reader:
            if row_count==0:
                loadHeader(row)
                row_count+=1
            else:
                test_data.append(row)
#	for i in range(17,24):
for i in range(0,len(target_list)):
    target= target_list[i]
    target_col_id= header_map[target]
    data = ([(row, row[target_col_id]) for row in raw_data])
    #print row,row[i],i
    #Run it for A through G
    featuresets = [(first_feature(r, target), a) for (r, a) in data]
    
#    train_set, test_set = featuresets[70000:], featuresets[:70001]
    train_set = 
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    #Display details
    print "Accuracy is for %s:"%target, nltk.classify.accuracy(classifier, test_set)
    print classifier.show_most_informative_features(5)

#    csvfile.seek(0) #inportant for resetting the file pointer and avoiding the empty bins in next iteration

	##data = ([(row, row[23]) for row in reader])
	#for row in reader:
		#print ', '.join(row)
		#first_feature(row)

	##featuresets = [(first_feature(r), a) for (r, a) in data]
	##train_set, test_set = featuresets[47000:], featuresets[:50009]
	##classifier = nltk.NaiveBayesClassifier.train(train_set)

	#classifier.classify(first_feature('CA'))
	##print "Accuracy is:", nltk.classify.accuracy(classifier, test_set)
	#print nltk.classify.accuracy(classifier, test_set)

	##print classifier.show_most_informative_features(5)