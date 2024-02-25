from seleniumbase import Driver

with Driver() as driver:
    driver.get('https://ploshadka.net/kak-obnovit-python-na-ubuntu/')
    driver.implicitly_wait(10)
    
    print(driver.find_element('h1').text)