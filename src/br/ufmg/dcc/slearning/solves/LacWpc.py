'''
Created on Jan 21, 2013

@author: rloliveirajr
'''
from br.ufmg.dcc.slearning.persistence.Transaction import Transaction
from br.ufmg.dcc.slearning.util.Util import write_file
from br.ufmg.dcc.slearning.classifier.LacFiltro import LacFiltro
from br.ufmg.dcc.slearning.utility.Skyline import SkylineBNL

class LacWpc(object):

    def resetLearner(self):
        self.window_1 = []
        self.window_2 = []
        self.train_instances = []
        self.resource = "/tmp"
        self.tmp_dir = "/tmp"
        self.nclasses = 2
        self.rules_size = 3
        self.test_file = "/tmp/lacWpc_test.lac"
        self.train_file = "/tmp/lacWpc_train.lac"
    
    def setParameters(self, params):
        self.window_1 = [Transaction(1, i, 8) for i in params["seed"]]
        self.window_2 = []
        self.resource = params["resource"]
        self.nclasses = int(params["nclasses"])
        self.rules_size = int(params["rules_size"])
        
        tmp_dir = params["tmp_dir"]
        self.test_file = "%s/lacWpc_test.lac" % (tmp_dir)
        self.train_file = "%s/lacWpc_train.lac" % (tmp_dir)
        
    def trainingOnInstance(self, stream_transaction):
        self.window_1.append(stream_transaction)
    
    def getVotesForInstance(self, stream_transaction):
        
        #Instancias de treino a serem escritas no arquivo de treino
        train_instances = [t_transaction.instance for t_transaction in self.window_1]
        
        #Cria os arquivos de treino e test
        write_file(self.test_file, stream_transaction.instance)
        write_file(self.train_file, train_instances)
    
        #Executa o LAC
        transactions = {}
        transactions[stream_transaction.tid] = stream_transaction
        
        lac = LacFiltro(self.nclasses, self.resource, "./", LacFiltro.FilterOption.PARETO_FILTER)
        result = lac.run(self.train_file, self.test_file, self.rules_size, transactions)
        
        self._utility(test=stream_transaction, train=self.window_1)
        
        probs = self._calc_prob(result)
        
        return probs
    def _calc_prob(self, result):
        
        probs = [0 for i in range(self.nclasses)]
        
        for i in range(self.nclasses) :
            if (result[0][0].probs[i]) > 0:
                probs[i] = result[0][0].probs[i]

        return probs
    
    def _utility(self, test, train):
        skyline = SkylineBNL()
        
        rules = test.rules
        
        for r in rules:
            skyline.addPoint(rules[r])
        
        self.rank = dict((t.tid,{"transaction":t, "window": 0, "subdued": 0}) for t in train)

        for w in skyline.window:
            self._rule_cover(rule=w, pareto_set="window", train=train)

        for t in self.rank.itervalues():
            if t["window"] == 0:
                index = train.index(t["transaction"])
                del train[index]
                
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
        