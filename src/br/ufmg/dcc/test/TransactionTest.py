'''
Created on Oct 29, 2012

@author: rloliveirajr
'''
import unittest
from br.ufmg.dcc.slearning.persistence.Transaction import Transaction

class Test(unittest.TestCase):


    def testCreateTransaction(self):
        _file = "/home/rloliveirajr/Documents/mestrado/dissertacao/entity_desambiguation_recognition/datasets/galo.tst"
        file_pointer = open(_file, "r")
        file_content = file_pointer.readlines()[0:100]
        ts = 1
        a = [Transaction(ts, i) for i in file_content]
        
        print a
        
        a = Transaction.create_transaction(file_content, 1)
        
        print a
        
    def testExtractionFields(self):
        _file = "/home/rloliveirajr/Documents/mestrado/dissertacao/entity_desambiguation_recognition/datasets/galo.tst"
        file_pointer = open(_file, "r")
        file_content = file_pointer.readlines()[0:100]
        ts = 1
        a = Transaction(ts, file_content[0])
        
        print a.fields  
        print a.label
        print a.tid

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testExtractionFields']
    unittest.main()