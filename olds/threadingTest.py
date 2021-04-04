import threading
import random
import time

def f(i):
    time.sleep(random.random())
    return f"yee {i}"

def go(mi):
    for i in range(mi):
        t = threading.Thread(target=f, args=(i,), name=i)
        t.start()
        print(t.name)

go(10)