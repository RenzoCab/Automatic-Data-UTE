#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests #https://curl.trillworks.com/#python
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import datetime
import csv


# In[2]:


def Salto_Grande_Data(Date): #https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx
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
    '__VIEWSTATE': '/wEPDwUKLTM4MDU5NTAxOQ9kFgJmDw8WAh4JX09wY2lvbmVzBQdFTUJBTFNFZBYCAgMPZBYGAgEPDxYCHgRUZXh0BSZOaXZlbGVzIGVuIGxhcyBQcmVzYXMgKERhdG9zIEhvcmFyaW9zKWRkAg0PZBYWAgMPPCsAEAEAFCsAAw8WAh4KUG9zdGVkRGF0ZQUKMDgvMDcvMjAxOWRkZBYEAgMPDxYCHg1BbHRlcm5hdGVUZXh0BQUgLi4uIBYEHgVzdHlsZQUqdmVydGljYWwtYWxpZ246dGV4dC1ib3R0b207Y3Vyc29yOnBvaW50ZXI7HgdvbmNsaWNrBUhDYWxlbmRhclBvcHVwX0ZpbmRDYWxlbmRhcignY3RsMDBfQ29udGVudFBsYWNlSG9sZGVyMV9GZWNoYUluaScpLlNob3coKTtkAgQPFgIeBXZhbHVlBQowMS8wMS8yMDA1ZAIHDxBkZBYBAgNkAgkPDxYCHgdFbmFibGVkZ2RkAg8PDxYCHwEFNkxhIGluZm9ybWFjacOzbiBhIGxhIGZlY2hhIHNlIGVuY3VlbnRyYSBzaW4gY29uZmlybWFyLmRkAhEPPCsADQEADxYGHgtfIURhdGFCb3VuZGceC18hSXRlbUNvdW50AgwfB2hkFgJmD2QWGgIBD2QWCGYPDxYCHwEFBDA6MDBkZAIBDw8WAh8BBQUzMyw0NmRkAgIPDxYCHwEFBDgsMDhkZAIDDw8WAh8BBQUyNSwzOGRkAgIPZBYIZg8PFgIfAQUEMTowMGRkAgEPDxYCHwEFBTMzLDQ0ZGQCAg8PFgIfAQUEOCwyMGRkAgMPDxYCHwEFBTI1LDI0ZGQCAw9kFghmDw8WAh8BBQQyOjAwZGQCAQ8PFgIfAQUFMzMsNDJkZAICDw8WAh8BBQQ3LDc2ZGQCAw8PFgIfAQUFMjUsNjZkZAIED2QWCGYPDxYCHwEFBDM6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDcsODJkZAIDDw8WAh8BBQUyNSw2MGRkAgUPZBYIZg8PFgIfAQUENDowMGRkAgEPDxYCHwEFBTMzLDM4ZGQCAg8PFgIfAQUENyw1MmRkAgMPDxYCHwEFBTI1LDg2ZGQCBg9kFghmDw8WAh8BBQQ1OjAwZGQCAQ8PFgIfAQUFMzMsMzhkZAICDw8WAh8BBQQ2LDg4ZGQCAw8PFgIfAQUFMjYsNTBkZAIHD2QWCGYPDxYCHwEFBDY6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDYsMjRkZAIDDw8WAh8BBQUyNywxOGRkAggPZBYIZg8PFgIfAQUENzowMGRkAgEPDxYCHwEFBTMzLDQwZGQCAg8PFgIfAQUENiwxMGRkAgMPDxYCHwEFBTI3LDMwZGQCCQ9kFghmDw8WAh8BBQQ4OjAwZGQCAQ8PFgIfAQUFMzMsNDBkZAICDw8WAh8BBQQ2LDAyZGQCAw8PFgIfAQUFMjcsMzhkZAIKD2QWCGYPDxYCHwEFBDk6MDBkZAIBDw8WAh8BBQUzMyw0MGRkAgIPDxYCHwEFBDYsMDJkZAIDDw8WAh8BBQUyNywzOGRkAgsPZBYIZg8PFgIfAQUFMTA6MDBkZAIBDw8WAh8BBQUzMywzOGRkAgIPDxYCHwEFBDYsMDBkZAIDDw8WAh8BBQUyNywzOGRkAgwPZBYIZg8PFgIfAQUFMTE6MDBkZAIBDw8WAh8BBQUzMywzOGRkAgIPDxYCHwEFBDYsMDBkZAIDDw8WAh8BBQUyNywzOGRkAg0PDxYCHgdWaXNpYmxlaGRkAhMPPCsADQEADxYGHwhnHwkCDB8HaGQWAmYPZBYaAgEPZBYIZg8PFgIfAQUFMTI6MDBkZAIBDw8WAh8BBQUzMyw0MGRkAgIPDxYCHwEFBDUsOThkZAIDDw8WAh8BBQUyNyw0MmRkAgIPZBYIZg8PFgIfAQUFMTM6MDBkZAIBDw8WAh8BBQUzMyw0MGRkAgIPDxYCHwEFBDUsOThkZAIDDw8WAh8BBQUyNyw0MmRkAgMPZBYIZg8PFgIfAQUFMTQ6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsOThkZAIDDw8WAh8BBQUyNyw0NGRkAgQPZBYIZg8PFgIfAQUFMTU6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsOThkZAIDDw8WAh8BBQUyNyw0NGRkAgUPZBYIZg8PFgIfAQUFMTY6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsNjhkZAIDDw8WAh8BBQUyNyw3NGRkAgYPZBYIZg8PFgIfAQUFMTc6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsNjRkZAIDDw8WAh8BBQUyNyw3OGRkAgcPZBYIZg8PFgIfAQUFMTg6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsNjRkZAIDDw8WAh8BBQUyNyw3OGRkAggPZBYIZg8PFgIfAQUFMTk6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsNjRkZAIDDw8WAh8BBQUyNyw3OGRkAgkPZBYIZg8PFgIfAQUFMjA6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDUsNjRkZAIDDw8WAh8BBQUyNyw3OGRkAgoPZBYIZg8PFgIfAQUFMjE6MDBkZAIBDw8WAh8BBQUzMyw0MGRkAgIPDxYCHwEFBDUsOTRkZAIDDw8WAh8BBQUyNyw0NmRkAgsPZBYIZg8PFgIfAQUFMjI6MDBkZAIBDw8WAh8BBQUzMyw0MmRkAgIPDxYCHwEFBDcsMDBkZAIDDw8WAh8BBQUyNiw0MmRkAgwPZBYIZg8PFgIfAQUFMjM6MDBkZAIBDw8WAh8BBQUzMywzOGRkAgIPDxYCHwEFBDcsMDRkZAIDDw8WAh8BBQUyNiwzNGRkAg0PDxYCHwpoZGQCFQ8PFgIfAQUxVmFsb3JlcyBhY3R1YWxlcyAtIENvdGFzIHBvciBDZW50cmFsIC0gMDgvMDcvMjAxOWRkAhcPPCsADQEADxYGHwhnHwkCBB8HaGQWAmYPZBYKAgEPZBYGZg8PFgIfAQUOQy4gSC4gRy4gVGVycmFkZAIBDw8WAh8BBQU3OSw3OWRkAgIPDxYCHwEFBTU0LDY2ZGQCAg9kFgZmDw8WAh8BBQ9DLiBILiBCYXlnb3JyaWFkZAIBDw8WAh8BBQU1Myw3MGRkAgIPDxYCHwEFBTQwLDA2ZGQCAw9kFgZmDw8WAh8BBRdDLiBILiBDb25zdGl0dWNpJiMyNDM7bmRkAgEPDxYCHwEFBTM5LDY2ZGQCAg8PFgIfAQUEOSwzNGRkAgQPZBYGZg8PFgIfAQURQy5ILiBTYWx0byBHcmFuZGVkZAIBDw8WAh8BBQUzNCwxN2RkAgIPDxYCHwEFBDcsMjRkZAIFDw8WAh8KaGRkAhkPDxYCHwEFLkVzdGFkb3MgZGUgVmVydGVkZXJvcyBwb3IgQ2VudHJhbCAtIDA4LzA3LzIwMTlkZAIbDzwrAA0BAA8WBh8IZx8JAgQfB2hkFgJmD2QWCgIBD2QWCmYPDxYCHwEFDkMuIEguIEcuIFRlcnJhZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFBiAgMC4wMGRkAgMPDxYCHwEFBTc5LDc5ZGQCBA8PFgIfAQUEMCwwMGRkAgIPZBYKZg8PFgIfAQUPQy4gSC4gQmF5Z29ycmlhZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFB0NlcnJhZG9kZAIDDw8WAh8BBQU1Myw3NGRkAgQPDxYCHwEFBDAsMDBkZAIDD2QWCmYPDxYCHwEFF0MuIEguIENvbnN0aXR1Y2kmIzI0MztuZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFB0NlcnJhZG9kZAIDDw8WAh8BBQUzOSw3MmRkAgQPDxYCHwEFBDAsMDBkZAIED2QWCmYPDxYCHwEFEUMuSC4gU2FsdG8gR3JhbmRlZGQCAQ8PFgIfAQUEMDowMGRkAgIPDxYCHwEFBiZuYnNwO2RkAgMPDxYCHwEFBTM0LDExZGQCBA8PFgIfAQUEMCwwMGRkAgUPDxYCHwpoZGQCHQ8PFgIfAQUySW5mb3JtYWNpw7NuIGluZ3Jlc2FkYSBoYXN0YSBlbCAwOC8wNy8yMDE5IC0gMDk6MDBkZAIPDzwrAAkCAA8WBh4NTmV2ZXJFeHBhbmRlZGQeDFNlbGVjdGVkTm9kZWQeCUxhc3RJbmRleAIQZAgUKwARBXIxOjI0LDE6MjMsMToyMiwxOjIxLDE6MjAsMToxOSwxOjE4LDE6MTcsMToxNiwxOjE1LDE6MTQsMToxMywxOjEyLDE6MTEsMToxMCwxOjksMTo4LDE6NywxOjYsMTo1LDE6NCwxOjMsMToyLDE6MSwxOjAUKwACFgIeCEV4cGFuZGVkaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OZ2RkGAUFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRJjdGwwMCRUcmVlVmlld01haW4FK2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZFJlc1ZlcnRlZGVyb3MPPCsACgEIAgFkBSZjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGdyaWRSZXNDb3Rhcw88KwAKAQgCAWQFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZENvdGFzMQ88KwAKAQgCAWQFI2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZENvdGFzDzwrAAoBCAIBZB9yDge6+uiDyua6wGuCOOYvjcqU',
    '__VIEWSTATEGENERATOR': '5B0928BE',
    '__EVENTVALIDATION': '/wEWGgL5uIGOAgKHxLbGBQLi1N8DAoPFhowBAozR5qwKAozR4qwKAozR6qwKAs+1/OwCAtSX9IoKAsLE9owOArXX6wQC16/w+QsC5aHR7QsCquvo2wYC7Ln23AUCkZnO3wgC5r2l1QQC2vnp9QYCr8D6iQwCzteRzA8CkuC+xwoCypWFrgsCw+a7mQ8CjMSQxAMCvPz7qwYC34vKwwq0aDz3GMk5FfP8u8Uhp3j4p05fRw==',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date,
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboCentrales': '2465501',
    'ctl00$ContentPlaceHolder1$cmdAplicar': 'Aplicar'
    }

    ok = 0;
    
    while ok == 0:
        try:
            response = requests.post('https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx', headers=headers, cookies=cookies, data=data)
            ok = 1;
            while response.status_code != 200:
                response = requests.post('https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx', headers=headers, cookies=cookies, data=data)
        except:
            ok = 0; 
    
    return response


# In[3]:


Date = datetime.datetime(1999,1,1)
today = Date.today()
twoDaysAgo = today - timedelta(days=2)
stringTDA = twoDaysAgo.strftime("%d/%m/%Y")
weWrote = 1

while Date.strftime("%d/%m/%Y") != stringTDA:

    if weWrote == 1:

        with open('Salto_Grande_Data_Horaria.csv', mode='r') as Salto_Grande_Data_Horaria:
            Salto_Grande_Data_Horaria = csv.reader(Salto_Grande_Data_Horaria, delimiter=',')
            List = list(Salto_Grande_Data_Horaria)
            lastDateString = List[-1][0] # i.e. '31/07/2019'.
            lastDate = datetime.datetime.strptime(lastDateString, '%d/%m/%Y')

        weWrote = 0

    if Date > lastDate:
        
        weWrote = 1

        with open('Salto_Grande_Data_Horaria.csv', mode='a') as Salto_Grande_Data_Horaria:
            Salto_Grande_Data_Horaria = csv.writer(Salto_Grande_Data_Horaria, delimiter=',')

            response = Salto_Grande_Data(Date)
            error = 0;
            while response.status_code != 200:
                response = Salto_Grande_Data(Date)
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

            # The first list is from 00:00 to 11:00.
            # The second list is from 12:00 to 23:00.

            L = len(List15)
            print(Date.strftime("%d/%m/%Y"))
            for i in range(0,int(L/4)):
                print(List15[i*4].string,                      List15[i*4+1].string.replace('.','').replace(',','.'),                      List15[i*4+2].string.replace('.','').replace(',','.'),                      List15[i*4+3].string.replace('.','').replace(',','.'))

                date = Date.strftime("%d/%m/%Y") # Fecha.
                data_1 = List15[i*4].string # Hora.
                data_2 = List15[i*4+1].string.replace('.','').replace(',','.') # Aguas arriba.
                data_3 = List15[i*4+2].string.replace('.','').replace(',','.') # Aguas abajo.
                data_4 = List15[i*4+3].string.replace('.','').replace(',','.') # Salto.

                try:
                    float(data_2)
                except:
                    data_2 = 0
                try:
                    float(data_3)
                except:
                    data_3 = 0
                try:
                    float(data_4)
                except:
                    data_4 = 0

                Salto_Grande_Data_Horaria.writerow([date,                                              data_1,                                              data_2,                                              data_3,                                              data_4])

            for i in range(0,int(L/4)):
                print(List64[i*4].string,                      List64[i*4+1].string.replace('.','').replace(',','.'),                      List64[i*4+2].string.replace('.','').replace(',','.'),                      List64[i*4+3].string.replace('.','').replace(',','.'))

                data_1 = List64[i*4].string # Hora.
                data_2 = List64[i*4+1].string.replace('.','').replace(',','.') # Aguas arriba.
                data_3 = List64[i*4+2].string.replace('.','').replace(',','.') # Aguas abajo.
                data_4 = List64[i*4+3].string.replace('.','').replace(',','.') # Salto.

                try:
                    float(data_2)
                except:
                    data_2 = 0
                try:
                    float(data_3)
                except:
                    data_3 = 0
                try:
                    float(data_4)
                except:
                    data_4 = 0

                Salto_Grande_Data_Horaria.writerow([Date.strftime("%d/%m/%Y"),                                              data_1,                                              data_2,                                              data_3,                                              data_4])
                
    else:
        
        print(Date.strftime("%d/%m/%Y"), 'exists')

    Date = Date + timedelta(days=1)

