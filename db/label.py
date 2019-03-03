# -*- coding: utf-8 -*-#
class Label(object):

    def __init__(self, record):

        self.id = record[0]
        self.filename = record[1]
        self.family = record[2]
        self.year = record[3]
        self.category = record[4]
        self.region = record[5]
        self.atype = record[6]
        self.sub = record[7]
        self.big = record[8]
        self.small = record[9]
        self.quality = record[10]
        self.label1 = record[11]
        self.label2 = record[12]
        self.label3 = record[13]
        self.label4 = record[14]
        self.score = record[15]
        self.difficulity = record[16]
        self.kp1 = record[17]
        self.kp2 = record[18]
        self.kp3 = record[19]
        self.kp4 = record[20]
        self.kp5 = record[21]
        self.kp6 = record[22]
        self.kp7 = record[23]
        self.kp8 = record[24]
        self.kp9 = record[25]
        self.kp10 = record[26]
        self.kp11 = record[27]
        self.kp12 = record[28]
        self.kp13 = record[29]
        self.kp14 = record[30]
        self.kp15 = record[31]
        self.kp16 = record[32]
        self.trait1 = record[33]
        self.trait2 = record[34]
        self.trait3 = record[35]
        self.trait4 = record[36]
        self.approach1 = record[37]
        self.approach2 = record[38]
        self.approach3 = record[39]
        self.approach4 = record[40]
        self.approach5 = record[41]
        self.approach6 = record[42]

    def show(self):

        print("------------------ labelSystem record start ----------------\n")
        print("id:        %s" % self.id)
        print("filename:  %s" % self.filename)
        print("family:    %s" % self.family)
        print("year:      %s" % self.year)
        print("category:  %s" % self.category)
        print("region:    %s" % self.region)
        print("type:      %s" % self.atype)
        print("sub:       %s" % self.sub)
        print("big:       %s" % self.big)
        print("small:     %s" % self.small)
        print("quality:   %s" % self.quality)
        print("score:     %s" % self.score)
        print("difficulity: %s" % self.difficulity)

        print("label[1~4]:  ( 1: %s - 2: %s - 3: %s - 4: %s )" %
                (self.label1, self.label2, self.label3, self.label4))

        print("kp[1~8]:     ( 1: %s - 2: %s - 3: %s - 4: %s - 5: %s - 6: %s - 7: %s - 8: %s )" %
                (self.kp1, self.kp2, self.kp3, self.kp4, self.kp5, self.kp6, self.kp7, self.kp8))

        print("kp[9~16]:    ( 9: %s - 10: %s - 11: %s - 12: %s - 13: %s - 14: %s - 15: %s - 16: %s )" %
                (self.kp9, self.kp10, self.kp11, self.kp12, self.kp13, self.kp14, self.kp15, self.kp16))

        print("trait[1~4]:  ( 1: %s - 2: %s - 3: %s - 4: %s )" %
                (self.trait1, self.trait2, self.trait3, self.trait4))

        print("approach[1~6]: ( 1: %s - 2: %s - 3: %s - 4: %s - 5: %s - 6: %s )" %
            (self.approach1, self.approach2, self.approach3, self.approach4, self.approach5, self.approach6))
