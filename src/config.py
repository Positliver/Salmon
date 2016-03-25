'''
Created on 2015-7-11

@author: livepc
'''
#encoding=utf-8
import os

DownloadDataDir = os.path.join(os.path.dirname(__file__), 'stockdata/')  # os.path.pardir: 上级目录
DownloadCodeDir = os.path.join(os.path.dirname(__file__), 'stockcode/')
HS300_CodePath =os.path.join(DownloadCodeDir, 'HS300S.csv')
SZ50_CodePath =os.path.join(DownloadCodeDir, 'SZ50S.csv')
ZZ500_CodePath =os.path.join(DownloadCodeDir, 'ZZ500S.csv')

MAX_SELECT_STOCK_COUNT = 5 


MAXDISTANCE_DAYS = 7
PRE_PRE_pCHANGE_WETIGHT = 1 # 前二天的跌幅所占的权重
PRE_pCHANGE_WETIGHT = 1 #前一天的跌幅 所占的权重
CURRENT_pCHANGE_WETIGHT = 1 #今天跌幅 所占的权重
OCDistance_PREDATE_WETIGHT = 2 # 前一天价格差 所占的权重
OCDistance_CURRENTDATE_WETIGHT = 5 # 今天价格差 所占的权重


KAIPAN_DELEGATESAIL_SCALE_0 = 1.02  #没有补过仓的开盘卖价
KAIPAN_DELEGATESAIL_SCALE_1 = 1.01  #补过一次仓的卖价
KAIPAN_DELEGATESAIL_SCALE_2 = 1.00  #补过两次仓的卖价

PANZHONG_BUCANG_SCALE_0 = 0.92 # 盘中相对于今天开盘价的跌8个点 补仓。

WEIPAN_BUCANG_SCALE_0 = 1.02  # 尾盘时 计算是否可以补仓， 当跌幅超过2个点的时候，可以补仓

# KAIPAN_DELEGATEBUY_SCALE_1 = 0.92  #开盘没有卖出，基本判定需要补仓
# KAIPAN_DELEGATEBUY_SCALE_1 = 0.96  #第二次进行开盘没有卖出的补仓
GEROU_SCALE_0 = 0.95  # 触发割肉条件，成本价跌5个点。
MOST_DAYS_CHIGU = 5  # 触发割肉 超过5天必须持股天数


INITIAL_MONEY= 100000  # 初始资金
CHICANG_BILIE_EXCEPT_BUCANG = 0.8  # 持仓比例， 新买入股票时使用， 补仓不使用

DATE_START = '2013-01-01'
DATE_END = '2013-2-01'