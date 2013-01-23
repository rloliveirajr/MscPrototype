'''
Created on Oct 29, 2012

@author: rloliveirajr
'''
import numpy as np

class Rule:
    def __init__(self, nmetrics, rule):
        self.values = np.zeros(nmetrics)
        self.rule =  rule
        self.idClass =  int(rule[-1])
        
    def  __repr__(self):
        return self.rule + ' ' + str(self.values)
        
    def addValue(self, idMetric, value):
        self.values[idMetric] = value
    
    def len(self):
        return len(self.values)
    
    def value(self, i):
        return self.values[i]