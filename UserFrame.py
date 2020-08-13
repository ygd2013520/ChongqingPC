#coding=utf-8
import wx
import os


class UserFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None):
        wx.Frame.__init__(self, parent, id, title=u'登录界面', size=(400, 200), pos=wx.DefaultPosition,style=wx.MINIMIZE_BOX | wx.SIMPLE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN )
        self.UpdateUI = UpdateUI
        self.InitUI() # 绘制UI界面
        self.Center()
           
    def InitUI(self):
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
        self.login_button = wx.Button(self.panel,label=u"确认", pos=(150, 90), size=(105, 28))

        self.Bind(wx.EVT_BUTTON, self.loginSys, self.login_button)

    def loginSys(self, event):
        password = self.passwordInput.GetValue()
        self.loginFunction(password)

    def loginFunction(self, password):
        if password == "123456":
            self.UpdateUI(1)
            self.passwordInput.Clear()
        else:
            wx.MessageBox(u"密码错误，重新输入密码！", u"登录错误" ,wx.OK|wx.ICON_INFORMATION) 
