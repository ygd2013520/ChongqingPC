#coding=utf-8
import wx
import os

from globalinfo import *


class MainFrame(wx.Frame):
    def __init__(self,parent=None,id=-1,UpdateUI=None):
        wx.Frame.__init__(self, parent, id, title=u'控制主界面', size=(900, 500), pos=wx.DefaultPosition,style=wx.MINIMIZE_BOX | wx.SIMPLE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN )
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

         #确认按钮
        self.begin_button = wx.Button(self.panel,label=u"开始", pos=(120, 20), size=(50, 28))
        self.stop_button = wx.Button(self.panel,label=u"停止", pos=(225, 20), size=(50, 28))

        self.pingtaistatic = wx.StaticText(self.panel, -1,u'选择平台：',pos=(120,97),size=(75,33), style=0)
        self.pingtaiComboBox = wx.ComboBox(self.panel, -1, value =  u"链家", pos=(200, 95),size =(75,33),choices = m_pingtailist, style = wx.CB_READONLY)
        
        self.pingtaistatic = wx.StaticText(self.panel, -1,u'选择区域：',pos=(120,147),size=(75,33), style=0)
        self.pingtaiComboBox = wx.ComboBox(self.panel, -1, value =  u"江北区", pos=(200, 145),size =(75,33),choices = m_qulist, style = wx.CB_READONLY)
        

        wx.StaticText(self.panel, -1,u'最小面积(㎡)：',pos=(120,217),size=(80,33), style=0)
        self.minsizeInput = wx.TextCtrl(self.panel, -1, u'50', pos=(200, 215), size=(75, 25))
        self.minsizeInput.SetForegroundColour('black')
        self.minsizeInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'最大面积(㎡)：',pos=(120,257),size=(80,33), style=0)
        self.maxsizeInput = wx.TextCtrl(self.panel, -1, u'130', pos=(200, 255), size=(75, 25))
        self.maxsizeInput.SetForegroundColour('black')
        self.maxsizeInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'最低价格(万)：',pos=(120,307),size=(80,33), style=0)
        self.minpriceInput = wx.TextCtrl(self.panel, -1, u'60', pos=(200, 305), size=(75, 25))
        self.minpriceInput.SetForegroundColour('black')
        self.minpriceInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'最高价格(万)：',pos=(120,347),size=(80,33), style=0)
        self.maxpriceInput = wx.TextCtrl(self.panel, -1, u'130', pos=(200, 345), size=(75, 25))
        self.maxpriceInput.SetForegroundColour('black')
        self.maxpriceInput.SetFont(self.font)

        wx.StaticText(self.panel, -1,u'每个小区(套)：',pos=(120,387),size=(80,33), style=0)
        self.maxpriceInput = wx.TextCtrl(self.panel, -1, u'3', pos=(200, 385), size=(75, 25))
        self.maxpriceInput.SetForegroundColour('black')
        self.maxpriceInput.SetFont(self.font)