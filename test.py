# -*- coding: utf-8 -*-
"""
author:xieguozhong
email:superxgz@gmail.com
 
修订历史：
V0.3 2009-04-30
1 修改为实时跟踪日志
2 将原来的按钮修正为"启动,暂停,复制,清除"
 
V0.2 2009-03-13
1 增加了初始化文件时就定位到日志结尾,无须再点"Clear"按钮
2 增加了复制按钮
3 增加了最小化按钮
4 增加了日志显示框的横拉条,并使显示框为只读
5 增加了JBOSS路径的保存功能,可以删除和增加
 
V0.1 不记得了
 
"""
import wx
import os
import time
import threading
from wx.lib.wordwrap import wordwrap
import wx.lib.buttons as buttons
import wx.richtext as rt
import sqlite3
 
class LogViewFrame(wx.Frame):
 
    objFile = None
    filename = "logview.conf"
    currentState = 0    # 0表示停止状态 1表示监视状态
    def __init__(self):
        wx.Frame.__init__(self, 
                          parent=None, 
                          id=-1, 
                          title="Jboss日志查看器 V0.3", 
                          pos=wx.DefaultPosition,
                          size=(800,600),
                          style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER |wx.MAXIMIZE_BOX),
                          name="mainFrame"
                          )
        #创建画板对象
        panel = wx.Panel(self)
 
        wx.StaticText(panel, -1,
                      "Jboss目录",
                      pos=(10,5)
                      )
        logList = self.controlConf("r","")
        self.tcJbossLogPath = wx.ComboBox(panel, -1, "", pos=(70,2), size=(350,25), choices=logList, style=wx.CB_DROPDOWN)
         
        #创建一个用于选择Jboss日志目录的按钮
        self.btGetJbossLogPath = wx.Button(panel, label="...", pos=(420, 2), size=(20, 25))
         
        #增加保存JBOSS地址按钮
        self.btSavePath = wx.Button(panel, label="＋", pos=(440, 2), size=(20, 25))
         
        #增加删除JBOSS地址按钮
        self.btDelPath = wx.Button(panel, label="－", pos=(460, 2), size=(20, 25))
         
        #创建开始按钮
        self.btStart = buttons.GenButton(panel, label="▲start", pos=(490, 2), size=(70, 25))
        self.btStart.SetForegroundColour("green")
         
        #创建暂停按钮
        self.btPause = buttons.GenButton(panel, label="〓pause", pos=(560, 2), size=(70, 25))
        #btStart.SetForegroundColour("green")
         
        #创建复制按钮
        self.btCopy = wx.Button(panel, label="◎copy", pos=(630, 2), size=(70, 25))
         
        #创建清理按钮
        self.btClear = wx.Button(panel, label="□clear", pos=(700, 2), size=(70, 25))
         
        #创建显示日志框
        self.mtLogBox = wx.TextCtrl(panel, -1,"", pos=(2,28), size=(795, 540), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY) 
 
                                 
        #下面开始绑定按钮和事件的关联
        self.Bind(wx.EVT_BUTTON, self.OnGetJbossLogPath, self.btGetJbossLogPath)
        self.Bind(wx.EVT_BUTTON, self.OnCopy, self.btCopy)
         
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.btStart)
        self.Bind(wx.EVT_BUTTON, self.OnPause, self.btPause)
         
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.btClear)
         
         
        self.Bind(wx.EVT_BUTTON, self.OnSavePath, self.btSavePath)
        self.Bind(wx.EVT_BUTTON, self.OnDelPath, self.btDelPath)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) 
 
         
    #下面是公共事件
    def onInitobjFile(self):
        if self.objFile == None:
            strJbossPath = self.tcJbossLogPath.GetValue().strip()
            if strJbossPath == "":
                wx.MessageBox("请先选择Jboss所在目录", "错误")
                return 1
            strJbossPath = strJbossPath + "/server/default/log/server.log"
            if not os.path.exists(strJbossPath):
                wx.MessageBox("Jboss日志文件不存在", "错误")
                return 1
            self.objFile = open(strJbossPath,"r")
             
            #初始化打开文件时,先移动到文本尾端
            sline = self.objFile.readline()
            while sline:
                sline = self.objFile.readline()
                 
        return 0
 
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
 
 
    #下面是响应事件
     
    def OnClear(self, event):
        #先保存好currentState原来的值,在清理动作完成后,要还原这个状态
        oldcurrentState = self.currentState
        self.currentState = 0
        self.mtLogBox.Clear()
         
        if self.objFile:
            sline = self.objFile.readline()
            while sline:
                sline = self.objFile.readline()
        self.currentState = oldcurrentState
     
    def OnPause(self, event):
 
        if self.objFile:
            if self.currentState == 0:
                self.currentState = 1
                self.btPause.SetLabel('〓pause')
                self.btPause.SetForegroundColour("black")
                if not self.readingThreading.isAlive():
                    self.readingThreading = None
                    self.readingThreading = threading.Thread(None,self.realTimeMonitorLog)
                    self.readingThreading.start()
            else:
                self.currentState = 0
                self.btPause.SetLabel('〓continue')
                self.btPause.SetForegroundColour("blue")
     
    def OnStart(self, event):
        if self.currentState == 0:
            
            #初始化日志文件对象,如果路径不对就返回
            if self.onInitobjFile():
                return
             
            self.btStart.SetLabel('■stop')
            self.btStart.SetForegroundColour("red")
            self.currentState =  1
             
            #初始化成功后,调用realTimeMonitorLog方法显示日志
            self.readingThreading = threading.Thread(None,self.realTimeMonitorLog)
            self.readingThreading.start()     
        else:
            self.currentState = 0
            if self.objFile != None:
                self.objFile.close()
                self.objFile = None
                 
            self.btStart.SetLabel('▲start')
            self.btStart.SetForegroundColour("green")
             
     
    def realTimeMonitorLog(self):
        while self.currentState == 1:
            sline = self.objFile.readline()
            while sline:
                self.mtLogBox.AppendText(sline)
                if self.currentState == 1:
                    sline = self.objFile.readline()
                else:
                    sline = None
            time.sleep(1)
     
    def OnGetJbossLogPath(self, event):
        path = self.showDirDialog("请选择Jboss所在目录")
        if path:
            self.tcJbossLogPath.Clear()
            self.tcJbossLogPath.WriteText(path)
 
    def OnCloseWindow(self, event):
        self.currentState = 0
        time.sleep(1)
        if self.objFile != None:
            self.objFile.close()
            self.objFile = None
        self.Destroy()
         
    def OnCopy(self, event):
        self.mtLogBox.SelectAll()
        self.mtLogBox.Copy()
     
    def OnSavePath(self, event):
        self.controlConf("a",self.tcJbossLogPath.GetValue())
         
    def OnDelPath(self, event):
        self.controlConf("d",self.tcJbossLogPath.GetValue())
         
    def controlConf(self, m, s):
        """
        m的参数 r 代表读  a 代表增加 d 代表删除
        s jboss路径
        """
        conn = sqlite3.connect("wb.db3")
        stmt = conn.cursor()
        conn.execute("create table if not exists jboss(id integer primary key autoincrement, path text)")
        paths = None
        if m == 'r':
            paths = []
            stmt.execute("select trim(path) from jboss order by id")
            rs = stmt.fetchall()
            for row in rs:
                paths.append(row[0])
             
        elif m == 'a':
            if s is None or s.strip() == '':
                wx.MessageBox("JBOSS路径不能为空", "错误")
            else:
                s = s.strip()
                stmt.execute("select id from jboss where path = ? limit 1",s)
                if stmt.fetchone[0][0] > 0:
                    wx.MessageBox('"' + s + '"已存在', "错误")
                else:
                    stmt.execute("insert into jboss(path) values(?)",s)
        stmt.close()
        conn.close()
        return paths
 
class LogViewApp(wx.App):
    def OnInit(self):
        self.mainFrame = LogViewFrame()
        self.mainFrame.Show()
        self.SetTopWindow(self.mainFrame)
        return True
 
if __name__ == "__main__":
    logviewApp = LogViewApp()
    logviewApp.MainLoop()