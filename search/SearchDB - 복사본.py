#-*- coding:cp949-*-
import socket
from C_Python_Socket import generalSend, generalRecv
#import C_Python_Socket
sType = dict(B_C_REQ_WORD = '509', B_S_ANS_SUBTITLE = '504', B_S_ANS_COUNT = '503', B_S_ANS_DICTIONARY = '504') # ��Ŷ Ÿ��

##############################################################
# SOCKET NETWORKING
HOST = '127.0.0.1'                # The remote host
PORT = 10001        # The same port as used by the server
s = socket.socket()
##############################################################



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
 
sdb = C_Python_Socket

class SearchDB:
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
        s.close();

    def __init__(self, mode, keyword):
        
        self.recvData = s.recv(67000)
        self.keyword = keyowrd
        

    def reqWord(self, mode, keyword, page):
        self.__init__(self, mode, keyword)
        if mode == 'allsearch':
            reqmode = 1
        elif mode == 'websearch':
            reqmode = 2
        elif mode == 'smisearch':
            reqmode = 3
        elif mode == 'dictsearch':
            reqmode = 4

        pagemode = (page-1)/10 + 1
        keywordTuple = (4, keyword)
        sdb.generalSend(C_Python_Socket.B_C_REQ_WORD, reqmode, pagemode, keywordTuple,  delay=0.01)

    def recvNum(self):
        self.__init__(self, mode, keyword)
        n_totallen = ''
        n_type = ''
        n_numlen = ''
        n_num = ''
        offset = 0
        for i in range(offset, offset+7):
            if(recvData[i] != '\0'):
                n_totallen += recvData[i]

        offset += 8
        a_totallen = int(a_totallen)
        for i in range(offset, offset+3):
            if(recvData[I] != '\0'):
                a_type += recvData[i]

        offset += 4

        for i in range(offset, offset+3):
            if(recvData[I] != '\0'):
                a_numlen += recvData[i]

        a_numlen = int(a_numlen)

        for i in range(offset, a_numlen-1):
            if(recvData[I] != '\0'):
                a_num += recvData[i]

        a_num = int(a_num)

        return a_num

    def recvAll(self):
        a_totallen = ''
        a_type = ''
        allTempList = []
        packetnum = 0
        offset = 0
        for i in range(offset, offset+7):
            if(recvData[i] != '\0'):
                a_totallen += recvData[i]

        offset += 8
        a_totallen = int(a_totallen)
        for i in range(offset, offset+3):
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
        sself.__init__(self, mode, keyword)
        #while packetnum < 10:
        #    packetnum += 1
            
        #    for i in range(offset, offset+7):
        #        if(recvData[I] != '\0'):
        #            a_totallen += recvData[i]

        #    offset += 8
        #    a_totallen = int(a_totallen)
        #    for i in range(offset, offset+3):
        #        if(recvData[I] != '\0'):
        #            a_type += recvData[i]

            
        #    if(r_type == '504'): # ���� ��Ŷ�� �ڸ��� ��
        #        for i in range(0, a_totallen):
        #            tempTuple = recvSub()

        #    elif(r_type == '505'): # ���� ��Ŷ�� ������ ��
        #        for i in range(0, a_totallen):
        #            tempTuple = recvDict()

        #    elif(r_type == '506'): # ���� ��Ŷ�� ���� ��
        #        for i in range(0, a_totallen):
        #            tempTuple = recvWeb()

        #    allTempList.append(tempTuple)
            
        #    offset +=a_totallen


    def recvSub(self):
        self.__init__(self, mode, keyword)
        s_totalsize = ''
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

        for i in range(0, 7):
            if(recvData[i] != '\0'):
                s_totalsize += recvData[i]
        
        s_totalsize = int(s_totalsize)
        
        for i in range(8, 11):
            if(recvData[i] != '\0'):
                s_type += recvData[i]

        for i in range(12, 15):
            if(recvData[i] != '\0'):
                s_keywordlen += recvData[i]
        
        s_keywordlen = int(r_keywordlen)
        
        for i in range(16, 16 + s_keywordlen -1):
            if(recvData[i] != '\0'):
                s_keyword += recvData[i]

        offset = 16 + s_keywordlen

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                s_titlelen += recvData[i]
        
        s_titlelen = int(s_titlelen)
        offset += 4
        
        for i in range(offset, offset + s_titlelen - 1):
            if(recvData[i] != '\0'):
                s_title += recvData[i]

        offset = offset + s_titlelen

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                s_englen += recvData[i]
        
        s_englen = int(s_englen)
        offset += 4
        
        for i in range(offset, offset + s_englen - 1):
            if(recvData[i] != '\0'):
                s_eng += recvData[i]

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                s_korlen += recvData[i]
        
        s_korlen = int(s_korlen)
        offset += 4
        
        for i in range(offset, offset + s_korlen - 1):
            if(recvData[i] != '\0'):
                s_kor += recvData[i]
                           
        subTuple = (s_title, s_eng, s_kor)

        return subTuple




    def recvDict(self):
        self.__init__(self, mode, keyword)
        d_totalsize = ''
        d_type = ''
        d_urllen = ''
        d_url = ''
        d_titlelen = ''
        d_title = ''
       
        for i in range(0, 7):
            if(recvData[i] != '\0'):
                d_totalsize += recvData[i]
        
        d_totalsize = int(d_totalsize)
        
        for i in range(8, 11):
            if(recvData[i] != '\0'):
                d_type += recvData[i]

        for i in range(12, 15):
            if(recvData[i] != '\0'):
                d_urllen += recvData[i]
        
        d_urllen = int(d_urllen)
        
        for i in range(16, 16 + d_urllen -1):
            if(recvData[i] != '\0'):
                d_url += recvData[i]

        offset = 16 + d_urllen

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                d_titlelen += recvData[i]
        
        d_titlelen = int(d_titlelen)
        offset += 4
        
        for i in range(offset, offset + d_titlelen - 1):
            if(recvData[i] != '\0'):
                d_title += recvData[i]

        dictTuple = (url, d_title)

        return dictTuple

    def recvDictContents(self):
        self.__init__(self, mode, keyword)
        d_totalsize = ''
        d_type = ''
        d_urllen = ''
        d_url = ''
        d_contentslen = ''
        d_contents = ''

        for i in range(0, 7):
            if(recvData[i] != '\0'):
                d_totalsize += recvData[i]
        
        d_totalsize = int(d_totalsize)
        
        for i in range(8, 11):
            if(recvData[i] != '\0'):
                d_type += recvData[i]

        for i in range(12, 15):
            if(recvData[i] != '\0'):
                d_urllen += recvData[i]
        
        d_urllen = int(d_urllen)
        
        for i in range(16, 16 + d_urllen -1):
            if(recvData[i] != '\0'):
                d_url += recvData[i]

        offset = 16 + d_urllen

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                d_contentslen[i] += recvData[i]
        
        d_contentslen = int(d_contentslen)
        offset += 4
        
        for i in range(offset, offset + d_contentslen - 1):
            if(recvData[i] != '\0'):
                d_contents += recvData[i]

        dictContentsTuple = (url, d_contents)

        return dictContentsTuple

    def recvWeb(self):
        #self.__init__(self, mode, keyword)
        w_totalsize = ''
        w_type = ''
        w_urllen = ''
        w_url = ''
        w_titlelen = ''
        w_title = ''
        w_contentslen = ''
        w_contents = ''

        for i in range(0, 7):
            if(recvData[i] != '\0'):
                w_totalsize += recvData[i]
        
        w_totalsize = int(w_totalsize)
        
        for i in range(8, 11):
            if(recvData[i] != '\0'):
                w_type += recvData[i]

        for i in range(12, 15):
            if(recvData[i] != '\0'):
                w_urllen += recvData[i]
        
        w_urllen = int(w_urllen)
        
        for i in range(16, 16 + w_urllen -1):
            if(recvData[i] != '\0'):
                w_url += recvData[i]

        offset = 16 + w_urllen

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                w_titlelen += recvData[i]
        
        w_titlelen = int(w_titlelen)
        offset += 4
        
        for i in range(offset, offset + w_titlelen - 1):
            if(recvData[i] != '\0'):
                w_title += recvData[i]

        webTuple = (url, w_title)

        return webTuple
   
    def recvWebContents(self):
        self.__init__(self, mode, keyword)
        w_totalsize = ''
        w_type = ''
        w_urllen = ''
        w_url = ''
        w_contentslen = ''
        w_contents = ''

        for i in range(0, 7):
            if(recvData[i] != '\0'):
                w_totalsize += recvData[i]
        
        w_totalsize = int(w_totalsize)
        
        for i in range(8, 11):
            if(recvData[i] != '\0'):
                w_type += recvData[i]

        for i in range(12, 15):
            if(recvData[i] != '\0'):
                w_urllen += recvData[i]
        
        w_urllen = int(w_urllen)
        
        for i in range(16, 16 + w_urllen -1):
            if(recvData[i] != '\0'):
                w_url += recvData[i]

        offset = 16 + w_urllen

        for i in range(offset, offset+3):
            if(recvData[i] != '\0'):
                w_contentslen[i] += recvData[i]
        
        w_contentslen = int(w_contentslen)
        offset += 4
        
        for i in range(offset, offset + w_contentslen - 1):
            if(recvData[i] != '\0'):
                w_contents += recvData[i]

        webContentsTuple = (url, w_contents)

        return webContentsTuple