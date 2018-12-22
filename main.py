# -*- coding: utf-8 -*-#
from chat import chatbot
from flask import Flask

chatter = chatbot.Chatbot(threshold=50, debug=False)

app = Flask(__name__)

@app.route("/search/video/tag/<query>", methods=['GET'])
def searchVideoTag(query):
    return chatter.searchVideoTag(query)

@app.route("/search/video/title/<query>", methods=['GET'])
def searchVideoTitle(query):
    return chatter.searchVideoTitle(query)

@app.route("/search/video/name/<query>", methods=['GET'])
def searchVideoName(query):
    return chatter.searchVideoName(query)

@app.route("/search/tag/<query>", methods=['GET'])
def searchTag(query):
    return chatter.searchTag(query)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
