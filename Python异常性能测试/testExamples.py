#coding: utf-8
from timer import timer


def do_something():
    a = 1


# 直接执行耗时操作
@timer
def test1():
    for _ in xrange(1000000):
        do_something()


# 耗时操作放在try中执行，不抛出错误
@timer
def test2():
    try:
        for _ in xrange(1000000):
            do_something()
    except Exception:
        do_something()
    else:
        pass
    finally:
        pass


# try放耗时操作中，try每一次操作，不抛出错误
@timer
def test3():
    for _ in xrange(1000000):
        try:
            do_something()
        except Exception:
            do_something()
        else:
            pass
        finally:
            pass


# try放耗时操作中，try每一次操作并进行异常处理(捕捉抛出的异常)
@timer
def test4():
    zero = 0
    for _ in xrange(1000000):
        try:
            if zero == 0:
                raise ZeroDivisionError
        except ZeroDivisionError:
            do_something()
        else:
            pass
        finally:
            pass


# try放耗时操作中，try每一次操作并进行异常处理(捕捉所有异常 try...except BaseException)
@timer
def test5():
    zero = 0
    for _ in xrange(1000000):
        try:
            if zero == 0:
                raise ZeroDivisionError
        except BaseException:
            do_something()
        else:
            pass
        finally:
            pass


# try放耗时操作中，try每一次操作并进行异常处理(捕捉所有异常 不带任何异常类型)
@timer
def test6():
    zero = 0
    for _ in xrange(1000000):
        try:
            if zero == 0:
                raise ZeroDivisionError
        except:
            do_something()
        else:
            pass
        finally:
            pass


# 耗时操作放在except中
@timer
def test7():
    zero = 0
    try:
        if zero == 0:
            raise ZeroDivisionError
    except ZeroDivisionError:
        for _ in xrange(1000000):
            do_something()
    else:
        pass
    finally:
        pass


# 防御式编码
@timer
def test8():
    zero = 0
    for _ in xrange(1000000):
        if zero == 0:
            do_something()


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
