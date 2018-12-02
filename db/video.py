# -*- coding: utf-8 -*-#
class Video(object):

    def __init__(self, record):

        self.id = record[0]
        self.content = record[1]
        self.filetype = record[2]
        self.tags = record[3]
        self.url = record[4]
        self.vote = record[5]

    def show(self):
        
        print("------------------ video record start ----------------\n")
        print("id:       %s" % self.id)
        print("url:      %s" % self.url)
        print("vote:     %s" % self.vote)
        print("tags:     %s" % self.tags)
        print("content:  %s" % self.content)
        print("filetype: %s" % self.filetype)
