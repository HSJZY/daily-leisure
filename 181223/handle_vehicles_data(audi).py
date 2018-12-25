#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 10:37:19 2018

@author: jiang
"""

import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
from copy import deepcopy
from pandas import Series,DataFrame

countries=['日本','奥迪香港','奥迪越南','马来西亚','韩国','奥迪泰国','新加坡']
months=13

df = pd.read_excel('vehicle_data.xlsx', sheetname='去除杂奥迪新加坡')
df=df.iloc[:,2:-1]
#print("df.head",df.head())

rows,columns=df.shape

#获取所有汽车型号
vehicle_type=[]
vehicle_num=columns
for i in range(0,vehicle_num):
    vehicle_type.append(df.columns[i])

#获取各个国家其所有车型价格
country_vehicles=[]
for i in range(len(countries)):
    country_vehicles.append(df.iloc[i*months:(i+1)*months])    
    

#获取每种车型各时期其各个国家的对应均值
all_mean_vehicles=[] #[vehicle,month]
for i,vehicle_name in enumerate(vehicle_type):
    count_exist_country=0
    sum_price_vehiclei=np.zeros(months)
    for j in range(len(countries)):
        df_vehicle_price=country_vehicles[j][vehicle_name]
        if(pd.isnull(df_vehicle_price.iloc[0])):
            continue
        count_exist_country+=1
#        print("sum_price_vehiclei:",sum_price_vehiclei,"df_vehicle_price.values:",df_vehicle_price.values)
        sum_price_vehiclei+=df_vehicle_price.values
    sum_price_vehiclei/=count_exist_country
    all_mean_vehicles.append(sum_price_vehiclei)
all_mean_vehicles=np.array(all_mean_vehicles)
assert len(all_mean_vehicles)==vehicle_num


df_relative_price=deepcopy(df)#获取相对价格
for i,vehicle_name in enumerate(vehicle_type):
    for j in range(rows):
        if pd.isnull(df_relative_price.iloc[j,i]):
            continue
        df_relative_price.iloc[j,i]=np.log(df_relative_price.iloc[j,i])-np.log(all_mean_vehicles[i][j%13])


#--------------------计算标准差---------------------------------------
df_std=deepcopy(df_relative_price)
#获取各个国家其所有车型相对价格横向取平均
country_vehicles_relative=[]
month_vehicles_avg=np.zeros(months)
mean_each_rows=[]
for i in range(rows):
    df_row_i=df_relative_price.iloc[i,:]
    df_row_i.dropna(inplace=True)
    mean_row_i=df_row_i.mean()
#    print("mean_i",mean_row_i)
    mean_each_rows.append(mean_row_i)

mean_each_month=np.zeros(months)
for i in range(rows):
    mean_each_month[i%months]+=(mean_each_rows[i]/len(countries))

square_relative_sum=np.zeros(months)
counts=np.zeros(months)
for i in range(rows):
    for j in range(columns):
        if pd.isnull(df_relative_price.iloc[i,j]):
            continue
        square_relative_sum[i%months]+=(df_relative_price.iloc[i,j]-mean_each_month[i%months])**2
        counts[i%months]+=1

#求相对价格的标准差
std_relative=np.zeros(months)
for i in range(months):
    std_relative[i]=np.sqrt(square_relative_sum[i]/counts[i])
print("std relative price:",std_relative)
#--------------------以上计算标准差---------------------------------------

Q_i_jk_t=np.zeros((len(vehicle_type),len(countries),len(countries),months))
Q_i_jk_t_mask=np.zeros((len(countries),len(countries)))
for i,vehicle_name in enumerate(vehicle_type):
    #获取两个国家的全组合
    select_two_set=[]
    for j in range(len(countries)):
        for k in range(j+1,len(countries)):
            if pd.isnull(df[vehicle_name].iloc[j*months]) or pd.isnull(df[vehicle_name].iloc[k*months]):
                continue
            select_two_set.append((j,k))

    for j in range(len(select_two_set)):
        country_j_price=country_vehicles[select_two_set[j][0]]
        country_k_price=country_vehicles[select_two_set[j][1]]
#        print("j:",j,"k:",k,"\ncountry_j_price:",country_j_price.head(2),"country_k_price",country_k_price.head(2))
        for t in range(months):
            Q_i_jk_t[i][select_two_set[j][0]][select_two_set[j][1]][t]=np.log(country_j_price[vehicle_name].iloc[t])-np.log(country_k_price[vehicle_name].iloc[t])
            Q_i_jk_t_mask[select_two_set[j][0]][select_two_set[j][1]]=1
Q_star_i_t=np.zeros((len(vehicle_type),months))
mask_counts=np.sum(Q_i_jk_t_mask)
for i in range(len(vehicle_type)):
    for t in range(months):
        for j in range(len(countries)):
            for k in range(len(countries)):
                if int(Q_i_jk_t_mask[j][k])==1:
                    Q_star_i_t[i][t]+=Q_i_jk_t[i][j][k][t]/mask_counts

q_i_jk_t=deepcopy(Q_i_jk_t)
for i in range(len(vehicle_type)):
    for j in range(len(countries)):
        for k in range(len(countries)):
            if int(Q_i_jk_t_mask[j][k])!=1:
                continue
            for t in range(months):
                q_i_jk_t[i][j][k][t]-=Q_star_i_t[i][t]

S_jk_t_avg=np.zeros((len(countries),len(countries),months))
S_jk_t=np.zeros((len(countries),len(countries),months))
for j in range(len(countries)):
    for k in range(len(countries)):
        for t in range(months):
            if int(Q_i_jk_t_mask[j][k])!=1:
                continue
            vehicle_counts=0
            for i in range(len(vehicle_type)):
                if q_i_jk_t[i][j][k][t]==0:
                    continue
                vehicle_counts+=1
                S_jk_t_avg[j][k][t]+=q_i_jk_t[i][j][k][t]
            S_jk_t_avg[j][k][t]/=vehicle_counts
            
            std_jk_t=0
            std_counts=0
            for i in range(len(vehicle_type)):
                if q_i_jk_t[i][j][k][t]==0:
                    continue
                std_jk_t+=(q_i_jk_t[i][j][k][t]-S_jk_t_avg[j][k][t])**2
                std_counts+=1
            if std_counts==0:
                continue
            std_jk_t/=std_counts
            S_jk_t[j][k][t]=np.sqrt(std_jk_t)
#------------------article 2-------------------------------------------------
#对价格取ln
country_vehicles_ln=deepcopy(country_vehicles)
for i,vehicle_name in enumerate(vehicle_type):
    for j in range(len(countries)):
        for t in range(months):
            if pd.isnull(country_vehicles_ln[j][vehicle_name].iloc[t]):
                break
            country_vehicles_ln[j][vehicle_name].iloc[t]=np.log(country_vehicles_ln[j][vehicle_name].iloc[t])
    
#获取每种车型各时期其各个国家的对应均值ln
all_mean_vehicles_ln=[] #[vehicle,month]
for i,vehicle_name in enumerate(vehicle_type):
    count_exist_country=0
    sum_price_vehiclei_ln=np.zeros(months)
    for j in range(len(countries)):
        df_vehicle_price=country_vehicles_ln[j][vehicle_name]
        if(pd.isnull(df_vehicle_price.iloc[0])):
            continue
        count_exist_country+=1
#        print("sum_price_vehiclei:",sum_price_vehiclei,"df_vehicle_price.values:",df_vehicle_price.values)
        sum_price_vehiclei_ln+=df_vehicle_price.values
    sum_price_vehiclei_ln/=count_exist_country
    all_mean_vehicles_ln.append(sum_price_vehiclei_ln)
all_mean_vehicles_ln=np.array(all_mean_vehicles_ln)
assert len(all_mean_vehicles_ln)==vehicle_num

S_i_t=np.zeros((len(vehicle_type),months))

for i,vehicle_name in enumerate(vehicle_type):
    for t in range(months):
        square_sum_S_i_t=0
        countries_count=0
        for j in range(len(countries)):
            if pd.isnull(country_vehicles_ln[j][vehicle_name].iloc[0]):
                continue
#            print('all_mean_vehicles_ln[i][t]:',all_mean_vehicles_ln[i][t])
#            print("country_vehicles_ln[j][vehicle_name][t]:",country_vehicles_ln[j][vehicle_name][t])
            square_sum_S_i_t+=(country_vehicles_ln[j][vehicle_name].iloc[t]-all_mean_vehicles_ln[i][t])**2
            countries_count+=1
        if countries_count==0:
            continue
        square_sum_S_i_t/=countries_count
#        print("i:",i,"t:",t)
        S_i_t[i][t]=np.sqrt(square_sum_S_i_t)

df_s_i_t=DataFrame(S_i_t.T, columns = vehicle_type)
#---------------------------------------------------------------------------- 
#生成excel计算表格
writer = pd.ExcelWriter('./result_audi.xlsx',engine='openpyxl')
#-------------------------生成第一个表格，包括原始数据以及同一产品不同国家之间标准差----------------
df_combine=pd.concat([df,df_s_i_t])
df_combine['time']=[i+1 for i in range(months)]*(len(countries)+1)
df_combine['标头']=[np.nan for i in range(df_combine.shape[0])]
for i,country_name in enumerate(countries):
    df_combine['标头'].iloc[i*months]=countries[i]
df_combine['标头'].iloc[months*len(countries)]='S_i_t'
order_columns=['标头','time']
order_columns.extend(vehicle_type)
print("order_columns:",order_columns)
df_combine=df_combine[order_columns]
df_combine.to_excel(excel_writer=writer, sheet_name='原始数据-S_i_t', encoding="utf-8", index=False)
#---------------------------------------------------------------------------------------------------

for j in range(len(countries)):
    for k in range(len(countries)):
        print('j:',j,'k:',k)
        if int(Q_i_jk_t_mask[j][k]) !=1:
            continue
        country_j_name=countries[j]
        country_k_name=countries[k]
        columns_name=["标头","时间t1"]
        country_j_price=country_vehicles[j]
        country_k_price=country_vehicles[k]
        for column_name in country_j_price.columns:
            columns_name.append(column_name)
        right_table_columns=["国家1","国家2","时间t2","产品","价格差异",'q_i_jk_t']
        table_1_columns=deepcopy(columns_name)
        columns_name.extend(right_table_columns)
        res_dict={}
        res_dict[columns_name[0]]=[np.nan for i in range(6*months)]
        res_dict[columns_name[0]][0]=country_j_name
        res_dict[columns_name[0]][months]=country_k_name
        res_dict[columns_name[0]][months*2]='Q_i_jk_t=ln(pitj)-ln(pitk)'
        res_dict[columns_name[0]][months*3]='q_i_jk_t=Q_i_jk_t-Q_star_i_t'
        res_dict[columns_name[0]][months*4]='S_jk_t'
        res_dict[columns_name[0]][months*5]='SD_star_t'
        res_dict[columns_name[1]]=[i for i in range(1,months+1)]*6
        
        for i,vehicle_name in enumerate(vehicle_type):
            res_dict[vehicle_name]=country_j_price[vehicle_name].values.tolist()
            res_dict[vehicle_name].extend(country_k_price[vehicle_name].values)
            res_dict[vehicle_name].extend(Q_i_jk_t[i][j][k][:])
            res_dict[vehicle_name].extend(q_i_jk_t[i][j][k][:])
            if i==0:
                res_dict[vehicle_name].extend(S_jk_t[j][k][:])
                res_dict[vehicle_name].extend(std_relative)
                res_dict[right_table_columns[0]]=[country_j_name for i in range(months)]
                res_dict[right_table_columns[1]]=[country_k_name for i in range(months)]
                res_dict[right_table_columns[2]]=[i for i in range(months)]
                res_dict[right_table_columns[3]]=[vehicle_name for i in range(months)]
                res_dict[right_table_columns[4]]=Q_i_jk_t[i][j][k][:].tolist()
                res_dict[right_table_columns[5]]=q_i_jk_t[i][j][k][:].tolist()
            else:
                res_dict[right_table_columns[0]].extend([country_j_name for i in range(months)])
                res_dict[right_table_columns[1]].extend([country_k_name for i in range(months)])
                res_dict[right_table_columns[2]].extend([i for i in range(months)])
                res_dict[right_table_columns[3]].extend([vehicle_name for i in range(months)])
                res_dict[right_table_columns[4]].extend(Q_i_jk_t[i][j][k][:])
                res_dict[right_table_columns[5]].extend(q_i_jk_t[i][j][k][:])
#        print("res_dict:",res_dict)
        table_size=0
        for i,item in res_dict.items():
            table_size=max(len(item),table_size)
        for column_name in table_1_columns:
            num_addnull=table_size-len(res_dict[column_name])
            res_dict[column_name].extend([np.nan for i in range(num_addnull)])
        df_j_k=DataFrame(res_dict,columns=columns_name)
        sheet_name=country_j_name+'-'+country_k_name
        df_j_k.to_excel(excel_writer=writer, sheet_name=sheet_name, encoding="utf-8", index=False)
writer.save()
writer.close()
            
        
        







