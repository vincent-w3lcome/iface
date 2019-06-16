import logging

from .matcher import Matcher

class linkMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, **kwargs):

        logging.info("match: Starting matching links")

        if len(kwargs) <= 0:
            logging.info("Empty Query condition Detected, skip link matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip link matching")
            return set()

        ret = self.db.queryEqualAndOne(table, **kwargs)
        logging.debug("Matched database records: %s", ret )

        return ret

    def fuzzyMatch(self, table, **kwargs):

        logging.info("fuzzyMatchName: Starting matching links")

        if len(kwargs) <= 0:
            logging.info("Empty Query condition Detected, skip link matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip link matching")
            return set()

        ret = self.db.queryContainAndOne(table, **kwargs)
        logging.debug("Matched database records: %s", ret )

        return ret
