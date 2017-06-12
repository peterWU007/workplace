# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 16:41:53 2017

@author: zc
"""
import pandas as pd  
import numpy as np  
#%%                    
def weight_adj(df,a,vol,cut,method):
       '''
     	 功能：weight_adj函数可以在持仓标的和现金之间动态调整权重，以控制持仓的波动
     	 参数：df----dataframe，里面包含'NetValue'列
     	      a ----计算日波动率的参数
     		    vol---目标波动率
     		    cut---权重改变的阈值
       返回：调整后的资产净值w_adj
     	 '''	             
       f=df.copy()['NetValue']
       f=pd.DataFrame(f)
       f['cash']=1.0
       f['log_ret'] = np.log(f['NetValue'] / f['NetValue'].shift(1))
       f['log_cash'] = np.log(f['cash'] / f['cash'].shift(1))
       f=f[1:]
       s0=f.head(242)['log_ret'].tolist()
       s02=[s*s for s in s0]
       sigma0=np.sqrt(np.sum(s02)*1.0/242)      #初始化日波动率
       
       ff=f[242:]
       sigma=[sigma0]   
       for i in range(1,ff.shape[0]):
           sigma0=np.sqrt(a*sigma0**2+(1-a)*ff['log_ret'][i]**2)
           sigma.append(sigma0)                   
     
       sigma_y=[x*np.sqrt(242) for x in sigma]  #年化波动率
       
                
       if (method==1):
          ff['sigma_y']=sigma_y
       elif (method==0):
          ff['sigma_y']=np.std(s0)*np.sqrt(242)
     
       ff['w']=ff['cash']*vol / (ff['sigma_y']*ff['NetValue']-(ff['NetValue']-ff['cash'])*vol)
       ff['w']=ff['w'].shift(1)
       ff=ff[1:]
       #去掉极值
       ff.loc[ff['w']>1,'w']=1
       ff.loc[ff['w']<0,'w']=0.0     
     
       w_adj=ff['w'].tolist() 
       log_ret=ff['log_ret'].tolist()
       for i in range(1,len(w_adj)):
           if log_ret[i-1]>0 or (log_ret[i-1]<0 and abs(w_adj[i]-w_adj[i-1])<cut):
              w_adj[i]=w_adj[i-1]
       ff['w_adj']=w_adj    
                                                                     
       fff=ff.copy()
       fff['w_cash']=1-fff['w_adj']
       fff['logR']=np.log(np.exp(fff['log_ret'])*fff['w_adj']+np.exp(fff['log_cash'])*fff['w_cash'])
       fff['net_value']=np.exp(np.cumsum(fff['logR']))
        
        
       fff['net_base']=fff['NetValue']*1.0/fff['NetValue'][0]
       fff['net_asset']=fff['net_value']*1.0/fff['net_value'][0]
        
       #fff[['net_base','net_asset']].plot()
       return fff['net_base'],fff['net_asset'],fff['w_adj'],fff['w_cash']