import sys
from chat import chatbot

chatter = chatbot.Chatbot(threshold=50, debug=False)

print("Hello, 我是韩小喵.")
print("请输入文字或语音:")

while True:
    speech = input()
    ret = chatter.run(speech)
    print('------------------------------')
