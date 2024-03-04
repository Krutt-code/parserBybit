from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from datetime import datetime, timedelta
from os import path
from time import sleep

from .manage_data import DataM
from .create_schedule import CreateSchedule

import logging
import asyncio
import json

logger = logging.getLogger('parser')
class BotBybit:
    def __init__(self, config) -> None:
        self.config = config
        self.canal_id = self.config.tg_bot.canal_id

    def __get_time(self):
        date = datetime.now() + timedelta(hours=3)
        return date.strftime('%Y %m %d %H %M %S')

    def __get_difference_seconds(self, time):
        new_date = self.__get_time()
        date = int((((datetime(*map(int, new_date.split())))) - (datetime(*map(int, time.split())))).total_seconds()) - 1
        return (self.config.data.period_time * 60) - date

    async def __send_message_to_user(self, data: dict) -> None:
        bot = Bot(token=self.config.tg_bot.token,
                parse_mode='Markdown')
        for mode, item in data.items():

            if not item:
                continue

            for index, item in enumerate(item.items()):
                sleep(0.5)

                if (index+1) % 20 == 0:
                    sleep(40)

                message = f'mode {mode}\n```KRIPTA\n'

                name, item = item
                item1, item2 = item.items()
                time1, price1 = item1
                time2, price2 = item2
                change = round(((price2 - price1) / price2) * 100, 1)
                message += f'{name}/USDT {change}%: \n{":".join(time1.split()[-3:-1])} = {price1}\n{":".join(time2.split()[-3:-1])} = {price2}\n'
 
                message += '```'

                data_path = path.join('bots', self.config.data.data_file_name)
                try:
                    with open(data_path) as file:
                        CreateSchedule(symbol=name, data=json.load(file)).run()
                except Exception as e:
                    logger.error(e)

                try:
                    await bot.send_photo(self.canal_id, FSInputFile("graph_image.png"), caption=message)
                except Exception as e:
                    logger.error(e)
                    sleep(20)
                    


        sleep(2)

        logger.info('Сообщение успешно отправлено')

    async def main(self):
        while True:
            # Проверяем условие
            time = self.__get_time()
            data = DataM(config=self.config, time=time).run()
            # print('\n'.join(data.values()))
            if any(i for i in data.values()):
                await self.__send_message_to_user(data=data)
            else:
                logger.info('Нет данных для отправки')
            
            await asyncio.sleep(self.__get_difference_seconds(time=time)) 

    def run(self):
        asyncio.run(self.main())