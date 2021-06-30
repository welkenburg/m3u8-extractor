import inspect

class option:
    def __init__(self:object, flag:str, func, helpmessage:str):
        self.flag= flag
        self.helpmessage = helpmessage
        self.activate = func

def opHelp():
    #do little explanation paragraph
    
    for op in options.values():
        print(op.flag,end=" ")
        [print(f' [{args}]', end=" ") for args in inspect.signature(op.activate).parameters if args != 'self']
        print(f'\t{op.helpmessage}')
    print('')
    exit()

def opName(name):
    currentOptions['videoName'] = name

def opRoot(r):
    currentOptions['root'] = r

def opThreadnumbers(nb):
	currentOptions['threadsNumber'] = int(nb)

def opVerbose():
    currentOptions['verbose'] = True

def opDelete():
    currentOptions['deleteFiles'] = True

def opOutput(out):
    currentOptions['outputFolder'] = out

currentOptions = {
    'verbose' : False,
    'deleteFiles' : False,
    'videoName' : None,
    'outputFolder' : 'videos',
    'threadsNumber' : 30,
    'root': ''
}

options ={}
options['-h'] = option('-h', opHelp,            helpmessage=f'\tprint this message')
options['-n'] = option('-n', opName,            helpmessage=f"in case of one file, the output will be named [name], in case of multiple files, the ouputs will be maned [name]X with X an interger based on the date of creation of the inputs")
options['-r'] = option('-r', opRoot,            helpmessage=f'provide the root url to download the files')
options['-t'] = option('-t', opThreadnumbers,   helpmessage=f'restrict the number of threads used by the program. default: {currentOptions["threadsNumber"]}')
options['-v'] = option('-v', opVerbose,         helpmessage=f'\tactivate the verbose mode, more info will be printed on the screen')
options['-d'] = option('-d', opDelete,          helpmessage=f'\tdelete the input file (.m3u8) after downloading the file')
options['-o'] = option('-o', opOutput,          helpmessage=f"change the ouput folder. default:'{currentOptions['outputFolder']}'")