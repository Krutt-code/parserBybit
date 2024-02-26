from seleniumbase import Driver
from time import sleep

with Driver(uc=True) as driver:
    driver.get('https://ploshadka.net/kak-obnovit-python-na-ubuntu/')
    # driver.implicitly_wait(10)
    sleep(1)
    print('Прошла 1с')
    sleep(2)
    print(driver.find_element('h1').text)

