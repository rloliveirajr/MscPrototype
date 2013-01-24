'''
Created on Jan 21, 2013

@author: rloliveirajr
'''
from br.ufmg.dcc.slearning.persistence.Transaction import Transaction
from br.ufmg.dcc.slearning.util.Util import write_file
from br.ufmg.dcc.slearning.classifier.Lac import Lac
import operator

class LacSlidingWindow(object):
    
    def resetLearner(self):
        self.timestamp = 1
        self.window_1 = []
        self.window_2 = []
        self.window_size = 1

        self.sub_judice = {}
        self.nclasses = -1
        self.resource = "/tmp/"
        
        self.is_fixed = True
        self.size = 1
        
        self.score_max = 0.1
        
        self.rule_size = 3
        self.confidence = 0.1
        self.support = 0.1
        
        self.train_file = "/tmp/lacSlidingWindow_test.lac"
        self.test_file = "/tmp/lacSlidingWindow_train.lac"
    
    def setParameters(self, params):
        self.timestamp = 1
        self.window_1 = [Transaction(self.timestamp, i, 0) for i in params["seed"]]
        
        self.window_2 = []
        
        self.window_size = int(params["window_size"])
        self.resource = params["resource"]
        self.nclasses = int(params["nclasses"])
        
        self.rules_size = int(params["rules_size"])
        self.confidence = float(params["confidence"])
        self.support = float(params["support"])
        
        self.is_fixed = params["is_fixed"]
        self.score_max = float(params["score_max"])
        
        tmp_dir = params["tmp_dir"]
        self.test_file = "%s/lacSlidingWindow_test.lac" % (tmp_dir)
        self.train_file = "%s/lacSlidingWindow_train.lac" % (tmp_dir)
        
    def trainingOnInstance(self, stream_transaction):
        self.timestamp += 1
        stream_transaction.timestamp = self.timestamp
        ranking = self._rank(stream_transaction)

        if self.is_fixed == "True":
            if len(self.window_1) > self.window_size:
                tid = ranking.keys()[0]
                for i in range(len(self.window_1)):
                    if(self.window_1[i].tid == tid):
                        del self.window_1[i]
                        break
        else:          
            window = [t for t in self.window_1 if ranking[t.tid]["value"] < self.score_max]
            if len(window) == 0:
                print "fudeu"
                
            self.window_1 = window
             
        self.window_1.append(stream_transaction)
        
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
        
        return probs
    
    def _rank(self,stream_transaction):
        rank  = {}
        features_stream_instance = set(list(stream_transaction.fields))
        for transaction in self.window_1:
            features = set(list(transaction.fields))
            
            s = float(len((features & features_stream_instance))) / float(len((features | features_stream_instance)))
            
            m = 1 - (float(transaction.timestamp)/float(stream_transaction.timestamp))
            
            rank[transaction.tid] = (s + m) / 2.0
            
        
        rank_sorted = sorted(rank.iteritems(), key=operator.itemgetter(1))
        rank_sorted.reverse()
        ranking = dict((r[0],{"value":r[1]}) for r in rank_sorted)

        return ranking
        