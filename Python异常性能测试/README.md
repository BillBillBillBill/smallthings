前言
---
___
Python的异常处理能力非常强大，但是用不好也会带来负面的影响。我平时写程序的过程中也喜欢使用异常，虽然采取防御性的方式编码会更好，但是交给异常处理会起到偷懒作用。偶尔会想想异常处理会对性能造成多大的影响，于是今天就试着测试了一下。

Python异常(谷歌开源风格指南)
---
___
**tip:**
    允许使用异常, 但必须小心。
 
**定义:**
    异常是一种跳出代码块的正常控制流来处理错误或者其它异常条件的方式。
    
**优点:**
    正常操作代码的控制流不会和错误处理代码混在一起. 当某种条件发生时, 它也允许控制流跳过多个框架. 例如, 一步跳出N个嵌套的函数, 而不必继续执行错误的代码。
    
**缺点:**
    可能会导致让人困惑的控制流. 调用库时容易错过错误情况。 
    
**结论:**
    异常必须遵守特定条件:
    
- 像这样触发异常: `raise MyException("Error message")` 或者 ``raise MyException`` . 不要使用两个参数的形式( ``raise MyException, "Error message"`` )或者过时的字符串异常( ``raise "Error message"`` )。
- 模块或包应该定义自己的特定域的异常基类, 这个基类应该从内建的Exception类继承. 模块的异常基类应该叫做"Error"。
```
class Error(Exception):
    pass   
```

- 永远不要使用 ``except:`` 语句来捕获所有异常, 也不要捕获 ``Exception`` 或者 ``StandardError`` , 除非你打算重新触发该异常, 或者你已经在当前线程的最外层(记得还是要打印一条错误消息). 在异常这方面, Python非常宽容, ``except:`` 真的会捕获包括Python语法错误在内的任何错误. 使用 ``except:`` 很容易隐藏真正的bug。
- 尽量减少try/except块中的代码量. try块的体积越大, 期望之外的异常就越容易被触发. 这种情况下, try/except块将隐藏真正的错误。
- 使用finally子句来执行那些无论try块中有没有异常都应该被执行的代码. 这对于清理资源常常很有用, 例如关闭文件。
- 当捕获异常时, 使用 ``as`` 而不要用逗号. 例如
        
```
try:
    raise Error
except Error as error:
    pass
```


设计实验方式
---
___
采取比较简单直观的对照实验。

先定义一个装饰器，用来计算每个函数执行所需时间：
```
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
```
然后用该装饰器装饰测试的函数即可。

再定义一个叫do_something的函数，这个函数中就做一件事，把1赋值给变量a。在每个测试函数中，都会调用这个函数1000000次。
do_something:
```
def do_something():
    a = 1
```

我根据情况设计了不同的测试组：
测试组1（直接执行耗时操作）:
```
@timer
def test1():
    for _ in xrange(1000000):
        do_something()
```

测试组2（耗时操作放在try中执行，不抛出错误）:
```
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
```

测试组3（try放耗时操作中，try每一次操作，不抛出错误）:
```
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
```

测试组4（try放耗时操作中，try每一次操作并进行异常处理(捕捉抛出的特定异常)）:
```
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
```

测试组5（try放耗时操作中，try每一次操作并进行异常处理(捕捉所有异常 try...except BaseException)）:
```
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
```

测试组6（try放耗时操作中，try每一次操作并进行异常处理(捕捉所有异常 不带任何异常类型)）:
```
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
```

测试组7（耗时操作放在except中）:
```
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
```

测试组8（防御式编码）:
```
@timer
def test8():
    zero = 0
    for _ in xrange(1000000):
        if zero == 0:
            do_something()
```

执行结果
---
![这里写图片描述](http://img.blog.csdn.net/20151101001938685)
___


对比结论
---
___

 - 通过对比1和2，可以得知直接执行耗时操作和耗时操作放在try中执行并无异常触发时性能消耗几乎是一样的。
 - 通过对比2和7，可以得知使用异常的使用无论是把代码放在 try 中执行还是在 except 中执行性能消耗几乎是一样的。
 - 通过对比2和3，可以得知当不抛出错误时，把try放耗时操作中比耗时操作放在try中性能消耗要略大。
 - 通过对比3和4，可以得知当使用try时无异常抛出跟使用try时抛出异常性能消耗几乎相差好几倍。
 - 通过对比4和5，可以得知try放耗时操作中时，try每一次操作并进行异常处理(捕捉抛出的特定异常)跟try每一次操作并进行异常处理(捕捉所有异常 try...except BaseException)性能消耗几乎是一样的。
 -  通过对比4和8，可以得知使用防御性方式编码比捕捉异常方式性能消耗几乎相差好几倍。
 - 通过对比5和6，可以得知捕捉所有异常（try...except）方式比捕捉所有异常(try...except BaseException)方式要略快。

总结
---
___
由以上对比结论，可以总结为：

 1. 无论是把代码放在 try 中执行还是在 except 中执行性能消耗几乎是一样的。
 
 2. 直接执行代码与放在try中执行且不抛出异常时性能消耗几乎是一样的，当然理论上try会消耗一点性能，可以忽略不计。

 3. 虽然try...except的方式比try...except BaseException和捕捉抛出的特定异常的方式要略快，但扔不建议采取这种方式，因为前者很容易隐藏真正的bug，从而带来严重后果。

 4. 通常要采取捕捉抛出的特定异常而不是捕捉所有异常，虽然二者性能消耗几乎一样。

 5. 防御性方式编码比捕捉异常方式性能消耗几乎相差好几倍，应尽量采取这种编程方式，提升性能并且更靠谱。
