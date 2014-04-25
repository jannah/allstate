#This version runs the classifer for A through G.
import nltk
import csv
features_list=["customer_ID", "day", "state",  "group_size","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous"]
target_list = ["A","B","C","D","E","F","G"]
#target_list = ["A","B"]

header_map = {}

test_file = "data/test_v2_first_0_last_1.csv"
train_file = "data/train_first_0_last_1.csv"
output_file = "data/NB_output.csv"
def first_feature (row, target, test):
#    global features
    features={}
    for item in features_list:
        features[item]=row[header_map[item]]
    if test==0:
        features["previous"]=row[header_map["prev_actual_%s"%target]]
    else:
        features["previous"]=row[header_map["%s"%target]]
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
    test = ([(row, row[target_col_id]) for row in test_data])
    #print row,row[i],i
    #Run it for A through G
    
    train_set = [(first_feature(r, target,0), a) for (r, a) in data]
#    print featuresets
    test_set=[(first_feature(r, target,1), a) for (r, a) in test]
#    print train_set
    train_set1, train_set2 = train_set[70000:], train_set[:27010]
#    train_set = featuresets
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    #Display details
#    print "Accuracy is for %s:"%target, nltk.classify.accuracy(classifier, train_set2)
    print classifier.show_most_informative_features(5)
    for (name, value)in test_set:
        guess = classifier.classify(name)
#        output[name.customer_ID][target]=guess
#        print name
        cust_id = name['customer_ID']
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