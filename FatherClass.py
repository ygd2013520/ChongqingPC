# -*- coding: utf-8 -*-
#父类

class FatherClassPC():
    def __init__(self,quyu,minsize,maxsize,minprice,maxprice,housenum,xiaoqunum,mtLogBox):
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
        self.quyu = quyu
        self.minsize = minsize
        self.maxsize = maxsize
        self.minprice = minprice
        self.maxprice = maxprice
        self.housenum = housenum
        self.xiaoqunum = xiaoqunum
        self.mtLogBox = mtLogBox
        self.allXiaoquID_Quyu = []
    
    def GetAllXioayuID_Quyu(self):
        pass
    def GetAll_Houses(self):
        pass
    def GetXiaoqu_Houses(self,idname):
        pass
