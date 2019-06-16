#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import logging

# used for loading tables from excel
import xlrd

inputPath = "./input"
replyPath = "./output"

def stripPunctuation(line):
    return line.strip(":").strip('“').strip("‘").strip("(").strip(")").strip("[").strip("]").strip("{").strip("}").strip('，').strip('。')

def stripP(line):
    # return re.sub(ur"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+", "", line.decode("utf8"))
    # return line.strip("①").strip("②").strip("③").strip("④").strip("⑤").strip("⑥")
    return re.sub('[^\u4e00-\u9fa5a-zA-Z0-9]', ',', line)
    pass

def getText(f):
    retContent = ""
    with open(f, 'r', encoding='utf-8') as content:
        for index, line in enumerate(content):
            line = stripP(line)
            retContent = retContent + line
    return retContent

def getXlsx(f):
    retLabels = {}
    data = xlrd.open_workbook(f)
    sheet = data.sheet_by_name('Sheet1')
    nrows_num = sheet.nrows
    ncols_num = sheet.ncols
    for ncols in range(ncols_num):
        for nrows in range(nrows_num):
            if nrows == 0:
                k = sheet.row_values(nrows)[ncols]
                retLabels[k] = []
                continue
            v = sheet.row_values(nrows)[ncols]
            if v != "":
                retLabels[k].append(str(v))

    return retLabels

# getRelevance gets relevance file information from folder p
# It returns a dictionary of relevances with Key being the 
# folder(p) name and Value being the Url of file under p.
def getRelevance(p):
    pass

def getReplyContent(p):

    Content = ""
    Vote = ""
    Url = ""
    NamedLabels = ""
    FileType = ""
    Relevance = []

    for f in os.listdir(p):
        filePath = p + "/" + f

        if os.path.isdir(filePath):
            # Note: Currently only one relevance folder is allowed,
            Relevance.append(getRelevance(filePath))
            continue

        if f.split('.')[1] == "png":
            continue

        if f.split('.')[1] == "txt":
            Content = getText(filePath)
            continue

        if f.split('.')[1] == 'xlsx':
            NamedLabels = getXlsx(filePath)
            continue

        if f.split('.')[1] != 'txt' and f.split('.')[1] != 'xlsx':
            Vote = f
            FileType = f.split('.')[1]
            Url = filePath
            continue

    return Content, Vote, Url, NamedLabels, FileType, Relevance

def genJsonReply(p, fd):
    c,v,u,l,f = getReplyContent(p)
    format_list = [v,c,u,l,f]
    string = '"Vote": "{}", "Content": "{}", "Url": "{}", "Labels": "{}", "FileType": "{}"'.format(*format_list)
    json.dump(json.loads("[{" + string + "}]"), fd)
    fd.write("\n")
    logging.info("Get: %s" % string)

def genReply(p, labelStr, fd):
    c,v,u,l,f,r = getReplyContent(p)
    writeReply(v, c, u, labelStr, l, f, str(r), fd)

    logging.info("Get: Content: %s, Vote: %s, Url: %s, Labels: %s, NamedLabels: %s, FileType: %s, Relevance: %s"
                 % (c,v,u,labelStr,l,f, str(r)))

def isDirAndNoSubDir(p):
    if os.path.isdir(p):
        for f in os.listdir(p):
            if os.path.isdir(f):
                return False
        return True
    return False

def containSubDir(p):
    if os.path.isdir(p):
        for f in os.listdir(p):
            if os.path.isdir(p + "/" + f):
                return True
    return False

def containSubFile(p):
    if os.path.isdir(p):
        for f in os.listdir(p):
            if os.path.isfile(p + "/" + f):
                return True
    return False

def subFileContainRelevance(p):
    return False

# Whether folder p contains all the files to generate a reply
def subFileContainContent(p):
    txtExist = False
    m4vExist = False
    xlsxExist = False

    for f in os.listdir(p):
        if os.path.isdir(p+"/"+f):
            continue
        if f.split('.')[1] == "txt":
            txtExist = True
            continue
        if f.split('.')[1] == 'xlsx':
            xlsxExist = True
            continue
        if f.split('.')[1] == 'm4v':
            m4vExist = True

    if txtExist and m4vExist and xlsxExist:
        return True

    return False

def NewRecursiveLoop(p, labelStr, fd):
    logging.info("rescursive path: %s" % p)
    if containSubFile(p) and subFileContainContent(p):
        genReply(p, labelStr, fd)
    else:
        if containSubFile(p):
            # Get relevance file here and pass it to next recursiveLoop
            pass
        if containSubDir(p):
            for f in os.listdir(p):
                if os.path.isdir(p + "/" + f):
                    recursiveLoop(p + "/" + f, labelStr+" "+f, fd)

def recursiveLoop(p, labelStr, fd):
    logging.info("rescursive path: %s" % p)
    if containSubFile(p):
        genReply(p, labelStr, fd)
    else:
        if containSubDir(p):
            for f in os.listdir(p):
                if os.path.isdir(p + "/" + f):
                    recursiveLoop(p + "/" + f, labelStr+" "+f, fd)

def writeReply(vote, content, url, labels, namedLabels, filetype, relevance, fd):
    fd.write('\t[\n')
    fd.write('\t\t{\n')
    fd.write('\t\t\t"Vote": "%s",\n' % vote)
    fd.write('\t\t\t"Content": "%s",\n' % str(content))
    fd.write('\t\t\t"Url": "%s",\n' % url)
    fd.write('\t\t\t"Labels": "%s",\n' % labels)
    fd.write('\t\t\t"NamedLabels": "%s",\n' % namedLabels)
    fd.write('\t\t\t"FileType": "%s",\n' % filetype)
    fd.write('\t\t\t"Relevance": "%s"\n' % relevance)
    fd.write('\t\t}\n')
    fd.write('\t],\n')

def writeFileTailer(fd):
    fd.write('\t[\n')
    fd.write('\t\t{\n')
    fd.write('\t\t\t"Vote": "",\n')
    fd.write('\t\t\t"Content": "",\n')
    fd.write('\t\t\t"Url": "",\n')
    fd.write('\t\t\t"Labels": "",\n')
    fd.write('\t\t\t"NamedLabels": "{}",\n')
    fd.write('\t\t\t"FileType": "",\n')
    fd.write('\t\t\t"Relevance": ""\n')
    fd.write('\t\t}\n')
    fd.write('\t]\n')

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    for topDir in os.listdir(inputPath):
        outputFile = open(replyPath + "/" + topDir + ".json", "w", encoding="utf-8")
        outputFile.write('[\n')
        recursiveLoop(inputPath + "/" + topDir, topDir, outputFile)
        writeFileTailer(outputFile)
        outputFile.write(']\n')
        outputFile.close()
        

if __name__ == "__main__":
    main()
