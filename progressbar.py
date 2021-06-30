from ctypes import windll, Structure, c_long, c_wchar_p, c_ulong, c_void_p, byref

gHandle = windll.kernel32.GetStdHandle(c_long(-11))

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt

def move (y, x):
   value = x + (y << 16)
   windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong(value))


def addstr (string):
   windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(string), c_ulong(len(string)), c_void_p(), None)
