import os
from os import *
from os.path import *
import Tkinter
import tkFileDialog
from shutil import copyfile
from shutil import rmtree
import urllib
from PIL import Image, ImageTk
from googleapiclient.discovery import build

dir_path = ''
add_path = ''
rem_path = ''
tmp_path = ''
files = []

apikey = 'AIzaSyBQ5EGq99YoBhDgUq3Rzon8iC51O_M5TGM'
searchengineid = '011053369210583291579:rynh5hhuntg'


class SettingFrame(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        lbl = Tkinter.Label(self, text="Please select the folder where the ROMs are", anchor="w", fg="white", bg="blue")
        lbl.grid(column=0, row=0, sticky='EW')

        self.usrpath = Tkinter.StringVar()
        txtFolder = Tkinter.Entry(self, textvariable=self.usrpath, width=50)
        txtFolder.grid(column=0, row=1)

        btnSelect = Tkinter.Button(self, text="Select folder", command=self.SelectFolder)
        btnSelect.grid(column=1, row=1)
        btnOK = Tkinter.Button(self, text="OK", command=self.ValidSettings)
        btnOK.grid(column=1, row=2)

    def SelectFolder(self):
        s = tkFileDialog.askdirectory()
        self.usrpath.set(s)

    def ValidSettings(self):
        setPath(self.usrpath.get())
        self.destroy()


class MainFrame(Tkinter.Tk):
    global files

    def __init__(self,parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        buttonAdd = Tkinter.Button(self, text=u"Add", command=self.ClickAdd)
        buttonAdd.grid(column=1, row=1)
        buttonRem = Tkinter.Button(self, text=u"Remove", command=self.ClickRem)
        buttonRem.grid(column=1, row=2)
        self.labelText = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelText, anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, sticky='EW')
        self.labelText.set(files[0])

        self.gamename = files[0][:files[0].find('(')]
        getImages(self.gamename)

    def ClickAdd(self):
        dest = add_path
        self.doDefaultFileManage(dest)

    def ClickRem(self):
        dest = rem_path
        self.doDefaultFileManage(dest)

    def doDefaultFileManage(self, dest):
        copyfile(dir_path + '/' + files[0], dest + '/' + files[0])
        remove(dir_path + '/' + files[0])
        files.remove(files[0])
        self.labelText.set(files[0])
        self.gamename = files[0][:files[0].find('(')]


def setPath(p):
    global dir_path, add_path, rem_path, tmp_path
    global files

    dir_path = p
    add_path = dir_path + '/To add'
    if not os.path.exists(add_path):
        os.makedirs(add_path)
    rem_path = dir_path + '/To remove'
    if not os.path.exists(rem_path):
        os.makedirs(rem_path)
    tmp_path = dir_path + '/tmp'
    os.makedirs(tmp_path)
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]


def getImages(query):
    global dir_path

    print("query for " + query)
    qquery = query + 'snes'
    service = build('customsearch', 'v1', developerKey=apikey)
    res = service.cse().list(q=qquery, cx=searchengineid, searchType='image').execute()
    cnt = 0
    for item in res['items']:
        urllib.urlretrieve(item['link'], tmp_path + '/' + query + str(cnt) + '.png')
        cnt += 1
    res2 = service.cse().list(q=qquery, cx=searchengineid, searchType='image', start=res['queries']['nextPage'][0]['startIndex']).execute()
    for item in res2['items']:
        urllib.urlretrieve(item['link'], tmp_path + '/' + query + str(cnt) + '.png')
        cnt += 1


#MAIN
app = SettingFrame(None)
app.title('settings')
app.mainloop()
app2 = MainFrame(None)
app2.title('sneSort')
app2.mainloop()
print('removing tmp files...')
rmtree(tmp_path)
