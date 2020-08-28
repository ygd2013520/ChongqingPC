# -*- coding: utf-8 -*-
#继承父类的子类
from FatherClass import *

#打印log信息代码
#self.mtLogBox.AppendText("mes test\n")
#链家主城八区URL网络地址
urljiangbei = "https://cq.lianjia.com/xiaoqu/jiangbei/"     #江北区小区url
urlnanan = "https://cq.lianjia.com/xiaoqu/nanan/"       #南岸区小区url
urlbanan = "https://cq.lianjia.com/xiaoqu/banan/"       #巴南区小区url
urlyuzhong = "https://cq.lianjia.com/xiaoqu/yuzhong/"     #渝中区小区url
urlyubei = "https://cq.lianjia.com/xiaoqu/yubei/"       #渝北区小区url
urljiulongpo = "https://cq.lianjia.com/xiaoqu/jiulongpo/"       #九龙坡区url
urldadukou = "https://cq.lianjia.com/xiaoqu/dadukou/"     #大渡口区小区url
urlshapingba = "https://cq.lianjia.com/xiaoqu/shapingba/"   #沙坪坝区小区url
urlbeibei = "https://cq.lianjia.com/xiaoqu/beibei/"   #北碚区小区url

from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
from publicinfo import *
#import datetime

class LjClassPC(FatherClassPC):
    def GetAllXioayuID_Quyu(self):
        if self.quyu == "江北区":
            url = urljiangbei
        elif self.quyu == "南岸区":
            url = urlnanan
        elif self.quyu == "巴南区":
            url = urlbanan
        elif self.quyu == "渝中区":
            url = urlyuzhong
        elif self.quyu == "渝北区":
            url = urlyubei
        elif self.quyu == "九龙坡":
            url = urljiulongpo
        elif self.quyu == "大渡口":
            url = urldadukou
        elif self.quyu == "沙坪坝":
            url = urlshapingba
        else:
            url = urlbeibei
        #根据区域获取小区ID和名称
        pagenum = 0
        try:
            # starttime = datetime.datetime.now()
            f = requests.get(url,timeout = 15,headers=self.headers)
            # endtime = datetime.datetime.now()
            # print(endtime-starttime)
        except Exception as e:
            self.mtLogBox.AppendText("LjClassPC 1 requests.get error\n")
            print(e)
            return
        self.begintime = datetime.datetime.now().replace(microsecond=0)
        self.mtLogBox.AppendText("正在抓取%s第1页的所有小区ID，请等待。。。耗时:%s\n" % (self.quyu,datetime.datetime.now().replace(microsecond=0) - self.begintime))
        soup = BeautifulSoup(f.content,"lxml")
        for i in soup.find_all("div",class_='leftContent'):
            for j1 in i.find_all("div",class_="contentBottom clear"):
                for j2 in j1.find_all("div",class_="page-box fr"):
                    for j3 in j2.find_all("div",class_="page-box house-lst-page-box"):
                        pagenum = int((j3.get("page-data").split(":")[1].split(",")[0].strip()))#获取一共多少页
                        break
            for j in  i.find_all("ul",class_="listContent"):
                for k in j.find_all("li",class_="clear xiaoquListItem"):
                    idname = {"id":"","name":"","junjia":0}
                    totalSellCount = k.find("a",{"class":"totalSellCount"}).find("span").text.strip()
                    if int(totalSellCount) ==  0:
                        continue
                    jj = k.find("div", {"class": "totalPrice"}).find("span").text.strip()
                    if jj == "暂无":
                        continue
                    idname["id"] = k.get("data-id")			#小区ID
                    idname["name"] = k.find("img").get("alt")	#小区名字
                    idname["junjia"] = int(jj)
                    self.allXiaoquID_Quyu.append(idname)
                    #break
        #根据页数获取所以小区ID名称
        if pagenum > 1:
            for num in range(2,pagenum+1):
                newurl = url + "pg%d/" % num
                self.mtLogBox.AppendText("正在抓取%s区第%d页的所有小区ID，共%d页，请等待。。。耗时:%s\n" % (self.quyu,num,pagenum,datetime.datetime.now().replace(microsecond=0) - self.begintime))
                try:
                    f = requests.get(newurl,timeout = 15,headers=self.headers)
                except Exception as e:
                    self.mtLogBox.AppendText("LjClassPC 2 requests.get error\n")
                    print(e)
                    continue
                soup = BeautifulSoup(f.content,"lxml")
                for i in soup.find_all("div",class_='leftContent'):
                    for j in  i.find_all("ul",class_="listContent"):
                        for k in j.find_all("li",class_="clear xiaoquListItem"):
                            idname = {"id":"","name":"","junjia":0}
                            totalSellCount = k.find("a",{"class":"totalSellCount"}).find("span").text.strip()
                            if int(totalSellCount) ==  0:
                                continue
                            jj = k.find("div", {"class": "totalPrice"}).find("span").text.strip()
                            if jj == "暂无":
                                continue
                            idname["id"] = k.get("data-id")			#小区ID
                            idname["name"] = k.find("img").get("alt")	#小区名字
                            idname["junjia"] = int(jj)
                            self.allXiaoquID_Quyu.append(idname)
                            #break
        self.mtLogBox.AppendText("%s区所有小区ID获取完成,一共%d个小区\n" % (self.quyu,len(self.allXiaoquID_Quyu)))               
    #获取所有house
    def GetAll_Houses(self):
        allgethouses = []
        allgethousesnew = []
        alllen = len(self.allXiaoquID_Quyu)
        for i in range(alllen):
            self.mtLogBox.AppendText("正在抓取%s 第 %d/%d小区数据，请等待。。。耗时:%s\n" % (self.quyu,i+1,alllen,datetime.datetime.now().replace(microsecond=0) - self.begintime))
            gethouses = self.GetXiaoqu_Houses(self.allXiaoquID_Quyu[i])
            if len(gethouses) == 0:
                continue
            gethousesnew = {"maxchajia":gethouses[0]["chajia"],"houses":gethouses}
            allgethouses.append(gethousesnew)
        #排序
        allgethouses.sort(key=lambda stu: stu["maxchajia"],reverse=True)
        if(len(allgethouses) > self.xiaoqunum):
            allgethouses = allgethouses[0:self.xiaoqunum:1]
        for i in range(len(allgethouses)):
            for j in range(len(allgethouses[i]["houses"])):
                allgethousesnew.append(allgethouses[i]["houses"][j])
        self.mtLogBox.AppendText("%s区所有小区数据抓取完成！！！\n" % self.quyu)
        return allgethousesnew
            

    def GetXiaoqu_Houses(self,idname):
        pagenum = 0
        houselist = []
        urlxiaoqu = "https://cq.lianjia.com/ershoufang/ie2sf1c%s/" % idname["id"]
        self.mtLogBox.AppendText("正在抓取%s区小区：%s的第1页数据，请等待。。。耗时:%s\n" % (self.quyu,idname["name"],datetime.datetime.now().replace(microsecond=0) - self.begintime))
        try:
            f = requests.get(urlxiaoqu,timeout = 15,headers=self.headers)
        except Exception as e:
            self.mtLogBox.AppendText("GetXiaoqu_Houses 1 requests.get error\n")
            print(e)
            return houselist
        soup = BeautifulSoup(f.content,"lxml")
        for i in soup.find_all("div",class_='leftContent'):
            for j3 in i.find_all("div",class_="resultDes clear"):
                n = j3.find("h2",{"class":"total fl"}).find("span").text.strip()
                if int(n) == 0:
                    return houselist
            for j1 in i.find_all("div",class_="contentBottom clear"):
                for j2 in j1.find_all("div",class_="page-box fr"):
                    for j3 in j2.find_all("div",class_="page-box house-lst-page-box"):
                        pagenum = int((j3.get("page-data").split(":")[1].split(",")[0].strip()))#获取一共多少页
                        break
            for j in  i.find_all("ul",class_="sellListContent"):
                for k in j.find_all("li",class_="clear LOGVIEWDATA LOGCLICKDATA"):
                    # u = k.find("a",{"class":"noresultRecommend img LOGCLICKDATA"}).get("href")
                    # if self.iszhuzhai(u) == False:
                    #     continue
                    for l in k.find_all("div",class_="info clear"):
                        houseinfo = {"name":"","huxing":"","size":0,"turn":"","isjz":"","loucen":"","year":"","banta":"","allprice":0,"danjia":0,"junjia":0,"chajia":0}
                        for m in l.find_all("div",class_="houseInfo"):
                            info = m.get_text()
                            info = info.split("|")
                            if len(info) == 7:
                                houseinfo["huxing"] = info[0].strip()
                                houseinfo["size"] = float(info[1].split("平米")[0].strip())
                                houseinfo["turn"] = info[2].strip()
                                houseinfo["isjz"] = info[3].strip()
                                houseinfo["loucen"] = info[4].strip()
                                houseinfo["year"] = info[5].strip()
                                houseinfo["banta"] = info[6].strip()
                                houseinfo["name"] = idname["name"]
                                houseinfo["junjia"] = idname["junjia"]
                                break
                        for m in l.find_all("div",class_="priceInfo"):
                            totalPrice = m.find("div", {"class": "totalPrice"}).find("span").text.strip()
                            unitPrice = m.find("div", {"class": "unitPrice"}).find("span").text.strip()
                            unitPrice = unitPrice.split("单价")[1].split("元")[0]
                            houseinfo["allprice"] = float(totalPrice)
                            houseinfo["danjia"] = float(unitPrice)
                            houseinfo["chajia"] = idname["junjia"] - houseinfo["danjia"]
                            break
                        if ((houseinfo["size"] < self.minsize) or (houseinfo["size"] > self.maxsize)):
                            continue
                        if ((houseinfo["allprice"] < self.minprice) or (houseinfo["allprice"] > self.maxprice)):
                            continue
                        if houseinfo in houselist:
                            continue
                        houselist.append(houseinfo)
                        if len(houselist) > self.housenum:
                            houselist.sort(key=lambda stu: stu["danjia"],reverse=True)
                            del houselist[0]
                    #break
        #根据页数获取每页小区信息
        if pagenum > 1:
            for num in range(2,pagenum+1):
                urlxiaoqu = "https://cq.lianjia.com/ershoufang/pg%die2sf1c%s/" % (num,idname["id"])
                self.mtLogBox.AppendText("正在抓取%s区小区：%s的第%d页数据，请等待。。。耗时:%s\n" % (self.quyu,idname["name"],num,datetime.datetime.now().replace(microsecond=0) - self.begintime))
                try:
                    f = requests.get(urlxiaoqu,timeout = 15,headers=self.headers)
                except Exception as e:
                    self.mtLogBox.AppendText("GetXiaoqu_Houses 2 requests.get error\n")
                    print(e)
                    continue
                soup = BeautifulSoup(f.content,"lxml")
                for i in soup.find_all("div",class_='leftContent'):
                    for j in  i.find_all("ul",class_="sellListContent"):
                        for k in j.find_all("li",class_="clear LOGVIEWDATA LOGCLICKDATA"):
                            # u = k.find("a",{"class":"noresultRecommend img LOGCLICKDATA"}).get("href")
                            # if self.iszhuzhai(u) == False:
                            #     continue
                            for l in k.find_all("div",class_="info clear"):
                                houseinfo = {"name":"","huxing":"","size":0,"turn":"","isjz":"","loucen":"","year":"","banta":"","allprice":0,"danjia":0,"junjia":0,"chajia":0}
                                for m in l.find_all("div",class_="houseInfo"):
                                    info = m.get_text()
                                    info = info.split("|")
                                    if len(info) == 7:
                                        houseinfo["huxing"] = info[0].strip()
                                        houseinfo["size"] = float(info[1].split("平米")[0].strip())
                                        houseinfo["turn"] = info[2].strip()
                                        houseinfo["isjz"] = info[3].strip()
                                        houseinfo["loucen"] = info[4].strip()
                                        houseinfo["year"] = info[5].strip()
                                        houseinfo["banta"] = info[6].strip()
                                        houseinfo["name"] = idname["name"]
                                        houseinfo["junjia"] = idname["junjia"]
                                        break
                                for m in l.find_all("div",class_="priceInfo"):
                                    totalPrice = m.find("div", {"class": "totalPrice"}).find("span").text.strip()
                                    unitPrice = m.find("div", {"class": "unitPrice"}).find("span").text.strip()
                                    unitPrice = unitPrice.split("单价")[1].split("元")[0]
                                    houseinfo["allprice"] = float(totalPrice)
                                    houseinfo["danjia"] = float(unitPrice)
                                    houseinfo["chajia"] = idname["junjia"] - houseinfo["danjia"]
                                    break
                                if ((houseinfo["size"] < self.minsize) or (houseinfo["size"] > self.maxsize)):
                                    continue
                                if ((houseinfo["allprice"] < self.minprice) or (houseinfo["allprice"] > self.maxprice)):
                                    continue
                                if houseinfo in houselist:
                                    continue
                                houselist.append(houseinfo)
                                if len(houselist) > self.housenum:
                                    houselist.sort(key=lambda stu: stu["danjia"],reverse=True)
                                    del houselist[0]
                            #break
        houselist.sort(key=lambda stu: stu["danjia"],reverse=False)
        return houselist
    
    #判断是否为住宅，暂时为使用该函数
    def iszhuzhai(self,url):
        try:
            f = requests.get(url,timeout = 15,headers=self.headers)
        except Exception as e:
            self.mtLogBox.AppendText("GetXiaoqu_Houses 3 requests.get error\n")
            print(e)
            return False
        soup = BeautifulSoup(f.content,"lxml")
        for i in soup.find_all("div",class_='box-l'):
            for j in i.find_all("div",class_="transaction"):
                mem = j.find("div",{"class":"content"}).get_text().strip()
                if "普通住宅" in mem:
                    return True
                else:
                    return False
            
        
        
                        

        