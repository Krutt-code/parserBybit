from seleniumbase import Driver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
from time import sleep

try:
    from json_handler import JsonHandler
except:
    from .json_handler import JsonHandler

import logging

class ParserBybit:
    def __init__(self) -> None:
        self.data = {}

    def __get_data(self, driver) -> list:
        soup = BS(driver.page_source, 'lxml')

        for item in soup.find_all('tr')[1:]:
            if item.find_all("span")[1].text.strip() != '/USDT':
                continue

            name = item.find_all("span")[0].text.strip()

            try: 
                price = float(item.find_all('td')[1].text.strip().replace(',', ''))
            except:
                price = float(item.find_all('td')[1].text.strip())

            self.data.update(
                {
                    name: price
                }
            )

    def __get_count_pages(self, driver) -> int:
        box = driver.find_element(By.CLASS_NAME, 'markets__box')
        return int(box.find_elements(By.TAG_NAME, 'li')[-3].get_attribute('title'))

    def __next_page(self, driver, page) -> None:
        box = driver.find_element(By.CLASS_NAME, 'markets__box')
        ul = box.find_elements(By.TAG_NAME, 'ul')[-1]
        for a in ul.find_elements(By.TAG_NAME, 'a'):
            if str(page) in a.text.strip():
                a.click()
                break

    def run(self) -> dict:
        url = 'https://www.bybit.com/ru-RU/markets/overview'

        logger = logging.getLogger('parser')

        while True:
            try:
                with Driver(uc=True) as driver:
                    logger.info('Начинаю сбор данных')
                    driver.get(url)
                    driver.implicitly_wait(10)
                    
                    page_count = self.__get_count_pages(driver=driver)
                    # logger.info(' - Страница 1 собирается')
                    for page in range(2, page_count + 1):
                        sleep(2)
                        self.__get_data(driver=driver)
                        self.__next_page(driver=driver, page=page)
                        # logger.info(f' - Страница {page} собрана')

                # data['data'] = data_m
                logger.info('Сбор данных завершен')        
                return self.data
            except Exception as e:
                logger.error(f'Ошибка при сборе данных: {e}')
                sleep(10)
                logger.info('Пробую еще раз...')

if __name__ == '__main__':
    pars = ParserBybit()

    JsonHandler('json.json').write_json(pars.run())
    