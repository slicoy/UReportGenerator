# -*- coding: utf-8 -*-
"""
Created on 20220116
@author: Liuy
"""
# 导入相关模块
import pandas as pd
import configparser
from jinja2 import Template, FileSystemLoader, Environment
from lib.DBinfo import DBinfo
from lib.DBCore import DBCore
from lib.ReportInfo import ReportInfo,ReportInfoItems


sql_structure ="""SELECT
  C .relname,
  CAST (obj_description (c.relfilenode, 'pg_class') AS VARCHAR) AS COMMENT,
  A .attname AS field,
  concat_ws('',t.typname,SUBSTRING(format_type(a.atttypid,a.atttypmod) from '\(.*\)')) as type_length,
  b.description AS COMMENT,
  case  when A .attnotnull = 't' THEN 'true' else 'false' end AS NOTNULL,
  case when(select count(pc.conname) from pg_constraint  pc where a.attnum = pc.conkey [ 1 ] and pc.conrelid = c.oid) = '1' then 'true' else 'false' end as iskey
FROM
  pg_class C,
  pg_attribute A

LEFT OUTER JOIN pg_description b ON A .attrelid = b.objoid
AND A .attnum = b.objsubid,
 pg_type T
WHERE
  C .relname in(select pt.tablename from pg_tables pt where pt.schemaname = 'public') 
AND A .attnum > 0
AND A .attrelid = C .oid
AND A .atttypid = T .oid
ORDER BY
  C .relname,
  A .attnum;"""

PGinfo= DBinfo()
pgcore = DBCore()

Rtsinfo = ReportInfo()
rts_condition_info = Rtsinfo.getInfo()

for rt_key in rts_condition_info:
    print(rt_key+':'+rts_condition_info[rt_key].groupby)

#生成PG结构的excel表单
df_pglog = pgcore.ExcSQL_SuperDataFrame(sql = sql_structure,columnsname = ['relname','comment','field','type_length','description','notnull','iskey'])
#df_pglog.to_excel(r"./log/源数据.xlsx")
df_pglog.mergewr_excel_output(r'./log/表结构信息.xlsx','表结构信息',['relname'],['relname','comment'])

#生成ureport报表
da1=pgcore.ExcSQL_DataFrame(sql_structure)
for df1 , df2 in da1.groupby([0],as_index=True):
    #日志打印
    print("------df1------------")
    print(df1)
    print("-------df2-----------")
    print(df2)
    df2.columns = ['relname','comment','field','type_length','description','notnull','iskey']
    rt_condition = {}
    rt_condition_item = ReportInfoItems("none","","","","")
    print(type(df1))
    if df1 in rts_condition_info.keys():
       rt_condition_item = rts_condition_info[df1]
    # 首先告诉Jinja2模块，jinja模板文件路径在哪？(如当前目录)
    j2_loader = FileSystemLoader('./template')
    # 然后定义一个环境，告诉jinja2，从哪里调用模板
    env = Environment(loader=j2_loader)
    # 之后通过 get_template 获取并载入模板
    j2_tmpl = env.get_template('./template.ureport.xml')
    # 最后传入参数，渲染模板
    result = j2_tmpl.render(name="LY",host=PGinfo.db_host,port=PGinfo.db_port,database=PGinfo.db_database,password=PGinfo.db_password,tablename=df1,tableColInfoDataFrame=df2,rts_condition_info = rt_condition_item,sql="sql")
    filename = "report/" + str(df1) +".xml"
    f = open(filename,'w',encoding="utf-8")
    f.write(result) #将字符串写入文件中
    print("------------------")
print(result)
#print(da1.shape[1])