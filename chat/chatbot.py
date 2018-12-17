# -*- coding: utf-8 -*-
import json
import logging
import os
import random

from .qa.base import Answerer
from message.messageBuffer import messageBuffer

class Chatbot(object):

    def __init__(self, name="韩小喵", threshold=50, debug=False):

        # The name of chatbot
        self.name = name
        self.threshold = threshold

        if debug:
            log_level = logging.DEBUG
            logFormat='%(asctime)s : %(levelname)s : [%(filename)15s:%(lineno)5s - %(funcName)10s()] %(message)s'
        else:
            log_level = logging.INFO
            logFormat='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s'

        logging.basicConfig(level=log_level, format=logFormat)

        # For Question Answering
        try:
            self.answerer = Answerer()
        except Exception as e:
            self.answerer.database.close()
            logging.exception("[QA] 问答资料集未载入")

    def run(self, speech):

        logging.info("检测到输入: '%s'" % speech)

        # Init msgBuf, setting User and Query
        # TODO: Add timestamp info in msgBuf
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        logging.info("message buffer: '%s'", msgBuf.getQuery())

        # Match for highest similarit above threshold
        self.analyse(msgBuf, self.threshold)

        # Get reply that will be passed to media consumer(outQueue)
        ret = msgBuf.getReply()

        # Save msgBuf per user
        # Log file at "chat/data/msgHistory/<userName>.txt"
        self.saveMsg(msgBuf)

        return str(ret)

    def analyse(self, msgBuf, threshold=0):
        #self.answerer.getResponse(msgBuf, threshold)
        self.answerer.getLabelResponse(msgBuf, threshold)
        self.answerer.getContainResponse(msgBuf, threshold)

    def saveMsg(self, msgBuf, path="./"):
        path = os.path.join(os.path.dirname(__file__), "data", "msgHistory")
        if not os.path.exists(path):
            os.mkdir(path)

        if msgBuf.user:
            fileName = msgBuf.user + ".txt"
        else:
            fileName = "noUser.txt"

        try:
            f = open(path + '/' + fileName, 'a+', encoding='utf-8')
            #msgBuf.setTargetIndex(list(msgBuf.getTargetIndex()))
            #f.write(json.dumps(msgBuf.__dict__))
            f.write('\n')
            f.close()
        except Exception as e:
            logging.error("Save message error: %s", e)
