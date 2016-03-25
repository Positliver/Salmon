'''
Created on Jul 9, 2015

@author: hanchunyu
'''
#encoding=utf-8

from enum import Enum
import os
import os.path
import pandas as pd
from pandas import Series, DataFrame
import lib.helper
import config
from stock import Stock
from stockPool import StockPool
from money import Fund

#STOCKTYPE = Enum('STOCKTYPE','HS300S SZ50S ZZ500S ALL')
   
def start():
    
    mystock = StockPool()  # 选股池
    myfund = Fund(config.INITIAL_MONEY)  # 初始资金
#     print('the count of HS300:',len(mystock.HS300S))
#     print('the count of SZ50:',len(mystock.SZ50S))    
#     print('the count of ZZ500:',len(mystock.ZZ500S))
    allstock = []
    allstock.extend(mystock.HS300S)
    allstock.extend(mystock.SZ50S)
    allstock.extend(mystock.ZZ500S)
    print('初始资金：',myfund.myCash, ' ,选股池数量:', len(allstock), ', 测试的起始时间和结束时间:', config.DATE_START, config.DATE_END )
    
    days = pd.period_range(config.DATE_START,config.DATE_END,freq='B')  # 测试的起始时间和结束时间
    
    for day in days :
        todaystock =  list(allstock)
        canBuyList = []
        print("-------------------------------------------------------------------------------------------------------------day:",day)
        
        # 初始化今天各个股票的情况
        for eachStock in todaystock :
            if not eachStock.startDay(day) :
                todaystock.remove(eachStock)
        print("今天可以交易的股票数目:",len(todaystock))  
#         for ts in todaystock:
#             print(", name:",ts.name, end="")

        # 开盘的交易
        for eachStock in todaystock :
            kaideMoney = eachStock.kaiPanJiaoYi(day)
            myfund.storeMoney(kaideMoney)         
    
        # 盘中补仓情况
        for  eachStock in todaystock :
            if eachStock.panZhongBuCang(day) and myfund.askForMoney(eachStock.panZhongBuCangNumber*eachStock.panZhongBuCangPrice):
                eachStock.panZhongBuCangFundIsEnough = True
                eachStock.panZhongJiaoYi(day)
            
        print("开盘交易后的资金余额：---------------->",myfund.myCash)
        for eachStock in todaystock :
            eachStock.computePreWeiPan(day) # 尾盘前各个股票的待买待卖情况
            if eachStock.needBuy == 1 :  # 补仓
                if myfund.askForMoney(eachStock.buCangNumber*eachStock.buyPrice):
                    eachStock.approvalBuy = 1
            if eachStock.needBuy == 2 : # 评分 买入
                canBuyList.append(eachStock)
                
        #统计目前持仓股市 和各个数量
        holdingNumber = []        
        for eachStock in allstock :            
            if eachStock.getHoldingNumber() !=0 :
                holdingNumber.append(eachStock.getHoldingNumber)
                

        howManyStockToBuy = len(canBuyList)
        howManyNeedBuy = config.MAX_SELECT_STOCK_COUNT - len(holdingNumber)
        print("根据得分今天可选的股票数量为",howManyStockToBuy,", 还需要再购买股票数量",howManyNeedBuy, "（不包括需要补仓的）,目前资金余额：",myfund.myCash)
        if howManyStockToBuy != 0 and howManyNeedBuy > 0:
            canBuyList.sort(key=lambda x:x.score, reverse=True)  # 根据得分先后，确定下单的股票 
            
            if howManyStockToBuy > howManyNeedBuy :
                canBuyList = canBuyList[:(howManyNeedBuy)]
            howManyStockToBuy = len(canBuyList)
           
#             for test in canBuyList:
#                 print(test.score,test.name)
            nowMyCash = myfund.myCash*config.CHICANG_BILIE_EXCEPT_BUCANG
            #print("nowMyCash:",nowMyCash,",howManyStockToBuy:",howManyStockToBuy,"==>nowMyCash // howManyStockToBuy:",nowMyCash // howManyStockToBuy)
            #averageMoneyForEachStock = int(nowMyCash // howManyStockToBuy)
            goumaiZiJin = [nowMyCash*0.4,nowMyCash*0.2,nowMyCash*0.2,nowMyCash*0.1,nowMyCash*0.1]
            
            print("目前可用资金：",nowMyCash,",一共有",howManyStockToBuy,"需要购买.")#,"平均每个股票资金：",averageMoneyForEachStock)
            # 开始下单购买       
            buy_iter = 0
            for buy in canBuyList :
                buy_price = buy.buyPrice
                keYongZiJin = goumaiZiJin[buy_iter]
                buy_iter +=1
                number = int(keYongZiJin// (buy_price*100)) # 可以购买多少手
                number = number*100
                if number < 100:
                    print("score:",buy.score,", 代码:",buy.code," 名称:",buy.name," 当前价格：",buy_price," 可购数量：",number,"数量太少无法购买！")
                elif  myfund.askForMoney(number*buy_price):
                    buy.approvalBuy = 1
                    buy.buyNumber = number# 尾盘前需要购买的数量
                    SurplusCash = myfund.myCash
                    print("score:",buy.score,", 代码:",buy.code," 名称:",buy.name," 当前价格：",buy_price," 购买数量：",number)
                    #print("score:",buy.score,", 代码:",buy.code," 名称:",buy.name," 当前价格：",buy_price," 可够数量：",number,", 花费:", str(buy_price*number)," 资金余额:",SurplusCash)
                else :
                    print("钱不够 ，无法购买！ 现在剩余：",myfund.myCash)
        
        
        # 尾盘交易并计算资金和股票情况  
        moneyInStock = 0
        for eachStock in todaystock :
            eachStock.weiPanJiaoYi(day)
        print("$$$")
        for eachStock in allstock :
            
            if eachStock.holdingStockStatus.number != 0 :
                #open_price_today = eachStock.pretodayDataFrame['open']
                #high_price_today = eachStock.pretodayDataFrame['high']
                close_price_today = eachStock.pretodayDataFrame['close']
                #low_price_today = eachStock.pretodayDataFrame['low']
                cost_price = eachStock.holdingStockStatus.getCostPrice()
                number =  eachStock.holdingStockStatus.number
                print("代码:",eachStock.code," 名称:",eachStock.name," 成本价格：",cost_price," 持仓数量：",number," 当前价格：",close_price_today,"持仓天数：", eachStock.holdingStockStatus.days)
                moneyInStock += number*close_price_today
                    
        print("$$$当前总资金：",myfund.myCash+moneyInStock, " 现金余额：",myfund.myCash," 当前股票市值：",moneyInStock,"\n\n")
    currentFund(allstock, myfund, config.DATE_END, moneyInStock)

def currentFund(allstock, myfund, day, moneyInStock):   
    result = 0
    for eachStock in allstock :
        
        if eachStock.holdingStockStatus.totalFund != 0 :
            close_price = eachStock.pretodayDataFrame['close']
            totalDays = eachStock.holdingStockStatus.getTotalDays(close_price)
            totalfund = eachStock.holdingStockStatus.totalFund
            stockfund = close_price*eachStock.holdingStockStatus.number
            print("code:", eachStock.code," name:", eachStock.name ,",总盈亏:", totalfund-stockfund,",割肉次数：",eachStock.holdingStockStatus.geRouCount)
            for day in totalDays:
                #print("day:",day)
                print("持仓天数:",day[0],",盈亏：",day[1])

#                   "总持仓天数：",eachStock.holdingStockStatus.getTotalDays(close_price)[0] \
#                   , "盈亏情况：",eachStock.holdingStockStatus.getTotalDays(close_price)[1])
            result += eachStock.holdingStockStatus.totalFund
        if eachStock.holdingStockStatus.number != 0 :
            result -= eachStock.holdingStockStatus.number*(eachStock.pretodayDataFrame['close'])

    print("##########################################################################################################") 
    print("The End, 现金:", myfund.myCash , ", 股票:", moneyInStock, ", 结余:", -result, ", 初始资金:",config.INITIAL_MONEY)
    print("##########################################################################################################") 
if __name__ == '__main__':
    start()
