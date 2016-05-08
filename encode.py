# -*- coding: cp936 -*-
#2016.1.8
import base64

def str2num(nbits,message):
    """返回明文的数字化分组"""

    if nbits % 2 == 0:#保证每组包含偶数位数
        nbits -= 2
    else:
        nbits -= 1

    message_b64 = base64.b64encode(message) #变为base64所用字符集
    message_num = []
    for char in message_b64:
        message_num.append(str(ord(char)-30))#保证base64的字符集化为两位数，再化为字符串
    message_str = ''.join(message_num)

    result = []
    while True:
        if len(message_str) > nbits:#不可以等于，否则else的return不执行
            result.append(long(message_str[:nbits]))#分组
            message_str = message_str[nbits:]
        else:
            result.append(long(message_str))
            return result#各分组的数字

def num2str(groups):#各分组的数字被传递过来
    """将数字转换成字符串，然后进行base64解码"""
    result = []
    for string in groups:
        string = str(string)#数字化为字符串 
        message = []
        for i in range(0,len(string),2):#即便最后一组数位数不到nbits，也没关系
            base = string[i:i+2] #每次取2位
            message.append(chr(int(base)+30))#化为字符追加到message列表中
        result.append(''.join(message))#先无缝拼接message，再追加到result列表中
    result = base64.b64decode(''.join(result))#先无缝拼接result，再解码

    return result
        
