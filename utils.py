import csv
import re
from urllib.request import urlretrieve
from datetime import date
import os
from apscheduler.schedulers.background import BackgroundScheduler


fileName = 'tecaj_{}.txt'.format(date.today())
fileNameCSV = 'tecaj_{}.csv'.format(date.today())
url = 'http://www.ljse.si/datoteke/BTStecajEUR.txt'

def getSymbols(file_name):
    list = ['SBITOP']
    with open(file_name) as file:
        for line in file:
            if line[1:5].lstrip().rstrip() == '0020':
                list.append(line[16:24].rstrip().lstrip())
    return list

def saveFile(url, file_name):
    return urlretrieve(url, file_name)

def getContent(file_name):
    with open(file_name) as file:
        content = file.read()
    file.close()
    return content

def makeDict(file_name):
    dict = {}
    date = ''
    with open(file_name) as file:
        for line in file:
            code = line[1:5].lstrip().rstrip()
            if code == '0002':
                date = line[6:16].rstrip().lstrip()
            if code == '0010':
                symbol = line[6:14].lstrip().rstrip()
                value = line[56:71].lstrip().rstrip().replace(',', '.')
                dict[symbol] = {
                    'Simbol' : symbol,
                    'Datum' : date,
                    'Vrednost indeksa' : value
                }
            if code == '0020':
                symbol = line[16:24].lstrip().rstrip()
                dict[symbol] = {'Simbol' : symbol, 'Datum' : date}
                max_price = line[205:220].lstrip().rstrip().replace(',', '.')
                dict[symbol]['Najvisji tecaj'] = max_price
                min_price = line[221:236].lstrip().rstrip().replace(',', '.')
                dict[symbol]['Najnizji tecaj'] = min_price
                open_price = line[237:252].lstrip().rstrip().replace(',', '.')
                dict[symbol]['Otvoritveni tecaj'] = open_price
                close_price = line[253:268].lstrip().rstrip().replace(',', '.')
                dict[symbol]['Uradni tecaj'] = close_price
    file.close()
    return dict


def makeCSV(dictionary, file_name, symbol):
    if symbol == 'SBITOP':
        fields = ['Simbol', 'Datum', 'Vrednost indeksa']
    else:
        fields = ['Simbol',
                  'Datum',
                  'Otvoritveni tecaj',
                  'Najvisji tecaj',
                  'Najnizji tecaj',
                  'Uradni tecaj']

        if os.path.isfile(file_name):
            with open(file_name, 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fields, extrasaction='ignore')
                writer.writerow(dictionary[symbol])
            csv_file.close()
        else:
            with open(file_name, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fields, extrasaction='ignore')
                writer.writeheader()
                writer.writerow(dictionary[symbol])
            csv_file.close


def get_history():
    symbols = getSymbols('tecaj_2016-09-10.txt')
    for symbol in symbols:
        file_name = '{}_history.txt'.format(symbol)
        symbol_url = 'http://www.ljse.si/cgi-bin/jve.cgi?doc=1298&date1=12.09.2015&date2=12.09.2016&SecurityId={}&IndexOrSecurity=%24SBITOP&x=26&y=8'.format(symbol)
        saveFile(symbol_url, file_name)
        lines = []
        with open(file_name) as file:
            for line in file:
                lines.append(line.strip())
        file.close()
        string = ''.join(lines)
        with open(file_name, 'w') as file:
            file.write(string)
        file.close

def make_history_csv():
    symbols = getSymbols('tecaj_2016-09-10.txt')
    for symbol in symbols:
        if symbol == 'SBITOP':
            fields = ['Simbol', 'Datum', 'Vrednost indeksa']
            file_name = 'ADM2_history.txt'
            reg_ex = re.compile(r'<TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top>(?P<datum>\d{2}.\d{2}.\d{4})</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<tocke>\d*,*\d*-*)</TD>')
        else:
            fields = ['Simbol',
                      'Datum',
                      'Otvoritveni tecaj',
                      'Najvisji tecaj',
                      'Najnizji tecaj',
                      'Uradni tecaj']
            file_name = '{}_history.txt'.format(symbol)
            reg_ex = re.compile(r'<TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top>(?P<datum>\d{2}.\d{2}.\d{4})</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<odpiralni_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<najvisji_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<najnizji_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<uradni_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<promet>\d*,*\d*-*)</TD>')
        for match in re.finditer(reg_ex, getContent(file_name)):
            dict = {'Simbol': symbol, 'Datum': match.groupdict()['datum']}
            if symbol == 'SBITOP':
                dict['Vrednost indeksa'] = match.groupdict()['tocke'].replace(',', '.')
            else:
                dict['Otvoritveni tecaj'] = match.groupdict()['odpiralni_tecaj'].replace(',', '.')
                dict['Najvisji tecaj'] = match.groupdict()['najvisji_tecaj'].replace(',', '.')
                dict['Najnizji tecaj'] = match.groupdict()['najnizji_tecaj'].replace(',', '.')
                dict['Uradni tecaj'] = match.groupdict()['uradni_tecaj'].replace(',', '.')
            if not os.path.isfile('{}.csv'.format(symbol)):
                with open('{}.csv'.format(symbol), 'w') as csv_file:
                    writer = csv.DictWriter(csv_file, fields)
                    writer.writeheader()
                    writer.writerow(dict)
                csv_file.close()
            else:
                with open('{}.csv'.format(symbol), 'a') as csv_file:
                    writer = csv.DictWriter(csv_file, fields)
                    writer.writerow(dict)
                csv_file.close()


def job_function():
    saveFile(url, fileName)
    dict = makeDict(fileName)
    for symbol in getSymbols(fileName):
        file_name = '{}.csv'.format(symbol)
        makeCSV(dict, file_name, symbol)


# scheduler = BackgroundScheduler()
# scheduler.add_job(job_function, trigger='cron', hour='17')
# scheduler.start()




