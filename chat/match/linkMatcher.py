import logging

from .matcher import Matcher

class linkMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, filename):

        logging.info("Starting matching links")

        if filename == None or filename == "":
            logging.info("Empty Query Tag Detected, skip link matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip link matching")
            return set()

        ret = self.db.queryEqualAnd(table, filename=filename)
        logging.debug("Matched database records: %s", ret )

        return ret
