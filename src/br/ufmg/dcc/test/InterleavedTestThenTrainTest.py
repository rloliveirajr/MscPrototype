'''
Created on Oct 29, 2012

@author: rloliveirajr
'''
import unittest
from br.ufmg.dcc.slearning.validation.TestThenTrain import TestThenTrain


class Test(unittest.TestCase):


    def testRun(self):
        dp = "/home/rloliveirajr/Downloads/analise-sentimento/felipemelo.lac"
        resource = "/home/rloliveirajr/Workspace/Msc/resource"
        nclasses = 2
        interleaved = TestThenTrain(nclasses, dp, resource)
        
        interleaved.run(seed=0.01, reliability=0.75, rule_size=3)
        
        print dp

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRun']
    unittest.main()