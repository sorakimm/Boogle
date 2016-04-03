#-*- coding:cp949-*-
import socket
from C_Python_Socket import generalSend, generalRecv
import C_Python_Socket
sType = dict(B_C_REQ_WORD = '509', B_S_ANS_SUBTITLE = '504', B_S_ANS_COUNT = '503', B_S_ANS_DICTIONARY = '504') # 패킷 타입

##############################################################
# SOCKET NETWORKING
HOST = '127.0.0.1'                # The remote host
PORT = 10001        # The same port as used by the server
s = socket.socket()
##############################################################

def connect(ip, port):
    """사용하기 전 주의 사항
    1) import socket
    2) 전역변수 s = socket.socket()를 선언"""
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = ip                # The remote host
    PORT = port              # The same port as used by the server
    s.connect((HOST, PORT))

def closesocket():
    s.close();

def FillSpacePacket(dataLen, index):
    """패킷의 자릿수를 채워야 할때 공백(' ')으로 빈공간을 채워줌
    dataLen : 분석을 원하는 변수의 길이
    index : space로 채울 인덱스 최대값
    ex)
    data = 'abcd'
    data += FillSpacePacket(data.__len__(), 5)
    print(data)
    결과 : 'abcd  '
    빈칸 두개 생성"""
    index += 1
    space = ''
    if dataLen < index:
        for count in range(0, index-dataLen):
            space += ' '
    return space

def isASCII(text): 
   """ASCII문자인지 판별. text에 ASCII가 아닌 문자가 한개라도 있으면 False, 없으면 True"""
   return not bool(re.search('[^\x00-\x7E]', text))

def __Len_Cstyle__(text):
   """text를 C 스타일 길이로 구함"""
   CLen = 0
   for i in text:
      if isASCII(i):
         CLen += 1
      else: CLen += 2
   return CLen
 
sdb = C_Python_Socket

class SearchDB(): 
    #def __init__(self, mode, keyword):
    #    self.recvData = sdb.generalRecv()
    #    self.mode = mode
    #    self.keyword = keyowrd
        

    def reqWord(self, mode, keyword):
        modeTuple = (4, mode)
        wordTuple = (4, keyword)
        sdb.generalSend(C_Python_Socket.B_C_REQ_WORD, modeTuple, wordTuple, delay=0.01)
        
    def recvAll(self):
        recvAllData = sdb.generalRecv()
        r_totallen = ''
        r_type = ''
        
        for i in range(0, 7):
            if(recvAllData[I] != '\0'):
                r_totallen += recvAllData[i]

        for i in range(8, 11):
            if(recvAllData[I] != '\0'):
                r_type += recvAllData[i]

        if(r_type == '504'): # 들어온 패킷이 자막일 때
            subtemp = recvSub()

    def recvSub(self):
        recvsubData = sdb.generalRecv()
        r_type = ''
        r_wordlen = ''
        r_word = ''
        r_urllen = ''
        r_url = ''
        r_titlelen = ''
        r_title = ''
        r_englen = ''
        r_eng = ''
        r_korlen = ''
        r_kor = ''

        for i in range(12, 15):
            if(recvsubData[i] != '\0'):
                r_wordlen += recvsubData[i]
        
        r_wordlen = int(r_wordlen)
        
        for i in range(12, 12 + r_wordlen -1):
            if(recvsubData[i] != '\0'):
                r_word += recvsubData[i]

        offset = 12 + r_wordlen

        for i in range(offset, offset+3):
            if(recvsubData[i] != '\0'):
                r_titlelen += recvsubData[i]
        
        r_titlelen = int(r_titlelen)
        offset += 4
        
        for i in range(offset, offset + r_titlelen - 1):
            if(recvsubData[i] != '\0'):
                r_title += recvsubData[i]

        offset = offset + r_titlelen

        for i in range(offset, offset+3):
            if(recvsubData[i] != '\0'):
                r_englen += recvsubData[i]
        
        r_englen = int(r_englen)
        offset += 4
        
        for i in range(offset, offset + r_englen - 1):
            if(recvsubData[i] != '\0'):
                r_eng += recvsubData[i]

        for i in range(offset, offset+3):
            if(recvsubData[i] != '\0'):
                r_korlen += recvsubData[i]
        
        r_korlen = int(r_korlen)
        offset += 4
        
        for i in range(offset, offset + r_korlen - 1):
            if(recvsubData[i] != '\0'):
                r_kor += recvsubData[i]
                           
        subList = [r_title, r_eng, r_kor]

        return subList

    def recvDict(self):
        recvDicData = sdb.generalRecv()
        r_type = ''
        r_urllen = ''
        r_url = ''
        r_titlelen = ''
        r_title = ''
        r_contentslen = ''
        r_contents = ''

        for i in range(12, 15):
            if(recvDicData[i] != '\0'):
                r_urllen += recvDicData[i]
        
        r_urllen = int(r_urllen)
        
        for i in range(12, 12 + r_urllen -1):
            if(recvDicData[i] != '\0'):
                r_url += recvDicData[i]

        offset = 12 + r_urllen

        for i in range(offset, offset+3):
            if(recvDicData[i] != '\0'):
                r_titlelen += recvDicData[i]
        
        r_titlelen = int(r_titlelen)
        offset += 4
        
        for i in range(offset, offset + r_titlelen - 1):
            if(recvDicData[i] != '\0'):
                r_title += recvDicData[i]

        offset = 12 + r_titlelen

        for i in range(offset, offset+3):
            if(recvDicData[i] != '\0'):
                r_contentslen += recvDicData[i]
        
        r_contentslen = int(r_contentslen)
        offset += 4
        
        for i in range(offset, offset + r_contentslen - 1):
            if(recvDicData[i] != '\0'):
                r_contents += recvDicData[i]

        
        dictTuple = (r_title, r_url, r_contents)

        return dictTuple

    def recvWeb(self):
        recvDicData = sdb.generalRecv()
        r_type = ''
        r_urllen = ''
        r_url = ''
        r_titlelen = ''
        r_title = ''
        r_contentslen = ''
        r_contents = ''

        for i in range(12, 15):
            if(recvDicData[i] != '\0'):
                r_urllen += recvDicData[i]
        
        r_urllen = int(r_urllen)
        
        for i in range(12, 12 + r_urllen -1):
            if(recvDicData[i] != '\0'):
                r_url += recvDicData[i]

        offset = 12 + r_urllen

        for i in range(offset, offset+3):
            if(recvDicData[i] != '\0'):
                r_titlelen += recvDicData[i]
        
        r_titlelen = int(r_titlelen)
        offset += 4
        
        for i in range(offset, offset + r_titlelen - 1):
            if(recvDicData[i] != '\0'):
                r_title += recvDicData[i]

        offset = 12 + r_titlelen

        for i in range(offset, offset+3):
            if(recvDicData[i] != '\0'):
                r_contentslen += recvDicData[i]
        
        r_contentslen = int(r_contentslen)
        offset += 4
        
        for i in range(offset, offset + r_contentslen - 1):
            if(recvDicData[i] != '\0'):
                r_contents += recvDicData[i]

        
        webTuple = (r_title, r_url, r_contents)

        return webTuple
   