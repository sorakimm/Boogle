#-*- coding: cp949 -*-
from django.http import HttpResponse

#for template
from django.template import Context, loader
from SubCrawler import *
from Searcher import SubSearcher, DictSearcher, WebSearcher
from Searcher import *
import os

#global value

listSize = 10
showLength = 100

def ParameterInputError(req):
    html = "error"
    return HttpResponse(html)

#def search_page(request):
#    return render(request, 'search/search.html', {})

   

def SearchPage(req, mode, keyword, page=1): # req : request
    global listSize
    mode = 'smisearch'
    keyword = 'good'
    page = int(page)
    #if(mode == smisearch):
    #    resultTup = callSMISearch(keyword)
    #elif(mode == dictsearch):
    #    resultTup = callDICTSearch(keyword)
    #elif(mode == websearch):
    #    resultTup = callWEBSearch(keyword)
    resultTup = callSearch(mode, keyword)
    showItemTup = resultTup[((page-1)*listSize):(page*listSize)] # �ѹ��� ������
    searchList = matchContentData(mode, keyword, showItemTup) # �������� ǥ���� ������ ����
    

    totalSize = len(resultTup) # �˻���� �� �׺������ �κ�
    pageCnt = totalSize / listSize
    if(totalSize % listSIze) != 0:
        pageCnt += 1
    pageList = range(1, pageCnt+1)

    tpl = loader.get_template('search/search.html') # ���ø� �ε�
    ctx = Context({
        'searchList' : searchList, # ������ ä���
        'keyword' : keyword,
        'mode' : mode,
        'pageList' : pageList,
        })

    html = tpl.render(ctx)
    return HttpResponse(html)

def callSearch(mode, keyword):
    if mode == "smisearch":
        rfunc = SubSearcher(keyword)
    elif mode == "dictsearch":
        rfunc = DictSearcher(keyword)
    elif mode == "websearch":
        rfunc = WebSearcher(keyword)

    searchTup = rfunc(keyword.encode('cp949'))
    return searchTup

def matchContentData(mode, keyword, listTup):
    "���ø��� ���� ������ ���� "
    ResultData = []
    if(mode == "smisearch"):
        for item in listTup:
            conTitle = item[0]
            conEng = item[1]
            conKor = item[2]
            ResultData.append(({'title':conTitle, 'eng':conEng, 'kor':conKor}))
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
        PreviewData = u"(������ ��� �ֽ��ϴ�)"
    
    # �����Ϳ��� Ű���忡 �ش��ϴ� �� �ҵ�ü�� ǥ��
    #strTitle = strTitle.replace(keyword, "<b>" + keyword + "</b>")
    PreviewData = PreviewData.replace(keyword, "<b>" + keyword + "</b>")

    return PreviewData

def makeTitle(title):
    strTitle = title
    strTitle = strTitle.replace(keyword, "<b>" + keyword + "</b>")
    return strTitle
