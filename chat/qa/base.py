# coding=utf-8
import json
import logging
import db.config as config

from chat.match.labelMatcher import labelMatcher
from chat.match.linkMatcher import linkMatcher
from chat.match.containMatcher import containMatcher
from chat.match.videoMatcher import videoMatcher
from chat.match.bm25Matcher import bestMatchingMatcher
from db.mysql import Mysql
from db.video import Video
from db.label import Label
from db.link import Link

class Answerer(object):

    def __init__(self):

        self.database = Mysql()
        self.labelMatcher = labelMatcher(self.database)
        self.linkMatcher = linkMatcher(self.database)
        self.containMatcher = containMatcher(self.database)
        self.videoMatcher = videoMatcher(self.database)
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

        self.labelMatcher.match(config.LABEL_TABLE_NAME, query)

        self.containMatcher.match(config.LABEL_TABLE_NAME, query)

        logging.info("=======================================================\n")

    def getLabelResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        tag = msgBuf.getQuery()

        records = self.labelMatcher.match(config.LABEL_TABLE_NAME, tag)

        if len(records) <= 0:
            return

        for record in records:
            s = Label(record)
            s.show()
            msgBuf.labelIndex.update(str(s.id))
            msgBuf.setReply(json.dumps(s.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getContainResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        heading = msgBuf.getQuery()

        records = self.containMatcher.match(config.LABEL_TABLE_NAME, heading)

        if len(records) <= 0:
            return

        for record in records:
            s = Label(record)
            s.show()
            msgBuf.labelIndex.update(str(s.id))
            msgBuf.setReply(json.dumps(s.__dict__, ensure_ascii=False))
            
        logging.info("=======================================================\n")

    def getLinkResponse(self, msgBuf):

        logging.info("=======================================================\n")

        filename = msgBuf.getQuery()

        records = self.linkMatcher.match(config.LINK_TABLE_NAME, filename)

        if len(records) <= 0:
            return

        for record in records:
            l = Link(record)
            l.show()
            msgBuf.labelIndex.update(str(l.id))
            msgBuf.setReply(json.dumps(l.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getVideoResponse(self, msgBuf):

        logging.info("=======================================================\n")

        videoname = msgBuf.getQuery()

        records = self.videoMatcher.match(config.VIDEO_TABLE_NAME, videoname)

        if len(records) <= 0:
            return

        for record in records:
            v = Video(record)
            v.show()
            msgBuf.labelIndex.update(str(v.id))
            msgBuf.setReply(json.dumps(v.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def randomPick(self, answers):

        if len(answers) == 1:
            return answers[0][0]
        try:
            answer = answers[random.randrange(0, len(answers))][0]
        except:
            answer = None

        return answer
