# -*- coding: UTF-8 -*-
from multiprocessing import Manager, Process
import os

def run(d, a):
    a.append(str(os.getpid()))
    d[str(os.getpid())] = [os.getpid()]
    print 'PID: %d ,%s,%s' %(os.getpid(),d,a)

if __name__ == "__main__":
    mgr = Manager()
    share_dict = mgr.dict()
    share_list = mgr.list()
    jobs = [Process(target=run, args=(share_dict,share_list)) for i in range(8)]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
