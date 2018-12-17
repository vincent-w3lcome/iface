class messageBuffer(object):

    def __init__(self, user=None, group=None, query=None):

        self.user = user
        self.group = group
        self.query = query
        self.segQuery = []
        self.reply = []
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

