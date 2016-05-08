# -*- coding: cp936 -*-
# 2016.1.8
import os
import math
import random
from time import clock as now
"""�� time module������ clock ����,������α������now"""

import Euclid
import fast_powmod
import prime_test
import encode

DEBUG = True#���Ƶ��ԣ�����ʾ�ؼ�����

begin = now()#�������һ������ʱ����ʼ��ʱ��
IV = 0#CBCģʽ�еĳ�ʼ����

def produce_primes(decimal_bits):
    """����ָ��λ���������"""
    start = 10 ** (decimal_bits-1) + 1
    stop = 10 ** (decimal_bits+1) - 1
    
    while True:
        random.seed()#�ı����������
        odd = random.randrange(start,stop,2)#����Ϊ2,����һ���������
        
        if prime_test.fast_prime_test(odd) == False:#�ȿ����ж�һ���Ƿ�Ϊ����
            continue
        is_prime = prime_test.miller_rabin(odd)#miller_rabin�㷨���Բ���
        if is_prime == True:
            return odd
        elif is_prime == False:
            continue


binary_bits = 32#ָ���������λ������ԼΪʮ���Ƶ�6λ������ʽ����ó�
decimal_bits = int(math.ceil(binary_bits * math.log10(2)))#math.ceilһ�����λ,�Ӷ�ֻʣһλС��
if DEBUG:
    print 'n��ʮ����λ��Ϊ:%d\n' %(decimal_bits)
decimal_bits >>=1#�൱�ڳ���2��Ϊp��q��λ��

siv = 10 ** (decimal_bits*2-1) + 1
tiv = 10 ** (decimal_bits*2+1) - 1
IV = random.randrange(siv,tiv)
"""����IV������Ҫ���Ǹ�IV��Ҫ���ܵ��ļ��е�IV�Ƿ�һ��,��d��nҲһ��"""
if DEBUG:
        print 'IVΪ:%d\n' %IV


def produce_p_q():
    """����������ͬ�Ĵ�����p��q"""
    p = produce_primes(decimal_bits)
    while True:
        q = produce_primes(decimal_bits)
        if q != p:
            return(p,q)

(p,q) = produce_p_q()
n = p*q


def bits_of_n(n):
    """������������n�Ķ�����λ��"""
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
    """����(e,d)"""
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
    "�����ֻ������Ϣ������м���"
    encrypted = []
    tmp = IV#CBCģʽ����
    for message in groups:
        t = fast_powmod.fast_powmod((tmp ^ message),e,n)
        encrypted.append(t)
        tmp = t
    return encrypted

def decrypt(cipher):
    "�Լ��ܺ�����ķ�����н���"
    plain_text = []
    tmp = IV#CBCģʽ����
    for decrypted in cipher:
        t = fast_powmod.fast_powmod(decrypted,d,n)
        p = t ^ tmp
        plain_text.append(p)
        tmp = decrypted
    return plain_text

def refresh():
    os.system('cls')#Linux��Ϊclear

def pause():
    os.system('pause')
"""Linux��Ϊ:function pause(){read -p "$*"} pause'Press any key to continue...'"""

count = 'y'
while count=='y' and len(count)==1:
    #refresh() #��������ʾ����Ҫ
    print '\n\n*********************RSA�㷨�ļ��������*********************'
    print ' ��ѡ��Ҫ���ܵ����ݣ�'
    print ' 1.��Ϣ����'
    print ' 2.�ļ�����'
    print ' 3.�ļ�����'
    print ' 4.�˳�����'
    flag = raw_input(' �밴��������ʾ�����������ִ����Ӧ�Ĳ��������������ˢ��!��')
    if flag=='1' and len(flag)==1:
        message = raw_input('***������Ҫ���ܵ����ݣ�')
        
    elif flag=='2' and len(flag)==1:#���ܵ����
        try :
            path = raw_input('***������Ҫ�����ļ�������·����\n���ļ�����ܳ�����ͬһ�ļ����£���ֱ�������ļ�����')
            print '�����С���'
            fp = open(path,'rb')
            message = fp.read()
            fp.close()
        except IOError:#�쳣������ֹ������ļ�������
            print '\n\n!!!���ļ������ڣ��밴������ص����˵�!!!'
            pause()
            continue
            
    elif flag=='3' and len(flag)==1:#���ܵ����
        try:
            path = raw_input('\n***������Ҫ�����ļ�������·����\n���ļ���ó�����ͬһ�ļ����£���ֱ�������ļ�����')
            print '��ȡ�С���'
            fp = open(path,'rb')
            ctmp = []
            cipher = []
            cstr = (fp.read())[1:-1]#ȥ���ַ�����β��������
            for c in cstr:
                if c != ',' and c!='L':#�������ֻ����ַ�','��'L'
                    ctmp.append(c)#��һ������������ʽ�ַ�������ȡ����
                elif len(ctmp)!=0:
                    cipher.append(long(''.join(ctmp)))
                    ctmp = []
            fp.close()
        except:#����ValueError��IOError
            print '!!!���ļ������ڣ�������Ĳ����ɴ˳�����ܣ��밴������ص����˵�!!!'
            pause()
            continue
        try:#���d���ļ�һ��Ҫ�����ķ���һ�𣬷������ʧ��
            fp = open((path+'_d'),'rb')
            d = long(fp.read())
        except:
            print '!!!���˽Կd���ļ�%s�����ڣ�����ļ������ɴ˳���������밴������ص����˵�!!!' %(path+'_d')
            pause()
            continue
        if cipher[-1]!=IV or cipher[-2]!=n:#����Ҫ
            IV = cipher[-1]
            n = cipher[-2]
            
    elif flag=='4' and len(flag)==1:
        break
    else:
        refresh()
        continue
    
    if flag=='1' or flag=='2':
        try:
            groups = encode.str2num(decimal_bits*2,message)#����Ϣת��Ϊ���ֵķ���
        except UnicodeEncodeError:
            print '!!!�������Ҫ���ܵ����ݲ���ȫ������ASCII���У��밴������ص����˵�!!!'
            pause()
            continue
        print '***����Ϊ%d����м���***\n' %len(groups)
        cipher = []
        cipher = encrypt(groups)#cipherΪ���ֻ����ܷ���
        cipher.append(long(e))
        """��e,n��IV��Ϊ���ĵ�һ���֣���Ϊ���ĵ������������"""
        cipher.append(n)
        cipher.append(IV)

        filename = raw_input('***���������Ľ�Ҫ���õ��ļ����������ڽ��ᴴ������')
        fp = open(filename,'wb')
        fp.write(str(cipher))#��Ϊ�ַ�����д�뵽�ļ���
        fp.close()
        fp = open((filename+'_d'),'wb')#�������d����ֵ
        fp.write(str(d))
        fp.close()
        print '***�����ѱ�д���ļ�%s��,˽Կd������ļ�%s�У��뱣֤�����ļ���ͬһĿ¼�£����������޷����ܣ�***' %(filename,(filename+'_d'))
        
    fg = raw_input('***��Ҫ��ʾ�����ģ�������y������������������һ��:')
    if fg == 'y':
        print '***The cipher is:\n',cipher
    fg = raw_input('\n***��Ҫ�Ӹ����Ļ�ԭ�����ģ�������y,����������������һ��:')    
    if fg == 'y':
        print '�����С���\n'
        plain_text = decrypt(cipher[:-3])#RSA�ӽ��ܺ��ģ��������Ķ�������,�����������Ϊe,n,IV
        plain_text = encode.num2str(plain_text)
    
        filename = raw_input('\n***���������Ľ�Ҫ���õ��ļ����������ڽ��ᴴ������')
        fp = open(filename,'wb')
        fp.write(plain_text)#д�뵽�ļ���
        fp.close()
        print '***�����ѱ�д���ļ�%s��***' %filename
    
        fg = raw_input('***��Ҫ��ʾ�����ģ�������y������������������һ��:')
        if fg == 'y':
            print '\n\n***The plain_text is:\n',plain_text

    end = now()
    print '\n***�ܹ���ʱ%d��***' %(end-begin)
    begin = now()
    count = raw_input('��Ҫ�����밴y�������������˳�:')
