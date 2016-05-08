# -*- coding: cp936 -*-
#2016.1.8
def fast_powmod(a,p,n):
    """����ģ�ظ�ƽ�����㷨������ result = a^p mod n"""
    result = a % n
    remainders = []
    while p != 1:
        remainders.append(p & 1)    #ȡ��ָ��p��Ϊ�����ƺ�����λ
        p = p >> 1
        
    while remainders:           #ֻҪremainders���վͱ���ѭ��
        rem = remainders.pop()
        result = ((a**rem) * (result**2)) % n
    return result
