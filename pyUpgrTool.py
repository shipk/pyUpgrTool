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
    def onScript(self):
        def t_dir(dname, lname):
            def t_file(name):
                s = ''
                s = s + 'prompt\n'
                s = s + 'prompt Exec ' + name + '\n'
                s = s + 'prompt ===========================\n'
                s = s + '@@' + server_name + '\\' + schema_name + '\\' + name + '\n'
                return s
            def t_ext(ext):
                names = [fname for fname in os.listdir(dname) if (os.path.isfile(os.path.join(dname, fname)) and fname.endswith('.' + ext))]
                s = ''
                for x in names:
                    s = s + t_file(x) + '\n'
                return s
            
            s = ''
            s = s + 'set define off\n'
            s = s + 'spool ' + lname + '\n'
            s = s + '\n'
            s = s + t_ext('tab')
            s = s + t_ext('vw')
            s = s + t_ext('mv')
            s = s + t_ext('sql') # Тоже с view
            s = s + t_ext('tps')
            s = s + t_ext('trg')
            s = s + t_ext('fnc')
            s = s + t_ext('prc')
            s = s + t_ext('pck')
            s = s + 'prompt All done.\n'
            s = s + '\n'
            s = s + 'spool off\n'
            s = s + '\n'
            return s

        root_name = r'C:\Users\KSHIPKOV\Documents\SVN\HS\Materials\Source code\Oracle\48to96\Output'
        s = ''
        server_names = [sname for sname in os.listdir(root_name) if os.path.isdir(os.path.join(root_name, sname))] 
        for server_name in server_names:
            schema_names = [sname for sname in os.listdir(os.path.join(root_name, server_name)) if os.path.isdir(os.path.join(root_name, server_name, sname))] 
            for schema_name in schema_names:
                s = s + 'file: ' + server_name + '_' + schema_name + '.sql\n'
                lname = server_name + '_' + schema_name + '.log'
                dname = os.path.join(root_name, server_name, schema_name)
                s = s + t_dir(dname, lname)

        self.st.insert(END, s)
    def onSubst1(self):
        s = self.st.get('1.0', END+'-1c')
        sr = ''
        ma = re.compile(r'(.*), nach([0-9]*),(.*)')
        for s1 in s.split('\n'):
            mo = ma.match(s1)
            if not mo is None: 
                g = mo.groups()
                s2 = g[0] + ', nullif(nach' + g[1] + ',0) nach' + g[1] + ','+ g[2]
            else:
                s2 = s1
            sr = sr + s2 + '\n'
        self.st.insert(END, '===================================================\n')
        self.st.insert(END, sr)
    def onClear(self):
        self.st.delete('1.0', END)
    def onDestroy(self, event):
        pass

if __name__ == '__main__':
    root = Tk()
    root.title("UpgrTool")
    UpgrTool(root).mainloop()
