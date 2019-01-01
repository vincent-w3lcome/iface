# coding=utf-8
import json
import logging
import db.config as config

from chat.match.labelMatcher import labelMatcher
from chat.match.containMatcher import containMatcher
from chat.match.bm25Matcher import bestMatchingMatcher
from db.mysql import Mysql
from db.video import Video

class Answerer(object):

    def __init__(self):

        self.database = Mysql()
        self.labelMatcher = labelMatcher(self.database)
        self.containMatcher = containMatcher(self.database)
        # self.moduleTest()

    def moduleTest(self):

        logging.info("测试问答与断词模块中...")
        try:
            self.bm25Matcher.wordSegmentation("测试一下断词")
            logging.info("测试成功")
        except Exception as e:
            logging.info(repr(e))
            logging.exception("模块载入失败，请确认data与字典齐全")

    def getResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        query = msgBuf.getQuery()

        self.labelMatcher.match(config.VIDEO_TABLE_NAME, query)

        self.containMatcher.match(config.VIDEO_TABLE_NAME, query)

        logging.info("=======================================================\n")

    def getLabelResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        tag = msgBuf.getQuery()

        records = self.labelMatcher.match(config.VIDEO_TABLE_NAME, tag)

        if len(records) <= 0:
            return

        for record in records:
            v = Video(record)
            v.show()
            msgBuf.labelIndex.update(str(v.id))
            msgBuf.setReply(json.dumps(v.__dict__, ensure_ascii=False))
            
        logging.info("=======================================================\n")

    def getContainResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        heading = msgBuf.getQuery()

        records = self.containMatcher.match(config.VIDEO_TABLE_NAME, heading)

        if len(records) <= 0:
            return

        for record in records:
            v = Video(record)
            v.show()
            msgBuf.containIndex.update(str(v.id))
            
        logging.info("=======================================================\n")

    def randomPick(self, answers):

        if len(answers) == 1:
            return answers[0][0]
        try:
            answer = answers[random.randrange(0, len(answers))][0]
        except:
            answer = None

        return answer
