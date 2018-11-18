import logging

from .matcher import Matcher

class labelMatcher(Matcher):

    def __init__(self, inverted_labels, inverted_namedLabels):
        self.inverted_labels = inverted_labels
        self.inverted_namedLabels = inverted_namedLabels

    def match(self, msgBuf):

        logging.info("Starting matching labels")

        for label in self.inverted_labels.keys():
            if label == msgBuf.getQuery():
                if not msgBuf.getTargetIndex():
                    msgBuf.setTargetIndex(msgBuf.getTargetIndex() | (self.inverted_labels[label]))
                else:
                    msgBuf.setTargetIndex(msgBuf.getTargetIndex() & (self.inverted_labels[label]))

        for label in self.inverted_namedLabels.keys():
            if label == msgBuf.getQuery():
                if not msgBuf.getTargetIndex():
                    msgBuf.setTargetIndex(msgBuf.getTargetIndex() | (self.inverted_namedLabels[label]))
                else:
                    msgBuf.setTargetIndex(msgBuf.getTargetIndex() & (self.inverted_namedLabels[label]))


        logging.debug("Matched inverted (named)Labels: %s", str(msgBuf.getTargetIndex()))
