# coding=utf-8
import json
import logging
import db.config as config

from chat.match.labelMatcher import labelMatcher
from chat.match.linkMatcher import linkMatcher
from chat.match.containMatcher import containMatcher
from chat.match.videoMatcher import videoMatcher
from chat.match.randomMatcher import randomMatcher
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
        self.randomMatcher = randomMatcher(self.database)

    def getResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        query = msgBuf.getQuery()

        self.labelMatcher.match(config.LABEL_TABLE_NAME, query)

        self.containMatcher.match(config.LABEL_TABLE_NAME, query)

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

        record = self.linkMatcher.match(config.LINK_TABLE_NAME, filename=filename)

        if record is not None:
            l = Link(record)
            l.show()
            self.getLinkVideoRecord(msgBuf, l.recommend1)
            self.getLinkVideoRecord(msgBuf, l.recommend2)
            self.getLinkVideoRecord(msgBuf, l.recommend3)

        logging.info("=======================================================\n")

    def getLinkVideoRecord(self, msgBuf, videoName, threshold=0):

        logging.info("=======================================================\n")

        records = self.videoMatcher.match(config.VIDEO_TABLE_NAME, name=videoName)

        for record in records:
            v = Video(record)
            v.show()
            self.getVideoLabelRecord(msgBuf, videoName)
            msgBuf.setReply(json.dumps(v.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getLabelVideoRecord(self, msgBuf, videoName, threshold=0):

        logging.info("=======================================================\n")

        records = self.videoMatcher.match(config.VIDEO_TABLE_NAME, name=videoName)

        for record in records:
            v = Video(record)
            v.show()
            msgBuf.setReply(json.dumps(v.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getLabelResponse(self, msgBuf, threshold=0):

        logging.info("=======================================================\n")

        query = msgBuf.getQuery()

        logging.info(query.split(","))

        l = query.split(",")
        if len(l) != 3:
            records = self.labelMatcher.fuzzyMatch(config.LABEL_TABLE_NAME, filename=query)
        else:
            records = self.labelMatcher.fuzzyMatch(config.LABEL_TABLE_NAME, \
                        year=l[0], region=l[1], sub=l[2])

        if len(records) <= 0:
            return

        for record in records:
            s = Label(record)
            s.show()
            msgBuf.setLabel(json.dumps(s.__dict__, ensure_ascii=False))
            self.getLabelVideoRecord(msgBuf, s.filename)

        logging.info("=======================================================\n")

    def getVideoLabelRecord(self, msgBuf, videoName, threshold=0):

        logging.info("=======================================================\n")

        record = self.labelMatcher.match(config.LABEL_TABLE_NAME, filename=videoName)

        s = Label(record)
        s.show()
        msgBuf.setLabel(json.dumps(s.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getVideoResponse(self, msgBuf, fuzzy=False):

        logging.info("=======================================================\n")

        query = msgBuf.getQuery()

        if query == "":
            return

        if fuzzy:
            records = self.videoMatcher.fuzzyMatch(config.VIDEO_TABLE_NAME, name=query)
        else:
            records = self.videoMatcher.match(config.VIDEO_TABLE_NAME, name=query)

        if len(records) <= 0:
            return

        for record in records:
            v = Video(record)
            v.show()
            self.getVideoLabelRecord(msgBuf, v.name)
            msgBuf.setReply(json.dumps(v.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getVideoIDResponse(self, msgBuf, fuzzy=False):

        logging.info("=======================================================\n")

        query = msgBuf.getQuery()

        if query == "":
            return

        if fuzzy:
            records = self.videoMatcher.fuzzyMatch(config.VIDEO_TABLE_NAME, vid=query)
        else:
            records = self.videoMatcher.match(config.VIDEO_TABLE_NAME, vid=query)

        if len(records) <= 0:
            return

        for record in records:
            v = Video(record)
            v.show()
            self.getVideoLabelRecord(msgBuf, v.name)
            msgBuf.setReply(json.dumps(v.__dict__, ensure_ascii=False))

        logging.info("=======================================================\n")

    def getRandomVideoResponse(self, msgBuf):

        logging.info("=======================================================\n")

        records = self.randomMatcher.match(config.VIDEO_TABLE_NAME, 5)

        if len(records) <= 0:
            return

        for record in records:
            v = Video(record)
            v.show()
            self.getVideoLabelRecord(msgBuf, v.name)
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
