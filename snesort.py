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

        self.usrpath.set('C:/Users/Chat/Desktop/SNES ROMS')

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

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        #Size of images/Buttons
        self.btwid = 200
        self.bthei = 160

        self.gamename = ''
        self.btnlist = []
        self.imgid = 0
        self.imgselected = False

        self.labelText = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelText, anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=0, sticky='EW')
        self.labelText.set(files[0])
        protip = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=protip, anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, sticky='EW')
        protip.set("Click on an image to save it as a cover when adding")
        buttonAdd = Tkinter.Button(self, text=u"Add", command=self.ClickAdd)
        buttonAdd.grid(column=1, row=0)
        buttonRem = Tkinter.Button(self, text=u"Remove", command=self.ClickRem)
        buttonRem.grid(column=2, row=0)

        self.gamename = files[0][:files[0].find('(')]
        getImages(self.gamename)

        for i in range(36):
            try:
                pic = Image.open(tmp_path + '/' + self.gamename + str(i) + '.png')
                pic = pic.resize((self.btwid, self.bthei), Image.NEAREST)
                tkpic = ImageTk.PhotoImage(pic)
            except IOError:
                print('image number ' + str(i) + ' is invalid')
            finally:
                bt = Tkinter.Button(self, image=tkpic, width=self.btwid,
                                    height=self.bthei, command=lambda cnt=i: self.SelectedImage(cnt))
                bt.grid(column=3 + (i % 5), row=i % 6)
                self.btnlist.append(bt)
                bt.image = tkpic
                bt.id = i

    def ClickAdd(self):
        dest = add_path
        self.sendFileToDirAndMove(dest)
        self.saveImage()
        getImages(self.gamename)
        self.changeButtonsForNewImages()

    def ClickRem(self):
        dest = rem_path
        self.sendFileToDirAndMove(dest)
        getImages(self.gamename)
        self.changeButtonsForNewImages()

    def SelectedImage(self, cnt):
        if self.imgselected is True:
            self.btnlist[self.imgid].config(bg='#40E0D0')
        else:
            self.imgselected = True
        self.imgid = self.btnlist[cnt].id
        self.btnlist[cnt].config(bg='red')


    def sendFileToDirAndMove(self, dest):
        #Copy file to adding or remove folder
        copyfile(dir_path + '/' + files[0], dest + '/' + files[0])
        remove(dir_path + '/' + files[0])
        #Get next file
        files.remove(files[0])
        self.labelText.set(files[0])
        self.gamename = files[0][:files[0].find('(')]

    def changeButtonsForNewImages(self):
        for i in range(36):
            try:
                pic = Image.open(tmp_path + '/' + self.gamename + str(i) + '.png')
                pic = pic.resize((self.btwid, self.bthei), Image.NEAREST)
                tkpic = ImageTk.PhotoImage(pic)
                self.btnlist[i].config(image=tkpic)
            except IOError:
                print('image number ' + str(i) + ' is invalid')
                self.btnlist[i].config(text='Invalid image', image=None)
            finally:
                self.imgselected = False

    def saveImage(self):
        print("img : " + tmp_path + '/' + self.gamename + str(self.imgid) + '.png' + " and p " + dir_path + '/' + self.gamename + '.png')
        copyfile(tmp_path + '/' + self.gamename + str(self.imgid) + '.png',
                 dir_path + '/' + self.gamename + '.png')



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
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]


def getImages(query):
    global dir_path

    if os.path.exists(tmp_path):
        rmtree(tmp_path)
    os.makedirs(tmp_path)

    print("query for " + '"' + query + '"')
    qquery = query + 'snes'
    try:
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
        res3 = service.cse().list(q=qquery, cx=searchengineid, searchType='image',
                                  start=res2['queries']['nextPage'][0]['startIndex']).execute()
        for item in res3['items']:
            urllib.urlretrieve(item['link'], tmp_path + '/' + query + str(cnt) + '.png')
            cnt += 1

        res4 = service.cse().list(q=qquery, cx=searchengineid, searchType='image',
                                  start=res3['queries']['nextPage'][0]['startIndex'], num=6).execute()
        for item in res4['items']:
            urllib.urlretrieve(item['link'], tmp_path + '/' + query + str(cnt) + '.png')
            cnt += 1
    except IOError:
        print('Invalid URL')


#MAIN
app = SettingFrame(None)
app.title('settings')
app.mainloop()
app2 = MainFrame(None)
app2.title('sneSort')
app2.mainloop()
print('removing tmp files...')
rmtree(tmp_path)
