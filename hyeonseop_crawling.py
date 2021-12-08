## import 정보

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import re

## 기타 옵션

pd.set_option('display.unicode.east_asian_width', True)
re_title = re.compile('[^가-힣|a-z|A-Z ]')   # 정규 표현식

# 셀레니움 옵션.

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

## 변수 선언

url_list = []

df = pd.DataFrame()

## review xpath

# /html/body/div/div[3]/div[6]/div/ul/li[1]/dl/dt/a
# /html/body/div/div[3]/div[6]/div/ul/li[2]/dl/dt/a
# /html/body/div/div[3]/div[6]/div/ul/li[10]/dl/dt/a
# /html/body/div/div[3]/div[6]/div/ul/li[9]/dl/dt/a

# 리뷰페이지수
# /html/body/div/div[3]/div[6]/div/div[2]/a[1]
# /html/body/div/div[3]/div[6]/div/div[2]/a[2]
# /html/body/div/div[3]/div[6]/div/div[2]/a[3]

for x in range(10, 12):
    #10부터 34까지 있고 중간에 없는것도 있음
    for y in range(1, 20):
        ## 100개 마다
        for i in range(1,6):
            try:
                url = 'https://book.naver.com/category/index.naver?cate_code={}0{}0&tab=top100&list_type=list&sort_type=publishday&page={}'.format(x,y,i)
                driver.get(url)
                for j in range(1,21):
                    temp = driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[9]/ol/li[{}]/dl/dt/a'.format(j))
                    new_url = temp.get_attribute("href")
                    url_list.append(new_url)
            except:
                print('.', end='')
                break
                # print(len(url_list))
        try:
            for z in range(100):
                driver.get(url_list[z])
                titles = []
                writers = []
                reviews = []
                title = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div[1]/h2/a').text
                writer = driver.find_element_by_xpath('//*[@id="container"]/div[4]/div[1]/div[2]/div[2]/a[1]').text
                #리뷰 페이지 클릭
                #1개의 리뷰
                try:
                    for a in range(2,4):
                        ## 리뷰 30개만.
                        for b in range(1, 11):
                            driver.get(url_list[z].replace('book_detail', 'review'))
                            driver.find_element_by_xpath('/html/body/div/div[3]/div[6]/div/ul/li[{}]/dl/dt/a'.format(b)).click
                            time.sleep(0.5)
                            review = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[8]/div[1]/div/table[2]/tbody/tr/td[2]/div[1]/div/div/div[3]').text
                            titles.append(title)
                            reviews.append(review)
                            writers.append(writer)

                except:
                    print('.')  #print('리뷰가 없습니다.')
            df_review_100 = pd.DataFrame({'titles': titles, 'writers': writers, 'reviews':reviews})
            df_review_100.to_csv('./datasets/review_{}_{}_cate'.format(x,y))
        except:
            print('이 카테고리는 없습니다.')




