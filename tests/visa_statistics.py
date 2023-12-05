#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pdfplumber
import pandas as pd
import os
import matplotlib.pyplot as plt
dfs=pd.DataFrame()
#os.walk(file_path) 深度遍历file_path下的所有子文件夹及文件
for root_dir,sub_dir,files in os.walk(r"/Users/qq/PycharmProjects/backtrader/datas"):
    for file in files:
        if file.endswith(".xlsx"):
            #构造绝对路径
            file_name = os.path.join(root_dir, file)
            #print(file_name)
            #读取sheet页
            #pd.read_excel(file_path,sheet_name=None).keys()获取excel表格所有的sheet页名称
            #for sheet in  pd.read_excel(file_name,sheet_name=None).keys():
            #df=pd.read_excel(file_name,header=None).drop(0)[:-1]
            #print(df)
            #excel_name=file.replace(".xlsx","")
            #新增两列用于记录数据所属excel及sheet页，这一步骤感觉很有用，因为后续数据清理的时候，遇到莫名其妙的数据不知道怎么办的话，还可以去源excel表格上看下。
            #df["excel_name"]=excel_name
            #dfs=pd.concat([dfs,df])
        elif file.endswith(".pdf") and file.__contains__("Nationality"):
            file_name = os.path.join(root_dir, file)
            with pdfplumber.open(file_name) as pdf:
                for page in pdf.pages:
                    table = page.extract_tables()
                    for t in table:
                        df = pd.DataFrame(t[2:], columns=t[1])
                        #print(df)
                        excel_name = file.replace(".pdf", "")
                        df["excel_name"] = excel_name
                        dfs = pd.concat([dfs, df])
                dfs = dfs[:-1]
dfs.to_csv("/Users/qq/PycharmProjects/backtrader/datas/visa.csv")
#b = dfs[dfs[0].isin(['Beijing','Shanghai','Shenyang','Chengdu','Guangzhou'])]
b = dfs[dfs['Nationality']=='China-mainland']
c = b[b['Visa Class']=='B1/B2'].copy()
c['Month_Year'] = c['excel_name'].str.split('-').str[0].str.strip()
c['Formatted_Date']= pd.to_datetime(c['Month_Year'], format="%B %Y")

# 创建每个城市的子图
cities = c['Nationality'].unique()
# 绘制趋势图
plt.figure(figsize=(10, 6))
for city in cities:
    city_data = c[c['Nationality'] == city].sort_values(by='Formatted_Date')
    plt.plot(city_data['Formatted_Date'], city_data['Issuances'], label=city, marker='o', linestyle='-')

# 设置图形的标题和标签
plt.title('Trend Over Time for the Third Column')
plt.xlabel('Date')
plt.ylabel('Value')

# 在 x 轴上显示日期标签
plt.xticks(rotation=45)
# 添加图例
plt.legend()
# 显示图形
plt.show()

