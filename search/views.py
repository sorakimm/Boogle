#-*- coding:cp949
from django.shortcuts import render
from Searcher import c_searcher
from django.http import HttpResponse

#for template
from django.template import Context, loader

listSize = 10
showLength = 100

past_mode=''
past_keyword=''

# Create your views here.
def main_page(request):
    return render(request, 'search/main_page.html', {})


def SearchPage(req, mode, keyword, page=1): # req : request
    global listSize
    global past_mode
    global past_keyword
    page = int(page)
    #print (page)
    print ("SearchPage - mode : ", mode)
    print ("SearchPage - keyword : ", keyword)
    print ("SearchPage - page : ", page)
    ######## keyword 같고 모드만 바뀌었을 때 데이터 가지고 있는 조건
    #if(past_mode == ''):
    #    past_mode = mode
    #if(past_keyword==''):
    #    past_keyword = keyword

    #if past_keyword != keyword:
    #    resultTup = callSearch(mode, keyword)
    ########
    #print (resultTup)
    resultTup = callSearch(mode, keyword, page)
    
    if mode != 'allsearch':
        showItemTup = resultTup[((page-1)*listSize):(page*listSize)] # 한번에 열개씩
        searchList = matchContentData(mode, keyword, showItemTup) # 페이지에 표시할 데이터 생성
    
        totalSize = len(resultTup) # 검색결과 밑 네비게이터 부분
        pageCnt = int(totalSize / listSize)
        if(totalSize % listSize) != 0:
            pageCnt += 1
        pageList = range(1, pageCnt+1)
        if mode == 'smisearch':
            tpl = loader.get_template('search/sub_search.html')
        elif mode == 'dictsearch':
            tpl = loader.get_template('search/dict_search.html') # 템플릿 로딩
        elif mode == 'websearch':
            tpl = loader.get_template('search/web_search.html') # 템플릿 로딩
        
        ctx = Context({
            'searchList' : searchList, # 변수값 채우기
            'keyword' : keyword,
            'mode' : mode,
            'pageList' : pageList,
            })

        html = tpl.render(ctx)
        return HttpResponse(html)

    elif mode == 'allsearch':
        web_resultTup = (resultTup[0], resultTup[1], resultTup[2])
        dict_resultTup = (resultTup[3], resultTup[4], resultTup[5])
        smi_resultTup = (resultTup[6], resultTup[7], resultTup[8])
        
        web_searchList = matchContentData('websearch', keyword, web_resultTup)
        dict_searchList = matchContentData('dictsearch', keyword, dict_resultTup)
        smi_searchList = matchContentData('smisearch', keyword, smi_resultTup)
        
        tpl = loader.get_template('search/all_search.html') # 템플릿 로딩
        ctx = Context({
            'web_searchList' : web_searchList, # 변수값 채우기
            'dict_searchList' : dict_searchList, # 변수값 채우기
            'smi_searchList' : smi_searchList, # 변수값 채우기
            'keyword' : keyword,
            'mode' : mode,
            })

        print('web_searchList : ', web_searchList)
        print('dict_searchList : ', dict_searchList)
        print('smi_searchList : ', smi_searchList)
       
        html = tpl.render(ctx)
        return HttpResponse(html)

def callSearch(mode, keyword, page):
    print("callSearch - mode : ", mode)
    print("callSearch - keyword : ", keyword)
    print("callSearch - page : ", page)
    
    searcher = c_searcher(mode, keyword, page)
    if mode == "allsearch":
        print("callSearch - mode:allsearch")
        searchTup = searcher.AllSearcher()
        print(searchTup)
    elif mode == "websearch":
        searchTup = searcher.WebSearcher()
    elif mode == "dictsearch":
        searchTup = searcher.DictSearcher(mode, keyword, page)
    elif mode == "smisearch":
        searchTup = searcher.SubSearcher(mode, keyword, page)
    return searchTup

def matchContentData(mode, keyword, listTup):
    #"템플릿에 사용될 데이터 생성 "
    ResultData = []
    
    #elif(mode == "allsearch"):
        #print ("allsearch listTup : ", listTup)
        #for i in range(0, 3):
        #    conTitle = listTup[i][0].replace(listTup[i][0], "<b>" + listTup[i][0] + "</b>")
        #    conEng = listTup[i][1]
        #    conKor = listTup[i][2]
        #    ResultData.append(({'title':conTitle, 'eng':conEng, 'kor':conKor}))
        #for i in range(3, len(listTup)):
        #    conTitle = listTup[i][0].replace(listTup[i][0], "<b>" +listTup[i][0] + "</b>")
        #    conPreview = makeContentPreview(keyword, listTup[i][1])
        #    conLink = listTup[i][2]
        #    ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))
           


    if(mode == "websearch"):
        for item in listTup:
            conTitle = item[0].replace(keyword, "<b>" + keyword + "</b>")
            conPreview = makeContentPreview(keyword, item[2])
            conLink = item[1]
            ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))

   
    elif(mode == "dictsearch"):
        for item in listTup:
            conTitle = item[0].replace(keyword, "<b>" + keyword + "</b>")
            conPreview = makeContentPreview(keyword, item[2])
            conLink = item[1]
            ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))


    elif(mode == "smisearch"):
        for item in listTup:
            conTitle = item[0].replace(item[0], "<b>" + item[0] + "</b>")
            conEng = item[1]
            conKor = item[2]
            ResultData.append(({'title':conTitle, 'eng':conEng, 'kor':conKor}))
            #print (ResultData)
        #return ResultData
    
    print ("ResultData : ", ResultData) 
    return ResultData

def makeContentPreview(keyword, text):
    global showLength
    contData = text
    #contData = contData.decode('utf-8')
    #strTitle = contData.readline()
    pos = contData.find(keyword)

    PreviewData = ""
    if pos > (showLength/2):
        PreviewData = contData[pos - (showLength / 2) : pos + (showLength / 2)]
    else:
        PreviewData = contData[0:showLength]

    if len(PreviewData) <= 0:
        PreviewData = "empty contents"
    
    # 데이터에서 키워드에 해당하는 곳 불드체로 표시
    #strTitle = strTitle.replace(keyword, "<b>" + keyword + "</b>")
    PreviewData = PreviewData.replace(keyword, "<b>" + keyword + "</b>")

    return PreviewData

def makeTitle(title):
    strTitle = title
    strTitle = strTitle.replace(keyword, "<b>" + keyword + "</b>")
    return strTitle
