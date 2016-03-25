'''
Created on 2015-7-12

@author: livepc
'''
#encoding=utf-8

import pandas as pd
import lib.helper
import config
from stock import Stock

class StockPool(object):
    def __init__(self):
        self.HS300S = []
        self.SZ50S = []
        self.ZZ500S = []
        self.initHS300S()
        self.initSZ50S()
        self.initZZ500S()
        
    def initHS300S(self):
        hs300s_df = pd.read_csv(config.HS300_CodePath, index_col=0)
        for idx, row in hs300s_df.iterrows():
            stock_code = row['code']
            stock_name = row['name']
            code = lib.helper.getSixDigitalStockCode(stock_code) # 将股票代码格式化为6位数字
            stocks = Stock(code, stock_name)
            self.HS300S.append(stocks)
            
    def initSZ50S(self):
        sz50s_df = pd.read_csv(config.SZ50_CodePath)
        for idx, row in sz50s_df.iterrows():
            stock_code = row['code']
            stock_name = row['name']
            code = lib.helper.getSixDigitalStockCode(stock_code) # 将股票代码格式化为6位数字
            stocks = Stock(code, stock_name)
            self.SZ50S.append(stocks)
            
    def initZZ500S(self):
        zz500s_df = pd.read_csv(config.ZZ500_CodePath)
        for idx, row in zz500s_df.iterrows():
            stock_code = row['code']
            stock_name = row['name']
            code = lib.helper.getSixDigitalStockCode(stock_code) # 将股票代码格式化为6位数字
            stocks = Stock(code, stock_name)
            self.ZZ500S.append(stocks)
            