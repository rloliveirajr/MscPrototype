'''
Created on Oct 29, 2012

@author: rloliveirajr
'''

def cmpf(a, b, EPS = 1e-15):
    if a > b - EPS:
        if b > a - EPS:
            return 0
        else:
            return 1
    return -1

def read_file(_file):
    '''
        Este metodo le um arquivo para um array
        
        @param _file: Nome do arquivo a ser lido
        @return: Um array em que cada posicao eh uma linha do arquivo.
    '''
    file_pointer = open(_file, "r")
    file_content = file_pointer.readlines()
    
    return file_content

def write_file(_file, content, mode="w"):
    '''
        Este metodo cria um arquivo
        
        @param _file: Nome do arquivo a ser criado
        @param content: Conteudo a ser escrito no arquivo
    '''
    file_pointer = open(_file, mode)
    
    file_pointer.writelines(content)