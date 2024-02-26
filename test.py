# from seleniumbase import Driver
# from time import sleep

# with Driver() as driver:
#     driver.get('https://ploshadka.net/kak-obnovit-python-na-ubuntu/')
#     # driver.implicitly_wait(10)
#     sleep(1)
#     print('Прошла 1с')
#     sleep(2)
#     print(driver.find_element('h1').text)

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--headless')

with webdriver.Chrome(options=options_chrome) as driver:
    driver.get('https://ploshadka.net/kak-obnovit-python-na-ubuntu/')
    # driver.implicitly_wait(10)
    sleep(1)
    print('Прошла 1с')
    sleep(2)
    print(driver.find_element(By.TAG_NAME, 'h1').text)