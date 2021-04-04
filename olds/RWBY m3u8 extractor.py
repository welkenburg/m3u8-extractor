import requests
import sys

def download(url,name,mode="wb"):
	r = requests.get(url, stream=True)
	with open(name, mode) as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
	return name

def makeVideo(url,videoName):
	root = "/".join(url.split("/")[:-1])
	m3u8 = download(url,"video.m3u8")

	with open(m3u8, 'r') as i:
		file = i.read().split("\n")
		maxFile = int(file[-3].split('/')[-1].split('.')[0][-5:])
		for line in file:
			if len(line) > 0 and line[0] != "#":
				download(f"{root}/{line}",f"videos/{videoName}.ts",'ab')
				print(f"{int(line.split('/')[-1].split('.')[0][-5:])}/{maxFile}", end="\r")
	print(f"{maxFile}/{maxFile} - DONE !")

	# sys.remove(m3u8)
	# not sure of what does that do 


if __name__ == "__main__":
	with open("videos.txt","r") as videos:
		lines = [tuple(l.split("#")) for l in videos.read().split("\n")]
		for line in lines:
			print(f"\n##### {line[1]} starting #####")
			makeVideo(line[0],line[1])
