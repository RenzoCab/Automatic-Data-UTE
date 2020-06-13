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


def Bonete_Data(Date): #https://apps.ute.com.uy/SgePublico/ConsNivelesPresasHoraria.aspx
    
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
    '__VIEWSTATE': '/wEPDwUKLTM4MDU5NTAxOQ9kFgJmDw8WAh4JX09wY2lvbmVzBQdFTUJBTFNFZBYCAgMPZBYGAgEPDxYCHgRUZXh0BSZOaXZlbGVzIGVuIGxhcyBQcmVzYXMgKERhdG9zIEhvcmFyaW9zKWRkAg0PZBYWAgMPPCsAEAEAFCsAAw8WAh4KUG9zdGVkRGF0ZQUKMDcvMDcvMjAxOWRkZBYEAgMPDxYCHg1BbHRlcm5hdGVUZXh0BQUgLi4uIBYEHgVzdHlsZQUqdmVydGljYWwtYWxpZ246dGV4dC1ib3R0b207Y3Vyc29yOnBvaW50ZXI7HgdvbmNsaWNrBUhDYWxlbmRhclBvcHVwX0ZpbmRDYWxlbmRhcignY3RsMDBfQ29udGVudFBsYWNlSG9sZGVyMV9GZWNoYUluaScpLlNob3coKTtkAgQPFgIeBXZhbHVlBQowMS8wMS8xOTk5ZAIHDxBkZBYBZmQCCQ8PFgIeB0VuYWJsZWRnZGQCDw8PFgIfAQUzTGEgaW5mb3JtYWNpw7NuIGEgbGEgZmVjaGEgc2UgZW5jdWVudHJhIGNvbmZpcm1hZGEuZGQCEQ88KwANAQAPFgYeC18hRGF0YUJvdW5kZx4LXyFJdGVtQ291bnQCDB8HaGQWAmYPZBYaAgEPZBYIZg8PFgIfAQUEMDowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTlkZAIDDw8WAh8BBQUxNiwzMGRkAgIPZBYIZg8PFgIfAQUEMTowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTVkZAIDDw8WAh8BBQUxNiwzNGRkAgMPZBYIZg8PFgIfAQUEMjowMGRkAgEPDxYCHwEFBTUzLDkwZGQCAg8PFgIfAQUFMzcsNTVkZAIDDw8WAh8BBQUxNiwzNWRkAgQPZBYIZg8PFgIfAQUEMzowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTBkZAIDDw8WAh8BBQUxNiwzOWRkAgUPZBYIZg8PFgIfAQUENDowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTBkZAIDDw8WAh8BBQUxNiwzOWRkAgYPZBYIZg8PFgIfAQUENTowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTJkZAIDDw8WAh8BBQUxNiwzN2RkAgcPZBYIZg8PFgIfAQUENjowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTVkZAIDDw8WAh8BBQUxNiwzNGRkAggPZBYIZg8PFgIfAQUENzowMGRkAgEPDxYCHwEFBTUzLDkyZGQCAg8PFgIfAQUFMzcsNjNkZAIDDw8WAh8BBQUxNiwyOWRkAgkPZBYIZg8PFgIfAQUEODowMGRkAgEPDxYCHwEFBTUzLDkyZGQCAg8PFgIfAQUFMzcsNjVkZAIDDw8WAh8BBQUxNiwyN2RkAgoPZBYIZg8PFgIfAQUEOTowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNjVkZAIDDw8WAh8BBQUxNiwyNGRkAgsPZBYIZg8PFgIfAQUFMTA6MDBkZAIBDw8WAh8BBQU1Myw4OWRkAgIPDxYCHwEFBTM3LDY1ZGQCAw8PFgIfAQUFMTYsMjRkZAIMD2QWCGYPDxYCHwEFBTExOjAwZGQCAQ8PFgIfAQUFNTMsODlkZAICDw8WAh8BBQUzNyw2NmRkAgMPDxYCHwEFBTE2LDIzZGQCDQ8PFgIeB1Zpc2libGVoZGQCEw88KwANAQAPFgYfCGcfCQIMHwdoZBYCZg9kFhoCAQ9kFghmDw8WAh8BBQUxMjowMGRkAgEPDxYCHwEFBTUzLDkwZGQCAg8PFgIfAQUFMzcsNTZkZAIDDw8WAh8BBQUxNiwzNGRkAgIPZBYIZg8PFgIfAQUFMTM6MDBkZAIBDw8WAh8BBQU1Myw5MGRkAgIPDxYCHwEFBTM3LDU0ZGQCAw8PFgIfAQUFMTYsMzZkZAIDD2QWCGYPDxYCHwEFBTE0OjAwZGQCAQ8PFgIfAQUFNTMsOTBkZAICDw8WAh8BBQUzNyw1NGRkAgMPDxYCHwEFBTE2LDM2ZGQCBA9kFghmDw8WAh8BBQUxNTowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNTdkZAIDDw8WAh8BBQUxNiwzMmRkAgUPZBYIZg8PFgIfAQUFMTY6MDBkZAIBDw8WAh8BBQU1Myw4OWRkAgIPDxYCHwEFBTM3LDU4ZGQCAw8PFgIfAQUFMTYsMzFkZAIGD2QWCGYPDxYCHwEFBTE3OjAwZGQCAQ8PFgIfAQUFNTMsODlkZAICDw8WAh8BBQUzNyw1OGRkAgMPDxYCHwEFBTE2LDMxZGQCBw9kFghmDw8WAh8BBQUxODowMGRkAgEPDxYCHwEFBTUzLDg5ZGQCAg8PFgIfAQUFMzcsNThkZAIDDw8WAh8BBQUxNiwzMWRkAggPZBYIZg8PFgIfAQUFMTk6MDBkZAIBDw8WAh8BBQU1Myw4OWRkAgIPDxYCHwEFBTM3LDU4ZGQCAw8PFgIfAQUFMTYsMzFkZAIJD2QWCGYPDxYCHwEFBTIwOjAwZGQCAQ8PFgIfAQUFNTMsODVkZAICDw8WAh8BBQUzNyw5MWRkAgMPDxYCHwEFBTE1LDk0ZGQCCg9kFghmDw8WAh8BBQUyMTowMGRkAgEPDxYCHwEFBTUzLDg1ZGQCAg8PFgIfAQUFMzgsNDJkZAIDDw8WAh8BBQUxNSw0M2RkAgsPZBYIZg8PFgIfAQUFMjI6MDBkZAIBDw8WAh8BBQU1Myw4M2RkAgIPDxYCHwEFBTM4LDUzZGQCAw8PFgIfAQUFMTUsMzBkZAIMD2QWCGYPDxYCHwEFBTIzOjAwZGQCAQ8PFgIfAQUFNTMsODRkZAICDw8WAh8BBQUzOCw1NmRkAgMPDxYCHwEFBTE1LDI4ZGQCDQ8PFgIfCmhkZAIVDw8WAh8BBTFWYWxvcmVzIGFjdHVhbGVzIC0gQ290YXMgcG9yIENlbnRyYWwgLSAwNy8wNy8yMDE5ZGQCFw88KwANAQAPFgYfCGcfCQIEHwdoZBYCZg9kFgoCAQ9kFgZmDw8WAh8BBQ5DLiBILiBHLiBUZXJyYWRkAgEPDxYCHwEFBTc5LDc2ZGQCAg8PFgIfAQUFNTQsODhkZAICD2QWBmYPDxYCHwEFD0MuIEguIEJheWdvcnJpYWRkAgEPDxYCHwEFBTUzLDcxZGQCAg8PFgIfAQUFNDAsMTlkZAIDD2QWBmYPDxYCHwEFF0MuIEguIENvbnN0aXR1Y2kmIzI0MztuZGQCAQ8PFgIfAQUFMzksNzJkZAICDw8WAh8BBQQ5LDg0ZGQCBA9kFgZmDw8WAh8BBRFDLkguIFNhbHRvIEdyYW5kZWRkAgEPDxYCHwEFBTM0LDA2ZGQCAg8PFgIfAQUENyw4N2RkAgUPDxYCHwpoZGQCGQ8PFgIfAQUuRXN0YWRvcyBkZSBWZXJ0ZWRlcm9zIHBvciBDZW50cmFsIC0gMDcvMDcvMjAxOWRkAhsPPCsADQEADxYGHwhnHwkCBB8HaGQWAmYPZBYKAgEPZBYKZg8PFgIfAQUOQy4gSC4gRy4gVGVycmFkZAIBDw8WAh8BBQQwOjAwZGQCAg8PFgIfAQUGICAwLjAwZGQCAw8PFgIfAQUFNzksNzZkZAIEDw8WAh8BBQQwLDAwZGQCAg9kFgpmDw8WAh8BBQ9DLiBILiBCYXlnb3JyaWFkZAIBDw8WAh8BBQQwOjAwZGQCAg8PFgIfAQUHQ2VycmFkb2RkAgMPDxYCHwEFBTUzLDc3ZGQCBA8PFgIfAQUEMCwwMGRkAgMPZBYKZg8PFgIfAQUXQy4gSC4gQ29uc3RpdHVjaSYjMjQzO25kZAIBDw8WAh8BBQQwOjAwZGQCAg8PFgIfAQUHQ2VycmFkb2RkAgMPDxYCHwEFBTM5LDc4ZGQCBA8PFgIfAQUEMCwwMGRkAgQPZBYKZg8PFgIfAQURQy5ILiBTYWx0byBHcmFuZGVkZAIBDw8WAh8BBQQwOjAwZGQCAg8PFgIfAQUGJm5ic3A7ZGQCAw8PFgIfAQUFMzQsMTFkZAIEDw8WAh8BBQQwLDAwZGQCBQ8PFgIfCmhkZAIdDw8WAh8BBTJJbmZvcm1hY2nDs24gaW5ncmVzYWRhIGhhc3RhIGVsIDA3LzA3LzIwMTkgLSAxOTowMGRkAg8PPCsACQIADxYGHg1OZXZlckV4cGFuZGVkZB4MU2VsZWN0ZWROb2RlZB4JTGFzdEluZGV4AhBkCBQrABEFcjE6MjQsMToyMywxOjIyLDE6MjEsMToyMCwxOjE5LDE6MTgsMToxNywxOjE2LDE6MTUsMToxNCwxOjEzLDE6MTIsMToxMSwxOjEwLDE6OSwxOjgsMTo3LDE6NiwxOjUsMTo0LDE6MywxOjIsMToxLDE6MBQrAAIWAh4IRXhwYW5kZWRoZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5nZGQYBQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFEmN0bDAwJFRyZWVWaWV3TWFpbgUrY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRncmlkUmVzVmVydGVkZXJvcw88KwAKAQgCAWQFJmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkZ3JpZFJlc0NvdGFzDzwrAAoBCAIBZAUkY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRncmlkQ290YXMxDzwrAAoBCAIBZAUjY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRncmlkQ290YXMPPCsACgEIAgFkI7QzHE2zZ+cJ+Em5EGUmepeQxYY=',
    '__VIEWSTATEGENERATOR': '5B0928BE',
    '__EVENTVALIDATION': '/wEWGgKetoOMBQKHxLbGBQLi1N8DAoPFhowBAozR5qwKAozR4qwKAozR6qwKAs+1/OwCAtSX9IoKAsLE9owOArXX6wQC16/w+QsC5aHR7QsCquvo2wYC7Ln23AUCkZnO3wgC5r2l1QQC2vnp9QYCr8D6iQwCzteRzA8CkuC+xwoCypWFrgsCw+a7mQ8CjMSQxAMCvPz7qwYC34vKwwqRtHZIGz5VM/2Y/Xm8VcssSToEgw==',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date,
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboCentrales': '100002',
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

        with open('Bonete_Data_Horaria.csv', mode='r') as Bonete_Data_Horaria:
            Bonete_Data_Horaria = csv.reader(Bonete_Data_Horaria, delimiter=',')
            List = list(Bonete_Data_Horaria)
            lastDateString = List[-1][0] # i.e. '31/07/2019'.
            lastDate = datetime.datetime.strptime(lastDateString, '%d/%m/%Y')

        weWrote = 0
    
    if Date > lastDate:
        
        weWrote = 1
        
        with open('Bonete_Data_Horaria.csv', mode='a') as Bonete_Data_Horaria:
            Bonete_Data_Horaria = csv.writer(Bonete_Data_Horaria, delimiter=',')

            response = Bonete_Data(Date)
            error = 0;
            while response.status_code != 200:
                response = Bonete_Data(Date)
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
                Bonete_Data_Horaria.writerow([Date.strftime("%d/%m/%Y"),                                              List15[i*4].string.replace('.','').replace(',','.'),                                              List15[i*4+1].string.replace('.','').replace(',','.'),                                              List15[i*4+2].string.replace('.','').replace(',','.'),                                              List15[i*4+3].string])
            for i in range(0,int(L/4)):
                print(List64[i*4].string,                      List64[i*4+1].string.replace('.','').replace(',','.'),                      List64[i*4+2].string.replace('.','').replace(',','.'),                      List64[i*4+3].string.replace('.','').replace(',','.'))
                Bonete_Data_Horaria.writerow([Date.strftime("%d/%m/%Y"),                                              List64[i*4].string.replace('.','').replace(',','.'),                                              List64[i*4+1].string.replace('.','').replace(',','.'),                                              List64[i*4+2].string.replace('.','').replace(',','.'),                                              List64[i*4+3].string])
        
    else:
        
        print(Date.strftime("%d/%m/%Y"), 'exists')
        
    Date = Date + timedelta(days=1)

