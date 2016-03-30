#-*- coding:cp949
from django.shortcuts import render
from Searcher import c_searcher
from django.http import HttpResponse

#for template
from django.template import Context, loader

listSize = 10
showLength = 100

# Create your views here.
def main_page(request):
    return render(request, 'search/main_page.html', {})


def SearchPage(req, mode, keyword, page=1): # req : request
    global listSize
    #mode = 'smisearch'
    #keyword = 'good'
    page = int(page)
    print (page)
    #if(mode == smisearch):
    #    resultTup = callSMISearch(keyword)
    #elif(mode == dictsearch):
    #    resultTup = callDICTSearch(keyword)
    #elif(mode == websearch):
    #    resultTup = callWEBSearch(keyword)
    resultTup = callSearch(mode, keyword)
    showItemTup = resultTup[((page-1)*listSize):(page*listSize)] # 한번에 열개씩
    
    searchList = matchContentData(mode, keyword, showItemTup) # 페이지에 표시할 데이터 생성
    #print(searchList)

    totalSize = len(resultTup) # 검색결과 밑 네비게이터 부분
    pageCnt = int(totalSize / listSize)
    if(totalSize % listSize) != 0:
        pageCnt += 1
    pageList = range(1, pageCnt+1)
    if mode == 'smisearch':
        tpl = loader.get_template('search/sub_search.html')
    else:
        tpl = loader.get_template('search/search.html') # 템플릿 로딩
    ctx = Context({
        'searchList' : searchList, # 변수값 채우기
        'keyword' : keyword,
        'mode' : mode,
        'pageList' : pageList,
        })

    html = tpl.render(ctx)
    return HttpResponse(html)

def callSearch(mode, keyword):
    searcher = c_searcher(keyword.encode('cp949'))
    if mode == "smisearch":
        searchTup = searcher.SubSearcher()
        
    #elif mode == "dictsearch":
    #    rfunc = DictSearcher(keyword)
    #elif mode == "websearch":
    #    rfunc = WebSearcher(keyword)

    return searchTup

def matchContentData(mode, keyword, listTup):
    #"템플릿에 사용될 데이터 생성 "
    ResultData = []
    if(mode == "smisearch"):
        for item in listTup:
            conTitle = item[0].replace(item[0], "<b>" + item[0] + "</b>")
            conEng = item[1]
            conKor = item[2]
            ResultData.append(({'title':conTitle, 'eng':conEng, 'kor':conKor}))
            #print (ResultData)
    return ResultData

    if(mode == "dictsearch" | mode == "websearch"):
        for item in listTup:
            conTitle = item[0].replace(keyword, "<b>" + keyword + "</b>")
            conPreview = makeContentPreview(keyword, item[2])
            conLink = item[1]
            ResultData.append(({'preview':conPreview, 'link':conLink, 'title':conTitle}))
    return ResultData

def makeContentPreview(keyword, text):
    global showLength
    contData = text
    contData = contData.decode('utf-8')
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
