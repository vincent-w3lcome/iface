# -*- coding: utf-8 -*-#
import logging
import os


class Loader(object):

    def __init__(self, fileDir):
        self.fileDir = fileDir
        self.stopwords = set()

    def loadStopWords(self):
        logging.info("Loading stop words")

        path = os.path.join(self.fileDir, "data", "stopWords")

        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.stopwords.add(word.strip('\n'))
