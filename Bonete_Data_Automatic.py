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


def Bonete_Data(Date):
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
    '__VIEWSTATE': '/wEPDwUKMTcxODcyOTgzMA9kFgJmDw8WAh4JX09wY2lvbmVzBQdFTUJBTFNFZBYCAgMPZBYGAgEPDxYCHgRUZXh0BRNCYWxhbmNlIEhpZHLDoXVsaWNvZGQCDQ9kFhYCAw88KwAQAQAUKwADDxYCHgpQb3N0ZWREYXRlBQowNS8wNy8yMDE5ZGRkFgQCAw8PFgIeDUFsdGVybmF0ZVRleHQFBSAuLi4gFgQeBXN0eWxlBSp2ZXJ0aWNhbC1hbGlnbjp0ZXh0LWJvdHRvbTtjdXJzb3I6cG9pbnRlcjseB29uY2xpY2sFSENhbGVuZGFyUG9wdXBfRmluZENhbGVuZGFyKCdjdGwwMF9Db250ZW50UGxhY2VIb2xkZXIxX0ZlY2hhSW5pJykuU2hvdygpO2QCBA8WAh4FdmFsdWUFCjE4LzA2LzIwMTlkAgcPEGRkFgFmZAIJDw8WAh4HRW5hYmxlZGdkZAINDw8WAh4MRXJyb3JNZXNzYWdlBSpMYSBGZWNoYSBkZWJlIHNlciBtZW5vciBhIGxhIGZlY2hhIGRlIGhveS5kZAIPDw8WAh8BBTNMYSBpbmZvcm1hY2nDs24gYSBsYSBmZWNoYSBzZSBlbmN1ZW50cmEgY29uZmlybWFkYS5kZAIRDzwrAA0BAA8WBh4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudAIIHwdoZBYCZg9kFhICAQ9kFghmDw8WAh8BBQQyMDE5ZGQCAQ8PFgIfAQUEMjAxOGRkAgIPDxYCHwEFBDIwMTlkZAIDDw8WAh8BBQQyMDE4ZGQCAg9kFgxmDw8WAh8BBRlWb2x1bWVuIEluaWNpYWwgRW1iYWxzYWRvZGQCAQ8PFgIfAQUINy43NDAsMDBkZAICDw8WAh8BBQg2LjIxMiwwMGRkAgMPDxYCHwEFCDMuODMxLDAwZGQCBA8PFgIfAQUIOC42NTIsMDBkZAIFDw8WAh8BBQg3LjE0MywwMGRkAgMPZBYMZg8PFgIfAQUXVm9sdW1lbiBGaW5hbCBFbWJhbHNhZG9kZAIBDw8WAh8BBQg3Ljk2MywwMGRkAgIPDxYCHwEFCDcuOTYzLDAwZGQCAw8PFgIfAQUINC4zOTksMDBkZAIEDw8WAh8BBQg3Ljk2MywwMGRkAgUPDxYCHwEFCDQuMzk5LDAwZGQCBA9kFgxmDw8WAh8BBQ1HYXN0byBkZSBBZ3VhZGQCAQ8PFgIfAQUFMTgsMzZkZAICDw8WAh8BBQYxNDMsODVkZAIDDw8WAh8BBQY5MzMsMDZkZAIEDw8WAh8BBQkxMC43NTcsODJkZAIFDw8WAh8BBQg2LjI4MiwwNWRkAgUPZBYMZg8PFgIfAQUVICAgIFZvbHVtZW4gVHVyYmluYWRvZGQCAQ8PFgIfAQUFMTYsMjBkZAICDw8WAh8BBQYxMDQsNDFkZAIDDw8WAh8BBQY5MDEsNzBkZAIEDw8WAh8BBQg2LjU5MSw5MWRkAgUPDxYCHwEFCDUuNjIyLDY5ZGQCBg9kFgxmDw8WAh8BBRMgICAgVm9sdW1lbiBWZXJ0aWRvZGQCAQ8PFgIfAQUEMCwwMGRkAgIPDxYCHwEFBDAsMDBkZAIDDw8WAh8BBQQwLDAwZGQCBA8PFgIfAQUIMy4yNTgsNTdkZAIFDw8WAh8BBQQwLDAwZGQCBw9kFgxmDw8WAh8BBRQgICAgVm9sdW1lbiBGaWx0cmFkb2RkAgEPDxYCHwEFBDAsNzVkZAICDw8WAh8BBQUxNCwzNWRkAgMPDxYCHwEFBTEzLDA3ZGQCBA8PFgIfAQUGMTI1LDY0ZGQCBQ8PFgIfAQUGMTEyLDQ1ZGQCCA9kFgxmDw8WAh8BBRUgICAgVm9sdW1lbiBFdmFwb3JhZG9kZAIBDw8WAh8BBQQxLDQyZGQCAg8PFgIfAQUFMjUsMDlkZAIDDw8WAh8BBQUxOCwyOWRkAgQPDxYCHwEFBjc4MSw3MWRkAgUPDxYCHwEFBjU0Niw5MWRkAgkPDxYCHgdWaXNpYmxlaGQWDGYPDxYCHwEFE0Fwb3J0ZSBUZSYjMjQzO3JpY29kZAIBDw8WAh8BBQYyNDEsMzNkZAICDw8WAh8BBQgxLjg5NCw1NmRkAgMPDxYCHwEFCDEuNTAwLDk2ZGQCBA8PFgIfAQUJMTAuMDY4LDgyZGQCBQ8PFgIfAQUIMy41MzgsMDVkZAITDw8WAh8BBUhBcG9ydGUgVGXDs3JpY28gUHJvbWVkaW8gQWN1bXVsYWRvIEhpc3TDs3JpY28gZGVzZGUgMTk5NCA9ICA5LjA5Niw0OSBobTNkZAIbDw8WAh8BBQYxODcsNTBkZAIhDw8WAh8BBQQwLDAwZGQCJw8PFgIfAQUIMi43OTMsMTdkZAIpDw8WAh8BBT9EZSBhY3VlcmRvIGNvbiBFVC1CT04tT1AtMDAwMywgRVQtQkFZLU9QLTAwMDMsIHkgRVQtUEFMLU9QLTAwMDNkZAIPDzwrAAkCAA8WBh4NTmV2ZXJFeHBhbmRlZGQeDFNlbGVjdGVkTm9kZWQeCUxhc3RJbmRleAIQZAgUKwARBXIxOjI0LDE6MjMsMToyMiwxOjIxLDE6MjAsMToxOSwxOjE4LDE6MTcsMToxNiwxOjE1LDE6MTQsMToxMywxOjEyLDE6MTEsMToxMCwxOjksMTo4LDE6NywxOjYsMTo1LDE6NCwxOjMsMToyLDE6MSwxOjAUKwACFgIeCEV4cGFuZGVkaGQUKwACFgIfD2hkFCsAAhYCHw9oZBQrAAIWAh8PaGQUKwACFgIfD2hkFCsAAhYCHw9oZBQrAAIWAh8PaGQUKwACFgIfD2hkFCsAAhYCHw9oZBQrAAIWAh8PaGQUKwACFgIfD2hkFCsAAhYCHw9oZBQrAAIWAh8PaGQUKwACFgIfD2hkFCsAAhYCHw9oZBQrAAIWAh8PZ2RkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRJjdGwwMCRUcmVlVmlld01haW4FImN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkR3JpZEluZm8PPCsACgEIAgFkoGr4G8hxY6398BEBV+bMCulaxKA=',
    '__VIEWSTATEGENERATOR': '797B1358',
    '__EVENTVALIDATION': '/wEWGQLtnO7zDQKHxLbGBQLi1N8DAoPFhowBAozR5qwKAozR4qwKAozR6qwKAtSX9IoKAsLE9owOArXX6wQC16/w+QsC5aHR7QsCquvo2wYC7Ln23AUCkZnO3wgC5r2l1QQC2vnp9QYCr8D6iQwCzteRzA8CkuC+xwoCypWFrgsCw+a7mQ8CjMSQxAMCvPz7qwYC34vKwwo+u3MdOysCdAiqPmRzKLnfYMLfrA==',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date,
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboCentrales': '100002',
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

file_path = './Bonete_Data.xls'

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
        response = Bonete_Data(date)
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

