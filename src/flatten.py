#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Apr 10, 2014 4:55:44 PM$"

import csv
from collections import Counter
target_cols=['A','B','C','D','E','F','G','C_previous','day','time','homeowner','group_size','age_oldest','age_youngest','married_couple','cost']

head_str = []
shopping_pt_count=1
head_count=0
output=[]
#filename="test_v2"
filename="train"
#delta ={}
def updateHeader(suffix):
    global head_count
#    print head_count
    global header
    for col in target_cols:
        head = "%s-%s"%(col,suffix)
        header[head]=head_count;
        head_count+=1
        head_str.append(head)
#    print "%s,%s"%(head_count,",".join(head_str))
def writeLine(f, row):
    f.write("%s\n"%",".join(row))

#f = open('data/change.csv','w')
last = open('data/%s_flat.csv'%filename,'w')
changeLog = open('data/%s_flat_change.log'%filename,'w')
reader =[]
row_count=0

changeCount = Counter()
with open('data/%s.csv'%filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
#    row_count=0
    header={}
    previous_row = ""
    previous_id = ""
    rows =[]
    active_row=[]
    for row in reader:
        if row_count==0:
            
            for head in row:
                header[head]=head_count;
                head_count+=1
                head_str.append(head)
            updateHeader("purchase")
#            f.write("%s\n"% ",".join(head_str))
#            last.write("%s\n"% ",".join(head_str))
#            print("%s\n"% ",".join(head_str))
            row_count+=1
        else:
            outputs = {}
            customer_id = row[0]
            copy_row = list(row)
            shopping_pt = row[header['shopping_pt']]
            record_type = row[header['record_type']]

            if int(shopping_pt)>shopping_pt_count:
                if record_type=="0":
                    updateHeader(shopping_pt)
                    shopping_pt_count+=1
            #same customer
            if customer_id==previous_id: 
                suffix = ""
                if record_type=="0":
                    suffix=shopping_pt
                    for i in range(0,len(target_cols)):
                        active_row.append("")
                else:
                    suffix="purchase"
                for col in target_cols:
                    head = "%s-%s"%(col,suffix)
                    index = int(header[col])
#                    print "%s,%s,%s,%s"%(head,header[head],col,index)
                    active_row[header[head]]=copy_row[index]
                    if int(shopping_pt)>1:
                        if len(previous_row)>0 and copy_row[index]<>previous_row[index]:
#                            print "updating change count %s,%s" % (col, customer_id)
                            changeCount[col]+=1
                    
#                print "same customer"
                previous_row = list(copy_row)
                
            else:
                if len(active_row)>0:
                    output.append(list(active_row))
#                    last.write("%s\n"%",".join(active_row))
                active_row=list(row)
                #Adding purchase columns
                for i in range(0,len(target_cols)):
                    active_row.append("")
                previous_row = []
            previous_id=customer_id
    output.append(active_row)
#    last.write("%s\n"%",".join(active_row))
#    print ",".join(changeCount)
#    print changeCount
    for key in changeCount.keys():
        
        str = "%s=%s\n"%(key, changeCount[key])
        print str
        changeLog.write(str)
#    for change in changeCount:
#        print ",".join(changeCount)
#    changeLog.write(",".join(changeCount))


writeLine(last, head_str)
for row in output:
    for i in range(len(row), len(header)-len(row)):
        row.append("")
#    print ",".join(row)
    writeLine(last, row)