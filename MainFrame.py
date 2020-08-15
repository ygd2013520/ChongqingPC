#coding=utf-8
import wx
import os
import _thread
import wx.lib.buttons as buttons

from publicinfo import *
from LjClass import *


class MainFrame(wx.Frame):
    def __init__(self,parent=None,id=-1,UpdateUI=None):
        wx.Frame.__init__(self, parent, id, title=u'控制主界面', size=(695, 600), pos=wx.DefaultPosition,style=wx.MINIMIZE_BOX | wx.SIMPLE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN )
        self.UpdateUI = UpdateUI
        self.InitUI() # 绘制UI界面
        self.Center() #使对话框居中
    
    def OnExit(self,event):
        wx.Exit()


    def InitUI(self):
        #font
        self.font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        self.Bind(wx.EVT_CLOSE,self.OnExit) #绑定退出按钮
        self.panel = wx.Panel(self)

        self.pingtaistatic = wx.StaticText(self.panel, -1,u'选择平台：',pos=(14,8),size=(75,30), style=0)
        self.pingtaiComboBox = wx.ComboBox(self.panel, -1, value =  u"链家", pos=(90, 5),size =(75,30),choices = m_pingtailist, style = wx.CB_READONLY)
        
        self.quyustatic = wx.StaticText(self.panel, -1,u'选择区域：',pos=(14,38),size=(75,30), style=0)
        self.quyuComboBox = wx.ComboBox(self.panel, -1, value =  u"江北区", pos=(90, 35),size =(75,30),choices = m_qulist, style = wx.CB_READONLY)
        

        wx.StaticText(self.panel, -1,u'最小面积(㎡)：',pos=(180,8),size=(80,33), style=0)
        self.minsizeInput = wx.TextCtrl(self.panel, -1, u'50', pos=(260, 6), size=(75, 25))
        self.minsizeInput.SetForegroundColour('black')
        self.minsizeInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'最大面积(㎡)：',pos=(180,38),size=(80,33), style=0)
        self.maxsizeInput = wx.TextCtrl(self.panel, -1, u'130', pos=(260, 36), size=(75, 25))
        self.maxsizeInput.SetForegroundColour('black')
        self.maxsizeInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'最低价格(万)：',pos=(350,8),size=(80,33), style=0)
        self.minpriceInput = wx.TextCtrl(self.panel, -1, u'60', pos=(430, 6), size=(75, 25))
        self.minpriceInput.SetForegroundColour('black')
        self.minpriceInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'最高价格(万)：',pos=(350,38),size=(80,33), style=0)
        self.maxpriceInput = wx.TextCtrl(self.panel, -1, u'130', pos=(430, 36), size=(75, 25))
        self.maxpriceInput.SetForegroundColour('black')
        self.maxpriceInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'每个小区(套)：',pos=(520,8),size=(80,28), style=0)
        self.housenumInput = wx.TextCtrl(self.panel, -1, u'3', pos=(600, 6), size=(75, 25))
        self.housenumInput.SetForegroundColour('black')
        self.housenumInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'小区数量(个)：',pos=(520,38),size=(80,28), style=0)
        self.xiaoqunumInput = wx.TextCtrl(self.panel, -1, u'200', pos=(600, 36), size=(75, 25))
        self.xiaoqunumInput.SetForegroundColour('black')
        self.xiaoqunumInput.SetFont(self.font)

        wx.StaticText(self.panel, -1, "保存目录:",pos=(14,78))
        self.FilePath = wx.ComboBox(self.panel, -1, "", pos=(70,75), size=(350,30), choices=[], style=wx.CB_DROPDOWN)
        #创建一个用于选择文件目录的按钮
        #self.GetFilePath = wx.Button(self.panel, label=u"选择", pos=(420, 73), size=(50, 30))
        self.GetFilePath = buttons.GenButton(self.panel, label=u"选择", pos=(420, 73), size=(50, 30))

        #开始按钮
        self.begin_button = buttons.GenButton(self.panel,label=u"开始", pos=(475, 73), size=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnStartFun, self.begin_button)
        self.begin_button.SetForegroundColour("blue")

        self.stop_button =buttons.GenButton(self.panel,label=u"停止", pos=(530,73), size=(50, 30))
        self.stop_button.SetForegroundColour("red")

        #创建清理按钮
        self.btClear = buttons.GenButton(self.panel, label=u"清除日志", pos=(585, 73), size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.btClear)
        #创建显示日志框
        self.mtLogBox = wx.TextCtrl(self.panel, -1,"", pos=(2,105), size=(675, 455), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY) 

        #下面开始绑定按钮和事件的关联
        self.Bind(wx.EVT_BUTTON, self.OnGetFilePath, self.GetFilePath)

    #清除显示日志框
    def OnClear(self, event):
        self.mtLogBox.Clear()

    #选择文件保存路径
    def OnGetFilePath(self, event):
        path = self.showDirDialog("请选择文件保存目录")
        if path:
            self.FilePath.Clear()
            self.FilePath.WriteText(path)

    #打开文件保存路径对话框
    def showDirDialog(self, dialogTitle):
        path = ""
        dlg = wx.DirDialog(self, dialogTitle,
                      style=wx.DD_DEFAULT_STYLE
                       #| wx.DD_DIR_MUST_EXIST
                       #| wx.DD_CHANGE_DIR
                       )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            path = path.replace("\\","/")
        dlg.Destroy()
        return path

    def OnStartFun(self,event):
        _thread.start_new_thread(self.OnStartFunThread,(0,))
    #开始抓取数据
    def OnStartFunThread(self,event):
        #获取界面设置的数据
        pingtai = self.pingtaiComboBox.GetValue().strip()
        quyu = self.quyuComboBox.GetValue().strip()
        minsize = int(self.minsizeInput.GetValue().strip())
        maxsize = int(self.maxsizeInput.GetValue().strip())
        minprice = int(self.minpriceInput.GetValue().strip())
        maxprice = int(self.maxpriceInput.GetValue().strip())
        housenum = int(self.housenumInput.GetValue().strip())
        xiaoqunum = int(self.xiaoqunumInput.GetValue().strip())
        path = self.FilePath.GetValue().strip()
        #参数异常判断
        if  maxsize == 0 or maxprice == 0 \
            or housenum == 0 or xiaoqunum == 0 \
            or path == "":
            wx.MessageBox("参数设置错误，请重新设置正确参数！！！", "错误信息")
            return
        #根据平台调用相应的类函数
        if pingtai == "链家":
            path = path + "/" + pingtai + quyu + ".xls"
            ljclass = LjClassPC(quyu,minsize,maxsize,minprice,maxprice,housenum,xiaoqunum,self.mtLogBox)
            ljclass.GetAllXioayuID_Quyu()
            allhouseslist = ljclass.GetAll_Houses()
            self.mtLogBox.AppendText("正在保存数据到文件：%s当中。。。\n" % path)
            WriteDataToExcel(path,allhouseslist)
            self.mtLogBox.AppendText("保存数据完成，整个过程已经全部完成！！！\n")
        elif pingtai == "58同城":
            pass
        elif pingtai == "贝壳网":
            pass
        elif pingtai == "安居客":
            pass
