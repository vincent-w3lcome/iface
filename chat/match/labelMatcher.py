import logging

from .matcher import Matcher

class labelMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, table, tag):

        logging.info("Starting matching labels")

        if tag == None or tag == "":
            logging.info("Empty Query Tag Detected, skip label matching")
            return set()

        if table == None or table == "":
            logging.info("Empty Query Table Detected, skip label matching")
            return set()

        ret = self.db.queryContainOr(table, label1=tag, label2=tag, label3=tag, label4=tag,
                                   filename=tag, family=tag, year=tag, category=tag, region=tag, score=tag,
                                   atype=tag, sub=tag, big=tag, small=tag, quality=tag, difficulity=tag)
        logging.debug("Matched database records: %s", ret )

        return ret
