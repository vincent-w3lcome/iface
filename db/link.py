# -*- coding: utf-8 -*-#
class Link(object):

    def __init__(self, record):

        self.id = record[0]
        self.filename = record[1]
        self.justification = record[2]
        self.recommend1 = record[3]
        self.recommend2 = record[4]
        self.recommend3 = record[5]

    def show(self):

        print("------------------ link record start ----------------\n")
        print("id:            %s" % self.id)
        print("filename:      %s" % self.filename)
        print("justification: %s" % self.justification)
        print("recommend1:    %s" % self.recommend1)
        print("recommend2:    %s" % self.recommend2)
        print("recommend3:    %s" % self.recommend3)
