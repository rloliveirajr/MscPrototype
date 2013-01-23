'''
Created on Jan 21, 2013

@author: rloliveirajr
'''
from br.ufmg.dcc.slearning.persistence.Transaction import Transaction
from br.ufmg.dcc.slearning.util.Util import write_file
from br.ufmg.dcc.slearning.classifier.LacFiltro import LacFiltro
from br.ufmg.dcc.slearning.utility.Skyline import SkylineBNL

class LacWcpc(object):

    def resetLearner(self):
        self.window_1 = []
        self.window_2 = []
        self.train_instances = []
        self.resource = "/tmp"
        self.tmp_dir = "/tmp"
        self.nclasses = 2
        self.rules_size = 3
        self.test_file = "/tmp/lacWcpc_test.lac"
        self.train_file_1 = "/tmp/lacWcpc_train_1.lac"
        self.train_file_2 = "/tmp/lacWcpc_train_2.lac"
        
    def setParameters(self, params):
        self.window_1 = [Transaction(1, i, 8) for i in params["seed"]]
        self.window_2 = []
        
        self.resource = params["resource"]
        self.nclasses = int(params["nclasses"])
        self.rules_size = int(params["rules_size"])
        
        tmp_dir = params["tmp_dir"]
        self.test_file = "%s/data/roberto_test.lac" % (tmp_dir)
        self.train_file_1 = "%s/data/lacWcpc_train_1.lac" % (tmp_dir)
        self.train_file_2 = "%s/data/lacWcpc_train_2.lac" % (tmp_dir)
        
    def trainingOnInstance(self, stream_transaction):
        self.window_1.append(stream_transaction)
    
    def getVotesForInstance(self, stream_transaction):
        
        #Instancias de treino a serem escritas no arquivo de treino
        instances_window_1 = [t_transaction.instance for t_transaction in self.window_1]
        instances_window_2 = [t_transaction.instance for t_transaction in self.window_2]
        
        #Cria os arquivos de treino e test
        write_file(self.test_file, stream_transaction.instance)
        write_file(self.train_file_1, instances_window_1)
        write_file(self.train_file_2, instances_window_2)
        
        #Executa o LAC
        transactions = {}
        transactions[stream_transaction.tid] = stream_transaction
        
        #Executa o LAC Window 1
        lac = LacFiltro(self.nclasses, self.resource, "./", LacFiltro.FilterOption.PARETO_FILTER)
        result_window_1 = lac.run(self.train_file_1, self.test_file, self.rules_size, transactions)
        
        #Executa o LAC Window 2
        lac = LacFiltro(self.nclasses, self.resource, "./", LacFiltro.FilterOption.PARETO_FILTER)
        result_window_2 = lac.run(self.train_file_2, self.test_file, self.rules_size, transactions)
        
        removed = self._utility(test=stream_transaction, train=self.window_1)
        self._utility(test=stream_transaction, train=self.window_2)
        self.window_2 += removed
        
        result = self._calc_ensemble_prob(result_window_1, result_window_2)
        
        return result
    
    def _calc_ensemble_prob(self, result_w_1, result_w_2):
        beta = 0.5
        
        probs = [0 for i in range(self.nclasses)]
        
        for i in range(self.nclasses) :
            if (result_w_1[0][0].probs[i] + result_w_2[0][0].probs[i]) > 0:
                probs[i] = (1 + beta * beta) * ((result_w_1[0][0].probs[i] * result_w_2[0][0].probs[i]) / ((beta * beta)*result_w_1[0][0].probs[i] + result_w_2[0][0].probs[i]))

        return probs
    
    def _utility(self, test, train):
        skyline = SkylineBNL()
        
        rules = test.rules
        
        for r in rules:
            skyline.addPoint(rules[r])
        
        self.rank = dict((t.tid,{"transaction":t, "window": 0, "subdued": 0}) for t in train)

        for w in skyline.window:
            self._rule_cover(rule=w, pareto_set="window", train=train)
        
        removed = []
        for t in self.rank.itervalues():
            if t["window"] == 0:
                index = train.index(t["transaction"])
                removed.append(train[index])
                del train[index]
                
        return removed
                
    def _rule_cover(self, rule, pareto_set, train):
        clauses = rule.split(",")
        
        clauses = clauses[0:len(clauses)]
        
        set_features = set(clauses)
                
        for t in train:
            t_features = list(t.fields)
            t_features.append(str(t.label))
            
            set_t_features = set(t_features)
            
            intersect = list(set_features & set_t_features)
            
            if len(intersect) == len(clauses):
                self.rank[t.tid][pareto_set] += 1
        