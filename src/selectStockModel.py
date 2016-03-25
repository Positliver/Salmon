'''
Created on 2015-7-12

@author: livepc
'''
import datetime
import math

import config

def distanceOfTwoDay(date1, date2):
    listdate1 = str(date1).split('-')
    listdate2 = str(date2).split('-')
    d1 = datetime.datetime(int(listdate1[0]), int(listdate1[1]), int(listdate1[2]))
    d2 = datetime.datetime(int(listdate2[0]), int(listdate2[1]), int(listdate2[2]))
    return (d1 - d2).days


def computeScore(prepreChange, prePChange, currentPChange):
    #OCDistance_preDate = preOpen - preClose
    #OCDistance_currentDate = currentOpen - currentClose
    score = math.fabs(prepreChange*100)*config.PRE_PRE_pCHANGE_WETIGHT+ math.fabs(prePChange*100)*config.PRE_pCHANGE_WETIGHT + math.fabs(currentPChange*100)*config.CURRENT_pCHANGE_WETIGHT
    #+ OCDistance_preDate*config.OCDistance_PREDATE_WETIGHT +OCDistance_currentDate*config.OCDistance_CURRENTDATE_WETIGHT
    return float('%0.3f'%score)

def getTodayDateFrame(stock_k_data, day):
    indexlist = list(stock_k_data.index)
    if not len(stock_k_data) ==0 and str(day) in indexlist :
        return stock_k_data.loc[str(day)]
    else :
        return []

    
def getPreDateFrame(stock_k_data, day, length):
    indexlist = list(stock_k_data.index)
    if not len(stock_k_data) ==0 and str(day) in indexlist :
        currentPositionIndex = indexlist.index(str(day))
        if currentPositionIndex <= length :
            return []
        preDate_df = stock_k_data.iloc[int(currentPositionIndex)-length]
        #preDate = preDate_df.name            
        return preDate_df
    else :
        return []    
def jiSuanDieFu(open_price, close_price):
    
    openPrice = float('%0.3f'%open_price)
    closePrice = float('%0.3f'%close_price)
    return float('%0.3f'%((closePrice-openPrice)/openPrice))

def jiSuanShangYingXian(open_price, close_price, high_price, low_price, isDieFu):
    if isDieFu:
        return float('%0.3f'%((high_price - open_price)/open_price))
    else :
        return float('%0.3f'%((high_price - close_price)/open_price))
    
def jiSuanXiaYingXian(open_price, close_price, high_price, low_price, isDieFu):
    if isDieFu:
        return float('%0.3f'%((close_price-low_price)/open_price))
    else :
        return float('%0.3f'%((open_price - low_price)/open_price))

def checkModel (stock, day):
    stock_k_data = stock.stock_k_data
    name = stock.name
    #print(preDate_df)
    prepreDate_df = getPreDateFrame(stock_k_data, day, 2)  #前天的数据
    preDate_df = getPreDateFrame(stock_k_data, day, 1) # 昨天的数据
    currentDate_df = getTodayDateFrame(stock_k_data, day) # 今天的数据
    if len(prepreDate_df)==0 or len(preDate_df)==0 or len(currentDate_df)== 0 :
        return int(0)
    prepreOpen = float(prepreDate_df['open'])
    prepreClose = float(prepreDate_df['close'])
    #preprePChange = float(prepreDate_df['p_change'])
    prepreHigh = float(prepreDate_df['high'])
    prepreLow = float(prepreDate_df['low'])   
    prepreDieFu = jiSuanDieFu(prepreOpen, prepreClose)
    if prepreDieFu < 0 :
        prepreShangYingXian = jiSuanShangYingXian(prepreOpen, prepreClose, prepreHigh, prepreLow, True)
        prepreXiaYingXian = jiSuanXiaYingXian(prepreOpen, prepreClose, prepreHigh, prepreLow, True)
    else:
        prepreShangYingXian = jiSuanShangYingXian(prepreOpen, prepreClose, prepreHigh, prepreLow, False)
        prepreXiaYingXian = jiSuanXiaYingXian(prepreOpen, prepreClose, prepreHigh, prepreLow, False)
    
    preOpen = float(preDate_df['open'])
    preClose = float(preDate_df['close'])
    #prePChange = float(preDate_df['p_change'])
    preHigh = float(preDate_df['high'])
    preLow = float(preDate_df['low'])    
    preDieFu = jiSuanDieFu(preOpen, preClose)
    if preDieFu < 0 :
        preShangYingXian = jiSuanShangYingXian(preOpen, preClose, preHigh, preLow, True)
        preXiaYingXian = jiSuanXiaYingXian(preOpen, preClose, preHigh, preLow, True)
    else:
        preShangYingXian = jiSuanShangYingXian(preOpen, preClose, preHigh, preLow, False)
        preXiaYingXian = jiSuanXiaYingXian(preOpen, preClose, preHigh, preLow, False)
    
    currentOpen = float(currentDate_df['open'])
    currentClose = float(currentDate_df['close'])
    #currentPChange = float(currentDate_df['p_change'])
    currentHigh = float(currentDate_df['high'])
    currentLow = float(currentDate_df['low'])
    currentDieFu = jiSuanDieFu(currentOpen, currentClose)
    if preDieFu < 0 :
        currentShangYingXian = jiSuanShangYingXian(currentOpen, currentClose, currentHigh, currentLow, True)
        currentXiaYingXian = jiSuanXiaYingXian(currentOpen, currentClose, currentHigh, currentLow, True)
    else:
        currentShangYingXian = jiSuanShangYingXian(currentOpen, currentClose, currentHigh, currentLow, False)
        currentXiaYingXian = jiSuanXiaYingXian(currentOpen, currentClose, currentHigh, currentLow, False)
    # 一阴配两阳
    #if preprePChange <0 and prePChange> 0 and currentPChange>0 and currentPChange>prePChange and currentClose> prepreOpen:
    # 三连跌  
    if prepreDieFu<0 and preDieFu>0 and currentDieFu>0 and currentOpen> preOpen: 
    #and currentClose<preClose and preOpen<prepreClose and currentXiaYingXian>= currentShangYingXian and preXiaYingXian<= preShangYingXian:
        #print("preOpen:",preOpen,",preClose:",preClose,"currentOpen:",currentOpen,"currentClose:",currentClose)
        
        score = computeScore(prepreDieFu, preDieFu, currentDieFu)
        print("score:",score,",name:",name,",day:",day,",prepreDieFu:",prepreDieFu,",preDieFu:",preDieFu,",currentDieFu:",currentDieFu)
#         print("code:",code,",name:",name,"preOpen:",preOpen,",preClose:",preClose,",prePChange:",prePChange,\
#           ",currentOpen:",currentOpen,",currentClose:",currentClose,",currentPChange:",currentPChange,\
#           "------------------------------------------------------->score:",score)   
        return score
#     print("code:",code,",preOpen:",preOpen,",preClose:",preClose,",prePChange:",prePChange,\
#           ",currentOpen:",currentOpen,",currentClose:",currentClose,",currentPChange:",currentPChange,\
#           "------------------------------------------------------->score:",0)   
    return int(0)