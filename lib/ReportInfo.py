import configparser
class ReportInfo:
      cf = configparser.ConfigParser()
      cf.read("report-config.ini", encoding="utf-8")
      rt_dic = {}
      def getInfo(self):
          for i, rt_item in enumerate(self.cf.sections()):
              if rt_item != 'Author':
                 _table = ""
                 _groupby = ""
                 _where = ""
                 _orderby = ""
                 _table = rt_item
                 _seach = ""
                 if self.cf.has_option(rt_item,"groupby"):
                    _groupby = self.cf.get(rt_item,"groupby")
                 if self.cf.has_option(rt_item,"where"):
                    _where = self.cf.get(rt_item,"where")
                 if self.cf.has_option(rt_item,"orderby"):
                    _orderby = self.cf.get(rt_item,"orderby")
                 if self.cf.has_option(rt_item,"seach"):
                    _seach = self.cf.get(rt_item,"seach")
                 tmp_rtinfo = ReportInfoItems(_table=_table,_where=_where,_groupby=_groupby,_orderby=_orderby,_seach=_seach)
                 self.rt_dic[rt_item] = tmp_rtinfo
          return self.rt_dic

class ReportInfoItems:
      table   = ""
      where   = ""
      groupby = ""
      orderby = ""
      seach   = ""
      def __init__(self,_table,_where,_groupby,_orderby,_seach):
          self.table = _table
          self.where = _where
          self.groupby = _groupby
          self.orderby = _orderby
          self.seach = _seach
      def prt(self):
          print(self.where)
          print(self.groupby)
          print(self.orderby)
          print(self.seach)
      def str(self):
          return self.table

if __name__=='__main__':
   t = ReportInfo()
   a = t.getInfo()
   for key in a:
       print(key+':'+a[key].groupby)
