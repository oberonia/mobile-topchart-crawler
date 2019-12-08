from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome('E:\mobile-topchart-crawler\chromedriver\chromedriver.exe')

# csv에서 게임명을 복사
# 검색창에 검색
# 회사명이 일치하는 항목을 선택
# 용량 정보 복사해서 csv에 채워넣기

# csv에서 게임명을 복사
datafile = open(r'E:\mobile-topchart-crawler\uk.csv', encoding='utf-8')
reader = csv.reader(datafile)
next(reader)
next(reader)
next(reader) # to skip header

# 검색창에 검색
test_count = 0

for line in reader:
    print(line[1])
    driver.get('https://play.google.com/store/apps/category/GAME?hl=en_US')
    searchfield = driver.find_element_by_id('gbqfq')
    searchfield.send_keys(line[1])
    searchfield.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.title_contains(line[1]))

    # 회사명이 일치하는 항목을 선택
    company = driver.find_elements_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz[2]/div/div[2]/div/c-wiz/c-wiz/c-wiz/div/div[2]/div/c-wiz/div/div/div[2]/div/div/div[1]/div/div/div[2]/a/div")
    # company = driver.find_elements_by_class_name('KoLSrc')
    for item in company:
        if line[2] in item.text:
            print(item.text)
            # item.click()
            result = item.find_element_by_xpath('../../div[1]')
            result.click()
            break

# datafile.close()