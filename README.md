# m3u8 extractor
author : welkenburg

language : python

transform m3u8 files / links to .ts files

```
usage : u8 [-options] [file(s)]
-h 		print this message
-n  [name] 	in case of one file, the output will be named [name], in case of multiple files, the ouputs will be maned [name]X with X an interger based on the date of creation of the inputs
-r  [r] 	provide the root url to download the files
-t  [nb] 	restrict the number of threads used by the program. default: 30
-v 		activate the verbose mode, more info will be printed on the screen
-d 		delete the input file (.m3u8) after downloading the file
-o  [out] 	change the ouput folder. default:'videos'
```

eg.
1. `u8 -v sources` will convert the playlist files in the folder `sources` and save the converted file in the `video` folder. Verbose mode is activated (`-v`) so loading bars will display to show the progress.

2. `u8 -n touhou -o touhou-episodes sources` will convert files in the `sources` folder, and will rename every file by a name begining with `touhou` + a number. Theses files will be saved in a `touhou-episodes` folder. If this one doesn't exist yet, the program will create a new folder and rename it appropriately.

**! Warning ! Loading bars are not pretty in linux**