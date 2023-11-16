from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from PIL import Image
import pytesseract
import time
import re

today=time.strftime('%Y-%m-%d', time.localtime())

baseUrl="https://ma.mohw.gov.tw/masearch/"
headers = {
    'authority': 'ma.mohw.gov.tw',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'origin': 'https://ma.mohw.gov.tw',
    'referer': 'https://ma.mohw.gov.tw/masearch/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
requests.packages.urllib3.disable_warnings()
baseSession=requests.request('GET',baseUrl,headers=headers ,verify=False)
getSessionId=re.search(r'ASP.NET_SessionId=([a-zA-Z0-9]+);',baseSession.headers['Set-Cookie']).group(1)
getVIEWSTATE=re.search(r'ASP.NET_SessionId=([a-zA-Z0-9]+);',baseSession.headers['Set-Cookie']).group(1)
getEVENTVALIDATION=re.search(r'ASP.NET_SessionId=([a-zA-Z0-9]+);',baseSession.headers['Set-Cookie']).group(1)
getVIEWSTATEGENERATOR=re.search(r'ASP.NET_SessionId=([a-zA-Z0-9]+);',baseSession.headers['Set-Cookie']).group(1)
print (getSessionId)

# data = {
#        '__eo_obj_states': '',
#        '__eo_sc': '',
#        '__EVENTTARGET': '',
#        '__EVENTARGUMENT': '',
#        '__LASTFOCUS': '',
#        '__VIEWSTATE': getVIEWSTATE,
#        '__VIEWSTATEGENERATOR': getVIEWSTATEGENERATOR,
#        '__VIEWSTATEENCRYPTED': '',
#        '__EVENTVALIDATION': getEVENTVALIDATION,
#        'eo_version': '12.0.10.2',
#        'eo_style_keys': '/wFk',
#        'ctl00$ContentPlaceHolder1$txtBAS_NAME': '',
#        'ctl00$ContentPlaceHolder1$ddlBAS_KIND': 'D',
#        'ctl00$ContentPlaceHolder1$ddlAREA_CODE': '',
#        'ctl00$ContentPlaceHolder1$ddlZIP_CODE': '',
#        'ctl00$ContentPlaceHolder1$ddlBasDep': '',
#        'ctl00$ContentPlaceHolder1$TextBox1': captua,
#        'ctl00$ContentPlaceHolder1$btnSearch': '查詢',
#    }
# 