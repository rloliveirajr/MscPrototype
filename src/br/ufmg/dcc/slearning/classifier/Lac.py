import os
from dummy_thread import exit

class Lac:
        
    def __init__(self, nclasses, execPath, inputPath, confidence, support):
        self.nclasses = nclasses
        self.execPath = execPath
        self.inputPath = inputPath
        self.c = confidence
        self.s = support

    def run(self, strain, stest, ruleSize, transaction_test):
        cmd = '%s/lazy -i %s -t %s -m %d -e 500000 -s %f -a 0 -c %f > prediction' % (self.execPath, strain, stest, ruleSize, self.c, self.s)
        #print cmd
        os.system(cmd)
        prediction_file = open(self.inputPath + "prediction")

        final_probs = [[] for t in transaction_test.keys()]

        line_num = 0
        for line in prediction_file:
            prediction = line.split()
            
            probs = prediction[1:]
            prbs = {}
            for p in probs:
                prbs[p[0:8]] = p[8:]
            
            p = [0 for i in range(self.nclasses)]
            
            for label in range(self.nclasses):
                key = "prob[%d]=" % label
                if key in prbs.keys():
                    p[label] = float(prbs[key])
                    
            final_probs[line_num] = p
            
            line_num += 1
            
        return final_probs