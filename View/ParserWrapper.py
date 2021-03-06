import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import csv
import datetime
from View import DBManager
#
# def clean_newline(name):
#     data = []
#     temp = None
#     with open(name) as f:
#         for line in f:
#             if line.endswith('n\n'):
#                 if temp:
#                     line = temp + line
#                     temp = None
#                 data.append(line)
#             else:
#                 temp = line
#                 temp.replace('\n', '')
#     return data
def read_from_file(filename, type):
    if type == '水泥':
        type = 0
    else:
        type = 1

    filename = filename
    data = read_from_source(filename)
    db_manager = DBManager.DatabaseManager()
    db_manager.create()
    customer_set = set()
    for i in data:
        customer_set.add(i[5])

    rowCount = 1
    for i in data:
        checkRowIntegrity(i, rowCount)
        rowCount += 1
        if i[6] == '':
            i[6] = '无'
        date = i[1].split('/')
        command = f'''INSERT INTO ORDERS VALUES (
        20{date[2]}, 
        {date[0]},
        {date[1]},
        '{i[2]}',
        '{i[3]}',
        '{i[5]}',
        {float(i[4])},
        0.0,
        '{i[6]}',
        {type})
        '''
        db_manager.execute(command)
    db_manager.commit()
    db_manager.close()

def checkRowIntegrity(rawRow, rowNum):
    # check if valid date
    try:
        format_date(rawRow[1])
    except:
        raise ValueError(f"{rowNum}行日期有误")

    try:
        float(rawRow[4])
    except:
        raise ValueError(f"{rowNum}行数量无法转换成数码")


def format_date(date_str):
    temp = str(date_str).split('/')
    temp[2] = '20' + temp[2]
    return datetime.date(int(temp[2]), int(temp[0]), int(temp[1]))


def read_from_source(name):
    data = []
    r = 0
    c = 0
    with open(name) as file:
        reader = csv.reader(file, delimiter=',')
        # print('Reading data from csv file')
        start = False
        for row in reader:
            r += 1
            if row[0] == '1':
                start = True
            if start:
                if 'END' not in row:
                    if row[len(row)-1] != 'n':
                        c = len(row)-1
                        raise ValueError(f"csv格式错误！请保证数据行最后一列是 n ，文件最后一行有 END。可能的错误位置：{r}行{c}列 \n 内容{row}")
                    else:
                        data.append(row)
    return data
