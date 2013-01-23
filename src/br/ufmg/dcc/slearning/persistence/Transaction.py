'''
Created on Oct 29, 2012

@author: rloliveirajr
'''
from br.ufmg.dcc.slearning.utility.Skyline import SkylineBNL
from br.ufmg.dcc.slearning.classifier.LacFiltro import Rule, cmpf

class Transaction(object):
    '''
    classdocs
    '''

    def __init__(self, timestamp, instance, nmetrics):
        self.timestamp = timestamp
        self.instance = instance
        self.probs = None
        self.nmetrics = nmetrics
        self.rules = {}
        
        self.__extract_fields()
        self.predicted = self.label 
        
    def addRule(self, idMetric, prule):
        tmp = prule.split(':')
        value = float(tmp[1])
        rule = tmp[0]
        
        if not rule  in self.rules:
            self.rules[rule] = Rule(self.nmetrics, rule)
        self.rules[rule].addValue(idMetric, value)
    
    def calcProbs(self, nclasses, idMetric):
        return self.__calcProbs(nclasses, idMetric, self.rules)
    
    def calcParetoProbs(self, nclasses, idMetric):
        skyline = SkylineBNL()
        
        for r in self.rules:
            skyline.addPoint(self.rules[r])
        
        predicted, probs, nrules = self.__calcProbs(nclasses, 1, skyline.window)
        
        return predicted, probs, nrules
    
    def calcParetoProbs2D(self, nclasses, idMetric):
        skyline = SkylineBNL()
        for r in self.rules:
            #skyline.addPoint(self.rules[r])
            #GAMBIARRA PARA fazer 2d
            r2 = Rule(2, self.rules[r].rule)
            r2.values[0] = self.rules[r].values[0] #confidence
            r2.values[1] = self.rules[r].values[idMetric]
            skyline.addPoint(r2)
        
        #print len(self.rules), len(skyline.window)
        
        #return self.__calcProbs(nclasses, idMetric, skyline.window)
        return self.__calcProbs(nclasses, 1, skyline.window)
    
    def __calcProbs(self, nclasses, idMetric, rules):
#            print rules
        probs = [0 for i in range(nclasses)]
        total = 0.0
        for r in rules:
            v =  rules[r].values[idMetric]
            probs[rules[r].idClass] += v
            total += v
            
        if cmpf(total, 0.0) < 0:
            total = abs(total)
            
        maxV = -1e38
        predicted = 0
        
        for i in range(len(probs)):
            if cmpf(probs[i], maxV) > 0:
                maxV = probs[i]
                predicted = i
            if cmpf(total, 0.0) != 0:
                probs[i] /= total
                
        return predicted, probs, len(rules)
    
    def update_label(self, predicted):
        self.predicted = predicted
        
#        old_label = "CLASS={0}".format(self.label)
#        new_label = "CLASS={0}".format(label)
#        updated_instance = self.instance.replace(old_label, new_label)
#        
#        self.or_instance = self.instance
#        self.instance = updated_instance
        
    def __extract_fields(self):
        splited_instance = self.instance.split()
        
        self.tid = splited_instance[0]
        self.label = int(splited_instance[1].replace("CLASS=",""))
        self.fields = [field for field in splited_instance[2:len(splited_instance)]]        
    
        