from os import *
from os.path import *
import Tkinter
from shutil import copyfile
from PIL import Image, ImageTk
import pprint
from googleapiclient.discovery import build

dir_path = 'C:/Users/Chat/Desktop/SNES ROMS'
sort_path = dir_path + '/tri'
add_path = dir_path + '/A ajouter'
rem_path = dir_path + '/A tej'
files = [f for f in listdir(sort_path) if isfile(join(sort_path, f))]

apikey = 'AIzaSyBQ5EGq99YoBhDgUq3Rzon8iC51O_M5TGM'
searchengineid = '011053369210583291579:rynh5hhuntg'


class Frame(Tkinter.Tk):
    global files
    def __init__(self,parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        buttonAdd = Tkinter.Button(self, text=u"Add", command=self.ClickAdd)
        buttonAdd.grid(column=1, row=0)

        buttonRem = Tkinter.Button(self, text=u"Remove", command=self.ClickRem)
        buttonRem.grid(column=1, row=1)

        self.labelText = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelText, anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=0, sticky='EW')
        self.labelText.set(files[0])

        self.gamename = files[0][:files[0].find('(')]
        getImages(self.gamename, add_path)

    def ClickAdd(self):
        dest = add_path
        self.doDefaultFileManage(dest)

    def ClickRem(self):
        dest = rem_path
        self.doDefaultFileManage(dest)

    def doDefaultFileManage(self, dest):
        copyfile(sort_path + '/' + files[0], dest + '/' + files[0])
        remove(sort_path + '/' + files[0])
        files.remove(files[0])
        self.labelText.set(files[0])
        self.gamename = files[0][:files[0].find('(')]

def getImages(query, path):
    query += 'snes'
    print(query)
    service = build('customsearch', 'v1', developerKey=apikey)
    res = service.cse().list(q='bob', cx=searchengineid, searchType='image').execute()
    print(res)




"""" 
fetcher = urllib2.build_opener()
    startIndex = 0

    for j in range(0, 9):
        searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + query + "&start=" + str(startIndex)
        f = fetcher.open(searchUrl)
        deserialized_output = simplejson.load(f)
        # 4 images sent at a time
        for i in range(0, 3):
            imageUrl = deserialized_output['responseData']['results'][i]['unescapedUrl']
            file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
            print(file)
            try:
                Image.open(file).save(open(path.join(path, '%s.jpg') % ((i + 1) * startIndex), 'w'), 'JPEG')
            except IOError:
                continue
            finally:
                file.close()

        startIndex += 4
"""


#MAIN
app = Frame(None)
app.title('sneSort')
app.mainloop()
