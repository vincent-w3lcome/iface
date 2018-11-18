# coding=utf-8

import json
import logging
import os

from chat.load.loader import Loader
from chat.match.labelMatcher import labelMatcher
from chat.match.containMatcher import containMatcher
from chat.match.bm25Matcher import bestMatchingMatcher

class Answerer(object):

    def __init__(self):

        self.loader = Loader(os.path.join(os.path.dirname(__file__), ".."))
        self.labelMatcher = labelMatcher(self.loader.inverted_labels, self.loader.inverted_namedLabels)
        self.containMatcher = containMatcher(self.loader.titles)
        self.bm25Matcher = bestMatchingMatcher(self.loader.titles, self.loader.segTitles)
        self.moduleTest()

    def moduleTest(self):

        logging.info("测试问答与断词模块中...")
        try:
            self.bm25Matcher.wordSegmentation("测试一下断词")
            logging.info("测试成功")
        except Exception as e:
            logging.info(repr(e))
            logging.exception("模块载入失败，请确认data与字典齐全")

    def getResponse(self, msgBuf, threshold=0):

        self.labelMatcher.match(msgBuf)

        if not msgBuf.getTargetIndex():
            logging.info("Cannot match any existing labels, "
                         "matching titles directly...")
            self.containMatcher.match(msgBuf)

        logging.debug("targetIndex(s): %s" % msgBuf.getTargetIndex())

        if msgBuf.getTargetIndex():
            # self.bm25Matcher.match(msgBuf)

            logging.info("=======================================================\n")

#            for item in msgBuf.getReplyIndex():
            for item in msgBuf.getTargetIndex():

                response = self.loader.getResponse(item)
                (msgBuf.getReply()).append(response)

            logging.info("=======================================================\n")

        else:
            self.bm25Matcher.match(msgBuf)
            

    def randomPick(self, answers):

        if len(answers) == 1:
            return answers[0][0]
        try:
            answer = answers[random.randrange(0, len(answers))][0]
        except:
            answer = None

        return answer
