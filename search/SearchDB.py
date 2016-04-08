#-*- coding:cp949-*-
import socket
import re
#from C_Python_Socket import generalSend, generalRecv
#import C_Python_Socket
pType = dict(B_C_REQ_WORD = '501', B_S_ANS_SUBTITLE = '504', B_S_ANS_DICTIONARY = '505', B_S_ANS_DICTIONARY_CONTENTS = '506', 
             B_S_ANS_COUNT = '507', B_S_ANS_WEB = '507', B_S_ANS_WEB_CONTENTS = '508') # ��Ŷ Ÿ��

##############################################################
# SOCKET NETWORKING
HOST = '127.0.0.1'                # The remote host
PORT = 10001        # The same port as used by the server
s = socket.socket()
##############################################################

buf_data = ''
BUF_SIZE = 67000

def FillSpacePacket(dataLen, index):
    """��Ŷ�� �ڸ����� ä���� �Ҷ� ����(' ')���� ������� ä����
    dataLen : �м��� ���ϴ� ������ ����
    index : space�� ä�� �ε��� �ִ밪
    ex)
    data = 'abcd'
    data += FillSpacePacket(data.__len__(), 5)
    print(data)
    ��� : 'abcd  '
    ��ĭ �ΰ� ����"""
    index += 1
    space = ''
    if dataLen < index:
        for count in range(0, index-dataLen):
            space += ' '
    return space

def isASCII(text): 
   """ASCII�������� �Ǻ�. text�� ASCII�� �ƴ� ���ڰ� �Ѱ��� ������ False, ������ True"""
   return not bool(re.search('[^\x00-\x7E]', text))

def __Len_Cstyle__(text):
   """text�� C ��Ÿ�� ���̷� ����"""
   CLen = 0
   for i in text:
      if isASCII(i):
         CLen += 1
      else: CLen += 2
   return CLen
 



def connect(ip, port):
    """����ϱ� �� ���� ����
    1) import socket
    2) �������� s = socket.socket()�� ����"""
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = ip                # The remote host
    PORT = port              # The same port as used by the server
    s.connect((HOST, PORT))

def closesocket():
    global s
    s.close()

def recvBuf():
    global s
    buf = s.recv(BUF_SIZE)
    buf = buf.decode('cp949')
    return buf

def reqWord(mode, keyword, page):
   
    if mode == 'allsearch':
        reqmode = '1'
    elif mode == 'websearch':
        reqmode = '2'
    elif mode == 'dictsearch':
        reqmode = '3'
    elif mode == 'smisearch':
        reqmode = '4'

    #keywordcnt = len(keywordList)
    # �ӽ�
    keywordcnt = 1
    keywordcnt = str(keywordcnt)
    pagecnt = int((page-1)/10 + 1)
        
    data = ''       
    sendData = ''
    keywordlen = __Len_Cstyle__(keyword)
    keywordlen = str(keywordlen)

                         
    data += pType['B_C_REQ_WORD'] # ��Ŷ req Ÿ��
    data += '\0'
    data += FillSpacePacket(data.__len__(), 3)
       
    data += reqmode # �˻� ���
    data += '\0'
    data += FillSpacePacket(data.__len__(), 7)
       
    data += keywordcnt# Ű���� ����
    data += '\0'
    data += FillSpacePacket(data.__len__(), 11)
        
    data += keywordlen
    data += '\0'
    keywordlenSpace = FillSpacePacket(keywordlen.__len__(), 2)
    data += keywordlenSpace
        
    data += keyword


    dataLen = __Len_Cstyle__(data) + 8
    dataLen = str(dataLen)
    dataLen += '\0'
    dataLen += FillSpacePacket(dataLen.__len__(), 7)
    sendData += dataLen
    sendData += data
    sendData = sendData.encode('cp949')

        
    s.sendall(sendData)

def recvNum(recvData):
    n_totallen = ''
    n_type = ''
    n_num = ''
    
    for i in range(0, 8):
        if(recvData[i] != '\0'):
            n_totallen += recvData[i]

    
    n_totallen = int(n_totallen)
    for i in range(8, 12):
        if(recvData[i] != '\0'):
            n_type += recvData[i]

   
    for i in range(12, 16):
        if(recvData[i] != '\0'):
            n_num += recvData[i]

    n_num = int(n_num)

   
    return n_num


def returnEachPacket(buf_data):
    p_totallen = ''
    p_type = ''

    #global buf_data
    try:
        for i in range(0, 8):
            if(buf_data[i] != '\0'):
                p_totallen += buf_data[i]
    except IndexError:
        buf_data += recvBuf()
        for i in range(0, 8):
            if(buf_data[i] != '\0'):
                p_totallen += buf_data[i]

    p_totallen = int(p_totallen)
    if(p_totallen > len(buf_data)):
        while(p_totallen < len(buf_data)):
            buf_data += recvBuf()

    for i in range(8, 12):
        if(buf_data[i] != '\0'):
                p_type += buf_data[i]

        
    if(p_type == '504'):
        # �ڸ� �м� �Լ�
        tempTuple = recvSub(buf_data)
    elif(p_type == '505'):
        # ���� �м� �Լ�
        tempTuple = recvDict(buf_data)
    elif(p_type == '506'):
        # ���� contents �м� �Լ�
        tempTuple = recvDictContents(buf_data)
    elif(p_type == '507'):
        # ���м� �Լ�
        tempTuple = recvWeb(buf_data)
    elif(p_type == '508'):
        # �� contents �м� �Լ�
        tempTuple = recvWebContents(buf_data)

        
    return tempTuple

def returnOffset(tempTuple):
    offset = tempTuple[0]
    return offset

def recvAll(self):
    a_totallen = ''
    a_type = ''
    allTempList = []
    packetnum = 0
    offset = 0
    for i in range(offset, offset+8):
        if(recvData[i] != '\0'):
            a_totallen += recvData[i]

    offset += 8
    a_totallen = int(a_totallen)
    for i in range(offset, offset+4):
        if(recvData[i] != '\0'):
            a_type += recvData[i]

            
    if(a_type == '504'): # ���� ��Ŷ�� �ڸ��� ��
        for i in range(0, a_totallen):
            allTuple = recvSub()
        typeTuple = tuple(a_type)
        allTuple = typeTuple + allTuple
    elif(a_type == '505'): # ���� ��Ŷ�� ������ ��
        for i in range(0, a_totallen):
            allTuple = recvDict()
        typeTuple = tuple(a_type)
        allTuple = typeTuple + allTuple
    elif(a_type == '506'): # ���� ��Ŷ�� ���� ��
        for i in range(0, a_totallen):
            allTuple = recvWeb()
        typeTuple = tuple(a_type)
        allTuple = typeTuple + allTuple
    return allTuple
       
def recvSub(buf_data):
    #global buf_data
    s_totallen = ''
    s_type = ''
    s_keywordlen = ''
    s_keyword = ''
    s_urllen = ''
    s_url = ''
    s_titlelen = ''
    s_title = ''
    s_englen = ''
    s_eng = ''
    s_korlen = ''
    s_kor = ''

    for i in range(0, 8):
        if(buf_data[i] != '\0'):
            s_totallen += buf_data[i]
        
    s_totallen = int(s_totallen)
        
    for i in range(8, 12):
        if(buf_data[i] != '\0'):
            s_type += buf_data[i]

    offset = 12
    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            s_titlelen += buf_data[i]
        
    s_titlelen = int(s_titlelen)
    offset += 4
        
    for i in range(offset, offset + s_titlelen):
        if(buf_data[i] != '\0'):
            s_title += buf_data[i]

    offset = offset + s_titlelen

    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            s_englen += buf_data[i]
        
    s_englen = int(s_englen)
    offset += 4
        
    for i in range(offset, offset + s_englen):
        if(buf_data[i] != '\0'):
            s_eng += buf_data[i]

    offset = offset + s_englen

    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            s_korlen += buf_data[i]
        
    s_korlen = int(s_korlen)
    offset += 4
        
    for i in range(offset, offset + s_korlen):
        if(buf_data[i] != '\0'):
            s_kor += buf_data[i]
                           
    #subTuple = (s_totallen, s_type, s_title, s_eng, s_kor)
    subTuple = (s_totallen, s_type, s_title, s_eng, s_kor)
    return subTuple


def recvDict(buf_data):
    d_totallen = ''
    d_type = ''
    d_urllen = ''
    d_url = ''
    d_titlelen = ''
    d_title = ''
    d_contentsnum = ''
    d_contents = ''

    for i in range(0, 8):
        if(buf_data[i] != '\0'):
            d_totallen += buf_data[i]
        
    d_totallen = int(d_totallen)
        
    for i in range(8, 12):
        if(buf_data[i] != '\0'):
            d_type += buf_data[i]


    for i in range(12, 16):
        if(buf_data[i] != '\0'):
            d_contentsnum += buf_data[i]

    d_contentsnum = int(d_contentsnum)
    
    for i in range(16, 20):
        if(buf_data[i] != '\0'):
            d_urllen += buf_data[i]
        
    d_urllen = int(d_urllen)
        
    for i in range(20, 20 + d_urllen):
        if(buf_data[i] != '\0'):
            d_url += buf_data[i]

    offset = 20 + d_urllen

    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            d_titlelen += buf_data[i]
        
    d_titlelen = int(d_titlelen)
    offset += 4
        
    for i in range(offset, offset + d_titlelen):
        if(buf_data[i] != '\0'):
            d_title += buf_data[i]

    dictTuple = (d_totallen, d_type, d_contentsnum,  d_url, d_title)

    return dictTuple
   

def recvDictContents(buf_data):
    #self.__init__(self, mode, keyword)
    #global buf_data
    d_totallen = ''
    d_type = ''
    d_urllen = ''
    d_url = ''
    d_contentslen = ''
    d_contents = ''

    for i in range(0, 8):
        if(buf_data[i] != '\0'):
            d_totallen += buf_data[i]
        
    d_totallen = int(d_totallen)
        
    for i in range(8, 12):
        if(buf_data[i] != '\0'):
            d_type += buf_data[i]

    for i in range(12, 16):
        if(buf_data[i] != '\0'):
            d_urllen += buf_data[i]
        
    d_urllen = int(d_urllen)
        
    for i in range(16, 16 + d_urllen):
        if(buf_data[i] != '\0'):
            d_url += buf_data[i]

    offset = 16 + d_urllen

    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            d_contentslen += buf_data[i]
        
    d_contentslen = int(d_contentslen)
    offset += 4
        
    for i in range(offset, offset + d_contentslen):
        if(buf_data[i] != '\0'):
            d_contents += buf_data[i]

    dictContentsTuple = (d_totallen, d_type, d_url, d_contents)

    return dictContentsTuple

def recvWeb(buf_data):
    #global buf_data
    w_totallen = ''
    w_type = ''
    w_urllen = ''
    w_url = ''
    w_titlelen = ''
    w_title = ''
    w_contentsnum = ''
    w_contents = ''

    for i in range(0, 8):
        if(buf_data[i] != '\0'):
            w_totallen += buf_data[i]
        
    w_totallen = int(w_totallen)
        
    for i in range(8, 12):
        if(buf_data[i] != '\0'):
            w_type += buf_data[i]


    for i in range(12, 16):
        if(buf_data[i] != '\0'):
            w_contentsnum += buf_data[i]

    w_contentsnum = int(w_contentsnum)
    
    for i in range(16, 20):
        if(buf_data[i] != '\0'):
            w_urllen += buf_data[i]
        
    w_urllen = int(w_urllen)
        
    for i in range(20, 20 + w_urllen):
        if(buf_data[i] != '\0'):
            w_url += buf_data[i]

    offset = 20 + w_urllen

    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            w_titlelen += buf_data[i]
        
    w_titlelen = int(w_titlelen)
    offset += 4
        
    for i in range(offset, offset + w_titlelen):
        if(buf_data[i] != '\0'):
           w_title += buf_data[i]

    webTuple = (w_totallen, w_type, w_contentsnum,  w_url, w_title)

    return webTuple
   
def recvWebContents(buf_data):
    #global buf_data
    w_totallen = ''
    w_type = ''
    w_urllen = ''
    w_url = ''
    w_contentslen = ''
    w_contents = ''

    for i in range(0, 8):
        if(buf_data[i] != '\0'):
            w_totallen += buf_data[i]
        
    w_totallen = int(w_totallen)
        
    for i in range(8, 12):
        if(buf_data[i] != '\0'):
            w_type += buf_data[i]

    for i in range(12, 16):
        if(buf_data[i] != '\0'):
            w_urllen += buf_data[i]
        
    w_urllen = int(w_urllen)
        
    for i in range(16, 16 + w_urllen):
        if(buf_data[i] != '\0'):
            w_url += buf_data[i]

    offset = 16 + w_urllen

    for i in range(offset, offset+4):
        if(buf_data[i] != '\0'):
            w_contentslen += buf_data[i]
        
    w_contentslen = int(w_contentslen)
    offset += 4
        
    for i in range(offset, offset + w_contentslen):
        if(buf_data[i] != '\0'):
            w_contents += buf_data[i]

    webContentsTuple = (w_totallen, w_type, w_url, w_contents)

    return webContentsTuple