import logging

from .matcher import Matcher

class labelMatcher(Matcher):

    def __init__(self, dbInstance):
        self.db = dbInstance

    def match(self, tag):

        logging.info("Starting matching labels")

        if tag == None or tag == "":
            logging.info("Empty Query Detected, skip label matching")
            return set()

        ret = self.db.queryContain("video", "tags", tag)
        logging.debug("Matched database records: %s", ret )

        return ret
