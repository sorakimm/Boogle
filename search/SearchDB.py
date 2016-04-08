#-*- coding:cp949-*-
import socket
import re
import konlpy
from konlpy.tag import Komoran
import nltk
from nltk.tokenize import RegexpTokenizer
import ShareBuf

tokenizer = None
tagger = None
#from C_Python_Socket import generalSend, generalRecv
#import C_Python_Socket
pType = dict(B_C_REQ_WORD = '501', B_S_ANS_SUBTITLE = '504', B_S_ANS_DICTIONARY = '505', B_S_ANS_DICTIONARY_CONTENTS = '506', 
             B_S_ANS_COUNT = '507', B_S_ANS_WEB = '507', B_S_ANS_WEB_CONTENTS = '508') # ��Ŷ Ÿ��

##############################################################
# SOCKET NETWORKING
#HOST = '127.0.0.1'                # The remote host
#PORT = 10001        # The same port as used by the server
HOST = '192.168.0.177'
PORT = 20000
s = socket.socket()
##############################################################
ShareBuf.buf_data = ''
ShareBuf.BUF_SIZE = 67000


def getKorNoun(_keyword):#�±׾��� content���� ��縸 �����ϱ�
    keyword = _keyword[:]
    keyword = re.sub('[^��-�R \n]+', '', keyword)
    #print (contents)
   
    kkma = konlpy.tag.Kkma() #-Xmx128m �� �ٲٱ�
    #print("Get nouns from contents...")
    
    keywords = kkma.nouns(keyword)
    #print (type(keywords))
    #print ("kkma   : ", keywords)
   
    for i in range(0, len(keywords)):
        keywords[i] = re.sub(keywords[i], str(keywords[i]), keywords[i])
    #keywords = list(set(keywords))
    return keywords

def getEngNoun(_keyword):
    keyword = _keyword[:]
    keyword = re.sub('[^a-z|A-Z \n]+', '', keyword)
    tokenizer = RegexpTokenizer("[\w']+")
    keywords = tokenizer.tokenize(keyword)
   
    #pSub = re.compile("sub_")
    for i in range(0, len(keywords)):
        keywords[i] = re.sub(keywords[i], str(keywords[i]), keywords[i])
    
    return keywords

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
 
def makeKeywordList(keyword):
    "Ű���� �����ؼ� ����Ʈ �����"
    keywordList = []
    keywordKOList = getKorNoun(keyword)
    keywordENList = getEngNoun(keyword)
    keywordList = keywordKOList + keywordENList
    return keywordList

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
    buf = s.recv(ShareBuf.BUF_SIZE)
    buf = buf.decode('cp949')
    return buf

def reqWord(mode, keyword, page):
    eachKeywordLenList = []
    if mode == 'allsearch':
        reqmode = '1'
    elif mode == 'websearch':
        reqmode = '2'
    elif mode == 'dictsearch':
        reqmode = '3'
    elif mode == 'smisearch':
        reqmode = '4'

    keywordList = makeKeywordList(keyword)

    keywordcnt = str(len(keywordList))
   
   
    pagecnt = str(int((page-1)/10 + 1))
        
    data = ''       
    sendData = ''
    for i in range(0, int(keywordcnt)): # ��Ŷ �ȿ� �� ���� �м��� ���� ���� �ܾ���� ���� ����
        eachKeywordLen = __Len_Cstyle__(keywordList[i])
        eachKeywordLenList.append(eachKeywordLen)

                         
    data += pType['B_C_REQ_WORD'] # ��Ŷ req Ÿ��
    data += '\0'
    data += FillSpacePacket(data.__len__(), 3)
       
    data += reqmode # �˻� ���
    data += '\0'
    data += FillSpacePacket(data.__len__(), 7)
       
    data += keywordcnt# Ű���� ����
    data += '\0'
    data += FillSpacePacket(data.__len__(), 11)
     
    for i in range(0, int(keywordcnt)):
        data += str(eachKeywordLenList[i]) # �� �ܾ���� �߰�
        data += '\0'
        eachKeywordSpace = FillSpacePacket(str(eachKeywordLenList[i]).__len__(), 2)
        data += eachKeywordSpace
        data += keywordList[i] # �� �ܾ� �߰�

    data += pagecnt

    dataLen = __Len_Cstyle__(data) + 8
    dataLen = str(dataLen)
    dataLen += '\0'
    dataLen += FillSpacePacket(dataLen.__len__(), 7)
    sendData += dataLen
    sendData += data
    print("reqkeyword packet : ", sendData)
    sendData = sendData.encode('cp949')

    
    s.sendall(sendData)

def recvNum(recvData):
    while True:
        n_totallen = ''
        n_type = ''
        n_num = ''
        try:
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
            break
        except IndexError:
            recvData += recvBuf()
            continue
    
    n_num = int(n_num)

    return n_num


def returnEachPacket():
    while True:
        p_totallen = ''
        p_type = ''
        try:
            for i in range(0, 8):
                if(ShareBuf.buf_data[i] != '\0'):
                    p_totallen += ShareBuf.buf_data[i]
  
           
            p_totallen = int(p_totallen)
            if(p_totallen > len(ShareBuf.buf_data)):
                while(p_totallen > len(ShareBuf.buf_data)):
                    ShareBuf.buf_data += recvBuf()

            for i in range(8, 12):
                if(ShareBuf.buf_data[i] != '\0'):
                        p_type += ShareBuf.buf_data[i]
            break
        except IndexError:
            ShareBuf.buf_data += recvBuf()
            continue
    if(p_type == '504'):
        # �ڸ� �м� �Լ�
        tempTuple = recvSub()
    elif(p_type == '505'):
        # ���� �м� �Լ�
        tempTuple = recvDict()
    elif(p_type == '506'):
        # ���� contents �м� �Լ�
        tempTuple = recvDictContents()
    elif(p_type == '507'):
        # ���м� �Լ�
        tempTuple = recvWeb()
    elif(p_type == '508'):
        # �� contents �м� �Լ�
        tempTuple = recvWebContents()

        
    return tempTuple

def returnOffset(tempTuple):
    offset = tempTuple[0]
    return offset

def recvSub():
    while True:
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
        try:
            for i in range(0, 8):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_totallen += ShareBuf.buf_data[i]
        
            s_totallen = int(s_totallen)
        
            for i in range(8, 12):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_type += ShareBuf.buf_data[i]

            offset = 12
            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_titlelen += ShareBuf.buf_data[i]
        
            s_titlelen = int(s_titlelen)
            offset += 4
        
            for i in range(offset, offset + s_titlelen):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_title += ShareBuf.buf_data[i]

            offset = offset + s_titlelen

            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_englen += ShareBuf.buf_data[i]
        
            s_englen = int(s_englen)
            offset += 4
        
            for i in range(offset, offset + s_englen):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_eng += ShareBuf.buf_data[i]

            offset = offset + s_englen

            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_korlen += ShareBuf.buf_data[i]
        
            s_korlen = int(s_korlen)
            offset += 4
        
            for i in range(offset, offset + s_korlen):
                if(ShareBuf.buf_data[i] != '\0'):
                    s_kor += ShareBuf.buf_data[i]
            break
        except IndexError:
            ShareBuf.buf_data += recvBuf()
            continue                 
    #subTuple = (s_totallen, s_type, s_title, s_eng, s_kor)
    subTuple = (s_totallen, s_type, s_title, s_eng, s_kor)
    return subTuple




def recvDict():
    while True:
        d_totallen = ''
        d_type = ''
        d_urllen = ''
        d_url = ''
        d_titlelen = ''
        d_title = ''
        d_contentsnum = ''
        d_contents = ''
        try:
            for i in range(0, 8):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_totallen += ShareBuf.buf_data[i]
        
            d_totallen = int(d_totallen)
        
            for i in range(8, 12):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_type += ShareBuf.buf_data[i]


            for i in range(12, 16):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_contentsnum += ShareBuf.buf_data[i]

            d_contentsnum = int(d_contentsnum)
    
            for i in range(16, 20):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_urllen += ShareBuf.buf_data[i]
        
            d_urllen = int(d_urllen)
        
            for i in range(20, 20 + d_urllen):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_url += ShareBuf.buf_data[i]

            offset = 20 + d_urllen

            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_titlelen += ShareBuf.buf_data[i]
        
            d_titlelen = int(d_titlelen)
            offset += 4
        
            for i in range(offset, offset + d_titlelen):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_title += ShareBuf.buf_data[i]
            break
        except IndexError:
            ShareBuf.buf_data += recvBuf()
            continue

    dictTuple = (d_totallen, d_type, d_contentsnum,  d_url, d_title)

    return dictTuple
   

def recvDictContents():
    while True:
        d_totallen = ''
        d_type = ''
        d_urllen = ''
        d_url = ''
        d_contentslen = ''
        d_contents = ''
        try:
            for i in range(0, 8):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_totallen += ShareBuf.buf_data[i]
        
            d_totallen = int(d_totallen)
        
            for i in range(8, 12):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_type += ShareBuf.buf_data[i]

            for i in range(12, 16):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_urllen += ShareBuf.buf_data[i]
        
            d_urllen = int(d_urllen)
        
            for i in range(16, 16 + d_urllen):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_url += ShareBuf.buf_data[i]

            offset = 16 + d_urllen

            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_contentslen += ShareBuf.buf_data[i]
        
            d_contentslen = int(d_contentslen)
            offset += 4
        
            for i in range(offset, offset + d_contentslen):
                if(ShareBuf.buf_data[i] != '\0'):
                    d_contents += ShareBuf.buf_data[i]
            break
        except IndexError:
            ShareBuf.buf_data += recvBuf()
            continue

    dictContentsTuple = (d_totallen, d_type, d_url, d_contents)

    return dictContentsTuple

def recvWeb():
    while True:
        w_totallen = ''
        w_type = ''
        w_urllen = ''
        w_url = ''
        w_titlelen = ''
        w_title = ''
        w_contentsnum = ''
        w_contents = ''
        try:
            for i in range(0, 8):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_totallen += ShareBuf.buf_data[i]
        
            w_totallen = int(w_totallen)
        
            for i in range(8, 12):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_type += ShareBuf.buf_data[i]


            for i in range(12, 16):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_contentsnum += ShareBuf.buf_data[i]

            w_contentsnum = int(w_contentsnum)
    
            for i in range(16, 20):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_urllen += ShareBuf.buf_data[i]
        
            w_urllen = int(w_urllen)
        
            for i in range(20, 20 + w_urllen):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_url += ShareBuf.buf_data[i]

            offset = 20 + w_urllen

            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_titlelen += ShareBuf.buf_data[i]
        
            w_titlelen = int(w_titlelen)
            offset += 4
        
            for i in range(offset, offset + w_titlelen):
                if(ShareBuf.buf_data[i] != '\0'):
                   w_title += ShareBuf.buf_data[i]
            break

        except IndexError:
            ShareBuf.buf_data += recvBuf()
            continue
    webTuple = (w_totallen, w_type, w_contentsnum,  w_url, w_title)

    return webTuple
   
def recvWebContents():
    while True:
        w_totallen = ''
        w_type = ''
        w_urllen = ''
        w_url = ''
        w_contentslen = ''
        w_contents = ''
        try:
            for i in range(0, 8):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_totallen += ShareBuf.buf_data[i]
        
            w_totallen = int(w_totallen)
        
            for i in range(8, 12):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_type += ShareBuf.buf_data[i]

            for i in range(12, 16):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_urllen += ShareBuf.buf_data[i]
        
            w_urllen = int(w_urllen)
        
            for i in range(16, 16 + w_urllen):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_url += ShareBuf.buf_data[i]

            offset = 16 + w_urllen

            for i in range(offset, offset+4):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_contentslen += ShareBuf.buf_data[i]
        
            w_contentslen = int(w_contentslen)
            offset += 4
        
            for i in range(offset, offset + w_contentslen):
                if(ShareBuf.buf_data[i] != '\0'):
                    w_contents += ShareBuf.buf_data[i]
            break
        except IndexError:
            ShareBuf.buf_data += recvBuf()
            continue

    webContentsTuple = (w_totallen, w_type, w_url, w_contents)

    return webContentsTuple