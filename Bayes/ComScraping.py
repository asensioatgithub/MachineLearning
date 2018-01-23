'''
爬取电影《战狼2》评论
'''

import urllib
from bs4 import BeautifulSoup
import re
import time
from os import mkdir
import random
import http.cookiejar


index = {'allstar10':0, 'allstar20':0, 'allstar30':0, 'allstar40':0, 'allstar50':0}


'''
如果不登录只能查看前10页评论，所以需要使用模拟登陆豆瓣获取cookie
'''

loginurl = "https://www.douban.com/accounts/login"
cookie = http.cookiejar.CookieJar()
# 实例化一个全局opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)

data={}
data["form_email"]="17623084391"
data["form_password"]="maohao4391"
data["source"]= "index_nav"

# 从首页提交登录，获取cookie
response = opener.open(loginurl,urllib.parse.urlencode(data).encode("utf-8"))

# 验证成功跳转至登录页
if response.geturl() == "https://www.douban.com/accounts/login":
    html = response.read().decode()
    print(html)

# 验证码图片地址
    imgurl = re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
    if imgurl:
        url = imgurl.group(1)

        # 将图片保存至同目录下
        res = urllib.request.urlretrieve(url, "v.jpg")

        # 获取captcha-id参数
        captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)

        if captcha:
            vcode = input("请输入图片上的验证码：") # 在输出的页面中点击验证码网址查看验证码
            data["captcha-solution"] = vcode
            data["captcha-id"] = captcha.group(1)
            data["user_login"] = "登录"

            # 提交验证码验证
            response = opener.open(loginurl, urllib.parse.urlencode(data).encode("utf-8"))

            #登录成功跳转至首页
            if response.geturl() == "https://www.douban.com/":
                print ("登录成功")




'''
以防网站机器人检测造成 "403 Forbidden"
'''
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]


def htmlScraping():
    try:
        mkdir('comments')
    except:
        pass
    print('Scraping...')
    for i in range(100): #  20*100 comments
        url = 'https://movie.douban.com/subject/26363254/comments?start=%d&limit=20&sort=new_score&status=P&percent_type=' % (i * 20)
        # randdom_header = random.choice(my_headers)
        # req = urllib.request.Request(url)
        # req.add_header("User-Agent", randdom_header)
        # req.add_header("Host", "movie.douban.com")
        # req.add_header("Referer", "https://movie.douban.com/")
        # req.add_header("GET", url)
        # resp = urllib.request.urlopen(req)
        resp = opener.open(url)
        html_data = resp.read().decode('utf-8')
        # print(html_data)
        commScraping(html_data)
        print('Scraping %d comments'%((i+1)*20))
        time.sleep(1)

def commScraping(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')
    #print(comment_div_lits)
    eachCommentList = [];

    for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:
            star = re.findall(r'allstar\d{2}', str(item))
            # 爬虫到一半的时候一直报错"list out of range", 百思不得其解，后来才发现有位老哥写了评论却没有评分...:)
            if(len(star) == 0):
                continue
            if(int(re.findall(r'\d{2}', str(star))[0])>30):
                label = 1
            else:
                label = 0
            comTxt = open('comments/%d_%d.txt'%(label, index[star[0]]), 'w')
            index[star[0]] += 1
            # print(item.find_all('p')[0].string)
            # 评论内容导致各种字符编码错误，对于有错的评论索性跳过...
            try:
                comTxt.write(item.find_all('p')[0].string)
            except:
                index[star[0]] -= 1
                pass
            comTxt.close()
            #print(star[0])
            #eachCommentList.append(item.find_all('p')[0].string)
    # print(eachCommentList)

htmlScraping()





# https://movie.douban.com/subject/26363254/comments?start=20&limit=20&sort=new_score&status=P&percent_type=