#This version runs the random forest classifer for A through G.

import csv
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer

# use a small amount of train_data: "playtrain_first_0_last_1.csv" (101 rows)
# final train_file = "train_first_0_last_1.csv"

# use a small amount of testdata (10 rows):"playtest_v2_first_0_last_1.csv"
# final test_file ="test_v2_first_0_last_1.csv"

#### PICK THE TRAINING FILE AND TEST FILE.THE LAST ONES ARE THE FULL SETS ####

# SAMPLE DATA SET (small training and test)
#train_file = "playtrain_first_0_last_1.csv"
#test_file = "playtest_v2_first_0_last_1.csv"

# SAMPLE DATA SET 1000 rows training and test
#train_file = "playtrain1000_first_0_last_1.csv"
#test_file = "playtest1000_v2_first_0_last_1.csv"

# SAMPLE DATA SET 10,000 rows training and test
#train_file = "playtrain10000_first_0_last_1.csv"
#test_file = "playtest10000_v2_first_0_last_1.csv"

# SAMPLE DATA SET 100,000 rows training and test
# NOTE: This has all the data (which is 97K training, 57K test)
# IS IDENTICAL TO FINAL DATA SET
# ORIGINAL FILE: train_file = "train_first_0_last_1.csv"
# ORIGINAL FILE: "test_v2_first_0_last_1.csv"
train_file = "playtrain100000_first_0_last_1.csv"
test_file = "playtest100000_v2_first_0_last_1.csv"

#### END OF FOUR FILE SET CHOICES ###########################################

output_file = "RF_output.csv"
target_list_names = set(["A","B","C","D","E","F","G"])

###### A FEW FUNCTIONS ###################################################

def make_list_of_dictionaries(data_file):
    # takes csv with first line of headers,
    # converts each row to a dictionary with headers as keys
    # outputs a list of dictionary items

    list_dict = []
    dict_file = csv.DictReader(open(data_file))
    for row in dict_file:
        list_dict.append(row)
    return list_dict

def split_training_set_into_input_and_target(list_dict):
    # for each sample, need to pull out the appropriate elements
    # should output two lists with the same length
    input_list_dict = []
    target_list_dict = []
    target_A_list_dict = []
    target_B_list_dict = []
    target_C_list_dict = []
    target_D_list_dict = []
    target_E_list_dict = []
    target_F_list_dict = []
    target_G_list_dict = []
    customer_ID_list = []
    counter = 0


    for eachsample in list_dict:
        # ensures the same number of samples in each list
        target_list_dict.append({})
        target_A_list_dict.append({})
        target_B_list_dict.append({})
        target_C_list_dict.append({})
        target_D_list_dict.append({})
        target_E_list_dict.append({})
        target_F_list_dict.append({})
        target_G_list_dict.append({})
        input_list_dict.append({})

        for eachkey in eachsample:

            ####some processing needed (needs to be same for test data as well)
            #1 for cost truncate to hundreds (take only first digit)
            #2 for time, use only hour (take only first two digits)
            #3 for age_youngest, take only first digit
            #4 for age_oldest, take only first digit

            if eachkey == 'location':
                eachsample[eachkey] = "90210"


            if eachkey == 'time':
                eachsample[eachkey] = eachsample[eachkey][0:2]
            if eachkey == 'cost':
                eachsample[eachkey] = eachsample[eachkey][0:1]

            if eachkey == 'age_youngest':
                #account for kids <10 (less than 2 digits will become "k")
                if len(eachsample[eachkey]) == 1:
                    modded = "k" + eachsample[eachkey]
                    print "modded adds k", modded
                else:
                    modded = eachsample[eachkey]

                eachsample[eachkey] = modded[0:1]

            if eachkey == 'age_oldest':
                #account for kids <10 (less than 2 digits will become "k6")
                if len(eachsample[eachkey]) == 1:
                    modded = "k" + eachsample[eachkey]
                else:
                    modded = eachsample[eachkey]

                eachsample[eachkey] = modded[0:1]

            ##### processing complete

            if eachkey in target_list_names:
                target_list_dict[counter].update({eachkey:eachsample[eachkey]})

            if eachkey == "A":
                target_A_list_dict[counter].update({eachkey:eachsample[eachkey]})
                #print "target", eachkey, eachsample[eachkey]
            elif eachkey == "B":
                target_B_list_dict[counter].update({eachkey:eachsample[eachkey]})
            elif eachkey == "C":
                target_C_list_dict[counter].update({eachkey:eachsample[eachkey]})
            elif eachkey == "D":
                target_D_list_dict[counter].update({eachkey:eachsample[eachkey]})
            elif eachkey == "E":
                target_E_list_dict[counter].update({eachkey:eachsample[eachkey]})
            elif eachkey == "F":
                target_F_list_dict[counter].update({eachkey:eachsample[eachkey]})
            elif eachkey == "G":
                target_G_list_dict[counter].update({eachkey:eachsample[eachkey]})
            elif eachkey == "customer_ID":
                customer_ID_list.append(eachsample[eachkey])
            else:
                input_list_dict[counter].update({eachkey:eachsample[eachkey]})
                #print "input", eachkey, eachsample[eachkey]
        counter += 1

    #print "input_list_dict"
    #print input_list_dict
    #print "input_list_dict length", len(input_list_dict)
    print

    #print "target_A_list_dict:"
    #print target_A_list_dict
    #print "target_A_list_dict length", len (target_A_list_dict)
    print

    #print "customer_ID_list"
    #print customer_ID_list
    #print "customer_ID_list length", len(customer_ID_list)
    print

    print "compare training and target dict lengths"
    print len(input_list_dict[0]), len(target_list_dict[0])

    return (input_list_dict, target_list_dict, target_A_list_dict, target_B_list_dict,
            target_C_list_dict, target_D_list_dict, target_E_list_dict,
            target_F_list_dict, target_G_list_dict, customer_ID_list)

def prepare_test_data(test_list_dict_unprepped):
    # for each sample, need to pull out the appropriate elements
    # should output two lists with the same length
    test_list_dict = []
    test_customer_ID_list = []
    counter = 0

    for eachsample in test_list_dict_unprepped:
        test_list_dict.append({})

        for eachkey in eachsample:

            ####some processing needed
            #1 for cost truncate to hundreds (take only first digit)
            #2 for time, use only hour (take only first two digits)
            #3 for age_youngest, take only first digit
            #4 for age_oldest, take only first digit

            if eachkey == 'location':
                eachsample[eachkey] = "90210"

            if eachkey == 'time':
                eachsample[eachkey] = eachsample[eachkey][0:2]
            if eachkey == 'cost':
                eachsample[eachkey] = eachsample[eachkey][0:1]
            if eachkey == 'age_youngest':
                #account for kids <10 (less than 2 digits will become "k")
                if len(eachsample[eachkey]) == 1:
                    modded = "k" + eachsample[eachkey]
                else:
                    modded = eachsample[eachkey]

                eachsample[eachkey] = modded[0:1]

            if eachkey == 'age_oldest':
                #account for kids <10 (less than 2 digits will become "k")
                if len(eachsample[eachkey]) == 1:
                    modded = "k" + eachsample[eachkey]
                else:
                    modded = eachsample[eachkey]

                eachsample[eachkey] = modded[0:1]
            if eachkey == "customer_ID":
                test_customer_ID_list.append(eachsample[eachkey])
            else:
                test_list_dict[counter].update({eachkey:eachsample[eachkey]})

        counter += 1


    # TOO MUCH TO SHOW ENTIRETY OF TEST DATA
    #print test_list_dict
    #print "test_list_dict length", len(test_list_dict)
    #print


    print "test_customer_ID_list"
    print test_customer_ID_list
    print "test_customer_ID_list length", len(test_customer_ID_list)
    print

    return (test_list_dict, test_customer_ID_list)

def PredictOneLetterForAllCustomers(train_input, target_input, test_input, test_customer_ID_list):

    output_dict = {}
    vec = DictVectorizer()

    input_X_for_forest = vec.fit_transform(train_input).toarray()

    target_vectorized = DictVectorizer()
    target_y_for_forest = target_vectorized.fit_transform(target_input).toarray()



    print "target vectorized feature names (letter_map_list):"
    print target_vectorized.get_feature_names()

    forest = RandomForestClassifier(n_estimators = 100)


    # Fit the targeting data to the labels and create the decision trees
    forest = forest.fit(input_X_for_forest,target_y_for_forest)

    # Predict just one row at at time of the test_input


    for i, each_row in enumerate(test_input):

        test_X_for_forest = vec.transform(each_row).toarray()

        output = forest.predict(test_X_for_forest)
        #print "output"
        #print output
        #print
        #temp_dict = {}
        letter_map_list = []
        temp_dict = {}
        letter_map_list = target_vectorized.inverse_transform(output)
        temp_dict = letter_map_list[0]
        #print temp_dict.keys(),
        #k = tuple(temp_dict.items())
        #print type(k),

##        k, v = temp_dict.items()[1]
##        print "k is", k
        #for idx, value in enumerate(output):
#            1 == 1
            #print"letter_map_list[idx]",
            #if not value[idx] == 1.0:
                #letter_value = letter_map_list[idx][-1]
        #output_dict[test_customer_ID_list[i]] = outputtemp_dict.keys()

        output_dict[test_customer_ID_list[i]] = temp_dict.keys()

        #print "test_customer_ID_list[i], output"
        #print test_customer_ID_list[i], output
        #print "targ.inverse_transform(output)"
        #print target_vectorized.inverse_transform(output)
        #print letter_value
        print test_customer_ID_list[i], temp_dict.keys(),

    print "output_dict:"
    print output_dict
    return output_dict

######### END OF FUNCTIONS ##################################################


### prepare input and target data (binning cost and time)

list_dict = make_list_of_dictionaries(train_file)
print "list_dict is a list of dictionaries with entire data set:"
print

# grab nicely processed data
(input_list_dict, target_list_dict, target_A_list_dict, target_B_list_dict, target_C_list_dict,
target_D_list_dict,target_E_list_dict,target_F_list_dict,target_G_list_dict,
customer_ID_list)=(split_training_set_into_input_and_target(list_dict))

### prepare test data
test_list_dict_unprepped = make_list_of_dictionaries(test_file)

### prepare test data (binning cost and time)
(test_list_dict, test_customer_ID_list) = prepare_test_data(test_list_dict_unprepped)

print "input_list_dict is a list of dictionaries with the training data set:"
print "the seven target_%_list_dicts are the different target data sets for the letters"
print "test_list_dict is a list of dictionaries with the test data set:"
print


#### PREDICT ALL OUTPUTS, ONE LETTER AT A TIME, FOR ALL CUSTOMERS ############

# All the final values will be concatenated into Prediction_dict then saved to file
Prediction_dict = {}

A_dict = {}
B_dict = {}
C_dict = {}
D_dict = {}
E_dict = {}
F_dict = {}
G_dict = {}

A_dict = PredictOneLetterForAllCustomers(input_list_dict, target_A_list_dict, test_list_dict, test_customer_ID_list)

B_dict = PredictOneLetterForAllCustomers(input_list_dict, target_B_list_dict, test_list_dict, test_customer_ID_list)

C_dict = PredictOneLetterForAllCustomers(input_list_dict, target_C_list_dict, test_list_dict, test_customer_ID_list)

D_dict = PredictOneLetterForAllCustomers(input_list_dict, target_D_list_dict, test_list_dict, test_customer_ID_list)

E_dict = PredictOneLetterForAllCustomers(input_list_dict, target_E_list_dict, test_list_dict, test_customer_ID_list)

F_dict = PredictOneLetterForAllCustomers(input_list_dict, target_F_list_dict, test_list_dict, test_customer_ID_list)

G_dict = PredictOneLetterForAllCustomers(input_list_dict, target_G_list_dict, test_list_dict, test_customer_ID_list)

# CLEAN UP DATA, GIVE DIFFERENT DEFAULTS TO MISSING PREDICTION VALUES
for key, value in A_dict.items():

    if value == []:
        A_dict[key] = "0"
    else:
        A_dict[key] = value[0][-1:]

print "A's cleaned"


for key, value in B_dict.items():

    if value == []:
        B_dict[key] = "0"
    else:
        B_dict[key] = value[0][-1:]

print "B's cleaned"


for key, value in C_dict.items():

    if value == []:
        C_dict[key] = "1"
    else:
        C_dict[key] = value[0][-1:]

print "C's cleaned"


for key, value in D_dict.items():

    if value == []:
        D_dict[key] = "1"
    else:
        D_dict[key] = value[0][-1:]

print "D's cleaned"


for key, value in E_dict.items():

    if value == []:
        E_dict[key] = "0"
    else:
        E_dict[key] = value[0][-1:]

print "E's cleaned"


for key, value in F_dict.items():

    if value == []:
        F_dict[key] = "0"
    else:
        F_dict[key] = value[0][-1:]

print "F's cleaned"


for key, value in G_dict.items():

    if value == []:
        G_dict[key] = "1"
    else:
        G_dict[key] = value[0][-1:]

    #############################################################
    #Concatenate all values into the master Prediction dictionary
    Prediction_dict[key] = (A_dict[key]+B_dict[key]+C_dict[key]+D_dict[key]
                            +E_dict[key]+F_dict[key]+G_dict[key])

print "G's cleaned and Prediction_dict created"


# WRITE OUTPUT to RF_output.csv

writer = csv.writer(open(output_file, 'wb'))
writer.writerow(["customer_ID","plan"])
for key, value in Prediction_dict.items():
    writer.writerow([key, value])


#   As a curiosity, after treating letters separately, try all letters at once!
#
#   PredictOneLetterForAllCustomers(input_list_dict, target_list_dict, test_list_dict, test_customer_ID_list)

### USEFUL LINKS ############################################################
#
# http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
#
# 1. Most promising: use same object for both training and test data.
# http://stackoverflow.com/questions/21362427/handling-categorical-features-using-scikit-learn?lq=1
#
# 2. fit_transform vs. transform
# http://stackoverflow.com/questions/19770147/how-to-force-scikit-learn-dictvectorizer-not-to-discard-features
#
# 3. chance that using integers might work (some debate- I'm wary)
# http://stackoverflow.com/questions/15821751/how-to-use-dummy-variable-to-represent-categorical-data-in-python-scikit-learn-r

# 4. sckikit learn memory issues with long arrays (removed zip codes to help)
# skikit learn memory error gvc_mode in linearmodels/ridge.py
# http://stackoverflow.com/questions/16332083/python-memoryerror-when-doing-fitting-with-scikit-learn

##############################################################################
