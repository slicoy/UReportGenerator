import os
import configparser

class DBinfo:
      cf = configparser.ConfigParser()
      cf.read("config.ini")
      secs = cf.sections() 
      items = cf.items("PG-Database")
      db_host = cf.get("PG-Database", "host")
      db_database = cf.get("PG-Database", "database")
      db_user = cf.get("PG-Database", "user")
      db_password = cf.get("PG-Database", "password")
      db_port = cf.get("PG-Database", "port")
      def prt(self):
        print(self)
        print(self.__class__)
        print(self.db_host)
        print(self.db_database)