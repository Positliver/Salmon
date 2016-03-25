'''
Created on 2015-7-11

@author: livepc
'''
#encoding=utf-8
from enum import Enum

import config
import lib.helper
import os
import os.path
import pandas as pd
from holdingStockStatus import holdingStockStatus, orderRecord 
from selectStockModel import checkModel
#from manager import myfund

def dateFormatForStock(date):  #date : 2015-01-01
    listdate = str(date).split('-')
    month = int(listdate[1])
    if month<10 :
        month_str = '0'+str(month)
    else :
        month_str = str(month)
    day = int(listdate[2])
    if day<10 :
        day_str = '0'+str(day)
    else :
        day_str = str(day)
    year = int(listdate[0])
    date_str = str(year) + '-' + month_str + '-' + day_str
    return date_str
    

    
class Stock(object):
    '''
    classdocs
    '''             
    def __init__(self, stock_code, stock_name):
        '''
        Constructor
        '''
        self.code = stock_code
        self.name = stock_name
        self.initStocks()
        self.holdingStockStatus = holdingStockStatus(stock_code, stock_name, 0,0)
        self.waitDelegateBuy = []
        self.preDataFrame = []
        self.todayDataFrame = []
        self.todayIsOK = False
        self.needBuy = 0  #  0-不需要买入 1-需要补仓 2-根据得分判断是否买入
        
    def initStocks(self):   # 从csv文件里面获取该股票的历史交易信息
        stock_code = lib.helper.getSixDigitalStockCode(self.code) # 将股票代码格式化为6位数字
        #print('------------stock_code:',code,'------------')
        filename =  os.path.join(config.DownloadDataDir, stock_code)
        self.stock_k_data = pd.read_csv(filename, index_col=0)  #stock_k_data type is dataframe , 保存历史交易信息
    def __getTodayDateFrame(self,day):
        indexlist = list(self.stock_k_data.index)
        if not len(self.stock_k_data) ==0 and str(day) in indexlist :
            return self.stock_k_data.loc[str(day)]
        else :
            return []

        
    def __getPreDateFrame(self,day):
        indexlist = list(self.stock_k_data.index)
        if not len(self.stock_k_data) ==0 and str(day) in indexlist :
            currentPositionIndex = indexlist.index(str(day))
            if currentPositionIndex == 1 :
                return []
            preDate_df = self.stock_k_data.iloc[int(currentPositionIndex)-1]
            #preDate = preDate_df.name            
            return preDate_df
        else :
            return []                   
        
    def getHoldingNumber(self):
        return self.holdingStockStatus.number
    
    def startDay(self, day):       
        if len(self.todayDataFrame) != 0 :           
            self.preDataFrame = self.todayDataFrame
            self.todayDataFrame = self.__getTodayDateFrame(day)
        else :
            self.preDataFrame = self.__getPreDateFrame(day)
            self.todayDataFrame = self.__getTodayDateFrame(day)
        if len(self.todayDataFrame) ==0 :
            self.todayIsOK = False
            return False
        self.pretodayDataFrame = self.todayDataFrame  # pretodayDataFrame 用于没有当天的数据时候采用上次获得数据， 以此来计算当前的持仓金额
        #self.countDay = distanceOfTwoDay(self.todayDataFrame.name, self.preDataFrame.name)
        #if self.countDay > config.MAXDISTANCE_DAYS :
            #print("stock_code:", self.code, ",-day1:", self.preDataFrame.name, ",day2:", self.todayDataFrame.name, " the distance of two day is greater than 7 days! ")
            #self.todayIsOK = True
            #return True
        self.todayIsOK = True
        return self.holdingStockStatus.startDay()
                  
    def kaiPanJiaoYi(self, date):
        if not self.todayIsOK :
            return 0
        open_price_today = self.todayDataFrame['open']
        high_price_today = self.todayDataFrame['high']
        close_price_today = self.todayDataFrame['close']
        low_price_today = self.todayDataFrame['low']
        if self.holdingStockStatus.number != 0:
            number = self.holdingStockStatus.number 
            # 计算开牌卖出价格
            if self.holdingStockStatus.days > config.MOST_DAYS_CHIGU \
            or (self.holdingStockStatus.getCostPrice() *config.GEROU_SCALE_0> open_price_today) :
                price = open_price_today
                print("割肉卖出----------------->日期:",date,",代码:",self.code,", 名称:", self.name ," 成本价格:",self.holdingStockStatus.getCostPrice(),\
                      " 卖出价格：",open_price_today," 卖出数量：",number,\
                      " 收入资金：",number*open_price_today,"持股天数：",self.holdingStockStatus.days,"跌幅：",(self.holdingStockStatus.getCostPrice()-open_price_today)/open_price_today,\
                      ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
                if not self.holdingStockStatus.Sail(date, number, price):
                    return 0
                self.holdingStockStatus.geRouCount += 1
                return (number* price)            
            elif self.holdingStockStatus.coverNumber == 0 :               
                price = self.holdingStockStatus.getCostPrice() * config.KAIPAN_DELEGATESAIL_SCALE_0
            elif self.holdingStockStatus.coverNumber == 1 :
                price = self.holdingStockStatus.getCostPrice() * config.KAIPAN_DELEGATESAIL_SCALE_1
            elif self.holdingStockStatus.coverNumber == 2 :
                price = self.holdingStockStatus.getCostPrice() * config.KAIPAN_DELEGATESAIL_SCALE_2
            else : 
                price = self.holdingStockStatus.getCostPrice()   # 补过二次仓后 成本价卖出
                
            price =float('%03f'%price)  #开盘之后委托的卖单价格
            
            #委托卖单
            #print("kaiPanDelegate --->code:",self.code, ", date:",date,", number:", self.holdingStockStatus.number, ", price:", price,"------DELEGATE SAIL!")
            if price<open_price_today :
                               
                print("卖出----------------->日期:",date,",代码:",self.code,", 名称:", self.name ," 委托卖出价格:",price,\
                      " 实际卖出价格：",open_price_today," 卖出数量：",number,\
                      " 收入资金：",number*open_price_today,\
                      ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
                if not self.holdingStockStatus.Sail(date, number, open_price_today):
                    return 0
                return  (number*open_price_today)
            elif price<high_price_today :  
                print("卖出----------------->日期:",date,",代码:",self.code,", 名称:", self.name ," 委托卖出价格:",price,\
                      " 实际卖出价格：",price," 卖出数量：",number,\
                      " 收入资金：",number*price,\
                      ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
                if not self.holdingStockStatus.Sail(date, number, price):
                    return 0
                return (number* price)
            else:
                print("开盘的委托卖出， 今天无法卖出！ 日期:",date,",代码:",self.code,", 名称:", self.name ," 委托卖价:",price," 委托数量：",number,\
                      ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
                return 0
        return 0
    

    def panZhongBuCang(self, date):
        if not self.todayIsOK :
            return 
        self.panZhongBuCangFundIsEnough = False # 最终是否有钱可以进行盘中补仓， 由manager设置。
        self.panZhongBuCangPrice = float('%0.3f'%(self.holdingStockStatus.getCostPrice() * config.PANZHONG_BUCANG_SCALE_0)) # 盘中跌幅补入。
        self.panZhongBuCangNumber = 0
        if self.holdingStockStatus.number != 0 :      
            if self.panZhongBuCangPrice >  self.todayDataFrame['low'] :
                if self.holdingStockStatus.coverNumber == 0 :
                    print("name:",self.name, "盘中，第一次补仓--盘中")
                    self.panZhongBuCangNumber = self.holdingStockStatus.number                    
                    
                elif self.holdingStockStatus.coverNumber == 1 :     # 已经补过一次仓位了
                    print("name:",self.name, "盘中，已经补过一次仓位了, 进行第二次补仓--盘中")
                    self.panZhongBuCangNumber = int(self.holdingStockStatus.number/2)
                elif self.holdingStockStatus.coverNumber >= 2 :
                    print("name:",self.name, "盘中，已经至少二次补仓了--盘中不再补仓")
                    #self.panZhongBuCangNumber = int(self.holdingStockStatus.number/(self.holdingStockStatus.coverNumber+1))
                    return False            
                return True
        return False
    def panZhongJiaoYi(self, date):
        if not self.todayIsOK :
            return 
        if self.panZhongBuCangFundIsEnough :
            open_price_today = self.todayDataFrame['open']
            high_price_today = self.todayDataFrame['high']
            close_price_today = self.todayDataFrame['close']
            low_price_today = self.todayDataFrame['low']
            self.holdingStockStatus.coverNumber +=1  # 补仓次数加1
            print("盘中补仓----------------->日期:",date,",代码:",self.code,", 名称:", self.name ," 买入价格:",self.panZhongBuCangPrice," 买入数量",self.panZhongBuCangNumber,\
                  " 买入花费：",self.panZhongBuCangNumber*self.panZhongBuCangPrice, \
                  ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
            print("------------------------------------------------------------------------------------------------------------------------------------------昨日开盘价：",\
                  self.preDataFrame['open'],",最高价：",self.preDataFrame['high'],",最低价：",self.preDataFrame['low'],",收盘价：",self.preDataFrame['close'],"\n")
            self.holdingStockStatus.Buy(date, self.panZhongBuCangNumber, self.panZhongBuCangPrice)
    
    def computePreWeiPan(self, date):        

        self.needBuy = 0  #  0-不需要买入 1-需要补仓 2-根据得分判断是否买入
        self.approvalBuy = 0  # 0-未批准买入  1-批准买入
        if not self.todayIsOK :
            return 
        self.buyPrice = self.todayDataFrame['close']  # 买入价格    
        self.buCangNumber = 0  # 补仓需要的数量
        self.buyNumber = 0  # 如果needBuy=2 根据得分得到的买入数量  ，由manager设置

        if self.holdingStockStatus.number != 0 :  # 判断尾盘是否需要补仓                
            if self.buyPrice*config.WEIPAN_BUCANG_SCALE_0 < self.todayDataFrame['open'] and not self.panZhongBuCangFundIsEnough:   
                self.buCangPrice = self.todayDataFrame['close']            
                if self.holdingStockStatus.coverNumber == 0 :
                    print("name:",self.name, "第一次补仓--尾盘")
                    self.buCangNumber = self.holdingStockStatus.number
                    
                    self.needBuy = 1
                elif self.holdingStockStatus.coverNumber == 1 :     # 已经补过一次仓位了
                    print("name:",self.name, "已经补过一次仓位了, 进行第二次补仓--尾盘")
                    self.buCangNumber = int(self.holdingStockStatus.number/2)
                
                    self.needBuy = 1
                else :     
                    print("name:",self.name, "已经补过两次仓了 ，不需要再补了-尾盘")           
                    self.needBuy = 0
                
            else:
                print("name:",self.name, "今日跌幅不够2个点 ，或者盘中已经补过了，所以不补！")         
                #self.holdingStockStatus.delegate_Buy(date, number, close_price_today, False, True) 
        elif len(self.preDataFrame) != 0:                  
            self.score =  checkModel(self, date)
            if self.score != 0 :
                self.needBuy = 2


    def weiPanJiaoYi(self, date):
        if not self.todayIsOK :
            return 
        open_price_today = self.todayDataFrame['open']
        high_price_today = self.todayDataFrame['high']
        close_price_today = self.todayDataFrame['close']
        low_price_today = self.todayDataFrame['low']
        if self.approvalBuy == 1 and self.needBuy == 1 : # 批准补仓   
            self.holdingStockStatus.coverNumber +=1  # 补仓次数加1
            print("补仓----------------->日期:",date,",代码:",self.code,", 名称:", self.name ," 买入价格:",self.buyPrice," 买入数量",self.buCangNumber,\
                  " 买入花费：",self.buCangNumber*self.buyPrice, \
                  ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
            print("------------------------------------------------------------------------------------------------------------------------------------------昨日开盘价：",\
                  self.preDataFrame['open'],",最高价：",self.preDataFrame['high'],",最低价：",self.preDataFrame['low'],",收盘价：",self.preDataFrame['close'],"\n")
            self.holdingStockStatus.Buy(date, self.buCangNumber, self.buyPrice)
        elif self.approvalBuy == 1 and self.needBuy == 2 : # 批准买入
            print("买入----------------->日期:",date,",代码:",self.code,", 名称:", self.name ," 买入价格:",self.buyPrice," 买入数量",self.buyNumber,\
                  " 买入花费：",self.buyNumber*self.buyPrice, \
                  ",-------------------------------------------开盘价：",open_price_today,",最高价：",high_price_today,",最低价：",low_price_today,",收盘价：",close_price_today)
            print("------------------------------------------------------------------------------------------------------------------------------------------昨日开盘价：",\
              self.preDataFrame['open'],",最高价：",self.preDataFrame['high'],",最低价：",self.preDataFrame['low'],",收盘价：",self.preDataFrame['close'],"\n")
            
            self.holdingStockStatus.Buy(date, self.buyNumber, self.buyPrice)       
        