#!/usr/bin/env python
def fun(name, *args, **kwargs):
    print len(name), len(args), len(kwargs)
    try:
        print dic["Django111"]
    except KeyError, e:
        print "The key is not exist."
fun("sb",123,sb='sssss')

def fun_var_args(farg, *args):  
    print "arg:", farg  
    for value in args:  
        print "another arg:", value  
fun_var_args(1, "two", 3, "sadasd")


def checkio(words):
    b = a.split(' ')
    for i in range(len(b)):
        if b[i].isalpha() and b[i+1].isalpha() and b[i+2].isalpha():
            return True
    return False
def checkio(text):
    l = []
    for i in text:
        if i == '(' or i == '[' or i == '{':
            l.append(i)
        if (len(l) != 0) and (i == ')' and l[-1] == '(' or i == ']' and l[-1] == '[' or i == '}' and l[-1] == '{'):
            l.pop()
        elif i == ')' or i == ']' or i == '}':
            return False
    if len(l) == 0:
        return True
    return False
checkio("(((1+(1+1))))]")

m = lambda x,y: x-y
print m(3,1)
f = lambda x,y:x if y==0 else f(y, x%y)
def f(x,y):
    if y == 0:
        return x
    return f(y,x%y)
f=lambda x,y:x if ~y else f(y,x%y)
def checkio(n):
    i = 2
    j = n/2
    l = []
    while i<=j:
        if  n % i == 0:
            l.append(i)
            n /= i
        else:
            i+=1
    if n != 1:
        l.append(1)
    for i in range(len(l)-1):
        j = i+1
        while j<len(l) and l[i]*l[j]<10:
            l[i] = l[i]*l[j]
            l.remove(l[j])
    s = 0
    while len(l) > 0:
        if l[0] > 10:
            s = 0
            break
        s = s*10+l[0]
        l.remove(l[0])
    return s
s = 0
def checkio(n):
    global s
    if len(n) == 1:
        return s + n[0]
    else:
        s = s + n[0]
        n.remove(n[0])
        return checkio(n)
checkio = lambda x:"Fizz Buzz" if x%15 == 0 else "Fizz" if x%3 == 0 else "Buzz" if x%5 == 0 else str(x)
def checkio(l):
    for i in l:
        if i[0] == i[1] and i[0] == i[2] and i[0] != '.':
            return i[0]
    for i in range(3):
        if l[0][i] == l[1][i] and l[0][i] == l[2][i] and l[0][i] != '.':
            return l[0][i]
    if l[0][0] == l[1][1] and l[0][0] == l[2][2] and l[0][0] != '.':
            return l[0][0]
    if l[0][2] == l[1][1] and l[0][2] == l[2][0] and l[0][2] != '.':
            return l[0][2]
    return "D"

checkio=lambda m,n:bin(m^n).count('1')

Speech Module
def checkio(number):
    s = ""
    if number/100 > 0:
        s+=FIRST_TEN[number/100-1]
        s+=" "
        s+=HUNDRED
        number = number%100
        if number > 0:
            s+=" "
    if number >0:
        if number < 20:
            if number < 10:
                s+=FIRST_TEN[number-1]
                return s
            s+=SECOND_TEN[number%10]
        else:
            s+=OTHER_TENS[number/10-2]
            if number%10:
                s+=" "
                s+=FIRST_TEN[number%10-1]
    return s

Feed Pigeons
def checkio(number):
    p = 1
    i = 2
    while number > 0:
        if number - p > 0:
            number = number - p
            p += i
            i += 1
        elif number - p + i - 1 > 0:
            return number
        else:
            return p-i+1

Roman numerals
def checkio(number):
    l = ""
    if number>=1000:
        l+='M'*(number/1000)
        number = number%1000
    if number<1000 and number>=900:
        l+='CM'
        number -=900
    if number<1000 and number>=500:
        l+='D'
        l+='C'*(number/100-5)
        number = number%100
    if number<1000 and number>=400:
        l+="CD"
        number = number%100
    if number<1000 and number>=100:
        l+="C"*(number/100)
        number = number%100
    if number<100 and number>=90:
        l+='XC'
        number -=90
    if number<100 and number>=50:
        l+='L'
        l+='X'*(number/10-5)
        number = number%10
    if number<100 and number>=40:
        l+="XL"
        number = number%10
    if number<100 and number>=10:
        l+="X"*(number/10)
        number = number%10
    if number<10 and number>=9:
        l+='IX'
    if number<9 and number>=5:
        l+='V'
        l+='I'*(number-5)
    if number==4:
        l+="IV"
    if number<4 and number>=1:
        l+="I"*number
    return l

checkio=lambda data: ['','M','MM','MMM'][data//1000]+['','C','CC','CCC','CD','D','DC','DCC','DCCC','CM'][data//100%10]+['','X','XX','XXX','XL','L','LX','LXX','LXXX','XC'][data//10%10]+['','I','II','III','IV','V','VI','VII','VIII','IX'][data%10]

Golden Pyramid
def count_gold(pyramid):
    length = len(pyramid)
    if len(pyramid) == 1:
        return pyramid[0];
    l2=list(pyramid[-1])
    i=2
    while len(l2) != 1 and pyramid[-i+1] != pyramid[0]:
        l1=list(pyramid[-i])
        l3=[]
        for j in range(len(l1)):
            l3.append((l1[j]+max(l2[j],l2[j+1])))
        i+=1
        l2=l3
    return l2[0]

def max(*args, **kwargs):
    print args
    print kwargs
    return 0

The Most Numbers
def checkio(*args):
    if args:
        return sorted(args)[-1]-sorted(args)[0]
    else:
        return 0

checkio=lambda *args:sorted(args)[-1]-sorted(args)[0] if args else 0

Digits Multiplication
slove=lambda number:int(number[0]) if len(number) == 1 and  number[0]!='0' else 1 if len(number) == 1 and  number[0]=='0'  else int(slove(number[1:])) if number[0]=='0'  else int(number[0])*int(slove(number[1:]))
def checkio(number):
    n=str(number)
    return slove(n)

Striped Words
VOWELS = "AEIOUY"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"
def checkio(s):
    s=s.replace(","," ")
    s=s.replace("."," ")
    l=s.split(' ')
    count = 0
    for i in l:
        if len(i) <2:
            continue
        else:
            flag = 0
            for j in range(len(i)-1):
                if (i[j].upper() in VOWELS and i[j+1].upper() in VOWELS) or (i[j].upper() in CONSONANTS and i[j+1].upper() in CONSONANTS) or not i[j].isalpha():
                    flag=0
                    break
                else:
                    flag=1
            count+=flag
    return count


Three Points Circle
import math
def checkio(s):
    s=s.replace("("," ")
    s=s.replace(","," ")
    s=s.replace(")"," ")
    l=s.split(' ')
    n=[]
    for i in l:
        if len(i) != 0:
            n.append(int(i))
    a=2*(n[2]-n[0])
    b=2*(n[3]-n[1])
    c=n[2]*n[2]+n[3]*n[3]-n[0]*n[0]-n[1]*n[1]
    d=2*(n[4]-n[2])
    e=2*(n[5]-n[3])
    f=n[4]*n[4]+n[5]*n[5]-n[2]*n[2]-n[3]*n[3]
    x=(b*f-e*c)/float((b*d-e*a))
    y=(d*c-a*f)/float((b*d-e*a))
    r=math.sqrt((x-n[0])*(x-n[0])+(y-n[1])*(y-n[1]))
    x=round(x,2)
    if x==int(x):
        x=int(x)
    y=round(y,2)
    if y==int(y):
        y=int(y)
    r=round(r,2)
    if r==int(r):
        r=int(r)
    return "(x-"+str(x)+")^2+(y-"+str(y)+")^2="+str(r)+"^2"


    Find Sequence

def checkio(matrix):
    if len(matrix)<4:
        return False
    for i in range(len(matrix)-3):
        for j in range(len(matrix)-3):
            if (matrix[i][j] == matrix[i][j+1] and matrix[i][j] == matrix[i][j+2] and matrix[i][j] == matrix[i][j+3]) or (matrix[i][j] == matrix[i+1][j] and matrix[i][j] == matrix[i+2][j] and matrix[i][j] == matrix[i+3][j]) or (matrix[i][j] == matrix[i+1][j+1] and matrix[i][j] == matrix[i+2][j+2] and matrix[i][j] == matrix[i+3][j+3]):
                return True
    for i in range(3,len(matrix)):
        for j in range(len(matrix)-3):
            if (matrix[i][j] == matrix[i][j+1] and matrix[i][j] == matrix[i][j+2] and matrix[i][j] == matrix[i][j+3]) or (matrix[i][j] == matrix[i-1][j-1] and matrix[i][j] == matrix[i-2][j-2] and matrix[i][j] == matrix[i-3][j-3]):
                return True
    for i in range(len(matrix)-3):
        for j in range(3,len(matrix)):
            if (matrix[i][j] == matrix[i+1][j] and matrix[i][j] == matrix[i+2][j] and matrix[i][j] == matrix[i+3][j]) or (matrix[i][j] == matrix[i+1][j-1] and matrix[i][j] == matrix[i+2][j-2] and matrix[i][j] == matrix[i+3][j-3]):
                return True
    return False



What does the cow say?
import re
def cowsay(words):
    l=re.split("\s+",words) 
    cutl=[""]*(len(l)+20)
    j=0
    out = "\n"
    print l
    for i in l:
        if len(cutl[j])+len(i)<40:
            cutl[j]+=i
            cutl[j]+=' '
        elif len(i)>=40:
            if j!=0:
                j+=1
            while len(i)>=40:
                cutl[j]= cutl[j]+i[:39]+' '
                i=i[39:]
                j+=1
            cutl[j]= cutl[j]+i[:39]+' '
        else:
            j+=1
            cutl[j]+=i
            cutl[j]+=' '
    print cutl
    lenl=sorted(cutl,key=lambda x:len(x),reverse=True)
    maxlen=len(lenl[0])
    for i in range(len(cutl)):
        if len(cutl[i])>=2 and len(cutl[i])==maxlen and cutl[i][-2]==' ':
            cutl[i] = cutl[i][0:-1]
    print cutl
    maxlen=len(lenl[0])
    out= out + " "+(maxlen+1)*'_'+"\n"
    if len(lenl[1]) == 0:
        out = out +"< "+cutl[0]+(maxlen-len(cutl[0]))*' '+">"+"\n"
    else:
        for i in range(len(cutl)):
            if len(cutl[i])==0:
                break
            if i == 0:
                out = out +"/ "+cutl[i]+(maxlen-len(cutl[i]))*' '+"\\"+"\n"
            elif len(cutl[i+1]) == 0:
                out = out +"\ "+cutl[i]+(maxlen-len(cutl[i]))*' '+"/"+"\n"
                break
            else:
                out = out +"| "+cutl[i]+(maxlen-len(cutl[i]))*' '+"|"+"\n"
    out= out + " "+(maxlen+1)*'-'+"\n"
    out+= "        \   ^__^\n"
    out+= "         \  (oo)\_______\n"
    out+= "            (__)\       )\/\\\n"
    out+= "                ||----w |\n"
    out+= "                ||     ||\n"
    print out
    return out


Verify anagrams
import re
verify_anagrams=lambda x,y:sorted(list(re.sub(r'\s+', '', x.lower())))==sorted(list(re.sub(r'\s+', '', y.lower())))



Open Labyrinth  
def checkio(maze):
    vis=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    direction=[[0,-1,'W'],[0,1,'E'],[-1,0,'N'],[1,0,'S']]
    Node=[1,1,""]
    q=[]
    q.append(Node)
    while len(q)>0:
        n=q[0]
        del q[0]
        if n[0]==10 and n[1]==10:
            return n[2]
        vis[n[0]][n[1]]=1
        for l in direction:
            x=n[0]+l[0]
            y=n[1]+l[1]
            print x,y,n[2]
            if (x > 0 and y >0 and x <12 and y <12 and vis[x][y]==0 and maze[x][y]==0):
                N=[x,y,n[2]+l[2]]
                vis[x][y]=1
                q.append(N)
    return -1


Transposed Matrix
checkio = lambda matrix:map(list, zip(*matrix))


How to find friends
def check_connection(network, first, second):
    l = []
    for i in network:
        l.append(i.split("-"))
    for i in l:
        if first in i:
            ind = l.index(i)
            break
    a=set(l[ind])
    for j in range(3):
        for i in l:
            if a & set(i):
                a = a|set(i)
    return second in a

Median
checkio = lambda data:sorted(data)[len(data)/2] if len(data)%2 else (sorted(data)[len(data)/2] + sorted(data)[len(data)/2-1]) / 2.0


Min and Max
def max(*args, **kwargs):
    if len(args)==1:
        a = list(args[0])
    else:
        a = list(args)
    if kwargs:
        d={}
        result = map(kwargs['key'],a)
        for i in range(len(result)):
            d[i]=result[i]
        orderl = sorted(d.items(), key=lambda d:d[1])
        size = len(orderl)-1
        while size:
            if orderl[size][1] != orderl[size-1][1]:
                return a[orderl[size][0]]
            size-=1
        return a[orderl[0][0]]
    else:
        result = sorted(a)
        size = len(result)-1
        while size:
            if result[size] != result[size-1]:
                return result[size]
            size-=1
        return a[0]
def min(*args, **kwargs):
    if len(args)==1:
        a = list(args[0])
    else:
        a = list(args)
    if kwargs:
        d={}
        result = map(kwargs['key'],a)
        for i in range(len(result)):
            d[i]=result[i]
        orderl = sorted(d.items(), key=lambda d:d[1])
        size = len(orderl)-1
        return a[orderl[0][0]]
    else:
        result = sorted(a)
        return result[0]

Absolute sorting
checkio = lambda data:sorted(list(data), key=abs)

Number Base
def checkio(n,r):
    try:
        return int(n,r)
    except ValueError:
        return -1

Common Words
def checkio(first, second):
    l=[]
    for i in set(first.split(","))&set(second.split(",")):
        if i in first:
            l.append(i)
    return ','.join(sorted(l)) 


The end of other
def checkio(words_set):
    for i in words_set:
        s=words_set.copy()
        s.remove(i)
        for j in s:
            if (i in j or j in i) and i[-1] == j[-1]:
                return True
    return False

The Flat Dictionary
def flatten(dictionary):
    stack = [((), dictionary)]
    result = {}
    while stack:
        path, current = stack.pop()
        for k, v in current.items():
            if v=={}:
                result["/".join((path + (k,)))] = ""
            elif isinstance(v, dict):
                stack.append((path + (k,), v))
            else:
                result["/".join((path + (k,)))] = v
    return result


def ispalindromic(n):
    return str(n)==str(n)[::-1]
def isprime(n):
    if n==2:
        return True
    if n%2==0 or n<=1:
        return False
    i=3
    while i*i<=n:
        if n%i==0:
            return False
        i+=2
    return True


p=lambda x: x>1 and all(map(lambda s:x%s,range(2,int(x**.5+1))))
def golf(n):
    for i in range(n+1,9999999):
        if str(i)==str(i)[::-1] and p(i):
            return i

golf=lambda n:filter(lambda x:str(x)==str(x)[::-1] and x>n and all(map(lambda s:x%s,range(2,int(x**.5+1)))),range(6**8))[0]

The Most Wanted Letter
from collections import Counter
def checkio(text):
    text = text.lower()
    c = Counter(text).most_common()
    c = filter(lambda x:x[0].isalpha(), c)
    most = c[0][1]
    c = filter(lambda x:x[1] == most, c)
    return sorted(c, key=lambda m: m[0])[0][0]


Robot Sort
def swapsort(number):
    string = ""
    number = list(number)
    for j in range(len(number)-1,-1,-1):
        for i in range(j):
            if number[i]>number[i+1]:
                if len(string) > 0:
                    string += ','
                string = string + str(i) + str(i+1)
                number[i],number[i+1] = number[i+1],number[i]
    return string

Weekend counter
from datetime import date
def checkio(begin,end):
    days = int(str(end - begin).split(" ")[0])
    weekendays = days / 7 * 2
    if begin.isoweekday() == 7:
        weekendays -= 1
    if begin.isoweekday() + (days % 7) == 6:
        weekendays += 1
    elif begin.isoweekday() + (days % 7) > 5:
        weekendays += 2
    return weekendays

The Angles of a Triangle
from math import *
def checkio(a, b, c):
    try:
        if a+b <= c or a+c <= b or b+c <= a:
            raise Exception("hehe")
        cosA = int(round(degrees(acos((b*b+c*c-a*a)/(2.0*b*c)))))
        cosB = int(round(degrees(acos((a*a+c*c-b*b)/(2.0*a*c)))))
        cosC = int(round(degrees(acos((b*b+a*a-c*c)/(2.0*b*a)))))
        return sorted([cosA,cosB,cosC])
    except Exception, e:
        return [0,0,0]


Weak Point
def weak_point(matrix):
    l=[]
    for index,item in enumerate(matrix):
        l.append([index,sum(item)])
    y = sorted(l,key=lambda m: m[1])[0][0]
    l=[]
    for index,item in enumerate(map(list, zip(*matrix))):
        l.append([index,sum(item)])
    x = sorted(l,key=lambda m: m[1])[0][0]
    return [y,x]

def weak_point(matrix):
    row = [sum(i) for i in matrix]
    col = [sum(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix))]
    return row.index(min(row)),col.index(min(col))



Morse Clock
def checkio(time_string):
    time = list("".join(map(lambda x:'0'+x if len(x) == 1 else x,time_string.split(':'))))
    time = map(lambda x:bin(int(x))[2::].replace('1','-').replace('0','.'),time)
    return '{0:.>2} {1:.>4} : {2:.>3} {3:.>4} : {4:.>3} {5:.>4}'.format(time[0],time[1],time[2],time[3],time[4],time[5])


digit_stack
def digit_stack(l):
    sum = 0
    n = []
    for i in range(len(l)):
        if l[i][1] == 'U':
            n.append(int(l[i][5:]))
        elif l[i][1] == 'E':
            if len(n) != 0:
                sum += n[-1]
        else:
            if len(n) != 0:
                sum += n.pop()
    return sum

Letter Queue
def letter_queue(commands):
    l = []
    for i in commands:
        if i[1] == 'U':
            l.append(i[5:])
        else:
            if len(l) != 0:
                del l[0]
    return "".join(l)

Bird Language
import re
def translate(s):
    out = ""
    while True:
        m1 = re.match("^[^(a,e,i,o,u,y,\s)][a,e,i,o,u,y]",s)
        m2 = re.match("^[a,e,i,o,u,y]{3}",s)
        m3 = re.match("^\s",s)
        print s
        if m1:
            out += s[0]
            s = s[2:]
        elif m2:
            out += s[0]
            s = s[3:]
        elif m3:
            out += s[0]
            s = s[1:]
        else:
            return out

The Good Radix
checkio = lambda number, radix = 0: checkio(number,int(sorted(number)[-1],36)+1) if radix == 0 else 0 if radix == 37 else radix if int(number,radix) % (radix-1) == 0  else checkio(number,radix+1)


Skew-symmetric matrix
def checkio(matrix):
    m = map(list, zip(*matrix))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != -m[i][j]:
                return False
    return True

Flatten a list
def flatten(array):
    try:
        for sublist in array:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield array

def flat_list(array):
    return list(flatten(array))

flat_list=lambda l:sum(([e] if type(e)!=list else flat_list(e) for e in l),[])

Call to Home
def total_cost(l):
    d = dict()
    for s in l:
        date = s[:10]
        time = int(s[20:])
        if time % 60:
            time = time / 60 + 1
        else:
            time = time / 60
        if date in d:
            d[date] = d[date] + time
        else:
            d[date] = time
    s = sum(map(lambda x:x if x <= 100 else (x-100) * 2 + 100, d.values()))
    return s

Pattern Recognition
def change(pattern, image, i, j):
    if (len(image) - i) < len(pattern) or (len(image[0]) - j) < len(pattern[0]):
        return
    for m in range(len(pattern)):
        for n in range(len(pattern[0])):
            if pattern[m][n] != image[m+i][n+j]:
                return
    for m in range(len(pattern)):
        for n in range(len(pattern[0])):
            image[m+i][n+j] += 2

def checkio(pattern, image):
    for i in range(len(image)):
        for j in range(len(image[0])):
            change(pattern, image, i, j)
    return image


Moore Neighbourhood
def count_neighbours(grid, row, col):
    s = 0
    for x in xrange(-1,2):
        for y in xrange(-1,2):
            try:
                if row+x>=0 and col+y>=0:
                    s += grid[row+x][col+y]
                print "row+x ",row+x,"col+y ",col+y,"s ",s
            except Exception, e:
                pass
    s-=grid[row][col]
    print s
    return s

def count_neighbours(grid, row, col):
    rows = range(max(row-1,0),min(row+2,len(grid)))
    cols = range(max(col-1,0),min(col+2,len(grid[0])))
    return sum(grid[r][c] for r in rows for c in cols) - grid[row][col]

Index Power
index_power = lambda li, num: li[num]**num if len(li) >= num else -1


Count Inversions
def count_inversion(l):
    l=list(l)
    k=0
    for i in range(len(l)):
        for j in range(i,len(l)):
            if l[i] > l[j]:
                l[i] , l[j] = l[j], l[i]
                k += 1
    return k

def count_inversion(l):
    sum = 0
    for i in range(len(l)-1):
        x = l[i]
        sum += len(filter(lambda i: True if x > i else False, l[i+1:]))
    return sum


Clock Angle
def clock_angle(time):
    time = time.split(":")
    h = int(time[0])%12+float(time[1])/60
    m = float(time[1])/5
    return min(abs(h-m)*30,360-abs(m-h)*30)

#!/usr/bin/env python

Color Map
def color_map(graph):
    graph = [[j for j in i] for i in graph]
    ans = []
    def color(num):
        colorlist = ['1','2','3','4']
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] == num:
                    if i-1 >= 0 and graph[i-1][j] != num and graph[i-1][j] in colorlist:
                        colorlist.remove(graph[i-1][j])
                    if j-1 >= 0 and graph[i][j-1] != num and graph[i][j-1] in colorlist:
                        colorlist.remove(graph[i][j-1])
                    if i+1 < len(graph) and graph[i+1][j] != num and graph[i+1][j] in colorlist:
                        colorlist.remove(graph[i+1][j])
                    if j+1 < len(graph[i]) and graph[i][j+1] != num and graph[i][j+1] in colorlist:
                        colorlist.remove(graph[i][j+1])
                if len(colorlist) == 1:
                    break
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] == num:
                    graph[i][j] = colorlist[0]
        return int(colorlist[0])

    m = 0
    for i in graph:
        m = max(i) if max(i) > m else m

    for i in range(m+1):
        ans.append(color(i))
    print ans
    return ans

Moria doors
import re
def calWord(a, b):
    f = 10 if a[0] == b[0] else 0
    l = 10 if a[-1] == b[-1] else 0
    u = len(a)/float(len(b))*30 if len(a) <= len(b) else len(b)/float(len(a))*30
    w = len(set(b).intersection(set(a)))/float(len(set(b).union(set(a))))*50
    return u+w+f+l

def find_word(message):
    msglist = [i.lower() for i in re.split("\W+",message) if i]
    d = dict()
    for i in range(len(msglist)):
        s = 0
        for j in range(len(msglist)):
            if i == j:
                continue
            s += calWord(msglist[i], msglist[j])
        d[msglist[i]] = s
    word = sorted(d.iteritems(),key = lambda i:i[1],reverse=True)
    print word[0][0]
    return word[0][0]

Radiation search
def checkio(matrix):
    l=[0,0]
    def search(i,j):
        #visited
        if matrix[i][j] == -1:
            return 0
        s = 1
        tem = matrix[i][j]
        #mark
        matrix[i][j] = -1
        #visit its neighbor
        if i-1 >= 0  and matrix[i-1][j] == tem:
            s += search(i-1,j)
        if j-1 >= 0  and matrix[i][j-1] == tem:
            s += search(i,j-1)
        if i+1 < len(matrix) and matrix[i+1][j] == tem:
            s += search(i+1,j)
        if j+1 < len(matrix[i]) and matrix[i][j+1] == tem:
            s += search(i,j+1)
        return s

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            tem = matrix[i][j]
            s = search(i,j)
            if s > l[0]:
                l[0] = s
                l[1] = tem
    return l

Numbers Factory
def checkio(number):
    n = 9
    ans = ""
    while n > 1:
        if number % n == 0:
            number /= n
            ans = str(n) + ans
        else:
            n -= 1
    return int(ans) if number == 1 else 0

Right to Left
def left_join(phrases):
    return ",".join(phrases).replace("right","left")

 Boolean Algebra
OPERATION_NAMES = ("conjunction", "disjunction", "implication", "exclusive", "equivalence")
def boolean(x, y, operation):
    op = OPERATION_NAMES.index(operation)
    if op == 0:
        return x and y
    if op == 1:
        return x or y
    if op == 2:
        return x <= y
    if op == 3:
        return x ^ y
    return x == y

Secret Message
def find_message(text):
    return filter(lambda w:"A"<=w<="Z",text)

Pangram
check_pangram = lambda text : set([chr(i) for i in range(97,123)]) == set(filter(lambda w:"a"<=w<="z",text.lower()))


Building Base
class Building() :
    def __init__(self,south, west, width_WE, width_NS, height=10):
        self.south = south
        self.west = west
        self.width_WE = width_WE
        self.width_NS = width_NS
        self.height = height
        self.north = south+width_NS
        self.east = west+width_WE
        self.__repr__()
    def  corners(self):
        d = {}
        d["north-west"] = [self.north,self.west]
        d["north-east"] = [self.north,self.east]
        d["south-west"] = [self.south,self.west]
        d["south-east"] = [self.south,self.east]
        return d
    def  area(self):
        return self.width_NS*self.width_WE
    def  volume(self):
        return self.area()*self.height
    def  __repr__(self):
        return "Building(%g, %g, %g, %g, %g)" % (self.south, self.west, self.width_WE, self.width_NS, self.height)


Days Between
import datetime
def days_diff(date1, date2):
    return abs((datetime.date(*date2)-datetime.date(*date1)).days)


Friends
class Friends:
    def __init__(self, connections):
        self.connections = list(connections)

    def add(self, connection):
      if connection in self.connections:
        return False 
      else:
        self.connections.append(connection)
        return True

    def remove(self, connection):
        try:
          self.connections.remove(connection)
          return True
        except Exception:
          return False

    def names(self):
        return reduce(lambda x,y:x|y,self.connections)

    def connected(self, name):
        try:
            return reduce(lambda x, y:x|y, filter(lambda x: name in x, self.connections))^{name}
        except Exception:
          return set()

Pawn Brotherhood
def safe_pawns(pawns):
    m = [[0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0]]
    safe = 0
    for i in pawns:
        m[8-int(i[1])][ord(i[0])-97] = 1
    for i in range(0,8):
      for j in range(0,8):
        if m[i][j] == 1 and i != 7 and ((j-1!=-1 and m[i+1][j-1] == 1) or (j+1!=8 and m[i+1][j+1] == 1)):
          print "yes"
          safe += 1
    return safe

Vigenere Cipher
import re

def enc(number):
    return chr(number+65)

def dec(e,k):
    return enc((ord(e)-ord(k))%26)

def getKeyword(k):
    keyword = ""
    for i in range(len(k)):
        m = re.search("^("+keyword+")+",k)
        left = k[m.end():]
        m2 = re.search("^("+left+")+",keyword)
        if m2 and  len(m2.group()) == len(k[m.end():]):
            return keyword
        keyword += k[i]
    return keyword

def decode_vigenere(om,oe,ne):
    k=""
    for i in range(len(oe)):
        k += dec(oe[i],om[i])
    k = getKeyword(k)
    print "keyword:", k
    k=k * 1000
    m=""
    for i in range(len(ne)):
        m += dec(ne[i],k[i])
    return m

Solution for anything
class AlwaysTrue():
    def __init__(self, arg):
        self.arg = arg
    
    def __gt__(self, arg):
        return True

    def __lt__(self, arg):
        return True

    def __eq__(self, arg):
        return True

    def __ge__(self, arg):
        return True

    def __le__(self, arg):
        return True

def checkio(anything):
    return AlwaysTrue(anything)