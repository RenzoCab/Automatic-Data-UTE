#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
import datetime
from datetime import timedelta
import webbrowser

# Author: Renzo Caballero
# KAUST: King Abdullah University of Science and Technology
# email: renzo.caballerorosas@kaust.edu.sa caballerorenzo@hotmail.com
# Website: None.
# August 2019; Last revision: 16/08/2019.


# In[2]:


def ADME_Historicos(date): # https://pronos.adme.com.uy
        
    date_next = date + timedelta(days=1)
    
    url1 = ['https://pronos.adme.com.uy/gpf.php?fecha_ini=',str(date.day),'%2F',str(date.month),'%2F',str(date.year),
            '&fecha_fin=',str(date_next.day),'%2F',str(date_next.month),'%2F',str(date_next.year),'&send=MOSTRAR']
    url1 = "".join(url1)
    
    file_name = [date.strftime("%Y%m%d"),'.ods']
    # The real format of the files is .ods.
    file_name = "".join(file_name) # The name to the file which we will save.
    file_path = ['./ADME_Historicos/',file_name]
    file_path = "".join(file_path)
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for root, dirs, files in os.walk(directory):
        if not file_name in files:
            sess = requests.Session()
            sess.get(url1) # This is to call the webpage before pressing the button download.
            response = requests.get('https://pronos.adme.com.uy/ods/datos_gen_int.ods')
            open(file_path, "wb").write(response.content)
            print(date)
            
    return


# In[3]:


date = datetime.datetime(2016,11,3)
today = date.today()
twoDaysAgo = today - timedelta(days=2)

while date.strftime("%d/%m/%Y") != twoDaysAgo.strftime("%d/%m/%Y"):
        
    ADME_Historicos(date)
        
    date = date + timedelta(days=1)

