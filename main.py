# -*- coding: utf-8 -*-#
from chat import chatbot
from flask import Flask

chatter = chatbot.Chatbot(threshold=50, debug=False)

app = Flask(__name__)

@app.route("/search/<query>", methods=['GET'])
def run(query):
    return chatter.run(query)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
