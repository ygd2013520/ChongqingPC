# -*- coding: utf-8 -*-
import xlwt 

urljiangbei = "https://cq.lianjia.com/xiaoqu/jiangbei/"     #江北区小区url
urlnanan = "https://cq.lianjia.com/xiaoqu/nanan/"       #南岸区小区url
urlbanan = "https://cq.lianjia.com/xiaoqu/banan/"       #巴南区小区url
urlyuzhong = "https://cq.lianjia.com/xiaoqu/yuzhong/"     #渝中区小区url
urlyubei = "https://cq.lianjia.com/xiaoqu/yubei/"       #渝北区小区url
urljiulongpo = "https://cq.lianjia.com/xiaoqu/jiulongpo/"       #九龙坡区url
urldadukou = "https://cq.lianjia.com/xiaoqu/dadukou/"     #大渡口区小区url
urlshapingba = "https://cq.lianjia.com/xiaoqu/shapingba/"   #沙坪坝区小区url

m_pingtailist = [u'链家', u'58同城', u'贝壳网', u'安居客']
m_qulist = [u'江北区', u'南岸区', u'巴南区', u'渝中区',u'渝北区', u'九龙坡', u'大渡口', u'沙坪坝']

m_stop = 0

def WriteDataToExcel(file = 'name.xls', list = []):
    book = xlwt.Workbook() #创建一个Excel
    sheet1 = book.add_sheet('hello') #在其中创建一个名为hello的sheet
    i = 0 #行序号
    for app in list : #遍历list每一行
        j = 0 #列序号
        for x in app : #遍历该行中的每个内容（也就是每一列的）
            sheet1.write(i, j, app[x]) #在新sheet中的第i行第j列写入读取到的x值
            j = j+1 #列号递增
        i = i+1 #行号递增
    book.save(file) #创建保存文件
