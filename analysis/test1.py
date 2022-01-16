'''
Author: your name
Date: 2022-01-11 13:17:48
LastEditTime: 2022-01-11 21:30:45
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /my_code/Multimodal-Transformer/analysis/test1.py
'''  
from matplotlib import rcParams
import matplotlib.pyplot as plt
import re
import xlsxwriter as xw
##显示中文
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'SimSun,Times New Roman'

##读取log文件
logFile = r'/home/pc/aibot/BAS/my_code/Multimodal-Transformer/single/mosei_aoa_interattention_vonly' 
number = 34
text = ''
file = open(logFile)
train_loss = []
for line in file:
    text += line
file.close()
all_data = []
train_loss_list = re.findall("Train Loss .*[0-9]",text)
valid_loss_list = re.findall("Valid Loss .*\|",text)
test_loss_list = re.findall("Test Loss .*[0-9]",text)
accuracy_list = re.findall("Accuracy: .*[0-9]",text)
F1_score_list = re.findall("F1 score: .*[0-9]",text)
MAE_list = re.findall("MAE: .*[0-9]",text)
accuracy7_list = re.findall("mult_acc_7: .*[0-9]",text)
correlation1 = re.findall("Correlation Coefficient: .*[0-9]",text)


def functions1(data_list):
    return_list = []
    for data in data_list:
        t = data.split(" ")
        value = float(t[-1].strip())
        return_list.append(round(value,4) * 100)
    return return_list


average_data = []
data = []

for loss in train_loss_list:
    t = loss.split(" ")
    acc_float = float(t[-1].strip())
    data.append(round(acc_float,5))
else:
    for i in range(0, len(data),number):
        average_data.append(round(sum(data[i:i+number]) / number, 4) ** 100)
    all_data.append(average_data[::])
    average_data.clear()
    data.clear()

data2 = []
for loss in valid_loss_list:
    t = loss.split(" ")
    acc_float = float(t[-2].strip())
    data2.append(round(acc_float,5) * 100)
else:
    all_data.append(data2[::])
    data2.clear()


for loss in test_loss_list:
    t = loss.split(" ")
    acc_float = float(t[-1].strip())
    data.append(round(acc_float,5) * 100)
else:
    all_data.append(data[::])
    data.clear()

all_data.append(functions1(accuracy_list))
all_data.append(functions1(F1_score_list))
all_data.append(functions1(accuracy7_list))
all_data.append(functions1(MAE_list))
all_data.append(functions1(correlation1))



"""
data 数据类型为列表
excel_path: 存储路径
"""
def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['train_loss','valid_loss','test_loss','acc2','F1Score','ACC7','MAE','corr']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
      # 从第二行开始写入数据
    i = 2
    for j in range(len(data[0])):
        insertData = [data[0][j],data[1][j],data[2][j],data[3][j],data[4][j],data[5][j],data[6][j],data[7][j]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表
 
 
# "-------------数据用例-------------"

fileName = 'v_only.xlsx'
xw_toExcel(all_data, fileName)
