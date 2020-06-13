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


def Baygorria_Data(Date):
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
    '__EVENTVALIDATION': '/wEWGQKh6o32BwKHxLbGBQLi1N8DAoPFhowBAozR5qwKAozR4qwKAozR6qwKAtSX9IoKAsLE9owOArXX6wQC16/w+QsC5aHR7QsCquvo2wYC7Ln23AUCkZnO3wgC5r2l1QQC2vnp9QYCr8D6iQwCzteRzA8CkuC+xwoCypWFrgsCw+a7mQ8CjMSQxAMCvPz7qwYC34vKwwooNvW7NRQ9IqprZEPYQvGOyPiD3A==',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date,
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboCentrales': '100003',
    'ctl00$ContentPlaceHolder1$cmdAplicar': 'Aplicar'
    }

    ok = 0;
    
    while ok == 0:
        try:
            response = requests.post('https://apps.ute.com.uy/SgePublico/ConsBalanceHid.aspx', headers=headers, cookies=cookies, data=data)
            ok = 1;
            while response.status_code != 200:
                print(response.status_code)
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

file_path = './Baygorria_Data.xls'

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
        response = Baygorria_Data(date)
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

