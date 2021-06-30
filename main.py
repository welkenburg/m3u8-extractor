import os
import sys
import requests
import concurrent.futures
import time

from progressbar import *
from options import *

class m3u8:
    def __init__(self,file,name,date = None):
        self.urls = self.exctractUrls(file)
        self.name = name
        self.date = date
        self.id   = 0

    def exctractUrls(self,raw : str):
        urls = []
        for line in raw.split("\n"):
            if len(line) > 0 and line[0] != "#":
                if line[:4] != "http" and currentOptions['root'] == "":
                    currentOptions['root'] = input("Warning : the m3u8 file(s) does not countains the base url of its ts files.\nYou can provide it by writing ' -r [root]' or here :\n")
                urls.append(currentOptions['root'] + line) if line[:4] != 'http' else urls.append(line)
        return urls

    def download(self):
        timer = time.perf_counter()
        
        if currentOptions['outputFolder'] not in os.listdir("."):
            os.mkdir(currentOptions['outputFolder'])

        #if a file has the same name, change the current file name to something(x)
        counter = 1
        self.finalName = self.name
        while self.finalName in os.listdir(currentOptions['outputFolder']):
            counter += 1
            self.finalName = f"{self.name} {counter}"

        for i in range(len(self.urls)):

            if currentOptions['verbose']:
                progressBarWidth = 50
                percentage = i / len(self.urls)
                self.printf(f'\r|{"*"*int(percentage*progressBarWidth) + " "*(progressBarWidth-int(percentage*progressBarWidth))}| {int(percentage*100)}%\t{self.finalName}')

            with open(f"{currentOptions['outputFolder']}/{self.name}.ts", "ab") as f:
                try:
                    r = requests.get(self.urls[i], stream=True)
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                except:
                    self.printf(f'Failed to download {self.finalName[20:]} -> connection error ?')
                    return 0 # connection issue or idk pakage loss ?

        return 1

    def printf(self,message):
        c = queryMousePosition()        # get cursor position
        move(self.id + 1, 0)            # move cursor to wanted position
        addstr(message)                 # prints wanted text
        move(c.y, c.x)                  # and go back to the previous cursor position


def throwError(message,doexit=True):
    print(message)
    if(doexit):
        print("\ttry 'u8 -h' for more info\n")
        exit()

def getLocalFile(file, index=None):
    try:
        with open(file,"r") as video:
            content = video.read()
            return m3u8(content, ' '.join(file.split('/')[-1].split('.')[:-1]) if currentOptions['videoName'] == None else currentOptions['videoName'] + f'{index+1}'*(index!=None), os.path.getctime(file))
    finally:
        if currentOptions['deleteFiles']:
            os.remove(file)
    

def getFiles(file):

    #case a link is provided
    if file[:4] == "http":
        r = requests.get(file, stream=True)
        content = ""
        for chunk in r.iter_content(chunk_size=1024):
            content += chunk.decode("utf-8")
        return [m3u8(content, file.split('/')[-1][:-5] if currentOptions['videoName'] == None else currentOptions['videoName'])]

    #case single m3u8 file
    if file.split(".")[-1] == "m3u8":
        return [getLocalFile(file)]
    
    def sortByDate(videos:m3u8):
        return sorted(videos,key = lambda x: x.date)

    #case a folder is provided
    if file in os.listdir("."):
        filenames = os.listdir(f"./{file}")
        m3u8s = [getLocalFile(f"{file}/{filenames[i]}",i) for i in range(len(os.listdir(f"./{file}"))) if filenames[i].endswith(".m3u8")]
        return sortByDate(m3u8s)

def lauchThreads(nb, videos):
    threads = []
    iterations = min(nb, len(videos))
    for i in range(iterations):
        t = concurrent.futures.ThreadPoolExecutor().submit(videos[i].download)
        threads.append(t)

    for t in threads:
        t.result()


    return videos[iterations:], True if videos[iterations:] != [] else False

def main(file):
    m3u8s = getFiles(file)

    # attribute an id to every file
    for i in range(len(m3u8s)):
        m3u8s[i].id = i

    if m3u8s:
        running = True
        while running:
            m3u8s, running = lauchThreads(currentOptions['threadsNumber'], m3u8s)
    
        #os.system('cls' if os.name=='nt' else 'clear')
        print(f"done in {(time.perf_counter()-timer)//60}'" + f'{(time.perf_counter()-timer)%60:0.4f}"')

if __name__ == "__main__":

    # init the clock and clear the screen
    timer = time.perf_counter()
    os.system('cls' if os.name=='nt' else 'clear')

    if(len(sys.argv) < 2):
        throwError("\nusage : u8 [-options] [file(s)]")

    sys.argv.pop(0) # remove command name
    optionsSet = [(options.get(sys.argv[e]),e) for e in range(len(sys.argv)) if sys.argv[e][0] == '-'] # find the different option flags
    
    # redo that with a while loop

    for option in optionsSet: # trigger option
        try:
            nbArgs = len(inspect.signature(option[0].activate).parameters)
            if(nbArgs > 0):
                args = sys.argv[option[1]+1:option[1]+nbArgs+1]
                option[0].activate(*args)
            else:
                option[0].activate()
        except AttributeError:
            throwError(f"\nerror: invalid option '{sys.argv[option[1]]}'")
    
    file = sys.argv[-1]

    main(file)