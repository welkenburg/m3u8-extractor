import requests

def download(url,name,mode="wb"):
	r = requests.get(url, stream=True)
	with open(name, mode) as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
	return name

def makeVideo(videoName,fileName="neko.m3u8"):
    with open(fileName, 'r') as i:
        file = i.read().split("\n")
        for line in file:
            if len(line) > 0 and line[0] != "#":
                download(f"{line}",f"videos/{videoName}.ts",'ab')
                print(line.split("/")[-1])
    print(f"DONE !")

def makeVideoFromFile(fileName):
    with open(fileName, "r") as infile:
        for line in infile.read().split("\n"):
            makeVideo(line.split("#")[1],line.split("#")[0])

makeVideoFromFile("snk.txt")