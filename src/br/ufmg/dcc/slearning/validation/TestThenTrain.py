'''
Created on Oct 26, 2012

@author: rloliveirajr
'''

from br.ufmg.dcc.slearning.util.Util import read_file, write_file
from br.ufmg.dcc.slearning.validation.Evaluate import Evaluate
from br.ufmg.dcc.slearning.util.timer import Timer
from br.ufmg.dcc.slearning.solves.IncrementalLac import IncrementalLac
from br.ufmg.dcc.slearning.solves.LacWpc import LacWpc
from br.ufmg.dcc.slearning.solves.LacWcpc import LacWcpc
from br.ufmg.dcc.slearning.solves.LacWpcRw import LacWpcRw
from br.ufmg.dcc.slearning.solves.ExtendedLacWcpc import ExtendedLacWcpc
from br.ufmg.dcc.slearning.solves.LacSlidingWindow import LacSlidingWindow
from br.ufmg.dcc.slearning.solves.SIGIR2011 import SIGIR2011
from br.ufmg.dcc.slearning.persistence.Transaction import Transaction


class TestThenTrain:
  
    class Classifiers:
        CLASSIFIER_INCREMENTAL_LAC = 1
        CLASSIFIER_LAC_WPC = 2
        CLASSIFIER_LAC_WCPC = 3
        CLASSIFIER_LAC_WPCRW = 4
        CLASSIFIER_EXTENDED_LAC_WCPC = 5
        CLASSIFIER_LAC_SLIDING_WINDOW = 6
        CLASSIFIER_SIGIR_2011 = 7
    '''
        Esta classe executa a avaliacao do metodo proposto utlizando o
        Interleaved Test-Then-Train
    '''
    def __init__(self, data, dataset, results, classifier_opt, params):
        self.nclasses = params["nclasses"]
        self.data = read_file(data)
        self.resource = params["resource"]
        self.temp_dir = params["tmp_dir"]
        self.classifier_opt = classifier_opt
        self.result_dir = results;
        self.classifier = None
        self.dataset = dataset
        self.params = params
        
    def _select_classifier(self):
        self.classifier_opt = int(self.classifier_opt)
        
        if self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_INCREMENTAL_LAC:
            self.classifier = IncrementalLac()
            
            return "IncrementalLac"
        
        elif self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_LAC_WPC:
            self.classifier = LacWpc()
            return "LacWpc"
        
        elif self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_LAC_WCPC:
            
            self.classifier = LacWcpc()
            return "LacWcpc"
        
        elif self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_LAC_WPCRW:
            self.classifier = LacWpcRw()
            return "LacWpcRw"
        
        elif self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_EXTENDED_LAC_WCPC:
            self.classifier = ExtendedLacWcpc()
            return "ExtendedLacWcpc"
        
        elif self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_LAC_SLIDING_WINDOW:
            self.classifier = LacSlidingWindow()
            return "LacSlidingWindow"
        
        elif self.classifier_opt == TestThenTrain.Classifiers.CLASSIFIER_SIGIR_2011:
            self.classifier = SIGIR2011()
            return "SIGIR2011"
        
        else:
            raise "Classifier not found."
        
    def run(self):
        
        #Extrai o conjunto de treino inicial
        seed_start = int(float(self.params["seed"]) * len(self.data))
        train_begin = 0
        train_end = train_begin + seed_start
        
        train_ex = self.data[train_begin:train_end]
        self.params["seed"] = train_ex
        
        #Utiliza os dados restantes como teste
        stream = self.data[train_end:len(self.data)]

        classifier = self._select_classifier()
        self.classifier.resetLearner()
        self.classifier.setParameters(self.params)
        
        print "Classifier choosen: {0}".format(classifier)
        
        time = []
        
        _eval = Evaluate(classifier)

        _file = "%sresult_%s_%s.csv" % (self.result_dir, classifier, self.dataset)
        
        
        write_file(_file, Evaluate.fields, "a")

        total = 2
        for stream_instance in stream:
                       
            stream_transaction = Transaction(total,stream_instance, 8)
            
            print "\rProcessing: %d/%d\r" % (total,len(stream_instance))
            
            timer = Timer()
            timer.start()
            probs = self.classifier.getVotesForInstance(stream_transaction)
            timer.end()
            time.append(timer.interval)
            
            self.classifier.trainingOnInstance(stream_transaction)
            print(probs)
            _max = max(probs)
            predicted_label = probs.index(_max)
            stream_transaction.update_label(predicted_label)

            processed = []
            processed.append(stream_transaction) 
            
            line = _eval.eval(self.classifier.window_1, self.classifier.window_2, processed, timer.interval)
            
            write_file(_file, line, "a")

            total += 1
