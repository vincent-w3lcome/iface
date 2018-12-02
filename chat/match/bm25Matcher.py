import logging
import math

from .matcher import Matcher
from chat.utils import utils


class bestMatchingMatcher(Matcher):

    """
    基于 bm25 算法取得最佳关联短语
    """

    def __init__(self, titles, segTitles, removeStopWords=False):
        super().__init__()

        self.titles = titles
        self.segTitles = segTitles
        self.cleanStopWords = removeStopWords
        self.D = 0 # 句子总数

        self.wordset = set() # Corpus 中所有词的集合
        self.words_location_record = dict()  # 纪录该词 (key) 出现在哪几个句子(id)
        self.words_idf = dict() # 纪录每个词的 idf 值

        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75

        self.initBM25()

        if removeStopWords:
            self.loadStopWords("data/stopwords/chinese_sw.txt")
            self.loadStopWords("data/stopwords/specialMarks.txt")

    def initBM25(self):

        logging.info("BM25模块初始化中")

        self.D = len(self.segTitles)
        self.avgdl = sum([len(title) + 0.0 for title in self.segTitles]) / self.D

        for seg_title in self.segTitles:
            tmp = {}
            for word in seg_title:
                if not word in tmp:
                    tmp[word] = 0
                tmp[word] += 1
            self.f.append(tmp)
            for k, v in tmp.items():
                if k not in self.df:
                    self.df[k] = 0
                self.df[k] += 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)

        logging.info("BM25模块初始化完成")

    def sim(self, doc, index):

        logging.debug("Calculating similarity for inverted title: "
                      "%s" %self.f[index])
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.segTitles[index])
            score += (self.idf[word]*self.f[index][word]*(self.k1+1)
                      / (self.f[index][word]+self.k1*(1-self.b+self.b*d
                                                      / self.avgdl)))
        return score

    def calculateIDF(self):

        # 构建词集与纪录词出现位置的字典
        if len(self.wordset) == 0:
            self.buildWordSet()
        if len(self.words_location_record) == 0:
            self.buildWordLocationRecord()

        # 计算 idf
        for word in self.wordset:
            self.words_idf[word] = math.log2((self.D + .5)/(self.words_location_record[word] + .5))


    def buildWordLocationRecord(self):
        """
        建构词与词出现位置（句子id）的字典
        """
        for idx,seg_title in enumerate(self.segTitles):
            for word in seg_title:
                if self.words_location_record[word] is None:
                    self.words_location_record[word] = set()
                self.words_location_record[word].add(idx)

    def buildWordSet(self):
        """
        建立 Corpus 词集
        """
        for seg_title in self.segTitles:
            for word in seg_title:
                self.wordset.add(word)

    def addNgram(self,n):
        """
        扩充 self.seg_titles 为 n-gram
        """
        idx = 0

        for seg_list in self.segTitles:
            ngram = self.generateNgram(n,self.titles[idx])
            seg_list = seg_list + ngram
            idx += 1

    def generateNgram(self,n,sentence):
        return [sentence[i:i+n] for i in range(0,len(sentence)-1)]

    def match(self, msgBuf):
        """
        读入 query，若语料库中存在类似的句子，便回传该句子与标号

        Args:
            - query: 使用者欲查询的语句
        """

        similarity = []
        reply_index = []

        # Segment query
        seg_query = utils.wordSegmentation(msgBuf.getQuery())
        logging.debug("Segmented query: %s" % str(seg_query))

        for index in msgBuf.getTargetIndex():
            score = self.sim(seg_query, index)
            logging.debug("Loop against matched titles: %s "
                          "with index: %s" % (str(self.titles[index]), index))
            logging.debug("Loop against matched titles, "
                          "get score: %d for index: %d" % (score, index))

            if score < 0:
                score = 0
            # normalization
            score = score / self.sim(self.segTitles[index], index)
            similarity.append(score * 100) #百分制
            reply_index.append(index)

        # max = max / self.sim(self.segTitles[reply_index], reply_index)
        # target = ''.join(self.segTitles[reply_index])

        msgBuf.setSimilarity(similarity)
        msgBuf.setReplyIndex(reply_index)
        logging.info("Similarity percentage: %s" % str(msgBuf.getSimilarity()))
