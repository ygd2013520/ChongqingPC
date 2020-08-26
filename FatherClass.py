# -*- coding: utf-8 -*-
#父类
import xlwt
import datetime
dictinfo = {"chajia":"差(面-总)","huxing":"户型","size":"大小(平米)","turn":"朝向","isjz":"是否精装","junjia":"均价(元)",\
    "loucen":"楼层","year":"年代","banta":"板塔","allprice":"总价(万)","danjia":"单价(元)","name":"小区名字"}

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
        self.begintime = None
    
    def GetAllXioayuID_Quyu(self):
        pass
    def GetAll_Houses(self):
        pass
    def GetXiaoqu_Houses(self,idname):
        pass
    #判断是否为住宅
    def iszhuzhai(self,url):
        pass
    def WriteDataToExcel(self,filepath, listdata = []):
        if len(listdata) == 0:
            return
        #excel内容居中
        alignment = xlwt.Alignment() # Create Alignmen
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style_jz = xlwt.XFStyle()
        style_jz.alignment = alignment
        #excel内容居中，背景色颜色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 5 #黄色
        style_jz_ys = xlwt.XFStyle()
        style_jz_ys.pattern = pattern
        style_jz_ys.alignment = alignment
        
        book = xlwt.Workbook() #创建一个Excel
        sheet1 = book.add_sheet('排序数据',cell_overwrite_ok=True) #在其中创建一个名为hello的sheet
        #print(listdata)
        i = 0 #行序号
        for app in listdata : #遍历list每一行
            if i == 0:
                k = 0
                for x in app : #遍历该行中的每个内容（也就是每一列的）
                    sheet1.write(i, k, dictinfo[x],style_jz_ys) #在新sheet中的第i行第j列写入读取到的x值
                    k = k+1 #列号递增
                i = 1
            j = 0 #列序号
            for x in app : #遍历该行中的每个内容（也就是每一列的）
                sheet1.write(i, j, app[x],style_jz) #在新sheet中的第i行第j列写入读取到的x值
                j = j+1 #列号递增
            i = i+1 #行号递增
        book.save(filepath) #创建保存文件
