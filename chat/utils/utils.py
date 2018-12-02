# -*- coding: utf-8 -*-#
import logging
import jieba

def wordSegmentation(self, string):
    logging.debug("Segmenting word")
    return [word for word in jieba.cut(string, cut_all=True)]
