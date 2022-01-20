# UReportGenerator  
**应用描述：自动根据数据库表结构批量生成UReport报表（目前只支持pg数据库，大家可以自行增加其它数据的支持）；**  
**步骤说明：**    
1.配置PG数据信息在config.ini文件中；   
2.运行目录中的ReportGenerator.py批量生成ureport报表，报表名称为表名、表头为表描述、列头为列描述；   
3.将模板COPY到UReport模板目录中；    
![image](https://user-images.githubusercontent.com/49675412/149872221-3860133c-047d-4922-9f7d-8781f36f177c.png)  
4.浏览效果  
![image](https://user-images.githubusercontent.com/49675412/149874630-6b1790a0-915e-4f9a-9e61-e720e0f177ed.png)  
![image](https://user-images.githubusercontent.com/49675412/149875681-f6ccbad3-ca6e-4000-9ba0-97f5d58c3be6.png)  

**2022-01-20 增加了生成报表的搜索、分组合并、排序功能**  
1.配置report-config.ini    
[sources]                 # 表名称  
where=where 1=1           # where 条件  
groupby=name              # 分组合并列名称  
orderby=order by name     # 排序条件  
seach=name                # 搜索列  
2.浏览效果  
![image](https://user-images.githubusercontent.com/49675412/150301475-70a57d50-2a9f-4ca0-957e-456529e1d17c.png)



