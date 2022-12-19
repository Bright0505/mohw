import time
import requests
from bs4 import BeautifulSoup
import env_config
import pymysql
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

today=time.strftime('%Y-%m-%d', time.localtime())

def insertSql(read_dataLink,read_dataInfo,chasest):
    db=pymysql.connect(host=env_config.db_host, port=int(env_config.db_port), user=env_config.db_user, passwd=env_config.db_pass, db=env_config.db_base, charset=chasest)
    cur=db.cursor()
    insertLink="INSERT INTO `"+env_config.db_base+"`."+env_config.db_linkTable+"(`basID`,`basUrl`,`createDate`) VALUES (%s,%s,%s)"
    insertInfo="INSERT INTO `"+env_config.db_base+"`."+env_config.db_infoTable+"(`basID`,`basName`,`basArea`,`basAddress`,`basTel`,`basType`,`nhiFlag`,`gvDep`,`gvDoc`,`createDate`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(insertInfo,(read_dataInfo))
    cur.executemany(insertLink,(read_dataLink))
    db.commit()
    cur.close()

def maSearchInfo (urlPath):
    rs=requests.get (str(urlPath).replace('\n',''))
    infoHtml=BeautifulSoup(rs.text,'html.parser')
    basId=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblBAS_ID').text
    basName=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblBAS_NAME').text
    basArea=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblBAS_AREA').text
    basAddress=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblBAS_ADDRESS').text
    basTel=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblBAS_TEL').text
    basType=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblBAS_TYPE').text
    nhiFlag=infoHtml.find('span',id='ctl00_ContentPlaceHolder1_lblNHI_FLAG').text
    gvDepHtml=infoHtml.find('table',id ='ctl00_ContentPlaceHolder1_gvDep')
    gvDep=[str(gvDep.find_previous('tr')).replace('<tr bgcolor="#DEDFDE">\n<td><font color="Black">','"').replace('</font></td><td><font color="Black">V</font></td><td><font color="Black">','":').replace('</font></td>\n</tr>','') for gvDep in gvDepHtml.find_all('td', text='V')[1:]]
    gvDocHtml=infoHtml.find('table',id ='ctl00_ContentPlaceHolder1_gvDoc')
    gvDoc=[str(gvDoc).replace('<tr bgcolor="#DEDFDE">\n<td><font color="Black">','"').replace('</font></td><td><font color="Black">','":').replace('</font></td>\n</tr>','') for gvDoc in gvDocHtml.find_all('tr')[1:]]
    links=basId,str(urlPath).replace('\n',''),today
    infos=basId,basName,basArea,basAddress,basTel,basType,str(nhiFlag).replace('是','1').replace('否','0'),str(gvDep).replace('[','{').replace(']','}').replace("'",""),str(gvDoc).replace('[','{').replace(']','}').replace("'",""),today
    paramLinks.append(links)
    paramInfo.append(infos)
    print (links)

paramLinks=[]
paramInfo=[]
with ThreadPoolExecutor(500) as executor:
    i=1
    for row in open('./tmp/藥局_藥事機構_2022-12-15.txt', 'r'):
        executor.submit(maSearchInfo,(str(row)))
        if i == 500:
            insertSql(paramLinks,paramInfo,'utf8')
            print('sleep 300s')
            time.sleep(300)
            i=1
        i+=1