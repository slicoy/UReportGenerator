# -*- coding: utf-8 -*-
"""
Created on 20170301
@author: ARK-Z

revise on 20220116
@author:Liuy
Version:1.2
Description:可合并列的DataFrame

"""
import xlsxwriter
import pandas as pd
 
class SupperDataFrame(pd.DataFrame):
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        pd.DataFrame.__init__(self, data, index, columns, dtype, copy)
 
    def mergewr_excel_output(self,path,worksheet_name,key_cols=[],merge_cols=[]):
        # sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True):
        print("----------------------")
        
        self_copy=SupperDataFrame(self,copy=True)
        line_cn=self_copy.index.size
        cols=list(self_copy.columns.values)
        if all([v in cols for i,v in enumerate(key_cols)])==False:     #校验key_cols中各元素 是否都包含与对象的列
            print("key_cols is not completely include object's columns")
            return False
        if all([v in cols for i,v in enumerate(merge_cols)])==False:  #校验merge_cols中各元素 是否都包含与对象的列
            print("merge_cols is not completely include object's columns")
            return False    
        
        wb2007 = xlsxwriter.Workbook(path)
        worksheet2007 = wb2007.add_worksheet(worksheet_name)
        #展现格式修改
        format_top = wb2007.add_format({'border':1,'bold':True,'text_wrap':True,'valign':'vcenter','align':'center'})
        format_top.set_bg_color('#F6F6F6')
        format_top.set_border_color('#CCCCCC')
        worksheet2007.set_row(0,25)#设置首行行高40
        worksheet2007.set_column(0,len(cols),20)#设置所有列宽40
        format_other = wb2007.add_format({'border':1,'valign':'vcenter','align':'center'})
        #format_other.cell_format()#文本自动换行
        format_other.set_border(3)
        format_other.set_border_color('#CCCCCC')
        worksheet2007.autofilter(0, 0, self_copy.shape[0], self_copy.shape[1]-1) #给excel列加到自动筛选功能
 
        for i,value in enumerate(cols):  #写表头
            #print(value)
            worksheet2007.write(0,i,value,format_top)
        
        #merge_cols=['B','A','C']
        #key_cols=['A','B']

        if key_cols ==[]:   #如果key_cols 参数不传值，则无需合并
            self_copy['RN']=1
            self_copy['CN']=1
            print("rn = 1")
        else:
            
            self_copy['RN']=self_copy.groupby(key_cols,as_index=False).rank(method='first',na_option="top").iloc[:,0] #以key_cols作为是否合并的依据
            
            #self_copy.groupby(key_cols,as_index=False).rank(method='first').to_excel(r"E:\202009\源数据\0005.xlsx")
            self_copy['CN']=self_copy.groupby(key_cols,as_index=False).rank(method='max',na_option="top").iloc[:,0]
        print("--------self_copy----------")
        print(self_copy)
        print("-------groupby---rank(method='first')-----------")
        print(self_copy.groupby(key_cols,as_index=False).rank(method='first'))
        print("-------groupby---rank(method='first')---iloc[:,0]-----")
        print(self_copy.groupby(key_cols,as_index=False,).rank(method='first').iloc[:,0])
        #self_copy.to_excel(r"./log/排序过程数据.xlsx")
        
        for i in range(line_cn):
            if self_copy.loc[i,'CN']>1:
                #print('该行有需要合并的单元格')
                for j,col in enumerate(cols):
                    #print(self_copy.loc[i,col])
                    if col in (merge_cols):   #哪些列需要合并
                        if self_copy.loc[i,'RN']==1:  #合并写第一个单元格，下一个第一个将不再写
                            worksheet2007.merge_range(i+1,j,i+int(self_copy.loc[i,'CN']),j, self_copy.loc[i,col],format_other) ##合并单元格，根据LINE_SET[7]判断需要合并几个
                            #worksheet2007.write(i+1,j,df.loc[i,col])
                            print("合并单元格---")
                            print(i)
                            print(col)
                        else:
                            pass
                        #worksheet2007.write(i+1,j,df.loc[i,j])
                    else:
                        worksheet2007.write(i+1,j,self_copy.loc[i,col],format_other)
                    #print(',')
            else:
                #print('该行无需要合并的单元格')
                for j,col in enumerate(cols):
                    #print(df.loc[i,col])
                    worksheet2007.write(i+1,j,self_copy.loc[i,col],format_other)
                
                
        wb2007.close()
        self_copy.drop('CN', axis=1)
        self_copy.drop('RN', axis=1)
        return self_copy #返回数据集
        