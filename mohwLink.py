import requests
from PIL import Image
import pytesseract
import time
import re
import csv
from concurrent.futures import ThreadPoolExecutor

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
session = requests.Session()
basePage=session.get(baseUrl,headers=headers ,verify=False)
getSessionId=basePage.cookies['ASP.NET_SessionId']

def getVIEWSTATE(html):
    return re.search(r'__VIEWSTATE" value="([^"]+)"',html).group(1)
def getEVENTVALIDATION(html):
    return re.search(r'__EVENTVALIDATION" value="([^"]+)"',html).group(1)
def getVIEWSTATEGENERATOR(html):
    return re.search(r'__VIEWSTATEGENERATOR" value="([^"]+)"',html).group(1)

cookie={'ASP.NET_SessionId': getSessionId}
captuaUrl="https://ma.mohw.gov.tw/ValidateCode.aspx"
getCaptuaImg=session.get(captuaUrl,headers=headers,cookies=cookie)
with open('./tmp/captua.png', 'wb') as file:
        file.write(getCaptuaImg.content)
captua=(pytesseract.image_to_string( Image.open('./tmp/captua.png'),lang='eng')).replace(" ","").replace("\n","")
payloadData = {
       '__eo_obj_states': '',
       '__eo_sc': '',
       '__EVENTTARGET': '',
       '__EVENTARGUMENT': '',
       '__LASTFOCUS': '',
       '__VIEWSTATE': getVIEWSTATE(basePage.text),
       '__VIEWSTATEGENERATOR': getVIEWSTATEGENERATOR(basePage.text),
       '__VIEWSTATEENCRYPTED': '',
       '__EVENTVALIDATION': getEVENTVALIDATION(basePage.text),
       'eo_version': '12.0.10.2',
       'eo_style_keys': '/wFk',
       'ctl00$ContentPlaceHolder1$txtBAS_NAME': '',
       'ctl00$ContentPlaceHolder1$ddlBAS_KIND': 'D',
       'ctl00$ContentPlaceHolder1$ddlAREA_CODE': '',
       'ctl00$ContentPlaceHolder1$ddlZIP_CODE': '',
       'ctl00$ContentPlaceHolder1$ddlBasDep': '',
       'ctl00$ContentPlaceHolder1$TextBox1': captua,
       'ctl00$ContentPlaceHolder1$btnSearch': '查詢',
    }
loginPage=session.post(baseUrl,headers=headers,cookies=cookie,data=payloadData)
getTotalPage=re.search(r'共 (\d+) 頁', loginPage.text).group(1)

def getLink (PageNum):
    payloadDataPage = {
         '__eo_obj_states': '',
         '__eo_sc': '',
         '__EVENTTARGET': '',
         '__EVENTARGUMENT': '',
         '__LASTFOCUS': '',
         '__VIEWSTATE': getVIEWSTATE(loginPage.text),
         '__VIEWSTATEGENERATOR': getVIEWSTATEGENERATOR(loginPage.text),
         '__VIEWSTATEENCRYPTED': '',
         '__EVENTVALIDATION': getEVENTVALIDATION(loginPage.text),
         'eo_version': '12.0.10.2',
         'eo_style_keys': '/wFk',
         'ctl00$ContentPlaceHolder1$txtBAS_NAME': '',
         'ctl00$ContentPlaceHolder1$ddlBAS_KIND': 'D',
         'ctl00$ContentPlaceHolder1$ddlAREA_CODE': '',
         'ctl00$ContentPlaceHolder1$ddlZIP_CODE': '',
         'ctl00$ContentPlaceHolder1$ddlBasDep': '',
         'ctl00$ContentPlaceHolder1$TextBox1': '',
         'ctl00$ContentPlaceHolder1$NetPager1$txtPage': str(PageNum),
         'ctl00$ContentPlaceHolder1$NetPager1$btGo': 'Go',
        }
    getLinkPage=session.post(baseUrl,headers=headers,cookies=cookie,data=payloadDataPage)
    return re.findall(r'<a.*?href="(.*?)"[^>]*>詳細資料</a>', getLinkPage.text)

with ThreadPoolExecutor(500) as executor:
    links = executor.map(getLink, map(str, range(1, int(getTotalPage) + 1)))

with open('./123.csv', "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    for link in links:
        csv_writer.writerows(zip(link))
