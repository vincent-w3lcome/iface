# -*- coding: utf-8 -*-
from chat import chatbot

chatter = chatbot.Chatbot(threshold=50, debug=False)

def searchTag(message):
    return chatter.searchTag(message)

def searchLink(message):
    return chatter.searchLink(message)
