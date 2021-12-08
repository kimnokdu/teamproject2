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
import html5lib

## 기타 옵션

pd.set_option('display.unicode.east_asian_width', True)
re_title = re.compile('[^가-힣|a-z|A-Z ]')   # 정규 표현식

# 셀레니움 옵션.

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
# 셀레니움 모바일 옵션 데스크탑 옵션
# options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

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
    for y in range(1, 10):
        # 1부터 존재함 & 변수 초기화
        # 2자리 숫자도 붙이는 방법을 강구해야함
        titles = []
        writers = []
        reviews = []
        url_list = []
        for i in range(1, 6):
            ## 100개 마다
            url = 'https://book.naver.com/category/index.naver?cate_code={}00{}0&tab=top100&list_type=list&sort_type=publishday&page={}'.format(x,y,i)
            driver.get(url)
            for j in range(1,21):
                temp = driver.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[9]/ol/li[{}]/dl/dt/a'.format(j))
                new_url = temp.get_attribute("href")
                url_list.append(new_url)
            # print(len(url_list))

        for z in range(100):
            driver.get(url_list[z])

            title = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div[1]/h2/a').text
            writer = driver.find_element_by_xpath('//*[@id="container"]/div[4]/div[1]/div[2]/div[2]/a[1]').text
            #리뷰 페이지 클릭
            #1개의 리뷰
            for a in range(1,4):
                review_page = url_list[z].replace('book_detail', 'review') + '&page={}'.format(a)
                driver.get(review_page)
                for b in range(1, 11):
                    # driver.find_element_by_xpath('/html/body/div/div[3]/div[6]/div/ul/li[{}]/dl/dt/a'.format(b)).click
                    # 클릭이 안먹힘
                    elem = driver.find_element_by_xpath('/html/body/div/div[3]/div[6]/div/ul/li[{}]/dl/dt/a'.format(b))
                    temp_url = elem.get_attribute('href') ## 리뷰 페이지마다 돌아가는 임시 url
                    driver.get(temp_url)
                    time.sleep(4)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    soup = soup.findAll(class_="se-main-container")
                    review = ''
                    sentence = ''
                    for i in soup:
                        sentence = i.get_text()
                        sentence = re.compile('[^가-힣 ]').sub(' ', sentence)
                        review += sentence
                    titles.append(title)
                    reviews.append(review)
                    writers.append(writer)
                    print(review[0:10])
                    print(title)
                    print(writer)
                    driver.back()
                    # except:
                    #     print('{}번째 리뷰가 없습니다.'.format(b))
                    #     break
        df_review_100 = pd.DataFrame({'titles': titles, 'writers': writers, 'reviews':reviews})
        df_review_100.to_csv('./datasets/review_{}_{}_cate'.format(x,y))




