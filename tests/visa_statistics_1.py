#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pdfplumber
import pandas as pd
import os
import matplotlib.pyplot as plt

file_name = "/Users/pingguo/PycharmProjects/backtrader/datas/visa.csv"
excel_file_name = "/Users/pingguo/PycharmProjects/backtrader/datas/visa_excel.csv"
dfs=pd.read_csv(file_name).iloc[:, 1:5].copy()
df=pd.read_csv(excel_file_name, dtype=str).iloc[:, 1:5].copy()
dfs = pd.concat([dfs,df])

b = dfs[dfs['Nationality'].isin(['China-mainland','China - mainland','China - Mainland'])]
c = b[b['Visa Class']=='B1/B2'].copy()
c['Month_Year'] = c['excel_name'].str.split('-').str[0].str.strip().str.replace('OCTOBER 2019 NIV Issuances by Nationality and Visa Class', 'OCTOBER 2019')
dateformat = ["%B %Y", "%B%Y"]
c['Formatted_Date']= pd.to_datetime(c['Month_Year'],  infer_datetime_format=True)


# 绘制趋势图
plt.figure(figsize=(10, 6))

china_data = c.sort_values(by='Formatted_Date')
china_data.to_csv("/Users/pingguo/PycharmProjects/backtrader/datas/visa_statistic.csv")
d = pd.to_numeric(china_data['Issuances'].str.replace(',', ''))
plt.plot(china_data['Formatted_Date'], pd.to_numeric(china_data['Issuances'].str.replace(',', '')), label="China", marker='o', linestyle='-')

# 设置图形的标题和标签
plt.title('Trend Over Time for the Nonimmigrant Visa')
plt.xlabel('Date')
plt.ylabel('Value')

# 在 x 轴上显示日期标签
plt.xticks(rotation=45)
# 添加图例
plt.legend()
# 显示图形
plt.show()

