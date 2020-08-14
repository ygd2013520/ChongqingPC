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


GetallxiaoquID(urljiangbei)


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
