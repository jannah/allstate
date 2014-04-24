#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Apr 10, 2014 4:55:44 PM$"

import csv
target_cols=['A','B','C','D','E','F','G','C_previous']
demo_cols=['homeowner','group_size','age_oldest','age_youngest','married_couple']

head_str = []
change_over_limit=1
first_entries =0
#last_1=[]
#last_2=[]
#last_entry=[[]]*change_over_limit
output=[[]]*(change_over_limit+first_entries)
#for i in range(0,change_over_limit):
#    last_entry.append([])
#filename = "train"
#filename="test_train"
filename="test_v2"
f = open('data/%s_change.csv'%filename,'w')
last = open('data/%s_first_%s_last_%s.csv'%(filename,first_entries,change_over_limit),'w')
with open('data/%s.csv'%filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_count=0
    header={}
    previous_row = ""
    previous_id = ""
    first_row = ""
    second_row = ""
    sub_row=0
    user_points=0
    rows = list(reader)
    total_rows = len(rows)
    row_count=0
#    print "rows = %s"%len(list(reader))
#    reader.len
    for row in rows:
        row_count+=1
        sub_row+=1
        user_points+=1
        if row_count==1:
            head_count=0
            for head in row:
                header[head]=head_count
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
                header["1_actual_%s"%col]=head_count
                head_count+=1
                head_str.append("1_actual_%s"%col)
                header["d2_%s"%col]=head_count
                head_count+=1
                head_str.append("d2_%s"%col)
                header["prev_actual_%s"%col]=head_count
                head_count+=1
                head_str.append("prev_actual_%s"%col)
            head_str.append("order")
            print "%s\n"% ",".join(head_str)
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
                copy_row.append("")
                copy_row.append("")
            if customer_id<>previous_id:
                sub_row=1
#            for demo in demo_cols:
#                demo_id = header[demo]
#                if sub_row>1:
#                    if copy_row[demo_id]<>previous_row[demo_id]:
#                        sub_row =1
#                        print "reset for %s on %s at %s"%(customer_id,demo, shopping_pt)
#                demo_id_old = header["prev_%s"%demo]
            for col in target_cols:
                col_id = header[col]
                col_id_old = header["prev_%s"%col]
                col_id1 = header["d1_%s"%col]
                col_id1_actual = header["1_actual_%s"%col]
                col_id2 = header["d2_%s"%col]
                col_id_prev_actual = header["prev_actual_%s"%col]
                val = 0
                val1 = 0
                val2 = 0

                if sub_row>1:
                    if row[col_id]<>previous_row[col_id]:
                        val =1
                    if row[col_id]<>first_row[col_id]:
                        val1=1
                    if len(second_row)>0 and row[col_id]<>second_row[col_id]:
                        val2=1
                copy_row[col_id_old]= "%s"% val
                copy_row[col_id1]= "%s"% val1
                copy_row[col_id2]= "%s"% val2
                if len(previous_row)>0:
                    copy_row[col_id_prev_actual]="%s"%previous_row[col_id]
                if len(first_row)>0:
                    copy_row[col_id1_actual]="%s"%first_row[col_id]
            f.write("%s\n"% (",".join(copy_row)))
            shopping_pt = row[header['shopping_pt']]
            if (shopping_pt=="1" or row_count==total_rows):
                out_len = len(output)
                if row_count==total_rows:
                    done = 0
                    for i in range(0,out_len):
                        if len(output[i])==0 and done==0:
                            output[i]=list(copy_row)
                            done=1
                    if done==0:
                        for i in range(0,change_over_limit-1):
                            output[first_entries+i]=output[first_entries+i+1]
                        output[first_entries+change_over_limit-1]=list(copy_row)
                    output[out_len-1]=list(copy_row)
                sub_row=1
                count_printed=1
                user_points-=1
                delta = out_len-user_points
                #fill 1st point forward
                if delta>1:
#                    print "%s,%s,%s"%(user_points, out_len,delta)
#                    for out in output:
#                        print ",".join(out)
                    fill = len(output[out_len-1])==0
                    for i in range(1,user_points-1):
                        if fill:
                            output[out_len-i]=list(output[out_len-delta-i])
                    for i in range(2, delta):
#                        print "fixing %s"%i
                        output[i]=list(output[1])
                    for i in range(2,out_len):
                        if len(output[i])==0:
                            output[i]=output[i-1]
#                    print "after"
#                    for out in output:
#                        print ",".join(out)
                for i in range(0,out_len):
                    if len(output[i])>0:
                        last.write("%s,%s\n"%(",".join(output[i]),i+1))
                    output[i]=[]
                first_row = list(copy_row)
                output[0]=list(copy_row)
#                for i in range(1,out_len-1):
##                    print "resetting"
#                    output[i]=[]
                user_points = 1
            else:
                for i in range(0,first_entries-1):
                    if sub_row==2:
                        second_row = list(copy_row)
                        output[1]=list(second_row)
                    i=i+2
                    if sub_row==i:
                        output[i-1]=list(copy_row)
                for i in range(0,change_over_limit-1):
                    output[first_entries+i]=output[first_entries+i+1]
                output[first_entries+change_over_limit-1]=list(copy_row)
            previous_row = row
            previous_id = row[0]
        
#    count_printed=1
#    for i in range(0,len(output)):
#        last.write("%s,%s\n"%(",".join(output[i]),i+1))
    
