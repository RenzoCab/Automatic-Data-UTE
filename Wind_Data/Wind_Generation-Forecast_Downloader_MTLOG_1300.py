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
# email 1: renzo.caballerorosas@kaust.edu.sa
# email 2: CaballeroRenzo@hotmail.com
# email 3: CaballeroRen@gmail.com
# Website: None
# November 2019; Last revision: 15/01/2020

# For more information about this file, check ./Notes/generalNotes.pdf.


# In[2]:


def Wind_G_F(Date, Parques, Procedencia, Hora, Tipo): #https://apps.ute.com.uy/SgePublico/ConsPrevGeneracioEolica.aspx
    
    # On 14/01/2020, I updated this cURL w.r.t. the older versions.
    # I do not know what is different, but it seems to work after I made the change.
    
    cookies = {
    'ASP.NET_SessionId': 'rtkkpwvns3xd24bez0rshd55',
    }

    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://apps.ute.com.uy',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Referer': 'https://apps.ute.com.uy/SgePublico/ConsPrevGeneracioEolica.aspx',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    }

    data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    'ctl00_TreeViewMain_ExpandState': 'nnnnnnnnnnnnnnnnnnnnnnnnn',
    'ctl00_TreeViewMain_SelectedNode': '',
    'ctl00_TreeViewMain_PopulateLog': '',
    '__VIEWSTATE': '/wEPDwUKMjEwNTI2MjQ4MQ9kFgJmDw8WAh4JX09wY2lvbmVzBQdFTkVSR0lBZBYCAgMPZBYGAgEPDxYCHgRUZXh0BSJQcm9uw7NzdGljbyBkZSBHZW5lcmFjacOzbiBFw7NsaWNhZGQCDQ9kFhYCAw8QZBAVEApBcnRpbGxlcm9zC0NhcmFwZSBJK0lJCUNhcmFjb2xlcxNDLlBlcmFsdGErUGVyMStQZXIyEUXDs2xpY28gRmxvcmlkYSBJEEp1YW4gUGFibG8gVGVycmEIS2VudGlsdXgLTHVjZXMgUitMK00HTWluYXMgSQhNZWxvd2luZAVQYW1wYQlSIGRlbCBTdXIVVGFsYXMgZGVsIE1hY2llbCBJK0lJFlRvdGFsIHBhw61zIChwcm92aXN0bykKVmFsZW50aW5lcxZWZW50dXMgQ29tLiBFbmVyLiBTLkEuFRAKQVJUSTAxUE9UUApDQVBFMDFQT1RQCkNBUkEwMVBPVFAKQ1BQUDAxUE9UUApGTE8xMDFQT1RQCkpQVEUwMVBPVFAKS0VOVDAxUE9UUApMUkxNMDFQT1RQCk1JTjEwMVBPVFAKTVdJTjAxUE9UUApQQU1QMDFQT1RQClJTVVIwMVBPVFAKVERNQTAxUE9UUApVUlVZMDFQT1RQClZBTEUwMVBPVFAKVkVDTzAxUE9UUBQrAxBnZ2dnZ2dnZ2dnZ2dnZ2dnFgECDWQCBw8QZGQWAWZkAgsPEGRkFgFmZAIRDzwrABABABQrAAMPFgIeClBvc3RlZERhdGUFCjE0LzAxLzIwMjBkZGQWBAIDDw8WAh4NQWx0ZXJuYXRlVGV4dAUFIC4uLiAWBB4Fc3R5bGUFKnZlcnRpY2FsLWFsaWduOnRleHQtYm90dG9tO2N1cnNvcjpwb2ludGVyOx4Hb25jbGljawVIQ2FsZW5kYXJQb3B1cF9GaW5kQ2FsZW5kYXIoJ2N0bDAwX0NvbnRlbnRQbGFjZUhvbGRlcjFfRmVjaGFJbmknKS5TaG93KCk7ZAIEDxYCHgV2YWx1ZQUKMjMvMDQvMjAxOWQCFQ8QZBAVAwxBV1NUcnVlcG93ZXIMTWV0ZW9sw7NnaWNhL1VURSBwcm9ub3N0aWNvIDUgLWVuc2VtYmxlcy0gaGF6IGRlIDIwIGNvcnJpZGFzFQMFQVdTVFAFTVRMT0cFVVRFUDUUKwMDZ2dnFgFmZAIZDxBkEBUDBGgyODgCaDYDaDcyFQMEaDI4OAJoNgNoNzIUKwMDZ2dnFgECAmQCHQ8QZBAVBAUwMTowMAUwNzowMAUxMzowMAUxOTowMBUEBDAxMDAEMDcwMAQxMzAwBDE5MDAUKwMEZ2dnZxYBZmQCHw8PFgIeB0VuYWJsZWRoZGQCIw88KwANAQAPFgYeC18hRGF0YUJvdW5kZx4LXyFJdGVtQ291bnQCAR4HVmlzaWJsZWhkFgJmD2QWBAIBD2QWDGYPDxYCHwEFBiZuYnNwO2RkAgEPDxYCHwEFBiZuYnNwO2RkAgIPDxYCHwEFBiZuYnNwO2RkAgMPDxYCHwEFBiZuYnNwO2RkAgQPDxYCHwEFBiZuYnNwO2RkAgUPDxYCHwEFBiZuYnNwO2RkAgIPDxYCHwpoZGQCKQ8PFgQfAQVATm8gc2UgZGlzcG9uZSBkZSBwcm9uw7NzdGljbyBwYXJhIGxhcyBjb25kaWNpb25lcyBzZWxlY2Npb25hZGFzLh8KaGRkAisPDxYEHwEFd1NlIGNvbnNpZGVyYSBsYSBkaXNwb25pYmlsaWRhZCBkZWwgMTAwICUgZGUgbGEgcG90ZW5jaWEgYXV0b3JpemFkYSBkZSBsYXMgdW5pZGFkZXMgZ2VuZXJhZG9yYXMgc2VsZWNjaW9uYWRhcyAgKDE0ODggTVcpHwpoZGQCDw88KwAJAgAPFgYeDU5ldmVyRXhwYW5kZWRkHgxTZWxlY3RlZE5vZGVkHglMYXN0SW5kZXgCGWQIFCsAGgVPMTo0MCwxOjM5LDE6MzgsMTozNywxOjM2LDE6MzUsMTozNCwxOjMzLDE6MzIsMTozMSwxOjMwLDE6MjksMToyOCwxOjI3LDE6MjYsMToyNRQrAAIWAh4IRXhwYW5kZWRoZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZBQrAAIWAh8OaGQUKwACFgIfDmhkFCsAAhYCHw5oZGQYAgUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFEmN0bDAwJFRyZWVWaWV3TWFpbgUiY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRncmlkUHJvbg88KwAKAQgCAWQaRwQwzHl632ItwPoq0G+ZDK7C5Q==',
    '__VIEWSTATEGENERATOR': '2CA7B51F',
    '__EVENTVALIDATION': '/wEWQALM65y7BwKojr+iBALj3MvgCAL1j//IAQL7iIjPAwL1j9fOCQLP45DTDQL6mNKdDALXzdfxCQKoi7mjBAL9vOP8DwKmr7PzDAKH7pKjCQL9wfN+AouwwsAFAuKrm8YKAo623eALAsvAwpMNAtuD0esHAvzI85UKArTDtCEC17j52AMC1Jf0igoCh8S2xgUC4tTfAwLsnvWEDgL87pOCAgLyutbaCQKrxq7wCwKp/qLSBAKjm9RkAuGR8L8IArH/j7YLAv6a6pgJAtS0o58JAtS0258JAte0q58JAte0g58JAsLE9owOAv2ip9AEArvb85MEArXX6wQCtavwkQ0C/rGGzgECh52z3AQCwdr+UwL9hriSCAKBi6gKApnSmYkJArWo9aoOAt3git8NAu/DvMoGAu7PpOYDApazzdYEAtOSkNcMAsm9hoAJArvi7M4FAraYyrkCAue6oZUMAvuD4PsLAtKLu4cHAtLFkJcIAub8l84EArniqqwKVhXv1BI4TaOPMyORj6uaoQO3kOg=',
    'ctl00$ContentPlaceHolder1$cboParques': Parques,
    'ctl00$ContentPlaceHolder1$cboAlcance': 'Totales',
    'ctl00$ContentPlaceHolder1$cboVariable': 'Potencia',
    'ctl00$ContentPlaceHolder1$cmdAplicar': 'Aplicar',
    'ctl00$ContentPlaceHolder1$FechaIni$textBox': Date, # E.g., '23/04/2019'.
    'ctl00$ContentPlaceHolder1$FechaIni$hidden': Date,
    'ctl00$ContentPlaceHolder1$cboProcedencia': Procedencia,
    'ctl00$ContentPlaceHolder1$cboTipoPron': Tipo,
    'ctl00$ContentPlaceHolder1$cboHoras': Hora,
    'ctl00$ContentPlaceHolder1$hdnCargar': 'NO'
    }

    response = requests.post('https://apps.ute.com.uy/SgePublico/ConsPrevGeneracioEolica.aspx', headers=headers, cookies=cookies, data=data)

    return response


# In[ ]:


### AWSTP --> 23/04/2019
### MTLOG --> 08/01/2016
### UTEP5 --> 05/07/2017

Date = datetime.datetime(2016,1,8)
final_day = Date.today() - timedelta(days = 6)

weWrote = 1
file_name = 'Wind_Data_MTLOG_1300.csv'
starting_hour = '1300'
Procedencia = 'MTLOG'

while Date < final_day:
    
    if weWrote == 1:
        
        with open(file_name, mode = 'r') as Wind_Data_AWSTP:
            
            Wind_Data_AWSTP = csv.reader(Wind_Data_AWSTP, delimiter = ',')
            List = list(Wind_Data_AWSTP)

            last_date_saved = List[-1][0]
            try:
                date_to_check = datetime.datetime.strptime(last_date_saved, '%d/%m/%Y') - timedelta(days = 3)
            except:
                print('This fails the first time ever we write, because the file does not have any date.')
                date_to_check = datetime.datetime.strptime('01/01/1999', '%d/%m/%Y') 
                
        weWrote = 0

    if  Date > date_to_check:

        weWrote = 1
        
        response = Wind_G_F(Date,'URUY01POTP',Procedencia,starting_hour,'h72')
        error = 0;
        while response.status_code != 200:
            response = Wind_G_F(Date,'URUY01POTP',Procedencia,starting_hour,'h72')
            error = error + 1
            print('Error:', error)

        response_soup = BeautifulSoup(response.content, 'html.parser')
        All_td = response_soup.find_all('td')
        List = list(All_td)
        Table = List[30].table
        All = Table.find_all('td')
        List_all = list(All)
        
        with open(file_name, mode = 'a') as Wind_Data_AWSTP:
            Wind_Data_AWSTP_csv = csv.writer(Wind_Data_AWSTP, delimiter=',')

            for i in range(0,72):
                
                try:
                    print(List_all[i*6+1].string,
                    List_all[i*6+2].string,\
                    starting_hour,
                    List_all[i*6+3].string.replace('.','').replace(',','.'),\
                    List_all[i*6+4].string.replace('.','').replace(',','.'),\
                    List_all[i*6+5].string.replace('.','').replace(',','.'),\
                    List_all[i*6+6].string.replace('.','').replace(',','.'))

                    Wind_Data_AWSTP_csv.writerow([List_all[i*6+1].string,
                    List_all[i*6+2].string,\
                    starting_hour,
                    List_all[i*6+3].string.replace('.','').replace(',','.'),\
                    List_all[i*6+4].string.replace('.','').replace(',','.'),\
                    List_all[i*6+5].string.replace('.','').replace(',','.'),\
                    List_all[i*6+6].string.replace('.','').replace(',','.')])
                except:
                    print('The data does not exist!')
                    
    Date = Date + timedelta(days = 1)


# In[ ]:


# codes = {

#     # Informational.
#     100: ('continue',),
#     101: ('switching_protocols',),
#     102: ('processing',),
#     103: ('checkpoint',),
#     122: ('uri_too_long', 'request_uri_too_long'),
#     200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
#     201: ('created',),
#     202: ('accepted',),
#     203: ('non_authoritative_info', 'non_authoritative_information'),
#     204: ('no_content',),
#     205: ('reset_content', 'reset'),
#     206: ('partial_content', 'partial'),
#     207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
#     208: ('already_reported',),
#     226: ('im_used',),

#     # Redirection.
#     300: ('multiple_choices',),
#     301: ('moved_permanently', 'moved', '\\o-'),
#     302: ('found',),
#     303: ('see_other', 'other'),
#     304: ('not_modified',),
#     305: ('use_proxy',),
#     306: ('switch_proxy',),
#     307: ('temporary_redirect', 'temporary_moved', 'temporary'),
#     308: ('permanent_redirect',
#           'resume_incomplete', 'resume',),  # These 2 to be removed in 3.0

#     # Client Error.
#     400: ('bad_request', 'bad'),
#     401: ('unauthorized',),
#     402: ('payment_required', 'payment'),
#     403: ('forbidden',),
#     404: ('not_found', '-o-'),
#     405: ('method_not_allowed', 'not_allowed'),
#     406: ('not_acceptable',),
#     407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
#     408: ('request_timeout', 'timeout'),
#     409: ('conflict',),
#     410: ('gone',),
#     411: ('length_required',),
#     412: ('precondition_failed', 'precondition'),
#     413: ('request_entity_too_large',),
#     414: ('request_uri_too_large',),
#     415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
#     416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
#     417: ('expectation_failed',),
#     418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
#     421: ('misdirected_request',),
#     422: ('unprocessable_entity', 'unprocessable'),
#     423: ('locked',),
#     424: ('failed_dependency', 'dependency'),
#     425: ('unordered_collection', 'unordered'),
#     426: ('upgrade_required', 'upgrade'),
#     428: ('precondition_required', 'precondition'),
#     429: ('too_many_requests', 'too_many'),
#     431: ('header_fields_too_large', 'fields_too_large'),
#     444: ('no_response', 'none'),
#     449: ('retry_with', 'retry'),
#     450: ('blocked_by_windows_parental_controls', 'parental_controls'),
#     451: ('unavailable_for_legal_reasons', 'legal_reasons'),
#     499: ('client_closed_request',),

#     # Server Error.
#     500: ('internal_server_error', 'server_error', '/o\\', '✗'),
#     501: ('not_implemented',),
#     502: ('bad_gateway',),
#     503: ('service_unavailable', 'unavailable'),
#     504: ('gateway_timeout',),
#     505: ('http_version_not_supported', 'http_version'),
#     506: ('variant_also_negotiates',),
#     507: ('insufficient_storage',),
#     509: ('bandwidth_limit_exceeded', 'bandwidth'),
#     510: ('not_extended',),
#     511: ('network_authentication_required', 'network_auth', 'network_authentication')
    
# }


# In[ ]:


# Parques = ['ARTI01POTP','CAPE01POTP','CARA01POTP','CPPP01POTP','FLO101POTP','JPTE01POTP','KENT01POTP',\
#           'LRLM01POTP','MIN101POTP','MWIN01POTP','PAMP01POTP','RSUR01POTP','TDMA01POTP','URUY01POTP',\
#           'VALE01POTP','VECO01POTP']
# Nombres = ['Artilleros','Carape I+II','Caracoles','C.Peralta+Per1+Per2','Eolico Florida I','Juan Pablo Terra',\
#           'Kentilux','Luces R+L+M','Minas I','Melowind','Pampa','R del Sur','Talas del Maciel I+II','Total pais (provisto)',\
#           'Valentines','Ventus Com. Ener. S.A.']
# Procedencia = ['GAHAS','MTLOG','UTEP3','UTEP5']
# TipoPron1 = ['10m432','h240','h6','h72']
# # GAHAS looks super unuseful.
# TipoPron2 = ['h240','h288','h6','h72']
# # h240 and h288 have only 1100. h6 has from 0000 to 2300.
# # h72 has 0100, 0700, 1300 and 1900.
# TipoPron3 = ['h6','h72','h240']
# # h6 has from 0000 to 2300. h72 has 0100, 0700, 1300 and 1900.
# # h240 has only 1100.
# TipoPron4 = ['h240','h288','h6','h72']
# h6_times = ['0000','0100','0200','0300','0400','0500','0600','0700',\
#            '0800','0900','1000','1100','1200','1300','1400','1500',\
#            '1600','1700','1800','1900','2000','2100','2200','2300',]
# h72_times = ['0100','0700','1300','1900']
# h240_times = ['1100']
# h288_times = ['1100']

# # The above is old, the new "Procedencia" are (14/01/2020):

# Procedencia = ['AWSTP','MTLOG','UTEP5']
# # The corresponding starting times are:
# ### AWSTP --> 23/04/2019
# ### MTLOG --> 08/01/2016
# ### UTEP5 --> 05/07/2017

