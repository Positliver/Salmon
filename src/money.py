'''
Created on 2015-7-12

@author: livepc
'''

import config


class Fund(object):
    def __init__(self, initial_money):
        self.myCash = initial_money
    def askForMoney(self,apply_money):
        if apply_money > self.myCash :
            return False
        else:
            self.myCash -=apply_money
            return True
    def storeMoney(self, store_money):
        self.myCash +=store_money
        return self.myCash

    