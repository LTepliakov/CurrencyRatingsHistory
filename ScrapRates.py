from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import re

import pandas as pd
pd.options.display.width = 0

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op,service=ChromeService(ChromeDriverManager().install()))
#driver = webdriver.Chrome(options=op)

#driver.get("https://www.prior.by/web/")
#innerHTML = driver.execute_script("return document.body.innerHTML")


file = open("inner.html", "r")
innerHTML = file.read()
file.close()

df = pd.DataFrame(columns=['client_currency_code',\
                           'bank_currency_code',\
                           'operation_place',\
                           'operation_code',\
                           'currency_buy_rate',\
                           'buy_rate_coefficient',\
                           'currency_sell_rate',\
                           'sell_rate_coefficient',\
                           'low_limit',\
                           'high_limit',\
                           'valid_from_datetime'])  

soup_page = BeautifulSoup(innerHTML, "lxml")

body=soup_page.find('div', class_='currency_rate')

tabarea=body.find('div',class_="tabs_area")

tabs=tabarea.findAll('div',recursive=False)

time_mask=re.compile('([0-9][0-9]):([0-9][0-9]) ([0-9][0-9])\.([0-9][0-9])\.([0-9][0-9][0-9][0-9]).*')
currency_mask=re.compile('([A-Z][A-Z][A-Z])/([A-Z][A-Z][A-Z].*)')
low_limit_mask=re.compile(r'.*от ([\d\ ]+)')
high_limit_mask=re.compile(r'.*до ([\d\ ]+)')
#coeff_mask=re.compile(.*(\([0-9]+\)))

def totime(tag_line):
    m=time_mask.match(tag_line.strip())
    return m.group(5)+'-'+m.group(4)+'-'+m.group(3)+'T'+m.group(1)+':'+m.group(2)+':00+03:00'

for t in tabs:
#    print (t.attrs['class'])
    operation_place=t.attrs['class'][1].replace('curr','')
    print ("Rate kind: ",operation_place)
#    operation_code=t.attrs['class'][1].replace('curr','')
    operation_code=t.attrs['class'][1].replace('curr','')
    op_code=operation_place
    if operation_place in ['Card','Online']:
        low_limit=0
        high_limit=None
        print('h3: ',t.div.div.h3.attrs['data-time'].replace('Действуют с ',''))
        valid_from_datetime = totime(t.div.div.h3.attrs['data-time'].replace('Действуют с ',''))
        tabs1=t.div.div.findAll('div',recursive=False)
        for t1 in tabs1:
#            print ('t1: ', t1)
            operation_code=t1.attrs['id'].replace('currRates','').replace('Card','').replace('Online','')
            print ("Operation kind: ",operation_code)
            table_rows=t1.table.tbody.findAll('tr',recursive=False)
#            print(t.table.h3.attrs['data-time'])
            row_no=0
            for r in table_rows:
                row_list=[]
                print('row',row_no,end="")
                if row_no==0:
                    print(r.attrs['class'])
                row_cells=r.findAll('td',recursive=False)    
                cell_no=0
                for c in row_cells:
                    if row_no==0:
                        row_list.append(c.text)
                    else:
                        if operation_code=='Exc':
                            if cell_no==0:
                                row_list.append(c.span.text)
                            else:
                                row_list.append(c.div.div.text)
                        elif operation_code=='Conv':
                            if cell_no==0:
                                row_list.append(c.text)
                            else:
                                row_list.append(c.div.text.strip())
                    cell_no=cell_no+1  
#                print("Row list: ",row_list)
                for i in row_list:
                    print('\t',i,end="")
                print()
                if operation_code=='Exc':
                    client_currency_code='BYN'
 #               elif operation_code=='Conv':
 #                   m=currency_mask.match(row_list[0])
 #                   client_currency_code=m.group(1)
 #                   bank_currency_code=m.group(2)

                if row_no>0: # Skipping table header

                    if operation_code=='Conv':
                        m=currency_mask.match(row_list[0])
                        client_currency_code=m.group(1)
                        bank_currency_code=m.group(2)

                    buy_rate_coefficient=1
                    sell_rate_coefficient=1
                    currency_buy_rate=row_list[1]
                    currency_sell_rate=row_list[2]
                    if bank_currency_code=='RUB':
                        if operation_code=='Exc':
                            sell_rate_coefficient=100
                            buy_rate_coefficient=100
 
                        currency_sell_rate=re.sub(r'\(.*\)','',currency_sell_rate)
                        currency_buy_rate=re.sub(r'\(.*\)','',currency_buy_rate)
 
                    print('*** ',client_currency_code,bank_currency_code,operation_place,operation_code,currency_buy_rate,buy_rate_coefficient, currency_sell_rate,sell_rate_coefficient,low_limit,high_limit,valid_from_datetime)
                    new_row={'client_currency_code':client_currency_code,\
                           'bank_currency_code':bank_currency_code,\
                           'operation_place':operation_place,\
                           'operation_code':operation_code,\
                           'currency_buy_rate':currency_buy_rate,\
                           'buy_rate_coefficient':buy_rate_coefficient,\
                           'currency_sell_rate':currency_sell_rate,\
                           'sell_rate_coefficient':sell_rate_coefficient,\
                           'low_limit':low_limit,\
                           'high_limit':high_limit,\
                           'valid_from_datetime':valid_from_datetime}
                    df = df._append(new_row, ignore_index=True)

                client_currency_code='---'
                row_no=row_no+1
    else:
#        print('***2',t.div.div.table.attrs['class'])
#        print('***3',t.div.div.attrs['id'])
        currencies=t.div.findAll('div',recursive=False)
        for crns in currencies:
#            print("currency:",crns)
            print ('***1',crns.attrs['id'].replace('curr',''))
            client_currency_code='BYN'
            cash_operration_code=crns.attrs['id'].replace('curr','')
            if cash_operration_code[0:5] == 'Rates':
                bank_currency_code=cash_operration_code[5:].upper()
                operation_code='Exc'
            else:
                operation_code='Conv'

            print('h3: ',crns.h3.attrs['data-time'].replace('Действуют с ',''))
            valid_from_datetime =totime(crns.h3.attrs['data-time'].replace('Действуют с ',''))
            table_rows=crns.table.tbody.findAll('tr',recursive=False)
            row_no=0
            for r in table_rows:
                low_limit=0
                high_limit=None
 #               client_currency_code='---'
 #               bank_currency_code='---'
                row_list=[]
                print('row',row_no,end='') #,r)
                if row_no==0:
                    print(r.attrs['class'])
                row_cells=r.findAll('td',recursive=False)    
                cell_no=0
                for c in row_cells:
#                    print('row_no=',row_no,'cell_no=',cell_no,'Cell=',c)
                    if row_no==0:
                        row_list.append(c.text)
                    else:
#                        if operation_code=='Exc':
                        if cell_no==0:
                            row_list.append(c.text.strip())
                        else:
                            row_list.append(c.div.text.strip())
                    cell_no=cell_no+1  
#                print("Row list: ",row_list)
                for i in row_list:
                    print('\t',i,end="")
                print()
               
                if row_no>0:  # Skipping table header
                    if operation_code=='Conv':
                        m=currency_mask.match(row_list[0])
                        client_currency_code=m.group(1)
                        bank_currency_code=m.group(2)
                    else:
                        m=low_limit_mask.match(row_list[0])
                        low_limit=m.group(1).replace(' ','') if m else 0
                        m=high_limit_mask.match(row_list[0])
                        high_limit=m.group(1).replace(' ','') if m else None

                    buy_rate_coefficient=1
                    sell_rate_coefficient=1
                    currency_buy_rate=row_list[1]
                    currency_sell_rate=row_list[2]

                    if bank_currency_code=='RUB':
                        if operation_code=='Exc':
                            sell_rate_coefficient=100
                            buy_rate_coefficient=100
                        currency_sell_rate=re.sub(r'\(.*\)','',currency_sell_rate)
                        currency_buy_rate=re.sub(r'\(.*\)','',currency_buy_rate)
  
                    print('*** ',client_currency_code,bank_currency_code,operation_place,operation_code, currency_buy_rate, buy_rate_coefficient,currency_sell_rate,sell_rate_coefficient,low_limit,high_limit,valid_from_datetime)
                    new_row={'client_currency_code':client_currency_code,\
                           'bank_currency_code':bank_currency_code,\
                           'operation_place':operation_place,\
                           'operation_code':operation_code,\
                           'currency_buy_rate':currency_buy_rate,\
                           'buy_rate_coefficient':buy_rate_coefficient,\
                           'currency_sell_rate':currency_sell_rate,\
                           'sell_rate_coefficient':sell_rate_coefficient,\
                           'low_limit':low_limit,\
                           'high_limit':high_limit,\
                           'valid_from_datetime':valid_from_datetime}
                    df = df._append(new_row, ignore_index=True)    
                row_no=row_no+1
    
print(df)
                

df.to_pickle("CurrencyRates.pkl") 