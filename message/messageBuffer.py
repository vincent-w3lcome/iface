# coding=utf-8
import json

class messageBuffer(object):

    def __init__(self, user=None, group=None, query=None):

        self.user = user
        self.group = group
        self.query = query
        self.segQuery = []
        self.reply = []
        self.label = []
        self.replyIndex = set()
        self.labelIndex = set()
        self.containIndex = set()

    def setUser(self, user):
        self.user = user

    def getUser(self):
        return self.user

    def setGroup(self, group):
        self.group = group

    def getGroup(self):
        return self.group

    def setQuery(self, query):
        self.query = query

    def getQuery(self):
        return self.query

    def setSegQuery(self, segQuery):
        self.segQuery = segQuery

    def getSegQuery(self):
        return self.segQuery

    def setReplyIndex(self, index):
        self.replyIndex = index

    def getReplyIndex(self):
        return self.replyIndex

    def setReply(self, reply):
        self.reply.append(reply)

    def getReply(self):
        return self.reply

    def setLabel(self, label):
        self.label.append(label)

    def getLabel(self):
        return self.label

    def getJsonReply(self):
        return {"Data": self.getReply()}


class apiVideoData(object):
    def __init__(self, msgBuf):

        self.msgBuf = msgBuf
        self.modId = "ID"
        self.cms_data = { "ZT_leaf_head": "视频列表标题" }
        self.meta = { "title": "视频列表元标题" }
        self.type = "video"
        self.list = []

    def getBgPic(self, labelRecord):
        topic = labelRecord["atype"].replace('补', '' )
        if topic == '语言文字运用':
            return "https://rs.yuwenmao.net/common/red.png"
        if topic == '作文':
            return "https://rs.yuwenmao.net/common/blue.png"
        if topic == '古代诗文阅读':
            return "https://rs.yuwenmao.net/common/green.png"
        if topic == '现代文阅读':
            return "https://rs.yuwenmao.net/common/yellow.png"
        if topic == '名著阅读':
            return "https://rs.yuwenmao.net/common/orange.png"
        if topic == '附加题':
            return "https://rs.yuwenmao.net/common/orange.png"
        return "https://rs.yuwenmao.net/common/bluedark.png"

    def getLabels(self, labelRecord):
        ret = []
        if labelRecord['label1'] != '':
            ret.append(labelRecord['label1'])
        if labelRecord['label2'] != '':
            ret.append(labelRecord['label2'])
        if labelRecord['label3'] != '':
            ret.append(labelRecord['label3'])
        if labelRecord['label4'] != '':
            ret.append(labelRecord['label4'])
        return ret

    def getReply(self):
        replyList = []

        for item in self.msgBuf.getReply():
            index = self.msgBuf.getReply().index(item)
            i = json.loads(item)
            l = json.loads(self.msgBuf.getLabel()[index])
            v = {'itemId': i["id"],
                 'itemType': i["type"],
                 'cid': i["classId"],
                 'vid': i["vid"],
                 'videoUrl': i["mediaUrl"],
                 'bgPic': self.getBgPic(l),
                 'pictype': "2",
                 '_hide': False,
                 'title': i["name"].replace('补', ''),
                 'subtitle': l["sub"].replace('补', ''),
                 'tagtext': self.getLabels(l),
                 'timelong': "05:12",
                 'year': l['year'].split('.')[0],
                 'region': l['region'],
                 'topic': l["atype"].replace('补', ''),
                 'type': "mp4"}
            replyList.append(v)

        d = self.constructReply(replyList)
        return d

    def constructReply(self, l):
        return {"modId": self.modId,
                "cms_data": self.cms_data,
                "meta": self.meta,
                "type": self.type,
                "list": l}

class Buffer(object):

    def __init__(self, user=None, group=None, query=None, reply=None, sim=0):

        self.user = user
        self.group = group

        self.query = query
        self.strippedQuery = None
        self.segQuery = None
        self.sim = sim
        self.reply = reply
        self.replyIndex = None

        self.targetIndex = set()

#            v = '{' + \
#                'itemId: %s,' % i["id"] + \
#                'itemType: "%s",' % i["type"] + \
#                'cid: %s,' % i["classId"] + \
#                'vid: %s,' % i["vid"] + \
#                'videoUrl: "%s",' % i["mediaUrl"] + \
#                'bgPic: 2,' + \
#                'pictype: 2,' + \
#                '_hide: false,' + \
#                'title: "%s",' % i["name"] + \
#                'subtitle: "%s",' % i["name"] + \
#                'tagtext: %s,' % i["tagSet"] + \
#                'timelong: 5,' + \
#                'year: 2018,' + \
#                'region: 北京,' + \
#                'topic: %s,' % i["name"] + \
#                'type: "mp4"' + \
#                '}'
