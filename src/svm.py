#Thisugh G.
import nltk
import nltk.classify
from sklearn.svm import LinearSVC
import csv, math
from collections import Counter
features_list=["customer_ID", "day", "state",  "group_size","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous","previous"]
target_list = ["A","B","C","D","E","F","G"] 
target_feature_list = {
# 'A':["day","state"car_value", ","group_size",""car_value", car_value","risk_factor","homeowner","car_age", "age_oldest", "age_youngest","married_couple"],
# 'B':["day","state","group_size","car_value","risk_factor","homeowner","car_age", ""car_value", age_oldest", "age_youngest","married_couple"],
# 'C':["day","state","group_size","car_value","risk_factor","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous"],
# 'D':["day","state","group_size","car_value","risk_factor","homeowner","car_age", "age_oldest", "age_youngest","married_couple",],
# 'E':["day","state","group_size","car_value","risk_factor","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous"],
# 'F':["day","state","group_size","car_value","risk_factor","homeowner","car_age", "age_oldest", "age_youngest","married_couple",],
# 'G':["day","state","group_size","car_value","risk_factor","homeowner","car_age", "age_oldest", "age_youngest","married_couple",]}
'A':["day","group_size","homeowner","car_value", 'previous'],
'B':["state", "car_age", "car_value","previous"],
'C':["state", "car_value","C_previous","previous"],
'D':["state", "car_age","previous"],
'E':["state", "car_value", "car_age", "previous"],
# 'F':["day","group_size","homeowner","car_age", "age_oldest", "age_youngest","married_couple","state2",],
'F':["car_age", "state","previous"],
'G':["state","previous"]}
#target_list = ["A","B"]
#set thsi flag to 1 if you want to include previous values
usePrevious = 1
useFirst=0
header_map = {}

test_file = "data/test_v2_first_0_last_1_2.csv"
train_file = "data/train_first_0_last_1_2_sid.csv"
output_file = "data/NB_output_bucket.csv"
bucket_car_age=0
bucket_ages = 0
include_previous=1
def get_car_age_bucket(value):
    value2 =(int(value)-1)/6+1
#   print "%s\t%s"%(value,value2)
    if value>0:
        value=value2
    return value
def get_age_bucket(value):
    value = int(value)
    value2=0
    if value >=18 and value<22:
        value2= 1
    else:
        value2= value/10
#    print "%s\t%s"%(value,value2)
    return value2

def first_feature (row, target, test):
#    global features
    features={}
    for item in target_feature_list[target]:
        
        if item =="car_age" and bucket_car_age==1:
            value = get_car_age_bucket(value)
        elif (item =="age_oldest" or item=="age_youngest") and bucket_ages==1:
            value = get_age_bucket(value)
        elif item == "previous":
#            print 'adding previous'
            for prev in range(0, include_previous):
                if test==0:
                    if prev==0:
                        features["previous%s"%prev]=row[header_map["%s"%target]]
                        features["previous_cost_%s"%prev]=row[header_map["%s"%("cost")]]
                    else:
                        features["previous%s"%prev]=row[header_map["prev_%s_%s"%(prev-1, target)]]
                        features["previous_cost_%s"%prev]=row[header_map["prev_%s_%s"%(prev-1, "cost")]]
                else:
                    features["previous%s"%prev]=row[header_map["prev_%s_%s"%(prev, target)]]
                    features["previous_cost_%s"%prev]=row[header_map["prev_%s_%s"%(prev, "cost")]]
        else:
            value = row[header_map[item]]
            if item =="car_age" and bucket_car_age==1:
                value = get_car_age_bucket(value)
            if (item =="age_oldest" or item=="age_youngest") and bucket_ages==1:
                value = get_age_bucket(value)
        features[item]=value
    return features

def loadHeader(row):
    global header_map
#    cols = row.split(',')
    for i in range(0,len(row)):
        header_map[row[i]]=i
#    print header_map
    
raw_data = []
test_data=[]
output = {}
with open(train_file) as csvfile:
    reader = csv.reader(csvfile)
    row_count=0
    for row in reader:
        if row_count==0:
            loadHeader(row)
            row_count+=1
        else:
            raw_data.append(row)

with open(test_file) as csvfile:
    reader = csv.reader(csvfile)
    row_count=0
    for row in reader:
        if row_count==0:
#            loadHeader(row)
            row_count+=1
        else:
            test_data.append(row)
            output[row[0]]={}
for i in range(0,len(target_list)):
    target= target_list[i]
    target_col_id= header_map[target]
    print "Training for %s"% target
    data = ([(row, row[target_col_id]) for row in raw_data])
    test = ([(row[0],row, row[target_col_id]) for row in test_data])
    #print row,row[i],i
    #Run it for A through G
    
    train_set = [(first_feature(r, target,0), a) for (r, a) in data]
    # print train_set[0]
    test_set=[(c, first_feature(r, target,1), a) for (c, r, a) in test]
    # print train_set[0]
    #train_set1, train_set2 = train_set[70000:], train_set[:27010]
    train_set1, train_set2 = train_set[48505:], train_set[:48505]
#    train_set = featuresets
    # classifier = nltk.NaiveBayesClassifier.train(train_set)
    #classifier = nltk.NaiveBayesClassifier.train(train_set1)
    #classifier = nltk.classify.svm.SvmClassifier.train(train_features)
    classifier = nltk.classify.SklearnClassifier(LinearSVC())
    classifier.train(train_set1)
    #Display details
    print "Accuracy is for %s:"%target, nltk.classify.accuracy(classifier, train_set2)
    # print classifier.show_most_informative_features(5)
    # useful = classifier.most_informative_features(1000)
#     feature_counter = Counter()
#     for index in range(0, len(useful)):
# #        print useful[index]
#         item, value = useful[index]
#         feature_counter[item]+=1
#     print feature_counter
#        print useful[item]
#    print classifier.show_least_informative_features(10)

    for (cust_id, name, value)in test_set:
#        print "guessing %s"% cust_id
        guess = classifier.classify(name)
#        output[name.customer_ID][target]=guess
#        print name
#        cust_id = name['customer_ID']
        output[cust_id][target]=guess
#        print "%s\t%s\t%s"%(cust_id, value, guess)
#print output
f = open(output_file,'w')
f.write("customer_ID,plan\n")
for out in output:
    value = ""
    for i in range(0,len(target_list)):
        target= target_list[i]
        value+= str(output[out][target])
    v = "%s,%s\n"%(out, value)
    f.write(v)
#    print v
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