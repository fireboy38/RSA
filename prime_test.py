# -*- coding: cp936 -*-
#2016.1.8
import fast_powmod
DEBUG = False   #�ж��Ƿ�Ҫ����

def get_d_r(prime_n_1):
    """prime_n_1 = prime-1,�� prime-1 = odd_m * 2^r,���أ�(odd_m,r)"""
    r = 0
    bits = prime_n_1
    while not (bits & 1):#�������Ƶ�λ�ж��ٸ�0������r��odd_m
        r += 1
        bits >>= 1
    odd_m = prime_n_1 / (2**r)    
    if DEBUG:
        print 'r=%d,odd_m=%d' %(r,odd_m)
    return (odd_m,r)
        

def fast_prime_test(prime):
    """���������İ취����3��5000�������ж�һ��prime�Ƿ�Ϊ����"""
    for test in range(3,5000,2):
        if prime % test == 0:
            return False    #һ����������
        else:
            return True     #����������
        

def miller_rabin(prime):
    """��miller_rabin�㷨�������Բ��ԣ�����False��ʾһ���Ƿ�������
        ����True���ʾ����Ϊ����"""
    witness = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47)
    """������15������,��primeΪ����������Ϊ����ҲѡΪ������
        ���߱�Ȼ����,������FermatС���������"""
    prime_n_1 = prime - 1
    (odd_m,r) = get_d_r(prime_n_1)#�ֽ�b^(n-1)mod(n)�е�n-1��СFermat��������ģΪ1

    for rand_witness in witness:
        y = fast_powmod.fast_powmod(rand_witness,odd_m,prime)
        if DEBUG:   
            print 'y=%d' %y
        """ƽ��������,ģprime�������,prime-1�൱��-1,���˴�����1����ͨ��"""
        if r == 0:
            if y == 1:  #СFermat
                continue
            else:
                return False
        else:
            if y==1 or y==prime_n_1:
                continue
            else:
                for j in range(1,r+1):
                    y = fast_powmod.fast_powmod(y,2,prime)
                    if y == prime_n_1:
                        break
                    else:
                        return False
             
    return True     #���r=0,�����һ����True
    """ֻ��-1�ܹ���-1ƽ����Ϊ1,����1ȫ���֣���1֮��ȫΪ1�������ٳ���-1������û��ȫ��������1,������"""
    """��Χ��1��r,СFermat��������ģΪ1��Ȼ��ƽ�������鲻�ܳ�������ֵ��ǰ���if����һ����Ϊ����1����"""


if __name__ == '__main__':
    prime = 2**4253-1
    print '%d �Ǹ�����ô\t%s' %(prime,miller_rabin(prime))
    
    print miller_rabin(105)#False

    print miller_rabin(2047)#False

    print miller_rabin(1373653)#False

             
                        
                
    
