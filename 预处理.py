#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 20:08:26 2021

@author: CaoHayashi
"""
from openpyxl import Workbook
from pandas import DataFrame
import numpy as np



txtNum = 1 #从第一个位置开始

while txtNum <= 324:
    f = open("./异常数据/"+str(txtNum)+".异常.txt", "r")#这边可以手动改成“正常”
    
    #首行舍弃
    str1 = f.readline()
    line = f.readline()
    
    #首行舍弃完，往下第一行为锚点A0到靶点的距离
    cnt = 1 #1代表锚点A0到靶点的距离，2代表代表锚点A1，以此类推
    sampleSS = []
    sample = []
    SS_sum = []
    while line:
        llist = line.split(':')
        if int(llist[5]) == int(llist[6]):
            sample.append( int(llist[6]) )#当校验值和采集值一致时才加进列表里
        else:
            sample.append('ineq')#否则在列表里记为ineq
        cnt += 1 #往下一行
        if cnt > 4:
            cnt = 1#当往下四行完，代表一个样本结束。下一行重新开始读取锚点A0到靶点的距离
            sampleSS.append(sample)
            SS_sum.append(np.sum(sample))
            sample = []
        line = f.readline()
        
    n_S_f = sampleSS[0]#忘记向前缩进了！
   
               
    for i in range(0,len(sampleSS)):
        sampleSS[i].append(SS_sum[i])

    
    mu = np.mean(SS_sum)
    sigma = np.std(SS_sum)
    cnt_outer = 0
    for sum_i in sampleSS:#去除异常值（3σ准则）
        if (sum_i[4] >= (mu + 3*sigma)) or (sum_i[4] <= mu - 3*sigma):
            cnt_outer += 1
            print('already:'+str(cnt_outer))
            sum_i.append('outer')#添加标记后手动去除
            
    dataF = DataFrame(sampleSS)
    new_sampleSS = dataF.drop_duplicates().values.tolist() #去重      
            
    










    
    f.close()
    #写成txt：
    # fw = open(str(txtNum)+".normal_outer.txt", "w")
    # for rr in sampleSS:
    #     sampleSS_str = ''
    #     for i in [0,1,2,3]:
    #         sampleSS_str += (str(rr[i])+'\t')
        
    #     sampleSS_str += '\n'
    #     fw.write(sampleSS_str)
        
    # fw.close()
            

    #写成excel：
    write_b = Workbook()
    write_s = write_b.active
    for row in new_sampleSS:
        # write_s_tmp = [row]
        write_s.append(row)
    # write_b.save('./abnormal_excel/'+str(txtNum)+'.abnormal.xlsx')
    write_b.save('100.abnormal_1018.xlsx')
    # print(str(txtNum)+'.异常.txt'+'完成！')
    print(str(txtNum)+' location Has:'+str(cnt_outer))
    txtNum += 1
