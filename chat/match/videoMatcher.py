import logging

from .matcher import Matcher

class videoMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, videoname):

        logging.info("Starting matching videos")

        if videoname == None or videoname == "":
            logging.info("Empty Query Tag Detected, skip video matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip video matching")
            return set()

        ret = self.db.queryEqualAnd(table, name=videoname)
        logging.debug("Matched database records: %s", ret )

        return ret
