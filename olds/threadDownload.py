import requests
import threading

stack = {}
threads = []

def writeTofile(name,chunks,mode="ab"):
    with open(name, mode) as out:
        for chunk in chunks:
            out.write(chunk)

def download(url,name):
    chunks = []
    try:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                chunks.append(chunk)
        stack[name] = chunks
    except:
        print(f"ERROR on thread {name}")

def getm3u8(url,name="video.m3u8"):
    download(url,"m3u8")
    writeTofile(name,stack["m3u8"])

def makeVideo(name,path=None,url=None):
    if url != None:
        root = "/".join(url.split("/")[:-1]) + "/"
        path = getm3u8(url)
    else:
        root = ""
    
    with open(path,"r") as infile:
        lines = [i for i in infile.read().split('\n') if (not "#" in i and i != "")]
        for i in range(1,len(lines)+1):
            # print(lines[i-1])
            t = threading.Thread(name=i, target=download, args=(f"{root}{lines[i-1]}",i))
            threads.append(t)
            t.start()
    
    with open(f"videos/{name}.ts","ab") as out:
        for t in threads:
            print(" " * 100, end="\r")
            print(f"downloading... {int(t.name)}/{len(lines)} done", end="\r")
            t.join()
            for chunk in stack[t.name]:
                out.write(chunk)
        print(" " * 100, end="\r")
        print("downloaing done !")

if __name__ == "__main__":
    # with open("videos.txt","r") as videos:
    #     lines = [l.split("#") for l in videos.read().split("\n")]
    #     for line in lines:
    #         print(f"\n##### {line[1]} starting #####")
    #         makeVideo(line[1],url=line[0])
    makeVideo("slime",path="neko.m3u8")