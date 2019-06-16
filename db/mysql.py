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

    def executeOne(self, cmd):
        ret = ""
        try:
            self._cursor.execute(cmd)
            ret = self._cursor.fetchone()
        except Exception as e:
            logging.error("Unable to execute cmd: %s, ERROR: %s" % (cmd, e))

        return ret

    def queryRandom(self, table, num):
        cmd = list()
        # cmd.append("SELECT * FROM %s " % table)
        # cmd.append("WHERE id >= (SELECT FLOOR( MAX(id) * RAND()) FROM `%s` ) ORDER BY id LIMIT %s" % (table, num))
        cmd.append("SELECT * FROM %s " % table)
        cmd.append("ORDER BY RAND() limit %s" % num)
        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def queryEqualAnd(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)
        if kwargs:
            cmd.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def queryEqualAndOne(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)
        if kwargs:
            cmd.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.executeOne(strCmd)

    def queryEqualOr(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)
        if kwargs:
            cmd.append("WHERE " + " OR ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def queryContainOr(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)

        if kwargs:
            num = 1
            cmd.append("WHERE ( ")
            for k, v in kwargs.items():
                num = num + 1
                cmd.append("".join("%s LIKE '%%" % k))
                cmd.append("".join("%s" % v))
                cmd.append("".join("%'"))
                if num <= len(kwargs):
                    cmd.append(" OR ")
            cmd.append(" )")

        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def queryContainAnd(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)

        if kwargs:
            num = 1
            cmd.append("WHERE ( ")
            for k, v in kwargs.items():
                num = num + 1
                cmd.append("".join("%s LIKE '%%" % k))
                cmd.append("".join("%s" % v))
                cmd.append("".join("%'"))
                if num <= len(kwargs):
                    cmd.append(" AND ")
            cmd.append(" )")

        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.execute(strCmd)

    def queryContainAndOne(self, table, **kwargs):
        cmd = list()
        cmd.append("SELECT * FROM %s " % table)

        if kwargs:
            num = 1
            cmd.append("WHERE ( ")
            for k, v in kwargs.items():
                num = num + 1
                cmd.append("".join("%s LIKE '%%" % k))
                cmd.append("".join("%s" % v))
                cmd.append("".join("%'"))
                if num <= len(kwargs):
                    cmd.append(" AND ")
            cmd.append(" )")

        cmd.append(";\n")

        strCmd = "".join(cmd)

        return self.executeOne(strCmd)

    def close(self):
        self._cursor.close()
        self._con.close()
