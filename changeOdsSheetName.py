#!/usr/bin/env python
# coding: utf-8

# In[14]:


from pyexcel_ods import get_data
from pyexcel_ods import save_data
from collections import OrderedDict
import unidecode
import os
import datetime
from datetime import timedelta

# Author: Renzo Caballero
# KAUST: King Abdullah University of Science and Technology
# email: renzo.caballerorosas@kaust.edu.sa caballerorenzo@hotmail.com
# Website: None.
# August 2019; Last revision: 29/08/2019.


# In[15]:


def ADME_Historicos_Modification(date):
    
    date = date.strftime("%Y%m%d")
    file_name = [date,'.ods']
    file_name = "".join(file_name)
    
    path = ['./ADME_Historicos/',file_name]
    path = "".join(path)
    
    path2 = ['./ADME_Historicos_Corrected/',file_name]
    path2 = "".join(path2)
    
    directory = os.path.dirname(path2)
    
    for root, dirs, files in os.walk(directory):
        if not file_name in files:
            
            data = get_data(path)
            
            List = list(data.keys())
            newList = []
            for i in range(0,len(List)):
                newList.append(unidecode.unidecode(List[i]))

            oldkey, newkey = List[1], newList[1]
            data[newkey] = data.pop(oldkey)
            oldkey, newkey = List[3], newList[3]
            data[newkey] = data.pop(oldkey)

            data.move_to_end(newList[5], last=False)
            data.move_to_end(newList[4], last=False)
            data.move_to_end(newList[3], last=False)
            data.move_to_end(newList[2], last=False)
            data.move_to_end(newList[1], last=False)
            data.move_to_end(newList[0], last=False)

            for i in range(0,len(newList)):
                for j in range(3,148):
                    data[newList[i]][j][0] = 'Waleed_Helped_Here'

            save_data(path2,data)
            
            print(path2,'done!')
            
        else:
            
            print(path2,'exists!')
    
    return


# In[17]:


date = datetime.datetime(2016,11,3)
today = date.today()
twoDaysAgo = today - timedelta(days=2)

while date.strftime("%d/%m/%Y") != twoDaysAgo.strftime("%d/%m/%Y"):
        
    ADME_Historicos_Modification(date)
        
    date = date + timedelta(days=1)

