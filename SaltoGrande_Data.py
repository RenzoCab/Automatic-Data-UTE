#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import os
import csv

# Author: Renzo Caballero
# KAUST: King Abdullah University of Science and Technology
# email: renzo.caballerorosas@kaust.edu.sa caballerorenzo@hotmail.com
# Website: None.
# August 2019; Last revision: 28/08/2019.


# In[2]:


date = datetime.datetime(2018,3,2) # Revisar! Tiene un error!

# https://www.saltogrande.org/datos_diarios.php?nf=02%2F03%2F2018&f=2018-03-02
# https://www.saltogrande.org/datos_diarios.php?nf=27%2F04%2F2018&f=2018-04-27
# Date.strftime("%d/%m/%Y")

today = date.today()
twoDaysAgo = today - timedelta(days=2)
stringTDA = twoDaysAgo.strftime("%d/%m/%Y")

while date.strftime("%d/%m/%Y") != stringTDA:

    year = ['20',str(date.strftime("%y"))]
    year = "".join(year)
    url = ['https://www.saltogrande.org/datos_diarios.php?nf=',str(date.strftime("%d")),'%2F',           str(date.strftime("%m")),'%2F',year,'&f=',year,str(date.strftime("-%m-%d"))]
    url = "".join(url)
    file_path = ["./SG_Data/",str(date.strftime("%y%m%d")),'.csv']
    file_path = "".join(file_path)
    file_name = [str(date.strftime("%y%m%d")),'.csv']
    file_name = "".join(file_name)
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    exists = os.path.isfile(file_path)
        
    if not exists:
            
        response = requests.get(url, allow_redirects=True)
        response_soup = BeautifulSoup(response.content, 'html.parser')

        All_td = response_soup.find_all('td')

        try:

            List = list(All_td)
            index = [3,5,7,9,11,13,15,17,19,23,25,27,29,31,35,37,39,41,43]
            title = [2,4,6,8,10,12,14,16,18,22,24,26,28,30,34,36,38,40,42]

            list_titles = [0] * len(title)
            for j in range(0,len(title)):
                list_titles[j] = List[title[j]].text

            list_index = [0] * len(index)
            for j in range(0,len(index)):
                list_index[j] = List[index[j]].text

            with open(file_path, mode='a') as SG_Data_Daily:
                SG_Data_Daily = csv.writer(SG_Data_Daily, delimiter=',')
                SG_Data_Daily.writerow(['',list_titles[0],list_titles[1],list_titles[2],list_titles[3],list_titles[4],                                      list_titles[5],list_titles[6],list_titles[7],list_titles[8],list_titles[9],                                      list_titles[10],list_titles[11],list_titles[12],list_titles[13],list_titles[14],                                      list_titles[15],list_titles[16],list_titles[17],list_titles[18]])
                SG_Data_Daily.writerow([date.strftime("%d/%m/%Y"),list_index[0],list_index[1],list_index[2],list_index[3],                                      list_titles[4],list_index[5],list_index[6],list_index[7],list_index[8],list_index[9],                                      list_index[10],list_index[11],list_index[12],list_index[13],list_index[14],                                      list_index[15],list_index[16],list_index[17],list_index[18]])

            print(date.strftime("%d/%m/%Y"))

            date = date + timedelta(days=1)

        except:

            print("An exception occurred")
            
    else:
        print(date.strftime("%d/%m/%Y"), 'exists')
        date = date + timedelta(days=1)


# In[3]:


date = datetime.datetime(2018,4,17,0)

# https://www.saltogrande.org/datos_horarios.php?nfh=01%2F01%2F2018+01%3A00&fh=2018-01-01+01%3A00%3A00
# https://www.saltogrande.org/datos_horarios.php?nfh=01%2F01%2F2018+02%3A00&fh=2018-01-01+02%3A00%3A00
# https://www.saltogrande.org/datos_horarios.php?nfh=01%2F01%2F2018+13%3A00&fh=2018-01-01+13%3A00%3A00
# https://www.saltogrande.org/datos_horarios.php?nfh=01%2F01%2F2018+23%3A00&fh=2018-01-01+23%3A00%3A00
# https://www.saltogrande.org/datos_horarios.php?nfh=09%2F02%2F2018+23%3A00&fh=2018-02-09+23%3A00%3A00

today = date.today()
twoDaysAgo = today - timedelta(days=2)
stringTDA = twoDaysAgo.strftime("%d/%m/%Y")

while date.strftime("%d/%m/%Y") != stringTDA:

    year = ['20',str(date.strftime("%y"))]
    year = "".join(year)
    hour = date.strftime("%H")
    
    url = ['https://www.saltogrande.org/datos_horarios.php?nfh=',str(date.strftime("%d")),           '%2F',str(date.strftime("%m")),'%2F',year,'+',hour,'%3A00&fh=',year,           str(date.strftime("-%m-%d")),'+',hour,'%3A00%3A00']
    url = "".join(url)
    file_path = ["./SG_Data_Hourly/",str(date.strftime("%y%m%d%H")),'.csv']
    file_path = "".join(file_path)
    file_name = [str(date.strftime("%y%m%d%H")),'.csv']
    file_name = "".join(file_name)
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    exists = os.path.isfile(file_path)
        
    if not exists:
            
        response = requests.get(url, allow_redirects=True)
        response_soup = BeautifulSoup(response.content, 'html.parser')

        All_td = response_soup.find_all('td')

        try:

            List = list(All_td)
            index = [3,5,7,9,11,13,15,19,21,23,27,29,31,33,35,37,41,43,45,47,49,51,53,55,57,59]
            title = [2,4,6,8,10,12,14,18,20,22,26,28,30,32,34,36,40,42,44,46,48,50,52,54,56,58]

            list_titles = [0] * len(title)
            for j in range(0,len(title)):
                list_titles[j] = List[title[j]].text

            list_index = [0] * len(index)
            for j in range(0,len(index)):
                list_index[j] = List[index[j]].text

            with open(file_path, mode='a') as SG_Data_Daily:
                SG_Data_Daily = csv.writer(SG_Data_Daily, delimiter=',')
                SG_Data_Daily.writerow(['',list_titles[0],list_titles[1],list_titles[2],list_titles[3],list_titles[4],                                      list_titles[5],list_titles[6],list_titles[7],list_titles[8],list_titles[9],                                      list_titles[10],list_titles[11],list_titles[12],list_titles[13],list_titles[14],                                      list_titles[15],list_titles[16],list_titles[17],list_titles[18]])
                SG_Data_Daily.writerow([date.strftime("%d/%m/%Y %H"),list_index[0],list_index[1],list_index[2],list_index[3],                                      list_titles[4],list_index[5],list_index[6],list_index[7],list_index[8],list_index[9],                                      list_index[10],list_index[11],list_index[12],list_index[13],list_index[14],                                      list_index[15],list_index[16],list_index[17],list_index[18]])

            print(date.strftime("%H - %d/%m/%Y"))

            date = date + timedelta(hours=1)

        except:

            print("An exception occurred")
            
    else:
        print(date.strftime("%d/%m/%Y"), 'exists')
        date = date + timedelta(days=1)


# In[ ]:




