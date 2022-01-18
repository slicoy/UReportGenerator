# -*- coding: utf-8 -*-
"""
Created on 20220116
@author: Liuy
"""
import psycopg2 #导入相关模块
import pandas as pd
import os
import configparser
from lib.DBinfo import DBinfo
from lib.SupperDataFrame import SupperDataFrame

class DBCore:
      #功能：执行SQL语句
      #返回：SupperDataFrame对象
      def ExcSQL_SuperDataFrame(self,sql,columnsname = []):
          info = DBinfo()
          conn=psycopg2.connect(database=info.db_database,user=info.db_user,password=info.db_password,host=info.db_host,port=info.db_port)
          curs=conn.cursor()
          select_sql=sql        #从表格table中读取全表内容
          curs.execute( select_sql)               #执行该sql语句
          data = curs.fetchall()                  #获取数据
          dframe= SupperDataFrame(data,columns = columnsname)
          curs.close()                                    
          conn.close()
          return dframe

      #功能：执行SQL语句
      #返回：DataFrame对象
      def ExcSQL_DataFrame(self,sql):
          info = DBinfo()
          conn=psycopg2.connect(database=info.db_database,user=info.db_user,password=info.db_password,host=info.db_host,port=info.db_port)
          curs=conn.cursor()
          select_sql=sql        #从表格table中读取全表内容
          curs.execute( select_sql)               #执行该sql语句
          data = curs.fetchall()                  #获取数据
          #dframe= DataFrame(data,columns = columnsname)
          curs.close()                                    
          conn.close()
          return pd.DataFrame(data)

      def prt(self):
        print(self)
        print(self.__class__)
        print(self.db_host)
        print(self.db_database)