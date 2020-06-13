#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests #https://curl.trillworks.com/#python
import os
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
from xlwt import easyxf # http://pypi.python.org/pypi/xlwt
import xlwt

# Author: Renzo Caballero
# KAUST: King Abdullah University of Science and Technology
# email: renzo.caballerorosas@kaust.edu.sa caballerorenzo@hotmail.com
# Website: None.
# August 2019; Last revision: 20/08/2019.


# In[2]:


def Palmar_Data(Date):
    cookies = {
    'ASP.NET_SessionId': 'ebrodb5503taw045sv4kdb34',
    }

    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://apps.ute.com.uy',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://apps.ute.com.uy/SgePublico/ConsBalanceHid.aspx',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    'ctl00_TreeViewMain_ExpandState': 'nnnnnnnnnnnnnnnn',
    'ctl00_TreeViewMain_SelectedNode': '',
    'ctl00_TreeViewMain_PopulateLog': '',
    '__VIEWSTATE': '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',
    '__VIEWSTATEGENERATOR': '797B1358',
    '__EVENTVALIDATION': '/wEWGQLEufTaDQKHxLbGBQLi1N8DAoPFhowBAozR5qwKAozR4qwKAozR6qwKAtSX9IoKAsLE9owOArXX6wQC16/w+QsC5aHR7QsCquvo2wYC7Ln23AUCkZnO3wgC5r2l1QQC2vnp9QYCr8D6iQwCzteRzA8CkuC+xwoCypWFrgsCw+a7mQ8CjMSQxAMCvPz7qwYC34vKwwpoqzu4utTzLMQ+fm8Ga3KziSgX1A==',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date,
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboCentrales': '100001',
    'ctl00$ContentPlaceHolder1$cmdAplicar': 'Aplicar'
    }
    
    ok = 0;
    
    while ok == 0:
        try:
            response = requests.post('https://apps.ute.com.uy/SgePublico/ConsBalanceHid.aspx', headers=headers, cookies=cookies, data=data)
            ok = 1;
            while response.status_code != 200:
                response = requests.post('https://apps.ute.com.uy/SgePublico/ConsBalanceHid.aspx', headers=headers, cookies=cookies, data=data)
        except:
            ok = 0;    
    
    return response


# In[3]:


date = datetime.datetime(2019,1,1)

today = date.today()
twoDaysAgo = today - timedelta(days=2)
stringTDA = twoDaysAgo.strftime("%d/%m/%Y")

Indexes = (19,25,31,37,43,49,55,61)
weWrote = 1

file_path = './Palmar_Data.xls'

while date.strftime("%d/%m/%Y") != stringTDA:
    
    print(date.strftime("%d/%m/%Y"))

    if weWrote == 1:

        rb = open_workbook(file_path,formatting_info=True)
        r_sheet = rb.sheet_by_index(0) # read only copy to introspect the file
        wb = copy(rb) # a writable copy (I can't read values out of this, only write to it)
        w_sheet = wb.get_sheet(0) # the sheet to write to within the writable copy
        lastRow = w_sheet.last_used_row # 0 based (subtract 1 from excel final row number).

        colDate = r_sheet.col(0)
        List = [None]*(len(colDate)-8000)
        for i in range(0,len(colDate)-8000):
            List[i] = colDate[i+8000].value
        #     print(List[i].value)

        weWrote = 0

    if not (date.strftime("%d/%m/%Y") in List):
        
        weWrote = 1
        j = 1
        response = Palmar_Data(date)
        response_soup = BeautifulSoup(response.content, 'html.parser')
        All_td = response_soup.find_all('td')
        List = list(All_td)
        print(date.strftime("%d/%m/%Y"))
        w_sheet.write(lastRow+1, 0, date.strftime("%d/%m/%Y"))
        for k in Indexes:
        
            string = List[k].string
            string = string.replace(".", "")
            string = string.replace(",", ".") # replace("A", "B") this replaces A by B in a string.
            number = float(string)
            print(number)
            
            w_sheet.write(lastRow+1, j, number)
            j = j + 1
            
        wb.save(file_path)
    
    date = date + timedelta(days=1)

