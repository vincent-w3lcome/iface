# -*- coding: utf-8 -*-#
import logging
import MySQLdb

class Db(object):

    def __init__(self, host="localhost", user="root", passwd="", database="yuwenmao"):

        self.con = MySQLdb.connect(host, user, passwd, database, charset="utf8")
        self.cursor = self.con.cursor()

    def execute(self, cmd):
        ret = ""
        try:
            self.cursor.execute(cmd)
            ret = self.cursor.fetchall()
        except Exception as e:
            logging.error("Unable to execute cmd: %s, ERROR: %s" % (cmd, e))

        return ret

    def query(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)
        if kwargs:
            cmd.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def queryContain(self, table, column, content):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)
        if column:
            cmd.append("WHERE %s LIKE " % (column) + "'%" + "%s" % (content) + "%'")
        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def close(self):
        self.con.close()
