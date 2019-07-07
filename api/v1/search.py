# -*- coding: utf-8 -*-
from chat import chatbot

chatter = chatbot.Chatbot(threshold=50, debug=False)

def searchTab(message):
    return chatter.searchTab(message)

def searchTag(message):
    return chatter.searchTag(message)

def searchLink(message):
    return chatter.searchLink(message)

def searchVideo(message):
    return chatter.searchVideo(message)

def getVideos(userid, pagetype, tab, currentvideoid, searchcontent):
    return chatter.getVideos(userid, pagetype, tab, currentvideoid, searchcontent)
