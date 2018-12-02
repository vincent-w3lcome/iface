import logging

from .matcher import Matcher

class containMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, heading):

        logging.info("Starting 'contain' matching")

        if heading == None or heading == "":
            logging.info("Empty Query Detected, skip contain matching")
            return set()

        ret = self.db.queryContain("video", "content", heading)
        logging.debug("containMatches records: '%s'", ret)

        return ret
