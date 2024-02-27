from aiogram import Bot, Dispatcher
from .manage_data import DataM
from time import sleep
from datetime import datetime, timedelta

import logging
import asyncio

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
        for mode, item in data.items():

            if not item:
                continue

            message = f'mode {mode}\n'

            for index, item in enumerate(item.items()):
                if index % 10 == 0:
                    message += '```KRIPTA\n'

                name, item = item
                item1, item2 = item.items()
                time1, price1 = item1
                time2, price2 = item2
                change = round(((price2 - price1) / price2) * 100, 1)
                message += f'{name}/USDT {change}%: \n{":".join(time1.split()[-2:-4:-1][::-1])} = {price1}\n{":".join(time2.split()[:-3:-1][::-1])} = {price2}\n{"#"*30}\n'
 
                if index % 10 == 9:
                    message += '```'
                    await self.bot.send_message(self.canal_id, message)
                    message = ''

            if message[:-4:-1] != '```':
                message += '```'
                await self.bot.send_message(self.canal_id, message)

        logger.info('Сообщение успешно отправлено')

    async def main(self):
        while True:
            # Проверяем условие
            time = self.__get_time()
            data = DataM(config=self.config, time=time).run()
            # print('\n'.join(data.values()))
            if any(i for i in data.values()):
                self.bot = Bot(token=self.config.tg_bot.token,
                parse_mode='Markdown')
                await self.__send_message_to_user(data=data)
            else:
                logger.info('Нет данных для отправки')
            
            await asyncio.sleep(self.__get_difference_seconds(time=time)) 

    def run(self):
        asyncio.run(self.main())