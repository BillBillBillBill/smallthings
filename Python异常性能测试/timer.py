#coding: utf-8


def timer(func):
    import time
    def wrapper(*args, **kwargs):
        startTime = time.time()
        f = func(*args, **kwargs)
        endTime = time.time()
        passTime = endTime - startTime
        print "执行函数%s使用了%f秒" % (getattr(func, "__name__"), passTime)
        return f
    return wrapper
