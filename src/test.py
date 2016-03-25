'''
Created on 2015-7-11

@author: livepc
'''

#encoding=utf-8

import tushare as ts
import pandas as pd
from pandas import Series, DataFrame
import os
import config
import lib.helper

def syncData() :
    hs300s_df = ts.get_sz50s()
    hs300s_df.to_csv(config.SZ50_CodePath, encoding="utf-8")

#     for idx, row in hs300s_df.iterrows():
#         stock_code = row['code']
#         code = config.getSixDigitalStockCode(stock_code) # 将股票代码格式化为6位数字
#         stock_k_data = ts.get_hist_data(code)
#         filename =  os.path.join(config.DownloadDataDir, code)
#         stock_k_data.to_csv(filename)

#def JudgeOK(someday_stock) :
   
       
def chooseStock(date) :
    month = int(date[4:6])
    if month<10 :
        month_str = '0'+str(month)
    else :
        month_str = str(month)
    day = int(date[6:8])
    if day<10 :
        day_str = '0'+str(day)
    else :
        day_str = str(day)
    year = int(date[0:4])
    date_str = str(year) + '-' + month_str + '-' + day_str
    print("year=",year,", month=",month,", day=",day)
    print(date_str)
    mystock = pd.read_csv(config.SZ50_CodePath)
    for idx, row in mystock.iterrows():
        stock_code = row['code']
        code = lib.helper.getSixDigitalStockCode(stock_code) # 将股票代码格式化为6位数字
        print('------------stock_code:',code,'------------')
        filename =  os.path.join(config.DownloadDataDir, code)
        stock_k_data = pd.read_csv(filename, index_col=0)
#         print(filename)
#         print(code,',',len(stock_k_data))
#         print(stock_k_data.index)
        #frame = DataFrame(stock_k_data, columns=['open','close','high','low'])
       
        if not len(stock_k_data) ==0 and date_str in stock_k_data.index :
            someday_df = stock_k_data.loc[date_str]
            print('stock_code:',code,',stock_k_data:', someday_df)
            #TODO slect stock
        else :
            print('stock_code:',code,' is empty')
#        print(stock_k_data)

syncData()
# test =ts.get_hist_data('000001')
# print(test.loc['2015-07-03'])
# test.to_csv('test.csv')
#test_read = pd.read_csv('/home/hanchunyu/workspace/stock/uTushare/stockdata/603993', index_col=0)
#print(test_read.loc['2015-07-03'])
chooseStock('20150415')
#frame = DataFrame(stock_k_data, columns=['open','close','high','low'])


#print(frame.loc['2015-01-05'])
#df = DataFrame.read_csv('stock_code.csv', chunksize=10000)
#for chunk in hs300s_df:
    # TODO: process the chunk as a normal DataFrame
#    print(chunk.values)


# newdf = DataFrame()
# for idx, row in hs300s_df.iterrows():
#     # TODO: handle index and row
#     stock_code = row['code']
#     stock_k_data = ts.get_hist_data(stock_code,start='2015-01-05',end='2015-01-09')
#     newdf = stock_k_data.merge(newdf)
# print( newdf)