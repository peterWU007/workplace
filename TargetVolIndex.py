# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:57:29 2017

@author: zc
"""
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sns
import heapq
import math
import time
import datetime
#import mlab
from weight_adj import *
from NetValue_Index import *

def TargetVolIndex(TargetV,method,date,dateBgt,dateEnd):
    daily=pd.read_excel('D:\\work\\whq\\dqInvestExplorerPython.git\\trunk\\python\\ETF_test.xlsx')
    qq=daily.columns[range(1,len(daily.columns))]
    daily=pd.DataFrame(index=daily['date'],columns=qq,data=daily.values[0:daily.shape[0],1:daily.shape[1]])
    daily = daily.fillna(method='pad')#上市后若停牌，则用前值替代
    daily = daily.fillna(method='bfill')
    daily = daily.fillna(1000000)
    daily['cash']=1#
    #%%
    daily1 = daily.copy()
    for s in daily.columns:
        daily1['ln_'+s] = np.log(daily[s]*1.0/daily[s].shift(1))
        del daily1[s] 
    #daily1['ln_cash']=-1*daily1['ln_cash'] 
    #daily1['ln_A']=-1*daily1['ln_A'] 
    #daily1['ln_B']=-1*daily1['ln_B']    
    df=pd.DataFrame()
    daily1=daily1.fillna(0)
    for i in range(daily1.shape[0]):
        for j in range(daily1.shape[1]):
            if abs(daily1.iloc[i,j])>0.11:
               daily1.iloc[i,j]=0
    #%% 
#时间上的划分好                             
    ss=daily1.shape
    begd=dateBgt#'2014-1-22'
    endd=dateEnd#'2015-10-31'
    datestr01=date#'2015-1-1'
    timeArray0= time.strptime(begd, "%Y-%m-%d")
    timeStamp0= int(time.mktime(timeArray0))
    timeArray1= time.strptime(endd, "%Y-%m-%d")
    timeStamp11= int(time.mktime(timeArray1))
    timeArray = time.strptime(datestr01, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    ind = []
    for s in daily.index:
        timeArray1= time.strptime(str(s)[0:10], "%Y-%m-%d")
        timeStamp1= int(time.mktime(timeArray1))
        ind.append(timeStamp1)
    ind=np.array(ind)
    
    for k0 in range(15):
        if timeStamp0+k0*86400 in ind:
            break
    itemindex0=np.argwhere(ind==timeStamp0+k0*86400)
    
    for k1 in range(15):
        if timeStamp11+k1*86400 in ind:
            break
    itemindex1=np.argwhere(ind==timeStamp11+k1*86400)
    
    for i in range(15):
        if timeStamp+i*86400 in ind: 
            break
    new_ind=ind[itemindex0:itemindex1+1]
    itemindex = np.argwhere(new_ind==timeStamp+i*86400) 
    
    daily1=daily1.iloc[range(itemindex0,itemindex1+1),:]
    daily=daily.iloc[range(itemindex0,itemindex1+1),:]
    #%%
    #制作净值序列 
    net_total=np.exp(np.cumsum(daily1))
       #%%
    net_control=pd.DataFrame()
    net_wgt=pd.DataFrame()
    for j in range(daily.shape[1]-1):
        df=pd.DataFrame(net_total.iloc[:,j])
        df.columns=['NetValue']
        [a1,a2,a3,a4]=weight_adj(df,0.98,TargetV,0.05,method)#vol_levels[i]+0.16-i*0.01
        net_control[qq[j]]=a1
        net_control['adj_'+qq[j]]=a2
        net_wgt[qq[j]]=a3
        net_wgt['cash_'+qq[j]]=a4
    for j in range((daily.shape[1]-1)*2):
        if j==0:
            nv_index=np.array(NetValue_Index(net_control.iloc[:,j]))
        else:
            a1=np.array(NetValue_Index(net_control.iloc[:,j]))
            nv_index=np.column_stack((nv_index,a1))
    ind_name=[u'累计收益',u'年化收益',u'胜率',u'盈亏比',u'最大回撤',u'波动率',u'年化波动率',
    u'下行波动率',u'年化下行波动率',u'夏普比率',u'索提诺比率',u'Calmarb比率']
    NetV_columns=[]
    for i in  range(daily.shape[1]-1):
        NetV_columns.append(daily.columns[i])
        NetV_columns.append('adj_'+daily.columns[i])   
    NetV_index=pd.DataFrame(index=ind_name,columns=NetV_columns,data=nv_index)  
             
    return net_control,net_wgt,NetV_index
    
    
    
    
    
