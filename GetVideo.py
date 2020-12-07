# 按类别自动获取PronHub视频
# Author: Minenami
# Date: 2020/12/6
import time
from time import sleep

import requests
import re
import random
import os


COOKIE = "ua=2d6330f380f44ac20f3a02eed0958f66; platform_cookie_reset=pc; platform=pc; bs=dq6n3vxz9pjn6zxi6alrfnlw9qhm0wyw; ss=955475151461275352; fg_9d12f2b2865de2f8c67706feaa332230=11312.100000; _ga=GA1.2.869429813.1607171866; _gid=GA1.2.1095966900.1607171866; d_uidb=6d5bf1b1-44a0-4124-bc8a-a8e5628adfe2; d_uid=6d5bf1b1-44a0-4124-bc8a-a8e5628adfe2; fg_7133c455c2e877ecb0adfd7a6ec6d6fe=26386.100000; desired_username=Minenami%7Cpft1060773618%40gmail.com; expiredEnterModalShown=1; il=v1r9OT89ePrOdqHVF_U_sVTHM1tHAKqretR1-NoxedD44xNjE1MDIxNDA4b3pONVh6THFsUUdCczdPYUVBUW1CVHZVdVpJTzdqWmdKUUFkX3V4Qw..; _gat=1"
# 伪造User-Agent
UA = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"]
# 主机地址
HOST_URL = "https://cn.pornhub.com/"

CAT_LIST = {
    "日本人": "video?c=111",
    "女同": "video?c=27",
    "内射中出": "video?c=15",
    "色情日漫": "categories/hentai",
    "女性高潮": "video?c=502",
    "潮吹": "video?c=69",
    "手淫": "video?c=22",
    "CosPlay": "video?c=241",
    "舔屄": "video?c=131"
}
catName = None
localUrl = None


def getVideoList(cat, page):
    headers = {
        "Cookie": COOKIE,
        "User-Agent": getRandomUA()
    }
    url = HOST_URL + cat + "&page=" + page
    response = requests.get(url, headers=headers, timeout=10).text
    # print(response)
    tempList = re.findall('<a href="/view_video.php\?viewkey=(.*?)" title="', response)
    # 对数组进行去重处理
    videoList = unique(tempList)
    # print(videoList)
    return videoList


def downloadVideo(url, title):
    headers = {
        "Cookie": COOKIE,
        "User-Agent": getRandomUA()
    }
    try:
        print("当前正在获取:" + title)
        response = requests.get(url, headers=headers, stream=True)
        contentSize = int(response.headers['content-length'])
        dataCount = 0
        with open(localUrl + catName + "\\" + title + ".mp4", "wb") as file:
            # 下载时实时显示进度与下载速度
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                dataCount = dataCount + len(data)
                speed = (dataCount / contentSize) * 100  # 计算下载的进度
                print("\r 文件下载进度：%d%%(%d/%d) - %s" % (speed, dataCount, contentSize, title + ".mp4"), end=" ")

        print("\n" + title + "下载完成！")
        sleep(2)
        return True
    except:
        print("获取失败。。。")

    return False


def unique(old_list):
    # 数组去重
    newList = []
    for x in old_list:
        if x not in newList:
            newList.append(x)
    return newList


def getRandomUA():
    # 从UA列表中获取一个随机UA
    return UA[random.randint(0, len(UA) - 1)]


def getDetailPage(videoParm):
    headers = {
        "Cookie": COOKIE,
        "User-Agent": getRandomUA()
    }
    url = HOST_URL + "view_video.php?viewkey=" + str(videoParm)
    response = requests.get(url, headers=headers, timeout=20).text
    resUrl = re.findall('<a class="downloadBtn greyButton" target="_blank" rel="noopener noreferrer" href="(.*?)" download="', response)[0]
    title = re.findall('<title>(.*?) - Pornhub.com</title>', response)[0]
    # print(resUrl)
    return resUrl, title


def main():
    global localUrl
    localUrl = input("输入本地储存根目录文件夹：")
    # 获取类别下的各个分页
    print("类别列表：")
    for index, key in enumerate(CAT_LIST):
        print(str(index) + "、" + key + "\t", end="")
    num = int(input("\n输入类别对应序号："))
    cat = None
    global catName
    for index, key in enumerate(CAT_LIST):
        if index == num:
            cat = CAT_LIST[key]
            catName = key
            break

    # print("debug:cat===>" + cat)
    if not os.path.exists(localUrl + catName):
        # 创建相应类别文件夹目录
        os.makedirs(localUrl + catName)
        print(catName + "=>文件夹创建成功")
    else:
        print(catName + "=>文件夹已存在")

    page = input("输入分页：")
    videoList = getVideoList(cat, page)

    # 启动计时
    timeStart = time.time()

    # 循环视频数组进行爬取
    totalCount = 0
    for index, value in enumerate(videoList):
        print("当前下载第" + str(index + 1) + "个视频")
        _url, _title = getDetailPage(value)
        if downloadVideo(_url, _title):
            totalCount += 1

    # 结束计时
    totalTime = time.time() - timeStart
    print("视频已下载完毕，共下载" + str(totalCount) + "个视频，总用时：" + str(totalTime) + "s")


main()