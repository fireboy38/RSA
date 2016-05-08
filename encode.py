# -*- coding: cp936 -*-
#2016.1.8
import base64

def str2num(nbits,message):
    """�������ĵ����ֻ�����"""

    if nbits % 2 == 0:#��֤ÿ�����ż��λ��
        nbits -= 2
    else:
        nbits -= 1

    message_b64 = base64.b64encode(message) #��Ϊbase64�����ַ���
    message_num = []
    for char in message_b64:
        message_num.append(str(ord(char)-30))#��֤base64���ַ�����Ϊ��λ�����ٻ�Ϊ�ַ���
    message_str = ''.join(message_num)

    result = []
    while True:
        if len(message_str) > nbits:#�����Ե��ڣ�����else��return��ִ��
            result.append(long(message_str[:nbits]))#����
            message_str = message_str[nbits:]
        else:
            result.append(long(message_str))
            return result#�����������

def num2str(groups):#����������ֱ����ݹ���
    """������ת�����ַ�����Ȼ�����base64����"""
    result = []
    for string in groups:
        string = str(string)#���ֻ�Ϊ�ַ��� 
        message = []
        for i in range(0,len(string),2):#�������һ����λ������nbits��Ҳû��ϵ
            base = string[i:i+2] #ÿ��ȡ2λ
            message.append(chr(int(base)+30))#��Ϊ�ַ�׷�ӵ�message�б���
        result.append(''.join(message))#���޷�ƴ��message����׷�ӵ�result�б���
    result = base64.b64decode(''.join(result))#���޷�ƴ��result���ٽ���

    return result
        
