import logging

from .matcher import Matcher

class videoMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, **kwargs):

        logging.info("match: Starting matching videos")

        if len(kwargs) <= 0:
            logging.info("Empty Query condition Detected, skip video matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip video matching")
            return set()

        ret = self.db.queryEqualAnd(table, **kwargs)
        logging.debug("Matched database records: %s", ret )

        return ret

    def fuzzyMatch(self, table, **kwargs):

        logging.info("fuzzyMatchName: Starting matching videos")

        if len(kwargs) <= 0:
            logging.info("Empty Query condition Detected, skip video matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip video matching")
            return set()

        ret = self.db.queryContainAnd(table, **kwargs)
        logging.debug("Matched database records: %s", ret )

        return ret