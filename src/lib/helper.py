'''
Created on 2015-7-11

@author: livepc
'''
#encoding=utf-8
import pandas as pd
import os
import os.path



# 补全股票代码(6位股票代码)
# input: int or string
# output: string
def getSixDigitalStockCode(code):
    strZero = ''
    for i in range(len(str(code)), 6):
        strZero += '0'
    return strZero + str(code)

def getStockDataFromFile(file_path, stock_code):
    return pd.read_csv(file_path, index_col=0)

def checkFolder(checkdirs):
    for checkdir in checkdirs :
        if(os.path.exists(checkdir)== False):  
            os.makedirs(checkdir)
            print("created ",checkdir)

