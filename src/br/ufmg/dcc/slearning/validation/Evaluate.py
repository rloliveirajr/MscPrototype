'''
Created on Nov 7, 2012

@author: rloliveirajr
'''
from copy import copy

class Evaluate:
    
    fields = "total,hits_total,hits_zero,hists_one,misses_total,misses_zero,misses_one,mse_global,mse_zero,mse_one,window_1_size,window_1_zero,window_1_one,window_2_size,window_2_zero,window_2_one,time_interval\n"
    
    def __init__(self, approach):
        self.window_1_size_hist = []
        self.window_1_one_hist = []
        self.window_1_zero_hist = []
        
        self.window_2_size_hist = []
        self.window_2_one_hist = []
        self.window_2_zero_hist = []
        
        self.approach = approach
        self.hits_total = 0
        self.misses_total = 0
        
        self.dict_model_eval_per_class = {0:0, 1:0}
        
        self.hits_per_class_hist = []
        self.misses_per_class_hist = []
        
        self.hits_per_class = {0:0, 1:0}
        self.misses_per_class = {0:0, 1:0}
        
        self.total = 0
    
    def add_hit(self,label):
        self.hits_per_class[label] += 1
        
        eval_per_class = copy(self.dict_model_eval_per_class)
        eval_per_class[label] += 1
        self.hits_per_class_hist.append(eval_per_class)
        
        self.hits_total += 1
        self.total += 1
    
    def add_miss(self, label):
        self.misses_per_class[label] += 1
        
        eval_per_class = copy(self.dict_model_eval_per_class)
        eval_per_class[label] += 1
        self.misses_per_class_hist.append(eval_per_class)
        
        self.misses_total += 1
        self.total += 1
        
    def mse(self):
        mse_global = self.misses_total/float(self.total)
        
        mse_zero = self.misses_per_class[0]/float(self.total)
        
        mse_one = self.misses_per_class[1]/float(self.total)
        
        return mse_global, mse_zero, mse_one
    
    def acc(self):
        acc_global = self.hits_total/float(self.total)
        
        acc_zero = self.hits_per_class[0]/float(self.total)
        
        acc_one = self.hits_per_class[1]/float(self.total)
        
        return acc_global, acc_zero, acc_one
    
    def calc_evaluate(self, processed):   
        for p in processed:
            if p.predicted == p.label:
                self.add_hit(p.label)
            else:
                self.add_miss(p.label)
                
    def train_stat(self, window_1, window_2):
        self.window_1_size_hist.append(len(window_1))
        self.window_2_size_hist.append(len(window_2))
        label_one = 0
        label_zero = 0
        for t in window_1:
            if t.label == 1:
                label_one += 1
            else:
                label_zero += 1
                
        self.window_1_one_hist.append(label_one)
        self.window_1_zero_hist.append(label_zero)
        
        label_one = 0
        label_zero = 0
        for t in window_2:
            if t.label == 1:
                label_one += 1
            else:
                label_zero += 1
                
        self.window_2_one_hist.append(label_one)
        self.window_2_zero_hist.append(label_zero)
    
    def eval(self, window_1, window_2, processed,time_interval):
        self.calc_evaluate(processed)
        mse_global, mse_zero, mse_one = self.mse()
        self.train_stat(window_1, window_2)
        #total,hits_total,hits_zero,hists_one,misses_total,misses_zero,misses_one,mse_global,mse_zero,mse_one,
        #window_1_size,window_1_zero,window_1_one,window_2_size,window_2_zero,window_2_one,time_interval
        line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}\n"
        line_formated = line.format(self.total,self.hits_total,self.hits_per_class[0],self.hits_per_class[1],
                    self.misses_total,self.misses_per_class[0],self.misses_per_class[1],
                    mse_global,mse_zero,mse_one,self.window_1_size_hist[-1],self.window_1_zero_hist[-1],
                    self.window_1_one_hist[-1],self.window_2_size_hist[-1],self.window_2_zero_hist[-1],
                    self.window_2_one_hist[-1],time_interval)
        
        return line_formated