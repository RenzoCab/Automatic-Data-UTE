#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests #https://curl.trillworks.com/#python
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import csv

# Author: Renzo Caballero
# KAUST: King Abdullah University of Science and Technology
# email: renzo.caballerorosas@kaust.edu.sa caballerorenzo@hotmail.com
# Website: None.
# August 2019; Last revision: 20/08/2019.


# In[2]:


def Palmar_Data(Date): #https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx
    
    cookies = {
    '_ga': 'GA1.3.1896229554.1560627182',
    'ASP.NET_SessionId': 'wzwatwmdvsmesj450brgx3a1',
    }

    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://apps.ute.com.uy',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx',
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
    '__VIEWSTATE': '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b3IgQ2VudHJhbCAtIDA4LzA3LzIwMTlkZAIbDzwrAA0BAA8WBh8IZx8JAgQfB2hkFgJmD2QWCgIBD2QWCmYPDxYCHwEFDkMuIEguIEcuIFRlcnJhZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFBiAgMC4wMGRkAgMPDxYCHwEFBTc5LDc5ZGQCBA8PFgIfAQUEMCwwMGRkAgIPZBYKZg8PFgIfAQUPQy4gSC4gQmF5Z29ycmlhZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFB0NlcnJhZG9kZAIDDw8WAh8BBQU1Myw3NGRkAgQPDxYCHwEFBDAsMDBkZAIDD2QWCmYPDxYCHwEFF0MuIEguIENvbnN0aXR1Y2kmIzI0MztuZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFB0NlcnJhZG9kZAIDDw8WAh8BBQUzOSw3MmRkAgQPDxYCHwEFBDAsMDBkZAIED2QWCmYPDxYCHwEFEUMuSC4gU2FsdG8gR3JhbmRlZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFBiZuYnNwO2RkAgMPDxYCHwEFBTM0LDExZGQCBA8PFgIfAQUEMCwwMGRkAgUPDxYCHwpoZGQCHQ8PFgIfAQUySW5mb3JtYWNpw7NuIGluZ3Jlc2FkYSBoYXN0YSBlbCAwOC8wNy8yMDE5IC0gMDk6MDBkZAIPDzwrAAkCAA8WBh4NTmV2ZXJFeHBhbmRlZGQeDFNlbGVjdGVkTm9kZWQeCUxhc3RJbmRleAIQZAgUKwARBXIxOjI0LDE6MjMsMToyMiwxOjIxLDE6MjAsMToxOSwxOjE4LDE6MTcsMToxNiwxOjE1LDE6MTQsMToxMywxOjEyLDE6MTEsMToxMCwxOjksMTo4LDE6NywxOjYsMTo1LDE6NCwxOjMsMToyLDE6MSwxOjAUKwACFgIeCEV4cGFuZGVkaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OZ2RkGAUFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRJjdGwwMCRUcmVlVmlld01haW4FK2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZFJlc1ZlcnRlZGVyb3MPPCsACgEIAgFkBSZjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGdyaWRSZXNDb3Rhcw88KwAKAQgCAWQFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZENvdGFzMQ88KwAKAQgCAWQFI2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZENvdGFzDzwrAAoBCAIBZP5POWRMZRQS0CSI1GAoJEH0Al65',
    '__VIEWSTATEGENERATOR': '5B0928BE',
    '__EVENTVALIDATION': '/wEWGgLDs+XXDQKHxLbGBQLi1N8DAoPFhowBAozR5qwKAozR4qwKAozR6qwKAs+1/OwCAtSX9IoKAsLE9owOArXX6wQC16/w+QsC5aHR7QsCquvo2wYC7Ln23AUCkZnO3wgC5r2l1QQC2vnp9QYCr8D6iQwCzteRzA8CkuC+xwoCypWFrgsCw+a7mQ8CjMSQxAMCvPz7qwYC34vKwwoSU0YcRqoM0etF4U5lAf/esqSTIA==',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date,
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboCentrales': '100001',
    'ctl00$ContentPlaceHolder1$cmdAplicar': 'Aplicar'
    }

    response = requests.post('https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx', headers=headers, cookies=cookies, data=data)

    return response


# In[3]:


Date = datetime.datetime(1999,1,1)

today = Date.today()
twoDaysAgo = today - timedelta(days=2)
stringTDA = twoDaysAgo.strftime("%d/%m/%Y")

weWrote = 1

while Date.strftime("%d/%m/%Y") != stringTDA:

    if weWrote == 1:

        with open('Palmar_Data_Horaria.csv', mode='r') as Palmar_Data_Horaria:
            Palmar_Data_Horaria = csv.reader(Palmar_Data_Horaria, delimiter=',')
            List = list(Palmar_Data_Horaria)
            lastDateString = List[-1][0] # i.e. '31/07/2019'.
            lastDate = datetime.datetime.strptime(lastDateString, '%d/%m/%Y')

        weWrote = 0
        
    if Date > lastDate:
        
        weWrote = 1

        with open('Palmar_Data_Horaria.csv', mode='a') as Palmar_Data_Horaria:
            Palmar_Data_Horaria = csv.writer(Palmar_Data_Horaria, delimiter=',')
    
            response = Palmar_Data(Date)
            error = 0;
            while response.status_code != 200:
                response = Palmar_Data(Date)
                error = error + 1
                print('Error:', error)

            response_soup = BeautifulSoup(response.content, 'html.parser')
            All_td = response_soup.find_all('td')
            List = list(All_td)

            Table15 = List[15].table
            Table64 = List[64].table

            All_td15 = Table15.find_all('td')
            All_td64 = Table64.find_all('td')

            List15 = list(All_td15) #[Date,H,h0,Delta_H]
            List64 = list(All_td64)

            L = len(List15)
            print(Date.strftime("%d/%m/%Y"))
            for i in range(0,int(L/4)):
                print(List15[i*4].string,                      List15[i*4+1].string.replace('.','').replace(',','.'),                      List15[i*4+2].string.replace('.','').replace(',','.'),                      List15[i*4+3].string.replace('.','').replace(',','.'))
                Palmar_Data_Horaria.writerow([Date.strftime("%d/%m/%Y"),                                              List15[i*4].string.replace('.','').replace(',','.'),                                              List15[i*4+1].string.replace('.','').replace(',','.'),                                              List15[i*4+2].string.replace('.','').replace(',','.'),                                              List15[i*4+3].string])
            for i in range(0,int(L/4)):
                print(List64[i*4].string,                      List64[i*4+1].string.replace('.','').replace(',','.'),                      List64[i*4+2].string.replace('.','').replace(',','.'),                      List64[i*4+3].string.replace('.','').replace(',','.'))
                Palmar_Data_Horaria.writerow([Date.strftime("%d/%m/%Y"),                                              List64[i*4].string.replace('.','').replace(',','.'),                                              List64[i*4+1].string.replace('.','').replace(',','.'),                                              List64[i*4+2].string.replace('.','').replace(',','.'),                                              List64[i*4+3].string])

    else:
        
        print(Date.strftime("%d/%m/%Y"), 'exists')
        
    Date = Date + timedelta(days=1)

