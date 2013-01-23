'''
Created on Nov 7, 2012

@author: rloliveirajr
'''
from br.ufmg.dcc.slearning.validation.TestThenTrain import TestThenTrain
from sys import argv

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
            argv = argv[2:]                    
        else:
            argv = argv[1:]
    return opts

def main(classifier, data_file, dataset, results, params):
    
    interleaved = TestThenTrain(classifier_opt=classifier, data=data_file, dataset=dataset, results=results, params=params)
    
    interleaved.run()
    
if __name__ == '__main__':
    args = getopts(argv)
    
    _dataset = args["-d"]
    _file = args["-f"]
    results = args["-o"]
    classifier = args["-c"]
    arg = argv[1:]
    params = {}
    for i in range(0,len(arg[1:]),2):
        key = arg[i].replace("-","")
        value = arg[i+1]
        print key
        params[key] = value
    
    print (float(params["seed"])*2)
    main(classifier=classifier, data_file=_file, dataset=_dataset, results=results, params=params)