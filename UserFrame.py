#coding=utf-8
import wx
import os
import win32com.client 

class UserFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None):
        wx.Frame.__init__(self, parent, id, title=u'密码验证', size=(400, 200), pos=wx.DefaultPosition,style=wx.MINIMIZE_BOX | wx.SIMPLE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN )
        self.UpdateUI = UpdateUI
        self.InitUI() # 绘制UI界面
        self.Center()
           
    def InitUI(self):
        #判断程序是否运行
        if self.proc_exist("main.exe"):
            wx.MessageBox(u"程序已经运行，不能再次运行！",u"运行警告",wx.OK|wx.ICON_INFORMATION)
            wx.Exit()
        #创建panel
        self.panel = wx.Panel(self)
        #font
        self.font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        #密码输入框
        self.passwordInput = wx.TextCtrl(self.panel, -1, u'', pos=(150, 40), size=(105, 28), style=wx.TE_PASSWORD)
        self.passwordInput.SetHint(u"请输入密码")
        self.passwordInput.SetForegroundColour('black')
        self.passwordInput.SetFont(self.font)

        #确认按钮
        self.login_button = wx.Button(self.panel,label=u"登陆", pos=(150, 90), size=(105, 28))

        self.Bind(wx.EVT_BUTTON, self.loginSys, self.login_button)

    def loginSys(self, event):
        password = self.passwordInput.GetValue()
        self.loginFunction(password)

    def loginFunction(self, password):
        if password == "2020":
            self.UpdateUI(1)
            self.passwordInput.Clear()
        else:
            wx.MessageBox(u"密码错误，重新输入密码！", u"登录错误" ,wx.OK|wx.ICON_INFORMATION) 
    
    
    def proc_exist(self,process_name):
        is_exist = False
        wmi = win32com.client.GetObject('winmgmts:')
        processCodeCov = wmi.ExecQuery('select * from Win32_Process where name=\"%s\"' %(process_name))
        if len(processCodeCov) > 2:
            is_exist = True
        return is_exist
