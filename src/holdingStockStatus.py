'''
Created on 2015-7-12

@author: livepc
'''


class orderRecord(object):
    def __init__(self, date , number, price, isBuy, isKaipan, isWeipan):
        self.date = date # 时间
        self.number = number # 交易的数量
        self.price = price # 交易的价格
        self.isBuy = isBuy  # 0-buy; 1-sail
        self.isKaipan = isKaipan # 是否是开盘交易
        self.isWeipan = isWeipan # 是否是尾盘交易
        
        
class holdingStockStatus(object):

    def __init__(self, code, name, number, totalFund):
        self.code = code
        self.name = name
        self.totalFund = totalFund # 该股的总资金
        
        self.number = number # 持仓数目
        self.costPrice = 0 # 持仓成本价
        self.days = 0 #持仓天数
        self.__totalDays = [] # 总持仓天数
                
        self.coverNumber = 0  # 补仓次数
        self.geRouCount = 0 # 统计割肉次数
        self.totalHistoryKnockdown = [] # 总成交的记录

        
    def startDay(self):        
        # 清空今天的列表
        #self.todayDelegateList = [] # 今天委托买单的记录
        if self.days != 0 :
            self.days +=1
        return True
                
    def Buy(self, date, number, price): # 买number数量的股票， 价格为price
        if self.number !=0 :
            self.costPrice = ((self.number*self.costPrice) +(number*price))/(self.number+number)
        else :
            self.costPrice = price
            self.days = 1
        self.number +=number
        self.totalFund += number*price
        self.totalHistoryKnockdown.append({date, number,price,True})
        #print("买入，已成交的交易--->日期:",date,",代码:",self.code,", 名称:", self.name ,"-->数量:",number,",价格:",price,"--------------------------------------买入!")
        
    def __hasQingCang(self, yingKui_status):
        self.costPrice = 0
        self.__totalDays.append([self.days,yingKui_status])
        self.days = 0
        self.coverNumber = 0
        
    def Sail(self, date, number, price): # 卖number数量的股票， 价格为price
        if number > self.number or self.number <=0 or number<0:
            return False
        yingKui = (self.costPrice - price)*number
        self.number -=number
        self.totalFund -=number*price
        # print("卖出，已成交的交易--->日期:",date,",代码:",self.code,", 名称:", self.name ,"-->数量:",number,",价格:",price,"------------------------------------------卖出!")
        if self.number == 0 :  # 已经清仓 
            self.__hasQingCang(yingKui)
        else :      
            self.costPrice = (self.number*self.costPrice - number* price)/(self.number-number)  
        self.totalHistoryKnockdown.append({date, number,price,False})
        return True
        
    def getInvoicePrice(self): # 该股持仓的成本价
        if self.number == 0 :
            return 0
        return float('%0.3f'%(self.totalFund/self.number))
    
    def getCostPrice(self):
        return float('%0.3f'%self.costPrice)
    
    def getTotalDays(self, price):
        if self.days != 0:
            yingKui = (self.costPrice - price)*self.number
            self.__totalDays.append([self.days, yingKui])
        return self.__totalDays
    