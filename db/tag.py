# -*- coding: utf-8 -*-#
class Tag(object):

    def __init__(self, record):

        self.id = record[0]
        self.name = record[1]
        self.style = record[2]

    def show(self):
        
        print("------------------ video record start ----------------\n")
        print("id:       %s" % self.id)
        print("name:     %s" % self.name)
        print("style:    %s" % self.style)
