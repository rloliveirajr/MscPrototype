import os

def cmpf(a, b, EPS = 1e-15):
    if a > b - EPS:
        if b > a - EPS:
            return 0
        else:
            return 1
    return -1

class Rule:
        def __init__(self, nmetrics, rule):
            self.values = [0 for i in range(nmetrics)]
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

class Result:
    def __init__(self):
        self.p = 0
        self.n = 0
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0
        
        self.nrules = 0
        self.ntransactions = 0
        
        self.probs = 0
        self.predicted = None
        
        self.window = None
        self.subdued = None
    
    def  __repr__(self):
        return "Predicted: " + str(self.predicted) + " Probs: " + str(self.probs) + " Accuracy: " + str(self.accuracy()) + " Recall: " + str(self.recall()) + " Precision: " + str(self.precision()) + " Nrules: " + str(self.nrules/float(self.ntransactions))
    
    def addResult(self, real, predicted, nrules, probs):
        self.nrules += nrules
        self.ntransactions += 1
        self.predicted = predicted
        self.probs = probs

        if real == 0:
            self.n += 1
            if real == predicted:
                self.tn += 1
            else:
                self.fn += 1
        else:
            self.p += 1
            if real == predicted:
                self.tp += 1
            else:
                self.fp += 1
    
    def precision(self):
        if self.tp + self.fp == 0:
            return 1.0
        return float(self.tp)/float(self.tp + self.fp)
    
    def recall(self):
        if (self.tp + self.fn) == 0:
            return 1.0
        return float(self.tp)/float(self.tp + self.fn)
    
    def accuracy(self):
        if self.p + self.n == 0:
            return 1.0
        return float(self.tp + self.tn)/float(self.p + self.n)
    
    def meanRuleNumber(self):
        if self.ntransactions == 0:
            return 0
        return float(self.nrules)/float(self.ntransactions)

class LacFiltro:
    class FilterOption:
        NONE = 0
        PARETO_FILTER = 1
        
    def __init__(self, nclasses, execPath, inputPath, filterOption):
        self.nclasses = nclasses
        self.execPath = execPath
        self.inputPath = inputPath
        self.filterOption = filterOption
        self.metrics = ["confidence",
                        "support",
                        "addedValue",
                        "certainty",
                        "yulesQ",
                        "yulesY",
                        "strengthScore",
                        "weightedRelativeConfidence"]

    def run(self, strain, stest, ruleSize, transaction_test):
        cmd = '%s/lazy_filtro -i %s -t %s -m %d -e 500000 -s 1 -a 0 > out' % (self.execPath, strain, stest, ruleSize)
        #print cmd
        os.system(cmd)
        return self.__avgPredict(self.inputPath, transaction_test)
    
    def __avgPredict(self, path, transactions):
#        print 'predicting...'
        results = [(Result(), s) for s in self.metrics]
        files = []
        for m in self.metrics:
            files.append(open(path + m))
        
        mustRun = True
        
        while mustRun:
            for idMetric in range(len(files)):
                line = files[idMetric].readline()
                if not line:
                    mustRun = False
                    break
                fields = line.split()
                #print self.metrics[idMetric]
                tid = fields[-1]
                classId = int(fields[-2])
                
                transaction = transactions[tid]
                
                for j in range(len(fields)-2):
                    transaction.addRule(idMetric, fields[j])
            if mustRun == False:
                break  
            
            for idMetric in range(len(files)):
                if self.filterOption == LacFiltro.FilterOption.PARETO_FILTER:
                    predited, probs, nrules = transaction.calcParetoProbs(self.nclasses, idMetric)
                    
                    results[idMetric][0].addResult(classId, predited, nrules, probs)
#                    print tid, idMetric, nrules
                else:
                    predited, probs, nrules = transaction.calcProbs(self.nclasses, idMetric)
                    results[idMetric][0].addResult(classId, predited, nrules, probs)
                #print tid, predited, probs
            
        return results
        

    
def main():
    path = '/mnt/hd0/itamar/Dropbox/lac/'
    strain = '/mnt/hd0/itamar/Dropbox/lac/trainning.txt'
    stest = '/mnt/hd0/itamar/Dropbox/lac/t'
    lac = LacFiltro(2, path, './', LacFiltro.FilterOption.PARETO_FILTER)
    results = lac.run(strain, stest, 3)
    for r in results:
        print r
    
if __name__ == "__main__":
    main();