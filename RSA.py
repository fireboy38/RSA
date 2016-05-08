# -*- coding: cp936 -*-
# 2016.1.8
import os
import math
import random
from time import clock as now
"""从 time module中引入 clock 方法,并将其伪命名成now"""

import Euclid
import fast_powmod
import prime_test
import encode

DEBUG = True#控制调试，可显示关键数据

begin = now()#当程序第一次运行时，开始计时，
IV = 0#CBC模式中的初始向量

def produce_primes(decimal_bits):
    """产生指定位数的随机数"""
    start = 10 ** (decimal_bits-1) + 1
    stop = 10 ** (decimal_bits+1) - 1
    
    while True:
        random.seed()#改变随机数种子
        odd = random.randrange(start,stop,2)#步长为2,产生一个随机奇数
        
        if prime_test.fast_prime_test(odd) == False:#先快速判断一下是否为素数
            continue
        is_prime = prime_test.miller_rabin(odd)#miller_rabin算法素性测试
        if is_prime == True:
            return odd
        elif is_prime == False:
            continue


binary_bits = 32#指定随机数的位数，大约为十进制的6位，由下式计算得出
decimal_bits = int(math.ceil(binary_bits * math.log10(2)))#math.ceil一定会进位,从而只剩一位小数
if DEBUG:
    print 'n的十进制位数为:%d\n' %(decimal_bits)
decimal_bits >>=1#相当于除以2，为p和q的位数

siv = 10 ** (decimal_bits*2-1) + 1
tiv = 10 ** (decimal_bits*2+1) - 1
IV = random.randrange(siv,tiv)
"""生成IV，最重要的是该IV与要解密的文件中的IV是否一样,对d和n也一样"""
if DEBUG:
        print 'IV为:%d\n' %IV


def produce_p_q():
    """产生两个不同的大素数p和q"""
    p = produce_primes(decimal_bits)
    while True:
        q = produce_primes(decimal_bits)
        if q != p:
            return(p,q)

(p,q) = produce_p_q()
n = p*q


def bits_of_n(n):
    """计算最后产生的n的二进制位数"""
    bits = 0
    while n >= 1:
        n >>= 1
        bits += 1
    return bits

bits = bits_of_n(n)
if DEBUG:
    print '\nThe binary bits of n is:',bits
m = (p-1)*(q-1)


def produce_e_d():
    """产生(e,d)"""
    e = 3
    while True:
        d = Euclid.extended_Euclid(e,m)#e*d=1modm
        if Euclid.gcd(m,e) == 1 and d > 0:
            break
        else:
            e += 2
    return (e,d)

(e,d) = produce_e_d()

if DEBUG:
    print '\nq is:',q
    print '\np is:',p
    print '\nm is:',m
    print '\ne is:',e
    print '\nd is:',d
    print '\nThe private Key (d,n) is:',(d,n)
    print '\nThe public Key (e,n) is:',(e,n)



def encrypt(groups):
    "对数字化后的消息分组进行加密"
    encrypted = []
    tmp = IV#CBC模式加密
    for message in groups:
        t = fast_powmod.fast_powmod((tmp ^ message),e,n)
        encrypted.append(t)
        tmp = t
    return encrypted

def decrypt(cipher):
    "对加密后的密文分组进行解密"
    plain_text = []
    tmp = IV#CBC模式解密
    for decrypted in cipher:
        t = fast_powmod.fast_powmod(decrypted,d,n)
        p = t ^ tmp
        plain_text.append(p)
        tmp = decrypted
    return plain_text

def refresh():
    os.system('cls')#Linux下为clear

def pause():
    os.system('pause')
"""Linux下为:function pause(){read -p "$*"} pause'Press any key to continue...'"""

count = 'y'
while count=='y' and len(count)==1:
    #refresh() #清屏，演示不需要
    print '\n\n*********************RSA算法的加密与解密*********************'
    print ' 请选择要加密的内容：'
    print ' 1.信息加密'
    print ' 2.文件加密'
    print ' 3.文件解密'
    print ' 4.退出程序'
    flag = raw_input(' 请按照上述提示输入数字序号执行相应的操作，错误输入会刷新!：')
    if flag=='1' and len(flag)==1:
        message = raw_input('***请输入要加密的内容：')
        
    elif flag=='2' and len(flag)==1:#加密的情况
        try :
            path = raw_input('***请输入要加密文件的完整路径，\n若文件与加密程序在同一文件夹下，可直接输入文件名：')
            print '加密中……'
            fp = open(path,'rb')
            message = fp.read()
            fp.close()
        except IOError:#异常处理，防止输入的文件不存在
            print '\n\n!!!该文件不存在，请按任意键回到主菜单!!!'
            pause()
            continue
            
    elif flag=='3' and len(flag)==1:#解密的情况
        try:
            path = raw_input('\n***请输入要解密文件的完整路径，\n若文件与该程序在同一文件夹下，可直接输入文件名：')
            print '读取中……'
            fp = open(path,'rb')
            ctmp = []
            cipher = []
            cstr = (fp.read())[1:-1]#去掉字符串首尾的中括号
            for c in cstr:
                if c != ',' and c!='L':#除了数字还有字符','和'L'
                    ctmp.append(c)#将一个完整的数字式字符串，提取出来
                elif len(ctmp)!=0:
                    cipher.append(long(''.join(ctmp)))
                    ctmp = []
            fp.close()
        except:#会有ValueError或IOError
            print '!!!该文件不存在，则该密文并非由此程序加密，请按任意键回到主菜单!!!'
            pause()
            continue
        try:#存放d的文件一定要和密文放在一起，否则解密失败
            fp = open((path+'_d'),'rb')
            d = long(fp.read())
        except:
            print '!!!存放私钥d的文件%s不存在，则该文件并非由此程序产生，请按任意键回到主菜单!!!' %(path+'_d')
            pause()
            continue
        if cipher[-1]!=IV or cipher[-2]!=n:#很重要
            IV = cipher[-1]
            n = cipher[-2]
            
    elif flag=='4' and len(flag)==1:
        break
    else:
        refresh()
        continue
    
    if flag=='1' or flag=='2':
        try:
            groups = encode.str2num(decimal_bits*2,message)#将消息转化为数字的分组
        except UnicodeEncodeError:
            print '!!!编码错误，要加密的内容并不全包含在ASCII码中，请按任意键回到主菜单!!!'
            pause()
            continue
        print '***共分为%d组进行加密***\n' %len(groups)
        cipher = []
        cipher = encrypt(groups)#cipher为数字化加密分组
        cipher.append(long(e))
        """把e,n和IV作为密文的一部分，成为密文的最后三个分组"""
        cipher.append(n)
        cipher.append(IV)

        filename = raw_input('***请输入密文将要放置的文件，若不存在将会创建它：')
        fp = open(filename,'wb')
        fp.write(str(cipher))#化为字符串，写入到文件中
        fp.close()
        fp = open((filename+'_d'),'wb')#单独存放d的数值
        fp.write(str(d))
        fp.close()
        print '***密文已被写到文件%s中,私钥d存放在文件%s中，请保证两个文件在同一目录下，否则密文无法解密！***' %(filename,(filename+'_d'))
        
    fg = raw_input('***若要显示该密文，请输入y，其他输入则跳过这一步:')
    if fg == 'y':
        print '***The cipher is:\n',cipher
    fg = raw_input('\n***若要从该密文还原出明文，请输入y,其他输入则跳过这一步:')    
    if fg == 'y':
        print '解密中……\n'
        plain_text = decrypt(cipher[:-3])#RSA加解密核心，明文密文都是数字,密文最后三组为e,n,IV
        plain_text = encode.num2str(plain_text)
    
        filename = raw_input('\n***请输入明文将要放置的文件，若不存在将会创建它：')
        fp = open(filename,'wb')
        fp.write(plain_text)#写入到文件中
        fp.close()
        print '***明文已被写到文件%s中***' %filename
    
        fg = raw_input('***若要显示该明文，请输入y，其他输入则跳过这一步:')
        if fg == 'y':
            print '\n\n***The plain_text is:\n',plain_text

    end = now()
    print '\n***总共用时%d秒***' %(end-begin)
    begin = now()
    count = raw_input('若要继续请按y，按其他键则退出:')
