# -*- coding: utf-8 -*-#
import logging
import MySQLdb
from DBUtils.PooledDB import PooledDB
from db import config

class Mysql(object):

    __pool = None

    def __init__(self):

        self._con = Mysql.__getCon()
        self._cursor = self._con.cursor()

    @staticmethod
    def __getCon():
        if Mysql.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=2, maxcached=5,
                              host=config.DATABASE_HOST,
                              user=config.DATABASE_USER,
                              passwd=config.DATABASE_PASSWORD,
                              db=config.DATABASE_NAME,
                              charset=config.DATABASE_CHARSET)

        return __pool.connection()

    def execute(self, cmd):
        ret = ""
        try:
            self._cursor.execute(cmd)
            ret = self._cursor.fetchall()
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
        self._cursor.close()
        self._con.close()
