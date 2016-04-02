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
    def reqWord(self, mode, keyword):
        modeTuple = (4, mode)
        wordTuple = (4, keyword)
        sdb.generalSend(C_Python_Socket.B_C_REQ_WORD, modeTuple, wordTuple, delay=0.01)
        

    def recvSub(self):
        recvsub = sdb.generalRecv()
        r_type = ''
        r_urllen = ''
        r_url = ''
        r_titlelen = ''
        r_title = ''
        for i in range(12, 15):
            if(data[i] != '\0'):
                b_urllen += data[i]
        
        r_urllen = int(r_urllen)
        for i in range(16,  16+r_urllen-1):
            if(data[i] != '\0'):
                r_url += data[i]
        
        for i in range(0, 0+int(b_urllen)):
            b_url += data[i+7]             
        

       
        print ("b_type : ", b_type)
        print ("b_urllen : ", b_urllen)
        print ("b_url : ", b_url)
        
        #b_list = "".join(b_listTemp)
        
        #print ("b_list : ", b_list)

        print ("-------------------------")
     
        return b_url


    def recvDict(self):
            b_type = ''
            b_urllen = ''
            b_url = ''
            data = s.recv(1024)
            data = data.decode('cp949')
             
            if not data:
                print ("no data received")
                pass

            print ('Received URL----------', data)
            b_listTemp = []
        
            for i in range(0, 3):
                if(data[i] != '\0'):
                    b_type += data[i]
        
            for i in range(4, 7):
                if(data[i] != '\0'):
                    b_urllen += data[i]
        
            for i in range(0, 0+int(b_urllen)):
                b_url += data[i+7]             
        

       
            print ("b_type : ", b_type)
            print ("b_urllen : ", b_urllen)
            print ("b_url : ", b_url)
        
            #b_list = "".join(b_listTemp)
        
            #print ("b_list : ", b_list)

            print ("-------------------------")
     
            return b_url

    def recvWeb(self):
            b_type = ''
            b_urllen = ''
            b_url = ''
            data = s.recv(1024)
            data = data.decode('cp949')
             
            if not data:
                print ("no data received")
                pass

            print ('Received URL----------', data)
            b_listTemp = []
        
            for i in range(0, 3):
                if(data[i] != '\0'):
                    b_type += data[i]
        
            for i in range(4, 7):
                if(data[i] != '\0'):
                    b_urllen += data[i]
        
            for i in range(0, 0+int(b_urllen)):
                b_url += data[i+7]             
        

       
            print ("b_type : ", b_type)
            print ("b_urllen : ", b_urllen)
            print ("b_url : ", b_url)
        
            #b_list = "".join(b_listTemp)
        
            #print ("b_list : ", b_list)

            print ("-------------------------")
     
            return b_url
   