#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import logging

# used for loading tables from excel
import xlrd
import xlwt

inputPath = "./input"
replyPath = "./output"
sqlScriptName = "script.sql"

SQL_DATABASE_NAME = "yuwenmao"
SQL_TABLE_NAME_TAG = "tag"
SQL_TABLE_NAME_VIDEO = "video"
SQL_TABLE_NAME_TAG_VIDEO_MAP = "tvmap"

#style = xlwt.easyxf('align: wrap on')
style = xlwt.XFStyle()
style.alignment.wrap = 1

workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet('worksheet', cell_overwrite_ok=True)

worksheet.col(0).width = 256*20
worksheet.col(1).width = 256*60
worksheet.col(2).width = 256*10
worksheet.col(3).width = 256*10
worksheet.col(4).width = 256*50
worksheet.col(5).width = 256*200
worksheet.col(6).width = 256*200
worksheet.write(0, 0, label="视频名称")
worksheet.write(0, 1, label="链接")
worksheet.write(0, 2, label="文件类型")
worksheet.write(0, 3, label="相关性")
worksheet.write(0, 4, label="基本标签")
worksheet.write(0, 5, label="自定义标签")
worksheet.write(0, 6, label="题目")
workbookIndex = 1
workbookFile = "workbook.xls"

def stripPunctuation(line):
    return line.strip(":").strip('“').strip("‘").strip("(").strip(")").strip("[").strip("]").strip("{").strip("}").strip('，').strip('。')

def stripP(line):
    # return re.sub(ur"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+", "", line.decode("utf8"))
    # return line.strip("①").strip("②").strip("③").strip("④").strip("⑤").strip("⑥")
    return re.sub('[^\u4e00-\u9fa5a-zA-Z0-9]', ',', line)
    pass

def getText(f):
    #retContent = ""
    #with open(f, 'r', encoding='utf-8') as content:
        #for index, line in enumerate(content):
            #line = stripP(line)
            #retContent = retContent + line
    #return retContent
    fd = open(f)
    content = fd.read()
    fd.close()
    return content

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
    NamedLabels = {}
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

def genReply(p, labelStr, fd):
    c,v,u,l,f,r = getReplyContent(p)
    writeSQLScript(fd, v, c, u, labelStr, l, f, str(r))
    writeExcel(v, c, u, labelStr, l, f, str(r))

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

def recursiveLoop(p, labelStr, fd):
    logging.info("rescursive path: %s" % p)
    if containSubFile(p):
        genReply(p, labelStr, fd)
    else:
        if containSubDir(p):
            for f in os.listdir(p):
                if os.path.isdir(p + "/" + f):
                    recursiveLoop(p + "/" + f, labelStr+" "+f, fd)

def writeSQLScript(fd, vote, content, url, labels, tags, fileType, relevance):
    videoTags = []
    for item in labels.split(" "):
        sqlcmd = upsert(SQL_TABLE_NAME_TAG, name=item, style='common')
        videoTags.append('common-' + item)
        fd.write(sqlcmd)

    for key in tags.keys():
        for value in tags[key]:
            videoTags.append(key + "-" + value)
            sqlcmd = upsert(SQL_TABLE_NAME_TAG, name=value, style=key)
            fd.write(sqlcmd)

    sqlcmd = upsert(SQL_TABLE_NAME_VIDEO,
                    content=content,
                    filetype=fileType,
                    tags=",".join(videoTags),
                    vote=vote,
                    url=url)
    fd.write(sqlcmd)

def writeExcel(vote, content, url, labels, tags, fileType, relevance):
    global workbookIndex
    global style
    worksheet.write(workbookIndex, 0, label=vote, style=style)
    worksheet.write(workbookIndex, 1, label=url, style=style)
    worksheet.write(workbookIndex, 2, label=fileType, style=style)
    worksheet.write(workbookIndex, 3, label=relevance, style=style)
    worksheet.write(workbookIndex, 4, label=str(labels), style=style)
    worksheet.write(workbookIndex, 5, label=str(tags), style=style)
    worksheet.write(workbookIndex, 6, label=content, style=style)
    workbookIndex = workbookIndex + 1

def read(table, **kwargs):
    """ Generates SQL for a SELECT statement matching the kwargs passed. """
    sql = list()
    sql.append("SELECT * FROM %s " % table)
    if kwargs:
        sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.iteritems()))
    sql.append(";\n")
    return "".join(sql)


def upsert(table, **kwargs):
    """ update/insert rows into objects table (update if the row already exists)
        given the key-value pairs in kwargs """
    keys = ["%s" % k for k in kwargs]
    values = ["'%s'" % v for v in kwargs.values()]
    sql = list()
    sql.append("REPLACE INTO %s (" % table)
    sql.append(", ".join(keys))
    sql.append(") VALUES (")
    sql.append(", ".join(values))
    sql.append(");\n")
    return "".join(sql)


def delete(table, **kwargs):
    """ deletes rows from table where **kwargs match """
    sql = list()
    sql.append("DELETE FROM %s " % table)
    sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.iteritems()))
    sql.append(";\n")
    return "".join(sql)

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    sqlFile = open(replyPath + "/" + sqlScriptName, "w", encoding="utf-8")
#    sqlcmd = "DROP DATABASE IF EXISTS " + SQL_DATABASE_NAME + ";\n"
#    sqlFile.write(sqlcmd)
#
#    sqlcmd = "CREATE DATABASE " + SQL_DATABASE_NAME + ";\n"
#    sqlFile.write(sqlcmd)

    sqlcmd = "DROP TABLE IF EXISTS " + SQL_TABLE_NAME_TAG + ";\n"
    sqlFile.write(sqlcmd)

    sqlcmd = "CREATE TABLE IF NOT EXISTS " + \
                SQL_TABLE_NAME_TAG + " ( " \
                "id INT AUTO_INCREMENT, " + \
                "name varchar(255), " + \
                "style varchar(255), " + \
                "PRIMARY KEY (id) );\n"
    sqlFile.write(sqlcmd)

    sqlcmd = "ALTER TABLE " + SQL_TABLE_NAME_TAG + " ADD unique(name, style);\n"
    sqlFile.write(sqlcmd)

    sqlcmd = "ALTER TABLE " + SQL_TABLE_NAME_TAG + " CONVERT TO character set utf8;\n"
    sqlFile.write(sqlcmd)

    sqlcmd = "DROP TABLE IF EXISTS " + SQL_TABLE_NAME_VIDEO + ";\n"
    sqlFile.write(sqlcmd)

    sqlcmd = "CREATE TABLE IF NOT EXISTS " + \
                SQL_TABLE_NAME_VIDEO + " ( " \
                "id INT AUTO_INCREMENT, " + \
                "content TEXT, " + \
                "filetype varchar(1024), " + \
                "tags varchar(1024), " + \
                "url varchar(10240), " + \
                "vote varchar(1024), " + \
                "PRIMARY KEY (id) );\n"
    sqlFile.write(sqlcmd)

    sqlcmd = "ALTER TABLE " + SQL_TABLE_NAME_VIDEO + " CONVERT TO character set utf8;\n"
    sqlFile.write(sqlcmd)

    for topDir in os.listdir(inputPath):
        recursiveLoop(inputPath + "/" + topDir, topDir, sqlFile)
    sqlFile.close()
    workbook.save(replyPath + "/" + workbookFile)
        
if __name__ == "__main__":
    main()
