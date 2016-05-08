# -*- coding: cp936 -*-
#2016.1.8
def gcd(a,b):
    """��2���������Լ��"""
    if(a < b):
        (a,b) = (b,a)
    if b == 0:  #��������
        return a
    else:
        return gcd(b,a%b)#�ݹ����


def extended_Euclid(e,z):
    """������չ��ŷ������㷨������Կeģz�ĳ˷���Ԫd"""
    (x1,x2,x3) = (1,0,z)
    (y1,y2,y3) = (0,1,e)
    while True:
        if y3 == 0:
            return False
        if y3 == 1:
            return y2
        div = x3/y3
        (t1,t2,t3) = (x1-div*y1,x2-div*y2,x3-div*y3)
        (x1,x2,x3) = (y1,y2,y3)
        (y1,y2,y3) = (t1,t2,t3)

if __name__ == '__main__':
    print gcd(100,125)
    print extended_Euclid(7,48)
        
