#-*- coding: cp949-*-
 
from SearchDB import PORT, HOST, s
import SearchDB
from SearchDB import buf_data
BUF_SIZE = 67000



def makeFullContents(tempTupleList):
    fullContents = ''
    tempContentsTupleList = []
    for i in range(0, len(tempTupleList)):
        if(tempTupleList[i][1] == '505' or tempTupleList[i][1] == '507'): # 패킷 종류가 사전결과 , 웹 결과일 때
            contentsCnt = tempTupleList[i][2]   # 컨텐츠 나눈 개수 저장
            for j in range(1, contentsCnt+1): # 결과패킷 다음 패킷의 컨텐츠만큼 포문 돌리기
                fullContents += tempTupleList[i+j][3] # 컨텐츠 이어줌
            tempContentsTuple = (tempTupleList[i][4], tempTupleList[i][3], fullContents) # title, url, contents 튜플 만들기
            tempContentsTupleList.append(tempContentsTuple)
            fullContents = ''
        elif(tempTupleList[i][1] == '504'):
            tempSubTuple = (tempTupleList[i][2], tempTupleList[i][3], tempTupleList[i][4])
            tempContentsTupleList.append(tempSubTuple)
        #tempContentsTupleList.append(tempContentsTuple)
    return tempContentsTupleList
  



class c_searcher(): 
    def __init__(self, mode, keyword, page):
        self.mode = mode
        self.keyword = keyword
        self.page = page
    
    def AllSearcher(self):
        global buf_data
        total_dataList = []
        total_data = ''
        ret = []
        contentsret = []
        num = 0
        pCNum = 0
        tempTupleList = []
        currentIndex = 0
        nextIndex = 0
        SearchDB.connect(HOST, PORT)
        print ("connect")

        SearchDB.reqWord(self.mode, self.keyword, self.page)
        print("reqword - mode : ", self.mode)
        print("reqword - keyword: ", self.keyword)
        print("reqword - page : ", self.page)
       

        buf_data += SearchDB.recvBuf()
        resultNum = SearchDB.recvNum(buf_data[0:16])
        buf_data = buf_data[16:]
        while(num < 7):
            tempTuple = SearchDB.returnEachPacket(buf_data)
            if(tempTuple[1] == '505' or tempTuple[1] == '507'):
                pContentsNum = tempTuple[2]
            if(tempTuple[1] == '506' or tempTuple[1] == '508'): # web contents packet 일 때
                num -= 1
                pCNum += 1
            
            tempTupleList.append(tempTuple)

            if(pCNum == pContentsNum):
                pCNum = 0
                if(num+1 == resultNum):
                    break
            buf_data = buf_data[int(tempTuple[0]): ] #tempTuple[0] : current packet size
            
            num += 1
       
        while(num < 9):    
            tempTuple = SearchDB.returnEachPacket(buf_data)
            tempTupleList.append(tempTuple)

            buf_data = buf_data[int(tempTuple[0]): ] #tempTuple[0] : current packet size
            num += 1        
            
        print (tempTupleList)
        SearchDB.closesocket()
             
        allTupleList = makeFullContents(tempTupleList)
        return tuple(allTupleList)





    def WebSearcher(self):
        global buf_data
        total_dataList = []
        total_data = ''
        ret = []
        contentsret = []
        num = 0
        pCNum = 0
        tempTupleList = []
        currentIndex = 0
        nextIndex = 0
        SearchDB.connect(HOST, PORT)
        print ("connect")

        SearchDB.reqWord(self.mode, self.keyword, self.page)
        print("reqword - mode : ", self.mode)
        print("reqword - keyword: ", self.keyword)
        print("reqword - page : ", self.page)
       

        buf_data += SearchDB.recvBuf()
        resultNum = SearchDB.recvNum(buf_data[0:16])
        buf_data = buf_data[16:]
        while(num < resultNum+1):
            tempTuple = SearchDB.returnEachPacket(buf_data)
            if(tempTuple[1] == '507'):
                pContentsNum = tempTuple[2]
            if(tempTuple[1] == '508'): # web contents packet 일 때
                num -= 1
                pCNum += 1
                
            tempTupleList.append(tempTuple)

            if(pCNum == pContentsNum):
                pCNum = 0
                if(num+1 == resultNum):
                    break
            buf_data = buf_data[int(tempTuple[0]): ] #tempTuple[0] : current packet size
            
            num += 1
            
            
        print (tempTupleList)
        SearchDB.closesocket()
             
        webTupleList = makeFullContents(tempTupleList)
        return tuple(webTupleList)

    def DictSearcher(self):
        global buf_data
        total_dataList = []
        total_data = ''
        ret = []
        contentsret = []
        num = 0
        pCNum = 0
        pContentsNum = 0
        tempTupleList = []
        currentIndex = 0
        nextIndex = 0
        SearchDB.connect(HOST, PORT)
        print ("connect")

        SearchDB.reqWord(self.mode, self.keyword, self.page)
        print("reqword - mode : ", self.mode)
        print("reqword - keyword: ", self.keyword)
        print("reqword - page : ", self.page)
       

        buf_data += SearchDB.recvBuf()
        resultNum = SearchDB.recvNum(buf_data[0:16])
        buf_data = buf_data[16:]
        while(num < resultNum+1):
            tempTuple = SearchDB.returnEachPacket(buf_data)
            if(tempTuple[1] == '505'):
                pContentsNum = tempTuple[2]
            if(tempTuple[1] == '506'): # web contents packet 일 때
                num -= 1
                pCNum += 1
                
            tempTupleList.append(tempTuple)

            if(pCNum == pContentsNum):
                pCNum = 0
                if(num+1 == resultNum):
                    break
            buf_data = buf_data[int(tempTuple[0]): ] #tempTuple[0] : current packet size
            
            num += 1
            
            
        print (tempTupleList)
        SearchDB.closesocket()
             
        dictTupleList = makeFullContents(tempTupleList)
        return tuple(dictTupleList)
    
    def SubSearcher(self):
        global buf_data
        total_dataList = []
        total_data = ''
        ret = []
        contentsret = []
        num = 0
        pCNum = 0
        tempTupleList = []
        currentIndex = 0
        nextIndex = 0
        SearchDB.connect(HOST, PORT)
        print ("connect")

        SearchDB.reqWord(self.mode, self.keyword, self.page)
        print("reqword - mode : ", self.mode)
        print("reqword - keyword: ", self.keyword)
        print("reqword - page : ", self.page)
       

        buf_data += SearchDB.recvBuf()
        resultNum = SearchDB.recvNum(buf_data[0:16])
        buf_data = buf_data[16:]
        while(num < resultNum):
            tempTuple = SearchDB.returnEachPacket(buf_data)
            tempTupleList.append(tempTuple)

            buf_data = buf_data[int(tempTuple[0]): ] #tempTuple[0] : current packet size
            num += 1
            
            
        print (tempTupleList)
        SearchDB.closesocket()
        #subTupleList = makeSubResult(tempTupleList)   
        subTupleList = makeFullContents(tempTupleList)
        return tuple(subTupleList)

     
        
if __name__ == '__main__':
    print ("start SubSearcher.py... ")
    
    searcher = c_searcher('allsearch', 'keyword', 1)
    webTuple = searcher.AllSearcher()
    print(webTuple)