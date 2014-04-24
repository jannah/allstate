#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Apr 10, 2014 4:55:44 PM$"

import csv
target_cols=['A','B','C','D','E','F','G','C_previous']

head_str = []
change_over_limit=2
first_entries =2
#last_1=[]
#last_2=[]
last_entry=[[]]*change_over_limit

#for i in range(0,change_over_limit):
#    last_entry.append([])
f = open('data/change.csv','w')
last = open('data/first_%s_last_%s.csv'%(first_entries,change_over_limit),'w')
with open('data/train.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_count=0
    header={}
    previous_row = ""
    previous_id = ""
    first_row = ""
    second_row = ""
    for row in reader:
        if row_count==0:
            head_count=0
            for head in row:
                header[head]=head_count;
                head_count+=1
                head_str.append(head)
            for col in target_cols:
                header["prev_%s"%col]=head_count
                head_count+=1
                head_str.append("prev_%s"%col)
#            for col in target_cols:
                header["d1_%s"%col]=head_count
                head_count+=1
                head_str.append("d1_%s"%col)
                header["d2_%s"%col]=head_count
                head_count+=1
                head_str.append("d2_%s"%col)
            head_str.append("order")
            f.write("%s\n"% ",".join(head_str))
            last.write("%s\n"% ",".join(head_str))
        else:
            outputs = {}
            customer_id = row[0]
            copy_row = list(row)
#            copy_row.append("")
#            copy_row.append("")
            for col in target_cols:
                copy_row.append("")
                copy_row.append("")
                copy_row.append("")
            for col in target_cols:
                col_id = header[col]
                col_id_old = header["prev_%s"%col]
                col_id1 = header["d1_%s"%col]
                col_id2 = header["d2_%s"%col]
                val = 0
                val1 = 0
                val2 = 0
                
                if customer_id==previous_id:
                    if row[col_id]<>previous_row[col_id]:
                        val =1
                    if row[col_id]<>first_row[col_id]:
                        val1=1
                    if len(second_row)>0 and row[col_id]<>second_row[col_id]:
                        val2=1
                copy_row[col_id_old]= "%s"% val
                copy_row[col_id1]= "%s"% val1
                copy_row[col_id2]= "%s"% val2
            f.write("%s\n"% (",".join(copy_row)))
            shopping_pt = row[header['shopping_pt']]
            if shopping_pt=="1":
                count_printed=1
                for i in range(0,change_over_limit):
                    if len(last_entry[i])>0:
                        count_printed+=1
                        last.write("%s,%s\n"%(",".join(last_entry[i]),count_printed))
                last.write("%s,%s\n"%(",".join(copy_row),1))
                first_row = list(copy_row)
#                print first_row
            for i in range(0,first_entries-1):
                if shopping_pt=="2":
                    second_row = list(copy_row)
                i=i+2
#                print str(i)
                if shopping_pt==str(i):
                    last.write("%s,%s\n"%(",".join(copy_row),shopping_pt))
            for i in range(0,change_over_limit-1):
                last_entry[i]=list(last_entry[i+1])
            last_entry[change_over_limit-1]=list(copy_row)
            previous_row = row
            previous_id = row[0]
        row_count+=1
    count_printed=1
    for i in range(0,change_over_limit):
        if len(last_entry[i])>0:
            count_printed+=1
            last.write("%s,%s\n"%(",".join(last_entry[i]),count_printed))
   
#    last.write("%s\n"%",".join(last_1))
#    last.write(",".join(last_2))
                
