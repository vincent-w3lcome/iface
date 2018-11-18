import jieba


class Matcher(object):

    """
    比对使用者输入的句子与目标语料集，
    回传语料集中最相似的一个句子。
    """

    def __init__(self):
        pass

    def match(self, query):

        """
        读入使用者 query，若语料库中存在相同的句子，便回传该句子与标号

        Args:
            - query: 使用者的输入

        Return: (title,index)
            - title: 最为相似的标题
            - 该标题的索引编号
        """

        result = None
        for index, title in enumerate(self.titles):
            if title == query:
                return title,index

    def wordSegmentation(self, string):

        return [word for word in jieba.cut(string,cut_all=True)]
