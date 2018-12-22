import logging

from .matcher import Matcher

class containMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, heading):

        logging.info("Starting 'contain' matching")

        if heading == None or heading == "":
            logging.info("Empty Query Heading Detected, skip contain matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip contain matching")
            return set()

        ret = self.db.queryContain(table, "content", heading)
        logging.debug("containMatches records: '%s'", ret)

        return ret
