import logging

from .matcher import Matcher

class randomMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, num):

        logging.info("Starting matching random records")

        if num == None or num == "":
            logging.info("Empty Query num detected, using 1")
            num = 1

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip link matching")
            return set()

        ret = self.db.queryRandom(table, num)
        logging.debug("Matched database records: %s", ret )

        return ret
