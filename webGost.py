import urllib.request as req
import requests
import os
import changTime
import datetime
#ifttt傳送line訊息(最新漫畫)
def send_ifttt(listUrl):   # 定義函式來向 IFTTT 發送 HTTP 要求
    if(len(listUrl) == 1):
        listUrl.append("")
        listUrl.append("")
    elif (len(listUrl) == 2):
        listUrl.append("")
    apiURL = ('https://maker.ifttt.com/trigger/{evt}' +
       '/with/key/{key}?value1={val1}&value2={val2}&value3={val3}').format(
    evt="line",
    key="YourKey",
    val1= listUrl[0],
    val2= listUrl[1],
    val3= listUrl[2])
    r = requests.get(apiURL)
    if r.text[:5] == 'Congr':  # 回應的文字若以 Congr 開頭就表示成功了
        print('已傳送 ('+str(listUrl[0])+','+str(listUrl[1])+','+str(listUrl[2])+') 到 Line')
    return r.text

#取得漫畫網址
def getData(lastOpen,url,type):
    #假裝使用者 - 並加上cookie
    request = req.Request(url, headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    })

    #發送網址
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    #解析資料
    import bs4
    root = bs4.BeautifulSoup(data,"html.parser")
    #網頁title - 漫畫名稱
    name = root.title.string
    print(name)
    valNumberFull = ""
    
    #最新更新時間
    mydivs = root.find_all("span",class_ = "detail-list-title-3")
    valueTime = mydivs[0]
    timeVal = valueTime.contents[0]
    lastTime = changTime.getDate(timeVal)
    print("timeVal : ",lastTime)
    
    #判斷更新時間>最後打開時間
    #year EX:  xx19-12-20
    lastOpenList = lastOpen.split("-")
    onlieTimeList = lastTime.split("-")
    lacalTime = int(lastOpenList[0])*10000+int(lastOpenList[1])*100+int(lastOpenList[2]) 
    onlieTime = int(onlieTimeList[0])*10000+int(onlieTimeList[1])*100+int(onlieTimeList[2])
    print("lacalTime =",lacalTime)
    print("onlieTime = ",onlieTime)
    if(lacalTime > onlieTime):            
        return None
    else:
        #更新開啟日期
        now = datetime.datetime.now()
        nowTime = now.strftime("%Y-%m-%d")
        #寫入今天的時間
        with open("dateInfo.txt",mode = "r+",encoding="utf-8")as file3:
            file3.seek(5)
            file3.write(nowTime)
    #尋找 class div 標籤
    titles = root.find_all("li")
    for title in titles:
        #如果有A
        if title.a != None: 
            print(title.a.string)
            valNumberFull = title.a.string
            break
    
    #连载中
    titles = root.find_all("div",class_ = "detail-list-title")
    for title in titles:
        #如果有span
        if title.span != None: 
            print(title.span.string)
        print("=========")
    #找到內文是"第xxx"话"
    if(type == 0):
        nextLink = root.find("a",string = valNumberFull)
    elif(type == 1):
        #抓更新的最新一集漫畫link
        nextLink = root.find("a",class_ = "detail-list-title-2")
    #丟出上一頁網址
    allData = "{} 漫畫:{},最後更新{}".format(nextLink["href"],name,timeVal)
    return allData
    #return nextLink["href"]

type = 1
#list1 = {pageUrl1,pageUrl2,pageUrl3}
list1 = []
lastOpen = ""
#取得漫畫網址
with open("dateInfo.txt",mode = "r",encoding="utf-8")as fileUrl:
    dataUrl = fileUrl.readlines()
    for line in dataUrl:
        if(line[:4]=="last"): 
            lastOpen = line[5:15]
            print("lastOpen =",lastOpen)
        elif(line[:4]!="===="):
            list1.append(line)
print("line1 = ",list1)
list2 = []

for index in list1:
    print("==========================\n")
    #print("https://www.manhuaren.com" + getData(i,type))
    #list2[count] = "https://www.manhuaren.com" + getData(lastOpen,index,type)
    newUrl = getData(lastOpen,index,type)
    if(newUrl != None):
        list2.append("https://www.manhuaren.com" + newUrl)
print("list2 = ", list2)    

if(len(list2)):
    #發送line訊息
    #ret = send_ifttt(list2)  #傳送 HTTP 請求到 IFTTT
    #print('IFTTT 的回應訊息：',ret)     # 輸出 IFTTT 回應的文字
    
    #建立.bat檔
    str4 = ""
    for item in list2:
        list3 =[]
        st1 = str(item)
        list3 = st1.split()
        str3 = "\nstart chrome --incognito " + "\"" + list3[0] + "\""
        print("list3[0] = ",str3)
        str4 += str3
    print("str4 = ",str4)

    with open("E:/Users/123/Desktop/comic.bat",mode = "w",encoding="utf-8") as file2:
        file2.write(str4)

os.system("pause")
