# -*- coding: utf-8 -*-
#继承父类的子类
from FatherClass import *

class LjClassPC(FatherClassPC):
    def GetMessage(self):
        self.mtLogBox.AppendText("mes test\n")
        pass