# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:13:29 2017

@author: zc
"""
import pandas as pd  
import numpy as np 

def NetValue_Index(x):
#%累计收益y0;年化收益y1;胜率\盈亏比y2,y3;最大回撤y4;波动率y5/年化波动率y6/下侧波动率y7/年化下侧波动率y8
#%夏普比率y9/索提诺比率y10/Calmarb比率y11 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%收益指标  
    a=x.shape[0]
    y0=x[-1]-1
    y1=x[-1]**(242.0/a)-1
    kk=0
    ss=0
    win=[]
    loss=[]
    for i in range(1,a):
        if x[i]>x[i-1]:
            kk=kk+1
            win.append(x[i]-x[i-1])
        elif x[i]<x[i-1]:
            ss=ss+1
            loss.append(x[i-1]-x[i])
    y2=kk*1.0/(ss+kk)
    y3=sum(win)/sum(loss)
# %%%%%%%%%%%%%%%%%%%%%%%%%风险指标
#    res=data[['net_base','net_value']].copy()
    maxx= pd.expanding_max(x)
    max_cha= 1 - x/maxx
    y4= max_cha.max()
    y=[]
    undery=[]
    for i in range(1,a):
        y.append(np.log(x[i]/x[i-1]))
        if np.log(x[i]/x[i-1])<0:
            undery.append(np.log(x[i]/x[i-1]))
    mm=(y-np.mean(y))**2
    nn=(undery-np.mean(undery))**2
    y5=np.sqrt(sum(mm)/(a-1))
    y6=y5*np.sqrt(242)
    y7=np.sqrt(sum(nn)/(len(undery)-1))
    y8=y7*np.sqrt(242)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    y9=(np.mean(y)-0.03/242)/y5*np.sqrt(242)
    y10=(np.mean(y)-0.03/242)/y7*np.sqrt(242)
    y11=y1/y4
    yy=[y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11]
    return yy     
         