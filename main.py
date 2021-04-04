import os
import sys
import requests
import concurrent.futures
import time

outFile = "video"

class m3u8:
    def __init__(self,file,name,root=""):
        self.urls = self.exctractUrls(file,root)
        self.name = name

    def exctractUrls(self,raw,root=""):
        urls = []
        for line in raw.split("\n"):
            if len(line) > 0 and line[0] != "#":
                if line[:4] != "http" and root == "":
                    root = input("\033[93mWarning : the m3u8 file does not countains the root of its ts files, make sure to provide it with the -r [root] option \033[0m \nroot : ")
                urls.append(root + line)
        return urls

    def download(self):
        timer = time.perf_counter()
        
        if "videos" not in os.listdir("."):
            pass
            #create the folder videos

        #if a file has the same name, change the current file name to something(x)
        counter = 0
        self.finalName = self.name
        while self.finalName in os.listdir("./videos"):
            counter += 1
            self.finalName = f"{self.name}({counter})"

        for url in self.urls:
            r = requests.get(url, stream=True)
            with open(f"videos/{self.name}.ts", "ab") as f:
                try:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                except:
                    print("\033[41mCRITICAL ERROR\033[0m\033[91m\tno internet connection \033[0m")
                    exit()

        # threads = []
        # for i in range(len(self.urls)):
        #     t = concurrent.futures.ThreadPoolExecutor().submit(self.downloadPacket,self.urls[i],i)
        #     threads.append(t)

        # results = {}
        # for t in threads:
        #     packet, n = t.result()
        #     results[n] = packet
        
        # with open(f"videos/{self.name}.ts", "ab") as f:
        #     for i in range(len(results)):
        #         f.write(results[i])

        # stop = f"{(time.perf_counter()-timer)//60}'" + f'{(time.perf_counter()-timer)%60:0.4f}"'
        # print(f"\033[92m{self.name} done in {stop} \033[0m")

        return 1
    
    def downloadPacket(self,url,n):
        packet = b''
        r = requests.get(url, stream=True)
        try:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    packet += chunk
        except:
            print("\033[41mCRITICAL ERROR\033[0m\033[91m\tno internet connection \033[0m")
            exit()
        return packet, n



def getFiles(file,url=None):
    m3u8s = []

    #case inFile is a text file
    if file.split(".")[-1] == "txt":
        with open(file, "r") as textFile:
            for link in textFile.read().split("\n"):
                r = requests.get(link.split("#")[0], stream=True)
                content = ""
                for chunk in r.iter_content(chunk_size=1024):
                    content += chunk.decode("utf-8")
                m3u8s.append(m3u8(content,link.split("#")[1] if link.split("#")[1] != "" else outFile ))
        return m3u8s

    #case a link is provided
    if file[:4] == "http":
        r = requests.get(file, stream=True)
        content = ""
        for chunk in r.iter_content(chunk_size=1024):
            content += chunk.decode("utf-8")
        return [m3u8(content, outFile)]

    #case single m3u8 file
    if file.split(".")[-1] == "m3u8":
        with open(f"{file}","r") as video:
            #delete m3u8
            return [m3u8(video.read(),outFile)]
    
    #case a folder is provided
    if file in os.listdir("."):
        root = ""
        if "root.txt" in os.listdir(f"./{file}"):
            root = open(f"{file}/root.txt").read()
        for i in os.listdir(f"./{file}"):
            if i.endswith(".m3u8"):
                with open(f"{file}/{i}","r") as video:
                    m3u8s.append(m3u8(video.read(),i[:-5] if i[:-5] != "" else outFile ,root))
                    #delete m3u8
        return m3u8s
    


if __name__ == "__main__":
    timer = time.perf_counter()

    if(len(sys.argv) < 2):
        print("\033[41mCRITICAL ERROR\033[0m\033[91m\tfile to read from is missing \033[0m")
        exit()

    elif(len(sys.argv) < 3):
        print(f"\033[93mWarning : the output file name is missing, default name : {outFile} \033[0m")
        _ , inFile, * flags = tuple(sys.argv)

    else:
        _ , inFile, outFile, * flags = tuple(sys.argv)

    m3u8s = getFiles(inFile , outFile)

    threads = []
    for m3u8 in m3u8s:
        t = concurrent.futures.ThreadPoolExecutor().submit(m3u8.download)
        threads.append(t)
    
    for t in threads:
        t.result()
    
    print(f"done in {(time.perf_counter()-timer)//60}'" + f'{(time.perf_counter()-timer)%60:0.4f}"')