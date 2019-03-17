# -*- coding: utf-8 -*-#
class Video(object):

    def __init__(self, record):

        self.id = record[0]
        self.name = record[1]
        self.fileId = record[2]
        self.vid = record[3]
        self.type = record[4]
        self.classId = record[5]
        self.className = record[6]
        self.classPath = record[7]
        self.createTime = record[8]
        self.expireTime = record[9]
        self.updateTime = record[10]
        self.mediaUrl = record[11]
        self.coverUrl = record[12]
        self.storageRegion = record[13]
        self.description = record[14]
        self.tagSet = record[15]

    def show(self):
        
        print("------------------ video record start ----------------\n")
        print("id:            %s" % self.id)
        print("name:          %s" % self.name)
        print("fileId:        %s" % self.fileId)
        print("vid:           %s" % self.vid)
        print("type:          %s" % self.type)
        print("classId:       %s" % self.classId)
        print("className:     %s" % self.className)
        print("classPath:     %s" % self.classPath)
        print("createTime:    %s" % self.createTime)
        print("expireTime:    %s" % self.expireTime)
        print("updateTime:    %s" % self.updateTime)
        print("mediaUrl:      %s" % self.mediaUrl)
        print("coverUrl:      %s" % self.coverUrl)
        print("storageRegion: %s" % self.storageRegion)
        print("description:   %s" % self.description)
        print("tagSet:        %s" % self.tagSet)
