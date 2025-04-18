import time
import datetime

def ConversionDay(passDay):
    # 先獲得時間數組格式的日期
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = passDay))
    # 轉換為時間戳:
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    # 轉換為其他字符串格式:
    #otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
    otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
    print(otherStyleTime)
    return otherStyleTime

def getDate(dataTime):
    #統一將更新日期轉換成 "2019-12-17" 格式
    """ 可能出現之格式
    今天 00:02
    昨天 09:32
    前天 11:29
    04月08号
    2017-09-20
    """
    print("source : ",dataTime)
    #取得現在時間
    now = datetime.datetime.now()
    nowTime = now.strftime("%Y-%m-%d")
    print("nowTime =",nowTime)
    totalStr = ""
    if(dataTime[:2] == "今天"):
        print("0")
        return nowTime
    elif(dataTime[:2] == "昨天"):
        print("-1")
        ConversionDay(1)
    elif(dataTime[:2] == "前天"):
        print("-2")
        ConversionDay(2)
    elif(dataTime[:2] != "20"):
        a = "{}-{}-{}".format(nowTime[:4],dataTime[0:2],dataTime[3:5])
        #將其轉換為時間數組
        print(a)
        timeArray = time.strptime(a,"%Y-%m-%d")
        print(timeArray)
        newTime = "{}-{}-{}".format(timeArray[0],timeArray[1],timeArray[2])
        print(newTime)
        print("-9")
        return newTime
    else:
        return dataTime
