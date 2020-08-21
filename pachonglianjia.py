# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
from publicinfo import *

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}

def GetallxiaoquID(url):
	print(url)
	f = requests.get(url,timeout = 15,headers=headers)
	soup = BeautifulSoup(f.content,"lxml")
	for i in soup.find_all("div",class_='leftContent'):
		for j in  i.find_all("ul",class_="listContent"):
			for k in j.find_all("li",class_="clear xiaoquListItem"):
				print(k.get("data-id"))			#小区ID
				print(k.find("img").get("alt"))	#小区名字
				break


#GetallxiaoquID(urljiangbei)
import datetime
import time
starttime = datetime.datetime.now().replace(microsecond=0)
time.sleep(1)
endtime = datetime.datetime.now().replace(microsecond=0)
tt = endtime-starttime

print("time:%s" % tt)
print(tt.seconds)
exit()

listtest = [{"num":12-30,"name":"kkk"},{"num":2,"name":"kkk"},{"num":15,"name":"kkk"},{"num":20,"name":"kkk"}]
print(listtest)
listtest.sort(key=lambda stu: stu["num"],reverse=True)
print(listtest)
del listtest[0]
print(listtest)

listnew = [{'chajia': 386.0, 'huxing': '3室2厅', 'size': 78.0, 'turn': '南', 'isjz': '简装', 'loucen': '中楼层(共10层)', 'year': '2000年建', 'banta': '塔楼', 'allprice': 76.5, 'danjia': 9808.0},\
	 		{'chajia': 194.0, 'huxing': '2室1厅', 'size': 78.0, 'turn': '东南', 'isjz': '其他', 'loucen': '中楼层(共8层)', 'year': '2000年建', 'banta': '塔楼', 'allprice': 78.0, 'danjia': 10000.0},\
			{'chajia': 106.0, 'huxing': '2室1厅', 'size': 69.39, 'turn': '南', 'isjz': '简装', 'loucen': '中楼层(共8层)', 'year':'2000年建', 'banta': '塔楼', 'allprice': 70.0, 'danjia': 10088.0}]


# item.contents[1].find("a").text):
# name = item.contents[1].find("a").text
# link = item.contents[1].find("a").get("href")
# des = item.contents[1].find("p").text
# number = item.contents[1].find("em", {"class": "learn-number"}).text
# time = item.contents[1].find("dd", {"class": "mar-b8"}).contents[1].text
# degree = item.contents[1].find("dd", {"class": "zhongji"}).contents[1].text
# lesson_info = {"name": name, "link": link, "des": des, "number": number, "time": time, "degree": degree}


# f = requests.get(url,headers=headers)
# soup = BeautifulSoup(f.content,"lxml")
# for i in soup.find_all("div",class_='leftContent'):
# 	for j in  i.find_all("ul",class_="sellListContent"):
# 		for k in j.find_all("li",class_="clear LOGVIEWDATA LOGCLICKDATA"):
# 			for l in k.find_all("div",class_="info clear"):
# 				for m in l.find_all("div",class_="houseInfo"):
# 					#print(m.a.string) 
# 					print(m.get_text())
# 				for m in l.find_all("div",class_="priceInfo"):
# 					print(m.get_text())

##
