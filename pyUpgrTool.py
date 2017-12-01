from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
import re
import os

class StatusBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._lblState = Label(self, text='', bd=2, relief=SUNKEN, width=15, anchor = W)
        self._lblState.pack(side=LEFT)

class UpgrTool(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(side=TOP, fill=BOTH, expand=YES)
        self.iniCtrls()
        self.bind("<Destroy>", self.onDestroy)
    def iniCtrls(self):
        frmTop = Frame(self)
        frmTop.pack(side=TOP, fill=X)
        
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.status_bar.config(bd=2, relief=SUNKEN)

        frmMiddle = Frame(self)
        frmMiddle.pack(fill=BOTH, expand=YES)

        self.btnCheckScripts = Button(frmTop, text='Check scripts',  command=self.onCheckScripts)
        self.btnCheckScripts.pack(side=LEFT, padx=5, pady=5)

        Button(frmTop, text='Clear',  command=self.onClear).pack(side=RIGHT, padx=5, pady=5)
        
        self.st = ScrolledText(frmMiddle, font=('courier', 9, 'normal'))
        self.st.pack(side=TOP, fill=BOTH, expand=YES)
    def onCheckScripts(self):
        root_name = r'C:\Users\KSHIPKOV\Documents\SVN\HS\Materials\Source code\Oracle\48to96\Output'

        # K1/B
        self.st.insert(END, '\n')
        flag = True
        dname = os.path.join(root_name, 'K1', 'B')
        self.st.insert(END, 'Проверка наличия вызовов скриптов из %s\n' % (dname))
        names = [fname.lower() for fname in os.listdir(dname) if (os.path.isfile(os.path.join(dname, fname)))] # список скриптов в каталоге
        d = {} # Словарь для имён вызываемых скриптов
        me = re.compile(r'@@K1\\B\\(.*)')
        with open(os.path.join(root_name, "K1_B.sql")) as fh: # Парсим головной скрипт для получения имён вызываемых скриптов
            for line in fh:
                mo = me.match(line)
                if mo:
                    filename = mo.group(1)
                    d[filename.lower()] = 1 # Заносим в словарь имя вызываемого скрипта
        for x in names:
            if not x in d:
                self.st.insert(END, 'Не вызывается скрипт: ' + x + '\n')
                flag = False
        if flag:
            self.st.insert(END, 'OK\n')

        # K2/B
        self.st.insert(END, '\n')
        flag = True
        dname = os.path.join(root_name, 'K2', 'B')
        self.st.insert(END, 'Проверка наличия вызовов скриптов из %s\n' % (dname))
        names = [fname.lower() for fname in os.listdir(dname) if (os.path.isfile(os.path.join(dname, fname)))] # список скриптов в каталоге
        d = {} # Словарь для имён вызываемых скриптов
        me = re.compile(r'@@K2\\B\\(.*)')
        with open(os.path.join(root_name, "K2_B.sql")) as fh: # Парсим головной скрипт для получения имён вызываемых скриптов
            for line in fh:
                mo = me.match(line)
                if mo:
                    filename = mo.group(1)
                    d[filename.lower()] = 1 # Заносим в словарь имя вызываемого скрипта
        for x in names:
            if not x in d:
                self.st.insert(END, 'Не вызывается скрипт: ' + x + '\n')
                flag = False
        if flag:
            self.st.insert(END, 'OK\n')
    def onClear(self):
        self.st.delete('1.0', END)
    def onDestroy(self, event):
        pass

if __name__ == '__main__':
    root = Tk()
    root.title("UpgrTool")
    UpgrTool(root).mainloop()
