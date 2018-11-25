import ast
import json
import logging
import os

import jieba


class Loader(object):

    def __init__(self, fileDir):

        self.fileDir = fileDir

        self.titles = [] # 欲进行匹配的所有标题
        self.titles_len = [] # 每个Titles.txt包含的条目个数相加列表
        self.segTitles = [] # 断好词的标题
        self.labels = []
        self.namedLabels = []
        self.inverted_labels = dict()
        self.inverted_namedLabels = dict()
        self.urls = []
        self.fileTypes = []
        self.stopwords = set()

        self.loadFormatReply()
        self.TitlesSegmentation()

    def jiebaCustomSetting(self, dict_path, usr_dict_path):

        jieba.set_dictionary(dict_path)
        with open(usr_dict_path, 'r', encoding='utf-8') as dic:
            for word in dic:
                jieba.add_word(word.strip('\n'))

    def loadStopWords(self):

        path = os.path.join(self.fileDir, "data", "stopWords")

        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.stopwords.add(word.strip('\n'))

    def loadFormatReply(self):

        path = os.path.join(self.fileDir, "data", "formatReply")

        logging.info("Start loading labels from: %s", path)
        for root, dirs, filenames in os.walk(path):
            for f in filenames:
                logging.info("Loading formatReply from file: %s", f)
                res = json.load(open(os.path.join(root,f), 'r', encoding='utf-8'))
                for r in res:
                    self.labels.append(r[0]['Labels'].split(' '))
                    self.namedLabels.append(r[0]['NamedLabels'])
                    self.titles.append(r[0]['Content'])
                    self.urls.append(r[0]['Url'])
                    self.fileTypes.append(r[0]['FileType'])
                self.titles_len.append([len(self.titles), f.split(".")[0]])
                logging.debug("Loaded labels: %s", str(self.labels))

        logging.debug("Loaded titles: %s", str(self.titles))

        for index, labels in enumerate(self.labels):
            for word in labels:
                if word not in self.inverted_labels.keys():
                    self.inverted_labels[word] = set()
                self.inverted_labels[word].add(index)

        for index, namedLabels in enumerate(self.namedLabels):
            if namedLabels == "":
                continue
            namedLabelsDict = ast.literal_eval(namedLabels)
            logging.debug("Loaded namedLabels: %s", str(namedLabelsDict))
            logging.debug("Loading URL: %s", self.urls[index])
            for k, v in namedLabelsDict.items():
                for word in v:
                    if word not in self.inverted_namedLabels.keys():
                        self.inverted_namedLabels[word] = set()
                    self.inverted_namedLabels[word].add(index)

        logging.debug("Loaded inverted labels: %s", str(self.inverted_labels))
        logging.debug("Loaded inverted namedLabels: %s", str(self.inverted_namedLabels))

    def wordSegmentation(self, string):

        return [word for word in jieba.cut(string,cut_all=True)]

    def TitlesSegmentation(self, cleanStopwords=False):

        """
        将 self.titles 断词后的结果输出，并储存于 self.segTitles

        Args:
            - cleanStopwords: 是否要清除标题中的停用词
        """

        logging.info("正准备将 titles 断词")

        count = 0

        path = os.path.join(self.fileDir, "data", "segTitles.txt")

        if not os.path.exists(path):

            self.segTitles = []
            for title in self.titles:

                if cleanStopwords:
                    clean = [word for word in self.wordSegmentation(title)
                            if word not in self.stopwords]
                    self.segTitles.append(clean)
                else:
                    self.segTitles.append(self.wordSegmentation(title))

                count += 1
                if count % 1000 == 0:
                    logging.info("已断词完前 %d 篇文章" % count)

            with open(path, 'w', encoding="utf-8") as seg_title:
                for title in self.segTitles:
                    seg_title.write(' '.join(title) + '\n')
            logging.info("完成标题断词，结果已暂存至 data/segTitles.txt")
        else:
            logging.info("侦测到先前的标题断词结果，读取中...")
            with open(path, 'r', encoding="utf-8") as seg_title:
                for line in seg_title:
                    line = line.strip('\n')
                    seg = line.split()

                    if cleanStopwords:
                        seg = [word for word in seg
                               if word not in self.stopwords]
                    self.segTitles.append(seg)
                logging.info("%d 个标题已完成载入" % len(self.segTitles))

        logging.debug("All segmented titles: %s" % str(self.segTitles))

    def getResponse(self, segTitleIndex):
        logging.debug("载入的标题长度列表: %s" % str(self.titles_len))
        for i, t in enumerate(self.titles_len):
            if segTitleIndex < t[0]:
                if i > 0:
                    titleIndex = segTitleIndex - self.titles_len[i-1][0]
                else:
                    titleIndex = segTitleIndex % t[0]
                break

        path = os.path.join(self.fileDir, "data", "formatReply", t[1] + ".json")
        res = json.load(open(path, 'r', encoding='utf-8'))
        logging.info("Labels: %s", res[titleIndex][0]["Labels"])
        logging.info("Vote: %s", res[titleIndex][0]["Vote"])
        logging.info("Url: %s", res[titleIndex][0]["Url"])
        logging.info("FileType: %s", res[titleIndex][0]["FileType"])
        return res[titleIndex]
