import logging

from .matcher import Matcher

class containMatcher(Matcher):

    def __init__(self, contents):
        self.contents = contents

    def match(self, msgBuf):

        logging.info("Starting 'contain' matching")

        targetIndex = set()
        query = msgBuf.getQuery()

        if query == None or query == "":
            return

        queryList = query.split(" ")

        for index, content in enumerate(self.contents):

            count = 0

            for q in queryList:
                if q in content:
                    count = count + 1

            if count == len(queryList):
                targetIndex.add(index)

        msgBuf.setTargetIndex(targetIndex)
                
        logging.info("containMatcher 后的 targetIndex : '%s'", msgBuf.getTargetIndex())
