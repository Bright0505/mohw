from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from PIL import Image
import pytesseract
import time
import env_config
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

today=time.strftime('%Y-%m-%d', time.localtime())
def maSearch(BAS_NAME,BAS_KIND):
    f=open('./tmp/'+BAS_NAME+'_'+BAS_KIND+'_'+today+'.txt','a',encoding='UTF-8')
    pytesseract.pytesseract.tesseract_cmd='tesseract'
    options=webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver=webdriver.Chrome(chrome_options=options,executable_path="./chromedriver")
    driver.get('https://ma.mohw.gov.tw/masearch/')
    driver.save_screenshot('./tmp/tmp.png')
    element=driver.find_element('id','ctl00_ContentPlaceHolder1_ImageCheck')
    left=element.location['x']
    right=element.location['x'] + element.size['width']
    top=element.location['y']
    bottom=element.location['y'] + element.size['height']
    img=Image.open('./tmp/tmp.png')
    img=img.crop((left,top,right,bottom))
    img.save('./tmp/captua.png')
    captua=pytesseract.image_to_string( Image.open('./tmp/captua.png'),lang='eng')
    driver.find_element('name','ctl00$ContentPlaceHolder1$txtBAS_NAME').send_keys(str(BAS_NAME))
    select=Select(driver.find_element('id','ctl00_ContentPlaceHolder1_ddlBAS_KIND'))
    select.select_by_visible_text(str(BAS_KIND))
    driver.find_element('name','ctl00$ContentPlaceHolder1$TextBox1').send_keys(str(captua))
    time.sleep(1)
    endNo=driver.find_element('id','ctl00_ContentPlaceHolder1_NetPager1').find_elements(By.TAG_NAME,'span')[1].text.replace('共 ','').replace(' 頁','')
    n=1
    i=1
    while (n <= int(endNo)):
        driver.find_element('name','ctl00$ContentPlaceHolder1$NetPager1$txtPage').send_keys(str(n))
        driver.find_element('name','ctl00$ContentPlaceHolder1$NetPager1$btGo').click()
        time.sleep(2)
        maLinks=driver.find_element(By.ID , 'ctl00_ContentPlaceHolder1_gviewMain').find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'a')
        for maInfoLink in maLinks[3:]:
            row=maInfoLink.get_attribute('href')+"\n"
            f.write(row)
        if i == 100:
            print('sleep 10s')
            time.sleep(30)
            i=1
        i+=1
        print ('pages:',n)
        n+=1
    driver.quit()

selectDict={'醫院':'醫療機構','診所':'醫療機構','藥局':'藥事機構'}

for row in selectDict.items():
    maSearch(row[0],row[1])
    time.sleep(60)