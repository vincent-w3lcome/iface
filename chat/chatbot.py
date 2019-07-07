# -*- coding: utf-8 -*-
import json
import logging
import os
import random

from .qa.base import Answerer
from message.messageBuffer import messageBuffer
from message.messageBuffer import apiVideoData
from message.messageBuffer import apiTabData

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

        apiRet = apiVideoData(msgBuf)

        # Save msgBuf per user
        # Log file at "chat/data/msgHistory/<userName>.txt"
        self.saveMsg(msgBuf)

        return str(apiRet.getReply())

    def searchVideoTag(self, speech):

        logging.info("检测到 searchVideoTag 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        self.answerer.getLabelResponse(msgBuf, self.threshold)
        self.saveMsg(msgBuf)
        return str(msgBuf.getReply())

    def searchVideoTitle(self, speech):

        logging.info("检测到 searchVideoTitle 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        self.answerer.getContainResponse(msgBuf, self.threshold)
        self.saveMsg(msgBuf)
        return str(msgBuf.getReply())

    def searchVideoName(self, speech):

        logging.info("检测到 searchVideoName 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        self.answerer.getContainResponse(msgBuf, self.threshold)
        self.saveMsg(msgBuf)
        return str(msgBuf.getReply())

    def searchVideo(self, speech):

        logging.info("检测到 searchVideo 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        self.answerer.getVideoResponse(msgBuf)
        self.saveMsg(msgBuf)
        return json.dumps(msgBuf.getJsonReply(), ensure_ascii=False)

    def searchTab(self, speech):

        logging.info("检测到 searchTab 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        ret = apiTabData(msgBuf)
        self.saveMsg(msgBuf)
        print(json.dumps(ret.getReply(), ensure_ascii=False))
        return json.dumps(ret.getReply(), ensure_ascii=False)

    def searchTag(self, speech):

        logging.info("检测到 searchTag 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        self.answerer.getLabelResponse(msgBuf, self.threshold)
        ret = apiVideoData(msgBuf)
        self.saveMsg(msgBuf)
        print(json.dumps(ret.getReply(), ensure_ascii=False))
        return json.dumps(ret.getReply(), ensure_ascii=False)

    def searchLink(self, speech):

        logging.info("检测到 searchLink 输入: '%s'" % speech)
        msgBuf = messageBuffer(user="defaultUser", query=speech)
        self.answerer.getLinkResponse(msgBuf)
        ret = apiVideoData(msgBuf)
        self.saveMsg(msgBuf)
        print(json.dumps(ret.getReply(), ensure_ascii=False))
        return json.dumps(ret.getReply(), ensure_ascii=False)

    def getVideos(self, userid, ptype, tab, videoid, searchcontent):

        logging.info("检测到 getVideos 输入: user id: '%s'" % userid)
        logging.info("检测到 getVideos 输入: port type: '%s'" % ptype)
        logging.info("检测到 getVideos 输入: tab: '%s'" % tab)
        logging.info("检测到 getVideos 输入: video id: '%s'" % videoid)
        logging.info("检测到 getVideos 输入: search content: '%s'" % searchcontent)

        msgBuf = messageBuffer(user="defaultUser")

        if userid != "":
            msgBuf.setUser(userid)

        if ptype == "home":
            logging.info("In page type.")
            self.answerer.getRandomVideoResponse(msgBuf)

        elif tab != "":
            logging.info("In tab.")
            msgBuf.setQuery(tab)
            self.answerer.getVideoResponse(msgBuf, True)

        elif videoid != "":
            logging.info("In video id.")
            msgBuf.setQuery(videoid)
            self.answerer.getVideoIDResponse(msgBuf)

        elif searchcontent != "":
            logging.info("In search content.")
            msgBuf.setQuery(searchcontent)
            self.answerer.getVideoResponse(msgBuf, True)

        else:
            logging.info("In else (no param match).")
            self.answerer.getRandomVideoResponse(msgBuf)

        ret = apiVideoData(msgBuf)
        self.saveMsg(msgBuf)
        print(json.dumps(ret.getReply(), ensure_ascii=False))
        return json.dumps(ret.getReply(), ensure_ascii=False)

    def analyse(self, msgBuf, threshold=0):
        #self.answerer.getResponse(msgBuf, threshold)
        self.answerer.getLabelResponse(msgBuf, threshold)
        #self.answerer.getContainResponse(msgBuf, threshold)
        #self.answerer.getLinkResponse(msgBuf)
        #self.answerer.getVideoResponse(msgBuf)
        #self.answerer.getVideoIDResponse(msgBuf)
        #self.getVideos(1,"home","","","")
        #self.getVideos(1,"home","2018","","")
        #self.getVideos(1,"","","5285890784391032512","")
        #self.getVideos(1,"","","5285890784391032512","考题2018高考浙江卷现代文阅读补文学类文本阅读1200标清")

    def saveMsg(self, msgBuf, path="./"):
        path = os.path.join(os.path.dirname(__file__), "data", "msgHistory")
        if not os.path.exists(path):
            os.mkdir(path)

        if msgBuf.user:
            fileName = str(msgBuf.user) + ".txt"
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
