from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome(
    'E:\mobile-topchart-crawler\chromedriver\chromedriver.exe')

# csv에서 게임명을 복사
# 검색창에 검색
# 회사명이 일치하는 항목을 선택
# 용량 정보 복사
# csv에 채워넣기

# csv에서 게임명을 복사
datafile = open(r'E:\mobile-topchart-crawler\uk.csv', encoding='utf-8')
reader = csv.reader(datafile)
next(reader)
next(reader)
next(reader)  # to skip header

resultfile = open(r'E:\mobile-topchart-crawler\uk-result.csv',
                  'w', encoding='utf-8')
storename = ['Game Name', 'Google Play']
writer = csv.DictWriter(resultfile, fieldnames=storename)
writer.writeheader()

# 검색창에 검색
test_count = 0

for line in reader:
    gamename = line[5]
    print(gamename)
    driver.get('https://play.google.com/store/apps/category/GAME')
    searchfield = driver.find_element_by_id('gbqfq')
    searchfield.send_keys(gamename)
    searchfield.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.title_contains(gamename))

    # 회사명이 일치하는 항목을 선택
    company_xpath = '//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/c-wiz/c-wiz/c-wiz/div/div[2]/div/c-wiz/div/div/div[2]/div/div/div[1]/div/div/div[2]/a/div'
    company = driver.find_elements_by_xpath(company_xpath)
    companyname = line[6]
    for item in company:
        if companyname.lower() in item.text.lower():
            print(item.text)
            result = item.find_element_by_xpath(
                company_xpath+'/ancestor::div[@class="kCSSQe"]/div[1]/a/div')
            result.click()

            # 용량 정보 복사
            # TODO: size | 크기 둘 다 되도록
            app_size_xpath = '(.//*[normalize-space(text()) and normalize-space(.)=("크기")])[1]/following::div[1]'
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, app_size_xpath)))
            app_size = driver.find_element_by_xpath(app_size_xpath).text
            print(app_size)
        else:
            print('Can not find that game: ' +
                  gamename+' or developers: '+companyname)
            app_size = 'N/A'  # 완전 일치 게임을 못찾았으면 N/A 반환

        # csv에 채워넣기
        writer.writerow({'Game Name': gamename, 'Google Play': app_size})
        break

# datafile.close()
