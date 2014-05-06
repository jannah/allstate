#This version runs the classifer for A through G.
import nltk
import csv, math, json, time
from collections import Counter
from pprint import pprint
from itertools import combinations

features_list=["customer_ID", "day", "state",  "group_size","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous", "cost"]
features_list2=[ "day", "state",  "group_size","homeowner","car_age", "age_oldest", "age_youngest","married_couple","C_previous","previous", "cost"]

target_list = ["A","B","C","D","E","F","G"]
prev_list =  ["A","B","C","D","E","F","G" ,"cost"]
target_feature_list = {}
#target_list = ["A","B"]
#set thsi flag to 1 if you want to include previous values
usePrevious = 1
usePrevious2 = 1
include_previous = 2
useFirst=0
header_map = {}
raw_data = []
test_data=[]
output = {}
test_file = "data/test_v2_first_0_last_1_2.csv"
train_file = "data/train_first_0_last_1_2.csv"
start_time = time.strftime("%Y%m%d-%H-%M-%S")
output_file = "data/NB_output%s.csv"%start_time
bucket_car_age=1
bucket_ages = 0


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

def first_feature (row, target, test, active_headers):
#    global features
    features={}
    for item in active_headers:
#        print item
        if item == "previous":
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
    
    if useFirst==1:
        features["first"]=row[header_map["1_actual_%s"%target]]
    return features

def load_header(row):
    global header_map
    for i in range(0,len(row)):
        header_map[row[i]]=i
def load_data():
    with open(train_file) as csvfile:
        reader = csv.reader(csvfile)
        row_count=0
        for row in reader:
            if row_count==0:
                load_header(row)
                row_count+=1
            else:
                raw_data.append(row)

    with open(test_file) as csvfile:
        reader = csv.reader(csvfile)
        row_count=0
        for row in reader:
            if row_count==0:
    #            load_header(row)
                row_count+=1
            else:
                test_data.append(row)
                output[row[0]]={}
def start(active_headers, active_targets, print_output):
    global raw_data
    global test_data
    global output
    if len(active_headers)==0:
        active_headers = target_feature_list
    if len(active_targets)==0:
        active_targets = target_list
    accuracy_list = {}
    for i in range(0,len(active_targets)):
        target= active_targets[i]
#        print target
        target_col_id= header_map[target]
#        print "Training for %s on %s"% (target, ",".join(active_headers))
        data = ([(row, row[target_col_id]) for row in raw_data])
        test = ([(row[0],row, row[target_col_id]) for row in test_data])
        test2 = ([(row, row[target_col_id]) for row in test_data])
        #Run it for A through G
#        print  active_headers
        train_set = [(first_feature(r, target,0, active_headers), a) for (r, a) in data]
#        print train_set[0]
        test_set=[(c, first_feature(r, target,1, active_headers), a) for (c, r, a) in test]
        test_set2=[(first_feature(r, target,1, active_headers), a) for (r, a) in test2]
    #    print train_set[0]
    #    train_set1, train_set2 = train_set[70000:], train_set[:27010]
    #    train_set = featuresets
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        #Display details
        accuracy_list[target]=nltk.classify.accuracy(classifier, test_set2)
#        print "Accuracy is for %s:"%target, accuracy_list[target]
#        print classifier.show_most_informative_features(20)
        useful = classifier.most_informative_features(20)
        feature_counter = Counter()
        for index in range(0, len(useful)):
    #        print useful[index]
            item, value = useful[index]
            feature_counter[item]+=1
#        print feature_counter
        # START CLASSIFYING
        for (cust_id, name, value)in test_set:
            guess = classifier.classify(name)
            output[cust_id][target]=guess
    
    if print_output==1:
        f = open(output_file,'w')
        f.write("customer_ID,plan\n")
        for out in output:
            value = ""
            for i in range(0,len(target_list)):
                target= target_list[i]
                value+= str(output[out][target])
            v = "%s,%s\n"%(out, value)
            f.write(v)
    return accuracy_list 
        
def findAccuracy(config):
    config2 = config
    acc_file = "data/logs/NB_output_accuracy%s.log"%time.strftime("%Y%m%d-%H%M%S")
    af = open(acc_file,'w')
    #    f.write("customer_ID,plan\n")
    accuracies = []
    top_acc = {}
    #target_list=["A"]
    for j in range(0, len(target_list)):

        target_output = target_list[j]
        print "Analyzing %s"%(target_output)
        af.write("Analyzing %s\n"%(target_output))
        top_acc[target_output] = {'value':0, 'config':""}
        for i in range (2, len(features_list2)+1):
        #    print i
            print "%s Combo Size %s"%(target_output, i)
            af.write("%s Combo Size %s\n"%(target_output, i))
            for config2 in combinations(features_list2, i):
        #        print config2
                acc = start(config2, [target_output], 0)
                accuracies.append({'target': target_output, 'config':config2, 'accuracy':acc[target_output]})
                if acc[target_output]> top_acc[target_output]['value']:
                    top_acc[target_output]['value']=acc[target_output]
                    top_acc[target_output]['config']='","'.join(config2)
                    af.write("%s\t%st\%s\t[%s]\n"%(time.strftime("%Y%m%d-%H-%M-%S"), target_output, top_acc[target_output]['value'], top_acc[target_output]['config']))
    #                pprint(top_acc)
            print "%s\t%s\t%s\t[%s]"%(time.strftime("%Y-%m-%d\t%H-%M-%S"), target_output, top_acc[target_output]['value'], top_acc[target_output]['config'])
        print "final for %s"%target_output
        print "%s\t%s\t%s\t[%s]"%(time.strftime("%Y-%m-%d\t%H-%M-%S"), target_output, top_acc[target_output]['value'], top_acc[target_output]['config'])

    print "finish time: %s"%time.strftime("%Y-%m-%d\t%H-%M-%S")
    pprint(accuracies)
    config_file_out = "config/acc_config%s.json"%start_time
    cfo = open(config_file_out,'w')
    cfo.write('{')
    count = 0
    for target in top_acc:
    #    out=top_acc[j]
        if count>0:
            cfo.write(",\n")
        cfo.write('"%s":["%s"]'%(target, top_acc[target]['config']))

        count+=1
    cfo.write('}')


print start_time
config ={}
#the config files has the featurs for each output value
config_file = "default.json"
with open('config/%s'%config_file) as data_file:    
    config = json.load(data_file)
#pprint(config)
load_data()

### Chose one of two modes.
start(config, target_list, 1)
#findAccuracy(config)
