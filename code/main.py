import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import re
from Processor import TextProcessor

TRAIN_DOCUMENTS = "dataset/train/"
TEST_DOCUMEMENTS = "dataset/test/"
VOCABULARY_DOCUMENT = "results/model.txt"
RESULT_DOCUMENT = "results/result.txt"


textProcessor = TextProcessor()

'''
FileProcessor class which reads and processes files
'''
class FileProcessor:

    def __init__(self):
        self.space = "  "
    
    '''
    function to get list of files in a directory
    '''
    def loadDataFiles(self, path):
        return os.listdir(path)
    
    '''
    Indentifies the class type (spam | ham) from the file name
    '''
    def getClassType(self, file):
        docBase = os.path.basename(file.__getattribute__('name'))
        docName = os.path.splitext(docBase)[0]

        if re.search('(.*)-(ham)-(.*)', docName):
            return 'ham'
        else:
            return 'spam'

    
    '''
    read files line by line and processes it from TextProcessor
    '''
    def processFiles(self, files, path):
        for file in files:
            try:
                with open(str(path+file), "r", encoding="utf8", errors='ignore') as f:
                    classType = self.getClassType(f)

                    for line in f:
                        line = line.strip()
                        words = textProcessor.tokenize(line)
                        textProcessor.recordWordCount(words)
                        textProcessor.updatefrequencyCountInClass(classType, words)

            finally:
                f.close()
    
    '''
    Store Vocabulary in given file
    Following the format: 
        1 abc 3 0.003 40 0.4
        2 airplane 3 0.003 40 0.4
        3 password 40 0.4 50 0.03
        4 zucchini 0.7 0.003 0 0.000001

        where; each word is seperated by two spaces,
        and followed by carriage return at the end of line
    '''
    def storeVocabulary(self, file, vocabulary):
        try:
            with open(file, "w") as f:
                lineNum = 0
                for key, value in vocabulary.items():
                    lineNum += 1
                    lineString = (str(lineNum) + self.space 
                    + str(key) + self.space
                    + str(value[0]) + self.space 
                    + str(value[1]) + self.space 
                    + str(value[2]) + self.space 
                    + str(value[3]) + "\r")

                    f.write(lineString)

        finally:
            f.close()

    '''
    Store Classification Results in given file
    '''
    def storeClassificationResult(self, file, result):
        # TODO
        pass

'''
main method to execute scripts
'''
def main():
    fileProcessor = FileProcessor()
    
    trainFiles = fileProcessor.loadDataFiles(TRAIN_DOCUMENTS)
    testFiles = fileProcessor.loadDataFiles(TEST_DOCUMEMENTS)
    
    fileProcessor.processFiles(trainFiles, TRAIN_DOCUMENTS)
    textProcessor.buildVocabulary()
    fileProcessor.storeVocabulary(VOCABULARY_DOCUMENT, textProcessor.getVocabulary())

if __name__ == "__main__":
    main()



