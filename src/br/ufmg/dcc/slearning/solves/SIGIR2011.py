'''
Created on Jan 21, 2013

@author: rloliveirajr
'''
from br.ufmg.dcc.slearning.persistence.Transaction import Transaction
from br.ufmg.dcc.slearning.util.Util import write_file
from br.ufmg.dcc.slearning.classifier.Lac import Lac

class SIGIR2011(object):
    
    def resetLearner(self):
        self.window_1 = []
        self.window_2 = []
        self.sub_judice = {}
        self.nclasses = 2
        self.resource = ""
        
        self.rule_size = 3
        self.confidence = 0.1
        self.support = 0.1
        
        self.train_file = "/tmp/sigir2011_train.lac"
        self.test_file = "/tmp/sigir2011_test.lac"
    
    def setParameters(self, params):
        self.window_1 = [Transaction(1, i, 0) for i in params["seed"]]
        self.window_2 = []
        self.resource = params["resource"]
        self.nclasses = int(params["nclasses"])
        
        self.rules_size = int(params["rules_size"])
        self.confidence = float(params["confidence"])
        self.support = float(params["support"])
        
        self.confidence_min = float(params["min_confidence"])
        self.max_timestamp = float(params["max_timestamp"])
        
        tmp_dir = params["tmp_dir"]
        self.test_file = "%s/data/sigir2011_test.lac" % (tmp_dir)
        self.train_file = "%s/data/sigir2011_train.lac" % (tmp_dir)
        
    def trainingOnInstance(self, stream_transaction):

        if not stream_transaction.tid in self.sub_judice.keys():
            self.window_1.append(stream_transaction)
        
        for tid in self.sub_judice.keys():
            transaction = self.sub_judice[tid]["transaction"]
            timestamp = self.sub_judice[tid]["timestamp"]
            
            if timestamp >= self.max_timestamp:
                del self.sub_judice[tid]
            else:
                self.getVotesForInstance(transaction)
        
    def getVotesForInstance(self, stream_transaction):
        
        train_instances = [t_transaction.instance for t_transaction in self.window_1]
        
        #Cria os arquivos de treino e test
        write_file(self.test_file, stream_transaction.instance)
        write_file(self.train_file, train_instances)
        
        #Executa o LAC
        transactions = {}
        transactions[stream_transaction.tid] = stream_transaction
        
        lac = Lac(self.nclasses, self.resource, "./", self.confidence, self.support)
        result = lac.run(self.train_file, self.test_file, self.rules_size, transactions)
        
        probs = result[0]
        
        self._sub_judice(probs, stream_transaction)
        
        return probs
    
    def _sub_judice(self, probs, transaction):
        max_probs = max(probs) 
        if max_probs < self.confidence_min:
            if transaction.tid in self.sub_judice.keys():
                self.sub_judice[transaction.tid]["timestamp"] += 1
            else:                   
                self.sub_judice[transaction.tid] = {"transaction":transaction,"timestamp":0}
        else:
            if transaction.tid in self.sub_judice.keys():
                del self.sub_judice[transaction.tid]
            self.window_1.append(transaction)
    
