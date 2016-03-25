'''
Created on 2015-7-11

@author: livepc
'''

#encoding=utf-8

import tushare as ts

import os
import lib.helper
import config
import os.path

def saveDataFileByCode(df):
    for idx, row in df.iterrows():
        stock_code = row['code']
        code = lib.helper.getSixDigitalStockCode(stock_code) # 将股票代码格式化为6位数字
        print("start sync ",code,"...")
        stock_k_data  = ts.get_h_data(code,start='2012-01-01',end='2015-07-10',autype='hfq')
        #stock_k_data = ts.get_hist_data(code)
        filename =  os.path.join(config.DownloadDataDir, code)
        stock_k_data.to_csv(filename, encoding="utf-8")

def syncHS300S():
    hs300s_df = ts.get_hs300s()
    hs300s_df.to_csv(config.HS300_CodePath, encoding="utf-8")
    saveDataFileByCode(hs300s_df)
    print("sync and save HS300 done!")

def syncSZ50S():
    sz50s_df = ts.get_sz50s()
    sz50s_df.to_csv(config.SZ50_CodePath, encoding="utf-8")
    saveDataFileByCode(sz50s_df)
    print("sync and save SZ50 done!")
            
def syncZZ500S():
    zz500s_df = ts.get_zz500s()
    zz500s_df.to_csv(config.ZZ500_CodePath, encoding="utf-8")
    saveDataFileByCode(zz500s_df)
    print("sync and save ZZ500 done!")

def syncAllData() :
    print("start sync...")
    syncHS300S()
    syncSZ50S()
    syncZZ500S()
    print("ALL DONE!")

def checkDirs():
    print("check file path is exist, and created folder if not exist...")
    checkdirs = []
    checkdirs.append(config.DownloadDataDir)
    checkdirs.append(config.DownloadCodeDir)
    lib.helper.checkFolder(checkdirs)
    print("CHECK DONE!")

def getDate():
    #hs300s_df = ts.get_hs300s()
    #qfq = ts.get_h_data('000024',start='2012-06-01',end='2015-06-10') #前复权
    hfq = ts.get_h_data('000024',start='2012-01-01',end='2015-07-10',autype='hfq') #后复权
    print(hfq)
    #bfq = ts.get_h_data('000024',start='2012-06-01',end='2015-06-10',autype=None) #不复权
    #datezhijian = ts.get_h_data('000024',start='2012-06-01',end='2015-06-10') #两个日期之间的前复权数据
    #print("qfq:",qfq,",hfq:",hfq,",bfq:",bfq,",datezhijian:",datezhijian)

if __name__ == '__main__':
    checkDirs()
    syncAllData()
